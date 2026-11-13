"""Hand-labelling kit: how many detections to check, and which ones."""
import math

import numpy as np
import pandas as pd


def sample_size(population, p=0.5, margin=0.05, z=1.96):
    """Detections to check by hand to estimate a proportion (e.g. precision) to +/- margin.

    n0 = z^2 p (1 - p) / e^2, then the finite-population correction n = n0 / (1 + (n0 - 1) / N). Rounded up.
    """
    if population <= 0:
        return 0
    n0 = z * z * p * (1 - p) / (margin * margin)
    return min(population, math.ceil(n0 / (1 + (n0 - 1) / population)))


def sample_size_table(population):
    rows = [{"p": p, "margin_pp": round(e * 100), "n_infinite": math.ceil(1.96 ** 2 * p * (1 - p) / e ** 2),
             "n_with_fpc": sample_size(population, p, e)} for p in (0.5, 0.8) for e in (0.05, 0.07, 0.10)]
    return pd.DataFrame(rows)


def stratified_sample(det, n, seed=0):
    """Pick about n detections, spread over year x zone in proportion to stratum size, at least 5 per stratum
    (or the whole stratum if it is smaller). Returns a shuffled copy."""
    rng = np.random.default_rng(seed)
    groups = det.groupby([det["datetime"].str[:4], det["zone"]])
    picks = []
    for _, g in groups:
        k = min(len(g), max(5, round(n * len(g) / len(det))))
        picks.append(g.iloc[rng.choice(len(g), k, replace=False)])
    out = pd.concat(picks)
    return out.iloc[rng.permutation(len(out))].reset_index(drop=True)
