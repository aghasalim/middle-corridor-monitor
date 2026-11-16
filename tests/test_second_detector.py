import importlib.util
from pathlib import Path

import numpy as np
import pandas as pd

ROOT = Path(__file__).resolve().parents[1]
spec = importlib.util.spec_from_file_location("second_detector", ROOT / "research" / "second_detector.py")
sd = importlib.util.module_from_spec(spec)
spec.loader.exec_module(sd)


def test_box_centre_maps_to_pixel_index():
    # a 3 px box covering pixels 10..12 (edges 10 and 13) is centred on pixel 11; patch origin adds on
    assert sd.box_to_rowcol([10, 20, 13, 23], 400, 300) == (400 + 21, 300 + 11)


def test_patches_cover_the_crop_with_overlap():
    s = sd.starts(1290)
    assert s[0] == 0 and s[-1] + sd.PATCH == 1290 and all(b - a <= sd.PATCH for a, b in zip(s, s[1:]))
    assert sd.starts(300) == [0]


def test_history_is_same_orbit_30_to_60_days_earlier():
    t = pd.to_datetime(["2020-01-01", "2020-03-01", "2020-03-20", "2020-04-15", "2020-04-14"], utc=True)
    p = pd.DataFrame({"scene_id": list("abcde"), "rel_orbit": [6, 6, 6, 6, 28], "t": t})
    assert sd.pick_history(p, "d") == ("b", -45.0)   # c is only 26 days back; e is another orbit
    assert sd.pick_history(p, "a")[0] == "b"           # nothing earlier: nearest >= 30 days, later side


def test_distance_nms_keeps_best_of_close_pair():
    rc = np.array([[0, 0], [3, 4], [50, 50]], float)
    assert sd.distance_nms(rc, np.array([0.8, 0.95, 0.9])) == [1, 2]
