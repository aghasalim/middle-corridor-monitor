# Sentinel-1 ship detections at Alat — method, first results, limits (13 Nov 2026)

**Status: unvalidated.** Everything below counts *bright transient blobs on water* in radar images.
No detection has been checked by a person or against AIS. Precision and recall are unknown.
Do not quote these numbers as vessel counts or as traffic until the hand labels in section 9 exist.

Every number here was produced by the code in `src/mcm/sar/` and can be found in the files named next to it.

## 1. Data source and scenes

- **Source:** Microsoft Planetary Computer, STAC API `https://planetarycomputer.microsoft.com/api/stac/v1`,
  collection `sentinel-1-grd`, anonymous (URLs signed with the `planetary_computer` package, no account).
  Product: IW GRDH, VV+VH, 10 m pixels, about 20 m x 22 m resolution. Only the window over the port is read over HTTP.
- **Time coverage of the source:** the collection starts 2014-10-10 and is open-ended. The latest pass over Alat
  on 13 Nov 2026 was 2026-11-10. This run uses 2019-01-01 to 2026-11-10.
- **Passes** (one pass = platform + absolute orbit; `outputs/tables/sar_scene_counts.csv`, one row each, with status):

  | | passes |
  |---|---|
  | found in the catalogue search over the working grid | 769 |
  | read without error | 769 (0 failed) |
  | **counted** (data over at least 99.9 % of both zones) | **671** |
  | partial coverage, not counted (`S1A_..._20250223T143708`, 99.65 %) | 1 |
  | no data over the grid, not counted (relative orbit 101, whose footprint only touches the grid) | 97 |

  Counted passes by relative orbit: 6 (descending, about 02:52 UTC, near range) 228; 28 (ascending, about 14:37 UTC) 226;
  108 (descending, about 02:44 UTC, far range) 217. By platform: Sentinel-1A 634, 1C 3, 1D 34.
  Mean gap between counted passes 4.3 days, median 5.0, longest 18.5.
- **Missing at the source:** the Copernicus catalogue lists 703 passes over the port for 2019–2026
  (same query as `research/s1_revisit.py`); Planetary Computer holds 672 of them. The 31 missing passes
  (2 in 2019, 8 in 2020, 4 in 2021, 2 in 2022, 5 in 2023, 10 in 2024, none in 2025–2026) are listed in
  `outputs/tables/sar_missing_at_source.csv`; per-year totals in `sar_source_coverage.csv`.
  They could only be fetched with a Copernicus or Earthdata login, so they were left out.
- Counted passes per year: 83, 81, 86, 84, 86, 80, 92, 79 (2019 … 2026 to 10 Nov).

## 2. Putting the image on a map (a correction that mattered)

GRD images are in radar geometry with 210 ground control points (GCPs). Two things were wrong with the easy route:

1. GDAL's default polynomial fit through the GCPs was off by up to about 200 pixels, so a thin-plate spline
   (exact at the GCPs) is used instead.
2. Each GCP sits at its own terrain height (0 to more than 1000 m in these frames). A point at height *z* appears
   *z* / tan(incidence) closer to the radar. Interpolating between GCPs of different height shifted the sea surface
   by up to about 160 m, and by a different amount for each frame (frames were cut differently in 2019 and 2024).
   Fix: every GCP is first moved to one common height, the Caspian surface (−28 m), using the incidence angle
   approximated as linear from 29.9° to 45.9° across the swath (`fetch.py`).

Checks: after the fix the Sentinel-2 waterline falls on the quay edges in all three orbits and in 2019, 2021, 2024
and 2026 (looked at by eye, within 1–2 pixels; `outputs/figures/sar_zones.png` shows the result for orbit 28).
The shift between the first and the last counted pass of each orbit, measured by phase correlation over the port,
is 0.91 px (orbit 6), 0.10 px (orbit 28), 0.22 px (orbit 108) (`sar_diagnostics.csv`).
Not done: exact incidence angles from the annotation files, a DEM-based terrain correction. Near the port
positions look right to 1–2 pixels (10–20 m) by eye; this was not measured, and not checked further out.

Images stay in uncalibrated digital numbers. Only contrasts (dB differences inside one image, or against the same
pixel's history in the same orbit) are used, never absolute backscatter.

## 3. Area of interest

`data/sar/zones.geojson` (WGS84), drawn on Sentinel-2 true colour (1 Sep 2025) and the radar images, on a
15 km x 17 km UTM 39N grid with 10 m pixels. OpenStreetMap was consulted first: it has the ferry terminal
(39.9721–39.9730 N, 49.4426–49.4430 E) and the port outline but no berths, so the berths were located on the imagery.

- **basin** (0.79 km²): the dredged harbour — the 280 m x 670 m dock with the general-cargo/container quay on
  its east side, the two ferry berths and the Ro-Ro ramps on the west, the south quay, and the turning area down
  to 1 km south of the terminal. The polygon reaches about 30 m onto the quays so that a ship alongside is inside it.
- **roadstead** (96.7 km²): the approach channel from the basin to the bay mouth, and the open water south and
  east of the Alat spit. It was drawn generously **before** any detection was run and not changed afterwards.
  No chart or AIS was used; where ships actually anchor was learnt from the detections (`sar_detection_map.png`:
  a dense cloud south-east of the spit, 5–10 km from the dock (5th–95th percentile 4.9–10.3 km), and a line of detections along the dredged channel).
  The cloud is cut by the polygon's east edge: 26 of 2,488 counted roadstead detections lie in its last 500 m,
  so some waiting ships further east are not seen.

The offshore oil platforms north-east of the port are outside both zones.

## 4. Method in plain words

For every pass, both polarisations:

1. **Smooth.** Power is averaged over 3 x 3 pixels and turned into dB. This tames speckle.
2. **Usual picture of each pixel.** For each relative orbit and polarisation, the *25th percentile* over time of
   that pixel, using all passes of the same orbit within one year either side of 1 July of the pass's year.
   Same orbit means same viewing geometry, so quays and cranes fall on the same pixels every time.
3. **Mask what is always bright.** A pixel whose usual value is more than 10 dB above the usual value of open
   water is a quay, crane, breakwater or land. It is masked, plus one pixel around it. Only pixels inside the two
   zones are ever searched.
4. **Threshold (CFAR-style).** For each remaining pixel the reference level is the larger of (a) its own usual
   value and (b) the median of the water around it in this very image (500 m blocks). The pixel is a candidate if
   it is brighter than the reference by at least 6 dB, or by 3.5 times the local spread of the sea (90th minus
   50th percentile of the block) when that is larger. So a rough sea raises its own threshold.
5. **Blobs.** Candidates from VV and VH are merged (either polarisation is enough; both flags are kept).
   Touching pixels (8 neighbours) form one blob.
6. **Size rules.** The blob's length is measured on its "core" (pixels within 10 dB of its brightest pixel).
   Dropped: area under 8 pixels; core shorter than 5 pixels; area over 1,500 pixels; core longer than 300 m.
7. **Zone** by the blob centre. **Fixed objects** in the roadstead (same 50 m spot in 12 or more passes spread
   over at least 180 days) are flagged and not counted.

| Threshold | Value | Why |
|---|---|---|
| Temporal background | 25th percentile, same orbit and polarisation, ±1 year | A berth must be empty at least a quarter of the time to count as water; the median would need half. The 2-year window follows port works and the falling Caspian level. |
| Permanently bright | usual value > open water + 10 dB, +1 px | Quays and cranes are 15–25 dB above water. A first run with 4 dB masked most of the dock in orbits 28 and 108 (see section 6). |
| Minimum contrast | 6 dB over the reference | Smoothed speckle has a spread of about 1.5 dB; cargo ships are 15–30 dB above the sea. |
| Sea-spread factor | 3.5 x (p90 − p50) | Equals about 6 dB on a calm, even sea; grows where the sea is streaky. |
| Block for sea statistics | 500 m | Larger than any ship, small enough to follow wind fronts. |
| Minimum size | 8 px and core ≥ 5 px (50 m measured) | Resolution plus smoothing add about 20 m, so 50 m measured is about 30 m real. A bright point (buoy, small boat) measures 30–40 m and is dropped. |
| Maximum size | 1,500 px or core > 300 m | Caspian ferries are about 150 m. Larger blobs are merged targets, wakes or interference. |
| Coverage to count a pass | 99.9 % of zone pixels | Otherwise ships could be outside the image. |
| Fixed object | ≥ 12 passes within 50 m, ≥ 180 days apart, roadstead only | In the roadstead the count of passes per 50 m spot stops at 10 and resumes at 12 and above 40; the latter are objects that never move. Not used in the basin, where berths are reused. |

Two ships stay separate only if at least one pixel between them is below the threshold. With 10 m of water
between hulls the smoothing closes the gap and they become one blob (tested).

## 5. First results (unvalidated)

3,406 blobs kept in 671 passes; 73 flagged as fixed objects; **3,333 counted** (basin 845, roadstead 2,488).
Files: `data/sar/detections.csv`, `outputs/tables/sar_scene_counts.csv`, `sar_monthly.csv` (95 months), `sar_yearly.csv`.

| Year | Passes | Basin blobs | Roadstead blobs | Mean per pass, basin | Mean per pass, roadstead | Mean per pass, total | Median total |
|---|---|---|---|---|---|---|---|
| 2019 | 83 | 89 | 164 | 1.07 | 1.98 | 3.05 | 3 |
| 2020 | 81 | 84 | 203 | 1.04 | 2.51 | 3.54 | 3 |
| 2021 | 86 | 93 | 426 | 1.08 | 4.95 | 6.03 | 6 |
| 2022 | 84 | 123 | 444 | 1.46 | 5.29 | 6.75 | 6 |
| 2023 | 86 | 96 | 169 | 1.12 | 1.97 | 3.08 | 3 |
| 2024 | 80 | 120 | 231 | 1.50 | 2.89 | 4.39 | 4 |
| 2025 | 92 | 139 | 330 | 1.51 | 3.59 | 5.10 | 5 |
| 2026 (to 10 Nov) | 79 | 101 | 521 | 1.28 | 6.59 | 7.87 | 7 |

Over all counted passes: mean 1.26 basin, 3.71 roadstead, 4.97 total per pass; 23 % of passes have no basin
blob and 10 % no roadstead blob; the largest roadstead count in one pass is 19.

What these are: snapshots of bright objects present at the moment of a pass, every 4–5 days. They are **not**
arrivals, departures or cargo. A ferry turns round in under a day; a ship waiting a week is counted in two passes.

What can be said without labels: roadstead blobs are mostly large and strong (median length 154 m, median peak
contrast 23 dB VV; 91 % have a peak of 15 dB or more, so the count barely depends on the 6 dB threshold; 94 % are seen in
both polarisations) and they trace an anchorage and the dredged channel. That is what ships would look like, but it is
my reading of the pictures, not a validation.

## 6. Junk checks, and what was found and fixed

Table: `outputs/tables/sar_diagnostics.csv`; figure: `outputs/figures/sar_diagnostics.png`; hot spots: `sar_hotspots.csv`.

- **Do counts follow the wind?** Spearman correlation between the count per pass and the open-water level of
  that pass (a roughness proxy): roadstead −0.08 (VV) and −0.03 (VH); basin +0.12 (VV) and +0.14 (VH).
  No sign that the roadstead count tracks sea state. The basin count rises slightly with roughness
  (small but not zero, p < 0.01); cause not established.
- **Do the three orbits agree?** Mean per pass, roadstead: 3.46 / 3.67 / 4.00 (orbits 6 / 28 / 108). Basin: 1.24 / 1.10 / 1.45.
  **Found and fixed:** with the first setting (permanently bright = 4 dB above open water) the basin gave
  1.92 / 0.56 / 0.45. The dock's water is 1.5–3.5 dB brighter than the open sea in orbits 28 and 108, so most of the dock
  had been masked there. The threshold is now 10 dB. The orbits still differ by up to 30 % in the basin.
- **Does the same spot fire again and again?** Roadstead: 9 % of blobs have another blob within 50 m in another
  pass within 30 days, 0.3 % have five or more. Two places fired for years and are now flagged as fixed objects
  and not counted: 49.445 E 39.874 N near the south-west shore (60 blobs, Jan 2019 – Feb 2023) and
  49.497 E 39.941 N off the spit (13 blobs, Mar 2019 – Dec 2021). What they are is unknown.
  Smaller repeats remain unflagged, e.g. a spot at the channel exit (about 49.437 E 39.926 N) and one north-east
  of the spit (about 49.503 E 39.947 N, 8 passes 2019–2021).
  Basin: 75 % of blobs have a neighbour within 30 days and 19 % have five or more. The busiest 50 m cells fire in
  15 %, 14 %, 9 %, 8.5 % and 8 % of all passes; they sit at the south ends of the two ferry piers and at the south end of the dock's west quay.
  This is what berths in use would give, and also what a flickering quay edge would give. The data cannot tell them apart.
- **Interference.** The pass of 2019-08-18 has a block of corrupt VH data; its straight edge produced three
  "blobs" of 430–580 m. The 300 m limit now drops them (6 blobs dropped by the upper size rules in total). Shorter pieces of such
  artefacts would get through.
- **Frame joins.** 173 counted passes are split over two frames. Frames are merged by taking the larger value,
  so the dark border noise of one frame does not overwrite the other.
- **Platform.** In 2026 Sentinel-1A passes (Jan–Jun, 44) average 7.9 roadstead blobs and Sentinel-1D passes
  (Jun–Nov, 34) average 4.9. The two do not overlap in time, so a sensor difference cannot be separated from
  a real change. Unresolved.
- **One polarisation only.** Of the 3,333 counted blobs, 157 are VV only and 155 VH only. The few VV-only chips
  looked at were faint streaks (possibly wakes or azimuth ghosts). They are counted, and flagged in the CSV
  (`det_vv`, `det_vh`) so the labels can decide.

## 7. Known failure modes

- **Ships alongside a quay merge with it.** The quay and one pixel around it are masked, so of a ship at a berth
  only a strip 1–2 pixels wide survives. Basin blobs are small (median 16 pixels, median length 90 m) for that
  reason; lengths in the basin are not ship lengths. Two ships end to end at one quay can become one blob.
- **Busy berths disappear.** A berth occupied more than about three quarters of the time is, to this method,
  part of the quay. The basin count is therefore not the number of ships in port.
- **Cranes, containers, trucks and rail wagons** within about 30 m of the quay edge move, and are inside the
  basin polygon. They can be counted as ships.
- **Quay-edge flicker.** A registration error of up to about one pixel (0.9 px measured for orbit 6) next to a
  bright edge can lift a row of pixels over the threshold.
- **Sidelobes and azimuth ambiguities.** Strong ships show a bright cross and can throw displaced "ghosts",
  mostly in VV. The cross is usually part of the same blob; a ghost would be counted as a ship. Ghosts of the
  oil platforms and of land were not checked for.
- **Wind-roughened sea, fronts, slicks, rain cells.** The local threshold adapts, and the correlation test above
  is reassuring for the roadstead, but sharp fronts and small bright patches can still pass.
- **Radio interference and corrupt blocks** (seen once, see above).
- **Moored tugs, pilot boats, dredgers, barges and service craft** over about 30 m count like cargo ships.
  39 % of basin blobs and 10 % of roadstead blobs measure under 80 m.
- **Moving ships** are displaced from their wakes along the flight direction, and a bright wake can be detected
  as a second blob or lengthen the first. In the 500 m wide channel the displacement can move a ship out of the zone.
- **Rafted or close ships** merge (10 m gap: one blob).
- **Fixed objects in the roadstead** are only caught after 12 hits; anything that sat for months but under
  that is counted every time.
- **Falling Caspian level and shoals.** Sandbars emerging inside the roadstead polygon would start to fire.
  The polygon avoids the shallows seen in 2025, not future ones.
- **Snapshot, not flow.** A pass every 3–6 days at fixed local times (about 06:45 and 18:40). It gives ships
  present at those moments. It cannot count calls, and the two times of day may not be comparable.
- **Gaps.** 31 passes are missing at the source, unevenly by year (10 in 2024), and the longest gap is 18.5 days.
  Monthly figures rest on 3–9 passes.

## 8. What is not known

- **Precision** (how many blobs are vessels) — unknown, for both zones.
- **Recall** (how many vessels are missed) — unknown. In the basin it is certainly incomplete (section 7).
- Whether the basin series means anything at all. Treat it as unreliable until labelled.
- Whether the rise and fall of the roadstead count (2021–2022, 2026) reflects ships, sensor or processing.
  No comparison with PortWatch, AIS or port statistics has been made here.
- Vessel type. Nothing separates a ferry from a tanker, a dry-cargo ship or a naval or service vessel.
- Position accuracy away from the port.

## 9. Hand-labelling kit

- `data/sar/label_sample.csv` + `data/sar/label_chips/` (314 PNG chips, 5.8 MB), shuffled, built with a fixed random seed.
- **186 detection chips**, stratified by year and zone (basin 48, roadstead 138; at least 5 per year and zone).
  Each chip is 640 m across, north up, detection in the centre (yellow ticks on the edges point at it), with a 200 m bar.
  Three panels: VV, VH, and the mean VV image of that orbit (what is usually there: quays stay, ships do not).
  Fill in `is_vessel` = yes / no / unsure and `note`.
- **128 tiles where the detector found nothing** (8 per year and zone, 960 m across), to look for missed ships.
  Fill in `n_vessels_seen` (0 if none). The number 128 is a convenience, not derived from a formula.
- `python -m mcm.sar.report` will not overwrite the sheet once any label has been entered.
- A person will often be unable to decide for blobs at a quay at this resolution. Record those as "unsure";
  the share of "unsure" is itself a result. Better references for the basin: Sentinel-2 images of the same days,
  or AIS.

How many detections to check, n = z² p (1 − p) / e² with finite-population correction, z = 1.96,
population N = 3,333 counted detections (`outputs/tables/sar_sample_size.csv`):

| Assumed precision p | Margin | n, infinite population | n, with correction (N = 3,333) |
|---|---|---|---|
| 0.5 (worst case) | ±5 points | 385 | 345 |
| 0.5 | ±7 points | 196 | 186 |
| 0.5 | ±10 points | 97 | 94 |
| 0.8 | ±5 points | 246 | 230 |
| 0.8 | ±7 points | 126 | 121 |
| 0.8 | ±10 points | 62 | 61 |

**Recommendation: check 186 detections** (p = 0.5, ±7 points). Reasons: nothing is known about precision yet, so
the worst case p = 0.5 is the honest assumption; ±10 points cannot tell a usable detector (say 80 %) from a
poor one (65 %); ±5 points costs almost twice the work (345) for a gain smaller than the uncertainty the
"unsure" answers will add. The kit already holds exactly these 186.
Per zone this sample gives about ±8 points for the roadstead (138 chips) and ±14 points for the basin (48 chips).
If the basin is to be judged on its own at ±10 points, label 87 basin detections instead of 48.

## 10. How to reproduce

```
.venv/Scripts/python -m mcm.sar.fetch 2019-01-01   # download windows into data/sar/cache/ (git-ignored, 6.3 GB)
.venv/Scripts/python -m mcm.sar.run                 # detection + tables   (--post: flags and tables only)
.venv/Scripts/python -m mcm.sar.report              # figures, diagnostics, labelling kit
.venv/Scripts/python -m pytest tests/test_sar.py    # 15 tests, synthetic images, no network
```

Measured on this machine (4 cores): download of 769 passes 1,005 s with 3 parallel reads; detection 845 s from
scratch, 468 s with cached stacks; report 121 s.
The download was started four times while the grid, the geolocation and the frame joins were being fixed
(about 1,600 pass reads in total, a little over two full passes over the catalogue).

Code: `aoi.py` (grid, zones), `fetch.py` (catalogue, GCP mapping, windowed reads), `detect.py` (the detector,
no I/O), `run.py` (stacks, backgrounds, tables), `sample.py` (sample size, stratified sample), `report.py`
(figures, diagnostics, chips).
