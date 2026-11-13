"""Transient bright targets on water: temporal background + CFAR-style threshold + connected components.

Pure numpy/scipy, no I/O, so it can be tested on synthetic images. All images are in dB of 3x3-smoothed
power (uncalibrated digital numbers: only contrasts are used, never absolute backscatter).
"""
import warnings

import numpy as np
from scipy import ndimage as ndi

# --- thresholds (each one is explained in research/SAR_METHOD.md) ---
BG_PERCENTILE = 25      # temporal background = 25th percentile of a pixel's history (same orbit, same pol)
T_MIN_DB = 6.0          # a pixel must be this much brighter than its reference level ...
K_SPREAD = 3.5          # ... or K x the local sea spread (p90 - p50), whichever is larger
BLOCK = 50              # px; the sea level and spread are measured in 500 m blocks
CORE_DB = 10.0          # "core" of a blob = pixels within 10 dB of its brightest pixel
MIN_CORE_LEN_PX = 5     # 50 m measured, about 30 m real once ~20 m of blur is taken off
MIN_AREA_PX = 8
MAX_CORE_LEN_PX = 30    # 300 m: no Caspian ship is that long -> merged targets, wakes, interference; dropped
MAX_AREA_PX = 1500      # 0.15 km2: bigger than any ship plus its sidelobes -> sea feature, dropped
PERSIST_DB = 10.0       # background this far above the usual open-water background = permanently bright -> masked
PIXEL_M = 10.0


def smooth_db(amp):
    """Amplitude (DN) -> dB of 3x3 mean power. Pixels with any no-data (0) neighbour become NaN."""
    a = amp.astype(np.float32)
    p = ndi.uniform_filter(a * a, 3, mode="nearest")
    bad = ndi.minimum_filter(a, 3, mode="nearest") == 0
    out = 10 * np.log10(np.maximum(p, 1e-3))
    out[bad] = np.nan
    return out


def background(stack, q=BG_PERCENTILE):
    """Per-pixel low percentile over time (axis 0) of scenes from the same orbit geometry and polarisation."""
    return np.percentile(stack, q, axis=0)


def water_mask(bg_db, zone):
    """Pixels of `zone` that are not permanently bright in any polarisation (+1 px for registration jitter).

    bg_db: {'vv': 2-D background dB, ...}; zone: bool array of where ships are looked for at all.
    'Permanently bright' = background more than PERSIST_DB above the median background of the zone,
    i.e. quays, cranes, breakwaters, platforms, land.
    """
    bright = np.zeros(zone.shape, bool)
    for b in bg_db.values():
        bright |= zone & (b > np.nanmedian(b[zone]) + PERSIST_DB)
    return zone & ~ndi.binary_dilation(bright, np.ones((3, 3)))


def sea_level_and_spread(db, water, block=BLOCK):
    """Median and (p90 - p50) of the water pixels in each block, bilinearly spread back to full size."""
    h, w = db.shape
    nby, nbx = -(-h // block), -(-w // block)
    pad = np.full((nby * block, nbx * block), np.nan, np.float32)
    pad[:h, :w] = np.where(water, db, np.nan)
    blocks = pad.reshape(nby, block, nbx, block).swapaxes(1, 2).reshape(nby, nbx, -1)
    n = np.isfinite(blocks).sum(-1)
    with warnings.catch_warnings():  # all-NaN blocks (land) are expected
        warnings.simplefilter("ignore")
        p50, p90 = np.nanpercentile(blocks, [50, 90], axis=-1)
    few = n < block * block // 10  # a block with under 10% water takes the scene-wide values
    g50 = np.nanmedian(p50[~few]) if (~few).any() else np.nan
    g90 = np.nanmedian(p90[~few]) if (~few).any() else np.nan
    p50 = np.where(few, g50, p50)
    p90 = np.where(few, g90, p90)
    yi = (np.arange(h) + 0.5) / block - 0.5
    xi = (np.arange(w) + 0.5) / block - 0.5
    yy, xx = np.meshgrid(yi, xi, indexing="ij")
    med = ndi.map_coordinates(p50, [yy, xx], order=1, mode="nearest")
    spread = ndi.map_coordinates(p90 - p50, [yy, xx], order=1, mode="nearest")
    return med.astype(np.float32), spread.astype(np.float32)


def excess_db(db, bg_db, water):
    """How far each pixel is above its threshold.

    Reference = the larger of (a) the pixel's own temporal background and (b) the sea around it right now.
    Threshold = reference + max(T_MIN_DB, K_SPREAD x local spread). Returns (excess over threshold, contrast
    over reference); both NaN-safe (NaN counts as 'not above').
    """
    med, spread = sea_level_and_spread(db, water)
    ref = np.fmax(bg_db, med)
    contrast = db - ref
    return contrast - np.maximum(T_MIN_DB, K_SPREAD * spread), contrast


def _extent(rows, cols):
    """Length and width (px) of a pixel set along its principal axes."""
    if len(rows) < 2:
        return 1.0, 1.0
    xy = np.column_stack([cols - cols.mean(), rows - rows.mean()]).astype(float)
    _, vecs = np.linalg.eigh(np.cov(xy.T) + 1e-9 * np.eye(2))
    proj = xy @ vecs  # columns: minor, major
    return float(np.ptp(proj[:, 1]) + 1), float(np.ptp(proj[:, 0]) + 1)


def detect(db, bg_db, water):
    """Find transient bright blobs.

    db, bg_db: dicts {'vv': array, 'vh': array} (either key may be missing) of scene / background dB.
    water: bool array, True where a ship may be (not land, not persistently bright).
    Returns (kept, dropped): lists of dicts; 'dropped' holds blobs removed by the size rules, with 'why'.
    Two ships stay separate only if at least one pixel between them is below threshold (8-connectivity);
    ships moored side by side merge into one blob.
    """
    pols = [p for p in ("vv", "vh") if p in db]
    exc, con = {}, {}
    for p in pols:
        exc[p], con[p] = excess_db(db[p], bg_db[p], water)
    hit = {p: water & (exc[p] > 0) for p in pols}
    mask = np.logical_or.reduce([hit[p] for p in pols])
    labels, n = ndi.label(mask, structure=np.ones((3, 3)))
    kept, dropped = [], []
    for i, sl in enumerate(ndi.find_objects(labels), 1):
        m = labels[sl] == i
        rows, cols = np.nonzero(m)
        area = int(m.sum())
        d = {"row": float(rows.mean() + sl[0].start), "col": float(cols.mean() + sl[1].start), "area_px": area}
        best = None
        for p in pols:
            c = np.where(m, con[p][sl], np.nan)
            d[f"det_{p}"] = bool(hit[p][sl][m].any())
            d[f"peak_db_{p}"] = round(float(np.nanmax(c)), 1) if np.isfinite(c).any() else np.nan
            d[f"mean_db_{p}"] = round(float(np.nanmean(c)), 1) if np.isfinite(c).any() else np.nan
            if d[f"det_{p}"] and (best is None or d[f"peak_db_{p}"] > d[f"peak_db_{best}"]):
                best = p
        c = np.where(m, con[best][sl], -np.inf)
        cr, cc = np.nonzero(c >= c.max() - CORE_DB)
        length, width = _extent(cr, cc)
        d["length_m"] = round(length * PIXEL_M)
        d["width_m"] = round(width * PIXEL_M)
        full_len, _ = _extent(rows, cols)
        d["blob_length_m"] = round(full_len * PIXEL_M)
        if area > MAX_AREA_PX or length > MAX_CORE_LEN_PX:
            dropped.append({**d, "why": "too_big"})
        elif area < MIN_AREA_PX or length < MIN_CORE_LEN_PX:
            dropped.append({**d, "why": "too_small"})
        else:
            kept.append(d)
    return kept, dropped
