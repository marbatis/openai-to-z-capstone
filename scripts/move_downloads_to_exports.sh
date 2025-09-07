#!/usr/bin/env bash
set -euo pipefail
PREFIX="${PREFIX:-marajo}"
mkdir -p data/exports
shopt -s nullglob
mv_one() {
  local pat="$1" dest="$2"
  local f
  f=$(ls -1 "$HOME/Downloads/${PREFIX}_${pat}" 2>/dev/null | head -n1 || true)
  if [[ -n "${f:-}" ]]; then
    echo "$f -> data/exports/${PREFIX}_${dest}"
    mv -f "$f" "data/exports/${PREFIX}_${dest}"
  fi
}
mv_one "S1_hotspots_coarse"*.geojson "S1_hotspots_coarse.geojson"
mv_one "S1VV_delta_db"*.tif          "S1VV_delta_db.tif"
mv_one "S1VV_delta_rgb"*.tif         "S1VV_delta_rgb.tif"
mv_one "ALOS2_delta_rgb"*.tif        "ALOS2_delta_rgb.tif"
mv_one "DEM_30m"*.tif                "DEM_30m.tif"
mv_one "S1_hotspots_mask_40m"*.tif   "S1_hotspots_mask_40m.tif"
echo "Done. Current exports:"
ls -lh data/exports | sed -n '1,80p' || true
