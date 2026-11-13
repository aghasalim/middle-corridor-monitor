"""Area of interest for the Port of Baku at Alat: the working grid and the two zones."""
import json
from pathlib import Path

import numpy as np
from pyproj import Transformer
from shapely.geometry import Point, Polygon, shape

ROOT = Path(__file__).resolve().parents[3]
SAR_DIR = ROOT / "data" / "sar"
CACHE = SAR_DIR / "cache"
ZONES_FILE = SAR_DIR / "zones.geojson"

# Working grid: UTM zone 39N, 10 m pixels (the GRD pixel spacing), north up.
CRS = "EPSG:32639"
RES = 10.0
X0, Y0 = 362000.0, 4431000.0  # top-left corner
W, H = 1500, 1700  # 15 km x 17 km: port, bay, and the open water south and east of the spit

_to_utm = Transformer.from_crs(4326, CRS, always_xy=True)
_to_ll = Transformer.from_crs(CRS, 4326, always_xy=True)


def lonlat_to_pixel(lon, lat):
    """Lon/lat -> fractional (row, col) on the working grid."""
    x, y = _to_utm.transform(lon, lat)
    return (Y0 - np.asarray(y)) / RES - 0.5, (np.asarray(x) - X0) / RES - 0.5


def pixel_to_lonlat(row, col):
    """Pixel centre (row, col) -> lon, lat."""
    return _to_ll.transform(X0 + (np.asarray(col) + 0.5) * RES, Y0 - (np.asarray(row) + 0.5) * RES)


def grid_bbox_lonlat():
    """Lon/lat ring around the working grid (for the catalogue search)."""
    xs = [X0, X0 + W * RES, X0 + W * RES, X0, X0]
    ys = [Y0, Y0, Y0 - H * RES, Y0 - H * RES, Y0]
    lon, lat = _to_ll.transform(xs, ys)
    return [[float(a), float(b)] for a, b in zip(lon, lat)]


def load_zones(path=ZONES_FILE):
    """{'basin': polygon, 'roadstead': polygon} in lon/lat."""
    fc = json.loads(Path(path).read_text(encoding="utf8"))
    return {f["properties"]["zone"]: shape(f["geometry"]) for f in fc["features"]}


def zone_of(lon, lat, zones):
    """Name of the zone containing the point; the basin wins where zones overlap; None if outside both."""
    p = Point(lon, lat)
    for name in ("basin", "roadstead"):
        if name in zones and zones[name].contains(p):
            return name
    return None


def zone_raster(zones):
    """uint8 grid: 0 outside, 1 basin, 2 roadstead."""
    from rasterio.features import rasterize
    from rasterio.transform import from_origin

    out = np.zeros((H, W), np.uint8)
    for code, name in ((2, "roadstead"), (1, "basin")):  # basin painted last so it wins
        if name in zones:
            geom = Polygon(zip(*_to_utm.transform(*zones[name].exterior.xy)))
            out[rasterize([geom], out_shape=(H, W), transform=from_origin(X0, Y0, RES, RES)) == 1] = code
    return out
