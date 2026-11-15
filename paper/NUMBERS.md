# NUMBERS.md: where every number in `paper/paper.md` comes from

One row per number or quantitative claim, in the order it appears in the paper. Checked on 13 November 2026 against the files as they were in the repository that day.

How to read the columns:

- **Source file** is relative to the repository root.
- **Row / column** names the row by its key fields and the column by its header. For `data/official/official_figures.csv`, "line N" is the line number in the file counting the header as line 1 (the file has 518 lines and no multi-line fields).
- **How** is one of: *copied* (same digits), *rounded* (value in the file given in brackets), *derived* (computed from the named cells; formula given), *note* (taken from a research note in the repository, not from a result table; see the list at the end).
- Table cells are listed one row per paper-table row.

## Front matter and abstract

| # | Section | Claim as written | Source file | Row / column (or bib key) | How |
|---|---|---|---|---|---|
| 1 | Header | "13 November 2026" (date of the draft and of the PortWatch download) | `data/portwatch/snapshot.json` | `downloaded_utc` = 2026-11-13T00:10:08Z | copied |
| 2 | Abstract | "January 2019 to October 2026" | `outputs/tables/index_monthly.csv` | first row `month` = 2019-01-01, last row `month` = 2026-10-01 | copied |
| 3 | Abstract | "the year-on-year correlation is -0.05 (n = 6)" | `outputs/tables/validate_summary.csv` | row entity = TITR (Kazakh ministry series), metric = tonnes_total, pw_measure = dry_calls; `yoy_pearson` (-0.0533), `yoy_n` (6) | rounded |
| 4 | Abstract | "a regression on PortWatch tonnage at Aktau has a larger error than two naive forecasts" | `outputs/tables/validate_monthly_summary.csv` | `rmse_portwatch` (144078.3) > `rmse_last_year` (104093.8) > `rmse_previous` (54863.5) | copied |
| 5 | Abstract | "its dry tonnage at Baku is about 12% of the official total" | `outputs/tables/validate_summary.csv` | row Port of Baku, tonnes_total, dry_tonnes; `mean_ratio` (0.1180) | rounded |
| 6 | Abstract | "rise about fourfold between 2021 and 2022" (three ports together) | `outputs/tables/index_annual.csv` | `caspian_roro_calls`, year 2021 (244) and 2022 (946); 946 / 244 = 3.88 | derived |
| 7 | Abstract | "a step at each port within three months" | `outputs/tables/index_roro_step.csv` | rows series = roro_calls; `break_month` = 2021-12 (Baku), 2022-01 (Aktau), 2021-11 (Turkmenbashi) | copied |
| 8 | Abstract | "Kuryk, with 12% to 30% of Kazakh seaport cargo" | `outputs/tables/validate_blind_spot.csv` | `kuryk_share_of_kz_seaports`: minimum 0.1249 (2020), maximum 0.2951 (2023) | rounded |

## 2. Introduction and question

| # | Section | Claim as written | Source file | Row / column (or bib key) | How |
|---|---|---|---|---|---|
| 9 | 2 | "4.119 million tonnes (Mt)" for 2025, Kazakh Ministry of Transport | `data/official/official_figures.csv` | line 438: TITR, 2025, tonnes_total, 4119000, status step1 | copied |
| 10 | 2 | "a vice minister spoke of 4.5 to 4.7 Mt" | `data/official/official_figures.csv` | line 428: TITR, 2025, tonnes_total, 4500000, status step1, note "stated as a range 4.5-4.7 Mt; lower bound recorded" | copied (upper bound from the note) |
| 11 | 2 | "1.867 Mt ... seen only in a search snippet" | `data/official/official_figures.csv` | line 423: TITR, 2025, tonnes_total, 1867000, status snippet | copied |
| 12 | 2 | "For 2024 the association published 3.3 Mt" | `data/official/official_figures.csv` | line 419: TITR, 2024, tonnes_total, 3300000, status opened | copied |
| 13 | 2 | "and the ministry 4.484 Mt" | `data/official/official_figures.csv` | line 437: TITR, 2024, tonnes_total, 4484000, status step1 | copied |
| 14 | 2 | Reports take volumes from operators, association, railways, port authorities, surveys and models; "no use of ship-tracking (AIS) or satellite data in any of them" | `research/references.bib` | worldbank2023middle, oecd2023realising, oecd2025enhancing, ebrd2023sustainable, adb2024tradeflows, carec2022cpmm, carec2024cpmm; reading recorded in `research/LITERATURE.md` section 2 | note |
| 15 | 2 | "explains 89% of the variation in official statistics" | `research/references.bib` | arslanalp2021tracking (as recorded in `research/LITERATURE.md` section 3) | note |
| 16 | 2 | "payload formula was validated for bulk carriers ... (abstract only read)" | `research/references.bib` | jia2019estimating, `note` field "Abstract only" | note |
| 17 | 2 | Quotation "may not be more accurate than using port call information" | `research/references.bib` | adb2023ais (quoted in `research/LITERATURE.md` sections 2 and 3) | note |
| 18 | 2 | "eleven component indices over 19 port or route-year observations", "uses no AIS data" | `research/references.bib` | gondauri2026bsmcii (as recorded in `research/LITERATURE.md` section 1) | note |
| 19 | 2 | "over a window in April 2026 without naming its data source" | `research/references.bib` | wu2026caspianshock (`research/LITERATURE.md` section 1: window 8 to 29 April 2026) | note |
| 20 | 2 | "excludes water within 1 km of shore" | `research/references.bib` | paolo2024satellite (as recorded in `research/STEP1_RESEARCH.md` section d) | note |
| 21 | 2 | "by our check of its published study area it does not cover the Caspian" | `research/STEP1_RESEARCH.md` | section d (study-area file on figshare; that file is not in `references.bib`) | note |
| 22 | 2 | "Google Scholar and eLIBRARY could not be searched" | `research/LITERATURE.md` | section 1, table rows 24 and 26 | note |
| 23 | 2 | "a comparison with 517 official figures" | `data/official/official_figures.csv` | number of data rows (518 lines less the header) | copied |
| 24 | 2 | "three questions" | none | count of the listed questions | count |

## 3. Data

| # | Section | Claim as written | Source file | Row / column (or bib key) | How |
|---|---|---|---|---|---|
| 25 | 3.1 | "five ports: Baku (port100), Aktau (port16), Turkmenbashi (port1330), ... Poti (port1016) and Batumi (port127)" | `src/mcm/index.py` | `NAMES`, `CASPIAN`, `BLACKSEA`; same ids in `data/portwatch/snapshot.json` | copied |
| 26 | 3.1 | "2,867 days per port, from 1 January 2019 to 6 November 2026" | `data/portwatch/snapshot.json` | each port: `rows` 2867, `first` 2019-01-01, `last` 2026-11-06 | copied |
| 27 | 3.1 | "turnaround under five hours and no change in draught" | `research/references.bib` | portwatch2026dailyports (item description, quoted in `research/LITERATURE.md` section 4) | note |
| 28 | 3.1 | "five ship types: container, dry bulk, general cargo, Ro-Ro and tanker" | `research/references.bib` | portwatch2026dailyports; matches the `portcalls_*` columns used in `src/mcm/index.py` | note |
| 29 | 3.1 | "AIS data come from Spire through the UN Global Platform" | `research/references.bib` | portwatch2026dailyports (quoted in `research/LITERATURE.md` section 4) | note |
| 30 | 3.1 | "Four exclusions" | none | count of the listed bullets | count |
| 31 | 3.1 | "underlying method keeps only trade-carrying vessels" | `research/references.bib` | verschuur2021global (quoted in `research/LITERATURE.md` section 3) | note |
| 32 | 3.1 | "Its point (40.2846 N, 49.7325 E)" | `research/STEP1_RESEARCH.md` | section a (PortWatch ports database, port100) | note |
| 33 | 3.1 | "about 43 km from Alat by our rough estimate" | `research/STEP1_RESEARCH.md` | section a ("roughly 43 km north-east of Alat (my distance estimate ...)") | note, estimate |
| 34 | 3.1 | "2.4 to 3.4 times the oil tonnage the Port of Baku reports for 2021, 2023 and 2024" | `outputs/tables/validate_periods.csv` | rows entity = Port of Baku, metric = tonnes_oil, pw_measure = tanker_tonnes; `ratio_pw_over_official` 3.378 (2021), 2.554 (2023), 2.421 (2024) | rounded |
| 35 | 3.2 | "517 published numbers" | `data/official/official_figures.csv` | number of data rows | copied |
| 36 | 3.2 | "433 opened at the source, 77 carried over ..., and 7 seen only in search snippets" | `data/official/official_figures.csv` | column `status`: count of opened (433), step1 (77), snippet (7) | derived (count) |
| 37 | 3.2 | "any of the four ports" | none | Baku/Alat, Aktau, Kuryk, Turkmenbashi | count |
| 38 | 3.2 | "most months of 2019 to 2022 are suppressed as confidential" | `data/official/official_figures.csv` | entity = Kazakhstan sea transport: 8 single-month rows in 2019, none in 2020 or 2021, 2 in 2022; reason given in `data/official/README.md` | derived (count) |
| 39 | 3.2 | "12.96 Mt handled in seaports" (Azerbaijan, 2025) | `data/official/official_figures.csv` | line 365: Azerbaijan seaports, 2025, tonnes_total, 12959500 | rounded |
| 40 | 3.2 | "9.09 Mt carried by sea transport" | `data/official/official_figures.csv` | line 293: Azerbaijan sea transport, 2025, tonnes_carried, 9089600 | rounded |
| 41 | 3.2 | "Kazakh seaports in 2025 handled 7.453 Mt in the port table" | `data/official/official_figures.csv` | line 98: KZ seaports, 2025, tonnes_total, 7453000, status opened | copied |
| 42 | 3.2 | "and 8 Mt in a press report" | `data/official/official_figures.csv` | line 502: KZ seaports, 2025, tonnes_total, 8000000, status step1 | copied |
| 43 | 3.2 | "Kuryk in 2025 handled 1.719 Mt in the port table" | `data/official/official_figures.csv` | line 116: Kuryk, 2025, tonnes_total, 1719000 | copied |
| 44 | 3.2 | "and 1.956 Mt in a port interview" | `data/official/official_figures.csv` | line 406: Kuryk, 2025, tonnes_total, 1955500 | rounded |
| 45 | 3.2 | "Kazakh ministry series for 2019 to 2025, the only one with seven consecutive years ... carried over and not re-opened" | `data/official/official_figures.csv` | lines 432 to 438: TITR, tonnes_total, years 2019 to 2025, status step1 | copied |
| 46 | 3.3 | "79 to 93 Sentinel-1 passes a year over Alat in 2019 to 2026" | `research/s1_revisit.json` | "Baku/Alat", `passes` by year: 85, 89, 90, 86, 91, 90, 93, 79 | copied (min, max) |
| 47 | 3.3 | "53 to 63 over Aktau" | `research/s1_revisit.json` | "Aktau", `passes`: 54, 60, 59, 54, 59, 61, 63, 53 | copied (min, max) |
| 48 | 3.3 | "78 to 93 over Kuryk" | `research/s1_revisit.json` | "Kuryk", `passes`: 82, 90, 88, 83, 88, 90, 93, 78 | copied (min, max) |
| 49 | 3.3 | "106 to 122 over Turkmenbashi" | `research/s1_revisit.json` | "Turkmenbashi", `passes`: 115, 118, 120, 113, 119, 119, 122, 106 | copied (min, max) |
| 50 | 3.3 | "All passes up to 2024 are from Sentinel-1A" | `research/s1_revisit.json` | years 2019 to 2024, every port: only the key `S1A` is present | copied |
| 51 | 3.3 | "In 2026, 34 of the 79 passes over Alat are from Sentinel-1D" | `research/s1_revisit.json` | "Baku/Alat", "2026": `S1D` 34, `passes` 79 | copied |
| 52 | 3.3 | "It holds 672 of the 703 catalogue passes" | `outputs/tables/sar_source_coverage.csv` | sum of `on_planetary_computer` (672) and of `copernicus_passes` (703) | derived (sum) |
| 53 | 3.3 | "The 31 missing passes (10 of them in 2024)" | `outputs/tables/sar_missing_at_source.csv` | 31 data rows; 10 rows with `year` = 2024 | derived (count) |
| 54 | 3.3 | "One pass has partial coverage, so 671 are counted" | `outputs/tables/sar_scene_counts.csv` | column `status`: partial_coverage 1, counted 671 | derived (count) |
| 55 | 3.3 | "mean gap between counted passes is 4.3 days and the longest is 18.5 days" | `outputs/tables/sar_scene_counts.csv` | differences of `datetime` between consecutive rows with status = counted: mean 4.28, maximum 18.5; same figures in `research/SAR_METHOD.md` section 1 | derived |

## 4. Method

| # | Section | Claim as written | Source file | Row / column (or bib key) | How |
|---|---|---|---|---|---|
| 56 | 4.1 | "the four non-tanker types at the three Caspian ports" | `src/mcm/index.py` | `DRY` (4 types), `CASPIAN` (3 ports) | copied |
| 57 | 4.1 | "94 months, January 2019 to October 2026" | `outputs/tables/index_monthly.csv` | 94 data rows; first and last `month` | copied |
| 58 | 4.1 | "divided by the mean month of 2019, times 100" | `src/mcm/index.py` | `rebase()`, `BASE_YEAR = 2019` | copied |
| 59 | 4.1 | "it sums four ship types"; "the five types" | `src/mcm/index.py`; `research/references.bib` | `DRY`; portwatch2026dailyports | copied |
| 60 | 4.1 | "monthly series for January 2021 to December 2023" | `src/mcm/index.py` | `roro_step(start="2021-01-01", end="2023-12-01")` | copied |
| 61 | 4.2 | "eight official series with seven PortWatch measures, 56 pairs" | `src/mcm/validate.py`; `outputs/tables/validate_summary.csv` | `ANNUAL_TARGETS` (8 entries), `PW_MEASURES` (7 entries); 56 data rows | copied |
| 62 | 4.2 | "for 2019 to 2025" | `src/mcm/validate.py` | `annual_comparison(years=range(2019, 2026))` | copied |
| 63 | 4.2 | "Levels have at most seven points and changes at most six" | `outputs/tables/validate_summary.csv` | maximum of `level_n` (7) and of `yoy_n` (6) | copied |
| 64 | 4.2 | "after the first 24 available months" | `src/mcm/validate.py` | `monthly_test(min_train=24)` | copied |
| 65 | 4.2 | "two naive forecasts" | `src/mcm/validate.py` | `fc_last_year`, `fc_previous` | count |
| 66 | 4.3 | "the 25th percentile over passes of the same orbit within a year either side" | `research/SAR_METHOD.md` | section 4, step 2 and threshold table | note |
| 67 | 4.3 | "at least 6 dB brighter than its reference" | `research/SAR_METHOD.md` | section 4, step 4 and threshold table | note |
| 68 | 4.3 | "Blobs under about 50 m or over 300 m are dropped" | `research/SAR_METHOD.md` | section 4, step 6 and threshold table (core of 5 pixels = 50 m measured; core longer than 300 m) | note |
| 69 | 4.3 | "two zones" | `research/SAR_METHOD.md` | section 3 (basin, roadstead) | note |
| 70 | 4.3 | "186 detections, enough for a margin of 7 percentage points in the worst case" | `outputs/tables/sar_sample_size.csv` | row p = 0.5, margin_pp = 7: `n_with_fpc` 186 | copied |
| 71 | 4.3 | "128 image tiles where the detector found nothing" | `research/SAR_METHOD.md` | section 9 | note |

## 5.1 The index series

| # | Section | Claim as written | Source file | Row / column (or bib key) | How |
|---|---|---|---|---|---|
| 72 | 5.1 | "rise from 1,442 in 2019 to 2,621 in 2022, fall to 2,215 in 2023 and reach 2,486 in 2025" | `outputs/tables/index_annual.csv` | `caspian_dry_calls`, years 2019, 2022, 2023, 2025 | copied |
| 73 | 5.1 | "The index averages 206 over January to October 2026" | `outputs/tables/index_monthly.csv` | mean of `caspian_dry_calls_index` over the ten rows 2026-01-01 to 2026-10-01 = 206.0 | derived (mean) |
| 74 | 5.1 | "June 2026 with 309 calls (index 257)" | `outputs/tables/index_monthly.csv` | row 2026-06-01: `caspian_dry_calls` 309, `caspian_dry_calls_index` 257.14 (the maximum of the column) | rounded |
| 75 | Table 1, 2019 | 1,442; 100.0; 240; 1,070; 1.24; 1,122 | `outputs/tables/index_annual.csv` | row 2019: `caspian_dry_calls`, `caspian_roro_calls`, `caspian_tanker_calls`, `caspian_dry_tonnes` (1236607), `blacksea_dry_calls`. Index = annual calls / 1442 x 100 (equal to the yearly mean of `caspian_dry_calls_index` in `index_monthly.csv`) | copied; tonnes rounded; index derived |
| 76 | Table 1, 2020 | 1,666; 115.5; 262; 1,104; 1.27; 1,020 | `outputs/tables/index_annual.csv` | row 2020; dry tonnes 1270422; index 1666 / 1442 x 100 = 115.5 | as row 75 |
| 77 | Table 1, 2021 | 2,051; 142.2; 244; 1,052; 1.73; 847 | `outputs/tables/index_annual.csv` | row 2021; dry tonnes 1729878; index 142.2 | as row 75 |
| 78 | Table 1, 2022 | 2,621; 181.8; 946; 1,481; 2.25; 1,006 | `outputs/tables/index_annual.csv` | row 2022; dry tonnes 2251756; index 181.8 | as row 75 |
| 79 | Table 1, 2023 | 2,215; 153.6; 1,006; 1,715; 1.84; 991 | `outputs/tables/index_annual.csv` | row 2023; dry tonnes 1844426; index 153.6 | as row 75 |
| 80 | Table 1, 2024 | 2,298; 159.4; 894; 1,472; 2.09; 1,031 | `outputs/tables/index_annual.csv` | row 2024; dry tonnes 2085582; index 159.4 | as row 75 |
| 81 | Table 1, 2025 | 2,486; 172.4; 778; 1,293; 2.28; 1,114 | `outputs/tables/index_annual.csv` | row 2025; dry tonnes 2282099; index 172.4 | as row 75 |
| 82 | 5.1 | "between 847 and 1,122 non-tanker calls a year" (Poti + Batumi) | `outputs/tables/index_annual.csv` | `blacksea_dry_calls`: minimum 847 (2021), maximum 1122 (2019) | copied |
| 83 | 5.1 | "they rise by 702" (Ro-Ro calls, 2021 to 2022) | `outputs/tables/index_annual.csv` | `caspian_roro_calls` 946 - 244 | derived |
| 84 | 5.1 | "all non-tanker calls rise by 570" | `outputs/tables/index_annual.csv` | `caspian_dry_calls` 2621 - 2051 | derived |
| 85 | 5.1 | "The other three types together fall by 132" | `outputs/tables/index_annual.csv` | 702 - 570 | derived |
| 86 | Figures 1 and 2 | "2019 monthly mean = 100" | `src/mcm/index.py` | `rebase()` | copied |

## 5.2 The Ro-Ro step

| # | Section | Claim as written | Source file | Row / column (or bib key) | How |
|---|---|---|---|---|---|
| 87 | 5.2 | "rise about fourfold, from 244 in 2021 to 946 in 2022" | `outputs/tables/index_annual.csv` | `caspian_roro_calls` 2021, 2022; 946 / 244 = 3.88 | copied; ratio derived |
| 88 | 5.2 | "within three months of each other: November 2021, December 2021 and January 2022" | `outputs/tables/index_roro_step.csv` | rows series = roro_calls, `break_month`: Turkmenbashi 2021-11, Baku 2021-12, Aktau 2022-01 | copied |
| 89 | 5.2 | "The mean after the break is 4.5 to 5.9 times the mean before it" | `outputs/tables/index_roro_step.csv` | rows series = roro_calls, `ratio`: 4.55, 5.22, 5.89 | rounded |
| 90 | 5.2 | "In January to June 2021 the three ports together record 28 Ro-Ro calls, and Aktau none" | `outputs/tables/index_roro_2021_2023.csv` | rows 2021-01-01 to 2021-06-01: Aktau 0+0+0+0+0+0 = 0, Baku 4+3+0+2+2+4 = 15, Turkmenbashi 5+3+2+0+0+3 = 13; total 28 | derived (sum) |
| 91 | 5.2 | "In July to December 2021 they record 216" | `outputs/tables/index_roro_2021_2023.csv` | rows 2021-07-01 to 2021-12-01: Aktau 28, Baku 104, Turkmenbashi 84; total 216 | derived (sum) |
| 92 | 5.2 | "a rise at all three ports from July 2021" | `outputs/tables/index_roro_2021_2023.csv` | row 2021-07-01 against row 2021-06-01: Aktau 0 to 3, Baku 4 to 8, Turkmenbashi 3 to 9 | copied |
| 93 | 5.2 | "Against 2019, the 2022 totals are about four times higher at each port" | `outputs/tables/index_per_port_monthly.csv` | yearly sums of `roro_calls`: Baku 496 / 126 = 3.94, Aktau 147 / 36 = 4.08, Turkmenbashi 303 / 78 = 3.88 | derived |
| 94 | Table 2, Baku | 126; 131; 119; 496; 518; 2021-12; 8.0; 41.8; 5.22 | `outputs/tables/index_per_port_monthly.csv`; `outputs/tables/index_roro_step.csv` | yearly sums of `roro_calls` for port = Baku, 2019 to 2023 (also `pw_baku_roro_calls` in `validate_blind_spot.csv`); step row Baku, roro_calls: `break_month`, `mean_before`, `mean_after`, `ratio` | yearly sums derived; rest copied |
| 95 | Table 2, Aktau | 36; 35; 28; 147; 183; 2022-01; 2.3; 13.8; 5.89 | same two files | yearly sums for port = Aktau (also the `portwatch` column of `validate_annual.csv`, KZ seaports / roro_calls); step row Aktau, roro_calls | as row 94 |
| 96 | Table 2, Turkmenbashi | 78; 96; 97; 303; 305; 2021-11; 5.5; 25.0; 4.55 | same two files | yearly sums for port = Turkmenbashi; step row Turkmenbashi, roro_calls | as row 94 |
| 97 | Table 2, All three | 240; 262; 244; 946; 1,006 | `outputs/tables/index_annual.csv` | `caspian_roro_calls`, 2019 to 2023 | copied |
| 98 | Table 2 caption | "window January 2021 to December 2023" | `src/mcm/index.py` | `roro_step()` defaults | copied |
| 99 | 5.2 | "44,175 rail wagons in 2019" | `data/official/official_figures.csv` | line 442: Port of Baku, 2019, wagons, 44175, status step1 | copied |
| 100 | 5.2 | "and 37,300 in 2023" | `data/official/official_figures.csv` | line 455: Port of Baku, 2023, wagons, 37300, status step1 | copied |
| 101 | 5.2 | "Wheeled vehicles rose from 33,671" | `data/official/official_figures.csv` | line 443: Port of Baku, 2019, trucks, 33671, status step1, note "wheeled vehicles" | copied |
| 102 | 5.2 | "to 54,200" | `data/official/official_figures.csv` | line 456: Port of Baku, 2023, trucks, 54200, status step1 | copied |
| 103 | 5.2 | "Kuryk recorded 487 ferry calls in 2019" | `data/official/official_figures.csv` | line 221: Kuryk, 2019, ferry_calls, 487 (also `kuryk_ferry_calls` in `validate_blind_spot.csv`) | copied |
| 104 | 5.2 | "and 618 in 2022" | `data/official/official_figures.csv` | line 227: Kuryk, 2022, ferry_calls, 618 | copied |
| 105 | 5.2 | "PortWatch Ro-Ro calls at Baku went from 126 to 518" (2019 to 2023) | `outputs/tables/validate_blind_spot.csv` | `pw_baku_roro_calls`, rows 2019 and 2023 | copied |
| 106 | 5.2 | "Four checks" | none | count of the listed bullets | count |
| 107 | 5.2 | "Ro-Ro calls were 103,762 in 2021 and 106,384 in 2022" (all PortWatch ports) | `outputs/tables/index_roro_global_2020_2022.csv` | sum of `roro_calls` over the 12 rows of year 2021 and of year 2022 | derived (sum) |
| 108 | 5.2 | "General cargo calls fall ... (ratios of 0.75, 0.59 and 0.46)" | `outputs/tables/index_roro_step.csv` | rows series = general_cargo_calls, `ratio`: Baku 0.75, Aktau 0.59, Turkmenbashi 0.46 | copied |
| 109 | 5.2 | "At Aktau that break is in July 2021, the month Ro-Ro calls reappear there" | `outputs/tables/index_roro_step.csv`; `outputs/tables/index_roro_2021_2023.csv` | row Aktau, general_cargo_calls: `break_month` 2021-07; column Aktau: 0 in 2021-01 to 2021-06, 3 in 2021-07 | copied |
| 110 | 5.2 | "no ship registered as a Ro-Ro cargo ship entered service in 2021 or 2022" | `research/FERRY_FLEET.md` | "What the evidence supports", item 4 | note |
| 111 | 5.2 | "2 to 22 ferry calls a year at Aktau in 2019 to 2024" | `data/official/official_figures.csv` | lines 220, 222, 224, 226, 228, 230: Aktau, ferry_calls, 2019 to 2024: 2, 4, 3, 7, 22, 2 | copied (min, max) |
| 112 | 5.2 | "PortWatch records 28 to 183 Ro-Ro calls a year there" | `outputs/tables/validate_periods.csv` | rows entity = Aktau, metric = ferry_calls, pw_measure = roro_calls, column `portwatch`: 36, 35, 28, 147, 183, 172 | copied (min, max) |
| 113 | 5.2 | "No PortWatch or IMF document that we read mentions a break in 2021 or 2022" | `research/LITERATURE.md` | section 4, "AIS-coverage change around 2021-2022" | note |
| 114 | 5.2 | Global Fishing Watch vendor change and its warning | `research/references.bib` | gfw2026vendor (as recorded in `research/LITERATURE.md` section 4) | note |
| 115 | 5.2 | "before mid-2021" | `outputs/tables/index_roro_2021_2023.csv` | onset in row 2021-07-01 (see row 92) | derived |

## 5.3 Agreement and disagreement

| # | Section | Claim as written | Source file | Row / column (or bib key) | How |
|---|---|---|---|---|---|
| 116 | Table 3 caption | "2019 to 2025" | `src/mcm/validate.py` | `annual_comparison(years=range(2019, 2026))` | copied |
| 117 | Table 3, row 1 | Aktau + AMCT vessel calls / all calls: 0.97; 0.90 (7); -0.16 (6) | `outputs/tables/validate_summary.csv` | row Aktau incl. AMCT, vessel_calls, all_calls: `mean_ratio` 0.9665, `level_pearson` 0.9021, `level_n` 7, `yoy_pearson` -0.1570, `yoy_n` 6 | rounded |
| 118 | Table 3, row 2 | Aktau vessel calls / all calls: 1.28; 0.87 (7); -0.39 (6) | `outputs/tables/validate_summary.csv` | row Aktau, vessel_calls, all_calls: 1.2815, 0.8680, 7, -0.3906, 6 | rounded |
| 119 | Table 3, row 3 | Aktau oil tonnes / tanker tonnes: 0.97; 0.85 (6); 0.89 (5) | `outputs/tables/validate_summary.csv` | row Aktau, tonnes_oil, tanker_tonnes: 0.9720, 0.8542, 6, 0.8870, 5 | rounded |
| 120 | Table 3, row 4 | Aktau oil tonnes / tanker calls: 0.999 (6); 0.99 (5) | `outputs/tables/validate_summary.csv` | row Aktau, tonnes_oil, tanker_calls: `level_pearson` 0.9985, 6, `yoy_pearson` 0.9920, 5 (no ratio: units differ) | rounded |
| 121 | Table 3, row 5 | Aktau total tonnes / all tonnes: 0.82; 0.75 (7); 0.53 (6) | `outputs/tables/validate_summary.csv` | row Aktau, tonnes_total, all_tonnes: 0.8243, 0.7502, 7, 0.5319, 6 | rounded |
| 122 | Table 3, row 6 | Aktau + AMCT total tonnes / all tonnes: 0.67; 0.57 (7); 0.16 (6) | `outputs/tables/validate_summary.csv` | row Aktau incl. AMCT, tonnes_total, all_tonnes: 0.6694, 0.5714, 7, 0.1563, 6 | rounded |
| 123 | Table 3, row 7 | Kazakh seaports total tonnes / all tonnes, Aktau: 0.51; 0.81 (7); 0.59 (6) | `outputs/tables/validate_summary.csv` | row KZ seaports, tonnes_total, all_tonnes: 0.5118, 0.8109, 7, 0.5933, 6 | rounded |
| 124 | Table 3, row 8 | Port of Baku total tonnes / dry tonnes: 0.12; 0.90 (7); 0.30 (6) | `outputs/tables/validate_summary.csv` | row Port of Baku, tonnes_total, dry_tonnes: 0.1180, 0.8999, 7, 0.2955, 6 | rounded |
| 125 | Table 3, row 9 | Port of Baku total tonnes / all tonnes: 0.77; 0.66 (7); 0.50 (6) | `outputs/tables/validate_summary.csv` | row Port of Baku, tonnes_total, all_tonnes: 0.7737, 0.6556, 7, 0.5009, 6 | rounded |
| 126 | Table 3, row 10 | Route total / non-tanker calls: 0.60 (7); -0.05 (6) | `outputs/tables/validate_summary.csv` | row TITR (Kazakh ministry series), tonnes_total, dry_calls: `level_pearson` 0.5975, 7, `yoy_pearson` -0.0533, 6 | rounded |
| 127 | Table 3, row 11 | Route total / Ro-Ro calls: 0.73 (7); 0.79 (6) | `outputs/tables/validate_summary.csv` | row TITR (Kazakh ministry series), tonnes_total, roro_calls: 0.7258, 7, 0.7878, 6 | rounded |
| 128 | Table 3, row 12 | Route total / tanker calls: 0.60 (7); 0.80 (6) | `outputs/tables/validate_summary.csv` | row TITR (Kazakh ministry series), tonnes_total, tanker_calls: 0.5955, 7, 0.8000, 6 | rounded |
| 129 | 5.3 | "PortWatch records 1,383 calls in 2025 against 1,394 official" | `outputs/tables/validate_annual.csv` | row Aktau incl. AMCT, vessel_calls, all_calls, year 2025: `portwatch` 1383, `official` 1394 | copied |
| 130 | 5.3 | "The ratio is between 0.98 and 1.04 in six of seven years" | `outputs/tables/validate_annual.csv` | same rows, `ratio_pw_over_official` by year: 1.038, 0.761, 0.980, 1.018, 0.976, 1.002, 0.992 | rounded |
| 131 | 5.3 | "the exception is 2020, with 748 against 983" | `outputs/tables/validate_annual.csv` | same rows, year 2020: `portwatch` 748, `official` 983 | copied |
| 132 | 5.3 | "The year-on-year changes do not correlate" | `outputs/tables/validate_summary.csv` | row Aktau incl. AMCT, vessel_calls, all_calls: `yoy_pearson` -0.1570, `yoy_spearman` -0.0286 | copied |
| 133 | 5.3 | "between 0.97 and 1.08 of the port's oil tonnage in 2019 to 2023" | `outputs/tables/validate_annual.csv` | rows Aktau, tonnes_oil, tanker_tonnes, `ratio_pw_over_official`: 0.966, 1.008, 0.981, 1.029, 1.077 | rounded |
| 134 | 5.3 | "and 0.77 in 2024" | `outputs/tables/validate_annual.csv` | same rows, year 2024: 0.771 | rounded |
| 135 | 5.3 | "Tanker calls follow oil tonnage more closely than any other pair" | `outputs/tables/validate_summary.csv` | row Aktau, tonnes_oil, tanker_calls has the largest `level_pearson` (0.9985) and `yoy_pearson` (0.9920) of the 56 rows | derived (maximum) |
| 136 | 5.3 | "0.82 of the official total on average" (Aktau total tonnage) | `outputs/tables/validate_summary.csv` | row Aktau, tonnes_total, all_tonnes: `mean_ratio` 0.8243 | rounded |
| 137 | 5.3 | "and 0.71 in 2025" | `outputs/tables/validate_annual.csv` | row Aktau, tonnes_total, all_tonnes, year 2025: `ratio_pw_over_official` 0.711 | rounded |
| 138 | 5.3 | "PortWatch at Aktau sees about half the tonnage" (all Kazakh seaports) | `outputs/tables/validate_summary.csv` | row KZ seaports, tonnes_total, all_tonnes: `mean_ratio` 0.5118 | rounded |
| 139 | 5.3 | "PortWatch dry tonnage is 12% of the port's official total on average" (Baku) | `outputs/tables/validate_summary.csv` | row Port of Baku, tonnes_total, dry_tonnes: `mean_ratio` 0.1180 | rounded |
| 140 | 5.3 | "The ratio for all tonnage looks better (0.77)" | `outputs/tables/validate_summary.csv` | row Port of Baku, tonnes_total, all_tonnes: `mean_ratio` 0.7737 | rounded |
| 141 | 5.3 | "PortWatch tanker tonnage is far above the port's own oil figure (section 3.1)" | `outputs/tables/validate_periods.csv` | see row 34 | copied |
| 142 | 5.3 | "of 6.3 Mt handled at Alat in 2022, 2.5 Mt moved on railcars and 1.1 Mt in trucks and trailers" | `research/references.bib` | worldbank2023middle, p. 43 (as recorded in `research/LITERATURE.md` section 2) | note |
| 143 | 5.3 | "PortWatch shows 1.03 Mt of dry cargo at Baku that year" | `outputs/tables/validate_annual.csv` | row Port of Baku, tonnes_total, dry_tonnes, year 2022: `portwatch` 1034371 | rounded |
| 144 | 5.3 | "For 2024 the port reports 1.044 Mt of 'dry cargo'" | `data/official/official_figures.csv` | line 464: Port of Baku, 2024, tonnes_dry, 1044000, status step1 | copied |
| 145 | 5.3 | "and PortWatch dry tonnage is 1.00 Mt" | `outputs/tables/validate_periods.csv` | row Port of Baku, tonnes_dry, 2024-01-01 to 2024-12-31, pw_measure = dry_tonnes: `portwatch` 999866 | rounded |

## 5.4 Question 1

| # | Section | Claim as written | Source file | Row / column (or bib key) | How |
|---|---|---|---|---|---|
| 146 | 5.4 | "level correlation of 0.60 (n = 7)" | `outputs/tables/validate_summary.csv` | row TITR (Kazakh ministry series), tonnes_total, dry_calls: `level_pearson` 0.5975, `level_n` 7 | rounded |
| 147 | 5.4 | "year-on-year correlation of -0.05 (n = 6)" | `outputs/tables/validate_summary.csv` | same row: `yoy_pearson` -0.0533, `yoy_n` 6 | rounded |
| 148 | 5.4 | "The route total rose by 153% in 2022 and 86% in 2023" | `outputs/tables/validate_annual.csv` | rows TITR (Kazakh ministry series), tonnes_total, dry_calls: `official_yoy` 1.534 (2022), 0.861 (2023) | rounded |
| 149 | 5.4 | "Non-tanker calls rose by 28% and then fell by 15%" | `outputs/tables/validate_annual.csv` | same rows: `portwatch_yoy` 0.278 (2022), -0.155 (2023) | rounded |
| 150 | 5.4 | "Ro-Ro calls (0.79) and tanker calls (0.80), both with n = 6" | `outputs/tables/validate_summary.csv` | rows TITR (Kazakh ministry series), tonnes_total, roro_calls and tanker_calls: `yoy_pearson` 0.7878 and 0.8000, `yoy_n` 6 | rounded |
| 151 | 5.4 | "The Ro-Ro result rests on 2022" | `outputs/tables/validate_annual.csv` | rows TITR (Kazakh ministry series), tonnes_total, roro_calls, year 2022: `official_yoy` 1.534, `portwatch_yoy` 2.877 | copied |
| 152 | 5.4 | "among 56 pairs tested on six points" | `outputs/tables/validate_summary.csv` | 56 data rows; `yoy_n` 6 | copied |
| 153 | 5.4 | "Non-tanker calls at Baku rise with the Port of Baku's total tonnage in levels (0.88, n = 7)" | `outputs/tables/validate_summary.csv` | row Port of Baku, tonnes_total, dry_calls: `level_pearson` 0.8770, `level_n` 7 | rounded |
| 154 | 5.4 | "year on year the correlation is 0.30" | `outputs/tables/validate_summary.csv` | same row: `yoy_pearson` 0.3025 | rounded |

## 5.5 Question 3

| # | Section | Claim as written | Source file | Row / column (or bib key) | How |
|---|---|---|---|---|---|
| 155 | 5.5 | "the 54 months between February 2019 and October 2026" | `outputs/tables/validate_monthly_summary.csv` | `months` 54, `first` 2019-02, `last` 2026-10 | copied |
| 156 | 5.5 | "the level correlation ... is 0.06" | `outputs/tables/validate_monthly_summary.csv` | `level_pearson` 0.0629 | rounded |
| 157 | 5.5 | "The year-on-year correlation is -0.23 (n = 34)" | `outputs/tables/validate_monthly_summary.csv` | `yoy_pearson` -0.2296, `yoy_n` 34 | rounded |
| 158 | 5.5 | "The out-of-sample test has 30 months, May 2024 to October 2026" | `outputs/tables/validate_monthly_summary.csv`; `outputs/tables/validate_monthly.csv` | `oos_months` 30; first and last rows with `fc_portwatch`, `fc_last_year` and `fc_previous` all present: 2024-05, 2026-10 | copied |
| 159 | 5.5 | "144.1 thousand tonnes for the PortWatch regression" | `outputs/tables/validate_monthly_summary.csv` | `rmse_portwatch` 144078.3 | rounded |
| 160 | 5.5 | "104.1 thousand tonnes for the same month a year earlier" | `outputs/tables/validate_monthly_summary.csv` | `rmse_last_year` 104093.8 | rounded |
| 161 | 5.5 | "54.9 thousand tonnes for the previous available month" | `outputs/tables/validate_monthly_summary.csv` | `rmse_previous` 54863.5 | rounded |
| 162 | 5.5 | "The PortWatch forecast is below the official value in all 30 months" | `outputs/tables/validate_monthly.csv` | rows 2024-05 to 2026-10: `fc_portwatch` < `official` in each of the 30 rows | derived (count) |
| 163 | 5.5 | "Only 10 of the 48 months of 2019 to 2022 are published" | `outputs/tables/validate_monthly.csv` | rows with `month` in 2019 (8) and 2022 (2); none in 2020 or 2021; 48 = 4 years x 12 | derived (count) |
| 164 | 5.5 | "34 to 90 thousand tonnes in 2019" (official monthly values) | `outputs/tables/validate_monthly.csv` | `official`, rows of 2019: minimum 33960 (2019-10), maximum 90120 (2019-12) | rounded |
| 165 | 5.5 | "228 to 467 thousand tonnes in 2025" | `outputs/tables/validate_monthly.csv` | `official`, rows of 2025: minimum 228260 (2025-08), maximum 467000 (2025-11) | rounded |
| 166 | 5.5 | "213 to 272 thousand tonnes in the 2019 months" (PortWatch, Aktau) | `outputs/tables/validate_monthly.csv` | `portwatch`, rows of 2019: minimum 213427 (2019-02), maximum 272467 (2019-03) | rounded |
| 167 | 5.5 | "109 to 404 thousand tonnes in 2025" | `outputs/tables/validate_monthly.csv` | `portwatch`, rows of 2025: minimum 109445 (2025-10), maximum 403576 (2025-03) | rounded |

## 5.6 Question 2

| # | Section | Claim as written | Source file | Row / column (or bib key) | How |
|---|---|---|---|---|---|
| 168 | 5.6 | "two gaps" | none | Kuryk; ferries that broadcast as passenger ships (the bold items of section 5.6) | count |
| 169 | 5.6 | "Kuryk handles 12% to 30% of all Kazakh seaport cargo in 2019 to 2025" | `outputs/tables/validate_blind_spot.csv` | `kuryk_share_of_kz_seaports`: minimum 0.1249 (2020), maximum 0.2951 (2023) | rounded |
| 170 | 5.6 | "receives 412 to 700 ferry calls a year" | `outputs/tables/validate_blind_spot.csv` | `kuryk_ferry_calls`: minimum 412 (2021), maximum 700 (2023); 2025 is blank | copied |
| 171 | 5.6 | "Kuryk's cargo as mainly trucks and rail wagons on the route to Baku" | `research/references.bib` | worldbank2023middle, p. 42 (as recorded in `research/LITERATURE.md` section 2: 79% of 2022 throughput) | note |
| 172 | 5.6 | "in 2019 to 2021 PortWatch records only 119 to 131 Ro-Ro calls a year at Baku" | `outputs/tables/validate_blind_spot.csv` | `pw_baku_roro_calls`, rows 2019 (126), 2020 (131), 2021 (119) | copied |
| 173 | Table 4, 2019 | 1,369.8; 5,895.0; 23.2%; 487; 126; 240 | `outputs/tables/validate_blind_spot.csv` | row 2019: `kuryk_tonnes` 1369800, `kz_seaports_tonnes` 5895000, `kuryk_share_of_kz_seaports` 0.2324, `kuryk_ferry_calls`, `pw_baku_roro_calls`, `pw_caspian_roro_calls` | tonnes shown in kt; share rounded; calls copied |
| 174 | Table 4, 2020 | 666.8; 5,338.8; 12.5%; 542; 131; 262 | `outputs/tables/validate_blind_spot.csv` | row 2020: 666800; 5338844.68; 0.1249; 542; 131; 262 | as row 173 |
| 175 | Table 4, 2021 | 974.5; 5,456.2; 17.9%; 412; 119; 244 | `outputs/tables/validate_blind_spot.csv` | row 2021: 974500; 5456163; 0.1786; 412; 119; 244 | as row 173 |
| 176 | Table 4, 2022 | 1,824.0; 6,493.6; 28.1%; 618; 496; 946 | `outputs/tables/validate_blind_spot.csv` | row 2022: 1824010; 6493572.95; 0.2809; 618; 496; 946 | as row 173 |
| 177 | Table 4, 2023 | 2,115.0; 7,168.0; 29.5%; 700; 518; 1,006 | `outputs/tables/validate_blind_spot.csv` | row 2023: 2115000; 7168000; 0.2951; 700; 518; 1006 | as row 173 |
| 178 | Table 4, 2024 | 1,931.9; 7,333.1; 26.3%; 645; 479; 894 | `outputs/tables/validate_blind_spot.csv` | row 2024: 1931900; 7333100; 0.2634; 645; 479; 894 | as row 173 |
| 179 | Table 4, 2025 | 1,719.0; 7,453.0; 23.1%; not published; 410; 778 | `outputs/tables/validate_blind_spot.csv` | row 2025: 1719000; 7453000; 0.2306; `kuryk_ferry_calls` blank; 410; 778 | as row 173 |
| 180 | 5.6 | "We identified 14 Caspian ferries" | `research/FERRY_FLEET.md` | fleet table, 14 vessel rows | note (count) |
| 181 | 5.6 | "Eight are registered as 'Passenger/Ro-Ro Cargo Ship'" | `research/FERRY_FLEET.md` | fleet table, column "Ship Type (register)": DAGISTAN, MERKURY 1, AKADEMIK M. TOPCHUBASHOV, PROFESSOR GUL, AZERBAIJAN, ZARIFA ALIYEVA, BERKARAR, BAGTYYAR | note (count) |
| 182 | 5.6 | "five of those broadcast the AIS type 'Passenger ship'" | `research/FERRY_FLEET.md` | column "AIS Type (broadcast)": DAGISTAN, MERKURY 1, PROFESSOR GUL, AZERBAIJAN, ZARIFA ALIYEVA (TOPCHUBASHOV not shown; BERKARAR "Medical"; BAGTYYAR "HSC") | note (count) |
| 183 | 5.6 | "Six are registered as 'Ro-Ro Cargo Ship'" | `research/FERRY_FLEET.md` | SHAHDAG, AGDAM, NAKHCHYVAN, BARDA, BALAKEN, BESTEKAR GARA GARAYEV | note (count) |
| 184 | 5.6 | "five of those broadcast 'Cargo ship'" | `research/FERRY_FLEET.md` | SHAHDAG, AGDAM, NAKHCHYVAN, BARDA, BALAKEN (BESTEKAR GARA GARAYEV not shown) | note (count) |
| 185 | 5.6 | "15 rail ferries, 2 Ro-Ro ships and 2 Ro-Pax ships" | `research/references.bib` | worldbank2023middle, pp. 43 to 44 (as recorded in `research/LITERATURE.md` section 2 and `research/FERRY_FLEET.md`) | note |
| 186 | 5.6 | "12 of our 14 belong to that fleet" | `research/FERRY_FLEET.md` | "So the table holds 12 ASCO vessels"; the other two are Turkmen-flagged. Operator is assumed, not confirmed, for 3 of the 12 (see the Operator column) | note (count) |
| 187 | 5.6 | "The detector kept 3,333 objects in 671 passes" | `outputs/tables/sar_yearly.csv` | sum of `detections_total` (253 + 287 + 519 + 567 + 265 + 351 + 469 + 622 = 3333); sum of `n_passes` (671) | derived (sum) |
| 188 | 5.6 | "845 in the basin and 2,488 in the roadstead" | `outputs/tables/sar_yearly.csv` | sum of `detections_basin` (845) and of `detections_roadstead` (2488); also `n` in `sar_diagnostics.csv` | derived (sum) |
| 189 | 5.6 | "until the 186 detections in the kit are labelled by hand" | `outputs/tables/sar_sample_size.csv` | row p = 0.5, margin_pp = 7: `n_with_fpc` 186; kit described in `research/SAR_METHOD.md` section 9 | copied |
| 190 | Table 5, 2019 | 83; 1.07; 1.98; 3.05; 1,044 | `outputs/tables/sar_yearly.csv`; `outputs/tables/sar_vs_portwatch_monthly.csv` | row 2019: `n_passes`, `mean_basin`, `mean_roadstead`, `mean_total`; PortWatch = sum of `portcalls` over the 12 rows of 2019 | copied; PortWatch sum derived |
| 191 | Table 5, 2020 | 81; 1.04; 2.51; 3.54; 1,217 | same two files | row 2020; sum of `portcalls` for 2020 | as row 190 |
| 192 | Table 5, 2021 | 86; 1.08; 4.95; 6.03; 1,399 | same two files | row 2021; sum of `portcalls` for 2021 | as row 190 |
| 193 | Table 5, 2022 | 84; 1.46; 5.29; 6.75; 2,136 | same two files | row 2022; sum of `portcalls` for 2022 | as row 190 |
| 194 | Table 5, 2023 | 86; 1.12; 1.97; 3.08; 2,036 | same two files | row 2023; sum of `portcalls` for 2023 | as row 190 |
| 195 | Table 5, 2024 | 80; 1.50; 2.89; 4.39; 1,897 | same two files | row 2024; sum of `portcalls` for 2024 | as row 190 |
| 196 | Table 5, 2025 | 92; 1.51; 3.59; 5.10; 1,815 | same two files | row 2025; sum of `portcalls` for 2025 | as row 190 |
| 197 | Table 5, 2026 | 79 (to 10 Nov); 1.28; 6.59; 7.87; 1,983 (Jan to Oct) | same two files; `outputs/tables/sar_scene_counts.csv` | row 2026; sum of `portcalls` over the ten rows 2026-01 to 2026-10; last counted pass `datetime` 2026-11-10 | as row 190 |
| 198 | 5.6 | "Spearman -0.08 and -0.03 for the two polarisations, n = 671" | `outputs/tables/sar_diagnostics.csv` | rows check = spearman_count_vs_sea_vv_level and spearman_count_vs_sea_vh_level, zone = roadstead: `value` -0.078 and -0.033, `n` 671 | rounded |
| 199 | 5.6 | "In 2026 the Sentinel-1A passes average 7.9 roadstead blobs and the Sentinel-1D passes 4.9" | `outputs/tables/sar_scene_counts.csv` | rows with status = counted and `datetime` in 2026: mean of `n_roadstead` for platform SENTINEL-1A (44 passes) = 7.93, for SENTINEL-1D (34 passes) = 4.91; same figures in `research/SAR_METHOD.md` section 6 | derived (mean) |
| 200 | 5.6 | "The two platforms do not overlap in time" | `research/SAR_METHOD.md` | section 6, "Platform" (Sentinel-1A January to June, Sentinel-1D June to November) | note |
| 201 | 5.6 | "Month by month over 94 months" | `outputs/tables/sar_vs_portwatch_summary.csv` | `n_months` 94 | copied |
| 202 | 5.6 | "0.41 for all calls, 0.53 for non-tanker calls, 0.23 for Ro-Ro calls and 0.14 for tanker calls" | `outputs/tables/sar_vs_portwatch_summary.csv` | rows sar = mean_total; `pearson` for portcalls 0.414, portcalls_dry 0.528, portcalls_roro 0.228, portcalls_tanker 0.143 | rounded |
| 203 | 5.6 | "the roadstead mean falls from 5.29 in 2022 to 1.97 in 2023" | `outputs/tables/sar_yearly.csv` | `mean_roadstead`, rows 2022 and 2023 | copied |
| 204 | 5.6 | "PortWatch calls barely change (2,136 and 2,036)" | `outputs/tables/sar_vs_portwatch_monthly.csv` | sum of `portcalls` over the rows of 2022 and of 2023 | derived (sum) |

## 6 to 8

| # | Section | Claim as written | Source file | Row / column (or bib key) | How |
|---|---|---|---|---|---|
| 205 | 6 | "before and after mid-2021" | `outputs/tables/index_roro_2021_2023.csv` | see row 92 | derived |
| 206 | 6 | "About half of the identified ferries are registered or broadcast as passenger ships" | `research/FERRY_FLEET.md` | 8 of 14 (rows 180 and 181) | note (count) |
| 207 | 6 | "Annual correlations rest on n of 5 to 7" | `outputs/tables/validate_summary.csv` | `level_n` 6 or 7; `yoy_n` 5 or 6 | copied |
| 208 | 6 | "With 56 pairs tested" | `outputs/tables/validate_summary.csv` | 56 data rows | copied |
| 209 | 6 | "The platform changed during 2026 and the counts differ between platforms" | `research/s1_revisit.json`; `outputs/tables/sar_scene_counts.csv` | "Baku/Alat", "2026": `S1A` 44, `S1D` 34, `S1C` 1; see row 199 | copied |
| 210 | 6 | "Passes missing at the source are uneven by year" | `outputs/tables/sar_missing_at_source.csv` | count of rows by `year`: 2019: 2, 2020: 8, 2021: 4, 2022: 2, 2023: 5, 2024: 10, none in 2025 or 2026 | derived (count) |
| 211 | 6 | "Turkmenbashi has official figures for one year only (2025)" | `data/official/official_figures.csv` | lines 376 to 379: the four rows with entity = Turkmenbashi, all 2025-01-01 to 2025-12-31 | copied |
| 212 | 6 | "PortWatch has added ports and refined port boundaries" | `research/references.bib` | arslanalp2026nowcasting (as recorded in `research/LITERATURE.md` section 3: 64 ports added, 18 boundaries refined) | note |
| 213 | 6 | "the download of 13 November 2026" | `data/portwatch/snapshot.json` | `downloaded_utc` | copied |
| 214 | 7 | "Label the 186 detections and the 128 empty tiles" | `outputs/tables/sar_sample_size.csv`; `research/SAR_METHOD.md` | see rows 70 and 71 | copied; note |
| 215 | 7 | "Three answers"; "the five categories"; "the first two" | none | counts in the text | count |
| 216 | 7 | "whether the AIS feed for the Caspian changed in 2021 or 2022" | `outputs/tables/index_roro_step.csv` | break months, see row 88 | copied |
| 217 | 7 | "Kuryk has about as many Sentinel-1 passes as Alat" | `research/s1_revisit.json` | sum of `passes` 2019 to 2026: Kuryk 692, Baku/Alat 703 | derived (sum) |
| 218 | 8 | "`python -m mcm.build` rebuilds the index and validation tables" | `README.md` | "How to reproduce" | copied |

## Numbers that do not come from a result table

The brief allows four kinds of source: `outputs/tables/`, `data/official/official_figures.csv`, `research/s1_revisit.json`, and works in `research/references.bib`. The rows below rest on something else and should be checked with extra care.

| Rows | What | Why it is used |
|---|---|---|
| 1, 26, 213 | `data/portwatch/snapshot.json` (download date, days per port, first and last day) | The only file that records the PortWatch download |
| 25, 56, 58 to 62, 64 | `src/mcm/index.py`, `src/mcm/validate.py` (port ids, definitions, windows, parameters) | Method settings, not results |
| 32, 33 | `research/STEP1_RESEARCH.md` section a (PortWatch point for "Baku Port"; the 43 km distance is an author estimate) | The brief asks for the Baku point location |
| 21 | `research/STEP1_RESEARCH.md` section d (Caspian not in the published study area of Paolo et al.) | The study-area file is not in `references.bib` |
| 66 to 69, 71, 200 | `research/SAR_METHOD.md` (detector settings, zones, 128 empty tiles, platform dates) | The brief asks for the detector in a few sentences |
| 110, 180 to 184, 186, 206 | `research/FERRY_FLEET.md` (vessel pages on VesselFinder, read 13 November 2026; not in `references.bib`) | The brief asks for the ferry classification from this file |
| 14 to 20, 27 to 29, 31, 114, 142, 171, 185, 212 | Claims about cited works. They were taken from the reading notes in `research/LITERATURE.md` and `research/STEP1_RESEARCH.md`. The works themselves were not re-opened while drafting | Each is tied to a key in `references.bib` |
| 22, 113 | `research/LITERATURE.md` (what could not be searched; no documented break) | Statements about the search, not data |

## Changes after the independent check (13 November 2026)

A second pass checked all rows above against the files (216 of 218 reproduced). The paper was then corrected and shortened. Rows above that quote a sentence no longer in the paper are superseded by this section: rows 152 and 200 were wrong as written; the "4.5 to 4.7 Mt" vice-minister figure, the comparator figure (old Figure 2), the Kuryk 2025 contradiction and the 2019/2025 PortWatch monthly ranges at Aktau were removed. Old Figures 3 and 4 are now Figures 2 and 3.

New or changed numbers, all from `outputs/tables/paper_checks.csv` (written by `research/paper_checks.py`) unless another file is named:

| Section | Claim as written | Source | Row / column | How |
|---|---|---|---|---|
| Abstract, 5.2 | Kuryk ferry calls "412 to 618 (+50%)", cargo "by 87%" | `paper_checks.csv` | `kuryk_ferry_calls_change_2021_2022` 0.5000; `kuryk_tonnes_change_2021_2022` 0.8717 | rounded |
| 5.2 | PortWatch Ro-Ro calls at the three ports "rose by 288%" | `paper_checks.csv` | `caspian_roro_calls_change_2021_2022` 2.8770 | rounded |
| Abstract, 5.6, Table 4 note | Kuryk share "18% to 30%"; 2020 "12.5% as published", "29.2%" and "1,560.1 kt" if transposed | `paper_checks.csv`; `validate_blind_spot.csv` | `kuryk_share_min_if_transposed` 0.1786 (2021); `kuryk_share_2020_as_published` 0.1249; `kuryk_share_2020_if_transposed` 0.2922; AMCT 2020 `tonnes_total` 1,560,104 in `data/official/official_figures.csv`; maximum 0.295 (2023) in `validate_blind_spot.csv` | rounded |
| 5.6 | ferry cargo equals Kuryk's tonnage "within 0.5% in every other year and equals AMCT's in 2020" | `paper_checks.csv` | `ferry_cargo_over_kuryk` 1.0006 to 1.0043 for 2019, 2021 to 2025; 2.3458 for 2020; `ferry_cargo_over_amct` 2020 = 1.0026 | derived |
| 5.6 | "an Aktau port report gives AMCT 667 kt for 2020" | `data/official/README.md` | contradictions table, row "AMCT 2020" | note |
| Table 3 note | Aktau + AMCT tonnes with the 2020 pair exchanged: "0.69, 0.65 (7), 0.20 (6)" | `paper_checks.csv` | `aktau_amct_tonnes_if_transposed` mean_ratio 0.6889, level_r 0.6453, yoy_r 0.2026 | rounded |
| 5.3 | "worsens it for tonnage (0.67 against 0.82)" | `validate_summary.csv` | Aktau incl. AMCT / Aktau, `tonnes_total`, `all_tonnes`, `mean_ratio` | rounded |
| 5.3 | January to September 2026: port "1.73 Mt", PortWatch "1.02 Mt", "ratio of 0.59" | `validate_periods.csv` | Port of Baku, `tonnes_dry`, 2026-01-01 to 2026-09-30, `dry_tonnes`: official 1,730,000, portwatch 1,024,625, ratio 0.5923 (status opened) | rounded |
| 5.4 | without the 2022 change: "0.27 and 0.42 (n = 5)", headline "-0.90" | `paper_checks.csv` | `route_total_yoy_r_without_2022`: roro_calls 0.2692, tanker_calls 0.4215, dry_calls -0.9042 | rounded |
| 5.4 | "56 pairs tested on five or six points" | `validate_summary.csv` | `yoy_n` is 5 or 6 in all 56 rows | copied |
| 5.1 | comparator "rise by 19% in 2022, against 28% for the Caspian" | `paper_checks.csv` | `blacksea_dry_calls_change_2021_2022` 0.1877; `caspian_dry_calls_change_2021_2022` 0.2779 | rounded |
| 5.2 | Poti: "no Ro-Ro calls from December 2020 to March 2021", "18 in 2021 against 42 in 2020 and 46 in 2022" | `paper_checks.csv` | `poti_roro_calls` | copied |
| 5.2 | general cargo breaks "September 2022 at Baku, July 2021 at Aktau and October 2022 at Turkmenbashi" | `index_roro_step.csv` | `general_cargo_calls` rows, `break_month` | copied |
| 5.2 | "33,671 wheeled vehicles in 2019 and 54,200 trucks in 2023" | `data/official/official_figures.csv` | Port of Baku, `trucks`, 2019 (note 'wheeled vehicles') and 2023, status step1 | copied |
| 2 | "about half of which can be set against a PortWatch period" | `validate_periods.csv` | 264 distinct official values (plus 24 derived increments) of 517 rows | derived |
| 2 | association's 2024 figure "via the seaports of Kazakhstan and Azerbaijan" | `data/official/README.md`; `official_figures.csv` | TITR 2024, 3.3 Mt, `definition` | note |
| 4.3 | "a rule that removes fixed objects (73 blobs)" | `research/SAR_METHOD.md` | sections 4 to 6 | note |
| 5.6 | Sentinel-1A "(January to June)", Sentinel-1D "(from 25 June)", "Only one Sentinel-1A pass falls after the first Sentinel-1D pass" | `sar_scene_counts.csv` via `paper_checks.py` | first 1D pass 2026-06-25, last 1A pass 2026-06-29; `s1a_passes_after_first_s1d_pass` 1 | derived |
| 5.6 | Sentinel-1A monthly mean "from 2.7 in January to 11.7 in June" | `paper_checks.csv` | `s1a_2026_roadstead_monthly_mean` 2026-01 2.7143, 2026-06 11.7143 | rounded |
| 5.6 | basin count and sea state "(+0.12 and +0.14)" | `sar_diagnostics.csv` | `spearman_count_vs_sea_vv_level` basin 0.116; `..._vh_level` basin 0.138 | rounded |
| 5.6 | "operator assumed for three" | `research/FERRY_FLEET.md` | fleet table, operator column | note |
| 6 | Turkmenbashi 2025: PortWatch tonnage "9% of the official total" | `paper_checks.csv` | `turkmenbashi_2025` ratio 0.0923 (675,647 / 7,316,326) | rounded |
| 2, 6 | "The World Bank's September 2026 report ... was not opened" | `research/OPEN_QUESTIONS.md` | item 9 | note |

## Changes after the research pass (14 November 2026)

Sources marked "re-opened" were opened again by the person assembling the paper; "agent" means opened once by a research agent (notes in `research/DEEP_*.md`).

| Section | Number or claim | Source | Status |
|---|---|---|---|
| 2 | Association chart: 1.867 Mt (2025), 1.857 Mt (2024) | middlecorridor.com home-page chart `grafik_green_2026.svg` | re-opened (values read from the rendered image) |
| 2 | Ministry series 4.484 Mt (2024) | `data/official/official_figures.csv` | as before |
| 2 | Association press release 3.3 Mt (2024) | middlecorridor.com news of 4 March 2025 | agent |
| 2 | World Bank 2026: no AIS or satellite data; 8.8 Mt across the Caspian in 2023 is model output | World Bank (2026), PDF p. 85 to 91, 241 | agent |
| 2 | CyberLeninka search found no such work | `research/DEEP_RORO_AND_REGIONAL.md` | agent |
| 3.1 | Port call = arrival at berth; provider named as Kpler | PortWatch FAQ, ArcGIS item 640b69a4a96f41a6937cb4d2984f26da | re-opened |
| 3.1 | Provider exactEarth (2021 method paper), Spire (dataset description) | `research/DEEP_PORTWATCH_METHOD.md` finding 3.6 | agent |
| 5.2 | Coverage change November 2021 at Gwangyang and the Malacca Strait | PortWatch FAQ | re-opened |
| 5.2 | Ro-Ro calls 2 (Mar to May 2021), 20 (Jul), 33 (Aug), 61 (Dec); all calls mean 250 and 306 | `outputs/tables/coverage_break_check.csv` | own code |
| 5.6 | Kuryk 1,560 kt and North Terminal 667 kt | Aktau port strategy 2022 to 2032, p. 7 | re-opened |
| 5.6 | Two more ferries (Mingachevir, Ordubad) | `research/DEEP_RORO_AND_REGIONAL.md` | agent |
| all | Citation line now "Sources: Kpler; UN Global Platform; IMF PortWatch" | PortWatch FAQ | re-opened |

Not reproduced: the agent's Gwangyang query (298 calls in October 2021, 1,205 in December). The service refused requests on 14 November, so these figures are not in the paper.

## Changes after the radar labels (14 November 2026)

All from `outputs/tables/sar_label_eval.csv` (written by `research/sar_label_eval.py` from `data/sar/model_labels.csv`). Every one of these numbers rests on AI labels (`claude-opus-5-5`) that no person has checked.

| Section | Claim as written | Source | Row / column | How |
|---|---|---|---|---|
| Abstract, 5.6 | roadstead "131 of 132 decided", basin "7 of 34" | `sar_label_eval.csv` | precision rows: roadstead `yes` 131, `no` 1; basin `yes` 7, `no` 27 | copied; derived (yes + no) |
| 4.3 | "186 detections", "128 tiles", "all 314 image chips", "a fixed random 50 chips" | `data/sar/model_labels.csv` | 186 detection + 128 empty_tile rows = 314; `human_check` = 1 on 30 detection and 20 empty_tile rows (seed 20261114) | count |
| 5.6 | roadstead "99%, 95% interval 96% to 99.9%; 6 unsure" | `sar_label_eval.csv` | roadstead precision: `value` 0.9924, `ci95_low` 0.958, `ci95_high` 0.9987, `unsure` 6, `n` 138 | rounded |
| 5.6 | basin "21%, 10% to 37%; 14 unsure" | `sar_label_eval.csv` | basin precision: `value` 0.2059, `ci95_low` 0.1034, `ci95_high` 0.3682, `unsure` 14, `n` 48 | rounded |
| 5.6 | "no vessel in the roadstead (0 of 64)" | `sar_label_eval.csv` | roadstead missed-vessel row: `yes` 0, `unsure` 0, `n` 64 (Wilson upper bound 0.057, not quoted) | copied |
| 5.6 | "a clear one in 2 of 64 in the basin (5 more possible)" | `sar_label_eval.csv` | basin missed-vessel row: `yes` 2, `unsure` 5, `n` 64 | copied |
| 4.3 | "a 10-chip spot check" (paper gives no agreement figure; detail in SAR_METHOD 9.1) | `outputs/tables/sar_label_agreement.csv` | detections `n_labelled_by_human` 5, `agreement` 0.6 (3 of 5; the 2 others are `model_is_vessel` unsure, `is_vessel` yes in `label_sample.csv` S0006, S0010); empty tiles 5, `agreement` 1.0 | derived: 3 + 5 = 8 |
| 7 | "a fixed random 50 chips" | `data/sar/model_labels.csv` | `human_check` = 1 | count |
