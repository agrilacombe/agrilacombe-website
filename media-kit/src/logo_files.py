"""Logo files for the media kit, all made from the farm's original logo.

  original          the file as-is (public/images/agrilacombe_logo.png)
  fond-transparent  same logo with the cream background removed, for light backgrounds
  noir-et-blanc     greyscale of the transparent version
"""

import shutil
from pathlib import Path

import numpy as np
from PIL import Image
from scipy import ndimage


def remove_background(src):
    """Colour-to-alpha against the cream background (GIMP's algorithm).

    Each pixel gets the smallest alpha that reproduces it over the background,
    so soft painted edges stay soft and the result over cream is the original.
    """
    im = np.asarray(Image.open(src).convert("RGB")).astype(float)
    border = np.concatenate([im[:8].reshape(-1, 3), im[-8:].reshape(-1, 3),
                             im[:, :8].reshape(-1, 3), im[:, -8:].reshape(-1, 3)])
    bg = np.median(border, axis=0)
    d = im - bg
    lighter = np.where(d > 0, d / (255 - bg + 1e-9), 0).max(axis=2)
    darker = np.where(d < 0, -d / (bg + 1e-9), 0).max(axis=2)
    # The cream is close to white, so faint paper grain slightly lighter than it would
    # come out nearly opaque. In the background connected to the edges, only darkening
    # counts; light details inside the drawing (the onion highlight) are untouched.
    near_bg = np.abs(d).max(axis=2) < 14
    labels, _ = ndimage.label(near_bg)
    edge = np.unique(np.concatenate([labels[0], labels[-1], labels[:, 0], labels[:, -1]]))
    outside = np.isin(labels, edge[edge > 0])
    alpha = np.where(outside, darker, np.maximum(lighter, darker))
    alpha = np.clip((alpha - 0.03) / 0.97, 0, 1)
    fg = np.clip(bg + d / np.maximum(alpha[..., None], 1e-6), 0, 255)
    out = Image.fromarray(np.dstack([fg, alpha * 255]).astype(np.uint8), "RGBA")
    left, top, right, bottom = out.getchannel("A").point(lambda a: 255 if a > 8 else 0).getbbox()
    pad = round(0.03 * max(right - left, bottom - top))
    return out.crop((left - pad, top - pad, right + pad, bottom + pad))


def build(src, out):
    """Write the three logo files into `out`, return {key: path}."""
    out.mkdir(parents=True, exist_ok=True)
    files = {
        "original": out / "AgriLacombe_Logo_original.png",
        "transparent": out / "AgriLacombe_Logo_fond-transparent.png",
        "nb": out / "AgriLacombe_Logo_noir-et-blanc.png",
    }
    shutil.copy(src, files["original"])
    transparent = remove_background(src)
    transparent.save(files["transparent"], optimize=True)
    grey = transparent.convert("LA")
    grey.save(files["nb"], optimize=True)
    return files
