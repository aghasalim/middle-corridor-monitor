"""docs/monitor.mp4 and docs/monitor.gif: one frame per month, January 2019 to the last month of the index.

Left: mean Sentinel-1 radar image of the Port of Baku at Alat with that month's radar detections (unlabelled bright
blobs, not confirmed ships; objects flagged as fixed are left out). Right: the index up to that month.
Real data only. Needs data/sar/cache/mean_vv_orb28.npy and data/sar/detections.csv (`python -m mcm.sar.run`), outputs/tables/index_monthly.csv
(`python -m mcm.build --offline`) and ffmpeg on the PATH. `--test` writes one frame to docs/monitor_test.png instead.
"""
import subprocess
import sys

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from matplotlib.animation import FFMpegWriter

import mcm  # noqa: F401  (registers the Inter font)

m = pd.read_csv("outputs/tables/index_monthly.csv", parse_dates=["month"])
R0, R1, C0, C1 = 250, 1250, 250, 1350  # crop of the 10 m grid that holds the port basin and the roadstead
ref = np.load("data/sar/cache/mean_vv_orb28.npy")[R0:R1, C0:C1]
lo, hi = np.nanpercentile(ref, 20) - 2, np.nanpercentile(ref, 99.7)
det = pd.read_csv("data/sar/detections.csv", parse_dates=["datetime"])
det = det[~det.fixed_object & det.row.between(R0, R1) & det.col.between(C0, C1)]
det_month = det.datetime.dt.strftime("%Y-%m")


def stretch(db):
    return np.clip((np.nan_to_num(db, nan=lo) - lo) / (hi - lo), 0, 1) ** 0.8


BG, FG, DIM, GOLD, BLUE = "#06101c", "white", "#9fb4c8", "#f0c85a", "#6fc3ff"
fig = plt.figure(figsize=(12.8, 7.2), dpi=100, facecolor=BG)
fig.text(0.04, 0.93, "Middle Corridor Monitor", color=FG, fontsize=26, fontweight="bold")
fig.text(0.04, 0.885, "Cargo ship calls on the Caspian, from open data  ·  preliminary, not peer reviewed", color=GOLD, fontsize=13)
fig.text(0.04, 0.03, "Sources: Kpler; UN Global Platform; IMF PortWatch (portwatch.imf.org). Contains modified Copernicus Sentinel data.",
         color=DIM, fontsize=10)
ax_img = fig.add_axes([0.04, 0.12, 0.42, 0.70]); ax_img.axis("off")
im = ax_img.imshow(stretch(ref), cmap="bone", vmin=0, vmax=1)
dots, = ax_img.plot([], [], "o", ms=5, color=GOLD, mec="black", mew=0.4)
year_txt = ax_img.text(0.03, 0.97, "", transform=ax_img.transAxes, color=FG, fontsize=22, fontweight="bold", va="top")
img_txt = fig.text(0.04, 0.085, "", color=FG, fontsize=11)
ax = fig.add_axes([0.54, 0.17, 0.42, 0.62], facecolor=BG)
ax.set_xlim(m.month.min(), m.month.max()); ax.set_ylim(0, max(m.caspian_roro_calls_index.max(), m.caspian_dry_calls_index.max()) * 1.3)
ax.axhline(100, color=DIM, lw=0.8, ls=":")
ax.tick_params(colors=DIM); [s.set_color(DIM) for s in ax.spines.values()]; ax.spines[["top", "right"]].set_visible(False)
ax.set_title("Port calls at Baku, Aktau and Turkmenbashi (2019 monthly mean = 100)", color=FG, fontsize=12, loc="left")
l_dry, = ax.plot([], [], color=BLUE, lw=2.4, label="Non-tanker calls (headline index)")
l_ro, = ax.plot([], [], color=GOLD, lw=1.6, label="Ro-Ro calls (step in 2021 is not explained)")
ax.legend(loc="upper left", frameon=False, labelcolor=FG, fontsize=10)
val_txt = fig.text(0.54, 0.085, "", color=FG, fontsize=11)


def draw(i):
    r = m.iloc[i]
    d = det[det_month == f"{r.month:%Y-%m}"]
    dots.set_data(d.col - C0, d.row - R0); year_txt.set_text(f"{r.month:%b %Y}")
    img_txt.set_text(f"Radar, Port of Baku at Alat: {len(d)} bright objects (not confirmed ships)")
    l_dry.set_data(m.month[: i + 1], m.caspian_dry_calls_index[: i + 1])
    l_ro.set_data(m.month[: i + 1], m.caspian_roro_calls_index[: i + 1])
    val_txt.set_text(f"{r.month:%B %Y}: headline index {r.caspian_dry_calls_index:.0f}. A count of ship calls, not of cargo.")


if "--test" in sys.argv:
    draw(len(m) - 1); fig.savefig("docs/monitor_test.png", facecolor=BG); sys.exit()

w = FFMpegWriter(fps=8, codec="libx264", extra_args=["-pix_fmt", "yuv420p", "-crf", "20"])
with w.saving(fig, "docs/monitor.mp4", dpi=100):
    for i in list(range(len(m))) + [len(m) - 1] * 24:  # hold the last month for 3 s
        draw(i); w.grab_frame(facecolor=BG)
subprocess.run(["ffmpeg", "-y", "-loglevel", "error", "-i", "docs/monitor.mp4", "-vf",
                "fps=8,scale=960:-1:flags=lanczos,split[a][b];[a]palettegen=max_colors=96[p];[b][p]paletteuse",
                "docs/monitor.gif"], check=True)
print("wrote docs/monitor.mp4 and docs/monitor.gif,", len(m), "months")
