feat(rat): Rede de Águas & Tesos — brief, checklist, and starter GEE notebooks

Why
- Add RAT (Rede de Águas & Tesos) materials: English/PT briefs, methods checklist, and starter notebooks for ALOS‑2 and GEDI workflows.
- Keep extras out of base CI; provide optional requirements for geospatial/cloud workflows.

What changed
- docs/BRIEF_RAT_EN.md — English overview of RAT objectives and scope.
- docs/BRIEF_RAT_PT.md — Portuguese version.
- docs/METHODS_CHECKLIST_RAT.md — methods mapped to impact, ingenuity, reproducibility.
- notebooks/10_ALOS2_seasonal_composites.ipynb — Google Earth Engine workflow (Python): wet/dry ALOS‑2 PALSAR‑2 L2.2 composites and ΔdB maps (DN→γ0 dB via 10*log10(DN^2) - 83).
- notebooks/11_GEDI_L4C_WSCI_extraction.ipynb — Earthdata (CMR) discovery + GEDI04_C v2 extraction; outputs GeoJSON/CSV footprints.
- scripts/gee_alos2_seasonal_composites.js — GEE Code Editor (JS) version of the ALOS‑2 workflow.
- requirements-extra.txt — optional dependencies for these notebooks; base CI remains unchanged.

How to use
- Optional env: `pip install -r requirements-extra.txt`
- Open notebooks with project kernel: `make notebook` or `make notebook2` (switch NOTEBOOK var to the file you want).

Notes
- No changes to base `requirements.txt` or CI workflow.
- Follow data licensing and access terms (GEE/Earthdata) when running notebooks.
