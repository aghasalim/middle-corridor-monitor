import pandas as pd
import pytest

from mcm import validate as v
from mcm.validate import COLUMNS


def official(rows):
    df = pd.DataFrame(rows, columns=["entity", "period_start", "period_end", "metric", "value", "unit"])
    for c in COLUMNS:
        if c not in df:
            df[c] = ""
    df["period_start"] = pd.to_datetime(df["period_start"])
    df["period_end"] = pd.to_datetime(df["period_end"])
    return df[COLUMNS]


def test_missing_file_returns_empty(tmp_path, capsys):
    df = v.load_official(tmp_path / "nope.csv")
    assert df.empty and "not found" in capsys.readouterr().out


def test_cumulative_to_increments():
    df = v.to_tonnes(official([
        ["Port of Baku", "2025-01-01", "2025-03-31", "tonnes_total", 1.9, "Mt"],
        ["Port of Baku", "2025-01-01", "2025-06-30", "tonnes_total", 3.9, "Mt"],
        ["Port of Baku", "2025-01-01", "2025-12-31", "tonnes_total", 8.2, "Mt"],
        ["Aktau", "2023-01-01", "2023-07-31", "tonnes_total", 2.6, "Mt"],
    ]))
    inc = v.increments(df)
    baku = inc[inc.entity == "Port of Baku"].sort_values("period_end")
    assert (~baku["derived"]).sum() == 3  # the cumulative releases themselves are kept
    inc_rows = baku[baku["derived"]]
    assert inc_rows["value_std"].tolist() == pytest.approx([2.0e6, 4.3e6])
    assert inc_rows["period_start"].dt.strftime("%Y-%m-%d").tolist() == ["2025-04-01", "2025-07-01"]
    assert len(inc[inc.entity == "Aktau"]) == 1  # single release: nothing to difference


def test_no_differencing_across_years():
    inc = v.increments(v.to_tonnes(official([
        ["TITR", "2024-01-01", "2024-12-31", "tonnes_total", 4.484, "Mt"],
        ["TITR", "2025-01-01", "2025-12-31", "tonnes_total", 4.119, "Mt"],
    ])))
    assert not inc["derived"].any()


def pw(start="2024-01-01", end="2025-12-31", tonnes=1.0):
    dates = pd.date_range(start, end, freq="D")
    return pd.DataFrame({"date": dates, **{m: 2 for m in v.PW_MEASURES},
                         "dry_tonnes": tonnes, "all_tonnes": tonnes * 3})


def test_period_alignment_sums_exact_days_and_skips_uncovered():
    off = v.increments(v.to_tonnes(official([
        ["Port of Baku", "2025-01-01", "2025-03-31", "tonnes_total", 90, "t"],
        ["Port of Baku", "2025-01-01", "2025-06-30", "tonnes_total", 181, "t"],
        ["Port of Baku", "2026-01-01", "2026-03-31", "tonnes_total", 5, "t"],  # beyond PortWatch
        ["Kuryk", "2024-01-01", "2024-12-31", "tonnes_total", 5, "t"],  # no PortWatch port
    ])))
    al = v.align(off, {"port100": pw()})
    dry = al[al.pw_measure == "dry_tonnes"].sort_values(["period_start", "period_end"])
    assert dry["portwatch"].tolist() == [90.0, 181.0, 91.0]  # Jan-Mar, Jan-Jun, derived Apr-Jun
    assert dry["ratio_pw_over_official"].tolist() == pytest.approx([1.0, 1.0, 1.0])
    assert (al.entity != "Kuryk").all()


def test_period_with_missing_day_is_skipped():
    d = pw()
    d = d[d["date"] != "2025-02-02"]
    assert v.pw_period(d, pd.Timestamp("2025-01-01"), pd.Timestamp("2025-03-31")) is None


def test_annual_comparison_growth_and_correlation():
    rows = [[v.TITR_KZ, f"{y}-01-01", f"{y}-12-31", "tonnes_total", val, "Mt"]
            for y, val in [(2019, 1.0), (2020, 2.0), (2021, 3.0), (2022, 5.0)]]
    off = v.increments(v.to_tonnes(official(rows)))
    daily = {p: pw("2019-01-01", "2022-12-31") for p in v.ENTITY_PORTS[v.TITR_KZ]}
    al = v.align(off, daily)
    yearly, summary = v.annual_comparison(al, years=range(2019, 2023))
    t = yearly[yearly.pw_measure == "dry_tonnes"].set_index("year")
    assert t.loc[2020, "official_yoy"] == pytest.approx(1.0)
    assert t.loc[2020, "portwatch_yoy"] == pytest.approx(366 / 365 - 1)  # 2020 is a leap year
    s = summary[summary.pw_measure == "dry_tonnes"].iloc[0]
    assert s.level_n == 4 and s.yoy_n == 3


def test_corr_needs_three_points():
    r = v.corr(pd.Series([1.0, 2.0]), pd.Series([2.0, 1.0]))
    assert r["n"] == 2 and pd.isna(r["pearson"])


def test_aktau_plus_amct_is_summed_from_the_same_source():
    df = v.to_tonnes(official([
        ["Aktau", "2024-01-01", "2024-12-31", "vessel_calls", 1019, "count"],
        [v.AMCT, "2024-01-01", "2024-12-31", "vessel_calls", 173, "count"],
        ["Aktau", "2023-01-01", "2023-12-31", "vessel_calls", 824, "count"],  # no AMCT row: no sum
    ]))
    df["source_url"] = "https://stat.gov.kz/x"
    out = v.add_aktau_amct(df)
    both = out[out.entity == "Aktau incl. AMCT"]
    assert both["value_std"].tolist() == [1192]


def test_monthly_test_out_of_sample_uses_only_earlier_months():
    months = pd.period_range("2022-01", "2025-12", freq="M")
    pwv = [100 + 10 * (i % 12) + i for i in range(len(months))]
    al = pd.DataFrame({"entity": "Kazakhstan sea transport", "metric": "tonnes_carried",
                       "pw_measure": "all_tonnes", "derived": False,
                       "period_start": [m.start_time.date() for m in months],
                       "period_end": [m.end_time.date() for m in months],
                       "official": [2 * x + 5 for x in pwv], "portwatch": pwv})
    table, res = v.monthly_test(al)
    assert res["months"] == 48 and res["level_pearson"] == pytest.approx(1.0)
    assert res["oos_months"] == 24  # months 25..48 have a fit on 24+ earlier months and a year-ago value
    assert res["rmse_portwatch"] == pytest.approx(0.0, abs=1e-6)  # exact linear relation
    assert res["rmse_last_year"] > 1
