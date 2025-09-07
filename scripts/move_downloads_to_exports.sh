#!/usr/bin/env bash
set -euo pipefail
mkdir -p data/exports
shopt -s nullglob
for pat in \
  "marajo_S1_hotspots_coarse*.geojson" \
  "marajo_S1VV_delta_db*.tif" \
  "marajo_S1VV_delta_rgb*.tif" \
  "marajo_ALOS2_delta_rgb*.tif" \
  "marajo_DEM_30m*.tif"
do
  f=$(ls -1 "$HOME/Downloads"/$pat 2>/dev/null | head -n1 || true)
  if [[ -n "${f:-}" ]]; then
    base=$(echo "$pat" | sed 's/\*.//; s/\*//g')
    # normalize to canonical name
    case "$pat" in
      marajo_S1_hotspots_coarse*)  dest="marajo_S1_hotspots_coarse.geojson" ;;
      marajo_S1VV_delta_db*)       dest="marajo_S1VV_delta_db.tif" ;;
      marajo_S1VV_delta_rgb*)      dest="marajo_S1VV_delta_rgb.tif" ;;
      marajo_ALOS2_delta_rgb*)     dest="marajo_ALOS2_delta_rgb.tif" ;;
      marajo_DEM_30m*)             dest="marajo_DEM_30m.tif" ;;
    esac
    echo "$f -> data/exports/$dest"
    mv -f "$f" "data/exports/$dest"
  fi
done
echo "Done. Current exports:"
ls -lh data/exports || true
