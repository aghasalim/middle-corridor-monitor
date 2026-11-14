"""Chart font: Inter where the user has it installed (Windows per-user fonts), otherwise matplotlib's default."""
import glob
import os

import matplotlib
from matplotlib import font_manager

_inter = glob.glob(os.path.expandvars("%LOCALAPPDATA%/Microsoft/Windows/Fonts/Inter-*.ttf"))
for _f in _inter:
    font_manager.fontManager.addfont(_f)
if _inter:
    matplotlib.rcParams["font.family"] = ["Inter", "DejaVu Sans"]
