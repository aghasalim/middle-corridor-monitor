"""Second, independent ship detector: Ai2's rslearn Sentinel-1 vessel model run on our cached passes.

    .venv/Scripts/python research/second_detector.py [--ids a,b] [--limit N] [--threads 3]   # detect (resumable)
    .venv/Scripts/python research/second_detector.py --compare [--ids a,b]                  # vs our detector, 50 m
    .venv/Scripts/python research/second_detector.py --plot ID [ID ...]                     # check figures

Model: rslearn_projects 20260626_num_historical / ..._1hist (Swin-B on the target pass + one historical pass,
FPN, Faster R-CNN), Apache-2.0. Inputs as in its config: VV, VH raw GRD DN / 250 clipped to [0, 4], 512 px patches,
overlap 0.1, distance NMS 10 px. Our passes are already DN on UTM 39N at 10 m (bilinear, GCPs at sea height;
Ai2 uses cubic and no height shift). Output is UNVALIDATED, like our own detector.

Writes data/sar/detections_ai2.csv (one row per box with score >= MIN_SCORE; the model's own threshold is 0.9)
and data/sar/detections_ai2_passes.csv (one row per finished pass; a pass listed there is skipped on rerun).
"""
import argparse
import os
import sys
import time
from pathlib import Path

import numpy as np
import pandas as pd

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))
from mcm.sar import aoi, detect, fetch, run  # noqa: E402

CKPT = aoi.SAR_DIR / "models" / "ai2_s1_vessel" / "best.ckpt"
# clone of https://github.com/allenai/rslearn_projects (commit 393636e); set RSLEARN_PROJECTS to its folder
CONFIG = Path(os.environ.get("RSLEARN_PROJECTS", "rslearn_projects")) / "data/sentinel1_vessels/20260626_num_historical/config_1hist.yaml"
OUT = aoi.SAR_DIR / "detections_ai2.csv"
PASSES_OUT = aoi.SAR_DIR / "detections_ai2_passes.csv"
COUNTS = aoi.ROOT / "outputs" / "tables" / "sar_scene_counts.csv"
FIGS = ROOT / "research" / "figs_ai2_check"
PATCH, OVERLAP, NMS_PX = 512, 0.1, 10
MIN_SCORE = 0.5      # kept in the CSV so the threshold can be varied later
MODEL_SCORE = 0.9    # Ai2's configured score_threshold
HIST_DAYS = (30, 60)  # Ai2 takes the historical pass from 60 to 30 days before the target
MATCH_M = 50.0
DET_COLS = ["scene_id", "datetime", "rel_orbit", "row", "col", "lon", "lat", "score", "zone", "masked", "box_w_px", "box_h_px"]
PASS_COLS = ["scene_id", "datetime", "rel_orbit", "hist_scene_id", "hist_offset_days", "n_boxes", "seconds"]


def counted_passes():
    s = pd.read_csv(COUNTS)
    s = s[s.status == "counted"].copy()
    s["t"] = pd.to_datetime(s.datetime, utc=True)
    return s.sort_values("t").reset_index(drop=True)


def pick_history(passes, scene_id):
    """Same-orbit counted pass 30-60 days earlier, closest to 60 days (as Ai2's search window starts there).
    Fallback (first two months of the archive): the nearest same-orbit pass at least 30 days away, either side.
    Returns (scene_id, offset_days; negative = earlier)."""
    me = passes[passes.scene_id == scene_id].iloc[0]
    same = passes[(passes.rel_orbit == me.rel_orbit) & (passes.scene_id != scene_id)]
    off = (same.t - me.t).dt.total_seconds().to_numpy() / 86400
    win = (off <= -HIST_DAYS[0]) & (off >= -HIST_DAYS[1] - 1)
    if win.any():
        i = np.flatnonzero(win)[np.argmin(np.abs(off[win] + HIST_DAYS[1]))]
    else:
        far = np.abs(off) >= HIST_DAYS[0]
        i = np.flatnonzero(far)[np.argmin(np.abs(off[far]))]
    return same.scene_id.iloc[i], round(float(off[i]), 1)


def load_dn(scene_id, sl):
    d = np.load(fetch.SCENE_CACHE / f"{scene_id}.npz")
    return np.stack([d["vv"][sl], d["vh"][sl]]).astype(np.float32)  # band order of the config: vv, vh


def load_model():
    import torch
    import yaml
    from jsonargparse import ArgumentParser
    from rslearn.models.multitask import MultiTaskModel

    cfg = yaml.safe_load(CONFIG.read_text(encoding="utf8"))["model"]["init_args"]["model"]
    p = ArgumentParser()
    p.add_argument("--model", type=MultiTaskModel)
    model = p.instantiate_classes(p.parse_object({"model": cfg})).model
    ck = torch.load(CKPT, map_location="cpu", weights_only=True)
    sd = {k.removeprefix("model."): v for k, v in ck["state_dict"].items()}
    model.load_state_dict(sd, strict=True)
    return model.eval()


def starts(n):
    """Patch origins along one axis: stride PATCH*(1-OVERLAP), last patch flush with the edge."""
    if n <= PATCH:
        return [0]
    step = int(PATCH * (1 - OVERLAP))
    s = list(range(0, n - PATCH, step))
    return s + [n - PATCH]


def box_to_rowcol(box, r0, c0):
    """Box (x0, y0, x1, y1) in patch pixel-edge coordinates -> (row, col) pixel-centre index on our grid."""
    return r0 + (box[1] + box[3]) / 2 - 0.5, c0 + (box[0] + box[2]) / 2 - 0.5


def distance_nms(rc, scores, radius=NMS_PX):
    """Greedy: keep the best box, drop others whose centre is within `radius` px of a kept one."""
    keep = []
    for i in np.argsort(-scores):
        if all(np.hypot(*(rc[i] - rc[j])) > radius for j in keep):
            keep.append(i)
    return sorted(keep)


def infer(model, cur, hist):
    """cur, hist: (2, H, W) DN. Returns rows of (row, col, score, w, h) in crop pixel coordinates, after NMS."""
    import torch
    from rslearn.train.model_context import ModelContext, RasterImage

    x = np.clip(np.stack([cur, hist], axis=1) / 250.0, 0, 4)  # C, T, H, W (Concatenate along time, Normalize)
    _, _, H, W = x.shape
    found = []
    with torch.no_grad():
        for r in starts(H):
            for c in starts(W):
                patch = np.zeros((2, 2, PATCH, PATCH), np.float32)
                tile = x[:, :, r:r + PATCH, c:c + PATCH]
                patch[:, :, :tile.shape[2], :tile.shape[3]] = tile
                ctx = ModelContext(inputs=[{"image": RasterImage(torch.from_numpy(patch))}], metadatas=[None])
                o = model(ctx).outputs[0]["detect"]
                for b, s in zip(o["boxes"].numpy(), o["scores"].numpy()):
                    if s >= MIN_SCORE:
                        rr, cc = box_to_rowcol(b, r, c)
                        if rr < H and cc < W:
                            found.append((rr, cc, float(s), b[2] - b[0], b[3] - b[1]))
    if not found:
        return []
    a = np.array(found)
    return [found[i] for i in distance_nms(a[:, :2], a[:, 2])]


def done_ids():
    """Scene ids already finished; drops detections of a pass that crashed half-written."""
    if not PASSES_OUT.exists():
        return set()
    done = set(pd.read_csv(PASSES_OUT).scene_id)
    if OUT.exists():
        d = pd.read_csv(OUT)
        if not d.scene_id.isin(done).all():
            d[d.scene_id.isin(done)].to_csv(OUT, index=False)
    return done


def append(path, rows, cols):
    pd.DataFrame(rows, columns=cols).to_csv(path, mode="a", header=not path.exists(), index=False)


def detect_all(ids=None, limit=None):
    zones, sl, _ = run.zone_setup()
    r0, c0 = int(sl[0].start), int(sl[1].start)
    passes = counted_passes()
    todo = passes if ids is None else passes[passes.scene_id.isin(ids)]
    done = done_ids()
    todo = todo[~todo.scene_id.isin(done)]
    if limit:
        todo = todo.head(limit)
    print(f"{len(todo)} passes to do ({len(done)} done before)", flush=True)
    if todo.empty:
        return
    model = load_model()
    water = {}
    for k, p in enumerate(todo.itertuples()):
        t0 = time.time()
        hid, hoff = pick_history(passes, p.scene_id)
        boxes = infer(model, load_dn(p.scene_id, sl), load_dn(hid, sl))
        key = (p.rel_orbit, p.t.year)
        if key not in water:
            water[key] = np.load(aoi.CACHE / f"bg_orb{p.rel_orbit}_{p.t.year}.npz")["water"]
        rows = []
        for rr, cc, s, w, h in boxes:
            lon, lat = aoi.pixel_to_lonlat(rr + r0, cc + c0)
            ir, ic = int(round(rr)), int(round(cc))
            rows.append([p.scene_id, p.datetime, p.rel_orbit, round(rr + r0, 1), round(cc + c0, 1),
                         round(float(lon), 6), round(float(lat), 6), round(s, 4),
                         aoi.zone_of(float(lon), float(lat), zones) or "",
                         not water[key][ir, ic], round(float(w), 1), round(float(h), 1)])
        append(OUT, rows, DET_COLS)
        sec = round(time.time() - t0, 1)
        append(PASSES_OUT, [[p.scene_id, p.datetime, p.rel_orbit, hid, hoff, len(rows), sec]], PASS_COLS)
        print(f"{k + 1}/{len(todo)} {p.scene_id[17:32]} orb {p.rel_orbit} hist {hoff:+.0f} d: "
              f"{len(rows)} boxes, {sec} s", flush=True)


def ai2_counted(d, score=MODEL_SCORE):
    """In a zone, on a pixel our detector also searches (not permanently bright), score over the model threshold."""
    return d[(d.score > score) & d.zone.isin(["basin", "roadstead"]) & ~d.masked.astype(bool)]


def compare(ids=None):
    from scipy.spatial import cKDTree

    ours = pd.read_csv(run.DET_CSV)
    ours = ours[~ours.fixed_object]
    ai2 = ai2_counted(pd.read_csv(OUT))
    done = pd.read_csv(PASSES_OUT).scene_id
    ids = list(done) if ids is None else ids
    rows = []
    for sid in ids:
        a, o = ai2[ai2.scene_id == sid], ours[ours.scene_id == sid]
        for z in ("basin", "roadstead"):
            az, oz = a[a.zone == z], o[o.zone == z]
            pa, po = az[["row", "col"]].to_numpy() * aoi.RES, oz[["row", "col"]].to_numpy() * aoi.RES
            o_hit = a_hit = 0
            if len(pa) and len(po):
                o_hit = int((cKDTree(pa).query(po)[0] <= MATCH_M).sum())
                a_hit = int((cKDTree(po).query(pa)[0] <= MATCH_M).sum())
            rows.append({"scene_id": sid, "zone": z, "ours": len(oz), "ai2": len(az),
                         "ours_matched": o_hit, "ai2_matched": a_hit})
    t = pd.DataFrame(rows)
    print(t.to_string(index=False))
    print(t.groupby("zone")[["ours", "ai2", "ours_matched", "ai2_matched"]].sum())
    return t


def plot(ids):
    import matplotlib
    matplotlib.use("Agg")
    import matplotlib.pyplot as plt

    _, sl, zr = run.zone_setup()
    r0, c0 = int(sl[0].start), int(sl[1].start)
    ai2 = pd.read_csv(OUT)
    ours = pd.read_csv(run.DET_CSV)
    FIGS.mkdir(parents=True, exist_ok=True)
    for sid in ids:
        vv = detect.smooth_db(np.load(fetch.SCENE_CACHE / f"{sid}.npz")["vv"])[sl]
        fig, ax = plt.subplots(figsize=(11, 11.5))
        ax.imshow(vv, cmap="gray", vmin=np.nanpercentile(vv, 2), vmax=np.nanpercentile(vv, 99.7))
        ax.contour(zr, levels=[0.5, 1.5], colors=["#3a7bd5", "#e0a800"], linewidths=0.8)
        a, o = ai2[ai2.scene_id == sid], ours[(ours.scene_id == sid) & ~ours.fixed_object]
        hi = a[a.score > MODEL_SCORE]
        ax.scatter(hi.col - c0, hi.row - r0, s=160, facecolors="none", edgecolors="red", lw=1.2,
                   label=f"Ai2 score > {MODEL_SCORE} ({len(hi)}, any zone/mask)")
        lo = a[a.score <= MODEL_SCORE]
        ax.scatter(lo.col - c0, lo.row - r0, s=160, facecolors="none", edgecolors="orange", lw=0.8, ls="--",
                   label=f"Ai2 {MIN_SCORE}-{MODEL_SCORE} ({len(lo)})")
        ax.scatter(o.col - c0, o.row - r0, s=18, marker="+", c="cyan", lw=1, label=f"ours ({len(o)})")
        ax.set_title(f"{sid[:32]}  VV dB, crop of our grid (row0 {r0}, col0 {c0})", fontsize=9)
        ax.legend(loc="upper left", fontsize=8)
        fig.tight_layout()
        fig.savefig(FIGS / f"{sid[17:32]}.png", dpi=110)
        plt.close(fig)
        print("wrote", FIGS / f"{sid[17:32]}.png")


if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("--ids", help="comma-separated scene ids (default: all counted passes)")
    ap.add_argument("--limit", type=int)
    ap.add_argument("--threads", type=int, default=3)
    ap.add_argument("--compare", action="store_true")
    ap.add_argument("--plot", nargs="+")
    a = ap.parse_args()
    ids = a.ids.split(",") if a.ids else None
    if a.plot:
        plot(a.plot)
    elif a.compare:
        compare(ids)
    else:
        import torch
        torch.set_num_threads(a.threads)
        detect_all(ids, a.limit)
