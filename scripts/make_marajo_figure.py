#!/usr/bin/env python
from __future__ import annotations

import argparse
from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np
import tifffile as tiff
from PIL import Image
from skimage.morphology import binary_opening, disk, remove_small_objects
from skimage.transform import resize


def load_gray_db(path: Path) -> np.ndarray:
    arr = tiff.imread(str(path)).astype("float32")
    if arr.ndim == 3:
        arr = arr.squeeze()
    bad = ~np.isfinite(arr)
    if bad.any():
        arr[bad] = np.nan
    return arr


def load_rgb(path: Path) -> np.ndarray:
    im = Image.open(path)  # 8-bit RGB GeoTIFF
    return np.asarray(im)


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--in-dir", default="data/exports")
    ap.add_argument("--out-dir", default="figures")
    ap.add_argument("--alos2-db", default="marajo_ALOS2_delta_db.tif")
    ap.add_argument("--alos2-rgb", default="marajo_ALOS2_delta_rgb.tif")
    ap.add_argument("--s1-db", default="marajo_S1VV_delta_db.tif")
    ap.add_argument("--s1-rgb", default="marajo_S1VV_delta_rgb.tif")
    ap.add_argument("--s1-hot-thresh", type=float, default=1.0)
    args = ap.parse_args()

    in_dir = Path(args.in_dir)
    out_dir = Path(args.out_dir)
    out_dir.mkdir(parents=True, exist_ok=True)

    # Load rasters
    alos_db = load_gray_db(in_dir / args.alos2_db)
    s1_db = load_gray_db(in_dir / args.s1_db)
    alos_rgb = load_rgb(in_dir / args.alos2_rgb)
    s1_rgb = load_rgb(in_dir / args.s1_rgb)

    # Align S1 Δ to ALOS shape if needed
    if s1_db.shape != alos_db.shape:
        s1_db = resize(
            s1_db, alos_db.shape, order=1, anti_aliasing=False, preserve_range=True
        ).astype("float32")

    # Hotspots mask from S1 Δ (positive wet–dry change)
    hot = s1_db > args.s1_hot_thresh
    hot = binary_opening(hot, disk(1))
    hot = remove_small_objects(hot, min_size=200)

    # Overlay hot mask (red) on ALOS RGB
    ov = alos_rgb.astype("float32") / 255.0
    if ov.ndim == 2:
        ov = np.repeat(ov[..., None], 3, axis=2)
    red = np.zeros_like(ov)
    red[..., 0] = 1.0
    alpha = 0.35
    mask = hot.astype("float32")[..., None]
    ov_mix = ov * (1 - alpha * mask) + red * (alpha * mask)

    # Figure
    import matplotlib

    matplotlib.rcParams["figure.dpi"] = 150
    fig, ax = plt.subplots(1, 3, figsize=(14, 5))
    ax[0].imshow(alos_rgb)
    ax[0].set_title("ALOS-2 Δ (γ0 dB, colorized)")
    ax[0].axis("off")
    ax[1].imshow(s1_rgb)
    ax[1].set_title("Sentinel-1 VV Δ (colorized)")
    ax[1].axis("off")
    ax[2].imshow(ov_mix)
    ax[2].set_title("Overlay: ALOS-2 Δ + S1 hotspots")
    ax[2].axis("off")
    fig.suptitle("Marajó AOI — Seasonal Δ maps and S1 hotspots", y=0.98)
    fig.tight_layout()

    png = out_dir / "marajo_delta_overview.png"
    pdf = out_dir / "marajo_delta_overview.pdf"
    fig.savefig(png, bbox_inches="tight")
    fig.savefig(pdf, bbox_inches="tight")
    print(f"Wrote {png} and {pdf}")


if __name__ == "__main__":
    main()

