# Middle Corridor Monitor

Status: **local draft, nothing published.** Preliminary. Not peer reviewed.

Authors: Aghasalim Mustafazada; Teymur Eyvazov (co-author to be confirmed before publication)

## Purpose

An open, monthly, independently checkable measure of cargo crossing the Caspian leg of the
Middle Corridor. The headline series is the monthly count of non-tanker port calls (container,
dry bulk, general cargo, Ro-Ro) at Baku, Aktau and Turkmenbashi, indexed to the 2019 monthly
mean = 100. Ro-Ro calls, tanker calls, PortWatch dry tonnage and a Black Sea comparator
(Poti + Batumi) are reported alongside it.

## Data sources

- IMF PortWatch daily port data (ArcGIS feature service `Daily_Ports_Data`), ports Baku
  (port100), Aktau (port16), Turkmenbashi (port1330), Poti (port1016), Batumi (port127).
  Sources: UN Global Platform; IMF PortWatch (portwatch.imf.org).
- Official figures for validation (Port of Baku, Kazakh seaports, TITR route) in
  `data/official/official_figures.csv`, each row with its source URL and date.

The download date and the first/last day per port are in `data/portwatch/snapshot.json`.

## How to reproduce

```
python -m venv .venv
.venv/Scripts/python -m pip install -r requirements.txt
.venv/Scripts/python -m pip install -e .
.venv/Scripts/python -m mcm.build            # downloads PortWatch, then builds everything
.venv/Scripts/python -m mcm.build --offline  # reuses data/portwatch/
.venv/Scripts/python -m pytest -q
```

(On macOS/Linux use `.venv/bin/python`.) The build fails loudly if a port's download is short,
has a duplicated day or a missing day.

## Repository layout

| Path | What |
|---|---|
| `src/mcm/portwatch.py` | download and check PortWatch daily data |
| `src/mcm/index.py` | monthly aggregation, 2019 = 100 indices, rolling 12-month sum, Ro-Ro step diagnostic |
| `src/mcm/validate.py` | comparison with official figures (cumulative releases to increments, same-period sums, ratios, YoY growth, Pearson/Spearman with n) |
| `src/mcm/build.py` | runs everything and writes outputs and the page |
| `src/mcm/page.py` | writes `docs/index.html` |
| `src/mcm/sar/` | Sentinel-1 detection at Alat: `fetch`, `run`, `report` (see `research/SAR_METHOD.md`) |
| `research/` | research notes, literature, references, one-off check scripts |
| `paper/` | draft paper |
| `data/portwatch/` | daily CSV per port + snapshot.json |
| `data/official/` | official figures |
| `outputs/tables/` | `index_*.csv`, `validate_*.csv`, `sar_*.csv` |
| `outputs/figures/` | `index_*.png`, `sar_*.png` |
| `docs/` | static page for GitHub Pages (generated) |
| `tests/` | pytest, synthetic data only |

## Limitations

- Kuryk, Kazakhstan's ferry port, is not in PortWatch, so it is missing from the index.
- The boundary of PortWatch's "Baku Port" is not published; whether it includes Alat is unknown.
- Ferry cargo is poorly captured: rail ferries may not be classed as Ro-Ro, and PortWatch
  dry-cargo tonnage at Baku is several times below official figures.
- Ro-Ro calls step up four- to sixfold between 2021 and 2022 at all three Caspian ports at once.
  This is not explained (see `outputs/tables/index_roro_step.csv` and `outputs/figures/index_roro_step.png`).
- Sentinel-1 radar detections at Alat exist (`research/SAR_METHOD.md`, `outputs/tables/sar_*.csv`) but are
  unlabelled bright blobs, not confirmed ships. Precision and recall are unknown until the sample in
  `data/sar/label_sample.csv` is labelled by hand.
- In checks against official figures the index does not track the official Trans-Caspian route total year on
  year and does not forecast Kazakhstan's monthly sea-cargo series (`outputs/tables/validate_*.csv`).
- Port calls are counted, not tonnes or containers; a call by a large ship and a small one count the same.

## Licence

To be decided before publication.
