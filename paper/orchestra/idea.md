# idea.md — Middle Corridor Monitor (PaperOrchestra input 1 of 2)

Built on 15 November 2026 from `paper/paper.md`, `paper/NUMBERS.md`, `research/SAR_METHOD.md` and
`research/OPEN_QUESTIONS.md`. Only facts that are in the repository. Numbers are in `experimental_log.md`.

## Problem

The Middle Corridor carries freight between Central Asia and Europe. Its sea leg crosses the Caspian between
Aktau and Kuryk (Kazakhstan), Turkmenbashi (Turkmenistan) and the Port of Baku at Alat (Azerbaijan).
How much cargo crosses is not settled: the Kazakh Ministry of Transport and the route association publish
totals that agree up to 2022 and part afterwards, and neither publishes a definition. The institutional
reports the authors read (World Bank 2023 and 2026, OECD 2023 and 2025, EBRD 2023, ADB 2024, CAREC 2022 and
2024) take their volumes from operators, the association, railways, port authorities, surveys or models.
None uses ship-tracking (AIS) or satellite data. So the official figures have no independent benchmark.

## What is proposed

Not a new method. A check of whether open data can serve as that benchmark:

1. An open, reproducible monthly index: non-tanker port calls (container, dry bulk, general cargo, Ro-Ro) at
   Baku, Aktau and Turkmenbashi from IMF PortWatch `Daily_Ports_Data`, 2019 monthly mean = 100, with Ro-Ro
   calls, tanker calls, PortWatch dry tonnage and a Black Sea comparator (Poti + Batumi) alongside.
2. A file of 517 official figures with status and source, and a validation that uses no estimates
   (cumulative releases are differenced only against the previous release of the same year; a PortWatch
   value is used only when PortWatch covers every day of the official period).
3. A first Sentinel-1 radar count at Alat: change detection against a per-pixel reference, two zones
   (harbour basin, roadstead), a labelling kit of 186 detections and 128 empty tiles.
4. A plain account of where each part fails.

## Research questions

1. Which official total does an AIS-based corridor index track?
2. How much traffic does AIS-based data miss?
3. Does the index predict the next official releases out of sample?

## Claimed contribution (narrow)

A monthly sum of PortWatch data is a re-aggregation, not a contribution in itself. The contribution is the
check: the reproducible index, the file of official figures, the radar count, and the documented failures.
The results are mostly negative.

## Framing that must not change

- Working paper, preliminary, not peer reviewed.
- Results mostly negative; conclusions as in `paper/paper.md`.
- Radar labels come from an AI model (Claude Opus 5.5) and have not been checked by a person beyond a
  10-chip spot check. The 50-chip human check was not done.
- The cause of the 2021-22 Ro-Ro step is not confirmed.
- Until a human radar check and answers from PortWatch exist, the index is a count of PortWatch port calls,
  not a measure of corridor cargo.

## Authors and roles

- Aghasalim Mustafazada (Howest University of Applied Sciences, Belgium; third-year bachelor student,
  Creative Technologies & AI): Sentinel-1 radar detection, the labelling kit, the project page, the figures.
- Teymur Eyvazov (University of Massachusetts Boston, USA): the index, the statistics, the validation
  against official figures.

## Venue

SSRN working paper 7706118 (under review); planned for arXiv econ.GN, cross-listed to stat.AP. arXiv prefers
TeX source; this LaTeX version is for that.
