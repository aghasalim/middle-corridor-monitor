"""Count Sentinel-1 IW GRDH passes over each port per year (Copernicus Data Space catalogue, no login)."""
import json, sys, time, urllib.parse, urllib.request, collections

PORTS = {  # lon, lat
    "Baku/Alat": (49.43, 39.98),
    "Aktau": (51.23, 43.60),
    "Kuryk": (51.62, 43.03),
    "Turkmenbashi": (53.01, 40.01),
}
BASE = "https://catalogue.dataspace.copernicus.eu/odata/v1/Products"


def passes(lon, lat, year):
    flt = (
        "Collection/Name eq 'SENTINEL-1' and "
        "Attributes/OData.CSC.StringAttribute/any(att:att/Name eq 'productType' and "
        "att/OData.CSC.StringAttribute/Value eq 'IW_GRDH_1S') and "
        f"OData.CSC.Intersects(area=geography'SRID=4326;POINT({lon} {lat})') and "
        f"ContentDate/Start ge {year}-01-01T00:00:00.000Z and ContentDate/Start lt {year + 1}-01-01T00:00:00.000Z"
    )
    names, skip = [], 0
    while True:
        q = urllib.parse.urlencode({"$filter": flt, "$select": "Name", "$top": 1000, "$skip": skip}, quote_via=urllib.parse.quote)
        with urllib.request.urlopen(f"{BASE}?{q}", timeout=120) as r:
            page = json.load(r)["value"]
        names += [p["Name"] for p in page]
        if len(page) < 1000:
            return names
        skip += 1000


out = {}
for port, (lon, lat) in PORTS.items():
    out[port] = {}
    for year in range(2019, 2027):
        names = passes(lon, lat, year)
        # one pass = one platform + absolute orbit (adjacent frames of the same pass both contain the point)
        uniq = {(n[:3], n.split("_")[6]) for n in names}
        by_sat = collections.Counter(s for s, _ in uniq)
        days = {n.split("_")[4][:8] for n in names}
        out[port][year] = {"products": len(names), "passes": len(uniq), "days": len(days), **by_sat}
        print(port, year, out[port][year], flush=True)
        time.sleep(0.5)
json.dump(out, open(sys.argv[1], "w"), indent=1)
