# review.md — content refinement (PaperOrchestra step 5)

Draft reviewed: `paper/latex/main.tex`, 15 November 2026. Two rounds by a simulated strict referee
(econometrics / remote-sensing reader of an econ.GN + stat.AP working paper). Rule kept from the method: no new
experiments, every number must trace to `paper/NUMBERS.md`, no defensive padding of the limitations to please
the reviewer, conclusions unchanged.

## Round 1

**Summary as the referee reads it.** An open monthly index of PortWatch port calls for three Caspian ports,
checked against 517 official figures and a first Sentinel-1 count. Mostly negative results, reported plainly.

**Strengths.** Clear questions; validation without estimated inputs; full number trace; honest negatives; the
Ro-Ro step is examined from four sides instead of being explained away.

**Weaknesses and questions (with the fix made).**

| # | Finding | Severity | Fix |
|---|---|---|---|
| 1 | Related work mixed introduction material (corridor reports) with technical baselines and had no SAR-detection or official-statistics precedent beyond Paolo et al. | major | Related work split into three clusters (AIS trade measurement; radar detection; measuring the corridor). Added confirmed works: Adland et al. 2017 (AIS vs customs, crude oil), van der Wielen et al. 2024 (AIS for official port statistics), Hütten 2026 (open AIS port mapping), Komaromi et al. 2022, Yang et al. 2019, Verschuur et al. 2022, Torres et al. 2012, Greidanus et al. 2017, Santamaria et al. 2017, Paolo et al. 2022, and three academic corridor studies. |
| 2 | "10-chip spot check" is stated without its result. | major | Result added from `sar_label_agreement.csv`: agreement on 8 of 10; on the other 2 the model said unsure and the author said vessel. Stated that the 50-chip blind check was not done. |
| 3 | Label shares come from a sample stratified by year and zone; are they reweighted? | major | Stated: per zone, not reweighted by year (`research/sar_label_eval.py` does no weighting); sample sizes per zone given. |
| 4 | Wilson intervals could be read as covering label error. | minor | Sentence added: intervals cover sampling error only. |
| 5 | The break-date method and the naive-forecast benchmark have no reference. | minor | Bai (1997) cited for least-squares break estimation, with a note that the fit dates the step and does not test it; Hyndman and Koehler (2006) cited for naive-forecast benchmarking. |
| 6 | Some detector settings were chosen after looking at first detections; this is in the method but not in the limits. | minor | Added to the radar item of the limits. |
| 7 | Table 3 shows 12 of 56 pairs and only Pearson; where are the rest? | minor | Caption points to `validate_summary.csv` (Spearman and the other 44 pairs). |
| 8 | Questions 1 and 3 rest on tables only; hard to see. | minor | Two new figures from the existing tables (`research/paper_figures.py`): yearly PortWatch/official ratios plus year-on-year changes (Q1), and the 30 out-of-sample months with the three forecasts (Q3). Counting zones figure (`sar_zones.png`, already in the repo) added to the method. |
| 9 | Devil's advocate: the AI labeller and the AI writing assistant are the same model family. Circularity risk in the only positive radar result. | critical (disclosure) | Disclosed in the AI-use statement; the paper already says the labels need a human check before they stand. Not resolvable without the human check; conclusions already conditional on it. |

**Devil's-advocate checks of the core claims.** Causal overclaiming: none found; the Ro-Ro cause stays "not
confirmed", the coverage explanation is "leading", not proven. Baseline fairness: the naive forecasts use the
same months as the regression. Multiple testing: the 56-pair caveat is kept next to the two high correlations.
Novelty: stated as narrow; "we found no ..." claims are scoped to the sources searched, and the gaps in the
search (Scholar, eLIBRARY, RePEc) are stated.

## Round 2 (after the fixes)

| # | Finding | Fix |
|---|---|---|
| 1 | "Where AIS-based estimates were checked ..., the checks concern countries ..." generalises over the literature. | Scoped: "In the works we read, ...". |
| 2 | Related-work claims for works read only as abstracts must not go beyond the abstract. | Each new claim checked against the abstract (OpenAlex or publisher); abstract-only works carry "Abstract only" in the bibliography. The xView3 and Sentinel-1 mission sentences were cut back to what the record supports. |
| 3 | A new corridor-study sentence could imply those papers were read in full. | "Their abstracts describe no use of ship-tracking data." |
| 4 | Style: no "delve", "landscape", "crucial", "furthermore", "moreover", "notably", "leverage" (checked by script). | none needed |

Remaining weaknesses the referee would still raise, and which only new work can fix (listed in Section 7 of the
paper, not padded): no human check of the radar labels; unpublished PortWatch polygons and type mapping; no
port-based monthly target; Alat only.

**Verdict as simulated: major revision, as expected for a working paper whose main results are negative and whose
one positive radar result rests on unchecked AI labels.** No conclusion of `paper/paper.md` was changed.

## Checks run on 15 November 2026

- `.venv/Scripts/python -m pytest -q`: 44 passed.
- `.venv/Scripts/python research/paper_checks.py`: ran; `outputs/tables/paper_checks.csv` unchanged.
- `.venv/Scripts/python -m mcm.build --offline`: ran; all tables and existing figures unchanged byte for byte;
  `docs/index.html` updated (radar line).
- Static check of `main.tex` (scratch script, not in the repo): every `\cite` key is in `references.bib` and
  every entry is cited; every `\ref` has a label; all six figure files exist; braces balance; every numeral in
  the text occurs in `paper/paper.md` or `paper/NUMBERS.md`.
- LaTeX compile: not run. No TeX engine is installed on this machine (pdflatex, xelatex, lualatex, tectonic,
  latexmk, MiKTeX: none; none in WSL either).
