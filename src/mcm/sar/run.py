"""Alat ship-count pipeline: cached scenes -> stacks -> backgrounds -> detections -> tables.

    python -m mcm.sar.fetch 2019-01-01      # download (cached)
    python -m mcm.sar.run                   # detect + tables
    python -m mcm.sar.report                # figures + hand-labelling kit

Counts are UNVALIDATED detector output ("bright blobs on water"), not a measurement of traffic.
"""
import hashlib
import time

import numpy as np
import pandas as pd
from scipy.spatial import cKDTree

from . import aoi, detect, fetch

DET_CSV = aoi.SAR_DIR / "detections.csv"
TABLES = aoi.ROOT / "outputs" / "tables"
MIN_COVER = 0.999        # share of zone pixels that must have data for a pass to be counted
BG_HALF_WINDOW_DAYS = 365
NODATA = np.int16(-32768)


def zone_setup():
    """Zone raster cropped to its bounding box: (zones dict, crop slices, zone raster crop)."""
    zones = aoi.load_zones()
    zr = aoi.zone_raster(zones)
    rows, cols = np.nonzero(zr)
    pad = detect.BLOCK
    sl = (slice(max(rows.min() - pad, 0), min(rows.max() + pad, aoi.H)),
          slice(max(cols.min() - pad, 0), min(cols.max() + pad, aoi.W)))
    return zones, sl, zr[sl]


def load_scene_db(scene_id, sl=(slice(None), slice(None))):
    d = np.load(fetch.SCENE_CACHE / f"{scene_id}.npz")
    return {p: detect.smooth_db(d[p])[sl] for p in ("vv", "vh") if p in d}


def build_stack(scene_ids, sl, zmask, tag):
    """(n_scenes, n_zone_pixels) int16 of dB x 100 per polarisation, cached on disk; plus zone coverage per scene."""
    key = hashlib.md5((",".join(scene_ids) + str(sl) + str(zmask.sum())).encode() + zmask.tobytes()).hexdigest()[:10]
    f = aoi.CACHE / f"stack_{tag}_{key}.npz"
    if f.exists():
        d = np.load(f)
        return {"vv": d["vv"], "vh": d["vh"]}, d["cover"], d["mean_vv"]
    n, npx = len(scene_ids), int(zmask.sum())
    st = {p: np.full((n, npx), NODATA, np.int16) for p in ("vv", "vh")}
    cover = np.zeros(n)
    acc = np.zeros((aoi.H, aoi.W)), np.zeros((aoi.H, aoi.W))
    for i, sid in enumerate(scene_ids):
        full = load_scene_db(sid)
        ok = np.isfinite(full["vv"])
        acc[0][ok] += full["vv"][ok]
        acc[1][ok] += 1
        for p, a in full.items():
            v = a[sl][zmask]
            st[p][i] = np.where(np.isfinite(v), np.rint(v * 100), NODATA).astype(np.int16)
        cover[i] = (st["vv"][i] != NODATA).mean()
    mean_vv = (acc[0] / np.maximum(acc[1], 1)).astype(np.float32)
    np.savez(f, vv=st["vv"], vh=st["vh"], cover=cover, mean_vv=mean_vv)
    return st, cover, mean_vv


def unflatten(v, zmask):
    out = np.full(zmask.shape, np.nan, np.float32)
    out[zmask] = np.where(v == NODATA, np.nan, v / 100.0)
    return out


def background(stack_rows):
    """Temporal background of int16 dB x 100 rows -> float dB; no-data sorts as darkest, harmless when rare."""
    return detect.background(stack_rows).astype(np.float32) / 100.0


def run():
    t0 = time.time()
    zones, sl, zr = zone_setup()
    zmask = zr > 0
    scenes = pd.read_csv(fetch.SCENES_CSV)
    scenes["t"] = pd.to_datetime(scenes["datetime"], utc=True)
    for c in ("cover", "sea_vv_db", "sea_vh_db", "n_too_small", "n_too_big", "masked_frac"):
        scenes[c] = np.nan
    dets = []
    for orbit, grp in scenes[(scenes.status == "ok") & (scenes.valid_frac > 0)].groupby("rel_orbit"):
        ids = list(grp.scene_id)
        st, cover, mean_vv = build_stack(ids, sl, zmask, f"orb{orbit}")
        np.save(aoi.CACHE / f"mean_vv_orb{orbit}.npy", mean_vv)
        scenes.loc[grp.index, "cover"] = cover
        good = cover >= MIN_COVER
        has_vh = (st["vh"] != NODATA).mean(axis=1) >= MIN_COVER
        tt = grp.t.dt.tz_convert(None).to_numpy()
        print(f"orbit {orbit}: {len(ids)} passes, {good.sum()} cover the zones, {time.time() - t0:.0f} s", flush=True)
        for year in sorted(grp.t.dt.year[good].unique()):
            mid = np.datetime64(f"{year}-07-01")
            win = good & (np.abs(tt.astype("datetime64[D]") - mid) <= np.timedelta64(BG_HALF_WINDOW_DAYS, "D"))
            bg = {"vv": unflatten_f(background(st["vv"][win]), zmask)}
            if (win & has_vh).sum() >= 10:
                bg["vh"] = unflatten_f(background(st["vh"][win & has_vh]), zmask)
            water = detect.water_mask(bg, zmask)
            np.savez(aoi.CACHE / f"bg_orb{orbit}_{year}.npz", water=water, r0=sl[0].start, c0=sl[1].start, **bg)  # kept for inspection
            open_sea = water & (zr == 2)
            for i in np.nonzero(good & (grp.t.dt.year.values == year))[0]:
                db = {"vv": unflatten(st["vv"][i], zmask)}
                if has_vh[i] and "vh" in bg:
                    db["vh"] = unflatten(st["vh"][i], zmask)
                kept, dropped = detect.detect(db, {p: bg[p] for p in db}, water)
                row = grp.index[i]
                lon, lat = aoi.pixel_to_lonlat(np.array([d["row"] for d in kept]) + sl[0].start,
                                               np.array([d["col"] for d in kept]) + sl[1].start)
                for d, lo, la in zip(kept, np.atleast_1d(lon), np.atleast_1d(lat)):
                    z = aoi.zone_of(lo, la, zones)
                    if z is None:
                        continue
                    dets.append({"scene_id": grp.scene_id[row], "datetime": grp.datetime[row],
                                 "platform": grp.platform[row], "rel_orbit": orbit, "direction": grp.direction[row],
                                 "lon": round(float(lo), 6), "lat": round(float(la), 6), "zone": z,
                                 **d, "row": round(d["row"] + sl[0].start, 1), "col": round(d["col"] + sl[1].start, 1)})
                scenes.loc[row, "sea_vv_db"] = float(np.nanmedian(db["vv"][open_sea]))
                if "vh" in db:
                    scenes.loc[row, "sea_vh_db"] = float(np.nanmedian(db["vh"][open_sea]))
                scenes.loc[row, "n_too_small"] = sum(d["why"] == "too_small" for d in dropped)
                scenes.loc[row, "n_too_big"] = sum(d["why"] == "too_big" for d in dropped)
                scenes.loc[row, "masked_frac"] = 1 - water.sum() / zmask.sum()
        del st
    det = pd.DataFrame(dets).sort_values(["datetime", "zone", "row"]).reset_index(drop=True)
    det.insert(0, "det_id", [f"D{i:05d}" for i in range(1, len(det) + 1)])
    det.to_csv(aoi.CACHE / "raw_detections.csv", index=False)
    scenes.drop(columns="t").to_csv(aoi.CACHE / "raw_scenes.csv", index=False)
    print(f"detection done, {time.time() - t0:.0f} s")
    return finish()


def finish():
    """Flags, counts and tables from the raw detections (fast; rerun with `python -m mcm.sar.run --post`)."""
    det = pd.read_csv(aoi.CACHE / "raw_detections.csv")
    scenes = pd.read_csv(aoi.CACHE / "raw_scenes.csv")
    scenes["t"] = pd.to_datetime(scenes["datetime"], utc=True)
    det["repeat_passes_30d"] = repeats(det)
    det["fixed_object"] = fixed_objects(det)
    DET_CSV.parent.mkdir(parents=True, exist_ok=True)
    det.to_csv(DET_CSV, index=False)
    counted = det[~det.fixed_object]
    for z in ("basin", "roadstead"):
        n = counted[counted.zone == z].groupby("scene_id").size()
        scenes[f"n_{z}"] = scenes.scene_id.map(n).fillna(0).where(scenes.cover >= MIN_COVER)
    write_tables(scenes, det)
    print(f"{len(det)} detections ({int(det.fixed_object.sum())} flagged as fixed objects) in "
          f"{int(scenes.n_basin.notna().sum())} counted passes")
    return scenes, det


def _days(datetimes):
    """ISO strings -> days since 1970 (float)."""
    t = pd.to_datetime(datetimes, utc=True).dt.tz_convert(None).to_numpy()
    return t.astype("datetime64[s]").astype(np.int64) / 86400.0


def unflatten_f(v, zmask):
    out = np.full(zmask.shape, np.nan, np.float32)
    out[zmask] = v
    return out


def repeats(det, radius_m=50.0, days=30):
    """For each detection: in how many OTHER passes within +/- `days` is there a detection within `radius_m`.
    A berthed ship gives 0-3; a value that stays high for months means a fixed object or a laid-up hull."""
    xy = np.column_stack([det["col"], det["row"]]) * aoi.RES
    t = _days(det["datetime"])
    sid = det["scene_id"].values
    tree = cKDTree(xy)
    out = []
    for i, nb in enumerate(tree.query_ball_point(xy, radius_m)):
        nb = [j for j in nb if sid[j] != sid[i] and abs(t[j] - t[i]) <= days]
        out.append(len(set(sid[nb])))
    return out


def fixed_objects(det, radius_m=50.0, min_passes=12, min_span_days=180):
    """Roadstead only: True where the same 50 m spot fires in >= 12 passes spread over >= 180 days.
    Anchored ships reuse a spot at most ~10 times in 8 years here (there is a gap in the histogram between
    10 and 12); a wreck, platform, buoy or sandbar fires far more often.
    Not applied in the basin, where berths are reused by design."""
    xy = np.column_stack([det["col"], det["row"]]) * aoi.RES
    t = _days(det["datetime"])
    sid, road = det["scene_id"].values, (det["zone"] == "roadstead").values
    out = np.zeros(len(det), bool)
    for i, nb in enumerate(cKDTree(xy).query_ball_point(xy, radius_m)):
        nb = [j for j in nb if road[j]]
        out[i] = road[i] and len(set(sid[nb])) >= min_passes and np.ptp(t[nb]) >= min_span_days
    return out


def write_tables(scenes, det):
    TABLES.mkdir(parents=True, exist_ok=True)
    s = scenes.copy()
    s["status"] = np.where(s.status != "ok", "failed_read",
                           np.where(s.cover >= MIN_COVER, "counted", np.where(s.cover > 0, "partial_coverage", "no_coverage")))
    s["cover"] = s.cover.fillna(0)  # passes whose frame has no data on the grid at all were never stacked
    s["n_total"] = s.n_basin + s.n_roadstead
    # sea level relative to the same orbit's median: a wind / roughness proxy (uncalibrated, so only relative)
    s["sea_vv_anom_db"] = (s.sea_vv_db - s.groupby("rel_orbit").sea_vv_db.transform("median")).round(2)
    s["sea_vh_anom_db"] = (s.sea_vh_db - s.groupby("rel_orbit").sea_vh_db.transform("median")).round(2)
    cols = ["scene_id", "datetime", "platform", "rel_orbit", "direction", "pols", "status", "cover", "n_basin",
            "n_roadstead", "n_total", "sea_vv_anom_db", "sea_vh_anom_db", "n_too_small", "n_too_big", "masked_frac", "item_ids"]
    s[cols].round({"cover": 4, "masked_frac": 4}).to_csv(TABLES / "sar_scene_counts.csv", index=False)
    c = s[s.status == "counted"].copy()
    for period, name in (("M", "sar_monthly.csv"), ("Y", "sar_yearly.csv")):
        key = c.t.dt.tz_localize(None).dt.to_period(period).astype(str)
        g = c.groupby(key)
        out = pd.DataFrame({"n_passes": g.size()})
        for z in ("basin", "roadstead", "total"):
            out[f"mean_{z}"] = g[f"n_{z}"].mean().round(2)
            out[f"median_{z}"] = g[f"n_{z}"].median()
            if period == "Y":
                out[f"detections_{z}"] = g[f"n_{z}"].sum().astype(int)
        out.rename_axis("month" if period == "M" else "year").to_csv(TABLES / name)


if __name__ == "__main__":
    import sys
    finish() if "--post" in sys.argv else run()
