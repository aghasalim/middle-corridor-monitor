"""Write docs/index.html (static, no external resources) from the build's outputs."""
import html
import shutil

import pandas as pd

CITE = "Sources: Kpler; UN Global Platform; IMF PortWatch (portwatch.imf.org)."
AUTHORS = "Aghasalim Mustafazada (Howest University of Applied Sciences, Belgium); Teymur Eyvazov (University of Massachusetts Boston, USA)"
CSS = """
:root{--fg:#1a1a1a;--muted:#555;--bg:#fff;--line:#ddd;--warn:#fff4d6;--warnline:#c99a00}
@media (prefers-color-scheme:dark){:root{--fg:#eee;--muted:#aaa;--bg:#141414;--line:#333;--warn:#3a3000;--warnline:#c99a00}
img{background:#fff}}
body{margin:0;background:var(--bg);color:var(--fg);font:16px/1.55 system-ui,-apple-system,"Segoe UI",sans-serif}
main{max-width:860px;margin:0 auto;padding:16px}
.banner{background:var(--warn);border-left:4px solid var(--warnline);padding:8px 12px;font-weight:600}
h1{font-size:1.6rem;margin:.8em 0 .2em}h2{font-size:1.2rem;margin-top:1.8em}
.muted{color:var(--muted);font-size:.9rem}
img{max-width:100%;height:auto;border:1px solid var(--line)}
.tw{overflow-x:auto}table{border-collapse:collapse;width:100%;font-variant-numeric:tabular-nums}
th,td{padding:4px 8px;border-bottom:1px solid var(--line);text-align:right}
th:first-child,td:first-child{text-align:left}
"""


def write(s, step, snap, fig_dir, docs):
    docs.mkdir(parents=True, exist_ok=True)
    for f in ("index_headline.png", "index_comparator.png", "index_roro_step.png"):
        shutil.copy(fig_dir / f, docs / f)
    last = min(p["last"] for p in snap["ports"].values())
    last_month = s.index[-1].strftime("%B %Y")
    rows = "".join(
        f"<tr><td>{m:%Y-%m}</td><td>{r.caspian_dry_calls:.0f}</td><td>{r.caspian_dry_calls_index:.1f}</td>"
        f"<td>{r.caspian_roro_calls:.0f}</td><td>{r.blacksea_dry_calls_index:.1f}</td></tr>"
        for m, r in s.tail(12).iterrows())
    steps = "; ".join(f"{r.port} {r.break_month}" for r in step[step.series == "roro_calls"].itertuples())
    e = html.escape
    tables = fig_dir.parent / "tables"
    vs = pd.read_csv(tables / "validate_summary.csv").set_index(["entity", "metric", "pw_measure"])
    titr = vs.loc[("TITR (Kazakh ministry series)", "tonnes_total", "dry_calls")]
    aktau = vs.loc[("Aktau incl. AMCT", "vessel_calls", "all_calls")]
    mo = pd.read_csv(tables / "validate_monthly_summary.csv").iloc[0]
    checks = f"""<h2>Checks against official figures</h2>
<ul>
<li>The index does not track the official Trans-Caspian route total. Over {titr.level_n:.0f} years both rise
(correlation of levels {titr.level_pearson:.2f}), but year-on-year changes are unrelated
(correlation {titr.yoy_pearson:.2f}, {titr.yoy_n:.0f} pairs).</li>
<li>It does not forecast Kazakhstan's monthly "cargo carried by sea transport" series. Over {mo.oos_months:.0f}
out-of-sample months the error (RMSE, tonnes) was {mo.rmse_portwatch:,.0f} with PortWatch, {mo.rmse_last_year:,.0f}
using the same month a year earlier and {mo.rmse_previous:,.0f} using the previous month.</li>
<li>Where the definitions match, PortWatch is close: its ship calls at Aktau average {aktau.mean_ratio:.2f} of the
calls reported by the Kazakh maritime administration over {aktau.years_with_both:.0f} years.</li>
</ul>
<p class="muted">Samples are short and these checks are preliminary. Full tables: outputs/tables/validate_*.csv.</p>
"""
    page = f"""<!doctype html>
<html lang="en"><head><meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<title>Middle Corridor Monitor</title>
<style>{CSS}</style></head>
<body><main>
<img src="banner.png" alt="Mean Sentinel-1 radar image of the Port of Baku at Alat, 2019 to 2026. Contains modified Copernicus Sentinel data.">
<p class="banner" role="note">Preliminary. Not peer reviewed.</p>
<h1>Middle Corridor Monitor</h1>
<p class="muted">{e(AUTHORS)}</p>
<video src="monitor.mp4" controls muted loop playsinline style="max-width:100%;height:auto" aria-label="Animation, January 2019 to October 2026: radar detections at the Port of Baku at Alat next to the port-call index"></video>
<p class="muted">One frame per month. Left: radar detections at Alat (bright objects on the water, not confirmed ships). Right: the index up to that month.</p>
<p>A monthly count of non-tanker ship calls at Baku, Aktau and Turkmenbashi, built from IMF PortWatch data, as an open
and checkable indicator of cargo crossing the Caspian leg of the Middle Corridor. Every number on this page is produced
by the code in this repository from a dated data snapshot.</p>
<p class="muted">Last data day: {e(last)}. Last complete month: {e(last_month)}. Data downloaded {e(snap['downloaded_utc'])}.</p>

<h2>Headline index</h2>
<img src="index_headline.png" alt="Line chart of the Caspian non-tanker port-call index and the Ro-Ro call index, 2019 monthly mean = 100, from January 2019 to {e(last_month)}.">

<h2>Latest 12 months</h2>
<div class="tw"><table>
<caption class="muted">Calls per month summed over Baku, Aktau and Turkmenbashi; index 2019 monthly mean = 100.</caption>
<thead><tr><th scope="col">Month</th><th scope="col">Non-tanker calls</th><th scope="col">Index</th>
<th scope="col">Ro-Ro calls</th><th scope="col">Black Sea index</th></tr></thead>
<tbody>{rows}</tbody></table></div>

<h2>Comparator</h2>
<img src="index_comparator.png" alt="Line chart comparing the Caspian non-tanker index with the Poti plus Batumi non-tanker index and Caspian tanker calls, 2019 = 100.">
<p>Poti and Batumi (Black Sea, Georgia) are shown for comparison only; they are not part of the Caspian index.
Tanker calls are reported separately and are not in the headline.</p>

{checks}
<h2>What this does not measure</h2>
<ul>
<li>Kuryk, Kazakhstan's ferry port, is not in PortWatch, so it is missing from the index.</li>
<li>The area PortWatch calls "Baku Port" is not published; whether it includes Alat is unknown.</li>
<li>Ferry cargo is poorly captured: rail ferries may not be classed as Ro-Ro, and PortWatch dry-cargo tonnage at Baku
is several times below official figures. Calls are counted, not tonnes or containers.</li>
<li>Ro-Ro calls step up four- to sixfold between 2021 and 2022 at all three ports at once. The cause is not
explained (single-break estimate of the first month of the higher level: {e(steps)}).</li>
<li>No hand-validated radar (Sentinel-1) ship counts exist yet.</li>
</ul>
<img src="index_roro_step.png" alt="Three panels of monthly Ro-Ro, general cargo and tanker calls at Baku, Aktau and Turkmenbashi, 2021 to 2023.">

<h2>Data</h2>
<p>{e(CITE)}</p>
<p class="muted">Daily port calls by ship type from the PortWatch Daily_Ports_Data service, ports Baku (port100),
Aktau (port16), Turkmenbashi (port1330), Poti (port1016), Batumi (port127). Code: MIT licence. Text and figures: CC BY 4.0. Repository: <a href="https://github.com/aghasalim/middle-corridor-monitor">https://github.com/aghasalim/middle-corridor-monitor</a>.</p>
</main></body></html>
"""
    (docs / "index.html").write_text(page, encoding="utf-8")
    print(f"page: wrote {docs / 'index.html'}")
