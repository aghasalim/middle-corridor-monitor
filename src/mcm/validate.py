"""Compare PortWatch aggregates with official figures (data/official/official_figures.csv).

No estimates: a PortWatch value is only computed when PortWatch covers every day of the
official period, and an increment is only derived from two consecutive cumulative releases.
"""
from pathlib import Path

import numpy as np
import pandas as pd
from scipy import stats

from mcm import index as ix

ROOT = Path(__file__).resolve().parents[2]
OFFICIAL = ROOT / "data" / "official" / "official_figures.csv"
COLUMNS = ["entity", "period_start", "period_end", "metric", "value", "unit",
           "definition", "source_url", "source_date", "status", "note"]
# Which PortWatch ports stand for each official entity. Kuryk is not in PortWatch.
TITR_KZ = "TITR (Kazakh ministry series)"  # one consistent 2019-2025 series; other TITR rows mix sources
# "KZ seaports" includes Kuryk, which PortWatch cannot see: the ratio shows what is visible.
ENTITY_PORTS = {"Port of Baku": ["port100"], "Aktau": ["port16"], "Aktau incl. AMCT": ["port16"],
                "KZ seaports": ["port16"], "Kazakhstan sea transport": ["port16"], "TITR": ix.CASPIAN, TITR_KZ: ix.CASPIAN}
PW_MEASURES = ["dry_calls", "dry_tonnes", "all_tonnes", "all_calls", "tanker_calls", "tanker_tonnes", "roro_calls"]
AMCT = "Aktau North Terminal (AMCT)"
TONNES = {"t": 1, "tonnes": 1, "tonne": 1, "kt": 1e3, "thousand tonnes": 1e3,
          "mt": 1e6, "million tonnes": 1e6}
ANNUAL_TARGETS = [("Port of Baku", "tonnes_total"), ("KZ seaports", "tonnes_total"),
                  (TITR_KZ, "tonnes_total"), ("Aktau", "tonnes_total"), ("Aktau", "tonnes_oil"),
                  ("Aktau", "vessel_calls"), ("Aktau incl. AMCT", "tonnes_total"),
                  ("Aktau incl. AMCT", "vessel_calls")]


def same_unit(metric, measure):
    """A level ratio only means something for tonnes vs tonnes or calls vs calls."""
    return (metric.startswith("tonnes") and measure.endswith("tonnes")) or            (metric.endswith("calls") and measure.endswith("calls"))


def add_aktau_amct(off):
    """PortWatch's "Aktau Port" boundary is unpublished and may include the separate AMCT
    terminal, so add official Aktau + AMCT (same source table, same year) as its own entity."""
    a = off[off["entity"].isin(["Aktau", AMCT]) & off["metric"].isin(["tonnes_total", "vessel_calls"])
            & off["source_url"].astype(str).str.contains("stat.gov.kz")]
    a = a.drop_duplicates(["entity", "metric", "period_start", "period_end"])
    rows = []
    for (met, ps, pe), g in a.groupby(["metric", "period_start", "period_end"]):
        if set(g["entity"]) == {"Aktau", AMCT}:
            r = g.iloc[0].copy()
            r["entity"], r["value"], r["value_std"] = "Aktau incl. AMCT", g["value"].sum(), g["value_std"].sum()
            r["definition"], r["note"] = "Aktau port + AMCT terminal, summed here", "derived sum of two official rows"
            rows.append(r)
    return pd.concat([off, pd.DataFrame(rows)], ignore_index=True) if rows else off


def load_official(path=OFFICIAL):
    """Read the CSV, or return an empty frame (and say why) when it is missing."""
    if not Path(path).exists():
        print(f"validate: {path} not found, nothing to compare")
        return pd.DataFrame(columns=COLUMNS)
    df = pd.read_csv(path)
    missing = [c for c in COLUMNS if c not in df.columns]
    if missing:
        raise ValueError(f"{path}: missing columns {missing}")
    df["period_start"] = pd.to_datetime(df["period_start"])
    df["period_end"] = pd.to_datetime(df["period_end"])
    df["value"] = pd.to_numeric(df["value"], errors="coerce")
    bad = df["value"].isna()
    if bad.any():
        print(f"validate: dropping {bad.sum()} rows with non-numeric value")
    return df[~bad].reset_index(drop=True)


def to_tonnes(df):
    """Add value_std: tonnes for tonne units, the raw value for counts (teu, wagons...)."""
    df = df.copy()
    f = df["unit"].astype(str).str.strip().str.lower().map(TONNES)
    is_t = df["metric"].astype(str).str.startswith("tonnes")
    unknown = is_t & f.isna()
    if unknown.any():
        print(f"validate: unknown tonne units {sorted(df.loc[unknown, 'unit'].unique())}, those rows skipped")
    df["value_std"] = df["value"].where(~is_t, df["value"] * f)
    return df[~unknown]


def increments(df):
    """Turn cumulative year-to-date releases into increments.

    Within an entity/metric/year, rows that all start on 1 January are cumulative; each
    one after the first becomes (this - previous) over (previous end + 1 day .. this end).
    Rows not starting on 1 January are left as they are. Output column `derived` marks
    the differenced rows.
    """
    df = df.copy()
    df["derived"] = False
    if df.empty:
        return df
    ytd = (df["period_start"].dt.month == 1) & (df["period_start"].dt.day == 1)
    dup = df[ytd].duplicated(["entity", "metric", "period_start", "period_end"], keep="first")
    if dup.any():
        print(f"validate: {dup.sum()} duplicate cumulative releases, keeping the first listed")
        df = df.drop(df[ytd].index[dup])
        ytd = ytd.loc[df.index]
    out = [df[~ytd]]
    for _, g in df[ytd].groupby(["entity", "metric", df.loc[ytd, "period_start"].dt.year]):
        g = g.sort_values("period_end")
        out.append(g)  # keep the cumulative releases themselves as well
        for prev, cur in zip(g.iloc[:-1].itertuples(), g.iloc[1:].itertuples()):
            row = cur._asdict()
            row.pop("Index")
            row.update(period_start=prev.period_end + pd.Timedelta(days=1),
                       value=cur.value - prev.value, derived=True,
                       note=f"increment of cumulative releases ending {prev.period_end.date()} and {cur.period_end.date()}")
            if "value_std" in row:
                row["value_std"] = cur.value_std - prev.value_std
            out.append(pd.DataFrame([row]))
    return pd.concat(out, ignore_index=True)


def pw_daily(dailies):
    """Per-port daily PortWatch measures used for comparison."""
    out = {}
    for p, d in dailies.items():
        m = ix.add_measures(d)
        m["all_tonnes"] = m["dry_tonnes"] + m["tanker_tonnes"]
        m["all_calls"] = m["dry_calls"] + m["tanker_calls"]
        out[p] = m[["date"] + PW_MEASURES]
    return out


def pw_period(daily, start, end):
    """Sum PortWatch daily measures over start..end inclusive, or None if any day is missing."""
    want = pd.date_range(start, end, freq="D")
    w = daily[(daily["date"] >= start) & (daily["date"] <= end)]
    if len(w) != len(want) or not w["date"].isin(want).all():
        return None
    return w[PW_MEASURES].sum()


def align(official, pw):
    """One row per official figure and PortWatch measure, with the PortWatch sum over the same period."""
    rows = []
    for r in official.itertuples():
        ports = ENTITY_PORTS.get(r.entity)
        if not ports:
            continue  # an entity PortWatch cannot see (e.g. Kuryk)
        if any(p not in pw for p in ports):
            continue
        sums = [pw_period(pw[p], r.period_start, r.period_end) for p in ports]
        if any(s is None for s in sums):
            print(f"validate: PortWatch does not cover {r.entity} {r.period_start.date()}..{r.period_end.date()}, skipped")
            continue
        tot = sum(sums)
        for meas in PW_MEASURES:
            rows.append({"entity": r.entity, "metric": r.metric, "period_start": r.period_start.date(),
                         "period_end": r.period_end.date(), "official": r.value_std,
                         "derived": r.derived, "status": r.status, "pw_measure": meas,
                         "portwatch": tot[meas],
                         "ratio_pw_over_official": tot[meas] / r.value_std if r.value_std else float("nan")})
    return pd.DataFrame(rows)


def corr(a, b):
    """Pearson and Spearman with n; NaN when fewer than 3 points."""
    ok = a.notna() & b.notna()
    n = int(ok.sum())
    if n < 3:
        return {"n": n, "pearson": float("nan"), "spearman": float("nan")}
    return {"n": n, "pearson": stats.pearsonr(a[ok], b[ok])[0], "spearman": stats.spearmanr(a[ok], b[ok])[0]}


def annual_comparison(aligned, years=range(2019, 2026)):
    """Annual (1 Jan - 31 Dec) rows for the target series: levels, ratios and YoY growth."""
    if aligned.empty:
        return pd.DataFrame(), pd.DataFrame()
    a = aligned.copy()
    ps, pe = pd.to_datetime(a["period_start"]), pd.to_datetime(a["period_end"])
    a = a[(ps.dt.month == 1) & (ps.dt.day == 1) & (pe.dt.month == 12) & (pe.dt.day == 31)
          & (ps.dt.year == pe.dt.year) & ps.dt.year.isin(list(years))].copy()
    a["year"] = pd.to_datetime(a["period_start"]).dt.year
    a = a.drop_duplicates(["entity", "metric", "pw_measure", "year"])
    tables, summary = [], []
    for (ent, met, meas), g in a.groupby(["entity", "metric", "pw_measure"]):
        if (ent, met) not in ANNUAL_TARGETS:
            continue
        g = g.set_index("year").sort_index().reindex(list(years))
        g["official_yoy"] = g["official"].pct_change(fill_method=None)
        g["portwatch_yoy"] = g["portwatch"].pct_change(fill_method=None)
        g[["entity", "metric", "pw_measure"]] = [ent, met, meas]
        tables.append(g.reset_index())
        lv, gr = corr(g["official"], g["portwatch"]), corr(g["official_yoy"], g["portwatch_yoy"])
        summary.append({"entity": ent, "metric": met, "pw_measure": meas,
                        "years_with_both": int(g["official"].notna().sum()),
                        "mean_ratio": g["ratio_pw_over_official"].mean() if same_unit(met, meas) else float("nan"),
                        "level_n": lv["n"], "level_pearson": lv["pearson"], "level_spearman": lv["spearman"],
                        "yoy_n": gr["n"], "yoy_pearson": gr["pearson"], "yoy_spearman": gr["spearman"]})
    cols = ["entity", "metric", "pw_measure", "year", "official", "portwatch",
            "ratio_pw_over_official", "official_yoy", "portwatch_yoy", "status"]
    t = pd.concat(tables, ignore_index=True)[cols] if tables else pd.DataFrame(columns=cols)
    return t, pd.DataFrame(summary)


def monthly_test(aligned, entity="Kazakhstan sea transport", metric="tonnes_carried",
                 measure="all_tonnes", min_train=24):
    """Single-month official figures against PortWatch for the same months, plus an honest
    out-of-sample check: does a regression on PortWatch (fitted only on earlier months)
    beat two naive forecasts (same month last year, previous available month)?"""
    a = aligned[(aligned["entity"] == entity) & (aligned["metric"] == metric)
                & (aligned["pw_measure"] == measure) & ~aligned["derived"]].copy()
    a["month"] = pd.to_datetime(a["period_start"]).dt.to_period("M")
    a = a[pd.to_datetime(a["period_end"]).dt.to_period("M") == a["month"]]
    a = a.drop_duplicates("month").set_index("month").sort_index()[["official", "portwatch"]]
    if len(a) < 3:
        return a.reset_index(), {}
    a["official_yoy"] = a["official"] / a["official"].reindex(a.index - 12).to_numpy() - 1
    a["portwatch_yoy"] = a["portwatch"] / a["portwatch"].reindex(a.index - 12).to_numpy() - 1
    lv, gr = corr(a["official"], a["portwatch"]), corr(a["official_yoy"], a["portwatch_yoy"])
    res = {"entity": entity, "metric": metric, "pw_measure": measure, "months": len(a),
           "first": str(a.index[0]), "last": str(a.index[-1]),
           "level_pearson": lv["pearson"], "level_spearman": lv["spearman"],
           "yoy_n": gr["n"], "yoy_pearson": gr["pearson"], "yoy_spearman": gr["spearman"]}
    a["fc_portwatch"] = float("nan")
    for i in range(min_train, len(a)):
        b, c = np.polyfit(a["portwatch"].iloc[:i], a["official"].iloc[:i], 1)
        a.iloc[i, a.columns.get_loc("fc_portwatch")] = b * a["portwatch"].iloc[i] + c
    a["fc_last_year"] = a["official"].reindex(a.index - 12).to_numpy()
    a["fc_previous"] = a["official"].shift(1)
    t = a.dropna(subset=["fc_portwatch", "fc_last_year", "fc_previous"])
    res["oos_months"] = len(t)
    for k in ("fc_portwatch", "fc_last_year", "fc_previous"):
        res[f"rmse_{k[3:]}"] = float(np.sqrt(((t[k] - t["official"]) ** 2).mean())) if len(t) else float("nan")
    return a.reset_index(), res


def blind_spot(off, dailies):
    """What PortWatch cannot see: Kuryk's share of Kazakh seaport cargo and its ferry calls,
    next to the Ro-Ro calls PortWatch records at Baku (where the Kuryk ferries sail to)."""
    o = off[(off["period_start"].dt.month == 1) & (off["period_start"].dt.day == 1)
            & (off["period_end"].dt.month == 12) & (off["period_end"].dt.day == 31)
            & off["source_url"].astype(str).str.contains("stat.gov.kz")].copy()
    o["year"] = o["period_start"].dt.year

    def col(ent, met):
        return o[(o["entity"] == ent) & (o["metric"] == met)].drop_duplicates("year").set_index("year")["value_std"]
    t = pd.DataFrame({"kuryk_tonnes": col("Kuryk", "tonnes_total"), "kz_seaports_tonnes": col("KZ seaports", "tonnes_total"),
                      "kuryk_vessel_calls": col("Kuryk", "vessel_calls"), "kuryk_ferry_calls": col("Kuryk", "ferry_calls")})
    t["kuryk_share_of_kz_seaports"] = t["kuryk_tonnes"] / t["kz_seaports_tonnes"]
    for name, ports in (("pw_baku_roro_calls", ["port100"]), ("pw_caspian_roro_calls", ix.CASPIAN)):
        d = sum(dailies[p].assign(date=pd.to_datetime(dailies[p]["date"])).set_index("date")["portcalls_roro"] for p in ports)
        t[name] = d.groupby(d.index.year).sum()
    return t.loc[2019:2025].reset_index()


def run(dailies, path=OFFICIAL, out_dir=ROOT / "outputs" / "tables"):
    off = load_official(path)
    if off.empty:
        print("validate: no official rows; no comparison written")
        return None
    off = add_aktau_amct(to_tonnes(off))
    kz = (off["entity"] == "TITR") & (off["metric"] == "tonnes_total") & off["source_url"].astype(str).str.contains("bizmedia.kz")
    off = increments(pd.concat([off, off[kz].assign(entity=TITR_KZ)], ignore_index=True))
    out_dir.mkdir(parents=True, exist_ok=True)
    blind_spot(off, dailies).to_csv(out_dir / "validate_blind_spot.csv", index=False)
    for ent, met in ANNUAL_TARGETS:
        if off[(off.entity == ent) & (off.metric == met)].empty:
            print(f"validate: no official rows for {ent} / {met}")
    al = align(off, pw_daily(dailies))
    yearly, summary = annual_comparison(al)
    out_dir.mkdir(parents=True, exist_ok=True)
    al.to_csv(out_dir / "validate_periods.csv", index=False)
    yearly.to_csv(out_dir / "validate_annual.csv", index=False)
    summary.to_csv(out_dir / "validate_summary.csv", index=False)
    monthly, mres = monthly_test(al)
    monthly.to_csv(out_dir / "validate_monthly.csv", index=False)
    pd.DataFrame([mres]).to_csv(out_dir / "validate_monthly_summary.csv", index=False)
    print("validate monthly:", {k: (round(v, 3) if isinstance(v, float) else v) for k, v in mres.items()})
    print(f"validate: {len(off)} official rows, {len(al)} aligned rows, {len(yearly)} annual rows")
    if not summary.empty:
        print(summary.round(3).to_string(index=False))
    return al, yearly, summary


if __name__ == "__main__":
    from mcm import portwatch
    run(portwatch.load())
