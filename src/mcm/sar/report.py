"""Figures, diagnostics and the hand-labelling kit for the Alat SAR detections.

    python -m mcm.sar.report

Everything drawn here is UNVALIDATED detector output; the figures say so in their titles.
"""
import shutil

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from PIL import Image, ImageDraw
from scipy.stats import spearmanr

from . import aoi, run, sample

FIGS = aoi.ROOT / "outputs" / "figures"
CHIPS = aoi.SAR_DIR / "label_chips"
LABEL_CSV = aoi.SAR_DIR / "label_sample.csv"
WARN = "UNVALIDATED detector output - not a traffic measurement"
ZCOL = {"basin": "tab:red", "roadstead": "tab:orange"}
N_EMPTY_TILES_PER_YEAR_ZONE = 8
PANEL = 192  # px per chip panel


def s2_reference():
    """Sentinel-2 true colour on the working grid (Planetary Computer, anonymous), cached. None if unavailable."""
    f = aoi.CACHE / "s2_visual.npy"
    if not f.exists():
        try:
            import planetary_computer, pystac_client, rasterio
            from rasterio.windows import from_bounds
            from .fetch import STAC
            it = next(pystac_client.Client.open(STAC, modifier=planetary_computer.sign_inplace).search(
                collections=["sentinel-2-l2a"], ids=["S2C_MSIL2A_20250901T072631_R049_T39TUE_20250901T112614"]).items())
            with rasterio.open(it.assets["visual"].href) as src:
                b = (aoi.X0, aoi.Y0 - aoi.H * aoi.RES, aoi.X0 + aoi.W * aoi.RES, aoi.Y0)
                np.save(f, src.read(window=from_bounds(*b, src.transform), boundless=True))
        except Exception as e:
            print("no Sentinel-2 reference:", e)
            return None
    return np.moveaxis(np.load(f), 0, -1)


def zone_outlines(ax, zones, lw=1.2):
    for name, poly in zones.items():
        lon, lat = poly.exterior.xy
        r, c = aoi.lonlat_to_pixel(np.array(lon), np.array(lat))
        ax.plot(c, r, color=ZCOL[name], lw=lw, label=name)


def gray(ax, db, lo=None):
    lo = np.nanpercentile(db, 20) - 2 if lo is None else lo
    ax.imshow(db, cmap="gray", vmin=lo, vmax=lo + 26, interpolation="nearest")


def fig_zones(zones):
    mean = np.load(aoi.CACHE / "mean_vv_orb28.npy")
    s2 = s2_reference()
    fig, ax = plt.subplots(1, 3, figsize=(19, 8), gridspec_kw={"width_ratios": [1.5, 1.7, 1.7]})
    gray(ax[0], mean)
    ax[0].set_title("Mean Sentinel-1 VV image, relative orbit 28 (all passes 2019-2026)")
    gray(ax[1], mean)
    ax[1].set_xlim(440, 640); ax[1].set_ylim(640, 440)
    ax[1].set_title("Same, port close-up (2 km x 2 km)")
    if s2 is not None:
        ax[2].imshow(s2)
        ax[2].set_xlim(440, 640); ax[2].set_ylim(640, 440)
        ax[2].set_title("Sentinel-2 true colour, 1 Sep 2025, same close-up")
    for a in ax:
        zone_outlines(a, zones)
        a.set_xlabel("grid column (10 m)"); a.set_ylabel("grid row (10 m)")
    ax[0].legend(loc="lower left")
    fig.suptitle("Port of Baku at Alat: basin (red) and roadstead/approach (orange) zones. UTM 39N grid, north up.")
    fig.tight_layout()
    fig.savefig(FIGS / "sar_zones.png", dpi=110)
    plt.close(fig)


def fig_timeseries(sc):
    c = sc[sc.status == "counted"].copy()
    c["t"] = pd.to_datetime(c.datetime, utc=True).dt.tz_localize(None)
    fig, ax = plt.subplots(3, 1, figsize=(15, 10), sharex=True)
    for a, z in zip(ax, ("basin", "roadstead", "total")):
        a.plot(c.t, c[f"n_{z}"], ".", ms=3, color="0.6", label="one pass")
        m = c.set_index("t")[f"n_{z}"].resample("MS").mean()
        a.plot(m.index + pd.Timedelta(days=15), m.values, "-", color="tab:blue", lw=1.6, label="monthly mean per pass")
        a.set_ylabel(f"blobs present per pass\n{z}")
        a.grid(alpha=0.3)
    ax[0].legend(loc="upper left", ncol=2)
    ax[0].set_title(f"Alat, Sentinel-1: bright transient blobs present per pass ({len(c)} passes). {WARN}")
    fig.tight_layout()
    fig.savefig(FIGS / "sar_timeseries.png", dpi=110)
    plt.close(fig)


def fig_map(det, zones):
    mean = np.load(aoi.CACHE / "mean_vv_orb28.npy")
    fig, ax = plt.subplots(1, 2, figsize=(17, 9.5), gridspec_kw={"width_ratios": [1.5, 1.7]})
    for a in ax:
        gray(a, mean)
        zone_outlines(a, zones, 0.8)
        for z, g in det[~det.fixed_object].groupby("zone"):
            a.plot(g.col, g.row, ".", ms=2.5, alpha=0.5, color=ZCOL[z])
        fx = det[det.fixed_object]
        a.plot(fx.col, fx.row, "x", ms=5, color="cyan", label=f"flagged as fixed object, not counted ({len(fx)})")
    ax[0].legend(loc="upper right", fontsize=8)
    ax[0].set_title(f"All {len(det)} detections 2019-2026 on the mean VV image")
    ax[1].set_xlim(440, 640); ax[1].set_ylim(640, 440)
    ax[1].set_title("Port close-up (2 km x 2 km)")
    fig.suptitle(f"Where the detector fired. {WARN}")
    fig.tight_layout()
    fig.savefig(FIGS / "sar_detection_map.png", dpi=110)
    plt.close(fig)


def _stretch(db, lo, span=28.0):
    return np.uint8(255 * np.clip((np.nan_to_num(db, nan=lo) - lo) / span, 0, 1))


def chip(scene_db, mean_vv, row, col, half=32):
    """RGB chip: [VV | VH | mean VV of all passes of that orbit], centred on (row, col), north up, 200 m bar."""
    r0, c0 = int(round(row)) - half, int(round(col)) - half

    def cut(a):
        out = np.full((2 * half, 2 * half), np.nan, np.float32)
        rs, cs = r0, c0
        ra, rb, ca, cb = max(rs, 0), min(rs + 2 * half, a.shape[0]), max(cs, 0), min(cs + 2 * half, a.shape[1])
        if rb > ra and cb > ca:
            out[ra - rs:rb - rs, ca - cs:cb - cs] = a[ra:rb, ca:cb]
        return out

    vv = cut(scene_db["vv"])
    lo = np.nanpercentile(vv, 30) - 3
    panels = [_stretch(vv, lo)]
    if "vh" in scene_db:
        vh = cut(scene_db["vh"])
        panels.append(_stretch(vh, np.nanpercentile(vh, 30) - 3))
    else:
        panels.append(np.zeros_like(panels[0]))
    panels.append(_stretch(cut(mean_vv), lo))
    k = PANEL / (2 * half)
    im = Image.new("RGB", (3 * PANEL + 8, PANEL + 14), (0, 0, 0))
    d = ImageDraw.Draw(im)
    for i, (p, name) in enumerate(zip(panels, ("VV", "VH", "VV mean"))):
        x = i * (PANEL + 4)
        im.paste(Image.fromarray(p).resize((PANEL, PANEL), Image.NEAREST), (x, 14))
        d.text((x + 2, 1), name, fill=(255, 255, 0))
        for a, b in (((x + PANEL // 2, 14), (x + PANEL // 2, 22)), ((x, 14 + PANEL // 2), (x + 8, 14 + PANEL // 2)),
                     ((x + PANEL // 2, PANEL + 5), (x + PANEL // 2, PANEL + 13)), ((x + PANEL - 9, 14 + PANEL // 2), (x + PANEL - 1, 14 + PANEL // 2))):
            d.line([a, b], fill=(255, 255, 0))  # edge ticks point at the centre without covering it
    d.line([(6, PANEL + 6), (6 + round(20 * k), PANEL + 6)], fill=(0, 255, 255), width=2)
    d.text((10 + round(20 * k), PANEL - 1), "200 m", fill=(0, 255, 255))
    return im


def label_kit(det, sc, n_det):
    """Chips + CSV for a human: a stratified sample of detections, plus tiles where the detector saw nothing."""
    if LABEL_CSV.exists():  # never wipe a sheet a human has started filling in
        old = pd.read_csv(LABEL_CSV)
        if old[["is_vessel", "n_vessels_seen", "note"]].notna().any().any():
            print(f"{LABEL_CSV.name} already has labels: kit left untouched (move it away to rebuild)")
            return old
    if CHIPS.exists():
        shutil.rmtree(CHIPS)
    CHIPS.mkdir(parents=True)
    rng = np.random.default_rng(0)
    rows = []
    s = sample.stratified_sample(det, n_det, seed=0)
    for _, d in s.iterrows():
        rows.append({"kind": "detection", "year": d.datetime[:4], "zone": d.zone, "scene_id": d.scene_id,
                     "datetime_utc": d.datetime, "rel_orbit": d.rel_orbit, "lon": d.lon, "lat": d.lat,
                     "det_id": d.det_id, "row": d.row, "col": d.col, "half": 32})
    # tiles with no detection: so that missed vessels can be found (recall)
    zr = aoi.zone_raster(aoi.load_zones())
    c = sc[sc.status == "counted"]
    for (year, zone, code) in [(y, z, k) for y in sorted(c.datetime.str[:4].unique()) for z, k in (("basin", 1), ("roadstead", 2))]:
        cy = c[c.datetime.str[:4] == year]
        zrows, zcols = np.nonzero(zr == code)
        got = tries = 0
        while got < N_EMPTY_TILES_PER_YEAR_ZONE and tries < 500:
            tries += 1
            p = cy.iloc[rng.integers(len(cy))]
            j = rng.integers(len(zrows))
            r, cc = int(zrows[j]), int(zcols[j])
            dd = det[det.scene_id == p.scene_id]
            if ((dd.row - r).abs() <= 48).mul((dd.col - cc).abs() <= 48).any():
                continue
            got += 1
            lon, lat = aoi.pixel_to_lonlat(r, cc)
            rows.append({"kind": "empty_tile", "year": year, "zone": zone, "scene_id": p.scene_id,
                         "datetime_utc": p.datetime, "rel_orbit": p.rel_orbit, "lon": round(float(lon), 6),
                         "lat": round(float(lat), 6), "det_id": "", "row": r, "col": cc, "half": 48})
    lab = pd.DataFrame(rows)
    lab = lab.iloc[rng.permutation(len(lab))].reset_index(drop=True)  # shuffled so the labeller sees no pattern
    lab.insert(0, "sample_id", [f"S{i:04d}" for i in range(1, len(lab) + 1)])
    lab["chip_file"] = "label_chips/" + lab.sample_id + ".png"
    for sid, g in lab.groupby("scene_id"):
        db = run.load_scene_db(sid)
        mean = np.load(aoi.CACHE / f"mean_vv_orb{int(g.rel_orbit.iloc[0])}.npy")
        for _, x in g.iterrows():
            chip(db, mean, x.row, x["col"], int(x.half)).save(CHIPS / f"{x.sample_id}.png", optimize=True)
    lab["is_vessel"] = ""        # detection chips: yes / no / unsure
    lab["n_vessels_seen"] = ""   # empty tiles: how many vessels a human sees (0 if none)
    lab["note"] = ""
    lab.drop(columns=["row", "col", "half"]).to_csv(LABEL_CSV, index=False)
    return lab


def fig_contact_sheet(lab, det, n=40):
    d = lab[lab.kind == "detection"].head(n).merge(det[["det_id", "length_m", "peak_db_vv", "peak_db_vh"]], on="det_id")
    fig, ax = plt.subplots(8, 5, figsize=(20, 12.5))
    for a in ax.ravel():
        a.axis("off")
    for a, (_, x) in zip(ax.ravel(), d.iterrows()):
        a.imshow(Image.open(aoi.SAR_DIR / x.chip_file))
        a.set_title(f"{x.sample_id} {x.datetime_utc[:10]} {x.zone} ~{x.length_m:.0f} m  VV {x.peak_db_vv:.0f} / VH {x.peak_db_vh:.0f} dB", fontsize=8)
    fig.suptitle(f"First {len(d)} detections of the (shuffled) hand-labelling sample. Panels: VV | VH | mean VV of that orbit. "
                 f"640 m across, north up. {WARN}", fontsize=11)
    fig.tight_layout()
    fig.savefig(FIGS / "sar_contact_sheet.png", dpi=100)
    plt.close(fig)


def diagnostics(sc, det):
    """Junk checks: do counts follow sea roughness, does the same spot fire again and again, do orbits disagree."""
    c = sc[sc.status == "counted"]
    rows = []
    fig, ax = plt.subplots(2, 3, figsize=(18, 10))
    for j, z in enumerate(("basin", "roadstead")):
        for i, pol in enumerate(("vv", "vh")):
            ok = c[f"sea_{pol}_anom_db"].notna()
            rho, p = spearmanr(c[f"sea_{pol}_anom_db"][ok], c[f"n_{z}"][ok])
            rows.append({"check": f"spearman_count_vs_sea_{pol}_level", "zone": z, "value": round(rho, 3), "p_value": float(f"{p:.3g}"), "n": int(ok.sum())})
        ax[j, 0].plot(c.sea_vv_anom_db, c[f"n_{z}"], ".", ms=4, alpha=0.5, color=ZCOL[z])
        ax[j, 0].set_xlabel("open-water VV level of the pass, dB relative to that orbit's median (roughness proxy)")
        ax[j, 0].set_ylabel(f"blobs per pass, {z}")
        ax[j, 0].set_title(f"{z}: count vs sea roughness, Spearman rho = {rows[-2]['value']}")
        g = [c[c.rel_orbit == o][f"n_{z}"].values for o in sorted(c.rel_orbit.unique())]
        ax[j, 1].boxplot(g, tick_labels=[f"orbit {o}" for o in sorted(c.rel_orbit.unique())])
        ax[j, 1].set_title(f"{z}: blobs per pass by relative orbit")
        for o in sorted(c.rel_orbit.unique()):
            rows.append({"check": "mean_per_pass_by_orbit", "zone": z, "value": round(c[c.rel_orbit == o][f"n_{z}"].mean(), 2), "n": int((c.rel_orbit == o).sum()), "orbit": o})
        for plat in sorted(c.platform.unique()):
            rows.append({"check": "mean_per_pass_by_platform", "zone": z, "value": round(c[c.platform == plat][f"n_{z}"].mean(), 2), "n": int((c.platform == plat).sum()), "platform": plat})
        dz = det[det.zone == z]
        ax[j, 2].hist(dz.repeat_passes_30d, bins=np.arange(-0.5, dz.repeat_passes_30d.max() + 1.5), color=ZCOL[z])
        ax[j, 2].set_xlabel("other passes within +/-30 days with a detection within 50 m")
        ax[j, 2].set_title(f"{z}: does the same spot fire again?")
        for k in (1, 5, 10):
            rows.append({"check": f"share_with_repeat_ge_{k}", "zone": z, "value": round(float((dz.repeat_passes_30d >= k).mean()), 3), "n": len(dz)})
        for thr in (10, 15, 20):
            pk = dz[["peak_db_vv", "peak_db_vh"]].max(axis=1)
            rows.append({"check": f"share_with_peak_contrast_ge_{thr}dB", "zone": z, "value": round(float((pk >= thr).mean()), 3), "n": len(dz)})
        for lim in (80, 120):
            rows.append({"check": f"share_with_length_under_{lim}m", "zone": z, "value": round(float((dz.length_m < lim).mean()), 3), "n": len(dz)})
        rows.append({"check": "median_length_m", "zone": z, "value": float(dz.length_m.median()), "n": len(dz)})
        rows.append({"check": "share_seen_in_both_polarisations", "zone": z, "value": round(float((dz.det_vv & dz.det_vh).mean()), 3), "n": len(dz)})
        rows.append({"check": "share_vv_only", "zone": z, "value": round(float((dz.det_vv & ~dz.det_vh).mean()), 3), "n": len(dz)})
        rows.append({"check": "share_vh_only", "zone": z, "value": round(float((~dz.det_vv & dz.det_vh).mean()), 3), "n": len(dz)})
    # registration: shift between the first and last counted pass of each orbit, land + port window (px of 10 m)
    from skimage.registration import phase_cross_correlation
    win = (slice(380, 560), slice(380, 620))
    for o in sorted(c.rel_orbit.unique()):
        ids = c[c.rel_orbit == o].sort_values("datetime").scene_id
        a, b = (np.nan_to_num(run.load_scene_db(s)["vv"][win], nan=0.0) for s in (ids.iloc[0], ids.iloc[-1]))
        shift, _, _ = phase_cross_correlation(a, b, upsample_factor=10)
        rows.append({"check": "registration_shift_px_first_vs_last_pass", "zone": "port", "orbit": o,
                     "value": round(float(np.hypot(*shift)), 2), "n": 2})
    fig.suptitle(f"Junk checks. {WARN}")
    fig.tight_layout()
    fig.savefig(FIGS / "sar_diagnostics.png", dpi=100)
    plt.close(fig)
    pd.DataFrame(rows).to_csv(run.TABLES / "sar_diagnostics.csv", index=False)
    # hot spots: 50 m cells where the detector fired in many different passes
    cell = det.assign(cr=(det.row // 5).astype(int), cc=(det.col // 5).astype(int))
    hs = cell.groupby(["zone", "cr", "cc"]).agg(n_passes=("scene_id", "nunique"), first=("datetime", "min"), last=("datetime", "max"),
                                                lon=("lon", "mean"), lat=("lat", "mean"), median_length_m=("length_m", "median")).reset_index()
    hs["share_of_counted_passes"] = (hs.n_passes / len(c)).round(3)
    hs.sort_values("n_passes", ascending=False).head(40).drop(columns=["cr", "cc"]).round({"lon": 5, "lat": 5}).to_csv(run.TABLES / "sar_hotspots.csv", index=False)


def main():
    FIGS.mkdir(parents=True, exist_ok=True)
    zones = aoi.load_zones()
    det_all = pd.read_csv(run.DET_CSV)
    det = det_all[~det_all.fixed_object].reset_index(drop=True)  # what the counts are made of
    sc = pd.read_csv(run.TABLES / "sar_scene_counts.csv")
    table = sample.sample_size_table(len(det))
    table.to_csv(run.TABLES / "sar_sample_size.csv", index=False)
    print(table.to_string(index=False))
    n_det = int(table[(table.p == 0.5) & (table.margin_pp == 7)].n_with_fpc.iloc[0])  # recommended, see SAR_METHOD.md
    fig_zones(zones)
    fig_timeseries(sc)
    fig_map(det_all, zones)
    diagnostics(sc, det)
    lab = label_kit(det, sc, n_det)
    fig_contact_sheet(lab, det)
    print(lab.groupby(["kind", "zone"]).size().to_string())
    print("chips:", sum(f.stat().st_size for f in CHIPS.glob("*.png")) / 1e6, "MB")


if __name__ == "__main__":
    main()
