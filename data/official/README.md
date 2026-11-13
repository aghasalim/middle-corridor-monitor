# Official figures — Caspian leg of the Middle Corridor

`official_figures.csv` holds one row per published number (517 rows, collected 13 Nov 2026). The columns are
`entity, period_start, period_end, metric, value, unit, definition, source_url, source_date, status, note`.

- Periods are inclusive ISO dates. Values are plain numbers in tonnes, TEU or a count. Thousand-tonne figures are
  multiplied out, and the decimals the source printed are kept.
- `status` is one of:
  - `opened`: the page, PDF or official table was opened and the number is visible there.
  - `step1`: carried over from `research/STEP1_RESEARCH.md` section e without being re-opened.
  - `snippet`: seen only in a search result.
- Words such as "over", "about" and "nearly" are kept in `note`. Ranges are recorded at their lower bound, with a note.
- Containers and TEU are never converted into each other. "ДФЭ" (DFE) is Russian for TEU.
- `source_date` is the publication date where it is known. Otherwise it is the month (`YYYY-MM`) of the PDF upload
  folder or table release. For the stat.gov.kz monthly table it is the download date.
- `sources/` holds small text or CSV extracts of the PDFs and tables that most rows come from, plus `build_official.py`,
  which regenerates the CSV. The builder reads the downloaded files from a scratch folder outside the repo.

Rows by entity: Aktau 89, KZ seaports 78, Port of Baku 57, Kazakhstan sea transport 55, Azerbaijan sea transport 51,
Kuryk 50, Aktau North Terminal (AMCT) 48, Azerbaijan corridors 28, ASCO 21, TITR 20, Azerbaijan seaports 10,
Turkmenbashi 4, Turkmen Marine Merchant Fleet 3, Kazmortransflot 2, Azerbaijan transit 1.

## Who publishes what, and how often

| Entity | Publisher | What | Frequency |
|---|---|---|---|
| Aktau | JSC NC "Aktau International Sea Trade Port" (AMTP) annual reports on portaktau.kz | Total, oil, grain, metal, other cargo, TEU (all directions and TITR route), 2018–2024. Reports exist for 2020–2024; 2025 not yet published (the 2024 report appeared April 2026) | Annual, about 16 months after year end |
| Aktau, Kuryk, AMCT, KZ seaports | Maritime Administration of Ports (Ministry of Transport), republished as a stat.gov.kz dynamic table ("Информация о деятельности морских портов", element 472909) | Cargo handled per port 2015–2025; export, import and transit; bulk, general, ferry and liquid cargo; vessel calls and ferry calls per port | Annual, published in May |
| Kazakhstan sea transport | Bureau of National Statistics, stat.gov.kz (form 1-transport; table element 445258, sheet "Морской") | Cargo **carried** by Kazakh-reporting sea carriers, **single-month** values since 2007. Most months of 2019–2022 are suppressed as confidential ("x") | **Monthly**, about 2 weeks after month end |
| Kuryk | Port management (KTZ press, rail-news.kz), lada.kz, Trend, Sputnik | Year totals split into rail, road and grain; occasional monthly figures (Jan–May 2026), ferries, wagons and trucks | Irregular |
| Port of Baku | Port press releases (via Azerbaijan Railways since the Feb 2025 merger), re-reported by Report, Trend, APA, news.az, Caliber | Cumulative releases (Q1, H1, 8, 9, 10, 11 months, year): tonnes, TEU, dry cargo, sometimes wagons and wheeled vehicles | About quarterly or monthly, cumulative, irregular |
| Azerbaijan sea transport | State Statistical Committee (SSC), stat.gov.az table 16 | Cargo **carried** by Azerbaijani sea transport: total, international, import, export, transit, cross-trade, cabotage | Annual table, plus a cumulative monthly figure in the SSC monthly report (re-reported by APA) |
| Azerbaijan seaports | SSC monthly report (re-reported by APA and Interfax) | Cargo **loaded and unloaded in all seaports**, its transit share, and cargo remaining in ports | **Monthly, cumulative** year-to-date |
| Azerbaijan corridors | SSC table 14 and quarterly releases | Cargo on the East-West, Europe-Caucasus-Asia, North-South and other corridors by mode, with the sea and sea-transit share | Annual; quarterly releases |
| ASCO | Company releases via APA, Report, Interfax | Fleet totals; tanker, dry-cargo and ferry figures (units, vehicles, wagons, weight of vehicles), TEU | Irregular, often monthly |
| TITR | TITR Association (middlecorridor.com), Kazakh Ministry of Transport, KTZ | Route tonnes and TEU, on bases that differ (see below) | Annual, irregular |
| Turkmenbashi | State media ("Turkmenistan" newspaper), World Bank via Trend | 2025 total, export, import, transit; fleet figures | Annual at best |

### Is there a regular monthly series?

Yes, but none of them measures the four ports directly.

1. **stat.gov.kz, "cargo carried by sea transport"** (Kazakhstan sea transport, `tonnes_carried`). This is monthly and
   non-cumulative, and the CSV has it from 2019 to Oct 2026: 55 months, the rest confidential. It counts cargo carried by
   Kazakh-reporting carriers, not cargo handled in ports. Jan–May 2026 sums to 1,751.6 kt, which matches the monthly
   release text.
2. **SSC Azerbaijan, "loading and unloading in seaports"** and **"cargo carried by sea"**. These are cumulative monthly
   figures in the SSC monthly report. Only Jan–Nov 2025, full-year 2025 and Jan–May 2026 were opened. Jan–May 2025,
   Jan–Jul 2025 and Jan–Jul 2026 are snippets. The full 2019–2026 run was **not** collected (see gaps).

The Kazakh Maritime Administration port table is annual only. Port of Baku cumulative releases come out often but on no
fixed schedule.

## The definitions problem

- **Handled vs carried.**
  - Handled: port tonnage counts cargo loaded plus unloaded at the quay. The KZ Maritime Administration figures, the AMTP
    reports, Port of Baku releases and the SSC "loading and unloading in seaports" figures are all of this kind.
  - Carried: "sea transport" statistics count cargo moved by a country's own carriers, wherever it is loaded. SSC sea
    transport (9,089.6 kt in 2025) equals ASCO's fleet total ("over 9.09 Mt"). stat.gov.kz sea transport means Kazakh
    carriers.
  - The two measures can differ by a factor of two. Azerbaijan in 2025: 12.96 Mt handled in seaports, 9.09 Mt carried.
- **Port company vs port area.**
  - "Aktau" in the AMTP reports and in the Maritime Administration table means the AMTP company only. The Aktau Marine
    North Terminal (AMCT, a separate grain, dry-cargo and container terminal) and Bautino are listed apart.
  - "Port of Baku" means the Baku International Sea Trade Port at Alat (the same port, sometimes called "Port of Alat").
    Azerbaijan's "seaports" total also includes other terminals.
- **Total vs transit vs route.**
  - Port of Baku: about 70% of its tonnage is transit.
  - AZ seaports: 79% transit in 2025. KZ seaports: transit was only 0.1–5.5% of handled cargo in 2023–2025, because export
    oil and grain dominate.
  - AZ corridors: 93% of sea transport through the corridors is transit.
  - TITR "route" figures cover a route, not a port. They have no stated border or mode.
- **TEU vs containers vs units.**
  - Aktau reports give TEU, split into all directions and the TITR route. Trend's Jan–Jul 2023 Aktau figure is
    "containers", and Turkmen fleet figures are containers.
  - ASCO "ferry units" lump wagons, trucks and vehicles together. Separate H1 2025 counts exist (wagons 18,227, trucks
    19,280).
  - Vehicle counts and "weight of vehicles" (tonnes) are different metrics.
- **The TITR figures for 2025 sit on three bases:**
  - 1.867 Mt (bm.ge snippet; "1.9 Mt" on a traceca.ge article): said to be "slightly above 2024".
  - 3.3 Mt in 2024 "via the seaports of Kazakhstan and Azerbaijan" (TITR Association's own release, 4 Mar 2025).
  - 4.119 Mt in 2025 and 4.484 Mt in 2024 (Kazakh Ministry of Transport). The Vice Minister said 4.5–4.7 Mt.

  The Association's TEU are consistent across years: 76,900 TEU in 2025 is 36% above its 56,500 TEU for 2024.
  The tonnes are not. A 2024 comparator "slightly below 1.867 Mt" cannot be the same series as the 3.3 Mt the
  Association itself published for 2024. So the 1.867 Mt figure counts something narrower than "cargo via KZ and AZ
  seaports". It is probably the cargo carried under the Association's coordinated route or tariffs, but this is
  **unverified**: no opened page defines it.

  The ministry and the Association matched in 2023. 3.3 Mt at +20% implies about 2.75 Mt for 2023, close to the
  ministry's 2.764 Mt. They diverged in 2024 (3.3 vs 4.484).

  For scale, all Kazakh-port ferry cargo was 1.72 Mt in 2025 and Aktau's TITR-route containers were 54,923 TEU in 2024.
  Neither number explains 4.119 Mt alone.

## Pairs that contradict each other

| Item | Figure A | Figure B |
|---|---|---|
| KZ seaports 2025 | 7,453 kt (Maritime Administration) | 8 Mt (Interfax KZ, step1) |
| Kuryk 2025 | 1,719 kt (Maritime Administration) | 1,955.5 kt (port interview, rail-news.kz). Its parts (1,059.4 + 659.6 + 246.4) sum to 1,965.4 |
| Kuryk 2024 | 1,931.9 kt (Maritime Administration) | 1,957.8 kt (Sputnik, step1) |
| AMCT 2020 | 1,560.1 kt (Maritime Administration) | 667 kt (Aktau 2024 report). 667 equals the Administration's Kuryk 2020 figure (666.8), so one of the tables has the two terminals mixed up |
| TITR 2025 tonnes | 1.867 Mt / 1.9 Mt (Association basis) | 4.119 Mt / "about 4.12" (ministry); 4.5–4.7 Mt (Vice Minister) |
| TITR 2025 TEU | 76,900 / "about 77,000" | 42,000 (KTZ via Trend and railways.kz) |
| TITR 2024 tonnes | 3.3 Mt (Association, via seaports) | 4.484 Mt (ministry) |
| Port of Baku 2022 | 6.3 Mt (AzerNews, step1) | Jan–Nov 5.43 Mt, which would need about 0.9 Mt in December, double the monthly run-rate. A search summary also cites a later port statement of 7.3 Mt for 2022 (not opened) |
| Port of Baku trucks 2022 | over 9,300 wheeled vehicles Jan–Sep (PortNews, port Telegram) | over 46,700 TIR trucks Jan–Nov (Trend) |
| Port of Baku TEU 2020 | 40,345 (TRACECA) | 40,395 (APA) |
| Port of Baku TEU 2024 | 76,800 (Trend) | 76,775 (Reuters) |
| Aktau small revisions | 2020 total 3,111 kt, 2023 TEU 22,780, 2021 oil 2,191 kt (the year's own report) | 3,110 / 22,782 / 2,190 (2024 report's table) |
| Kuryk May 2025 | 267,000 t (Trend, step1) | 287,000 t (Moscow Times, search summary only) |
| Interfax AZ seaports | Text says "January–May 2025, 5.18 Mt" | Dated 29 Jun 2026; the -9.2% matches Jan–May 2025 = 5,704.4 kt. Recorded as Jan–May 2026 |
| APA AZ seaports 2025 | Printed "129,59.5 thousand tons" | Read as 12,959.5 kt (Interfax: 12.95 Mt) |

## Not found or not verified

- **The 1.867 Mt sentence on a page that opens.** bm.ge returns 403. web.archive.org cannot be fetched from here. The
  TITR Association site has no 2025-results news item in its list (its 24 Apr 2026 item mentions the 2025 report with no
  numbers), and Russian and Kazakh searches found nothing. The only opened carrier is a traceca.ge opinion article
  ("1.9 million tons", 76,900 TEU, no source given).
- **TITR Association's own annual numbers for 2019–2023.** Only 2024 was found (3.3 Mt, 56,500 TEU).
- **Aktau 2025** from the port company: the annual report is not published yet. The Maritime Administration's 4,909 kt
  is in the CSV.
- **Kuryk monthly figures** beyond Jan–May 2026 and May 2025. **Kuryk wagons and trucks per year** exist only for
  Jan–Aug 2023 and 2025 (trucks).
- **Kazakh ferry calls for 2025.** The Administration table leaves 2025 ferries blank. Kuryk's 734 calls in 2025 are
  mostly booked as "other" (569).
- **Port of Baku:** portofbaku.com returns 403 to automated requests, so its own statistics and news were not read. Not
  found: full-year 2022 TEU, wagons and trucks; full-year 2021 wagons and trucks; wagons and trucks for 2025 and 2026; a
  separate ferry-terminal tonnage. ady.az was not opened.
- **The full SSC monthly runs** (AZ seaports handled; AZ sea transport carried) for 2019–2026. Each month is in the
  SSC's monthly socio-economic report, re-reported by APA. www.stat.gov.az resets connections often, and the monthly
  release index was not reachable, so only 3 months were opened. Next step: collect the remaining months one per
  release, or fetch the SSC monthly report files.
- **stat.gov.kz monthly sea transport**: most months of 2019–2022 are confidential ("x") and cannot be filled.
- **Turkmenbashi:** only 2025 (7,316,326 t, from state media) was found. No official figures for 2019–2024, no TEU, no
  monthly data. The World Bank utilisation figures (19% in 2023, 43% in 2025 of 17 Mt) are percentages and were not
  converted into tonnes.
- **Kazmortransflot / KTZ ferries: wagons or trucks carried per year.** Only Kazmortransflot feeder TEU (59,400 in 2025)
  was found.
- **Step1 rows** (77) were not re-opened. That covers most Port of Baku rows for 2019–2025, the TITR ministry series, and
  several Aktau and Kuryk partials.
