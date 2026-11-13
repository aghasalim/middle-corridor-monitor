"""Extra numbers quoted in paper/paper.md that the main tables do not hold. Writes outputs/tables/paper_checks.csv.

Run after `python -m mcm.build --offline`.
"""
import pandas as pd

T = "outputs/tables/"
rows = []


def add(check, key, value):
    rows.append({"check": check, "key": key, "value": round(float(value), 4)})


# 1. Kuryk and AMCT tonnage look transposed in 2020 in the Maritime Administration table.
off = pd.read_csv("data/official/official_figures.csv")
off["year"] = off.period_start.str[:4].astype(int)
full = off[off.period_start.str.endswith("01-01") & off.period_end.str.endswith("12-31")
           & off.source_url.str.contains("stat.gov.kz", na=False)]


def series(entity, metric):
    return full[(full.entity == entity) & (full.metric == metric)].drop_duplicates("year").set_index("year")["value"]


kuryk, amct = series("Kuryk", "tonnes_total"), series("Aktau North Terminal (AMCT)", "tonnes_total")
ferry, kz = series("KZ seaports", "tonnes_ferry"), series("KZ seaports", "tonnes_total")
for y in range(2019, 2026):
    add("ferry_cargo_over_kuryk", y, ferry[y] / kuryk[y])
add("ferry_cargo_over_amct", 2020, ferry[2020] / amct[2020])
add("kuryk_share_2020_as_published", 2020, kuryk[2020] / kz[2020])
add("kuryk_share_2020_if_transposed", 2020, amct[2020] / kz[2020])
share = (kuryk / kz).loc[2019:2025].copy()
share[2020] = amct[2020] / kz[2020]
add("kuryk_share_min_if_transposed", int(share.idxmin()), share.min())

va = pd.read_csv(T + "validate_annual.csv")
a = va[(va.entity == "Aktau incl. AMCT") & (va.metric == "tonnes_total") & (va.pw_measure == "all_tonnes")].set_index("year")
o = a.official.copy()
o[2020] += kuryk[2020] - amct[2020]  # put Kuryk's published figure where AMCT's is
add("aktau_amct_tonnes_if_transposed", "mean_ratio", (a.portwatch / o).mean())
add("aktau_amct_tonnes_if_transposed", "level_r", a.portwatch.corr(o))
add("aktau_amct_tonnes_if_transposed", "yoy_r", a.portwatch.pct_change().corr(o.pct_change()))

# 2. Route total year on year without the 2022 change.
for m in ["roro_calls", "tanker_calls", "dry_calls"]:
    r = va[(va.entity == "TITR (Kazakh ministry series)") & (va.pw_measure == m) & (va.year != 2022)].dropna(subset=["official_yoy"])
    add("route_total_yoy_r_without_2022", f"{m} (n={len(r)})", r.official_yoy.corr(r.portwatch_yoy))

# 3. Black Sea comparator and the early-2021 Ro-Ro trough at Poti.
ann = pd.read_csv(T + "index_annual.csv").set_index("year")
add("blacksea_dry_calls_change_2021_2022", "pct", ann.blacksea_dry_calls[2022] / ann.blacksea_dry_calls[2021] - 1)
add("caspian_dry_calls_change_2021_2022", "pct", ann.caspian_dry_calls[2022] / ann.caspian_dry_calls[2021] - 1)
add("caspian_roro_calls_change_2021_2022", "pct", ann.caspian_roro_calls[2022] / ann.caspian_roro_calls[2021] - 1)
pp = pd.read_csv(T + "index_per_port_monthly.csv", parse_dates=["month"])
pp["year"] = pp.month.dt.year
for y, v in pp[pp.port == "Poti"].groupby("year").roro_calls.sum().loc[2019:2022].items():
    add("poti_roro_calls", y, v)
z = pp[(pp.port == "Poti") & (pp.month >= "2020-12-01") & (pp.month <= "2021-03-01")]
add("poti_roro_calls", "2020-12..2021-03", z.roro_calls.sum())
gc = pp[pp.port.isin(["Baku", "Aktau", "Turkmenbashi"])].groupby("year").general_cargo_calls.sum()
for y in range(2019, 2024):
    add("caspian_general_cargo_calls", y, gc[y])

# 4. Official ferry growth 2021 -> 2022 (Kazakh port table).
add("kuryk_ferry_calls_change_2021_2022", "pct", series("Kuryk", "ferry_calls")[2022] / series("Kuryk", "ferry_calls")[2021] - 1)
add("kuryk_tonnes_change_2021_2022", "pct", kuryk[2022] / kuryk[2021] - 1)

# 5. Turkmenbashi, the one official year.
t = pp[(pp.port == "Turkmenbashi") & (pp.year == 2025)]
pw_t = t.dry_tonnes.sum() + t.tanker_tonnes.sum()
off_t = off[(off.entity == "Turkmenbashi") & (off.metric == "tonnes_total")].value.iloc[0]
add("turkmenbashi_2025", "portwatch_tonnes", pw_t)
add("turkmenbashi_2025", "official_tonnes", off_t)
add("turkmenbashi_2025", "ratio", pw_t / off_t)

# 6. Sentinel-1A against 1D in 2026 at Alat (roadstead blobs per counted pass).
s = pd.read_csv(T + "sar_scene_counts.csv", parse_dates=["datetime"])
s = s[(s.status == "counted") & (s.datetime.dt.year == 2026)]
for plat, g in s.groupby("platform"):
    add("s1_2026_roadstead_mean", plat, g.n_roadstead.mean())
    print(plat, "first", g.datetime.min().date(), "last", g.datetime.max().date(), "passes", len(g))
a26 = s[s.platform == "SENTINEL-1A"]
for mth, v in a26.groupby(a26.datetime.dt.strftime("%Y-%m")).n_roadstead.mean().items():
    add("s1a_2026_roadstead_monthly_mean", mth, v)
d0 = s[s.platform != "SENTINEL-1A"].datetime.min()
add("s1a_passes_after_first_s1d_pass", "n", (a26.datetime > d0).sum())

out = pd.DataFrame(rows)
out.to_csv(T + "paper_checks.csv", index=False)
print(out.to_string(index=False))
