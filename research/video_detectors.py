"""docs/detectors.mp4 and docs/detectors.gif: the two radar detectors on real Sentinel-1 passes at Alat.

Left: the VV image of one pass (relative orbit 6, every third counted pass) with our detections and those of Ai2's
vessel model. Right: roadstead detections per pass by each detector, up to that pass. Real data only; both detectors
are unvalidated. Needs the pass cache (`python -m mcm.sar.fetch`), data/sar/detections.csv, detections_ai2.csv and
ffmpeg. `--test` writes one frame to docs/detectors_test.png instead.
"""
import contextlib
import io
import subprocess
import sys
from pathlib import Path

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from matplotlib.animation import FFMpegWriter

sys.path.insert(0, str(Path(__file__).parent))
import second_detector as sd  # noqa: E402
from mcm.sar import detect, fetch, run  # noqa: E402

ORBIT, STEP = 6, 3
_, sl, zr = run.zone_setup()
r0, c0 = int(sl[0].start), int(sl[1].start)
ours = pd.read_csv(run.DET_CSV)
ours = ours[~ours.fixed_object & ours.zone.isin(["basin", "roadstead"])]
ai2 = sd.ai2_counted(pd.read_csv(sd.OUT))
with contextlib.redirect_stdout(io.StringIO()):  # compare() prints every pass
    t = sd.compare()
t = t[t.zone == "roadstead"].merge(sd.counted_passes()[["scene_id", "t", "rel_orbit"]], on="scene_id").sort_values("t")
t = t[t.rel_orbit == ORBIT].reset_index(drop=True)
frames = list(range(0, len(t), STEP))

BG, FG, DIM, GOLD, BLUE = "#06101c", "white", "#9fb4c8", "#f0c85a", "#6fc3ff"
fig = plt.figure(figsize=(12.8, 7.2), dpi=100, facecolor=BG)
fig.text(0.04, 0.93, "Two detectors, one radar image", color=FG, fontsize=26, fontweight="bold")
fig.text(0.04, 0.885, "Port of Baku at Alat, Sentinel-1  ·  both detectors unvalidated  ·  preliminary, not peer reviewed", color=GOLD, fontsize=13)
fig.text(0.04, 0.03, "Contains modified Copernicus Sentinel data. Second detector: Allen Institute for AI, rslearn_projects (Apache-2.0).", color=DIM, fontsize=10)
ax_img = fig.add_axes([0.04, 0.12, 0.42, 0.72]); ax_img.axis("off")
im = ax_img.imshow(np.zeros(zr.shape), cmap="bone", vmin=0, vmax=1)
ax_img.contour(zr, levels=[0.5, 1.5], colors=[DIM, DIM], linewidths=0.6)
p_ai2, = ax_img.plot([], [], "o", ms=13, mfc="none", mec=BLUE, mew=1.4)
p_ours, = ax_img.plot([], [], "o", ms=4, color=GOLD, mec="black", mew=0.3)
date_txt = ax_img.text(0.97, 0.03, "", transform=ax_img.transAxes, color=FG, fontsize=20, fontweight="bold", ha="right", va="bottom",
                      bbox=dict(facecolor=BG, alpha=0.6, edgecolor="none"))
img_txt = fig.text(0.04, 0.085, "", color=FG, fontsize=11)
ax = fig.add_axes([0.54, 0.17, 0.42, 0.62], facecolor=BG)
ax.set_xlim(t.t.min(), t.t.max()); ax.set_ylim(0, max(t.ours.max(), t.ai2.max()) * 1.25)
ax.tick_params(colors=DIM); [s.set_color(DIM) for s in ax.spines.values()]; ax.spines[["top", "right"]].set_visible(False)
ax.set_title(f"Roadstead detections per pass (relative orbit {ORBIT})", color=FG, fontsize=12, loc="left")
l_ours, = ax.plot([], [], color=GOLD, lw=2.2, label="Our detector (brightness against the usual image)")
l_ai2, = ax.plot([], [], color=BLUE, lw=1.4, label="Ai2 vessel model (neural network)")
ax.legend(loc="upper left", frameon=False, labelcolor=FG, fontsize=10)
val_txt = fig.text(0.54, 0.085, "", color=FG, fontsize=11)


def draw(i):
    r = t.iloc[i]
    vv = detect.smooth_db(np.load(fetch.SCENE_CACHE / f"{r.scene_id}.npz")["vv"])[sl]
    lo, hi = np.nanpercentile(vv, 2), np.nanpercentile(vv, 99.7)
    im.set_data(np.clip((np.nan_to_num(vv, nan=lo) - lo) / (hi - lo), 0, 1))
    o, a = ours[ours.scene_id == r.scene_id], ai2[ai2.scene_id == r.scene_id]
    p_ours.set_data(o.col - c0, o.row - r0); p_ai2.set_data(a.col - c0, a.row - r0)
    date_txt.set_text(f"{r.t:%d %b %Y}")
    img_txt.set_text("Gold dot: our detector.  Blue ring: Ai2 model.  Outlines: basin and roadstead.")
    l_ours.set_data(t.t[: i + 1], t.ours[: i + 1]); l_ai2.set_data(t.t[: i + 1], t.ai2[: i + 1])
    val_txt.set_text(f"This pass, roadstead: ours {r.ours}, Ai2 {r.ai2}, matched within 50 m: {r.ours_matched}.")


if "--test" in sys.argv:
    draw(frames[len(frames) * 2 // 3]); fig.savefig("docs/detectors_test.png", facecolor=BG); sys.exit()

w = FFMpegWriter(fps=5, codec="libx264", extra_args=["-pix_fmt", "yuv420p", "-crf", "23"])
with w.saving(fig, "docs/detectors.mp4", dpi=100):
    for i in frames + [frames[-1]] * 10:  # hold the last pass for 2 s
        draw(i); w.grab_frame(facecolor=BG)
subprocess.run(["ffmpeg", "-y", "-loglevel", "error", "-i", "docs/detectors.mp4", "-vf",
                "fps=5,scale=800:-1:flags=lanczos,split[a][b];[a]palettegen=max_colors=64[p];[b][p]paletteuse=dither=none",
                "docs/detectors.gif"], check=True)
print("wrote docs/detectors.mp4 and docs/detectors.gif,", len(frames), "passes")
