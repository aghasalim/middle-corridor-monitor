"""Detector precision and missed-vessel rate at Alat from the labelled chips.

Inputs:  data/sar/label_sample.csv (zone, kind; human labels if any)
         data/sar/model_labels.csv (AI labels by an LLM looking at the same chips, blind to detector scores)
Output:  outputs/tables/sar_label_eval.csv  and outputs/tables/sar_label_agreement.csv
         (AI vs human on whatever chips a human has labelled so far)
Run:     .venv/Scripts/python research/sar_label_eval.py
"""
from math import sqrt
from pathlib import Path

import pandas as pd

ROOT = Path(__file__).resolve().parents[1]
SAR = ROOT / "data" / "sar"
TABLES = ROOT / "outputs" / "tables"


def wilson(k, n, z=1.96):
    """95 % Wilson interval for k successes out of n."""
    if n == 0:
        return float("nan"), float("nan")
    p = k / n
    d = 1 + z * z / n
    c = (p + z * z / (2 * n)) / d
    h = z * sqrt(p * (1 - p) / n + z * z / (4 * n * n)) / d
    return max(0.0, c - h), min(1.0, c + h)


def kappa(a, b):
    """Cohen's kappa for two equal-length label lists."""
    n = len(a)
    if n == 0:
        return float("nan")
    po = sum(x == y for x, y in zip(a, b)) / n
    cats = set(a) | set(b)
    pe = sum((list(a).count(c) / n) * (list(b).count(c) / n) for c in cats)
    return float("nan") if pe == 1 else (po - pe) / (1 - pe)


def evaluate(df, source):
    """Rows: precision per zone (detections) and missed-vessel rate per zone (empty tiles)."""
    rows = []
    for zone in ("roadstead", "basin", "all"):
        z = df if zone == "all" else df[df.zone == zone]
        d = z[z.kind == "detection"]
        n = len(d)
        yes, no, uns = (d.is_vessel == "yes").sum(), (d.is_vessel == "no").sum(), (d.is_vessel == "unsure").sum()
        lo, hi = wilson(yes, yes + no)
        rows.append({"label_source": source, "zone": zone, "measure": "precision (yes / (yes + no))", "n": n,
                     "yes": yes, "no": no, "unsure": uns, "value": yes / (yes + no) if yes + no else float("nan"),
                     "ci95_low": lo, "ci95_high": hi,
                     "bound_unsure_as_no": yes / n if n else float("nan"),
                     "bound_unsure_as_yes": (yes + uns) / n if n else float("nan")})
        e = z[z.kind == "empty_tile"]
        m = len(e)
        clear = (e.n_seen > 0).sum()
        poss = ((e.n_seen + e.n_possible) > 0).sum()
        lo, hi = wilson(clear, m)
        rows.append({"label_source": source, "zone": zone, "measure": "share of empty tiles with a missed vessel", "n": m,
                     "yes": clear, "no": m - poss, "unsure": poss - clear, "value": clear / m if m else float("nan"),
                     "ci95_low": lo, "ci95_high": hi,
                     "bound_unsure_as_no": clear / m if m else float("nan"),
                     "bound_unsure_as_yes": poss / m if m else float("nan"),
                     "vessels_seen": int(e.n_seen.sum()), "vessels_possible": int(e.n_possible.sum())})
    return pd.DataFrame(rows)


def main():
    lab = pd.read_csv(SAR / "label_sample.csv", dtype=str, keep_default_na=False)
    mod = pd.read_csv(SAR / "model_labels.csv", dtype=str, keep_default_na=False)
    assert (lab.sample_id == mod.sample_id).all() and (lab.kind == mod.kind).all()
    model = lab[["sample_id", "kind", "zone"]].assign(
        is_vessel=mod.model_is_vessel,
        n_seen=pd.to_numeric(mod.model_n_vessels_seen, errors="coerce").fillna(0),
        n_possible=pd.to_numeric(mod.model_n_vessels_possible, errors="coerce").fillna(0))
    name = mod.model_name.iloc[0]
    out = evaluate(model, f"AI-labelled ({name}), not checked by a human")
    TABLES.mkdir(parents=True, exist_ok=True)
    out.round(4).to_csv(TABLES / "sar_label_eval.csv", index=False)
    print(out.round(3).to_string(index=False))

    # Agreement on every chip a human has labelled (the 50-chip check sample was not finished)
    chk = lab.assign(m_v=mod.model_is_vessel, m_n=mod.model_n_vessels_seen)
    d = chk[(chk.kind == "detection") & (chk.is_vessel != "")]
    e = chk[(chk.kind == "empty_tile") & (chk.n_vessels_seen != "")]
    agr = pd.DataFrame([
        {"set": "detections, yes/no/unsure", "n_labelled_by_human": len(d),
         "agreement": (d.is_vessel == d.m_v).mean() if len(d) else float("nan"), "cohen_kappa": kappa(d.is_vessel, d.m_v)},
        {"set": "empty tiles, any vessel (0 vs >=1)", "n_labelled_by_human": len(e),
         "agreement": ((e.n_vessels_seen.astype(int) > 0) == (e.m_n.astype(int) > 0)).mean() if len(e) else float("nan"),
         "cohen_kappa": kappa(e.n_vessels_seen.astype(int) > 0, e.m_n.astype(int) > 0) if len(e) else float("nan")},
    ])
    agr.round(4).to_csv(TABLES / "sar_label_agreement.csv", index=False)
    print(agr.round(3).to_string(index=False))


if __name__ == "__main__":
    main()
