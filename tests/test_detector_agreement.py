import sys
from pathlib import Path

import pandas as pd

sys.path.insert(0, str(Path(__file__).parents[1] / "research"))
from detector_agreement import by_zone_year


def test_by_zone_year_sums_and_shares():
    t = pd.DataFrame({"zone": ["roadstead"] * 3, "year": ["2019", "2019", "2020"], "ours": [4, 6, 10],
                      "ai2": [4, 4, 10], "ours_matched": [4, 4, 5], "ai2_matched": [4, 4, 5]})
    g = by_zone_year(t).set_index("year")
    assert g.loc["2019", "ours"] == 10 and g.loc["2019", "ours_matched_share"] == 0.8
    assert g.loc["all", "ai2"] == 18 and g.loc["all", "ai2_matched_share"] == round(13 / 18, 3)
