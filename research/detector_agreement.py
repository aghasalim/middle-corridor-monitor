"""Our radar detector against Ai2's Sentinel-1 vessel model at Alat: outputs/tables/sar_detector_agreement*.csv.

A detection is matched when the other detector has one within 50 m in the same pass and zone. Both detectors are
unvalidated; agreement between them is not accuracy. Needs data/sar/detections.csv, detections_ai2.csv and
model_labels.csv (research/second_detector.py, research/sar_label_eval.py).
"""
import contextlib
import io
import sys
from pathlib import Path

import pandas as pd
from scipy.spatial import cKDTree

sys.path.insert(0, str(Path(__file__).parent))
import second_detector as sd  # noqa: E402
from mcm.sar import aoi, run  # noqa: E402

TAB = sd.ROOT / "outputs" / "tables"


def by_zone_year(t):
    """t: one row per pass and zone (ours, ai2, ours_matched, ai2_matched) with a year column."""
    cols = ["ours", "ai2", "ours_matched", "ai2_matched"]
    g = pd.concat([t.groupby(["zone", "year"])[cols].sum().reset_index(),
                   t.groupby("zone")[cols].sum().reset_index().assign(year="all")])
    g["ours_matched_share"] = (g.ours_matched / g.ours).round(3)
    g["ai2_matched_share"] = (g.ai2_matched / g.ai2).round(3)
    r = {z: round(x.ours.corr(x.ai2), 3) for z, x in t.groupby("zone")}  # per-pass counts, Pearson
    g["r_counts_per_pass"] = [r[z] if y == "all" else "" for z, y in zip(g.zone, g.year)]
    return g


def by_label():
    """Labelled detections: does Ai2 have a detection within 50 m, by the AI label."""
    s = pd.read_csv(aoi.SAR_DIR / "label_sample.csv").merge(pd.read_csv(aoi.SAR_DIR / "model_labels.csv"), on=["sample_id", "kind"])
    s = s[s.kind == "detection"].merge(pd.read_csv(run.DET_CSV)[["det_id", "row", "col"]], on="det_id")
    ai2 = sd.ai2_counted(pd.read_csv(sd.OUT))
    hit = []
    for r in s.itertuples():
        a = ai2[ai2.scene_id == r.scene_id][["row", "col"]].to_numpy() * aoi.RES
        hit.append(bool(len(a)) and cKDTree(a).query([r.row * aoi.RES, r.col * aoi.RES])[0] <= sd.MATCH_M)
    s["ai2_match"] = hit
    g = s.groupby(["zone", "model_is_vessel"]).ai2_match.agg(n="size", ai2_matched="sum").reset_index()
    return g.rename(columns={"model_is_vessel": "ai_label"})


if __name__ == "__main__":
    with contextlib.redirect_stdout(io.StringIO()):  # compare() prints every pass
        t = sd.compare()
    t["year"] = t.scene_id.str.extract(r"_(\d{4})\d{4}T")[0]
    a, b = by_zone_year(t), by_label()
    a.to_csv(TAB / "sar_detector_agreement.csv", index=False)
    b.to_csv(TAB / "sar_detector_agreement_labels.csv", index=False)
    print(a.to_string(index=False), b.to_string(index=False), sep="\n\n")
