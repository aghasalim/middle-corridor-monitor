import importlib.util
import shutil
from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parents[1]
spec = importlib.util.spec_from_file_location("label_tool", ROOT / "research" / "label_tool.py")
lt = importlib.util.module_from_spec(spec)
spec.loader.exec_module(lt)


def test_roundtrip_keeps_file_byte_identical(tmp_path, monkeypatch):
    copy = tmp_path / "label_sample.csv"
    shutil.copy(lt.CSV_PATH, copy)
    monkeypatch.setattr(lt, "CSV_PATH", copy)
    lt.write_rows(*lt.read_rows())
    assert copy.read_bytes() == (ROOT / "data/sar/label_sample.csv").read_bytes()


def test_only_label_columns_change(tmp_path, monkeypatch):
    copy = tmp_path / "label_sample.csv"
    shutil.copy(ROOT / "data/sar/label_sample.csv", copy)
    monkeypatch.setattr(lt, "CSV_PATH", copy)
    header, rows = lt.read_rows()
    before = [dict(r) for r in rows]
    rows[0].update(lt.clean(rows[0]["kind"], {"n_vessels_seen": "2", "note": "a, \"b\"\nc"}
                            if rows[0]["kind"] == "empty_tile" else {"is_vessel": "yes", "note": "a, \"b\"\nc"}))
    lt.write_rows(header, rows)
    _, after = lt.read_rows()
    assert after[0]["note"] == 'a, "b" c'
    for b, a in zip(before, after):
        assert {k: v for k, v in b.items() if k not in lt.LABEL_COLS} == {k: v for k, v in a.items() if k not in lt.LABEL_COLS}


@pytest.mark.parametrize("kind,data", [("detection", {"is_vessel": "maybe"}), ("empty_tile", {"n_vessels_seen": "-1"}),
                                       ("empty_tile", {"n_vessels_seen": "1.5"}), ("detection", {"n_vessels_seen": "1"}),
                                       ("empty_tile", {"is_vessel": "yes"})])
def test_bad_answers_rejected(kind, data):
    with pytest.raises(ValueError):
        lt.clean(kind, data)


def test_page_gets_no_detector_fields():
    assert set(lt.SHOWN) == {"sample_id", "kind", "zone", "chip_file", "is_vessel", "n_vessels_seen", "note"}
