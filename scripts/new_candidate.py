#!/usr/bin/env python
from __future__ import annotations
import argparse
from zexplorer.data_id_logger import log_evidence, DataSource, ModelInfo
from zexplorer.geoutils import bbox_from_center

def main():
    ap = argparse.ArgumentParser(description="Log a new candidate site/evidence line")
    ap.add_argument("--lat", type=float, required=True)
    ap.add_argument("--lon", type=float, required=True)
    ap.add_argument("--candidate-id", type=str, default="cand-0001")
    ap.add_argument("--buffer-m", type=float, default=50_000)  # 100x100km default AOI
    ap.add_argument("--dataset-type", type=str, required=True, help="e.g., Sentinel-2, LiDAR, GEDI")
    ap.add_argument("--dataset-id", type=str, required=True, help="Scene/tile/DOI/ID")
    ap.add_argument("--dataset-url", type=str, default=None)
    ap.add_argument("--model-name", type=str, default=None)
    ap.add_argument("--model-version", type=str, default=None)
    ap.add_argument("--notes", type=str, default=None)
    args = ap.parse_args()

    bbox = bbox_from_center(args.lat, args.lon, args.buffer_m)
    sources = [DataSource(type=args.dataset_type, id=args.dataset_id, url=args.dataset_url)]
    model = None
    if args.model_name and args.model_version:
        model = ModelInfo(name=args.model_name, version=args.model_version)

    rec = log_evidence(
        lat=args.lat,
        lon=args.lon,
        candidate_id=args.candidate_id,
        sources=sources,
        bbox=bbox,
        model=model,
        notes=args.notes,
    )
    print("Logged:", rec)

if __name__ == "__main__":
    main()
