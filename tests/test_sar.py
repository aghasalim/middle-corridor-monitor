"""SAR detector, sample size and zone assignment. Synthetic images only, no network."""
import numpy as np
import pytest
from shapely.geometry import box

from mcm.sar import aoi, detect, sample

H = W = 200
SEA, SHIP, QUAY = 100.0, 1500.0, 2500.0  # amplitudes (DN): ship is ~23 dB above the sea


def scene(rng, ships=(), quay=True):
    """Speckled sea (gamma power, ~4 looks) with an optional permanent quay and rectangular ships (r0, r1, c0, c1)."""
    amp = np.sqrt(rng.gamma(4.0, SEA ** 2 / 4.0, (H, W)))
    if quay:
        amp[20:26, 30:170] = QUAY * np.sqrt(rng.gamma(4.0, 0.25, (6, 140)))
    for r0, r1, c0, c1 in ships:
        amp[r0:r1, c0:c1] = SHIP
    return amp.astype(np.float32)


def run_detector(ships, quay=True, seed=1):
    rng = np.random.default_rng(seed)
    stack = np.stack([detect.smooth_db(scene(rng, quay=quay)) for _ in range(20)])
    bg = detect.background(stack)
    zone = np.ones((H, W), bool)
    water = detect.water_mask({"vv": bg}, zone)
    kept, dropped = detect.detect({"vv": detect.smooth_db(scene(rng, ships, quay))}, {"vv": bg}, water)
    return kept, dropped, water


def test_ship_on_dark_water_is_found():
    kept, _, _ = run_detector([(100, 102, 80, 95)])  # 150 m x 20 m
    assert len(kept) == 1
    d = kept[0]
    assert abs(d["row"] - 100.5) < 1.5 and abs(d["col"] - 87) < 1.5
    assert 150 <= d["length_m"] <= 190  # true length + up to ~2 px of smoothing at each end
    assert d["det_vv"] and d["peak_db_vv"] > 15


def test_permanent_quay_is_masked_not_detected():
    kept, dropped, water = run_detector([])
    assert kept == []
    assert not water[20:26, 30:170].any()       # the quay itself is masked out
    assert water[100, 100]                      # open water is not
    assert not [d for d in dropped if d["why"] == "too_big"]


def test_empty_sea_gives_nothing():
    kept, _, _ = run_detector([], quay=False)
    assert kept == []


def test_target_under_size_limit_is_dropped():
    kept, dropped, _ = run_detector([(100, 101, 80, 82)])  # 20 m x 10 m bright point
    assert kept == []
    assert any(d["why"] == "too_small" for d in dropped)


def test_thirty_metre_vessel_is_kept():
    kept, _, _ = run_detector([(100, 101, 80, 83)])  # 30 m x 10 m: the smallest size we mean to keep
    assert len(kept) == 1


def test_two_ships_with_a_gap_stay_separate():
    kept, _, _ = run_detector([(100, 102, 60, 75), (107, 109, 60, 75)])  # 50 m of water between them
    assert len(kept) == 2


def test_two_ships_side_by_side_merge():
    # Documented behaviour: with one pixel (10 m) between hulls the 3x3 smoothing closes the gap -> one blob.
    kept, _, _ = run_detector([(100, 102, 60, 75), (103, 105, 60, 75)])
    assert len(kept) == 1


def test_ship_at_a_usually_empty_berth_is_found_next_to_quay():
    kept, _, _ = run_detector([(28, 30, 80, 95)])  # 20 m off the quay face (quay rows 20-25, +1 px mask)
    assert len(kept) == 1


def test_both_polarisations_are_flagged():
    rng = np.random.default_rng(3)
    bg = detect.background(np.stack([detect.smooth_db(scene(rng, quay=False)) for _ in range(20)]))
    water = np.ones((H, W), bool)
    with_ship = detect.smooth_db(scene(rng, [(100, 102, 80, 95)], quay=False))
    without = detect.smooth_db(scene(rng, quay=False))
    kept, _ = detect.detect({"vv": with_ship, "vh": without}, {"vv": bg, "vh": bg}, water)
    assert len(kept) == 1 and kept[0]["det_vv"] and not kept[0]["det_vh"]


def test_sample_size():
    assert sample.sample_size(10 ** 9, 0.5, 0.05) == 385      # textbook infinite-population value
    assert sample.sample_size(1000, 0.5, 0.05) == 278         # 384.16 / (1 + 383.16 / 1000) = 277.7
    assert sample.sample_size(1000, 0.8, 0.10) == 58          # 61.47 / (1 + 60.47 / 1000) = 57.96
    assert sample.sample_size(20, 0.5, 0.05) == 20            # never more than the population
    assert sample.sample_size(0) == 0
    t = sample.sample_size_table(5000)
    assert len(t) == 6 and (t.n_with_fpc <= t.n_infinite).all()


def test_stratified_sample_covers_every_stratum():
    import pandas as pd
    det = pd.DataFrame({"datetime": ["2024-01-01"] * 300 + ["2025-01-01"] * 30 + ["2026-01-01"] * 3,
                        "zone": ["basin", "roadstead", "basin"] * 111})
    s = sample.stratified_sample(det, 60)
    assert set(zip(s.datetime.str[:4], s.zone)) == set(zip(det.datetime.str[:4], det.zone))
    assert len(s) < len(det)


def test_zone_assignment_synthetic():
    zones = {"basin": box(49.0, 40.0, 49.1, 40.1), "roadstead": box(49.05, 40.0, 49.3, 40.1)}
    assert aoi.zone_of(49.02, 40.05, zones) == "basin"
    assert aoi.zone_of(49.07, 40.05, zones) == "basin"       # overlap: basin wins
    assert aoi.zone_of(49.2, 40.05, zones) == "roadstead"
    assert aoi.zone_of(49.5, 40.05, zones) is None


def test_zone_file_and_grid():
    zones = aoi.load_zones()
    assert set(zones) == {"basin", "roadstead"}
    assert aoi.zone_of(49.4465, 39.9742, zones) == "basin"          # middle of the dock
    assert aoi.zone_of(49.4305, 39.9915, zones) is None             # on land north-west of the port
    assert aoi.zone_of(49.5082, 39.9160, zones) == "roadstead"      # anchorage south-east of the spit
    r, c = aoi.lonlat_to_pixel(*aoi.pixel_to_lonlat(700, 500))
    assert r == pytest.approx(700, abs=1e-3) and c == pytest.approx(500, abs=1e-3)
    zr = aoi.zone_raster(zones)
    assert zr.shape == (aoi.H, aoi.W) and set(np.unique(zr)) == {0, 1, 2}


def test_blob_longer_than_any_ship_is_dropped():
    kept, dropped, _ = run_detector([(100, 102, 60, 100)])  # 400 m
    assert kept == [] and any(d["why"] == "too_big" for d in dropped)


def test_fixed_object_flag_only_in_roadstead():
    import pandas as pd
    from mcm.sar import run
    days = pd.date_range("2020-01-01", periods=13, freq="30D").strftime("%Y-%m-%dT00:00:00Z")
    rows = [{"scene_id": f"s{i}", "datetime": d, "zone": z, "row": r, "col": 500.0}
            for z, r in (("roadstead", 1000.0), ("basin", 500.0)) for i, d in enumerate(days)]
    rows += [{"scene_id": f"s{i}", "datetime": d, "zone": "roadstead", "row": 1200.0 + 30 * i, "col": 900.0}
             for i, d in enumerate(days)]  # 13 different anchor positions
    det = pd.DataFrame(rows)
    flag = run.fixed_objects(det)
    assert flag[:13].all()            # same roadstead spot in 13 passes over a year: fixed object
    assert not flag[13:].any()        # a reused berth in the basin, and scattered anchored ships, are not
