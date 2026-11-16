# Builds data/official/official_figures.csv from hand-checked rows plus two official tables.
# Run: .venv/Scripts/python -I build_official.py <scratch_dir> <out_csv>
import csv, sys, calendar
import openpyxl, xlrd

SCR, OUT = sys.argv[1], sys.argv[2]
rows = []

def add(entity, ps, pe, metric, value, unit, definition, url, sdate, status, note=""):
    rows.append(dict(entity=entity, period_start=ps, period_end=pe, metric=metric, value=value,
                     unit=unit, definition=definition, source_url=url, source_date=sdate,
                     status=status, note=note))

def yr(y):
    return f"{y}-01-01", f"{y}-12-31"

def kt(v):  # thousand tonnes -> tonnes, keep the precision the source printed
    return round(float(v) * 1000, 3)

# ---------------- Aktau port company (JSC NC AMTP) annual reports ----------------
AK24 = "https://portaktau.kz/wp-content/uploads/2026/04/godovoj-otchet-ao-nk-ammtp-za-2024-god.pdf"
AK23 = "https://portaktau.kz/wp-content/uploads/2025/04/godovoj-otchet-ao-nk-amtp-za-2023-god-na-angl.pdf"
AK21 = "https://portaktau.kz/wp-content/uploads/2023/02/godovoj-otchet-ao-nk-amtp-za-2021-god.pdf"
AK20 = "https://portaktau.kz/wp-content/uploads/2026/04/godovoj-otchet-ao-nk-amtp-za-2020-god.pdf"
A = "Aktau"
# 2024 report, market table p.43 (2019-2024), thousand tonnes / TEU
t24 = {
    "tonnes_oil":   [2136, 2213, 2190, 2462, 3614, 3721],
    "tonnes_grain": [795, 457, 635, 447, 177, 208],
    "tonnes_metal": [47, 11, 29, 121, 148, 59],
    "tonnes_other": [536, 429, 647, 788, 544, 893],
    "teu":          [14324, 17969, 27624, 30708, 22782, 58563],
    "tonnes_total": [3514, 3110, 3501, 3818, 4483, 4881],
}
defs = {"tonnes_oil": "oil transshipped", "tonnes_grain": "grain transshipped",
        "tonnes_metal": "metal transshipped", "tonnes_other": "other cargo (incl. containers) transshipped",
        "teu": "containers transshipped, all directions", "tonnes_total": "total cargo transshipped by the port company (excl. AMCT terminal)"}
for m, vals in t24.items():
    for y, v in zip(range(2019, 2025), vals):
        note = "AMTP 2024 annual report (RU), p.43 table '№ Номенклатура 2019-2024'"
        if m == "tonnes_total" and y == 2020:
            note += "; 2020 and 2021 reports give 3,111 kt"
        if m == "teu" and y == 2023:
            note += "; 2023 and 2024 reports' production tables give 22,780 TEU"
        if m == "tonnes_oil" and y == 2021:
            note += "; 2021 and 2023 reports' tables give 2,191 kt"
        add(A, *yr(y), m, v if m == "teu" else kt(v), "TEU" if m == "teu" else "tonnes",
            defs[m], AK24, "2026-04", "opened", note)
# figures that only the production tables carry (or that differ)
add(A, *yr(2020), "tonnes_total", kt(3111), "tonnes", defs["tonnes_total"], AK20, "2026-04", "opened", "2020 report production table; 2024 report gives 3,110 kt")
add(A, *yr(2023), "teu", 22780, "TEU", defs["teu"], AK23, "2025-04", "opened", "2023 report (EN) production table p.37; 2024 report market table gives 22,782")
add(A, *yr(2021), "tonnes_oil", kt(2191), "tonnes", defs["tonnes_oil"], AK21, "2023-02", "opened", "2021 report production table; 2024 report market table gives 2,190 kt")
add(A, *yr(2018), "tonnes_total", kt(3554), "tonnes", defs["tonnes_total"], AK20, "2026-04", "opened", "2020 report production table")
add(A, *yr(2018), "tonnes_oil", kt(2089), "tonnes", defs["tonnes_oil"], AK20, "2026-04", "opened", "2020 report production table")
add(A, *yr(2018), "tonnes_grain", kt(823), "tonnes", defs["tonnes_grain"], AK20, "2026-04", "opened", "2020 report production table")
add(A, *yr(2018), "tonnes_other", kt(642), "tonnes", "other and general cargo", AK20, "2026-04", "opened", "2020 report production table")
add(A, *yr(2018), "teu", 2489, "TEU", defs["teu"], AK20, "2026-04", "opened", "2020 report production table")
for y, v, src, sd in [(2018, 536, AK20, "2026-04"), (2019, 8272, AK20, "2026-04"), (2020, 12491, AK21, "2023-02"),
                      (2021, 17741, AK21, "2023-02"), (2022, 27094, AK23, "2025-04"), (2023, 16387, AK23, "2025-04"),
                      (2024, 54923, AK24, "2026-04")]:
    add(A, *yr(y), "teu_titr", v, "TEU", "containers on the TITR (Middle Corridor) route, subset of teu", src, sd, "opened",
        "production table row 'маршрут ТМТМ' / 'MIDDLE CORRIDOR route'")
add(A, "2024-01-01", "2024-11-30", "teu_titr", 48983, "TEU", "containers on the TITR route, Jan-Nov", AK24, "2026-04", "opened", "strategy section; same period 2023: 15,060 TEU")
add(A, "2023-01-01", "2023-11-30", "teu_titr", 15060, "TEU", "containers on the TITR route, Jan-Nov", AK24, "2026-04", "opened", "comparison figure in 2024 report")
for mo, v, nm in [(5, 5165, "May"), (6, 5869, "June"), (8, 8251, "August")]:
    add(A, f"2024-{mo:02d}-01", f"2024-{mo:02d}-{calendar.monthrange(2024, mo)[1]}", "teu", v, "TEU",
        f"containers transshipped in {nm} 2024", AK24, "2026-04", "opened", "monthly record mentioned in the report's 2024 chronology; only these three months given")
add(A, *yr(2024), "container_trains", 333, "count", "container trains arriving at Aktau", AK24, "2026-04", "opened", "2023: 11 trains")
add("Port of Baku", *yr(2024), "tonnes_total", 7600000, "tonnes", "Baku port cargo turnover", AK24, "2026-04", "opened", "stated as 7.6 Mt in Aktau report's competitor overview")

# AMCT (Aktau Marine North Terminal), table in Aktau 2024 report p.44
B = "Aktau North Terminal (AMCT)"
amct = {"tonnes_grain": [793, 430, 623, 465, 210, 265], "tonnes_metal": [58, 0, 0, 0, 138, 18],
        "tonnes_other": [160, 237, 358, 386, 222, 235], "teu": [928, 4116, 3388, 7427, 9850, 9994],
        "tonnes_total": [1011, 667, 981, 851, 570, 518]}
for m, vals in amct.items():
    for y, v in zip(range(2019, 2025), vals):
        note = "AMTP 2024 report p.44 table placed under the AMCT heading (checked by text position); the extracted text puts the Kuryk paragraph next to it, but the table sits inside the AMCT section"
        if m == "tonnes_total" and y == 2020:
            note += "; Kazakh Maritime Administration gives AMCT 1,560.1 kt for 2020 (667 equals its Kuryk figure 666.8)"
        add(B, *yr(y), m, v if m == "teu" else kt(v), "TEU" if m == "teu" else "tonnes",
            "AMCT terminal " + defs.get(m, m).replace(" by the port company (excl. AMCT terminal)", ""), AK24, "2026-04", "opened", note)

# ---------------- Kazakh Maritime Administration via stat.gov.kz (annual, by port) ----------------
KZT = "https://stat.gov.kz/api/iblock/element/472909/file/ru/"
KZ_NOTE = "stat.gov.kz dynamic table 'Информация о деятельности морских портов' (data from the Maritime Administration of Ports, Ministry of Transport); published by 29.05.2026"
wb = openpyxl.load_workbook(f"{SCR}/kzstat/472909.xlsx", data_only=True)
ws = wb.worksheets[0]
years = None
port_rows = {"Перегружено грузов - всего": ("KZ seaports", "tonnes_total", "cargo handled (loaded+unloaded) in all Kazakh seaports"),
             "Актау": ("Aktau", "tonnes_total", "cargo handled at Aktau port (excl. AMCT and Bautino)"),
             "Курык": ("Kuryk", "tonnes_total", "cargo handled at Kuryk port"),
             "Актауский морской северный терминал": ("Aktau North Terminal (AMCT)", "tonnes_total", "cargo handled at AMCT"),
             "на экспорт": ("KZ seaports", "tonnes_export", "export cargo handled, all KZ seaports"),
             "импорт": ("KZ seaports", "tonnes_import", "import cargo handled, all KZ seaports"),
             "транзит": ("KZ seaports", "tonnes_transit", "transit cargo handled, all KZ seaports"),
             "насыпные": ("KZ seaports", "tonnes_bulk", "dry bulk handled, all KZ seaports"),
             "генеральные грузы": ("KZ seaports", "tonnes_general", "general cargo handled, all KZ seaports"),
             "паромные": ("KZ seaports", "tonnes_ferry", "ferry cargo handled, all KZ seaports"),
             "Наливные грузы": ("KZ seaports", "tonnes_oil", "liquid (oil) cargo handled, all KZ seaports")}
in_section2 = False
for row in ws.iter_rows(values_only=True):
    lab = str(row[0]).strip() if row[0] else ""
    if lab.startswith("2. Погрузочно"):
        in_section2 = True
    if in_section2 and row[0] is None and row[1] == 2015:
        years = list(row[1:12])
        continue
    if in_section2 and years and lab in port_rows:
        ent, met, d = port_rows[lab]
        for y, v in zip(years, row[1:12]):
            if y < 2017 or not isinstance(v, (int, float)):
                continue
            add(ent, *yr(y), met, kt(v), "tonnes", d, KZT, "2026-05", "opened", KZ_NOTE + " table 2")
    if lab.startswith("*Информация") and years:
        if in_section2:
            break
# vessel calls (sheet 3), columns: per year Aktau, Bautino, Kuryk, AMCT
ws3 = wb.worksheets[2]
r = [list(x) for x in ws3.iter_rows(values_only=True)]
yrow = next(x for x in r if x[1] == 2015)
prow = r[r.index(yrow) + 1]
ports = {"Актау": "Aktau", "Курык": "Kuryk", "Актауский морской северный терминал": "Aktau North Terminal (AMCT)"}
for x in r:
    lab = str(x[0]).strip() if x[0] else ""
    if lab in ("Всего", "паромы"):
        met = "vessel_calls" if lab == "Всего" else "ferry_calls"
        y = None
        for i in range(1, len(x)):
            if isinstance(yrow[i], (int, float)):
                y = int(yrow[i])
            p = prow[i] if i < len(prow) else None
            if y is None or y < 2017 or p not in ports or not isinstance(x[i], (int, float)):
                continue
            add(ports[p], *yr(y), met, x[i], "count",
                "all vessel calls" if met == "vessel_calls" else "ferry calls", KZT, "2026-05", "opened", KZ_NOTE + " table 4")

# ---------------- Kazakhstan sea transport, monthly (stat.gov.kz) ----------------
KZM = "https://stat.gov.kz/api/iblock/element/445258/file/ru/"
wb = openpyxl.load_workbook(f"{SCR}/kzstat/445258.xlsx", data_only=True)
for row in wb["Морской"].iter_rows(values_only=True):
    if isinstance(row[0], int) and row[0] >= 2019:
        for mo, v in enumerate(row[1:13], start=1):
            if isinstance(v, (int, float)):
                add("Kazakhstan sea transport", f"{row[0]}-{mo:02d}-01", f"{row[0]}-{mo:02d}-{calendar.monthrange(row[0], mo)[1]}",
                    "tonnes_carried", kt(v), "tonnes",
                    "cargo carried by sea transport (form 1-transport reporting carriers), single month",
                    KZM, "2026-11-13", "opened",
                    "stat.gov.kz dynamic table 'Перевезено грузов по всем видам транспорта по месяцам', sheet 'Морской'; months marked x (confidential) omitted; source_date = download date")
add("Kazakhstan sea transport", "2026-01-01", "2026-01-31", "tonnes_carried", 318100, "tonnes",
    "cargo carried by sea transport, January", "https://stat.gov.kz/ru/industries/business-statistics/stat-transport/publications/475509/",
    "2026-02", "opened", "monthly release 'Транспорт в Республике Казахстан (январь 2026г.)'; -10.3% y/y")

# ---------------- Azerbaijan, State Statistical Committee tables ----------------
AZS = "https://www.stat.gov.az/source/transport/en/016_1en.xls"
b = xlrd.open_workbook(f"{SCR}/azstat/016_1en.xls").sheet_by_index(0)
hdr = b.row_values(3)
azmap = {"Freight transportation, thousand tonnes": ("tonnes_carried", "cargo carried by Azerbaijani sea transport, all"),
         "international": ("tonnes_international", "international cargo carried by Azerbaijani sea transport"),
         "import": ("tonnes_import", "import cargo carried by sea"), "export": ("tonnes_export", "export cargo carried by sea"),
         "transit": ("tonnes_transit", "transit cargo carried by Azerbaijani sea transport"),
         "beetwen foreign ports": ("tonnes_cross_trade", "cargo carried between foreign ports"),
         "cabotage": ("tonnes_cabotage", "cabotage cargo")}
seen = set()
for i in range(b.nrows):
    rv = b.row_values(i)
    lab = str(rv[1]).strip()
    if lab in azmap and lab not in seen:
        seen.add(lab)
        met, d = azmap[lab]
        for y, v in zip(hdr, rv):
            if isinstance(y, float) and y >= 2019 and isinstance(v, float):
                add("Azerbaijan sea transport", *yr(int(y)), met, kt(v), "tonnes", d, AZS, "2026-09-15", "opened",
                    "stat.gov.az table 16 'Sea transport' (file saved 15 Sep 2026); 2025 preliminary")
AZC = "https://www.stat.gov.az/source/transport/en/014_1en.xls"
bk = xlrd.open_workbook(f"{SCR}/azstat/014_1en.xls")
s0 = bk.sheet_by_index(0)
h0 = s0.row_values(3)
sea_rows = [i for i in range(s0.nrows) if str(s0.row_values(i)[1]).strip() == "Sea"][:2]  # 1st: transported goods, 2nd: transit
for i, (met, d) in zip(sea_rows, [("tonnes_sea_eca", "sea cargo on the Europe-Caucasus-Asia corridor"),
                                  ("tonnes_sea_eca_transit", "sea transit cargo on the Europe-Caucasus-Asia corridor")]):
    rv = s0.row_values(i)
    for y, v in zip(h0, rv):
        if isinstance(y, float) and y >= 2019 and isinstance(v, float):
            add("Azerbaijan corridors", *yr(int(y)), met, kt(v), "tonnes", d, AZC, "2026-09-15", "opened", "stat.gov.az table 14, old series (ECA corridor, to 2022)")
s1 = bk.sheet_by_index(1)
want = {"East-West": [("tonnes_east_west", "all modes, East-West corridor"), ("tonnes_east_west_transit", "transit, all modes, East-West corridor")],
        "Europe Caucasus-Asia": [("tonnes_eca", "all modes, Europe-Caucasus-Asia corridor"), ("tonnes_eca_transit", "transit, all modes, ECA corridor")],
        "sea": [("tonnes_sea", "sea transport through all corridors"), ("tonnes_sea_transit", "sea transit through all corridors"),
                None, None]}
count = {}
for i in range(s1.nrows):
    rv = s1.row_values(i)
    lab = str(rv[1]).strip()
    if lab in want:
        k = count.get(lab, 0)
        count[lab] = k + 1
        if k < len(want[lab]) and want[lab][k]:
            met, d = want[lab][k]
            for y, v in zip([2023, 2024, 2025], rv[2:5]):
                add("Azerbaijan corridors", *yr(y), met, kt(v), "tonnes", d, AZC, "2026-09-15", "opened", "stat.gov.az table 14-cont (new corridor series)")
add("Azerbaijan corridors", "2026-01-01", "2026-03-31", "tonnes_sea", 1391800, "tonnes", "sea transport through all corridors, Q1",
    "https://stat.gov.az/special_version/news/index.php?id=6720", "2026-05-15", "opened", "89.4% transit")

# ---------------- hand rows: (entity, start, end, metric, value, unit, definition, url, date, status, note) ----------------
H = [
# Azerbaijan seaports and sea transport, SSC monthly report via APA / Interfax / Report
("Azerbaijan sea transport","2025-01-01","2025-11-30","tonnes_carried",8334400,"tonnes","cargo carried by sea, Jan-Nov","https://en.apa.az/energy-and-industry/more-than-46-of-cargo-transported-by-sea-in-azerbaijan-consists-of-oil-486275","2025-12-12","opened","APA citing SSC monthly report; 46.8% oil"),
("Azerbaijan sea transport","2025-01-01","2025-12-31","tonnes_carried",9089600,"tonnes","cargo carried by sea, year","https://en.apa.az/energy-and-industry/oil-accounted-for-47-of-cargo-transported-by-sea-in-azerbaijan-last-year-489302","2026-01-19","opened","APA citing SSC; 47.5% oil; matches stat.gov.az table 16"),
("Azerbaijan seaports","2025-01-01","2025-11-30","tonnes_total",11940300,"tonnes","loading and unloading operations in seaports","https://en.apa.az/energy-and-industry/more-than-46-of-cargo-transported-by-sea-in-azerbaijan-consists-of-oil-486275","2025-12-12","opened","APA citing SSC; 431.3 kt remaining in ports on 1 Dec 2025"),
("Azerbaijan seaports","2025-01-01","2025-11-30","tonnes_transit",9480800,"tonnes","transit cargo in seaport loading/unloading","https://en.apa.az/energy-and-industry/more-than-46-of-cargo-transported-by-sea-in-azerbaijan-consists-of-oil-486275","2025-12-12","opened","79.4% of total"),
("Azerbaijan seaports","2025-01-01","2025-12-31","tonnes_total",12959500,"tonnes","loading and unloading operations in seaports","https://en.apa.az/energy-and-industry/oil-accounted-for-47-of-cargo-transported-by-sea-in-azerbaijan-last-year-489302","2026-01-19","opened","printed as '129,59.5 thousand tons' (typo); read as 12,959.5 kt, consistent with Interfax 12.95 Mt and the 79.1% transit share"),
("Azerbaijan seaports","2025-01-01","2025-12-31","tonnes_transit",10246300,"tonnes","transit cargo in seaport loading/unloading","https://en.apa.az/energy-and-industry/oil-accounted-for-47-of-cargo-transported-by-sea-in-azerbaijan-last-year-489302","2026-01-19","opened","79.1% of total; 441.3 kt remaining 1 Jan 2026"),
("Azerbaijan seaports","2025-01-01","2025-12-31","tonnes_total",12950000,"tonnes","cargo handled by Azerbaijan's seaports","https://interfax.com/newsroom/top-stories/118247/","2026-06-29","opened","stated as 12.95 Mt, -7.8% vs 2024"),
("Azerbaijan seaports","2026-01-01","2026-05-31","tonnes_total",5180000,"tonnes","cargo handled by Azerbaijan's seaports","https://interfax.com/newsroom/top-stories/118247/","2026-06-29","opened","article text says 'January-May 2025' but is dated 29 Jun 2026 and cites stock on 1 June; -9.2% fits Jan-May 2025 = 5,704.4 kt (search snippet of APA) so read as 2026"),
("Azerbaijan seaports","2026-01-01","2026-05-31","tonnes_transit",4350000,"tonnes","international transit cargo in seaports","https://interfax.com/newsroom/top-stories/118247/","2026-06-29","opened","84% of total; same period caveat as total"),
("Azerbaijan seaports","2025-01-01","2025-05-31","tonnes_total",5704400,"tonnes","loading and unloading operations in seaports","","","snippet","search-result summary of an APA item; transit 4,663.5 kt (81.8%)"),
("Azerbaijan seaports","2025-01-01","2025-07-31","tonnes_total",6830500,"tonnes","loading and unloading operations in seaports","","","snippet","search-result summary; transit 5,553.3 kt (81.3%)"),
("Azerbaijan seaports","2026-01-01","2026-07-31","tonnes_total",7546600,"tonnes","loading and unloading operations in seaports","","","snippet","search-result summary of SSC-based reports; 119.8 kt remaining 1 Aug 2026"),
("Azerbaijan sea transport","2026-01-01","2026-07-31","tonnes_carried",5067400,"tonnes","cargo carried by sea","https://www.ankasam.org/azerbaijans-sea-freight-falls-6-1-to-5-07-million-tonnes/?lang=en","","snippet","headline opened (5.07 Mt, -6.1%), body not visible; 5,067.4 kt and 40.5% oil from search summary"),
("Azerbaijan sea transport","2026-01-01","2026-03-31","tonnes_carried",1927000,"tonnes","cargo carried by sea","","","snippet","search summary: -12.8%, transit 1.244 Mt"),
("Azerbaijan corridors","2025-01-01","2025-12-31","tonnes_east_west",16909800,"tonnes","all modes, East-West corridor","https://stat.gov.az/special_version/news/index.php?id=6620","2026-02-16","opened","release 16 Feb 2026; also in table 14"),
# Turkmenbashi
("Turkmenbashi","2025-01-01","2025-12-31","tonnes_total",7316326,"tonnes","total cargo turnover of Turkmenbashi International Seaport","https://centralasianlight.org/news/turkmenbashi-international-sea-port-reports-15.2-cargo-growth-in-2025-handling-over-7.3-million-tons","2026-02-25","opened","citing the 'Turkmenistan' state newspaper; +15.2% y/y"),
("Turkmenbashi","2025-01-01","2025-12-31","tonnes_export",4465956,"tonnes","export cargo","https://centralasianlight.org/news/turkmenbashi-international-sea-port-reports-15.2-cargo-growth-in-2025-handling-over-7.3-million-tons","2026-02-25","opened",""),
("Turkmenbashi","2025-01-01","2025-12-31","tonnes_import",1522793,"tonnes","import cargo","https://centralasianlight.org/news/turkmenbashi-international-sea-port-reports-15.2-cargo-growth-in-2025-handling-over-7.3-million-tons","2026-02-25","opened",""),
("Turkmenbashi","2025-01-01","2025-12-31","tonnes_transit",1327576,"tonnes","transit cargo","https://centralasianlight.org/news/turkmenbashi-international-sea-port-reports-15.2-cargo-growth-in-2025-handling-over-7.3-million-tons","2026-02-25","opened",""),
("Turkmen Marine Merchant Fleet","2025-01-01","2025-12-31","tonnes_carried",2454106,"tonnes","cargo carried by the state fleet (20 vessels)","https://centralasianlight.org/news/turkmenbashi-international-sea-port-reports-15.2-cargo-growth-in-2025-handling-over-7.3-million-tons","2026-02-25","opened","fleet, not port"),
("Turkmen Marine Merchant Fleet","2025-01-01","2025-12-31","vehicles",20267,"count","vehicles carried by the state fleet","https://centralasianlight.org/news/turkmenbashi-international-sea-port-reports-15.2-cargo-growth-in-2025-handling-over-7.3-million-tons","2026-02-25","opened",""),
("Turkmen Marine Merchant Fleet","2025-01-01","2025-12-31","containers",3207,"count","containers carried by the state fleet","https://centralasianlight.org/news/turkmenbashi-international-sea-port-reports-15.2-cargo-growth-in-2025-handling-over-7.3-million-tons","2026-02-25","opened","containers, not TEU"),
# ASCO
("ASCO","2025-01-01","2025-12-31","tonnes_carried",9090000,"tonnes","all cargo carried by ASCO fleet","https://www.interfax.com/newsroom/top-stories/115533/","2026-01-12","opened","stated as 'over 9.09 million tonnes'"),
("ASCO","2025-01-01","2025-12-31","tonnes_dry",1330000,"tonnes","cargo carried by dry-cargo vessels","https://www.interfax.com/newsroom/top-stories/115533/","2026-01-12","opened","+45%"),
("ASCO","2025-01-01","2025-12-31","tonnes_oil",4310000,"tonnes","cargo carried by tankers","https://www.interfax.com/newsroom/top-stories/115533/","2026-01-12","opened","stated as 'exceeded 4.31 million'"),
("ASCO","2024-01-01","2024-12-31","tonnes_oil",4220000,"tonnes","cargo carried by tankers","https://www.interfax.com/newsroom/top-stories/115533/","2026-01-12","opened","stated as 'more than 4.22 million'"),
("ASCO","2025-01-01","2025-12-31","ferry_units",77070,"count","wagons, trucks and vehicles carried by ferries (combined)","https://www.interfax.com/newsroom/top-stories/115533/","2026-01-12","opened","+0.4%; Report.az gives 77,071 (2024: 76,757)"),
("ASCO","2025-01-01","2025-12-31","teu",22030,"TEU","containers carried by ASCO vessels","https://www.interfax.com/newsroom/top-stories/115533/","2026-01-12","opened","up threefold"),
("ASCO","2025-01-01","2025-06-30","tonnes_carried",4600000,"tonnes","all cargo carried by ASCO fleet","https://report.az/en/infrastructure/asco-boosts-cargo-transportation-by-12","2025-07-14","opened","+12%"),
("ASCO","2025-01-01","2025-06-30","tonnes_oil",2200000,"tonnes","cargo carried by tankers","https://report.az/en/infrastructure/asco-boosts-cargo-transportation-by-12","2025-07-14","opened","+10%"),
("ASCO","2025-01-01","2025-06-30","trucks",19280,"count","trucks carried by ferries and Ro-Pax","https://report.az/en/infrastructure/asco-boosts-cargo-transportation-by-12","2025-07-14","opened","+3%"),
("ASCO","2025-01-01","2025-06-30","wagons",18227,"count","rail wagons carried by ferries and Ro-Pax","https://report.az/en/infrastructure/asco-boosts-cargo-transportation-by-12","2025-07-14","opened","-4%"),
("ASCO","2024-01-01","2024-06-30","wagons",19068,"count","rail wagons carried by ferries and Ro-Pax","https://report.az/en/infrastructure/asco-boosts-cargo-transportation-by-12","2025-07-14","opened","comparison figure"),
("ASCO","2025-01-01","2025-06-30","tonnes_dry",666000,"tonnes","cargo carried by 'this fleet' (context: dry-cargo fleet)","https://report.az/en/infrastructure/asco-boosts-cargo-transportation-by-12","2025-07-14","opened","fleet named only as 'this fleet'; H1 2024: 363,818 t"),
("ASCO","2026-01-01","2026-08-31","vehicles",28178,"count","motor vehicles carried by ferries","https://en.apa.az/infrastructure/azerbaijan-sees-13-increase-in-motor-vehicle-transportation-by-ferries-526810","2026-09-28","opened","Jan-Aug 2025: 25,641"),
("ASCO","2025-01-01","2025-08-31","vehicles",25641,"count","motor vehicles carried by ferries","https://en.apa.az/infrastructure/azerbaijan-sees-13-increase-in-motor-vehicle-transportation-by-ferries-526810","2026-09-28","opened","comparison figure"),
("ASCO","2026-01-01","2026-08-31","tonnes_ferry_vehicles",728536,"tonnes","weight of motor vehicles carried by ferries","https://en.apa.az/infrastructure/azerbaijan-sees-13-increase-in-motor-vehicle-transportation-by-ferries-526810","2026-09-28","opened","Jan-Aug 2025: 643,623 t; transit 678,760 t"),
("ASCO","2026-01-01","2026-09-30","vehicles",32380,"count","motor vehicles carried by ferries","https://en.apa.az/infrastructure/vehicle-transportation-by-ferries-in-azerbaijan-increases-by-12-532166","2026-10-26","opened","Jan-Sep 2025: 28,847"),
("ASCO","2025-01-01","2025-09-30","vehicles",28847,"count","motor vehicles carried by ferries","https://en.apa.az/infrastructure/vehicle-transportation-by-ferries-in-azerbaijan-increases-by-12-532166","2026-10-26","opened","comparison figure; a search summary gave 28,330 vehicles and 28,076 wagons for 9M 2025 (not opened)"),
("ASCO","2026-01-01","2026-09-30","tonnes_ferry_vehicles",837557,"tonnes","weight of motor vehicles carried by ferries","https://en.apa.az/infrastructure/vehicle-transportation-by-ferries-in-azerbaijan-increases-by-12-532166","2026-10-26","opened","Jan-Sep 2025: 725,966 t"),
("ASCO","2026-01-01","2026-09-30","tonnes_ferry_vehicles_transit",776744,"tonnes","transit motor vehicles by ferries, weight","https://en.apa.az/infrastructure/vehicle-transportation-by-ferries-in-azerbaijan-increases-by-12-532166","2026-10-26","opened","+11%"),
("ASCO","2026-01-01","2026-09-30","tonnes_dry",1415187,"tonnes","cargo carried by dry-cargo vessels","https://en.apa.az/infrastructure/significant-increase-in-dry-cargo-transportation-in-azerbaijan-transit-volume-more-than-doubles-529508","2026-10-12","opened","Jan-Sep 2025: 1,019,065 t; transit 1,014,615 t (2025: 476,192 t)"),
("ASCO","2026-09-01","2026-09-30","tonnes_dry",163090,"tonnes","cargo carried by dry-cargo vessels, September","https://en.apa.az/infrastructure/significant-increase-in-dry-cargo-transportation-in-azerbaijan-transit-volume-more-than-doubles-529508","2026-10-12","opened","Sep 2025: 143,115 t"),
("Kazmortransflot","2025-01-01","2025-12-31","teu",59400,"TEU","containers on the Aktau-Baku-Aktau feeder line","https://api.report.az/en/infrastructure/kazmortransflot-s-container-shipments-via-caspian-grew-by-over-15-in-2025","2026-01-14","opened","citing KazMunayGas"),
("Kazmortransflot","2024-01-01","2024-12-31","teu",51400,"TEU","containers on the Aktau-Baku-Aktau feeder line","https://api.report.az/en/infrastructure/kazmortransflot-s-container-shipments-via-caspian-grew-by-over-15-in-2025","2026-01-14","opened","comparison figure"),
# Kuryk
("Kuryk","2025-01-01","2025-12-31","tonnes_total",1955500,"tonnes","total cargo handled at Kuryk (port management interview)","https://rail-news.kz/ru/interview/24282-port-kuryk-raskryvaet-svoi-potencial-kak-kliucevoe-zveno-tmtm.html","2026-07-17","opened","KTZ newspaper interview; Maritime Administration gives 1,719 kt; rail+road+grain components sum to 1,965.4 kt, not 1,955.5"),
("Kuryk","2025-01-01","2025-12-31","tonnes_rail",1059400,"tonnes","cargo over rail (ferry) berths","https://rail-news.kz/ru/interview/24282-port-kuryk-raskryvaet-svoi-potencial-kak-kliucevoe-zveno-tmtm.html","2026-07-17","opened",""),
("Kuryk","2025-01-01","2025-12-31","tonnes_road",659600,"tonnes","cargo over road (ferry) berths","https://rail-news.kz/ru/interview/24282-port-kuryk-raskryvaet-svoi-potencial-kak-kliucevoe-zveno-tmtm.html","2026-07-17","opened",""),
("Kuryk","2025-01-01","2025-12-31","trucks",25544,"count","trucks handled in the road sector","https://rail-news.kz/ru/interview/24282-port-kuryk-raskryvaet-svoi-potencial-kak-kliucevoe-zveno-tmtm.html","2026-07-17","opened","3% above plan"),
("Kuryk","2025-01-01","2025-12-31","tonnes_grain",246400,"tonnes","grain terminal throughput","https://rail-news.kz/ru/interview/24282-port-kuryk-raskryvaet-svoi-potencial-kak-kliucevoe-zveno-tmtm.html","2026-07-17","opened",""),
("Kuryk","2026-01-01","2026-05-31","tonnes_total",731500,"tonnes","total cargo handled, Jan-May","https://rail-news.kz/ru/interview/24282-port-kuryk-raskryvaet-svoi-potencial-kak-kliucevoe-zveno-tmtm.html","2026-07-17","opened","sum of the five monthly figures = 731.5 kt"),
("Kuryk","2021-01-01","2021-12-31","tonnes_total",974000,"tonnes","cargo transshipped at Kuryk","https://www.trend.az/business/transport/3550421.html","2022-02-04","opened","port told Trend; 971 kt to/from Azerbaijan; Maritime Administration 974.5 kt"),
("Kuryk","2019-01-01","2019-11-30","tonnes_total",1200000,"tonnes","cargo transshipped, Jan-Nov","https://www.lada.kz/aktau_news/society/75450-za-tri-goda-port-kuryk-perevez-bolee-chetyreh-millionov-tonn-gruzov.html","2019-12-13","opened","stated as 'more than 1.2 million'; 760 kt import, 485 kt export"),
("Kuryk","2026-01-01","2026-06-30","tonnes_total",884800,"tonnes","total cargo handled, H1","https://www.lada.kz/aktau_news/ekonomika/156293-port-kuryk-obrabotal-pochti-885-tysiach-tonn-gruzov-za-pervoe-polugodie.html","2026-08-04","opened","also Trend 4213821 (step1)"),
("Kuryk","2026-01-01","2026-06-30","tonnes_rail",475500,"tonnes","rail direction, H1","https://www.lada.kz/aktau_news/ekonomika/156293-port-kuryk-obrabotal-pochti-885-tysiach-tonn-gruzov-za-pervoe-polugodie.html","2026-08-04","opened","export 242.3 kt, import 233.2 kt"),
("Kuryk","2026-01-01","2026-06-30","tonnes_road",306200,"tonnes","road direction, H1","https://www.lada.kz/aktau_news/ekonomika/156293-port-kuryk-obrabotal-pochti-885-tysiach-tonn-gruzov-za-pervoe-polugodie.html","2026-08-04","opened","export 151.4 kt, import 154.8 kt"),
("Kuryk","2026-01-01","2026-06-30","tonnes_grain",104100,"tonnes","grain terminal, H1","https://www.lada.kz/aktau_news/ekonomika/156293-port-kuryk-obrabotal-pochti-885-tysiach-tonn-gruzov-za-pervoe-polugodie.html","2026-08-04","opened",""),
("KZ seaports","2025-01-01","2025-06-30","tonnes_total",4500000,"tonnes","cargo through Aktau and Kuryk ports, H1","https://www.portseurope.com/kazakhstans-aktau-and-kuryk-ports-handled-4-5-mln-tonnes-of-cargo-in-h125/","2025-07-19","opened","citing the Kazakh government; +25% y/y"),
# TITR
("TITR","2024-01-01","2024-12-31","tonnes_total",3300000,"tonnes","freight via the seaports of Kazakhstan and Azerbaijan, per Association members","https://middlecorridor.com/en/press-center/news/04-03-2025","2025-03-04","opened","TITR Association; +20% vs 2023"),
("TITR","2024-01-01","2024-12-31","teu",56500,"TEU","container transportation volume, TITR Association","https://middlecorridor.com/en/press-center/news/04-03-2025","2025-03-04","opened","+176% vs 2023"),
("TITR","2025-01-01","2025-12-31","tonnes_total",1900000,"tonnes","'cargo turnover' of the route, maximum since 2021","https://traceca.ge/en/route/silk-road/institutionalmechanismsofthetrans-caspianinternationaltransportroute","2026-04-07","opened","opinion article by a Georgian rail consultant on traceca.ge; no source or definition given; rounds the 1.867 Mt figure"),
("TITR","2025-01-01","2025-12-31","teu",76900,"TEU","container volume on the route","https://traceca.ge/en/route/silk-road/institutionalmechanismsofthetrans-caspianinternationaltransportroute","2026-04-07","opened","+36% vs previous year; same article"),
("TITR","2025-01-01","2025-12-31","tonnes_total",1867000,"tonnes","'cargo moved through the Middle Corridor', TITR Association","https://bm.ge/en/news/container-traffic-surges-36-on-trans-caspian-middle-corridor-in-2025","","snippet","bm.ge returns 403; only search snippet seen; 'slightly exceeds 2024'"),
("TITR","2025-01-01","2025-12-31","teu",76900,"TEU","containers, TITR Association","https://bm.ge/en/news/container-traffic-surges-36-on-trans-caspian-middle-corridor-in-2025","","snippet","+36%"),
("TITR","2025-01-01","2025-12-31","teu",42000,"TEU","container transportation along TITR, per KTZ","https://www.trend.az/casia/kazakhstan/4163354.html","2026-03-11","opened","+15%; conflicts with 76,900"),
("TITR","2025-01-01","2025-12-31","tonnes_total",4120000,"tonnes","total freight volume on TITR, 'official figures'","https://timesca.com/middle-corridor-must-get-faster-titr-chief-tells-tca/","2026-08-30","opened","stated as 'about 4.12 million tons' (2024: 4.48); container traffic 'around 77,000 TEUs'"),
]
for h in H:
    add(*h)

# ---------------- SCOPING_RESEARCH.md section e, carried over ----------------
S = "step1"
ST = [
("TITR","2025-01-01","2025-12-31","tonnes_total",4119000,"tonnes","route cargo per year (Kazakh Ministry of Transport)","https://astanatimes.com/2026/03/trans-caspian-transport-route-cargo-volumes-increase-fivefold-in-seven-years/","2026-03","2024: 4.484 Mt; no definition of modes or border"),
("TITR","2025-01-01","2025-12-31","tonnes_total",4500000,"tonnes","'total cargo traffic' by end of 2025 (Vice Minister)","https://www.trend.az/casia/4213821.html","2026","stated as a range 4.5-4.7 Mt; lower bound recorded"),
("TITR","2022-01-01","2022-12-31","teu",33000,"TEU","TITR containers","https://astanatimes.com/2023/12/cargo-transportation-along-middle-corridor-soars-88-reaches-2-million-tons-in-2023/","2023-12",""),
("TITR","2025-01-01","2025-12-31","teu",77000,"TEU","TITR containers (Kazakh ministry)","https://www.gov.kz/memleket/entities/transport/press/news/details/1177616?lang=ru","2026","stated as 'about 77 thousand TEU'"),
("TITR","2025-01-01","2025-12-31","teu",42000,"TEU","containers 'on the route' per KTZ","https://railways.kz/en/news2026/development-titr-discussed/","2026",""),
]
for y, v in zip(range(2019, 2026), [0.759, 0.783, 0.586, 1.485, 2.764, 4.484, 4.119]):
    ST.append(("TITR", f"{y}-01-01", f"{y}-12-31", "tonnes_total", round(v * 1e6), "tonnes", "route cargo per year (Kazakh Ministry of Transport)",
               "https://bizmedia.kz/2026-03-10-za-7-let-tmtm-uvelichil-perevozki-pochti-v-5-raz/", "2026-03-10", "series as listed in STEP1"))
PB = "Port of Baku"
ST += [
(PB,"2019-01-01","2019-12-31","tonnes_total",4061600,"tonnes","cargo handled","https://en.portnews.ru/news/290601","",""),
(PB,"2019-01-01","2019-12-31","tonnes_transit",3444200,"tonnes","transit cargo handled","https://en.portnews.ru/news/290601","",""),
(PB,"2019-01-01","2019-12-31","teu",35152,"TEU","containers handled","https://en.portnews.ru/news/290601","",""),
(PB,"2019-01-01","2019-12-31","wagons",44175,"count","rail wagons handled","https://en.portnews.ru/news/290601","",""),
(PB,"2019-01-01","2019-12-31","trucks",33671,"count","wheeled vehicles handled","https://en.portnews.ru/news/290601","","'wheeled vehicles'"),
(PB,"2020-01-01","2020-12-31","tonnes_total",4800000,"tonnes","cargo handled","https://traceca-org.org/en/news/single-news/n/baku_port_increases_cargo_turnover_by_20_pct_in_2020","","transit 87%"),
(PB,"2020-01-01","2020-12-31","teu",40345,"TEU","containers handled","https://traceca-org.org/en/news/single-news/n/baku_port_increases_cargo_turnover_by_20_pct_in_2020","",""),
(PB,"2020-01-01","2020-12-31","teu",40395,"TEU","containers handled","https://en.apa.az/corridors/record-turnover-at-port-of-baku-annual-container-throughput-reaches-100000-teu-486763","","later source; conflicts with 40,345"),
(PB,"2020-01-01","2020-12-31","trucks",43218,"count","trucks handled","https://traceca-org.org/en/news/single-news/n/baku_port_increases_cargo_turnover_by_20_pct_in_2020","",""),
(PB,"2021-01-01","2021-12-31","tonnes_total",5600000,"tonnes","cargo handled","https://en.portnews.ru/news/325155","","transit 92.7%"),
(PB,"2021-01-01","2021-12-31","teu",45025,"TEU","containers handled","https://en.portnews.ru/news/325155","",""),
(PB,"2021-01-01","2021-12-31","tonnes_oil",1100000,"tonnes","oil (Dubendi terminal)","https://en.portnews.ru/news/325155","","stated as 'over 1.1 Mt'"),
(PB,"2022-01-01","2022-12-31","tonnes_total",6300000,"tonnes","cargo handled","https://www.azernews.az/business/220584.html","",""),
(PB,"2023-01-01","2023-12-31","tonnes_total",7400000,"tonnes","cargo handled","http://report.az/en/infrastructure/cargo-handling-at-baku-port-climbs-up","","stated as 'about'"),
(PB,"2023-01-01","2023-12-31","tonnes_transit",5300000,"tonnes","transit cargo","http://report.az/en/infrastructure/cargo-handling-at-baku-port-climbs-up","",""),
(PB,"2023-01-01","2023-12-31","teu",43900,"TEU","containers handled","http://report.az/en/infrastructure/cargo-handling-at-baku-port-climbs-up","",""),
(PB,"2023-01-01","2023-12-31","wagons",37300,"count","rail wagons handled","http://report.az/en/infrastructure/cargo-handling-at-baku-port-climbs-up","",""),
(PB,"2023-01-01","2023-12-31","trucks",54200,"count","trucks handled","http://report.az/en/infrastructure/cargo-handling-at-baku-port-climbs-up","",""),
(PB,"2023-01-01","2023-12-31","tonnes_oil",2100000,"tonnes","oil handled","http://report.az/en/infrastructure/cargo-handling-at-baku-port-climbs-up","",""),
(PB,"2024-01-01","2024-12-31","tonnes_total",7600000,"tonnes","cargo handled","https://www.trend.az/business/4018095.html","",""),
(PB,"2024-01-01","2024-12-31","tonnes_transit",5300000,"tonnes","transit cargo","https://www.trend.az/business/4018095.html","",""),
(PB,"2024-01-01","2024-12-31","teu",76800,"TEU","containers handled","https://www.trend.az/business/4018095.html","",""),
(PB,"2024-01-01","2024-12-31","wagons",37500,"count","rail wagons handled","https://www.trend.az/business/4018095.html","",""),
(PB,"2024-01-01","2024-12-31","trucks",58200,"count","trucks handled","https://www.trend.az/business/4018095.html","",""),
(PB,"2024-01-01","2024-12-31","tonnes_oil",1800000,"tonnes","oil handled","https://www.trend.az/business/4018095.html","",""),
(PB,"2024-01-01","2024-12-31","tonnes_dry",1044000,"tonnes","dry cargo handled","https://www.trend.az/business/4018095.html","",""),
(PB,"2024-01-01","2024-06-30","tonnes_total",3695910,"tonnes","cargo handled","https://report.az/en/infrastructure/cargo-turnover-at-baku-port-up-by-over-6-in-first-half-of-2025","",""),
(PB,"2024-01-01","2024-06-30","teu",30869,"TEU","containers handled","https://report.az/en/infrastructure/cargo-turnover-at-baku-port-up-by-over-6-in-first-half-of-2025","",""),
(PB,"2025-01-01","2025-03-31","tonnes_total",1900000,"tonnes","cargo handled","https://report.az/en/infrastructure/baku-port-sees-nearly-9-increase-in-cargo-handling","","stated as 'over'"),
(PB,"2025-01-01","2025-03-31","teu",30034,"TEU","containers handled","https://report.az/en/infrastructure/baku-port-sees-nearly-9-increase-in-cargo-handling","",""),
(PB,"2025-01-01","2025-03-31","wagons",7765,"count","rail wagons handled","https://report.az/en/infrastructure/baku-port-sees-nearly-9-increase-in-cargo-handling","",""),
(PB,"2025-01-01","2025-03-31","trucks",13711,"count","wheeled vehicles handled","https://report.az/en/infrastructure/baku-port-sees-nearly-9-increase-in-cargo-handling","",""),
(PB,"2025-01-01","2025-06-30","tonnes_total",3930521,"tonnes","cargo handled","https://report.az/en/infrastructure/cargo-turnover-at-baku-port-up-by-over-6-in-first-half-of-2025","",""),
(PB,"2025-01-01","2025-06-30","teu",53030,"TEU","containers handled","https://report.az/en/infrastructure/cargo-turnover-at-baku-port-up-by-over-6-in-first-half-of-2025","","stated as 'over'"),
(PB,"2025-01-01","2025-10-31","tonnes_total",7000000,"tonnes","cargo handled","https://report.az/en/infrastructure/ady-cargo-handling-at-baku-port-surges-by-nearly-6","","stated as 'nearly'"),
(PB,"2025-01-01","2025-10-31","teu",86000,"TEU","containers handled","https://report.az/en/infrastructure/ady-cargo-handling-at-baku-port-surges-by-nearly-6","",""),
(PB,"2025-01-01","2025-11-30","tonnes_total",7547000,"tonnes","cargo handled","https://en.apa.az/corridors/record-turnover-at-port-of-baku-annual-container-throughput-reaches-100000-teu-486763","",""),
(PB,"2025-01-01","2025-12-18","teu",100000,"TEU","containers handled by 18 Dec","https://en.apa.az/corridors/record-turnover-at-port-of-baku-annual-container-throughput-reaches-100000-teu-486763","","stated as 'over'"),
(PB,"2025-01-01","2025-12-31","tonnes_total",8200000,"tonnes","cargo handled","https://mincom.gov.az/en/media-en/news/record-transit-freight-volumes-highest-level-in-five-years","","stated as 'over'"),
(PB,"2025-01-01","2025-12-31","teu",107000,"TEU","containers handled","https://mincom.gov.az/en/media-en/news/record-transit-freight-volumes-highest-level-in-five-years","",""),
(PB,"2026-01-01","2026-07-31","tonnes_dry",1400000,"tonnes","dry cargo handled","https://mincom.gov.az/en/media-en/news/record-transit-freight-volumes-highest-level-in-five-years","","a search summary calls this 'Port of Alat' (the same port)"),
(PB,"2026-01-01","2026-07-31","teu",72370,"TEU","containers handled","https://mincom.gov.az/en/media-en/news/record-transit-freight-volumes-highest-level-in-five-years","",""),
("Aktau","2022-01-01","2022-12-31","tonnes_total",3850000,"tonnes","cargo handled","https://www.portseurope.com/kazakh-port-of-aktau-handle-3-8-million-tonnes-of-cargo-in-2022/","","stated as 'over'; oil 2.5 Mt, grain 447 kt"),
("Aktau","2023-01-01","2023-07-31","tonnes_total",2600000,"tonnes","cargo handled","https://www.trend.az/casia/kazakhstan/3792392.html","","stated as 'over'"),
("Aktau","2023-01-01","2023-07-31","containers",13000,"count","containers handled","https://www.trend.az/casia/kazakhstan/3792392.html","","stated as 'over'; containers, not TEU"),
("Aktau","2024-01-01","2024-08-31","tonnes_total",3000000,"tonnes","cargo handled","https://ktze.kz/en/news/c368be52-df73-492b-898d-bea0443594c9","","stated as 'over'"),
("Aktau","2024-01-01","2024-12-31","teu",58500,"TEU","transit containers","https://www.argusmedia.com/pt/news-and-insights/latest-market-news/2723885-tranzit-konteynerov-cherez-aktau-vyrastet-v-2026-g.","","stated as 'about 58.5k'"),
("Aktau","2025-01-01","2025-12-31","teu",65000,"TEU","transit containers, FORECAST","https://www.argusmedia.com/pt/news-and-insights/latest-market-news/2723885-tranzit-konteynerov-cherez-aktau-vyrastet-v-2026-g.","","forecast made mid-2025, not an outturn"),
("Kuryk","2023-01-01","2023-08-31","tonnes_total",1500000,"tonnes","cargo transshipped","https://railways.kz/en/news/about-15-million-tons-cargo-were-transshipped-through-port-kuryk/","","stated as 'about'"),
("Kuryk","2023-01-01","2023-08-31","ferry_calls",480,"count","ferries handled","https://railways.kz/en/news/about-15-million-tons-cargo-were-transshipped-through-port-kuryk/","",""),
("Kuryk","2023-01-01","2023-08-31","wagons",13800,"count","wagons handled","https://railways.kz/en/news/about-15-million-tons-cargo-were-transshipped-through-port-kuryk/","","stated as 'about'"),
("Kuryk","2023-01-01","2023-08-31","trucks",18000,"count","vehicles handled","https://railways.kz/en/news/about-15-million-tons-cargo-were-transshipped-through-port-kuryk/","","stated as 'over'"),
("Kuryk","2023-01-01","2023-10-31","tonnes_total",1800000,"tonnes","cargo transshipped","https://bizmedia.kz/2023-11-28-morskoj-port-kuryk-uspeshno-obrabotal-bolee-18-milliona-tonn-gruza/","",""),
("Kuryk","2023-01-01","2023-10-31","ferry_calls",600,"count","ferries handled","https://bizmedia.kz/2023-11-28-morskoj-port-kuryk-uspeshno-obrabotal-bolee-18-milliona-tonn-gruza/","","stated as 'about'"),
("Kuryk","2024-01-01","2024-12-31","tonnes_total",1957800,"tonnes","cargo transshipped","https://ru.sputnik.kz/20250128/cherez-port-kuryk-v-2024-godu-perevaleno-okolo-dvukh-millionov-tonn-gruzov-50366321.html","","Maritime Administration gives 1,931.9 kt"),
("Kuryk","2024-01-01","2024-12-31","tonnes_rail",1150600,"tonnes","rail cargo","https://ru.sputnik.kz/20250128/cherez-port-kuryk-v-2024-godu-perevaleno-okolo-dvukh-millionov-tonn-gruzov-50366321.html","",""),
("Kuryk","2024-01-01","2024-12-31","tonnes_road",781300,"tonnes","road cargo","https://ru.sputnik.kz/20250128/cherez-port-kuryk-v-2024-godu-perevaleno-okolo-dvukh-millionov-tonn-gruzov-50366321.html","",""),
("Kuryk","2024-01-01","2024-12-31","tonnes_grain",25900,"tonnes","grain","https://ru.sputnik.kz/20250128/cherez-port-kuryk-v-2024-godu-perevaleno-okolo-dvukh-millionov-tonn-gruzov-50366321.html","",""),
("Kuryk","2025-05-01","2025-05-31","tonnes_total",267000,"tonnes","cargo handled in May (monthly record)","https://www.trend.az/business/transport/4054130.html","","a search summary of Moscow Times gives 287,000 t for the same month (not opened)"),
("Kuryk","2026-01-01","2026-06-30","tonnes_total",884800,"tonnes","cargo handled, H1","https://www.trend.az/casia/4213821.html","",""),
("KZ seaports","2023-01-01","2023-11-30","tonnes_total",6500000,"tonnes","transportation through seaports","https://primeminister.kz/en/news/for-11-months-of-2023-transportation-through-seaports-amounted-to-65-million-tons-karabayev-26627","",""),
("KZ seaports","2023-01-01","2023-12-31","tonnes_total",7200000,"tonnes","cargo through seaports","https://www.trend.az/casia/kazakhstan/3866319.html","","Maritime Administration gives 7,168 kt"),
("KZ seaports","2024-01-01","2024-10-31","tonnes_total",6200000,"tonnes","cargo through Caspian ports","https://timesca.com/kazakhstans-caspian-sea-ports-increase-cargo-transportation/","",""),
("KZ seaports","2025-01-01","2025-12-31","tonnes_total",8000000,"tonnes","cargo through seaports","https://www.interfax.kz/en/news/78594","","Maritime Administration gives 7,453 kt"),
("KZ seaports","2025-01-01","2025-12-31","teu",90637,"TEU","containers through seaports","https://astanatimes.com/2026/02/kazakhstan-strengthens-its-role-as-eurasian-transit-hub-with-36-9-million-tons-of-freight-in-2025/","",""),
]
for e, ps, pe, m, v, u, d, url, sd, note in ST:
    add(e, ps, pe, m, v, u, d, url, sd, S, note)
# Port of Baku rows re-opened in this pass
for e, ps, pe, m, v, u, d, url, sd, note in [
 (PB,"2022-01-01","2022-11-30","tonnes_total",5430000,"tonnes","cargo handled","https://www.trend.az/business/transport/3681349.html","2022-12-14","+14.7%"),
 (PB,"2022-01-01","2022-11-30","teu",48345,"TEU","containers handled","https://www.trend.az/business/transport/3681349.html","2022-12-14",""),
 (PB,"2022-01-01","2022-11-30","trucks",46700,"count","wheeled vehicles (TIR) handled","https://www.trend.az/business/transport/3681349.html","2022-12-14","stated as 'over 46,700'; conflicts with PortNews 'over 9,300' for Jan-Sep 2022"),
 (PB,"2022-01-01","2022-11-30","wagons",36187,"count","rail wagons handled","https://www.trend.az/business/transport/3681349.html","2022-12-14","text says 'in 2022' in a Jan-Nov release"),
 (PB,"2022-01-01","2022-09-30","trucks",9300,"count","wheeled vehicles handled","https://en.portnews.ru/news/337256","2022-10-19","stated as 'over 9,300', 'tripled'; port Telegram channel"),
 (PB,"2021-01-01","2021-12-31","tonnes_total",5600000,"tonnes","port throughput","https://en.portnews.ru/news/337256","2022-10-19","+14.6%"),
 (PB,"2024-01-01","2024-12-31","teu",76775,"TEU","containers handled","https://www.maritimeprofessional.com/news/baku-port-handles-more-containers-413710","2025-12-19","Reuters via MarineLink; 2025 forecast 105,000 TEU"),
 (PB,"2025-01-01","2025-09-30","tonnes_total",6108000,"tonnes","cargo handled","https://news.az/news/port-of-baku-posts-highest-cargo-performance-in-22-years","2025-10-06","citing Azerbaijan Railways; +6.7%"),
 (PB,"2025-01-01","2025-09-30","teu",77295,"TEU","containers handled","https://news.az/news/port-of-baku-posts-highest-cargo-performance-in-22-years","2025-10-06","+40.4%"),
 (PB,"2026-01-01","2026-08-31","tonnes_total",5500000,"tonnes","cargo handled","https://caliber.az/en/post/baku-port-handles-5-5-million-tons-of-cargo-in-eight-months","2026-09-17","stated as 'more than'; +~3%"),
 (PB,"2026-01-01","2026-08-31","teu",85000,"TEU","containers handled","https://caliber.az/en/post/baku-port-handles-5-5-million-tons-of-cargo-in-eight-months","2026-09-17","stated as 'more than'; +~22%"),
 (PB,"2026-08-01","2026-08-31","teu",12900,"TEU","containers handled in August","https://caliber.az/en/post/baku-port-handles-5-5-million-tons-of-cargo-in-eight-months","2026-09-17","+39% y/y"),
 (PB,"2026-01-01","2026-09-30","teu",100000,"TEU","containers handled","https://en.apa.az/entrepreneurship/transit-cargo-transportation-through-azerbaijan-reaches-record-high-531120","2026-10-20","+29%"),
 (PB,"2026-01-01","2026-09-30","tonnes_dry",1730000,"tonnes","dry cargo handled","https://en.apa.az/entrepreneurship/transit-cargo-transportation-through-azerbaijan-reaches-record-high-531120","2026-10-20","+71%"),
 ("Azerbaijan transit","2026-01-01","2026-09-30","tonnes_transit",12000000,"tonnes","transit cargo through Azerbaijan, all modes","https://en.apa.az/entrepreneurship/transit-cargo-transportation-through-azerbaijan-reaches-record-high-531120","2026-10-20","stated as 'exceeded 12 million'; +14.5%"),
]:
    add(e, ps, pe, m, v, u, d, url, sd, "opened", note)

cols = ["entity", "period_start", "period_end", "metric", "value", "unit", "definition", "source_url", "source_date", "status", "note"]
with open(OUT, "w", newline="", encoding="utf-8") as f:
    w = csv.DictWriter(f, fieldnames=cols)
    w.writeheader()
    for r in rows:
        if isinstance(r["value"], float) and r["value"].is_integer():
            r["value"] = int(r["value"])
        w.writerow(r)
print(len(rows), "rows")
