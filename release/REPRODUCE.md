# Reproducibility (quick)

## Prereqs
- Python 3.11+ (local venv `.venv`)
- Earth Engine exports for each AOI in `~/Downloads`:
  - `<prefix>_S1VV_delta_db.tif` (required)
  - `<prefix>_S1VV_delta_rgb.tif` (optional, figure quality)
  - `<prefix>_S1_hotspots_coarse.geojson` (or the mask to polygonize)
  - `<prefix>_DEM_30m.tif`
  - `<prefix>_ALOS2_delta_rgb.tif` (optional)

## 1) Stage downloads → data/exports
make move-downloads PREFIX=marajo
make move-downloads PREFIX=santarem

## 2) Run end-to-end per AOI
make marajo-pipeline
make santarem-pipeline

Outputs:
- Candidates: `data/candidates/<prefix>/hotspots_topN.{geojson,csv}`
- Scores:     `data/candidates/<prefix>/hotspots_scores.csv`
- Figures:    `figures/<prefix>/*_overview.png` and `contact_sheet.png`

## 3) Write-up stub
make writeup PREFIX=marajo
make writeup PREFIX=santarem

## Notes
- Large rasters (`data/exports/*.tif`) are ignored in git on purpose.
- Evidence lines (scene IDs) live in `logs/evidence_log.jsonl`.
