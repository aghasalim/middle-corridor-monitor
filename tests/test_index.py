import numpy as np
import pandas as pd
import pytest

from mcm import index as ix
from mcm.portwatch import check_daily, SUFFIXES


def fake_daily(start, end, calls=1, roro=1, tanker=2, tonnes=10.0):
    dates = pd.date_range(start, end, freq="D")
    d = pd.DataFrame({"date": dates})
    for s in SUFFIXES:
        d[f"portcalls_{s}"] = 0
        d[f"import_{s}"] = 0.0
        d[f"export_{s}"] = 0.0
    d["portcalls_container"] = calls
    d["portcalls_roro"] = roro
    d["portcalls_tanker"] = tanker
    d["import_dry_bulk"] = tonnes
    d["export_tanker"] = 99.0
    return d


def test_monthly_sums_and_drops_incomplete_last_month():
    d = ix.add_measures(fake_daily("2019-01-01", "2019-03-15"))
    m = ix.monthly(d, ["dry_calls", "tanker_calls", "dry_tonnes"])
    assert list(m.index) == [pd.Timestamp("2019-01-01"), pd.Timestamp("2019-02-01")]
    assert m.loc["2019-01-01", "dry_calls"] == 31 * 2  # container + roro
    assert m.loc["2019-02-01", "tanker_calls"] == 28 * 2
    assert m.loc["2019-01-01", "dry_tonnes"] == 310.0  # tanker tonnes excluded


def test_monthly_drops_month_with_missing_day():
    d = ix.add_measures(fake_daily("2019-01-01", "2019-02-28"))
    d = d[d["date"] != "2019-02-10"]
    m = ix.monthly(d, ["dry_calls"])
    assert list(m.index) == [pd.Timestamp("2019-01-01")]


def test_rebase_2019_mean_is_100():
    idx = pd.date_range("2019-01-01", "2020-12-01", freq="MS")
    m = pd.DataFrame({"x": np.arange(24, dtype=float) + 1}, index=idx)
    r = ix.rebase(m)
    assert r.loc[r.index.year == 2019, "x"].mean() == pytest.approx(100)
    assert r.loc["2019-01-01", "x"] == pytest.approx(1 / 6.5 * 100)


def test_rebase_needs_full_base_year():
    idx = pd.date_range("2019-03-01", "2020-12-01", freq="MS")
    with pytest.raises(ValueError):
        ix.rebase(pd.DataFrame({"x": 1.0}, index=idx))


def test_rolling12():
    idx = pd.date_range("2019-01-01", periods=14, freq="MS")
    r = ix.rolling12(pd.DataFrame({"x": 1.0}, index=idx))
    assert r["x"].isna().sum() == 11
    assert r["x"].iloc[11] == 12 and r["x"].iloc[13] == 12


def test_sum_ports_adds_and_rejects_missing_day():
    a = fake_daily("2019-01-01", "2019-01-31", calls=1)
    b = fake_daily("2019-01-01", "2019-01-31", calls=3)
    s = ix.sum_ports({"a": a, "b": b}, ["portcalls_container"])
    assert (s["portcalls_container"] == 4).all() and len(s) == 31
    with pytest.raises(ValueError):
        ix.sum_ports({"a": a, "b": b[b["date"] != "2019-01-15"]}, ["portcalls_container"])


def test_check_daily_rejects_gap_and_duplicate():
    d = fake_daily("2019-01-01", "2019-01-31")
    check_daily(d, "x")
    with pytest.raises(ValueError):
        check_daily(d.drop(index=5), "x")
    with pytest.raises(ValueError):
        check_daily(pd.concat([d, d.iloc[[3]]]), "x")


def test_series_index_and_comparator():
    dailies = {p: fake_daily("2019-01-01", "2020-06-10") for p in ix.CASPIAN + ix.BLACKSEA}
    s = ix.series(dailies)
    assert s.index[-1] == pd.Timestamp("2020-05-01")
    assert s.loc["2019-01-01", "caspian_dry_calls"] == 3 * 31 * 2
    assert s.loc["2019-01-01", "blacksea_dry_calls"] == 2 * 31 * 2
    assert s.loc[s.index.year == 2019, "caspian_dry_calls_index"].mean() == pytest.approx(100)


def test_step_month_finds_break():
    idx = pd.date_range("2021-01-01", periods=24, freq="MS")
    s = pd.Series([10.0] * 14 + [40.0] * 10, index=idx)
    mon, before, after = ix.step_month(s)
    assert mon == pd.Timestamp("2022-03-01") and before == 10 and after == 40
