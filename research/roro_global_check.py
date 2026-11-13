"""Is the 2021-22 Ro-Ro step global? Monthly Ro-Ro, general-cargo and all port calls summed over every PortWatch port."""
import json, sys, urllib.parse, urllib.request
import pandas as pd

URL = "https://services9.arcgis.com/weJ1QsnbMYJlCHdG/arcgis/rest/services/Daily_Ports_Data/FeatureServer/0/query"
stats = [{"statisticType": "sum", "onStatisticField": f, "outStatisticFieldName": n}
         for f, n in (("portcalls_roro", "roro_calls"), ("portcalls_general_cargo", "general_cargo_calls"), ("portcalls", "all_calls"))]
q = urllib.parse.urlencode({"where": "year IN (2020,2021,2022)", "groupByFieldsForStatistics": "year,month",
                            "outStatistics": json.dumps(stats), "orderByFields": "year,month", "f": "json"})
with urllib.request.urlopen(f"{URL}?{q}", timeout=180) as r:
    d = json.load(r)
if "error" in d:
    sys.exit(str(d["error"]))
t = pd.DataFrame([f["attributes"] for f in d["features"]])
assert len(t) == 36, len(t)
t.to_csv("outputs/tables/index_roro_global_2020_2022.csv", index=False)
h1, h2 = t[(t.year == 2021) & (t.month <= 6)].roro_calls.mean(), t[(t.year == 2022)].roro_calls.mean()
print(f"world Ro-Ro calls per month: Jan-Jun 2021 mean {h1:.0f}, 2022 mean {h2:.0f}, ratio {h2 / h1:.2f}")
