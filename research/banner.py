"""docs/banner.png: title banner over the real mean Sentinel-1 VV image of Alat (not an illustration).

Needs data/sar/cache/mean_vv_orb28.npy (written by `python -m mcm.sar.run`). Windows fonts.
"""
import numpy as np
from PIL import Image, ImageDraw, ImageFont

db = np.load("data/sar/cache/mean_vv_orb28.npy")[230:700, :]  # 10 m grid, port in the upper left
lo, hi = np.nanpercentile(db, 20) - 2, np.nanpercentile(db, 99.7)
g = np.clip((np.nan_to_num(db, nan=lo) - lo) / (hi - lo), 0, 1) ** 0.8
rgb = np.stack([g * 150 + 8, g * 200 + 20, g * 215 + 38], axis=-1)  # steel-blue tint
W, H = 1600, 500
im = Image.fromarray(rgb.astype("uint8")).resize((W, H), Image.LANCZOS).convert("RGBA")

shade = np.zeros((H, W, 4), "uint8")  # darken the right side, where the text sits
shade[..., :3] = (6, 14, 28)
shade[..., 3] = (np.clip((np.arange(W) - 450) / 500, 0, 1) * 215).astype("uint8")[None, :]
im = Image.alpha_composite(im, Image.fromarray(shade))

F = "C:/Windows/Fonts/"
d = ImageDraw.Draw(im)
x = 700
d.text((x, 150), "Middle Corridor Monitor", font=ImageFont.truetype(F + "segoeuib.ttf", 68), fill="white")
d.text((x, 245), "An open, checkable look at cargo crossing the Caspian",
       font=ImageFont.truetype(F + "segoeui.ttf", 30), fill=(205, 222, 240))
d.text((x, 300), "Preliminary  ·  not peer reviewed", font=ImageFont.truetype(F + "segoeuisl.ttf", 24), fill=(240, 200, 90))
d.text((x, 455), "Background: mean Sentinel-1 radar image, Port of Baku at Alat, 2019–2026. "
                 "Contains modified Copernicus Sentinel data.",
       font=ImageFont.truetype(F + "segoeui.ttf", 15), fill=(160, 180, 200))
im.convert("RGB").save("docs/banner.png", optimize=True)
print("wrote docs/banner.png", im.size)
