import importlib.util
from pathlib import Path

import pandas as pd
import pytest

ROOT = Path(__file__).resolve().parents[1]
spec = importlib.util.spec_from_file_location("sar_label_eval", ROOT / "research" / "sar_label_eval.py")
ev = importlib.util.module_from_spec(spec)
spec.loader.exec_module(ev)


def test_wilson_known_value():
    lo, hi = ev.wilson(8, 10)  # textbook value: 0.490 to 0.943
    assert lo == pytest.approx(0.490, abs=1e-3) and hi == pytest.approx(0.943, abs=1e-3)


def test_kappa_perfect_and_chance():
    assert ev.kappa(["yes", "no", "yes"], ["yes", "no", "yes"]) == 1
    assert ev.kappa(["yes", "no", "yes", "no"], ["yes", "yes", "no", "no"]) == pytest.approx(0)


def test_precision_ignores_unsure_and_bounds_use_it():
    df = pd.DataFrame({"kind": ["detection"] * 4, "zone": ["basin"] * 4, "is_vessel": ["yes", "yes", "no", "unsure"],
                       "n_seen": 0, "n_possible": 0})
    r = ev.evaluate(df, "t").set_index(["zone", "measure"]).loc[("basin", "precision (yes / (yes + no))")]
    assert r.value == pytest.approx(2 / 3) and r.bound_unsure_as_no == 0.5 and r.bound_unsure_as_yes == 0.75
