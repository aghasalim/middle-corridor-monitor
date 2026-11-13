"""List Sentinel-1 GRD passes over Alat on Microsoft Planetary Computer (anonymous) and read the AOI window.

GRD is in radar geometry with ground control points (GCPs). We map our UTM grid to image row/col
through a thin-plate spline on the GCPs (exact at the GCPs; GDAL's polynomial fit was off by up to
~200 px), read only that window over HTTP, and resample it onto the grid.

Each GCP sits at its own terrain height (0 to >1000 m here), and a point at height z is imaged
z / tan(incidence) nearer to the radar. Interpolating between such GCPs misplaces the sea surface by
up to ~160 m, differently for every frame. So every GCP is first moved to one common height, the
Caspian surface, which makes passes of all years and orbits line up.
"""
import time
from concurrent.futures import ThreadPoolExecutor

import numpy as np
import pandas as pd
import planetary_computer
import pystac_client
import rasterio
from rasterio.control import GroundControlPoint
from rasterio.transform import GCPTransformer
from rasterio.windows import Window
from scipy.ndimage import map_coordinates

from . import aoi

STAC = "https://planetarycomputer.microsoft.com/api/stac/v1"
COLLECTION = "sentinel-1-grd"
SCENES_CSV = aoi.SAR_DIR / "scenes.csv"
SCENE_CACHE = aoi.CACHE / "scenes"
SEA_HEIGHT_M = -28.0  # Caspian surface relative to the GCP height datum (checked against Sentinel-2, see SAR_METHOD)
INC_NEAR_DEG, INC_FAR_DEG = 29.9, 45.9  # IW swath incidence, near to far range; linear across columns (good to ~1 deg)
GRD_SPACING_M = 10.0
STEP = 50  # coarse grid step (px) for the row/col mapping; it is smooth, so 500 m is plenty


def collection_extent():
    col = pystac_client.Client.open(STAC).get_collection(COLLECTION)
    return [str(t) for t in col.extent.temporal.intervals[0]]


def search_passes(start="2019-01-01", end=None):
    """One row per pass (platform + absolute orbit); a pass can be split over two frames."""
    end = end or time.strftime("%Y-%m-%d", time.gmtime())
    geom = {"type": "Polygon", "coordinates": [aoi.grid_bbox_lonlat()]}
    client = pystac_client.Client.open(STAC)
    rows = []
    for it in client.search(collections=[COLLECTION], intersects=geom, datetime=f"{start}/{end}").items():
        p = it.properties
        if p.get("sar:instrument_mode") != "IW" or "vv" not in it.assets:
            continue
        rows.append({
            "item_id": it.id, "datetime": p["datetime"], "platform": p["platform"].upper(),
            "abs_orbit": p["sat:absolute_orbit"], "rel_orbit": p["sat:relative_orbit"],
            "direction": p["sat:orbit_state"], "pols": "+".join(sorted(k for k in ("vv", "vh") if k in it.assets)),
            "vv": it.assets["vv"].href, "vh": it.assets["vh"].href if "vh" in it.assets else "",
        })
    df = pd.DataFrame(rows).sort_values("datetime")
    g = df.groupby(["platform", "abs_orbit"], sort=False)
    passes = g.agg(
        scene_id=("item_id", "first"), item_ids=("item_id", "+".join), datetime=("datetime", "first"),
        rel_orbit=("rel_orbit", "first"), direction=("direction", "first"), pols=("pols", "first"),
        vv=("vv", "|".join), vh=("vh", "|".join),
    ).reset_index().sort_values("datetime").reset_index(drop=True)
    return passes


def _rowcol_fields(src):
    """Image row/col of every grid pixel, from the GCPs (thin-plate spline) on a coarse grid, then bilinear."""
    ys = np.arange(0, aoi.H + STEP, STEP)
    xs = np.arange(0, aoi.W + STEP, STEP)
    cc, rr = np.meshgrid(xs, ys)
    lon, lat = aoi.pixel_to_lonlat(rr - 0.5, cc - 0.5)  # grid node (r, c) = top-left corner of pixel
    gcps = []
    for g in src.gcps[0]:
        inc = np.radians(INC_NEAR_DEG + (INC_FAR_DEG - INC_NEAR_DEG) * g.col / src.width)
        dcol = (g.z - SEA_HEIGHT_M) / (np.tan(inc) * GRD_SPACING_M)  # where this lon/lat would be imaged at sea height
        gcps.append(GroundControlPoint(row=g.row, col=g.col + dcol, x=g.x, y=g.y, z=SEA_HEIGHT_M))
    with GCPTransformer(gcps, tps=True) as gt:
        r, c = gt.rowcol(lon.ravel(), lat.ravel(), op=lambda v: v)
    r = np.asarray(r, float).reshape(rr.shape)
    c = np.asarray(c, float).reshape(rr.shape)
    yi, xi = np.meshgrid((np.arange(aoi.H) + 0.5) / STEP, (np.arange(aoi.W) + 0.5) / STEP, indexing="ij")
    return map_coordinates(r, [yi, xi], order=1), map_coordinates(c, [yi, xi], order=1)


def read_window(href):
    """Amplitude (DN, float32) of one GRD band on the working grid; 0 where the frame has no data."""
    with rasterio.open(planetary_computer.sign(href)) as src:
        R, C = _rowcol_fields(src)
        r0, r1 = max(int(R.min()) - 2, 0), min(int(R.max()) + 3, src.height)
        c0, c1 = max(int(C.min()) - 2, 0), min(int(C.max()) + 3, src.width)
        if r1 <= r0 or c1 <= c0:
            return np.zeros((aoi.H, aoi.W), np.float32)
        a = src.read(1, window=Window(c0, r0, c1 - c0, r1 - r0)).astype(np.float32)
    out = map_coordinates(a, [R - r0, C - c0], order=1, mode="constant", cval=0.0)
    # bilinear next to no-data (0) gives a darkened rim; drop any pixel whose nearest source pixel is 0
    near = map_coordinates(a, [R - r0, C - c0], order=0, mode="constant", cval=0.0)
    out[near == 0] = 0
    return out


def fetch_pass(p, tries=4):
    """Read (or load from cache) one pass. Returns {'vv': uint16 array, 'vh': ...}."""
    f = SCENE_CACHE / f"{p['scene_id']}.npz"
    if f.exists():
        return dict(np.load(f))
    out = {}
    for pol in ("vv", "vh"):
        hrefs = [h for h in str(p[pol]).split("|") if h and h != "nan"]
        if not hrefs:
            continue
        img = np.zeros((aoi.H, aoi.W), np.float32)
        for href in hrefs:  # two frames of one pass: take the larger value, so one frame's dark border noise loses
            for k in range(tries):
                try:
                    a = read_window(href)
                    break
                except Exception:
                    if k == tries - 1:
                        raise
                    time.sleep(3 * 2 ** k)
            img = np.maximum(img, a)
        out[pol] = np.clip(np.rint(img), 0, 65535).astype(np.uint16)
    SCENE_CACHE.mkdir(parents=True, exist_ok=True)
    tmp = f.with_suffix(".tmp.npz")
    np.savez_compressed(tmp, **out)
    tmp.replace(f)
    return out


def fetch_all(passes, workers=3):
    """Download every pass into the cache; returns passes with 'status' and 'valid_frac' columns."""
    def one(p):
        try:
            d = fetch_pass(p)
            return "ok", float((d["vv"] > 0).mean())
        except Exception as e:  # report, don't hide
            return f"FAILED: {type(e).__name__}: {str(e)[:150]}", 0.0

    env = rasterio.Env(GDAL_DISABLE_READDIR_ON_OPEN="EMPTY_DIR", GDAL_HTTP_MAX_RETRY=3, GDAL_HTTP_RETRY_DELAY=2,
                       GDAL_HTTP_TIMEOUT=60, CPL_VSIL_CURL_ALLOWED_EXTENSIONS=".tiff,.tif")
    res = []
    with env, ThreadPoolExecutor(workers) as ex:
        for i, r in enumerate(ex.map(one, [p for _, p in passes.iterrows()])):
            res.append(r)
            if i % 25 == 0:
                print(f"fetched {i + 1}/{len(passes)}  {r[0][:60]}", flush=True)
    passes = passes.copy()
    passes["status"] = [r[0] for r in res]
    passes["valid_frac"] = [round(r[1], 4) for r in res]
    return passes


if __name__ == "__main__":
    import sys
    t = time.time()
    print("collection extent:", collection_extent())
    ps = search_passes(*(sys.argv[1:3]))
    print(len(ps), "passes;", ps.groupby(ps.datetime.str[:4]).size().to_dict())
    ps = fetch_all(ps)
    ps.drop(columns=["vv", "vh"]).to_csv(SCENES_CSV, index=False)
    print(ps.status.str[:6].value_counts().to_dict(), f"{time.time() - t:.0f} s")


def missing_at_source(scenes):
    """Passes that the Copernicus catalogue lists over the port but Planetary Computer does not hold.

    Same query as research/s1_revisit.py (IW_GRDH_1S products containing the port point, no login).
    """
    import requests
    base = "https://catalogue.dataspace.copernicus.eu/odata/v1/Products"
    have = {(r.platform[-2:], int(r.abs_orbit)) for r in scenes.itertuples()}
    rows = []
    for year in range(2019, time.gmtime().tm_year + 1):
        flt = ("Collection/Name eq 'SENTINEL-1' and Attributes/OData.CSC.StringAttribute/any(att:att/Name eq 'productType' "
               "and att/OData.CSC.StringAttribute/Value eq 'IW_GRDH_1S') and "
               "OData.CSC.Intersects(area=geography'SRID=4326;POINT(49.4465 39.9742)') and "
               f"ContentDate/Start ge {year}-01-01T00:00:00.000Z and ContentDate/Start lt {year + 1}-01-01T00:00:00.000Z")
        r = requests.get(base, params={"$filter": flt, "$select": "Name", "$top": 1000}, timeout=120)
        r.raise_for_status()
        names = sorted({n["Name"] for n in r.json()["value"] if "_COG" not in n["Name"]})
        seen = set()
        for n in names:
            key = (n[1:3], int(n.split("_")[6]))  # e.g. ('1A', 25278)
            if key in seen:
                continue
            seen.add(key)
            rows.append({"year": year, "name": n, "on_planetary_computer": key in have})
        time.sleep(0.5)
    df = pd.DataFrame(rows)
    out = aoi.ROOT / "outputs" / "tables"
    df[~df.on_planetary_computer].to_csv(out / "sar_missing_at_source.csv", index=False)
    summary = df.groupby("year").on_planetary_computer.agg(copernicus_passes="size", on_planetary_computer="sum")
    summary.to_csv(out / "sar_source_coverage.csv")
    return summary
