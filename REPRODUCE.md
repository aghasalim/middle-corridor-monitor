# Reproducing the results

## Repository layout

```
src/mcm/          index, validation, project page (python -m mcm.build)
src/mcm/sar/      radar detector (python -m mcm.sar.run)
research/         notes on sources and method, one-off checks, figure and video scripts
data/portwatch/   dated copy of the PortWatch download
data/official/    official figures, one row per number with its source
data/sar/         radar detections of both detectors, counting zones, AI labels
outputs/          tables (CSV) and figures (PNG) written by the build
paper/            paper source (LaTeX), PDF, and NUMBERS.md
docs/             project page and animations
tests/            unit tests
```

The radar image cache and the source PDFs of the official figures are not stored here.

## Steps

```
python -m venv .venv
.venv/Scripts/python -m pip install -r requirements.txt
.venv/Scripts/python -m pip install -e .
.venv/Scripts/python -m mcm.build            # downloads PortWatch, then builds everything
.venv/Scripts/python -m mcm.build --offline  # reuses data/portwatch/
.venv/Scripts/python -m pytest -q
.venv/Scripts/python research/paper_checks.py    # extra numbers quoted in the paper
.venv/Scripts/python research/paper_figures.py   # the two validation figures used in the paper
```

On macOS and Linux use `.venv/bin/python`. The build stops with an error if a port's download is short or has a
duplicated or missing day. The download date and the first and last day per port are in
`data/portwatch/snapshot.json`.

The paper is in `paper/latex/` (`main.tex`, `references.bib`, `figures/`). Build it with
`pdflatex main && bibtex main && pdflatex main && pdflatex main`. An earlier 8-page version is `paper/paper.md`
(`paper/build_pdf.py`, needs Chrome).

The second radar detector (`research/second_detector.py`, then `research/detector_agreement.py`) needs PyTorch,
`rslearn`, a clone of https://github.com/allenai/rslearn_projects (set `RSLEARN_PROJECTS` to its folder) and its
1.26 GB checkpoint; see `research/SECOND_DETECTOR_OPTIONS.md`. Its results are already in
`data/sar/detections_ai2.csv`.

The animations and the title image are rebuilt with `research/video.py`, `research/video_detectors.py` (both need
ffmpeg) and `research/banner.py`.
