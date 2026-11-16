# A second, independent ship detector for Alat: options (16 Nov 2026)

Research only. Nothing was downloaded or installed. Licences, file names and sizes below were read from the
repositories, the GitHub and Hugging Face APIs, and HTTP `HEAD` requests (headers only) on 16 Nov 2026.
Runtimes on our CPU are **estimates, not measurements**, unless a source is given.

## 0. What we have (checked on disk)

- **Source:** Planetary Computer `sentinel-1-grd` (not RTC), IW GRDH, **VV + VH**, read as windows
  (`src/mcm/sar/fetch.py`).
- **Values:** uncalibrated GRD **digital numbers (amplitude)**, stored as uint16. No calibration to sigma0, no
  thermal-noise removal, no dB.
- **Geometry:** resampled with a thin-plate spline through the GCPs, with GCPs moved to sea height (−28 m), bilinear,
  onto a north-up grid in **UTM 39N (EPSG:32639), 10 m pixels, 1,500 × 1,700 px** (15 × 17 km). This is not the
  1,000 × 1,100 px the brief assumed.
- **Passes:** 671 counted passes over three relative orbits (6: 228, 28: 226, 108: 217), not 671 in orbit 28 alone.
- **Cache:** `data/sar/cache/` (git-ignored) holds 806 files, 6.05 GB in total:
  - `scenes/`: 769 `.npz` files, 3.15 GB, each holding `vv` and `vh` arrays of 1700 × 1500 uint16;
  - per-orbit stacks, backgrounds and mean images: about 2.9 GB.

  `data/sar/raw/` does not exist. No full GRD scenes are on disk.
- **Python:** `.venv` runs Python 3.12.10. It has numpy 2.5.4, scipy, rasterio 1.5.2, pyproj, shapely, scikit-image,
  pandas, pystac-client and planetary-computer. It does **not** have torch, torchvision, onnxruntime, ultralytics,
  timm or GDAL Python bindings. Every ML option below needs at least a CPU torch install.

## 1. Ranked shortlist

| Rank | Option | Code licence | Weights licence | Input it expects | Fit for our cache |
|---|---|---|---|---|---|
| **1** | Ai2 `rslearn_projects` Sentinel-1 vessel detector (Skylight, current) | Apache-2.0 | **Apache-2.0, stated in the README** | Raw GRD DN, VV+VH, UTM 10 m, target + 1 historical pass | **Very close**: same values, CRS, pixel size and GCP method |
| 2 | xView3 1st place (BloodAxe), **one** fold model | MIT | **Not stated**; trained on xView3 data, whose licence is unverified | sigma0 in **dB**, VH+VV, 10 m UTM (SNAP-processed) | Needs calibration of DN to sigma0 dB |
| 3 | Ai2 `vessel-detection-sentinels` (older Skylight model, archived) | Apache-2.0 | No separate statement; the weights are files inside the Apache-2.0 repo (Git LFS) | Raw GRD DN clipped to 0–255, VH+VV + 2 historical passes, Web Mercator zoom 13 | Needs reprojection to EPSG:3857 and 2 history passes |

**Not shortlisted:**
- xView3 2nd place (selimsef): Apache-2.0 code; release weights of 92–462 MB each, 1.66 GB for all six; no
  weights licence; inputs in dB with normalisation `(dB+40)/15`. It has the same calibration problem as option 2
  and no advantage over it.
- xView3 3rd–5th place: repositories exist under DIUx-xView. I did not check them for weights.
- The xView3 reference model: BSD-3 code, but its v1.0 release has **no** weights files. It also needs bathymetry.
- GFW, Paolo et al. 2024: see section 3.
- SNAP Ocean Tools, SARFish, and the Hugging Face YOLO models: see section 3.

## 2. Candidates in detail

### 2.1 Ai2 rslearn_projects — Sentinel-1 vessel detection (recommended)

- **Source:**
  - code and docs: https://github.com/allenai/rslearn_projects (owner Allen Institute for AI; actively maintained,
    last push 15 Nov 2026), file `docs/sentinel1_vessels.md`;
  - model config: `data/sentinel1_vessels/20260626_num_historical/config_1hist.yaml`.
- **Licences:** the repo README says "Model weights and Code: Licensed under Apache License 2.0" and
  "Annotations: CC-BY 4.0". This is the only candidate with an explicit, commercial-friendly weights licence.
- **Weights:** files and sizes from HTTP `HEAD`.

  | File | Format | Size |
  |---|---|---|
  | detector `best.ckpt` | PyTorch Lightning checkpoint, **pickle** | 1,262,487,287 bytes (1.18 GiB) |
  | vessel-attribute `best.ckpt` (length, type, heading; optional, not needed) | Lightning checkpoint, pickle | about 1.10 GiB (1,103.4 MiB) |
  | marine-infrastructure GeoJSON (optional filter) | GeoJSON | about 6.9 MiB |

  The detector checkpoint is probably that large because it includes optimiser state (unverified).
- **Architecture:** a Swin-B backbone runs on the target pass and on one historical pass. The features are
  concatenated and go through an FPN and a Faster R-CNN head. The historical pass is there "to help distinguish
  vessels from fixed infrastructure".
- **Inputs:**
  - **VV + VH**, raw GRD (their data source is the AWS raw GRD bucket), float32, normalised as **DN / 250,
    clipped to [0, 4]**;
  - **UTM at 10 m** (`RESOLUTION = 10` in `predict_pipeline.py`), from GCPs with `gcp_transform_method: tps`, cubic
    resampling;
  - one historical pass with the **same orbit direction**, about 60 days earlier;
  - 512 px patches with 0.1 overlap, NMS at 10 px, default score threshold 0.9.

  No bathymetry, wind or land mask goes into the model. After detection, the pipeline drops detections within 50 m
  of the Satlas marine-infrastructure points. The source does not say how the model treats land.
- **Fit for us:** this is the closest match of any candidate. Our cache already has DN amplitude, VV and VH,
  UTM 10 m and TPS on GCPs. Two differences: we resample bilinear (they use cubic), and we shift the GCPs to sea
  height (they do not, as far as I can see). For the historical input we can take the same orbit, which is better
  than "same direction".
- **Glue code:** the shipped `predict` command with local files reads raw GRD TIFFs that have GCPs (radar
  geometry). It would not accept our resampled grid without changes. The simplest route bypasses the pipeline:
  1. build the model from `config_1hist.yaml`;
  2. load the checkpoint;
  3. feed `[vv, vh, vv_hist, vh_hist] / 250`, clipped to 0–4, in 512 px patches;
  4. apply 10 px NMS;
  5. map pixels to lon/lat with `aoi.pixel_to_lonlat`.

  Estimated at about 100–150 lines, plus a test on one pass. Packages to install: torch (CPU), torchvision,
  `rslearn` (≥ 0.1.16) and its dependencies, including lightning. I did not check that rslearn installs on Windows.
- **Runtime (estimate):** our grid gives about 4 × 4 = 16 patches per pass. Two Swin-B forward passes at 512 px
  on a 4-core i5-7400T is roughly 1–3 s per patch, so about 0.5 min per pass and **3–10 h for 671 passes**
  (unverified). Cropping to the zones' bounding box cuts this.
- **Weak spots:**
  - The training regions are not documented in what I read. Whether it covers the Caspian, or harbours, is
    **unverified**.
  - The history channel targets fixed objects. A ship lying at the same berth in both passes may be suppressed:
    the same blind spot as our 25th-percentile background, though not the same mechanism. In the roadstead this
    matters little.
  - It is not fully independent of us: it uses the same pre-processing family (DN, TPS, UTM 10 m). It is
    independent in its labels and method (learned, not a threshold).
  - The checkpoint is a pickle. Load it in a separate process. Try `torch.load(weights_only=True)` first; check
    the size and MD5 (GCS header `md5=fnbrEjjIcSuuFTbzscZZQw==`) before loading.

### 2.2 xView3 first place — BloodAxe CircleNet

- **Source:**
  - https://github.com/BloodAxe/xView3-The-First-Place-Solution (Eugene Khvedchenya); DIU mirror
    https://github.com/DIUx-xView/xView3_first_place;
  - weights in release `1.0`.
- **Licences:**
  - code: **MIT** (GitHub API);
  - weights: **no licence stated**. They were trained on xView3-SAR data, and I could not verify the xView3
    dataset licence. Treat commercial use as **unclear** until DIU/GFW terms are read.
- **Weights:** 12 `.pth` files (**pickle**), plus one TorchScript archive.

  | Model | Files | Size each |
  |---|---|---|
  | EfficientNet-B4 U-Net | 4 folds | 79,101,113 bytes (75.4 MiB) |
  | EfficientNetV2-S U-Net | 4 folds | 117.1 MiB |
  | EfficientNet-B5 U-Net | 4 folds | 116.1 MiB |
  | `traced_ensemble.jit` (TorchScript, all 12 models) | 1 file | 1,244.4 MiB |

  A single B4 fold is enough for a second opinion. The full ensemble takes "up to 12 minutes per scene" on GPU
  (README).
- **Inputs:**
  - 2 channels **[VH, VV]** in **dB** (xView3 GeoTIFFs: SNAP-derived backscatter in dB, UTM, 10 m);
  - normalised with a sigmoid, midpoint −20 dB, temperature 0.18;
  - no-data filled with 0;
  - tiles of 2048 px with step 1536; left-right flip TTA.

  Bathymetry, wind and ice were tried and dropped. There is no land mask: land saturates in the normalisation.
  Near-shore objects were balanced in sampling.
- **Fit for us:** our DN must first become sigma0 in dB.
  - This needs the per-scene calibration look-up table (sigmaNought) from the product annotation. Whether
    Planetary Computer items expose the calibration XML as an asset is **unverified**.
  - xView3 data also had thermal-noise removal. Without it, the VH noise floor differs.
  - A cheaper approximation: shift our dB so that open water matches typical xView3 sea values. This is untested
    and weak.

  Pixel size (10 m) and projection (UTM) match. Glue code: about 150 lines. It needs `pytorch_toolbelt` and
  `timm`-style encoders from the repo, or loading of one fold's state_dict into the repo's model class.
- **Runtime (estimate):** one B4 fold on one 2048 px tile (our grid padded) with flip TTA: a few seconds to tens of
  seconds per pass on our CPU, so **under about 3 h for 671 passes** (unverified).
- **Weak spots:**
  - xView3 scenes are mostly open water and coasts of Europe and West Africa, scored with a 2 km shore tolerance.
    Labels near shore are sparse and partly from AIS. Inside a dredged basin next to quays and cranes, expect false
    positives on quay structures and misses for ships alongside.
  - In the open roadstead it should behave well.
  - Calibration mismatch is the biggest risk.

### 2.3 Ai2 vessel-detection-sentinels (older Skylight model)

- **Source:** https://github.com/allenai/vessel-detection-sentinels (archived, read-only).
- **Licences:** code Apache-2.0. The weights sit in the repo as Git LFS files with no separate weights licence, so
  they are presumably covered by the repo licence (my reading, **unverified**).
- **Weights:** both are **pickle** `.pth` files (from the LFS pointers).
  - detector `data/model_artifacts/sentinel-1/frcnn_cmp2/3dff445/best.pth`: 121,693,810 bytes;
  - attribute model `attr/c34aa37/best.pth`: 96,460,157 bytes (optional).
- **Inputs:**
  - raw GRD measurement TIFF, cast to uint8 by clipping DN to 0–255;
  - warped to **EPSG:3857 at zoom 13**: 9.55 m Web-Mercator pixels, about 7.3 m on the ground at 40° N;
  - 6 channels: VH, VV of the target plus two historical passes;
  - windows of 2048 px with 400 px padding; confidence 0.9; NMS 10 px.
- **Fit for us:** our DN values fit. The grid would need reprojection to EPSG:3857 at about 1.37 × upsampling, plus
  two history passes, which we have.
- **Runtime:** the README gives 2,100 s per full scene on a CPU (on a machine with an RTX 2070, GPU disabled). Our
  crop is a small fraction of a scene, so roughly tens of seconds per pass (estimate).
- **Weak spots:** superseded by 2.1 and archived. The 0–255 clip saturates bright ships. Same unknowns about
  training coverage as 2.1.

## 3. Checked and set aside

- **Global Fishing Watch, Paolo et al. 2024** (https://github.com/GlobalFishingWatch/paper-industrial-activity):
  - **Licence:** dual licence, Apache-2.0 and **CC BY-NC 4.0 ("Noncommercial Use Only")**.
  - **Detector:** `detector/` is a **classical CFAR detector in Google Earth Engine**, not a neural network.
    Example parameters: `thresholdx=22`, `resolution=20`, `window_inner=140`, `window_outer=240`.
  - **Neural nets:** `nnets/` (TensorFlow) holds classifiers on detection thumbnails (vessel vs noise plus length,
    on 80 × 80 px dual-channel chips; infrastructure). They are not detectors.
  - **Weights:** **no trained weights published.** No repo release; neither figshare record (24309469, 24309475)
    lists model files.
  - **Data:** the training data is on figshare under CC BY 4.0 (`detection_tiles.zip` 136.3 MB,
    `infra_tiles.zip` 1,558.8 MB, `feature_tiles.zip` 17,703.6 MB). Usable to train our own classifier later. That
    is not a ready-made detector.
  - A port of their CFAR would be a third threshold detector, hardly independent of ours. It also needs Earth
    Engine, Cloud Storage and BigQuery.
- **ESA SNAP Ocean Tools (Ship Detection / Object Detection):**
  - classical adaptive-threshold detector; needs calibrated sigma0 and a land mask; no ML weights;
  - needs a full SNAP install (large) and full GRD products, which we do not have on disk;
  - SNAP is GPL-3.0 to my knowledge (**unverified here**);
  - methodologically too close to our own detector to count as independent.
- **SARFish** (https://github.com/DIUx-xView/SARFish): a dataset (SLC + GRD, built on xView3 labels) and a
  challenge. Apache-2.0 badge on the code, with separate dataset terms. No reference detector weights found.
- **Hugging Face:**
  - Searches for "sar ship", "sar vessel", "sentinel-1 ship", "hrsid" and "ssdd" found only small personal
    uploads with 0–19 downloads, mostly YOLOv8 or RetinaNet trained on SSDD or HRSID chips. Examples:
    `hewitleo/sar-ship-detection-yolov8` (Apache-2.0 tag), `MeWan2808/yolov8n-sar-vessel-detection` (MIT tag),
    `PUSHPENDAR/hrsid-ship-detection` (Apache-2.0 tag), and `roth1414/SAR-VesselBench` (licence "other").
  - These models were trained on 8-bit image chips with undocumented scaling, mixed sensors (HRSID includes
    TerraSAR-X) and other pixel sizes. Ultralytics YOLOv8 itself is AGPL-3.0.
  - Not credible as a reference. I did not open the model cards one by one.
- **"SARfish" (MJCruickshank):** a work-in-progress Faster R-CNN trained on LS-SSDD-v1.0, VH only. No licence seen.
  Not pursued.

## 4. Recommendation

Use **option 1, the Ai2 rslearn Sentinel-1 vessel detector**, detection model only.
- It is the only candidate with an explicit Apache-2.0 licence on the weights.
- It is maintained.
- It takes exactly what we have cached: raw DN, VV+VH, UTM 10 m. So no calibration step adds its own error.
- Our same-orbit stacks give it the historical pass it needs.

Use it as a check on the **roadstead** first: compare blob by blob within about 50 m on the same passes. In the
basin, read its output as a second opinion only. No candidate was trained for ships alongside quays.

If a learned detector with a different training lineage is also wanted, add **option 2 (one BloodAxe B4 fold)**
later. Do so only after (a) the xView3 data and weights terms are confirmed for our use, and (b) DN-to-sigma0
calibration is solved.

First step after approval: run option 1 on about 5 passes from different years and orbits. Measure the time per
pass and look at the overlap before running all 671.

## 5. Files to approve for download (option 1)

| What | Source URL | Size | Needed |
|---|---|---|---|
| Detector checkpoint `best.ckpt` | https://storage.googleapis.com/ai2-rslearn-projects-data/projects/20260626_num_historical/data_20250521_model_20250530_satlaspretrain_unfreeze4_13_1hist/best.ckpt | 1,262,487,287 bytes (GCS md5 `fnbrEjjIcSuuFTbzscZZQw==`) | yes |
| Model code `rslearn_projects` (git clone, code only, for `rslp.sentinel1_vessels`) | https://github.com/allenai/rslearn_projects | not measured (code repo) | yes |
| Python packages into `.venv`: `torch` (CPU wheel), `torchvision`, `rslearn>=0.1.16` and its dependencies (lightning and others) | PyPI and download.pytorch.org | not measured; run a dry install list first | yes |
| Marine-infrastructure filter `latest.geojson` | https://storage.googleapis.com/satlas-explorer-public/outputs/marine/latest.geojson | about 6.9 MiB | optional |
| Attribute model `best.ckpt` | https://storage.googleapis.com/ai2-rslearn-projects-data/projects/2026_09_17_vessel_attribute_l1/sentinel1_l1/best.ckpt | about 1.10 GiB | no |

If option 2 is approved later, the one file needed is
`211117_10_52_b4_unet_s2_leaky_valid_4fold_rfl_soft_bce_mse_regularized_flips_light_medium_fold0.pth`,
79,101,113 bytes, from
https://github.com/BloodAxe/xView3-The-First-Place-Solution/releases/download/1.0/211117_10_52_b4_unet_s2_leaky_valid_4fold_rfl_soft_bce_mse_regularized_flips_light_medium_fold0.pth.
It also needs the repo code (MIT) and `pytorch_toolbelt`.

## 6. Unverified, to check before relying on it

- The licence of the xView3-SAR dataset, and whether the winners' weights inherit it.
- Whether the Ai2 training data covers the Caspian Sea or harbour interiors.
- Every CPU runtime figure above, except the Ai2 README's 2,100 s per full scene.
- Whether `rslearn` installs cleanly on Windows with Python 3.12.
- Whether the Ai2 checkpoint loads with `torch.load(weights_only=True)`.
- Whether Planetary Computer GRD items carry calibration XML, which option 2 would need.
- The SNAP licence.
