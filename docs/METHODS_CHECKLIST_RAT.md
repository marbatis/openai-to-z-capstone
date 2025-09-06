# Methods Checklist — Rede de Águas & Tesos (RAT)

This checklist mirrors the OpenAI‑to‑Z rubric: **Archaeological Impact → Investigative Ingenuity → Reproducibility**. Tick items as you progress.

## A) Archaeological Impact
- [ ] Define Brazilian AOI (bbox/geojson) and justify (floodplain focus, known/unknown gaps).
- [ ] Generate **new network candidates** (not just points), with measurements (length, spacing, orientation).
- [ ] Contextualize with literature (fish‑weirs/tesos/waterscapes in BR). 
- [ ] Provide **two independent lines of evidence** per candidate network.

## B) Investigative Ingenuity
- [ ] **Signal A (L‑band seasonality)**: wet vs dry composites, ΔdB maps, linear segment extraction.
- [ ] **Signal B (Hydrodynamics)**: HAND & drainage overlays; ponding/deflection plausibility score.
- [ ] **Signal C (optional, GEDI WSCI)**: footprint stats vs controls.
- [ ] False‑positive analysis (natural levees/bars); ablation or thresholds rationale.

## C) Reproducibility
- [ ] Log **all scene/tile IDs** and parameters (time windows, bands, filters) to `logs/evidence_log.jsonl`.
- [ ] Fix random seeds; keep config in a small YAML/JSON block.
- [ ] Export intermediate rasters/vectors with metadata (CRS, pixel size, scale factors).
- [ ] Bilingual summary (PT/EN) + clear rerun instructions.
- [ ] Ethics: obfuscate exact coordinates in public artifacts; internal list kept private.

## D) Deliverables
- [ ] 2–3 page write‑up with figures (ΔdB, HAND, GEDI).
- [ ] CSV/GeoJSON of candidates (obfuscated).
- [ ] Links to datasets (GEE IDs, DAAC granules) and scripts.
