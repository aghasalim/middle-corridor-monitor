# Middle Corridor Monitor — literature and methods (13 Nov 2026)

Extends `SCOPING_RESEARCH.md` (sections a, b, d, f, g); does not repeat it.
Tags: **opened** = I opened the page or PDF and read the passage; **abstract** = only the abstract/metadata record (Crossref/OpenAlex/publisher landing page) was read, not the full text; **snippet** = search-result text only; **not opened** = could not open.
PDFs read as text are in `E:\salim\middle-corridor-monitor-scratch\lit\` (outside the repo).

## Novelty verdict (five lines)

1. Nothing identical or near-identical was found: no open, documented, recurring AIS- or SAR-based measure of cargo crossing the Caspian leg, in English, Russian, Turkish or Azerbaijani sources searched.
2. The closest items are (i) IMF PortWatch itself (raw daily port calls/tonnage, no Caspian-specific validation), (ii) EPINOVA policy briefs (2026) on "Caspian port rhythm", Russia–Iran framed, data source not named, and (iii) Lloyd's List / Windward / Texty one-off AIS or SAR pieces on Russia–Iran traffic.
3. None of the institutional Middle Corridor reports (World Bank 2023, OECD 2023 and 2025, EBRD 2023, ADB/CAREC 2022–2024) uses AIS or satellite data; all rely on operator/association statistics, port statistics, stakeholder surveys and models.
4. The contribution is therefore real but narrow: a validated, documented, monthly re-aggregation of PortWatch for four ports, reconciled against official ferry/port statistics, plus an honest account of where AIS fails (the 2022 Ro-Ro step, ferries classed as passenger ships, Kuryk missing).
5. Google Scholar could not be searched (bot-verification page; not bypassed), eLIBRARY needs a login, and the CyberLeninka API returned zero for every query, so the Russian-language check rests on general web search and is weaker than the English one.

---

## 1. Novelty check — queries and results

Search engines used: WebSearch (general web), OpenAlex API, arXiv API, Crossref API, plus `site:` searches for cyberleninka.ru, ssrn.com, researchgate.net and dergipark.

| # | Query (tool) | Returned | Relevant hit? |
|---|---|---|---|
| 1 | `"Middle Corridor" AIS vessel data port calls analysis` (web) | Generic AIS port-call method papers (IMF WP 2020/057, 2019/275, a 2025 Frontiers paper on open-AIS port traffic), Kpler marketing | No Caspian work (snippet) |
| 2 | `"Trans-Caspian" AIS shipping satellite` (web) | Satellite-AIS explainers (ESA, Spire, DLR) | None (snippet) |
| 3 | `Caspian Sea "port calls" AIS study` (web) | Lloyd's List Intelligence blog on Caspian AIS gaps; Foreign Policy 2023 piece (republished by Turan/Caliber); vessel pages | Russia–Iran dark-port-call analysis, not a cargo measure (snippet) |
| 4 | `Caspian Sea Sentinel-1 ship detection SAR` (web) | General S-1 ship-detection reviews, LS-SSDD dataset, one 2015 ISPRS paper on Iranian-coast S-1 | None for Caspian shipping (snippet) |
| 5 | `"Средний коридор" АИС судоходство анализ` (web) | World Bank 2023 exec. summary (RU), Lloyd's List on Kerch/Azov AIS gaps | None (snippet) |
| 6 | `Транскаспийский маршрут судоходство спутниковые данные АИС Каспий` (web) | Lloyd's List Russia–Iran pieces, Windward (Volga–Don cargo ships 35 → 50, 2021→2022), JCFA | None for the Middle Corridor (snippet) |
| 7 | `"Orta Koridor" AIS gemi verisi Hazar` (web) | VesselFinder/Maritime Optima vessel pages, a GetTransport logistics blog | None (snippet) |
| 8 | `Hazar Denizi gemi trafiği AIS analizi` (web) | Caspian Policy Center "Dark deals on the Caspian" (AIS gaps of Russian/Iranian ships, May 2023), Maritime Executive, NTV | Russia–Iran only (snippet) |
| 9 | `cyberleninka Каспийское море АИС суда мониторинг порт` (web) and `site:cyberleninka.ru …` ×2 (web) | No cyberleninka.ru pages returned; LETI radar-monitoring news (2021), LOT Group Caspian surveillance deck, Russian S-AIS papers (spacedevice.ru) | None (snippet) |
| 10 | CyberLeninka API, 6 Russian queries (e.g. "Транскаспийский международный транспортный маршрут", "АИС Каспий") | `found: 0` for every query, including generic ones — API probably not working for outside clients | **Not effectively searched** |
| 11 | `Orta Dəhliz AIS gəmi Xəzər peyk monitorinq` (web) | English Caspian AIS-gap pieces; Texty S-1 project | No Azerbaijani-language source (snippet) |
| 12 | `dergipark "Orta Koridor" Hazar … AIS uydu` (web) | DergiPark corridor-strategy papers, Turkish ministry bulletin | None using AIS/satellite (snippet) |
| 13 | `Middle Corridor nowcast OR tracker OR index satellite … ferry` (web) | IMF WP 2025/093, Caspian Policy Center guides, water-level pieces | None (snippet) |
| 14 | `PortWatch Caspian Aktau Baku port calls analysis Middle Corridor` (web) | Port news only | No study using PortWatch for the Caspian (snippet) |
| 15 | OpenAlex `"Middle Corridor" AIS` | 12 works | **Black Sea–Middle Corridor Integration Index (BSMCII)**, Zenodo 2026 — opened, see below |
| 16 | OpenAlex `Caspian AIS vessel` | 371 works (first 25 read) | EPINOVA PB-44, PB-47, PB-50 (2026) — PB-44 opened, see below; rest oil-spill/ecology |
| 17 | OpenAlex `Trans-Caspian satellite shipping` | 439 (first 25) | OECD 2025 TCTC report; EarthArXiv 2025 "Adapting Caspian Sea ports to climate-induced water level declines: Aktau" (abstract only); no AIS work |
| 18 | OpenAlex `Caspian "port calls"` | 86 (first 25) | EPINOVA PB-63, PB-67 (Hormuz/logistics framing); nothing AIS-based on the Middle Corridor |
| 19 | OpenAlex `Caspian Sentinel-1 ship detection` | 330 (first 25) | All oil-spill / platform detection; none on ships in Caspian ports |
| 20 | arXiv API: `"Middle Corridor"`, `"Trans-Caspian"`, `PortWatch` | 0, 0, 0 | — |
| 21 | arXiv API: `Caspian AND port`; `Caspian AND (ship OR AIS OR vessel)`; `"port calls" AND AIS` | 2 (wave energy); 1 (hovercraft noise); 1 (liner network) | None |
| 22 | `site:ssrn.com "Middle Corridor" OR "Trans-Caspian" shipping` (web) | No SSRN pages; Carnegie 2026, HCSS/Clingendael 2026, ORF | None (snippet) |
| 23 | `site:researchgate.net Caspian Sea AIS ship traffic analysis` (web) | Only a general AIS-conservation review on RG; Lloyd's List | None (snippet) |
| 24 | Google Scholar (`"Middle Corridor" AIS port calls`) | Returned a bot-verification page | **Not searched** (not bypassed) |
| 25 | RePEc/IDEAS htsearch (`Caspian AIS`) | Page returned with no parseable results | **Not effectively searched**; EconPapers/IDEAS listings seen only for the IMF WPs |
| 26 | eLIBRARY | Requires login | **Not searched** |
| 27 | CORE | Not queried directly (API key needed); CORE PDFs appeared in web results only | Partial |

### Closest works found (new relative to Step 1)

- **Gondauri, D. and Guramishvili, G. (2026), "Black Sea–Middle Corridor Integration Index (BSMCII)"**, Zenodo, doi:10.5281/zenodo.21282793 (v1, 9 Jul 2026), CC BY 4.0 — **opened** (record page). A composite "readiness" index of eleven component indices over 19 port/route-year observations, 2020–2025. States that AIS, forwarder, customs and emissions data "are not yet publicly available" and are not used. Annual, not a flow measure. Cite as a contrast: it measures readiness from official/proxy indicators, not cargo from AIS.
- **Wu, S. (2026), EPINOVA Policy Brief PB-44, "Caspian Logistics Shock: … Visible Vessel Contraction, Port-Rhythm Inversion …"**, doi:10.67037/epinova.pb.2026.044 (29 Apr 2026) — **opened**. Vessel counts are "author-compiled indicators of visible Russian vessel composition"; no AIS provider, satellite source, ports list or frequency given; observation window 8–29 Apr 2026; a GitHub repo is linked but not stated to hold the data. Sister briefs PB-47 (Step 1) and PB-50 ("Caspian Shipping Rhythm", doi:10.67037/epinova.pb.2026.050) — PB-50 **abstract only**.
- **Lloyd's List Intelligence / Foreign Policy (2023)**: on a sampled day, Azerbaijani, Kazakh and Turkmen ships had "very few AIS gaps" compared with Russian and Iranian ships (snippet, via Turan/Caliber republication). Useful supporting evidence that the Middle Corridor fleet broadcasts AIS, but not verified at source.
- **Caspian Policy Center, "Dark deals on the Caspian"** (2023): 657 AIS gaps across 138 Russian-flagged ships in May 2023, concentrated near Amirabad, Anzali, Astrakhan, Volga (snippet).

---

## 2. Institutional reports — what data they used for Caspian crossing volumes

| Report | Opened? | Data for Caspian volumes | AIS or satellite? |
|---|---|---|---|
| **World Bank (2023), "Middle Trade and Transport Corridor: Policies and Investments to Triple Freight Volumes and Halve Travel Time by 2030"**, OKR handle 10986/40626 | **opened** (70-page PDF; copy from developmentaid.org mirror, matches WB © page; OKR itself returns 403) | Container dynamics "based on data from the Trans-Caspian International Transport Route Association" (Fig. 2); port figures from port authorities ("According to statistics provided by the Port of Baku", fn. 16; Maritime Transport Agency of Georgia); stakeholder survey of May 2023; trade forecasts from InfraForecast gravity model, national customs, UN Comtrade, BACI | **No** (zero occurrences of "AIS" or "satellite") |
| **OECD (2023), "Realising the Potential of the Middle Corridor"**, doi:10.1787/635ad854-en | **opened** (142-page PDF from oecd.org content store) | Policy consultation: survey + qualitative interviews in KZ, AZ, GE, TR (Box 1.2; Annex A); volumes quoted from ITF 2022, Middle Corridor Association 2022, EBRD 2023; trade from UN Comtrade, OEC | **No** |
| **OECD (2025), "Enhancing the Competitiveness of the Trans-Caspian Transport Corridor in Central Asia"**, doi:10.1787/f261e7fa-en (Nov 2025) — 2024–25 follow-up | **opened** (195-page PDF) | ~30 firms per country, government questionnaires, interviews (Annex A); TCTC 2024 "4.5 million tonnes" (+62%) from press (Portnews, Trans.ru, Infranews, EDB); QazStat; OEC | **No** (only "satellite" = navigation satellite system) |
| **EBRD (2023), "Sustainable transport connections between Europe and Central Asia"** (info valid 9 Jun 2023; CPCS Transcom) | **opened** (55-page PDF from transport.ec.europa.eu) | Kazakh Railways TITR figure (1.5 Mt in 2022); Eurasian Rail Alliance Index; "around 33,000 containers were carried between Aktau and Baku" in 2022, split by "stakeholder consultations"; CPCS demand/choice models | **No** |
| **ADB (May 2024), "Trade Flows and Transport Routes in the CAREC Region Amid External Shocks"** (SOM paper) | **opened** (27 pp.) | UN Comtrade, national statistics/customs, Kazakhstan State Revenue Committee; "Sources: Ports of Aktau and Turkmenbashi" (Fig. 11); Eurasian Rail Alliance Index | **No** |
| **CAREC CPMM Annual Report 2022** | **opened** | Sampled road and rail shipments from carriers/forwarders (time/cost–distance); Trans-Caspian case study: seaport border-crossing time 21.0 h vs 7.8 h on land, cost $236.80 vs $62.60; port times for Aktau, Kuryk, Baku from shipments sampled since 2018 | **No** (survey of shipments) |
| **CAREC CPMM Annual Report 2024** (released Jul 2026) | **opened** | Same CPMM mechanism; data "originate from the transport operators"; route figures from middlecorridor.com | **No** |
| **ADB Brief 244 (Mar 2023), "Economic Applicability of the AIS Data"**, doi:10.22617/BRF230082-2 | **opened** | Not Caspian; reviews AIS trade use cases (Singapore, Hong Kong, Busan, Port Klang) | Describes AIS: UNGP data "from December 2018 onward"; says draught-based trade estimates have "mixed results" and "may not be more accurate than using port call information" |
| **World Bank (Sep 2026), "Integration: World-Class Trade Logistics Along the Trans-Caspian Transport Corridor"** (ECA Economic Update) | **not opened** (landing page opened; OKR download blocked, 403/HTML) | Press coverage: 8.8 Mt (2023) → 32.1 Mt (2040); "According to data from the Middle Corridor Association" for 2021–25 growth (Trend, 1 Oct 2026, opened) | Unknown; the landing page names no data sources |
| **OSW (2024?) "The Middle Corridor"** report | **opened** (text scanned only for AIS/satellite) | — | **No** |
| **UNECE / UNCTAD** | **not found**: no standalone UNECE or UNCTAD Trans-Caspian volume study surfaced; UNCTAD RMT 2024 search returned nothing on the Caspian; UNECE work found only on digital data exchange among Baku, Aktau, Turkmenbashi (snippet) | — | — |

**Finding:** every institutional estimate of Caspian crossing volumes traces back to operator, association (TITR/Middle Corridor Association), railway (KTZ) or port-authority statistics, or to surveys and models. None uses AIS or satellite observation. This is the gap the Monitor fills, and it also means there is no independent benchmark the Monitor can be validated against beyond those same official figures.

Useful numbers from the opened reports for validation (all **opened**):
- World Bank 2023, p. 43: Alat 2022 throughput 6.3 Mt, "of which 2.5 Mt on railcars, 1.1 Mt in trucks-trailers and 2.7 Mt through the multi-purpose terminal"; ferry-terminal capacity 6.2 Mt, Ro-Ro terminal 1.8 Mt; round trip Baku–Aktau–Baku 5 days by ferry, 4.3 days by Ro-Pax.
- World Bank 2023, p. 43–44: ASCO owns "15 rail-ferries, 2 ro-ro ships, 2 modern ro-pax carrying also rail wagons"; ASCO carries containers on ferries.
- World Bank 2023, p. 42: Kuryk 2022 throughput 1.8 Mt, 79% general cargo in trucks and rail wagons on the Kuryk–Baku route.
- ADB 2024, ¶37: diversion of Kazakh oil to Caspian crossings "largely explained the freight turnover growth" at Aktau in 2022–2023 — relevant because PortWatch tanker tonnage will carry that, not Ro-Ro.

---

## 3. Method precedents

| Work | Tag | Relevant point | Stated limits |
|---|---|---|---|
| **Cerdeiro, Komaromi, Liu, Saeed (2020)**, "World Seaborne Trade in Real Time: A Proof of Concept for Building AIS-based Nowcasts from Scratch", IMF WP 20/57, doi:10.5089/9781513544106.001 | **opened** (imf.org markdown version) | MarineTraffic AIS 2015–Apr 2020, hourly down-sampled; port areas from weighted DBSCAN on slow/moored messages, convex hulls; random-forest port-call classifier trained on US entrance records (accuracy 91.3%); cargo = DWT × draught fraction between ballast and design draught. Ro-Ro evaluated in detection (false-negative rate 2.99%) | Draught "manually entered and prone to measurement error and lags"; linear draught–cargo assumption ("rectangular cuboid hull"); most false negatives are ships missing from the AIS data |
| **Arslanalp, Marini, Tumbarello (2019)**, "Big Data on Vessel Traffic: Nowcasting Trade Flows in Real Time", IMF WP 19/275, doi:10.5089/9781513521121.001 | **opened** | Malta 2015–18, MarineTraffic terrestrial network; port call = slow movement inside bounding box; drops stays <5 h or >60 h; cargo-number index correlates 0.75 with port statistics, cargo-load 0.65 with trade volume; AIS counts run 20–30% above official counts | Accuracy depends on receiver coverage near ports; manual draught; "fast ferries" can stay under 5 hours and are lost by the filter; "do not replace customs-based official trade statistics" |
| **Arslanalp, Koepke, Verschuur (2021)**, "Tracking Trade from Space: An Application to Pacific Island Countries", IMF WP 21/225, doi:10.5089/9781513593531.001 — **the PortWatch method paper** | **opened** | UN Global Platform AIS 2019–20; port polygons drawn from vessel movements and satellite imagery around WPI/Google-Maps port points (Box 2); drop calls <5 h with no draught change; cargo from length, width, draught, design draught, block coefficients and DWT following Jia et al. (2019); explains 89% of variation in official statistics | Value vs volume mismatch; drafts not updated → backpropagation/averages; hub-and-spoke transshipment. No discussion of Ro-Ro, ferries or AIS coverage changes over time |
| **Arslanalp, Choi, Kamali, Koepke, McKetty, Ruta, Saraiva, Sozzi, Verschuur (2025)**, "Nowcasting Global Trade from Space", IMF WP 25/093, doi:10.5089/9798229009294.001 | **opened** (markdown version; author list from Crossref) | Global monthly nowcast from PortWatch; groups vessels as tankers, dry bulk, and "containerships/other cargo" (container, general cargo, Ro-Ro); corr. 0.95 (value) with CPB | AIS "observe[s] only the net change in a vessel's draft" → two-way trade understated (netting fix for containers only); port coverage grew from 1,378 to 1,666 ports, so series are not fixed in scope; no separate Ro-Ro treatment |
| **Arslanalp, Exton, Gao, Saraiva, Kamali, Sozzi, Verschuur (2026)**, "Nowcasting Country-Level Trade Estimates Using IMF PortWatch", IMF WP 26/099, doi:10.5089/9798229046893.001 | **opened** (markdown version) | "Port review" added 64 ports and refined 18 boundaries; Ro-Ro folded into the container group; US port-call correlation 0.93 | Small economies fit poorly (Jamaica export value corr. 0.34, Samoa 0.06); passenger vessels not in the groupings (Japan's official calls include them); no mention of data breaks in 2021–22 |
| **Verschuur, Koks, Hall (2021)**, "Global economic impacts of COVID-19 lockdown measures stand out in high-frequency shipping data", PLoS ONE 16(4): e0248818, doi:10.1371/journal.pone.0248818 | **opened** | UNGP AIS (AIS Task Team), Jan 2019–Aug 2020, ~3.2 M port calls, 1,153 ports; port-level validation corr. 0.52–0.96 | "we include only the main trade-carrying vessels" (passenger vessels excluded); draught "less frequently reported in developing countries"; overestimates small ports |
| **Verschuur, Koks, Hall (2022)**, "Ports' criticality in international trade and global supply-chains", Nature Communications 13: 4351, doi:10.1038/s41467-022-32070-0 | **opened** (PDF; abstract checked) | Port-level trade flows for ~1,300 ports allocated on the maritime network; basis of PortWatch's port database | No Ro-Ro/ferry discussion found in text scan |
| **Jia, Prakash, Smith (2019)**, "Estimating vessel payloads in bulk shipping using AIS data", Int. J. Shipping and Transport Logistics 11(1): 25–40, doi:10.1504/IJSTL.2019.096864 | **abstract** (Inderscience page) | The payload formula PortWatch cites; validated for bulk carriers | Bulk carriers only — no evidence it holds for Ro-Ro/rail ferries |
| **Lechthaler, Stamer (2022)**, "The Kiel Trade Indicator – A real-time indicator for trade flows", SUERF Policy Brief 418 | **opened** | FleetMon container-ship positions, >500 ports, draught vs min/max → utilisation × capacity, ML aggregation, 75 countries | Container ships only; "should not be confused with an all-encompassing forecasting model of trade" |
| **Stamer (2024)**, "Thinking outside the container: A sparse partial least squares approach to forecasting trade flows", Int. J. Forecasting 40(4): 1336–1358, doi:10.1016/j.ijforecast.2023.11.007 | **abstract** (OpenAlex) | Method paper behind the Kiel indicator; beats benchmarks for most of 76 countries | Container vessels only (abstract) |
| **Paolo et al. (2024)**, "Satellite mapping reveals extensive industrial activity at sea", Nature 625: 85–91, doi:10.1038/s41586-023-06825-8 | **opened** (PDF; Step 1 checked study area) | S-1 + AIS + deep learning, 2017–2021; 21–30% of transport/energy vessel activity missing from public tracking | Caspian outside study area and nearshore 1 km excluded (Step 1) |
| **Paolo et al. (2022)**, "xView3-SAR: Detecting Dark Fishing Activity Using Synthetic Aperture Radar Imagery", NeurIPS 2022 Datasets & Benchmarks, arXiv:2206.00897 | **opened** (abs page) | ~1,000 analysis-ready S-1 scenes with vessel labels, bathymetry, wind | Objects "relatively small and sparse"; no stated near-port coverage |
| **Greidanus et al. (2017)**, "The SUMO Ship Detector Algorithm for Satellite Radar Images", Remote Sensing 9(3): 246, doi:10.3390/rs9030246 | **abstract** (OpenAlex; MDPI 403) | JRC SUMO is "a pixel-based CFAR … detector" assuming K-distributed clutter, with land masking, azimuth-ambiguity removal, reliability indicator — a usable, documented baseline detector | Performs well "within the physical limits imposed by the radar imaging"; near-harbour performance not stated in abstract |
| **Santamaria et al. (2017)**, "Mass Processing of Sentinel-1 Images for Maritime Surveillance", Remote Sensing 9(7): 678, doi:10.3390/rs9070678 | **abstract** (OpenAlex; MDPI 403) | >11,500 S-1A images over the Mediterranean (Oct 2014–Sep 2016) processed with SUMO and matched to AIS — the closest precedent for S-1/AIS cross-checking | Not read beyond abstract |
| **Crisp (2004)**, "The State-of-the-Art in Ship Detection in Synthetic Aperture Radar Imagery", DSTO-RR-0272 (DTIC ADA426096) | **snippet** (DTIC PDF 403) | Standard CFAR/ship-detection review | Not opened — cite only after reading |
| **UN AIS Handbook** (UN-CEBD AIS Task Team, "released in February 2020") | **not opened** — wiki URL `unstats.un.org/wiki/display/AIS/AIS+Handbook+Outline` returns 404; Task Team page **opened** | — | — |
| **Draught for Ro-Ro / ferries** | **snippet** only: a 1989 paper on ro-ro ferry draught gauges reports rolling of minutes' period and crests > ±500 mm; a Scandinavian-ferry payload study (Inderscience) was found but the opened page was the bulk-carrier paper above | No peer-reviewed work found that validates AIS-draught cargo estimates for Ro-Ro or rail ferries. The IMF papers never discuss it | — |
| **AIS coverage in enclosed seas** | **snippet** only: Lapinski & Isenor (J. Navigation) estimate terrestrial reception coverage from messages (Norwegian/North/Baltic Seas); S-AIS message collisions in dense areas | Nothing Caspian-specific found | — |

**What a paper must take from this:** PortWatch's tonnage method is validated for bulk/container trade at large ports; there is no published validation for Ro-Ro or rail ferries, whose draught barely changes with a deck of wagons and trucks, and whose short port stays fall foul of the 5-hour filter (Arslanalp et al. 2019 note this for "fast ferries"). Port-call counts, not tonnage, are the defensible Ro-Ro signal — consistent with ADB Brief 244's finding that draught-based estimates "may not be more accurate than using port call information".

---

## 4. PortWatch port areas, call assignment, and the 2022 Ro-Ro step

### How PortWatch defines ports and calls (documentation)

- **Daily_Ports_Data item description** (ArcGIS item 83b1bbc7b3354c5fb1f40673bb8f852e, read via ArcGIS REST, **opened**): "a port call is defined when a ship enters the port boundary"; calls with "turnaround time of less than 5 hours and no draft change" are excluded; five categories "container, dry bulk, general cargo, ro-ro and tanker"; cites Arslanalp, Koepke, Verschuur (2021) as the method source.
- Same description, **key for task 4**: "AIS data at the UNGP are provided by Spire, which collects AIS messages from two different satellite constellations, with more than 65 AIS equipped satellites. Spire complements this information with data collected by FleetMon through terrestrial receivers." Archive "from December 1, 2018". Vessel capacity and maximum draught come from "ship registry databases from FleetMon and IHS Markit". It also says terrestrial receivers "typically cover only about 15–20 nautical miles from the coast" and are "useful for congested ports".
- **Port polygons**: Arslanalp et al. (2021, Box 2) build boundaries from vessel movements and satellite imagery around a central point (WPI/Google Maps) (**opened**). The 2026 WP describes a "port review" that refines boundaries (**opened**). Polygons are **not published**: I listed PortWatch's ArcGIS items; the layer `PortWatch_boundaries` (a9598ad5276a40f7b44f4b5cdd6cc1f0) has fields ISO3/formalname/country — these are **country** boundaries, not port polygons (**opened**). So Step 1's "boundary unverified" stands.
- **Ship-type mapping**: no document says which registry ship types map to "ro-ro". The 2025/2026 WPs fold Ro-Ro into a container group and do not list passenger types (**opened**). Verschuur et al. (2021) exclude passenger vessels (**opened**).

### AIS-coverage change around 2021–2022 (evidence, not proof)

- Spire agreed to buy exactEarth in Sep 2021 (Satellite Today, 14 Sep 2021, **snippet**) and had completed it by 2 Dec 2021 (Satellite Today, 2 Dec 2021, **opened**: Spire would "integrate exactEarth's historical database"; no integration timeline). The PortWatch item now says UNGP data come from Spire's "two different satellite constellations" — consistent with exactEarth's constellation being added to the UNGP feed after the 2021 acquisition. **The date it entered the UNGP feed is not documented anywhere I found.**
- Kpler later absorbed Spire Maritime (deal announced Nov 2024, close expected Q1 2025) and MarineTraffic/FleetMon (2023) (**snippet**). Global Fishing Watch documented that its own switch of AIS vendor (to Kpler, 22 Apr 2026) caused a global drop in data volume and warns against comparing before/after (GFW platform update, **opened**) — a documented precedent that vendor changes create artificial steps in AIS-derived series.
- **No IMF document mentions a break in 2021–2022.** The 2025 WP mentions port-coverage expansion (1,378 → 1,666 ports), not message-coverage changes.

### Independent evidence on 2021 vs 2022 ferry traffic

| Indicator | 2021 | 2022 | Change | Source / tag |
|---|---|---|---|---|
| Baku port, wagons through the ferry terminal | 30,426 (−18.7% y/y): 20,867 Baku–Turkmenbashi, 9,559 Baku–Kuryk/Aktau | Jan–Nov: 36,187 (+31.7% vs Jan–Nov 2021) | about +30% | APA 9 Feb 2022 (**opened**); Sea-News.az 10 Feb 2022 (**opened**); Trend 14 Dec 2022 (**opened**) |
| Baku port, TIR trucks | 39,431 (Sea-News) / 39,341 (APA) (−8.8% y/y): 59.5% Turkmenbashi, 40.5% Kuryk | Jan–Nov: over 46,700 (+32.2%) | about +30% | same |
| Baku port, wagons H1 | 14,603 | 18,376 (+25.8%) | +26% | Ports Europe (**snippet**) |
| Alat 2022 by mode | — | 2.5 Mt on railcars, 1.1 Mt trucks-trailers | — | World Bank 2023 (**opened**) |
| Aktau + Kuryk, Jan–Sep | — | ~1.4 Mt, 2.4× Jan–Sep 2021 | ×2.4 | bizmedia/Russian-language source (**snippet**) |
| ASCO all cargo, Jan–Sep | — | 2.3 Mt, +21% y/y (bulk carriers −22.4%) | +21% | Ports Europe (**snippet**) |
| Baku port total | 5.6 Mt | 6.314 Mt (+13.6%) | +14% | Step 1; search snippet |
| For reference: 2019 | 44,175 wagons; 33,671 wheeled vehicles | — | — | Step 1 (PortNews) |
| For reference: 2023 | — | 37,300 wagons; 54,200 trucks | — | Step 1 (Report.az) |

**Reading:** the Baku ferry terminal's physical traffic rose by roughly 30% in 2022, and 2019 wagon traffic (44,175) was *higher* than 2022 (≈39,000 annualised) — yet PortWatch Ro-Ro calls at Baku are 126 in 2019 and 496 in 2022. Real traffic did grow (Kazakh-side tonnage more than doubled), but nothing in the official ferry statistics supports a fourfold rise in ferry calls at Baku, and no Ro-Ro-registered ship joined the fleet in 2021–22 (the two new ships are Passenger/Ro-Ro, see FERRY_FLEET.md). **The step is most likely a data artefact** (AIS feed/coverage change, classification change, or port-boundary change), with the exactEarth integration into the UNGP Spire feed as the leading but **unverified** candidate. Treat 2019–2021 Ro-Ro counts as not comparable with 2022+ until resolved.

---

## 5. Ferry fleet

See `FERRY_FLEET.md`.

---

## 6. Publishing practicalities

### arXiv categories (category_taxonomy page, **opened**)

| Category | Official description (short) | Fit |
|---|---|---|
| stat.AP | Applications (biology, education, epidemiology, engineering, environmental sciences, medical, physical sciences …) | Good: applied measurement and validation of a statistical indicator |
| econ.GN | "General methodological, applied, and empirical contributions to economics." | Good: trade/transport measurement for economists |
| econ.EM | Econometric theory, micro-/macro-econometrics … | Only if the paper has real nowcasting/econometric content |
| cs.CV | "image processing, computer vision, pattern recognition, and scene understanding" | Cross-list only if S-1 detection is a substantive part |
| eess.IV | Theory, algorithms and architectures for formation, capture, processing, analysis of images | Alternative cross-list for SAR processing |
| physics.soc-ph | "Structure, dynamics and collective behavior of societies and groups" | Weak fit |

**Recommendation:** primary **econ.GN** (the readership that uses PortWatch/trade nowcasts), cross-list **stat.AP**; add **eess.IV** (or cs.CV) only if the Sentinel-1 check has a real detection method and validation, not just counts. physics.soc-ph does not fit.

### arXiv on AI-assisted writing (**opened**: moderation page and blog of 31 Jan 2023)
- Authors must report "any significant use of sophisticated tools", including text-to-text generative AI; AI tools "should not be listed as an author"; each author takes "full responsibility for all its contents, irrespective of how the contents were generated".
- A May 2026 arXiv-wide one-year submission ban for "incontrovertible evidence" of unchecked AI content (hallucinated references, leftover chatbot text) is reported by CASRAI (24 Jul 2026) from statements by the CS section chair — **secondary source only**; not on arXiv's moderation page I opened. Treat as likely and check every reference by hand.
- Endorsement: see Step 1 (g). Moderation may decline submissions without "original or substantive research".

### SSRN (Elsevier support pages)
- **Who may submit / cost:** posted "by authors and their affiliates"; authors submit directly; posting is free ("free author posting") — "How do papers get on SSRN?", updated 13 Aug 2026 (**opened**). A free SSRN account is required; submitter is assumed to have co-authors' consent (**snippet**). No affiliation or student restriction stated on the page I opened (**opened**); no SSRN student-specific rule found. → Students may post, as far as the official pages show.
- **Review:** "subject to passing our research integrity checks. Rejection decisions are final" (**snippet**); third-party guides say 1–3 days, administrative not peer review (**snippet**).
- **Rights:** author keeps copyright; SSRN gets "the non-exclusive right to post and distribute"; author may remove the paper "at any time" — copyright policy, updated 3 Aug 2026 (**opened**).
- **Generative AI:** may be used to support preparation (grammar, language, translation, literature discovery) with human oversight; material use must be disclosed (basic grammar/spell checks need not be); AI "must not be listed or cited as authors"; authors "fully responsible" — updated 3 Aug 2026 (**opened**).
- **Network:** official classification page returned 404; the Economics Research Network (ERN) is the natural home — **not verified** on an official page.

### Both SSRN and arXiv?
Neither service forbids it on the pages I opened. SSRN takes only a non-exclusive licence; arXiv requires the submitter to "certify that they have the right to grant that license" (licence page, **opened**), which a non-exclusive SSRN grant does not prevent. arXiv's "Duplicated content" rule concerns duplicates within arXiv. **Conclusion:** dual posting is allowed; post on arXiv first (needs endorsement), then SSRN with the arXiv identifier, and keep versions in step. Check any target journal's preprint policy before either.

### Recommendation
SSRN (ERN) is the low-friction route — free, no endorsement, quick screening. arXiv econ.GN + stat.AP gives better visibility among data-science readers but needs a personal endorser (Step 1 g). Do both if an endorser is found; otherwise SSRN alone. In both, add a short AI-use disclosure statement.
