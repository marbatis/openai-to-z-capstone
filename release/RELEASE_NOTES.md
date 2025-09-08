# v1.0 — Marajó & Santarém–Óbidos Candidate Package

**Highlights**
- Prefix-aware pipeline (`scripts/run_marajo_pipeline.py --prefix <aoi>`) + Make targets (`*-pipeline`)
- End-to-end selection → hydro-plausibility scoring → figures
- Contact sheets and short write-up stubs per AOI
- Evidence logging with scene-ID samples; big rasters excluded from git

**Included**
- `release/ABSTRACT_200w.md`, `release/REPRODUCE.md`, `CITATION.cff`
- `data/candidates/<prefix>/hotspots_{topN,scores}.(geojson|csv)`
- `figures/<prefix>/*_overview.png`, `figures/<prefix>/contact_sheet.png`
- `reports/<prefix>-candidate.md`

**Run**
make move-downloads PREFIX=marajo
make marajo-pipeline
make contact-sheet PREFIX=marajo
make writeup PREFIX=marajo

**Ethics**
Coordinates are obfuscated in public artifacts. Share exacts only with qualified reviewers in coordination with local stakeholders.
