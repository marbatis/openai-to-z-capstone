from __future__ import annotations

import argparse
import json
import os
from pathlib import Path

import earthaccess
import geopandas as gpd
import h5py
import numpy as np
import pandas as pd
from shapely.geometry import Point, box
from zexplorer.data_id_logger import DataSource, log_evidence


def ring_from_bbox(b):
    # [(lon,lat) … closed ring]
    return [
        (b[0], b[1]),
        (b[2], b[1]),
        (b[2], b[3]),
        (b[0], b[3]),
        (b[0], b[1]),
    ]


def pad_bbox(b, pad_deg=0.5):
    return [b[0] - pad_deg, b[1] - pad_deg, b[2] + pad_deg, b[3] + pad_deg]


def search_gedi(bbox, start, end):
    ring = ring_from_bbox(bbox)
    # Try cloud, then DAAC; guard empty results each time
    for daac in (None, "ORNL_DAAC"):
        try:
            res = earthaccess.search_data(
                short_name="GEDI04_C",
                version="2",
                temporal=(start, end),
                polygon=ring,
                daac=daac,  # daac=None = auto/cloud
            )
            if res:
                return res
        except Exception as e:
            print("Search error (daac=%s): %s" % (daac, e))
    # Pad AOI and try DAAC once more
    b2 = pad_bbox(bbox, 0.5)
    ring2 = ring_from_bbox(b2)
    try:
        res = earthaccess.search_data(
            short_name="GEDI04_C",
            version="2",
            temporal=(start, end),
            polygon=ring2,
            daac="ORNL_DAAC",
        )
        if res:
            print("Found granules after padding AOI by 0.5°.")
            return res
    except Exception as e:
        print("Search error (padded, DAAC):", e)
    return []


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--aoi", default="config/aoi_marajo.json")
    ap.add_argument("--candidate-id", required=True)
    ap.add_argument("--outdir", default="data/gedi_l4c_marajo")
    ap.add_argument("--start", default="2019-04-01")
    ap.add_argument("--end", default="2025-12-31")
    ap.add_argument("--max-granules", type=int, default=6)
    args = ap.parse_args()

    # AOI
    if Path(args.aoi).exists():
        cfg = json.loads(Path(args.aoi).read_text())
        bbox = cfg["bbox"]
    else:
        bbox = [-50.0167, -1.3667, -49.1167, -0.4667]  # Marajó fallback
    aoi_poly = box(*bbox)
    latc = (bbox[1] + bbox[3]) / 2
    lonc = (bbox[0] + bbox[2]) / 2

    # Auth + search
    earthaccess.login()  # prompts once; cached in ~/.netrc
    results = search_gedi(bbox, args.start, args.end)
    if not results:
        print(
            "No GEDI04_C granules found near AOI. You can:\n"
            "- widen the dates (e.g., --start 2019-01-01 --end 2025-12-31), or\n"
            "- increase the AOI padding, or\n"
            "- use Sentinel-1 as the second independent method.\n"
            "Exiting without logging GEDI evidence."
        )
        return

    # Download a few
    out_dir = Path(args.outdir)
    out_dir.mkdir(parents=True, exist_ok=True)
    files = earthaccess.download(results[: args.max_granules], str(out_dir))
    print(f"Downloaded {len(files)} granules")

    # Extract WSCI/lat/lon
    rows = []
    for fp in files:
        try:
            with h5py.File(fp, "r") as h5:

                def walk(g, p=""):
                    for k in g.keys():
                        v = g[k]
                        pp = f"{p}/{k}" if p else k
                        if isinstance(v, h5py.Group):
                            yield from walk(v, pp)
                        elif isinstance(v, h5py.Dataset):
                            yield pp, v

                paths = {p for p, _ in walk(h5)}

                def pick(name):
                    for p in paths:
                        if p.endswith("/" + name) or p == name:
                            return p

                Wp = pick("WSCI")
                Lap = pick("lat") or pick("latitude")
                Lop = pick("lon") or pick("longitude")

                if not all([Wp, Lap, Lop]):
                    print("Skip (no WSCI/lat/lon):", os.path.basename(fp))
                    continue
                WSCI = np.array(h5[Wp][:])
                LAT = np.array(h5[Lap][:])
                LON = np.array(h5[Lop][:])

                for la, lo, w in zip(LAT, LON, WSCI):
                    if (
                        np.isfinite(la)
                        and np.isfinite(lo)
                        and Point(float(lo), float(la)).within(aoi_poly)
                    ):
                        rows.append(
                            {
                                "lat": float(la),
                                "lon": float(lo),
                                "WSCI": float(w),
                                "granule": os.path.basename(fp),
                            }
                        )
        except Exception as e:
            print("Skip file", os.path.basename(fp), e)

    df = pd.DataFrame(rows)
    out_geo = out_dir / "gedi_wsci_points.geojson"
    out_csv = out_dir / "gedi_wsci_points.csv"
    if not df.empty:
        gdf = gpd.GeoDataFrame(
            df,
            geometry=[Point(xy) for xy in zip(df["lon"], df["lat"])],
            crs="EPSG:4326",
        )
        gdf.to_file(out_geo, driver="GeoJSON")
        df.to_csv(out_csv, index=False)
        print("GEDI points:", len(df), "→", out_geo)
    else:
        print("Downloaded granules did not contain WSCI points within AOI.")

    # Log evidence (use downloaded granule names even if no WSCI points fell inside AOI)
    granules = ",".join(sorted({os.path.basename(f) for f in files})[:3])
    log_evidence(
        lat=latc,
        lon=lonc,
        candidate_id=args.candidate_id,
        bbox=bbox,
        sources=[
            DataSource(
                type="GEDI04_C v2 (WSCI)",
                id=f"granules:{granules}",
                url="https://gedi.umd.edu/gedi-l4c-footprint-level-waveform-structural-complexity-index-released/",
            )
        ],
        notes=(f"Independent evidence: GEDI L4C WSCI search {args.start}..{args.end} near AOI"),
    )
    print("Logged GEDI evidence line.")


if __name__ == "__main__":
    main()
