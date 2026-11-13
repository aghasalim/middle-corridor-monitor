"""Monthly Caspian indices from PortWatch daily data. Pure functions: DataFrame in, DataFrame out."""
import pandas as pd

DRY = ["container", "dry_bulk", "general_cargo", "roro"]  # non-tanker ship types
CASPIAN = ["port100", "port16", "port1330"]  # Baku, Aktau, Turkmenbashi
BLACKSEA = ["port1016", "port127"]  # Poti, Batumi
NAMES = {"port100": "Baku", "port16": "Aktau", "port1330": "Turkmenbashi",
         "port1016": "Poti", "port127": "Batumi"}
BASE_YEAR = 2019


def add_measures(daily):
    """Add dry_calls, roro_calls, tanker_calls, dry_tonnes, tanker_tonnes columns to one port's daily rows."""
    d = daily.copy()
    d["dry_calls"] = d[[f"portcalls_{s}" for s in DRY]].sum(axis=1)
    d["roro_calls"] = d["portcalls_roro"]
    d["general_cargo_calls"] = d["portcalls_general_cargo"]
    d["tanker_calls"] = d["portcalls_tanker"]
    d["dry_tonnes"] = d[[f"{k}_{s}" for k in ("import", "export") for s in DRY]].sum(axis=1)
    d["tanker_tonnes"] = d["import_tanker"] + d["export_tanker"]
    return d


def sum_ports(dailies, cols):
    """Sum daily columns across ports. Every port must have exactly the same set of days."""
    dates = None
    for pid, d in dailies.items():
        if d["date"].duplicated().any():
            raise ValueError(f"{pid}: duplicated dates")
        s = set(d["date"])
        if dates is not None and s != dates:
            raise ValueError(f"{pid}: dates differ from the other ports ({len(s ^ dates)} days)")
        dates = s
    total = sum(d.set_index("date")[cols] for d in dailies.values())
    return total.sort_index().reset_index()


def monthly(daily, cols):
    """Daily rows -> monthly sums, keeping only months with every calendar day present
    (so the incomplete last month is dropped)."""
    d = daily.set_index("date")[cols]
    m = d.resample("MS").sum()
    days = d.resample("MS").size()
    complete = days == m.index.days_in_month
    return m[complete].rename_axis("month")


def rebase(m, year=BASE_YEAR):
    """Index each column so that the monthly mean of `year` = 100."""
    base = m[m.index.year == year]
    if len(base) != 12:
        raise ValueError(f"base year {year} has {len(base)} complete months, need 12")
    return m / base.mean() * 100


def rolling12(m):
    """12-month rolling sum (NaN for the first 11 months)."""
    return m.rolling(12).sum()


def series(dailies):
    """Headline and comparator monthly series, with *_index columns (2019 = 100)."""
    d = {p: add_measures(x) for p, x in dailies.items()}
    cols = ["dry_calls", "roro_calls", "tanker_calls", "dry_tonnes"]
    casp = monthly(sum_ports({p: d[p] for p in CASPIAN}, cols), cols)
    casp.columns = ["caspian_" + c for c in cols]
    bs = monthly(sum_ports({p: d[p] for p in BLACKSEA}, ["dry_calls"]), ["dry_calls"])
    bs.columns = ["blacksea_dry_calls"]
    out = casp.join(bs, how="inner")
    idx = rebase(out).add_suffix("_index")
    roll = rolling12(out[["caspian_dry_calls"]]).add_suffix("_12m")
    return out.join(idx).join(roll)


def per_port(dailies, cols=("dry_calls", "roro_calls", "general_cargo_calls", "tanker_calls", "dry_tonnes", "tanker_tonnes")):
    """Long monthly table: one row per port and month."""
    parts = []
    for p, x in dailies.items():
        m = monthly(add_measures(x), list(cols))
        m.insert(0, "port", NAMES.get(p, p))
        parts.append(m)
    return pd.concat(parts).rename_axis("month").reset_index()


def step_month(s):
    """Single least-squares break in the mean: the first month of the higher/lower regime.
    Returns (month, mean_before, mean_after)."""
    best = None
    for i in range(3, len(s) - 2):
        a, b = s.iloc[:i], s.iloc[i:]
        sse = ((a - a.mean()) ** 2).sum() + ((b - b.mean()) ** 2).sum()
        if best is None or sse < best[0]:
            best = (sse, s.index[i], a.mean(), b.mean())
    return best[1], best[2], best[3]


def roro_step(pp, start="2021-01-01", end="2023-12-01"):
    """For each port and call type, the break month in start..end and the means either side."""
    w = pp[(pp["month"] >= start) & (pp["month"] <= end)]
    rows = []
    for port, g in w.groupby("port", sort=False):
        g = g.set_index("month")
        for col in ("roro_calls", "general_cargo_calls", "tanker_calls"):
            mon, before, after = step_month(g[col])
            rows.append({"port": port, "series": col, "break_month": mon.strftime("%Y-%m"),
                         "mean_before": round(before, 1), "mean_after": round(after, 1),
                         "ratio": round(after / before, 2) if before else float("nan")})
    return pd.DataFrame(rows)


def annual(m):
    """Calendar-year totals of complete years only."""
    y = m.groupby(m.index.year)
    return y.sum()[y.size() == 12]
