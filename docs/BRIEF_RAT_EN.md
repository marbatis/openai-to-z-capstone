# Rede de Águas & Tesos (RAT) — Project Brief (EN)

**One‑line:** Detect **floodplain mound (“teso”) and fish‑weir networks** across the Brazilian Amazon using **seasonal L‑band SAR** + **hydrodynamic plausibility** and validate with **GEDI WSCI** canopy structure.

**Goal (contest‑style):** Produce **new, previously unrecorded site *networks*** in Brazil that pass the Challenge’s “two independent methods” bar, with transparent IDs and a judge‑ready write‑up.

## 1) Area & scope
- Focus: Pará & Amazonas floodplains (extendable to Acre, Rondônia).
- Include terra firme margins within 50–100 km of principal channels for completeness.
- Public‑only datasets; coordinates obfuscated in public artifacts (see `docs/ETHICS.md`).

## 2) Datasets (public, persistent IDs)
- **ALOS‑2 PALSAR‑2 ScanSAR L2.2 (25 m)** — L‑band backscatter time series 2014‑present (GEE ID: `JAXA/ALOS/PALSAR-2/Level2_2/ScanSAR`). Convert DN→γ0 dB via `10*log10(DN^2) - 83`. *Primary seasonal signal.*
- **Sentinel‑1 C‑band** — Seasonality cross‑check in cloud seasons.
- **GEDI L4C — Waveform Structural Complexity Index (WSCI)** — Footprint‑scale canopy complexity (download via NASA ORNL DAAC, product `GEDI04_C` v2). *Independent structure signal.*
- **Hydro/topo** — MERIT Hydro (HAND, drainage area), SRTM/AW3D30 as needed.

## 3) Methods (designed to meet “two independent methods”)
**Signal A — Seasonal L‑band hysteresis (primary):**
1. Build **wet** (Dec–May) and **dry** (Jun–Nov) γ0 dB composites.
2. Compute **Δ = wet − dry (dB)** and local z‑scores; extract linear/zig‑zag segments aligned to floodplain flow.
3. Candidate networks = connected segments with consistent Δ sign/strength and plausible spacing.

**Signal B — Hydrodynamic plausibility (physics):**
1. Use MERIT Hydro **HAND** and drainage area to model potential **ponding/deflection**.
2. Score each candidate by overlap with HAND≤N m zones and **flow‑convergent** pixels.

**Optional Signal C — GEDI L4C WSCI:**
- Extract WSCI statistics over candidate berms/mounds vs local controls; expect shifts in canopy complexity.

## 4) Evidence & logging
- For each candidate network: store AOI, method metrics, **scene/tile IDs**, processing params and seeds in `logs/evidence_log.jsonl` via `zexplorer.data_id_logger`.

## 5) Deliverables
- **Maps + overlays** (ΔdB, HAND flow, GEDI footprints), **2–3‑page** write‑up (PT/EN), repo with scripts and IDs.
- Optional CSV of candidates (coords obfuscated to ≥1–2 km in public).

## 6) Timeline (4 weeks)
- **W1:** ALOS‑2 seasonal composites + ΔdB candidates (v0).
- **W2:** Hydrodynamic plausibility + pruning; log evidence lines.
- **W3:** GEDI WSCI extraction and stats; finalize shortlist.
- **W4:** Write‑up, ethical review, bilingual README.

## 7) Ethics
- Do **not** publish exact coordinates publicly; follow `docs/ETHICS.md` and Brazilian norms (IPHAN, Indigenous lands).

## References (dataset docs)
- ALOS‑2 ScanSAR L2.2 (GEE): https://developers.google.com/earth-engine/datasets/catalog/JAXA_ALOS_PALSAR-2_Level2_2_ScanSAR
- GEDI L4C WSCI (UMD/ORNL DAAC landing): https://gedi.umd.edu/gedi-l4c-footprint-level-waveform-structural-complexity-index-released/
