"""The coverage break PortWatch documents (FAQ: Gwangyang, November 2021) against the three Caspian ports.

Writes outputs/tables/coverage_break_check.csv. The Caspian rows come from the build's tables; the Gwangyang
(port432) rows need a download. On 14 Nov 2026 the public service answered 429 (quota) for over ten minutes, so
the Gwangyang rows were not produced that day: run again with `--gwangyang`.
Run after `python -m mcm.build --offline`.
"""
import sys

import pandas as pd

OUT = "outputs/tables/coverage_break_check.csv"
rows = []
c = pd.read_csv("outputs/tables/index_per_port_monthly.csv")
c = c[c.port.isin(["Baku", "Aktau", "Turkmenbashi"]) & (c.month >= "2021-01") & (c.month < "2022-03")]
c = c.assign(all=c.dry_calls + c.tanker_calls, period=c.month.str[:7])
cm = c.groupby("period")[["all", "roro_calls", "tanker_calls", "general_cargo_calls"]].sum()
assert len(cm) == 14, len(cm)  # January 2021 to February 2022
for month, r in cm.iterrows():
    for k, col in {"all": "all", "roro": "roro_calls", "tanker": "tanker_calls", "general_cargo": "general_cargo_calls"}.items():
        rows.append({"place": "Caspian three ports", "period": month, "series": k, "calls": int(r[col])})
rows.append({"place": "Caspian three ports", "period": "mean 2021-01..2021-10", "series": "all", "calls": round(cm["all"][:"2021-10"].mean(), 1)})
rows.append({"place": "Caspian three ports", "period": "mean 2021-11..2022-02", "series": "all", "calls": round(cm["all"]["2021-11":].mean(), 1)})

if "--gwangyang" in sys.argv:
    from mcm.portwatch import fetch_port
    g = fetch_port("port432")
    g["date"] = pd.to_datetime(g["date"])
    g = g[(g.date >= "2021-07-01") & (g.date <= "2022-02-28")]
    types = {"all": "portcalls", "roro": "portcalls_roro", "tanker": "portcalls_tanker",
             "general_cargo": "portcalls_general_cargo", "container": "portcalls_container"}
    gm = g.groupby(g.date.dt.strftime("%Y-%m"))[list(types.values())].sum()
    assert len(gm) == 8, len(gm)
    for month, r in gm.iterrows():
        for k, col in types.items():
            rows.append({"place": "Gwangyang", "period": month, "series": k, "calls": int(r[col])})
    for d, v in g[(g.date >= "2021-11-05") & (g.date <= "2021-11-12")].set_index("date").portcalls.items():
        rows.append({"place": "Gwangyang", "period": d.strftime("%Y-%m-%d"), "series": "all", "calls": int(v)})

out = pd.DataFrame(rows)
out.to_csv(OUT, index=False)
print(out[out.series == "all"].tail(4).to_string(index=False))
