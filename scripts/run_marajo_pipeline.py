#!/usr/bin/env python3
import argparse
from pathlib import Path
from typing import Optional

import geopandas as gpd
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import rasterio
from rasterio.features import geometry_mask
from rasterio.warp import Resampling, reproject
from rasterio.windows import from_bounds
from skimage.filters import gaussian

ROOT = Path(".")
EXPORTS = ROOT / "data" / "exports"
CANDS_RT = ROOT / "data" / "candidates"
FIGS_RT = ROOT / "figures"


def need(p: Path, msg: str):
    if not p.exists():
        raise FileNotFoundError(f"Missing {p} — {msg}")


def deg_buffer(bbox, buffer_m):
    d = buffer_m / 111_320.0
    xmin, ymin, xmax, ymax = bbox
    return (xmin - d, ymin - d, xmax + d, ymax + d)


def window_extent(ds: rasterio.io.DatasetReader, win):
    left, top = ds.transform * (win.col_off, win.row_off)
    right, bottom = ds.transform * (win.col_off + win.width, win.row_off + win.height)
    return (left, right, bottom, top)


def step_select_topN(coarse_gj: Path, topN: int, out_dir: Path):
    print(f"[1/3] Selecting top-{topN} hotspots from {coarse_gj.name}")
    gdf = gpd.read_file(coarse_gj)
    if gdf.empty:
        raise SystemExit("Hotspot GeoJSON is empty.")
    if "area_ha" in gdf.columns:
        gdf = gdf.sort_values("area_ha", ascending=False)
    else:
        # compute area in hectares via Web Mercator
        gm = gdf.to_crs(3857)
        gdf = gdf.assign(area_ha=gm.area / 10_000.0).sort_values("area_ha", ascending=False)
    out_dir.mkdir(parents=True, exist_ok=True)
    top = gdf.head(topN).reset_index(drop=True)
    (out_dir / "hotspots_topN.geojson").write_text(top.to_json())
    top[["area_ha"]].to_csv(out_dir / "hotspots_topN.csv", index=False)
    print("  ->", out_dir / "hotspots_topN.geojson")
    print("  ->", out_dir / "hotspots_topN.csv")
    return top


def step_score(top, s1_db: Path, dem30: Path, out_csv: Path):
    print(f"[2/3] Scoring hydro-plausibility using {s1_db.name} + {dem30.name}")
    with rasterio.open(s1_db) as rs1:
        s1, s1_tr, s1_crs, s1_sh = rs1.read(1).astype("float32"), rs1.transform, rs1.crs, rs1.shape
    with rasterio.open(dem30) as rd:
        dem, dem_tr, dem_crs, dem_sh = rd.read(1).astype("float32"), rd.transform, rd.crs, rd.shape
    if (dem_sh != s1_sh) or (dem_crs != s1_crs) or (dem_tr != s1_tr):
        dem_res = np.empty(s1_sh, dtype="float32")
        reproject(
            source=dem,
            destination=dem_res,
            src_transform=dem_tr,
            src_crs=dem_crs,
            dst_transform=s1_tr,
            dst_crs=s1_crs,
            resampling=Resampling.bilinear,
            num_threads=2,
        )
    else:
        dem_res = dem
    dem_blur = gaussian(dem_res, sigma=5, preserve_range=True)
    rel = dem_res - dem_blur
    rel[~np.isfinite(rel)] = np.nan
    rows = []
    for i, r in top.reset_index(drop=True).iterrows():
        mask = geometry_mask(
            [r.geometry.__geo_interface__], out_shape=s1_sh, transform=s1_tr, invert=True
        )
        pix = int(mask.sum())
        if pix == 0:
            rows.append(
                {"idx": i + 1, "area_ha": float(r.get("area_ha", np.nan)), "pix": 0, "frac_ok": 0.0}
            )
            continue
        ok = (s1 > 0.5) & (rel <= 5.0) & mask & np.isfinite(s1) & np.isfinite(rel)
        rows.append(
            {
                "idx": i + 1,
                "area_ha": float(r.get("area_ha", np.nan)),
                "pix": pix,
                "frac_ok": float(ok.sum()) / float(pix),
            }
        )
    df = pd.DataFrame(rows).sort_values("frac_ok", ascending=False)
    out_csv.parent.mkdir(parents=True, exist_ok=True)
    df.to_csv(out_csv, index=False)
    print("  ->", out_csv)
    print(df.to_string(index=False))
    return df


def step_render_figs(
    top, alos_rgb: Optional[Path], s1_rgb: Optional[Path], s1_db: Path, buffer_m: int, out_dir: Path
):
    print(f"[3/3] Rendering overview PNGs (buffer ≈ {buffer_m} m)")
    out_dir.mkdir(parents=True, exist_ok=True)
    rdA = None
    if alos_rgb and alos_rgb.exists():
        try:
            rdA = rasterio.open(alos_rgb)
        except Exception:
            rdA = None
    rdSRGB = rasterio.open(s1_rgb) if (s1_rgb and s1_rgb.exists()) else None
    rdSDB = rasterio.open(s1_db)

    for i, r in top.reset_index(drop=True).iterrows():
        bb = deg_buffer(r.geometry.bounds, buffer_m)
        fig, ax = plt.subplots(1, 2, figsize=(8.5, 4.5), dpi=150)

        # ALOS-2 RGB (left)
        if rdA is not None and rdA.count >= 3:
            w = from_bounds(*bb, transform=rdA.transform)
            left, rgt, b, t = window_extent(rdA, w)
            A = rdA.read([1, 2, 3], window=w).astype("float32")
            A = np.clip(A / (np.percentile(A, 99) + 1e-6), 0, 1)
            ax[0].imshow(np.transpose(A, (1, 2, 0)), extent=(left, rgt, b, t))
            ax[0].set_title("ALOS-2 Δ (colorized)")
        else:
            ax[0].text(
                0.5,
                0.5,
                "ALOS-2 Δ not available",
                transform=ax[0].transAxes,
                ha="center",
                va="center",
            )
            ax[0].set_title("ALOS-2 Δ")

        # S1 RGB or dB (right)
        drawn = False
        if rdSRGB is not None and rdSRGB.count >= 3:
            w = from_bounds(*bb, transform=rdSRGB.transform)
            left, rgt, b, t = window_extent(rdSRGB, w)
            S = rdSRGB.read([1, 2, 3], window=w).astype("float32")
            S = np.clip(S / (np.percentile(S, 99) + 1e-6), 0, 1)
            ax[1].imshow(np.transpose(S, (1, 2, 0)), extent=(left, rgt, b, t))
            ax[1].set_title("Sentinel-1 VV Δ (RGB)")
            drawn = True
        if not drawn:
            w = from_bounds(*bb, transform=rdSDB.transform)
            left, rgt, b, t = window_extent(rdSDB, w)
            s1 = rdSDB.read(1, window=w).astype("float32")
            ax[1].imshow(
                np.clip((s1 + 3) / 6, 0, 1), extent=(left, rgt, b, t), cmap="RdBu_r", vmin=0, vmax=1
            )
            ax[1].set_title("Sentinel-1 VV Δ (dB)")

        for a in ax:
            a.set_xlabel("lon")
            a.set_ylabel("lat")
        area = float(r.get("area_ha", float("nan")))
        fig.suptitle(f"Candidate rank {i+1} (≈{area:.2f} ha)")
        fig.tight_layout()
        out = out_dir / f"marajo-hot-01{i+1:02d}_overview.png"
        fig.savefig(out, bbox_inches="tight")
        plt.close(fig)
        print("  ->", out)

    if rdA is not None:
        rdA.close()
    if rdSRGB is not None:
        rdSRGB.close()
    rdSDB.close()


def main():
    ap = argparse.ArgumentParser(description="AOI-scoped pipeline: select→score→render")
    ap.add_argument(
        "--prefix", type=str, default="marajo", help="AOI prefix (e.g., marajo, santarem, tapajos)"
    )
    ap.add_argument("--topN", type=int, default=5)
    ap.add_argument("--buffer_m", type=int, default=6000)
    args = ap.parse_args()
    px = args.prefix

    # Inputs expected as data/exports/<prefix>_*
    coarse_gj = EXPORTS / f"{px}_S1_hotspots_coarse.geojson"
    s1_db = EXPORTS / f"{px}_S1VV_delta_db.tif"
    dem30 = EXPORTS / f"{px}_DEM_30m.tif"
    alos_rgb = EXPORTS / f"{px}_ALOS2_delta_rgb.tif"
    s1_rgb = EXPORTS / f"{px}_S1VV_delta_rgb.tif"

    need(coarse_gj, f"Export from Earth Engine as {px}_S1_hotspots_coarse.geojson")
    need(s1_db, f"Export {px}_S1VV_delta_db.tif")
    need(dem30, f"Export {px}_DEM_30m.tif")

    # Outputs to data/candidates/<prefix>/ and figures/<prefix>/
    cand_dir = CANDS_RT / px
    figs_dir = FIGS_RT / px

    top = step_select_topN(coarse_gj, args.topN, cand_dir)
    _ = step_score(top, s1_db=s1_db, dem30=dem30, out_csv=cand_dir / "hotspots_scores.csv")
    step_render_figs(
        top,
        alos_rgb=alos_rgb if alos_rgb.exists() else None,
        s1_rgb=s1_rgb if s1_rgb.exists() else None,
        s1_db=s1_db,
        buffer_m=args.buffer_m,
        out_dir=figs_dir,
    )


if __name__ == "__main__":
    main()
