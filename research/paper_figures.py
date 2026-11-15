"""Two validation figures for the paper, drawn from outputs/tables/validate_*.csv.

    .venv/Scripts/python research/paper_figures.py      (after `python -m mcm.build --offline`)

Writes outputs/figures/validation_annual.png and outputs/figures/validation_monthly.png.
"""
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt  # noqa: E402
import pandas as pd  # noqa: E402

import mcm  # noqa: E402,F401  (registers the Inter font)

T, F = "outputs/tables/", "outputs/figures/"
CITE = "Sources: Kpler; UN Global Platform; IMF PortWatch (portwatch.imf.org); official figures in data/official/."
NOTE = " Preliminary, not peer reviewed."

va = pd.read_csv(T + "validate_annual.csv")


def pair(entity, metric, measure):
    r = va[(va.entity == entity) & (va.metric == metric) & (va.pw_measure == measure)].set_index("year")
    assert len(r), (entity, metric, measure)
    return r


# Left: PortWatch / official by year for four pairs of Table 3. Right: year-on-year changes, route total vs headline.
RATIOS = [
    ("Aktau incl. AMCT", "vessel_calls", "all_calls", "Aktau + AMCT: vessel calls vs all calls"),
    ("Aktau", "tonnes_oil", "tanker_tonnes", "Aktau: oil tonnes vs tanker tonnes"),
    ("Aktau", "tonnes_total", "all_tonnes", "Aktau: total tonnes vs all tonnes"),
    ("Port of Baku", "tonnes_total", "dry_tonnes", "Port of Baku: total tonnes vs dry tonnes"),
]
fig, (a, b) = plt.subplots(1, 2, figsize=(10, 4.2), gridspec_kw={"width_ratios": [1.15, 1]})
for (ent, met, mea, lab), mk in zip(RATIOS, "osD^"):
    r = pair(ent, met, mea).ratio_pw_over_official.dropna()
    a.plot(r.index, r.values, marker=mk, linewidth=1.4, label=lab)
a.axhline(1, color="#999", linewidth=0.8, linestyle=":")
a.set_ylim(0, 1.25)
a.set_title("PortWatch divided by official, by year", loc="left", fontsize=11)
a.set_ylabel("Ratio (1 = same level)")
a.set_xlabel("Year")
a.grid(alpha=0.3)
a.legend(frameon=False, fontsize=8, loc="lower left", bbox_to_anchor=(0, 0.2))  # in the empty band above the Baku line

r = pair("TITR (Kazakh ministry series)", "tonnes_total", "dry_calls").dropna(subset=["official_yoy", "portwatch_yoy"])
x = r.index.to_numpy()
b.bar(x - 0.2, 100 * r.official_yoy, width=0.4, label="Route total (Kazakh ministry), tonnes")
b.bar(x + 0.2, 100 * r.portwatch_yoy, width=0.4, label="Headline: non-tanker calls, three ports")
b.axhline(0, color="#444", linewidth=0.8)
b.set_ylim(-35, 195)  # room for the legend above the 2022 bar
b.set_title("Year-on-year change: route total and headline", loc="left", fontsize=11)
b.set_ylabel("Change on previous year, %")
b.set_xlabel("Year")
b.set_xticks(x)
b.grid(alpha=0.3, axis="y")
b.legend(frameon=False, fontsize=8)
fig.tight_layout(rect=(0, 0.05, 1, 1))
fig.text(0.01, 0.01, CITE + NOTE, fontsize=7, color="#444")
fig.savefig(F + "validation_annual.png", dpi=150)
plt.close(fig)

# Monthly out-of-sample test: official Kazakh sea-transport series and the three forecasts.
vm = pd.read_csv(T + "validate_monthly.csv", parse_dates=["month"])
o = vm.dropna(subset=["fc_portwatch", "fc_last_year", "fc_previous"])
fig, ax = plt.subplots(figsize=(10, 3.8))
ax.plot(o.month, o.official / 1e3, color="#111", linewidth=2, marker="o", markersize=3, label="Official (cargo carried by Kazakh sea transport)")
ax.plot(o.month, o.fc_portwatch / 1e3, linewidth=1.4, label="Forecast: regression on PortWatch tonnes at Aktau")
ax.plot(o.month, o.fc_last_year / 1e3, linewidth=1.2, linestyle="--", label="Forecast: same month a year earlier")
ax.plot(o.month, o.fc_previous / 1e3, linewidth=1.2, linestyle=":", label="Forecast: previous available month")
ax.set_ylim(bottom=0)
ax.set_title(f"Monthly out-of-sample test, {o.month.min():%B %Y} to {o.month.max():%B %Y} ({len(o)} months)", loc="left", fontsize=11)
ax.set_ylabel("Thousand tonnes")
ax.set_xlabel("Month")
ax.grid(alpha=0.3)
ax.legend(frameon=False, fontsize=8, ncol=2, loc="lower left")
fig.tight_layout(rect=(0, 0.05, 1, 1))
fig.text(0.01, 0.01, CITE + NOTE, fontsize=7, color="#444")
fig.savefig(F + "validation_monthly.png", dpi=150)
plt.close(fig)
print("wrote", F + "validation_annual.png", F + "validation_monthly.png", "oos months:", len(o))
