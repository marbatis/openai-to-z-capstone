# Reports Usage

This repo includes utilities to produce a contact sheet of candidate overviews and a short, prefix-aware write-up stub.

- Inputs live under `data/exports/<prefix>_*` (e.g., `santarem_S1VV_delta_db.tif`).
- Pipeline outputs go to `data/candidates/<prefix>/` and `figures/<prefix>/`.

## Commands
- Stage downloads into exports:
  - `make move-downloads PREFIX=<prefix>`
- Run the pipeline (select → score → render):
  - `make <prefix>-pipeline` (e.g., `make santarem-pipeline`)
- Build a contact sheet from `<prefix>/*_overview.png`:
  - `make contact-sheet PREFIX=<prefix>`
- Generate a write-up stub from `hotspots_scores.csv`:
  - `make writeup PREFIX=<prefix>`

See top-level README for more details and examples.
