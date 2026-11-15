# experimental_log.md — Middle Corridor Monitor (PaperOrchestra input 2 of 2)

Every number below is copied from a file in the repository; the file is named for each block. Row numbers in
`paper/NUMBERS.md` trace each one further. Nothing here was re-run except `research/paper_figures.py`
(new figures, same tables) and the build and checks listed at the end.

## 1. Data

PortWatch (`data/portwatch/snapshot.json`): download 13 November 2026; five ports, Baku (port100), Aktau
(port16), Turkmenbashi (port1330), Poti (port1016), Batumi (port127); 2,867 days per port, 1 January 2019 to
6 November 2026. Five ship types: container, dry bulk, general cargo, Ro-Ro, tanker. No passenger type.
Kuryk is not in PortWatch. Port polygons are not published. "Baku Port" point 40.2846 N, 49.7325 E, about
43 km from Alat (author estimate). PortWatch tanker tonnage at Baku = 2.4 to 3.4 times the Port of Baku's
oil tonnage in 2021, 2023, 2024 (`validate_periods.csv`).

Official figures (`data/official/official_figures.csv`): 517 rows; 433 opened at source, 77 carried over
(step1), 7 snippet only. About half (264 distinct values plus 24 derived increments) can be set against a
PortWatch period. Kazakhstan monthly "cargo carried by sea transport": 10 of 48 months of 2019-2022 published.
Azerbaijan 2025: 12.96 Mt handled in seaports, 9.09 Mt carried by sea transport. Kazakh seaports 2025:
7.453 Mt (port table) vs 8 Mt (press). Route total 2025: 4.119 Mt (ministry) vs 1.867 Mt (association chart);
2024: 4.484 Mt (ministry), 1.857 Mt (chart), 3.3 Mt (association press release).

Sentinel-1 (`research/s1_revisit.json`, `outputs/tables/sar_*.csv`): passes per year 2019-2026: Alat 79-93,
Aktau 53-63, Kuryk 78-93, Turkmenbashi 106-122. All S1A up to 2024; 2026 Alat 34 of 79 from S1D. Planetary
Computer holds 672 of 703 catalogue passes; 31 missing (10 in 2024); 1 partial; 671 counted. Mean gap 4.3 days,
longest 18.5 days. Kuryk 692 passes 2019-2026 vs Alat 703.

## 2. Index (`outputs/tables/index_annual.csv`, `index_monthly.csv`)

94 complete months, January 2019 to October 2026.

| Year | Non-tanker calls | Index | Ro-Ro | Tanker | Dry Mt | Poti+Batumi |
|---|---|---|---|---|---|---|
| 2019 | 1,442 | 100.0 | 240 | 1,070 | 1.24 | 1,122 |
| 2020 | 1,666 | 115.5 | 262 | 1,104 | 1.27 | 1,020 |
| 2021 | 2,051 | 142.2 | 244 | 1,052 | 1.73 | 847 |
| 2022 | 2,621 | 181.8 | 946 | 1,481 | 2.25 | 1,006 |
| 2023 | 2,215 | 153.6 | 1,006 | 1,715 | 1.84 | 991 |
| 2024 | 2,298 | 159.4 | 894 | 1,472 | 2.09 | 1,031 |
| 2025 | 2,486 | 172.4 | 778 | 1,293 | 2.28 | 1,114 |

Index mean Jan-Oct 2026: 206; maximum June 2026, 309 calls, index 257. Black Sea +19% in 2022 vs Caspian +28%.
2021-22: Ro-Ro +702, all non-tanker +570, other three types -132.

## 3. Ro-Ro step (`index_roro_step.csv`, `index_roro_2021_2023.csv`, `paper_checks.csv`, `coverage_break_check.csv`)

Single break in the mean, least squares, Jan 2021-Dec 2023: Baku 2021-12 (8.0 -> 41.8, x5.22), Aktau 2022-01
(2.3 -> 13.8, x5.89), Turkmenbashi 2021-11 (5.5 -> 25.0, x4.55). Ro-Ro per year 2019-2023: Baku 126, 131, 119,
496, 518; Aktau 36, 35, 28, 147, 183; Turkmenbashi 78, 96, 97, 303, 305; all 240, 262, 244, 946, 1,006.
Jan-Jun 2021: 28 calls (Aktau 0); Jul-Dec 2021: 216. Poti: 0 Dec 2020-Mar 2021; 18 in 2021, 42 in 2020, 46 in 2022.
All PortWatch ports Ro-Ro: 103,762 (2021), 106,384 (2022). General cargo break ratios 0.75, 0.59, 0.46;
breaks 2022-09 Baku, 2021-07 Aktau, 2022-10 Turkmenbashi. Kuryk ferry calls 412 -> 618 (+50%), Kuryk tonnes
+87%, PortWatch three-port Ro-Ro +288%. Port of Baku: wagons 44,175 (2019), 37,300 (2023); wheeled vehicles
33,671 (2019), trucks 54,200 (2023). Aktau official ferry calls 2-22 a year (2019-2024) vs PortWatch Ro-Ro 28-183.
Three-port Ro-Ro 2 a month Mar-May 2021, 20 Jul, 33 Aug, 61 Dec. All calls mean 250/month Jan-Oct 2021, 306 Nov
2021-Feb 2022. 14 ferries identified; none listed as Ro-Ro cargo built or delivered 2021-22.

## 4. Annual validation (`validate_summary.csv`, `validate_annual.csv`; 56 pairs, 2019-2025)

| Official | PortWatch | Mean ratio | r levels (n) | r yoy (n) |
|---|---|---|---|---|
| Aktau + AMCT vessel calls | all calls, Aktau | 0.97 | 0.90 (7) | -0.16 (6) |
| Aktau vessel calls | all calls, Aktau | 1.28 | 0.87 (7) | -0.39 (6) |
| Aktau oil tonnes | tanker tonnes | 0.97 | 0.85 (6) | 0.89 (5) |
| Aktau oil tonnes | tanker calls | | 0.999 (6) | 0.99 (5) |
| Aktau total tonnes | all tonnes | 0.82 | 0.75 (7) | 0.53 (6) |
| Aktau + AMCT total tonnes | all tonnes | 0.67 | 0.57 (7) | 0.16 (6) |
| Kazakh seaports total | all tonnes, Aktau | 0.51 | 0.81 (7) | 0.59 (6) |
| Port of Baku total | dry tonnes, Baku | 0.12 | 0.90 (7) | 0.30 (6) |
| Port of Baku total | all tonnes, Baku | 0.77 | 0.66 (7) | 0.50 (6) |
| Route total (ministry) | non-tanker calls | | 0.60 (7) | -0.05 (6) |
| Route total (ministry) | Ro-Ro calls | | 0.73 (7) | 0.79 (6) |
| Route total (ministry) | tanker calls | | 0.60 (7) | 0.80 (6) |

Transposed 2020 variant: 0.69, 0.65 (7), 0.20 (6). Aktau+AMCT calls 2025: 1,383 vs 1,394; ratio 0.98-1.04 in six
of seven years; 2020 748 vs 983. Aktau oil ratio 0.97-1.08 in 2019-2023, 0.77 in 2024. Aktau total 0.71 in 2025.
Baku 2022: World Bank 6.3 Mt at Alat, 2.5 Mt railcars, 1.1 Mt trucks; PortWatch dry 1.03 Mt. 2024: port dry
cargo 1.044 Mt vs PortWatch 1.00 Mt. Jan-Sep 2026: 1.73 Mt vs 1.02 Mt (0.59). Route total yoy +153% (2022),
+86% (2023); non-tanker calls +28%, -15%. Without 2022: Ro-Ro 0.27, tanker 0.42 (n = 5), headline -0.90.
Baku non-tanker calls vs Port of Baku total tonnes: levels 0.88 (7), yoy 0.30. Turkmenbashi 2025: PortWatch 9%.

## 5. Monthly out-of-sample test (`validate_monthly_summary.csv`, `validate_monthly.csv`)

54 months Feb 2019-Oct 2026; level r 0.06; yoy r -0.23 (n = 34). Expanding-window regression after 24 months:
30 out-of-sample months May 2024-Oct 2026. RMSE (thousand tonnes): PortWatch 144.1, same month a year earlier
104.1, previous available month 54.9. PortWatch forecast below official in all 30 months. Official 34-90 kt/month
in 2019, 228-467 kt in 2025.

## 6. Kuryk (`validate_blind_spot.csv`, `paper_checks.csv`)

Kuryk share of Kazakh seaport tonnage 18-30% (2020 12.5% as published, 29.2% if Kuryk and AMCT are transposed;
1,560.1 kt). Ferry calls 412-700 (2019-2024). Ferry cargo = Kuryk tonnage within 0.5% in other years, = AMCT
in 2020. Aktau strategy p. 7: Kuryk 1,560 kt, North Terminal 667 kt. Ferries: 8 of 14 Passenger/Ro-Ro (5
broadcast "Passenger ship"); 6 Ro-Ro cargo (5 broadcast "Cargo ship"). World Bank: ASCO 15 rail ferries,
2 Ro-Ro, 2 Ro-Pax; 12 of our 14 attributed to ASCO (operator assumed for 3).

## 7. Radar at Alat (`sar_yearly.csv`, `sar_label_eval.csv`, `sar_label_agreement.csv`, `sar_diagnostics.csv`)

3,333 detections in 671 passes: basin 845, roadstead 2,488. Fixed-object rule removed 73 blobs.
Thresholds: reference = 25th percentile, same orbit, one year either side; candidate >= 6 dB above; blobs
50-300 m. Kit: 186 detections (worst-case margin 7 points; basin 48, roadstead 138), 128 empty tiles.

AI labels (Claude Opus 5.5, all 314 chips, no detector scores shown; NOT checked by a person):
roadstead 131 yes / 1 no / 6 unsure, precision 99% (95% Wilson 96%-99.9%); basin 7 / 27 / 14, 21% (10%-37%).
Empty tiles: roadstead 0 of 64 with a vessel; basin 2 of 64 clear (5 more possible).
Spot check (10 chips labelled by one author before the AI labels existed): 8 of 10 agree; on the 2 others the
model said unsure and the person said vessel. The fixed 50-chip blind check was not done.

| Year | Passes | Basin/pass | Roadstead/pass | Total/pass | PortWatch Baku calls |
|---|---|---|---|---|---|
| 2019 | 83 | 1.07 | 1.98 | 3.05 | 1,044 |
| 2020 | 81 | 1.04 | 2.51 | 3.54 | 1,217 |
| 2021 | 86 | 1.08 | 4.95 | 6.03 | 1,399 |
| 2022 | 84 | 1.46 | 5.29 | 6.75 | 2,136 |
| 2023 | 86 | 1.12 | 1.97 | 3.08 | 2,036 |
| 2024 | 80 | 1.50 | 2.89 | 4.39 | 1,897 |
| 2025 | 92 | 1.51 | 3.59 | 5.10 | 1,815 |
| 2026 | 79 (to 10 Nov) | 1.28 | 6.59 | 7.87 | 1,983 (Jan-Oct) |

Sea state: roadstead Spearman -0.08 / -0.03 (n = 671); basin +0.12 / +0.14. 2026: S1A 7.9 roadstead/pass,
S1D 4.9; one S1A pass after the first S1D pass; S1A monthly mean 2.7 (Jan) to 11.7 (Jun). Monthly correlation
with PortWatch Baku calls over 94 months: all 0.41, non-tanker 0.53, Ro-Ro 0.23, tanker 0.14.

## 8. Runs on 15 November 2026

- `python -m mcm.build --offline` (page rebuilt after the README/page fix).
- `python -m pytest -q` and `python research/paper_checks.py` — results in `paper/orchestra/review.md`.
- `python research/paper_figures.py` — new Figures 3 and 4 (validation), from `validate_annual.csv` and
  `validate_monthly.csv`; no new numbers in the text.
