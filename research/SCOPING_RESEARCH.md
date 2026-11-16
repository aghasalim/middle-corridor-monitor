# Middle Corridor Monitor: scoping research (13 Nov 2026)

Status of each claim: **checked** = the query was run or the page opened directly; **agent** = an AI research assistant opened the page and read the number, and it was not re-opened; **snippet** = seen only in a search result; **unverified** = not confirmed.

## a) PortWatch "Baku Port" — checked, boundary unverified

- PortWatch ports database (ArcGIS `PortWatch_ports_database`): `port100`, "Baku Port", lat 40.2846, lon 49.7325, no LOCODE.
- OpenStreetMap reverse geocode puts that point on the Baku–Alat highway, on the coast between Baku and Alat. It is roughly 14 km south-west of the old city port and roughly 43 km north-east of Alat (my distance estimate from approximate coordinates). So the point is neither the old port nor Alat.
- "Baku Port" is the only Azerbaijani entry. Alat, Sangachal and Dubendi are not listed separately. PortWatch does not publish port polygons, so whether Alat's ferry terminal lies inside the Baku boundary is **unverified**.
- Indirect evidence that it is a wide Baku-area aggregate: in 2025 PortWatch shows 720 tanker calls and 3.75 Mt tanker cargo at "Baku Port", but Port of Baku (the company) is mostly a dry-cargo port and counts only about 1.8 Mt oil (Dubendi, 2024).
- Other Caspian entries: Aktau (port16), Bautino, Turkmenbashi (port1330), Okaram, Kiyanly, Astrakhan, Makhachkala, Anzali, Amirabad, Nowshahr. **Kuryk is not listed.** Black Sea: Poti (port1016), Batumi (port127), Kulevi, Supsa.
- Data run 2019-01-01 to 2026-11-06 for all five ports (about one week lag).

## b) Rail ferries and Ro-Ro in PortWatch — partly checked

- Checked (dataset description): five ship categories — container, dry bulk, general cargo, Ro-Ro, tanker. Passenger ships are not a category. Port calls under 5 hours with no draught change are dropped. Tonnage = change in draught-based payload × deadweight.
- Unverified: whether Caspian rail ferries are classed as Ro-Ro or as passenger/Ro-Pax (and so dropped). The description does not say.
- Checked (my query of `Daily_Ports_Data`), yearly Ro-Ro calls:

| Port | 2019 | 2020 | 2021 | 2022 | 2023 | 2024 | 2025 | 2026 to 6 Nov |
|---|---|---|---|---|---|---|---|---|
| Baku | 126 | 131 | 119 | 496 | 518 | 479 | 410 | 371 |
| Aktau | 36 | 35 | 28 | 147 | 183 | 172 | 185 | 163 |
| Turkmenbashi | 78 | 96 | 97 | 303 | 305 | 243 | 183 | 203 |

- The fourfold jump in 2022 happens at all three ports at once. It may be the real 2022 rerouting, or a change in AIS coverage or vessel classification. **Unverified — must be resolved before any index is trusted.**
- PortWatch tonnage for Baku 2025: tanker 3.75 Mt (import 3.32, export 0.44), all dry cargo 0.97 Mt, Ro-Ro 0.33 Mt. Official Port of Baku 2025: more than 8.2 Mt in total. PortWatch's dry-cargo tonnage is therefore several times below the official non-oil figure. The areas are not the same, so this is a first indication, not a result.
- PortWatch total tonnage (import + export), 2025: Baku 4.72 Mt, Aktau 3.49 Mt, Turkmenbashi 0.68 Mt, Poti 3.66 Mt, Batumi 3.28 Mt.

## c) Sentinel-1 revisit — checked

Copernicus Data Space catalogue, product type IW_GRDH_1S, scenes containing the port point, one pass = one platform + orbit. Script: `s1_revisit.py` (to be moved into the project repo in Step 2).

| Port (point used) | 2019 | 2020 | 2021 | 2022 | 2023 | 2024 | 2025 | 2026 to 12 Nov | Mean gap |
|---|---|---|---|---|---|---|---|---|---|
| Baku / Alat (39.98, 49.43) | 85 | 89 | 90 | 86 | 91 | 90 | 93 | 79 | about 4 days |
| Aktau (43.60, 51.23) | 54 | 60 | 59 | 54 | 59 | 61 | 63 | 53 | about 6 days |
| Kuryk (43.16, 51.44) | 82 | 90 | 88 | 83 | 88 | 90 | 93 | 78 | about 4 days |
| Turkmenbashi (40.01, 53.01) | 115 | 118 | 120 | 113 | 119 | 119 | 122 | 106 | about 3 days |

- Sentinel-1B never imaged these ports; all passes 2019–2024 are Sentinel-1A. Sentinel-1C appears a handful of times in 2025; Sentinel-1D supplies about 45% of 2026 passes.
- A pass every 3–6 days cannot count ferry crossings (a ferry turns round in under a day). It can only give snapshots of ships present.

## d) Global Fishing Watch SAR detections — checked for the paper, unverified for the live product

- Paolo et al. (Nature 2024) publish their study area on figshare (doi 10.6084/m9.figshare.24309475, `study_area.csv`, CC BY 4.0). Of 18,714 polygons, **none** has a vertex in the Caspian (lon 46.5–54.8, lat 36.5–47.2). The same test finds 144 polygons in the Black Sea and 612 in the Persian Gulf. The 2017–2021 paper data do not cover the Caspian.
- The paper also drops everything within 1 km of shore, so ships at berth are excluded anywhere.
- Whether the live GFW dataset (2017 to 5 days ago) has added the Caspian is **unverified**; checking needs a free GFW account and API token.
- Detection performance stated in the paper: over 95% of vessels above 50 m, about 80% for 25–50 m, most vessels under 15 m missed.

## e) Official figures — collected by research agent; one row spot-checked by me

No regular monthly series exists for any of the four entities. Port of Baku figures arrive as cumulative press releases (Q1, H1, 9, 10, 11 months, annual) through Azerbaijan Railways; Aktau, Kuryk and TITR are irregular.

### The three conflicting 2025 totals

| Figure | Source | What it says | Status |
|---|---|---|---|
| 1.867 Mt, 76,900 TEU (+36%) | TITR Association via bm.ge (page returned 403) | "1.867 million tons of cargo moved through the Middle Corridor" | **snippet only**; not found on middlecorridor.com |
| 4.119 Mt (2024: 4.484) | Kazakh Ministry of Transport via [Astana Times](https://astanatimes.com/2026/03/trans-caspian-transport-route-cargo-volumes-increase-fivefold-in-seven-years/), [bizmedia.kz](https://bizmedia.kz/2026-03-10-za-7-let-tmtm-uvelichil-perevozki-pochti-v-5-raz/) | Route cargo per year, no definition of modes or border | agent |
| 4.5–4.7 Mt | Vice Minister Nusupov via [Trend](https://www.trend.az/casia/4213821.html) | "total cargo traffic" by end of 2025 | agent |
| 16,909.8 kt | [stat.gov.az release 16 Feb 2026](https://stat.gov.az/special_version/news/index.php?id=6620) | East-West corridor through Azerbaijan, all modes; of which Europe-Caucasus-Asia corridor 8,173.2 kt; sea transport through corridors 7,229.7 kt (93.3% transit) | **checked** |

The Azerbaijani figure is all cargo crossing Azerbaijan by rail, road and sea, so it is not a measure of the Caspian leg. The TITR Association's own 2024 figure was 3.3 Mt "via Kazakh and Azerbaijani seaports" ([middlecorridor.com, 4 Mar 2025](https://middlecorridor.com/en/press-center/news/04-03-2025)); a 2025 figure of 1.867 Mt that "slightly exceeds 2024" must be on a different basis. Which basis is unverified.

### TITR route series (Kazakh Ministry of Transport, agent)

| Year | 2019 | 2020 | 2021 | 2022 | 2023 | 2024 | 2025 |
|---|---|---|---|---|---|---|---|
| Mt | 0.759 | 0.783 | 0.586 | 1.485 | 2.764 | 4.484 | 4.119 |

Source: [bizmedia.kz, 10 Mar 2026](https://bizmedia.kz/2026-03-10-za-7-let-tmtm-uvelichil-perevozki-pochti-v-5-raz/). Other TITR numbers: 2022 33,000 TEU ([Astana Times](https://astanatimes.com/2023/12/cargo-transportation-along-middle-corridor-soars-88-reaches-2-million-tons-in-2023/)); 2024 56,500 TEU (TITR Association, link above); 2025 "about 77 thousand TEU" ([gov.kz](https://www.gov.kz/memleket/entities/transport/press/news/details/1177616?lang=ru)); 2025 42,000 TEU "on the route" per KTZ ([railways.kz](https://railways.kz/en/news2026/development-titr-discussed/)) — conflicts with 77,000.

### Port of Baku (agent)

| Period | Tonnes | TEU | Other | Source |
|---|---|---|---|---|
| 2019 | 4,061.6 kt (transit 3,444.2 kt) | 35,152 | 44,175 wagons; 33,671 wheeled vehicles | [PortNews](https://en.portnews.ru/news/290601) |
| 2020 | 4.8 Mt (transit 87%) | 40,345 (40,395 in a later source) | 43,218 trucks | [TRACECA](https://traceca-org.org/en/news/single-news/n/baku_port_increases_cargo_turnover_by_20_pct_in_2020), [APA](https://en.apa.az/corridors/record-turnover-at-port-of-baku-annual-container-throughput-reaches-100000-teu-486763) |
| 2021 | 5.6 Mt (transit 92.7%) | 45,025 | oil over 1.1 Mt (Dubendi) | [PortNews](https://en.portnews.ru/news/325155) |
| 2022 | 6.3 Mt | — | — | [AzerNews](https://www.azernews.az/business/220584.html) |
| 2023 | about 7.4 Mt (transit 5.3 Mt) | 43,900 | 37,300 wagons; 54,200 trucks; oil 2.1 Mt | [Report](http://report.az/en/infrastructure/cargo-handling-at-baku-port-climbs-up) |
| 2024 | 7.6 Mt (transit 5.3 Mt) | 76,800 | 37,500 wagons; 58,200 trucks; oil 1.8 Mt; dry 1.044 Mt | [Trend](https://www.trend.az/business/4018095.html) |
| H1 2024 | 3,695,910 t | 30,869 | — | [Report](https://report.az/en/infrastructure/cargo-turnover-at-baku-port-up-by-over-6-in-first-half-of-2025) |
| Q1 2025 | over 1.9 Mt | 30,034 | 7,765 wagons; 13,711 wheeled | [Report](https://report.az/en/infrastructure/baku-port-sees-nearly-9-increase-in-cargo-handling) |
| H1 2025 | 3,930,521 t | over 53,030 | — | same as H1 2024 row |
| Jan–Sep 2025 | 6.108 Mt | 77,295 | — | [Report](https://report.az/en/infrastructure/baku-international-sea-port-handles-over-6m-tons-of-cargo-in-9-months) |
| Jan–Oct 2025 | nearly 7 Mt | 86,000 | — | [Report](https://report.az/en/infrastructure/ady-cargo-handling-at-baku-port-surges-by-nearly-6) |
| Jan–Nov 2025 | 7.547 Mt | over 100,000 by 18 Dec | — | [APA](https://en.apa.az/corridors/record-turnover-at-port-of-baku-annual-container-throughput-reaches-100000-teu-486763) |
| 2025 | over 8.2 Mt | 107,000 | — | [Ministry of Economy](https://mincom.gov.az/en/media-en/news/record-transit-freight-volumes-highest-level-in-five-years) |
| Jan–Jul 2026 | dry cargo 1.4 Mt | 72,370 | — | same |

### Aktau, Kuryk, Kazakh seaports (agent)

| Entity | Period | Value | Source |
|---|---|---|---|
| Aktau | 2022 | over 3.85 Mt (oil 2.5 Mt, grain 447 kt) | [Ports Europe](https://www.portseurope.com/kazakh-port-of-aktau-handle-3-8-million-tonnes-of-cargo-in-2022/) |
| Aktau | Jan–Jul 2023 | over 2.6 Mt; over 13,000 containers | [Trend](https://www.trend.az/casia/kazakhstan/3792392.html) |
| Aktau | Jan–Aug 2024 | over 3 Mt | [KTZ Express](https://ktze.kz/en/news/c368be52-df73-492b-898d-bea0443594c9) |
| Aktau | 2024 / 2025 forecast | 58.5k / 65k TEU transit | [Argus](https://www.argusmedia.com/pt/news-and-insights/latest-market-news/2723885-tranzit-konteynerov-cherez-aktau-vyrastet-v-2026-g.) |
| Kuryk | Jan–Aug 2023 | about 1.5 Mt; 480 ferry calls; about 13,800 wagons; over 18,000 vehicles | [KTZ](https://railways.kz/en/news/about-15-million-tons-cargo-were-transshipped-through-port-kuryk/) |
| Kuryk | Jan–Oct 2023 | 1.8 Mt; about 600 ferry calls | [bizmedia.kz](https://bizmedia.kz/2023-11-28-morskoj-port-kuryk-uspeshno-obrabotal-bolee-18-milliona-tonn-gruza/) |
| Kuryk | 2024 | 1,957,800 t (rail 1,150,600; road 781,300; grain 25,900) | [Sputnik KZ](https://ru.sputnik.kz/20250128/cherez-port-kuryk-v-2024-godu-perevaleno-okolo-dvukh-millionov-tonn-gruzov-50366321.html) |
| Kuryk | May 2025 | 267,000 t (monthly record) | [Trend](https://www.trend.az/business/transport/4054130.html) |
| Kuryk | H1 2026 | 884,800 t | [Trend](https://www.trend.az/casia/4213821.html) |
| KZ seaports | Jan–Nov 2023 | 6.5 Mt | [primeminister.kz](https://primeminister.kz/en/news/for-11-months-of-2023-transportation-through-seaports-amounted-to-65-million-tons-karabayev-26627) |
| KZ seaports | 2023 | 7.2 Mt | [Trend](https://www.trend.az/casia/kazakhstan/3866319.html) |
| KZ seaports | Jan–Oct 2024 | 6.2 Mt | [Times of Central Asia](https://timesca.com/kazakhstans-caspian-sea-ports-increase-cargo-transportation/) |
| KZ seaports | 2025 | 8 Mt; 90,637 TEU | [Interfax KZ](https://www.interfax.kz/en/news/78594), [Astana Times](https://astanatimes.com/2026/02/kazakhstan-strengthens-its-role-as-eurasian-transit-hub-with-36-9-million-tons-of-freight-in-2025/) |

Gaps: Aktau annual tonnage 2019–2021 and 2023–2025 (the port's annual-report PDFs on portaktau.kz exist but were not read); Kuryk annual totals except 2024; any separate ferry tonnage for Baku; TITR Association's own releases for 2019–2023. portofbaku.com and kuryk.kz were not opened.

## f) Prior work — research agent; EPINOVA page and PortWatch spot-checked by me

Nothing identical was found: no open, recurring, documented index of the Caspian leg. Closest:

1. **IMF PortWatch** — open daily port calls and tonnage for Baku, Aktau, Turkmenbashi. A monthly sum of these is a reaggregation, not a contribution. Method papers: Arslanalp, Koepke, Verschuur, IMF WP 2021/225; "Nowcasting Global Trade from Space", [IMF WP 2025](https://www.imf.org/en/publications/wp/issues/2025/05/16/nowcasting-global-trade-from-space-566957) (agent).
2. **EPINOVA "Caspian Port System Monitor" / Caspian Logistics Resilience Index** (S. Wu, policy briefs Apr–Jul 2026, e.g. [PB-47](https://publications.epinova.org/epinova-pb-2026-047/)) — arrivals and departures at Caspian ports, Russia–Iran framing, data source not named, dataset unpublished, irregular. Must be cited and distinguished.
3. **Texty.org.ua** — [Sentinel-1 points near Caspian ports, Jul 2022–Jun 2023](https://texty.org.ua/projects/110257), one-off, no code; [2026 follow-up](https://texty.org.ua/articles/117082/kaspijskyj-ekspres-rosijska-dopomoha-iranu-tryvaye-infohrafika/) using Global Fishing Watch AIS (agent).
4. **Lloyd's List Intelligence** — Caspian AIS-gap counts, Russia–Iran, paywalled ([2022 article](https://www.lloydslist.com/LL1142744/Suspicious-activity-rises-in-Caspian-Sea-as-Russia-looks-for-supply-chain-alternatives)) (agent).
5. **CAREC CPMM** — annual corridor performance reports with a TITR port case study, survey-based, no AIS ([2022 report](https://cpmm.carecprogram.org/2022-report/)) (agent).
6. **Caspian Policy Center** — [Middle Corridor Live Map](https://caspianpolicy.org/research/maps/middle-corridor-live-map), infrastructure only (agent).

Not searched directly: Google Scholar, SSRN, RePEc, ResearchGate (Semantic Scholar, OpenAlex and web search were used). Not read: World Bank 2023 Middle Corridor report, OECD report (403), CAREC Middle Corridor assessment.

## g) arXiv — checked

- [Policy change of 21 Jan 2026](https://blog.arxiv.org/2026/01/21/attention-authors-updated-endorsement-policy/): an institutional email alone no longer qualifies. A new submitter needs an institutional email **and** prior authorship of an accepted arXiv paper in that domain, or else a personal endorsement from an established arXiv author in the same domain. One endorsement per endorsement domain ([help page](https://info.arxiv.org/help/endorsement.html)).
- Neither author has an arXiv paper (to my knowledge), so a personal endorser is needed.
- Category (my recommendation, taxonomy not re-read today): `stat.AP` or `econ.GN` as primary, cross-list `cs.CV` for the ship detection.
- SSRN requirements not checked.
