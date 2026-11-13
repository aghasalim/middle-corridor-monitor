"""Weak aggregate check: Sentinel-1 blobs per pass at Alat vs PortWatch "Baku Port" calls, by month and year.

Not a validation: radar blobs are unlabelled, PortWatch's Baku polygon is unpublished,
and a pass every 4-5 days gives ships present, not calls.
"""
import pandas as pd

sar = pd.read_csv("outputs/tables/sar_monthly.csv")
pw = pd.read_csv("data/portwatch/daily_port100.csv", parse_dates=["date"])
pw["month"] = pw["date"].dt.strftime("%Y-%m")
calls = pw.groupby("month")[["portcalls", "portcalls_tanker", "portcalls_roro"]].sum()
calls["portcalls_dry"] = calls["portcalls"] - calls["portcalls_tanker"]
m = sar.merge(calls, left_on="month", right_index=True)
m = m[m["month"] < "2026-11"]  # November 2026 is a part month in both sources
m.to_csv("outputs/tables/sar_vs_portwatch_monthly.csv", index=False)

rows = []
for zone in ["mean_basin", "mean_roadstead", "mean_total"]:
    for col in ["portcalls", "portcalls_dry", "portcalls_tanker", "portcalls_roro"]:
        rows.append({"sar": zone, "portwatch": col, "n_months": len(m),
                     "pearson": round(m[zone].corr(m[col]), 3),
                     "spearman": round(m[zone].corr(m[col], method="spearman"), 3)})
out = pd.DataFrame(rows)
out.to_csv("outputs/tables/sar_vs_portwatch_summary.csv", index=False)
print(out.to_string(index=False))

m["year"] = m["month"].str[:4]
print(m.groupby("year")[["portcalls", "portcalls_dry", "portcalls_tanker", "portcalls_roro"]].sum())
