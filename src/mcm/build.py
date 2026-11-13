"""python -m mcm.build [--offline]: download, compute, write tables, figures and docs/index.html."""
import argparse
import json
from pathlib import Path

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt  # noqa: E402

from mcm import index as ix, page, portwatch, validate  # noqa: E402

ROOT = Path(__file__).resolve().parents[2]
TABLES = ROOT / "outputs" / "tables"
FIGS = ROOT / "outputs" / "figures"
CITE = "Sources: UN Global Platform; IMF PortWatch (portwatch.imf.org)."


def footer(fig, last):
    fig.text(0.01, 0.01, f"{CITE} Data to {last}. Preliminary, not peer reviewed.", fontsize=7, color="#444")


def line_chart(df, cols, labels, title, ylabel, path, last):
    fig, ax = plt.subplots(figsize=(9, 4.5))
    for c, lab in zip(cols, labels):
        ax.plot(df.index, df[c], label=lab, linewidth=1.6)
    ax.axhline(100, color="#999", linewidth=0.8, linestyle=":")
    ax.set_title(title, loc="left", fontsize=12)
    ax.set_ylabel(ylabel)
    ax.set_xlabel("Month")
    ax.grid(alpha=0.3)
    ax.legend(frameon=False, fontsize=9)
    fig.tight_layout(rect=(0, 0.04, 1, 1))
    footer(fig, last)
    fig.savefig(path, dpi=130)
    plt.close(fig)


def roro_chart(pp, path, last):
    w = pp[(pp["month"] >= "2021-01-01") & (pp["month"] <= "2023-12-01")]
    fig, axes = plt.subplots(3, 1, figsize=(9, 7), sharex=True)
    for ax, (port, g) in zip(axes, w.groupby("port", sort=False)):
        for col, lab in [("roro_calls", "Ro-Ro"), ("general_cargo_calls", "General cargo"), ("tanker_calls", "Tanker")]:
            ax.plot(g["month"], g[col], label=lab, linewidth=1.5)
        ax.set_title(port, loc="left", fontsize=10)
        ax.set_ylabel("Calls per month")
        ax.grid(alpha=0.3)
    axes[0].legend(frameon=False, fontsize=8, ncol=3)
    axes[-1].set_xlabel("Month")
    fig.suptitle("Monthly port calls by ship type, 2021-2023", x=0.01, ha="left")
    fig.tight_layout(rect=(0, 0.03, 1, 1))
    footer(fig, last)
    fig.savefig(path, dpi=130)
    plt.close(fig)


def main(argv=None):
    ap = argparse.ArgumentParser()
    ap.add_argument("--offline", action="store_true", help="reuse data/portwatch instead of downloading")
    a = ap.parse_args(argv)
    if not a.offline:
        portwatch.download()
    snap = json.loads((portwatch.DATA_DIR / "snapshot.json").read_text())
    dailies = portwatch.load()
    last = min(p["last"] for p in snap["ports"].values())

    s = ix.series(dailies)
    pp = ix.per_port(dailies)
    caspian_pp = pp[pp["port"].isin([ix.NAMES[p] for p in ix.CASPIAN])]
    step = ix.roro_step(caspian_pp)
    base_cols = ["caspian_dry_calls", "caspian_roro_calls", "caspian_tanker_calls",
                 "caspian_dry_tonnes", "blacksea_dry_calls"]
    yearly = ix.annual(s[base_cols]).rename_axis("year")
    roro_wide = (caspian_pp[(caspian_pp["month"] >= "2021-01-01") & (caspian_pp["month"] <= "2023-12-01")]
                 .pivot(index="month", columns="port", values="roro_calls"))

    TABLES.mkdir(parents=True, exist_ok=True)
    FIGS.mkdir(parents=True, exist_ok=True)
    s.round(2).to_csv(TABLES / "index_monthly.csv")
    pp.to_csv(TABLES / "index_per_port_monthly.csv", index=False, float_format="%.1f")
    yearly.round(0).astype(int).to_csv(TABLES / "index_annual.csv")
    roro_wide.to_csv(TABLES / "index_roro_2021_2023.csv")
    step.to_csv(TABLES / "index_roro_step.csv", index=False)

    line_chart(s, ["caspian_dry_calls_index", "caspian_roro_calls_index"],
               ["Non-tanker calls (headline)", "Ro-Ro calls"],
               "Caspian non-tanker port calls: Baku, Aktau, Turkmenbashi",
               "Index, 2019 monthly mean = 100", FIGS / "index_headline.png", last)
    line_chart(s, ["caspian_dry_calls_index", "blacksea_dry_calls_index", "caspian_tanker_calls_index"],
               ["Caspian non-tanker calls", "Black Sea non-tanker calls (Poti + Batumi)", "Caspian tanker calls"],
               "Caspian index against the Black Sea comparator and tanker calls",
               "Index, 2019 monthly mean = 100", FIGS / "index_comparator.png", last)
    roro_chart(caspian_pp, FIGS / "index_roro_step.png", last)

    print("\nAnnual totals (complete years):")
    print(yearly.round(0).astype(int).to_string())
    print("\nLatest 12 complete months:")
    print(s[["caspian_dry_calls", "caspian_dry_calls_index", "caspian_roro_calls", "blacksea_dry_calls_index"]]
          .tail(12).round(1).to_string())
    print("\nRo-Ro step (single break in the mean, 2021-01..2023-12):")
    print(step.to_string(index=False))

    print()
    validate.run(dailies)
    page.write(s, step, snap, FIGS, ROOT / "docs")


if __name__ == "__main__":
    main()
