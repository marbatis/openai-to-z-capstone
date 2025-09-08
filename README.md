**Release:** [v1.0 — Marajó & Santarém–Óbidos candidate package](https://github.com/marbatis/openai-to-z-capstone/releases/tag/v1.0-marajo-santarem)

# ZExplorer: OpenAI-to-Z Capstone (Self‑Guided)

[![CI](https://github.com/marbatis/openai-to-z-capstone/actions/workflows/ci.yml/badge.svg)](https://github.com/marbatis/openai-to-z-capstone/actions/workflows/ci.yml)

This repository is a **training/capstone** adaptation of the OpenAI *to Z* Challenge (now closed).
It mirrors the original checkpoints and deliverables so you can practice end‑to‑end: define an area
in the Amazon biome, gather open data, generate candidate archaeological sites, and log reproducible
evidence using modern tooling and AI assistance.

> **Scope:** Brazil first; optionally borders of Bolivia, Colombia, Ecuador, Guyana, Peru, Suriname,
> Venezuela, and French Guiana. **Do not** disclose sensitive coordinates publicly without ethics review.

---

## Quickstart

### 1) Create a Python env
```bash
# macOS/Linux (venv)
python -m venv .venv
source .venv/bin/activate

# Windows (PowerShell)
python -m venv .venv
.\.venv\Scripts\Activate.ps1

python -m pip install -U pip
pip install -r requirements.txt

# (Optional) add a Jupyter kernel
python -m ipykernel install --user --name zexplorer
```

> If you prefer Conda/Mamba, use `environment.yml` you may create later, or adapt requirements.

### 2) Configure secrets
Copy `config/.env.example` to `.env` and set your keys (e.g., `OPENAI_API_KEY`).

### 3) Sanity checks
```bash
make lint
make test
```

### 4) Start with Checkpoint 1
Open the starter notebook:
```bash
jupyter notebook notebooks/01_checkpoint1.ipynb
```
Work through: define a bounding box, list at least **one** data source (LiDAR tile ID, Sentinel/ Landsat scene ID, etc.), and log it with `zexplorer.data_id_logger`.

### Next: Checkpoint 2
Open the scaffolded search + logging notebook:
```bash
make notebook2
```
This queries Sentinel-2 L2A via a public STAC endpoint within your AOI, saves a small search artifact to `data/stac_search`, visualizes footprints, and logs a JSONL evidence record.

---

## Project Layout
```
openai-to-z-capstone/
├─ README.md
├─ requirements.txt
├─ Makefile
├─ pyproject.toml
├─ LICENSE
├─ NOTICE
├─ .gitignore
├─ config/
│  └─ .env.example
├─ src/
│  └─ zexplorer/
│     ├─ __init__.py
│     ├─ data_id_logger.py
│     ├─ geoutils.py
│     └─ anomaly.py
├─ scripts/
│  └─ new_candidate.py
├─ notebooks/
│  └─ 01_checkpoint1.ipynb
├─ abstract/
│  └─ abstract.md
├─ writeup/
│  └─ WRITEUP_TEMPLATE.md
├─ prompts/
│  ├─ system_prompt.md
│  └─ checkpoint1_user_prompt.md
├─ docs/
│  └─ ETHICS.md
├─ .github/workflows/
│  └─ ci.yml
└─ tests/
   └─ test_logger.py
```

---

## Evidence logging (JSONL)
Use `zexplorer.data_id_logger.log_evidence(...)` to append a line to `logs/evidence_log.jsonl` with:
- dataset/source identifiers (e.g., LiDAR tile IDs, STAC IDs, DOIs),
- model name/version used for any AI step,
- candidate coordinates/bbox,
- reproducibility notes and optional content hashes.

Example CLI:
```bash
python scripts/new_candidate.py   --lat -10.123 --lon -52.456   --dataset-type "Sentinel-2"   --dataset-id "S2A_MSIL2A_20250101T135321_N0515_R081_T21LVC"   --model-name "gpt-4.1" --model-version "2025-06-01"   --notes "Initial scan over 100x100km tract; canopy breaks near levee."
```

---

## Abstract & Write‑up
- Draft your **200‑word abstract** in `abstract/abstract.md` (a stub is included).
- Use `writeup/WRITEUP_TEMPLATE.md` to assemble your evidence with overlays and citations.

---

## Ethics
Read `docs/ETHICS.md` **before** publishing any coordinates or sensitive cultural information.

---

## Make targets
```bash
make help
```

---

## License
Apache-2.0 (see `LICENSE`, `NOTICE`).


## AOI: Ilha do Marajó (Pará)

Start with the Brazilian **Ilha do Marajó** floodplain AOI (100×100 km). This region is ideal for
validating the L‑band seasonal ΔdB + hydro plausibility + GEDI WSCI workflow.

**Docs:** [AOI_MARAJO_EN.md](docs/AOI_MARAJO_EN.md) · [AOI_MARAJO_PT.md](docs/AOI_MARAJO_PT.md)

**Quick commands**
```bash
# Preview the AOI bbox and save an HTML map to data/
make marajo-preview

# Open ALOS-2 seasonal composites notebook (Δ = wet − dry in γ0 dB)
make marajo

# Open GEDI L4C WSCI extraction notebook for the same AOI
make marajo-gedi

# Open both notebooks
make marajo-all
```

## Marajó Quickstart

Required exports in `data/exports/`:
- `marajo_S1_hotspots_coarse.geojson` (Sentinel-1 hotspots polygons)
- `marajo_S1VV_delta_db.tif` (Sentinel-1 VV seasonal Δ, dB)
- `marajo_DEM_30m.tif` (DEM at ~30 m)
- `marajo_ALOS2_delta_rgb.tif` (colorized ALOS-2 Δ RGB)
- `marajo_S1VV_delta_rgb.tif` (optional; if absent, dB layer is used)

Move from Downloads:
- `make move-downloads`

Run the end-to-end pipeline:
- `make marajo`

Outputs:
- `data/candidates/*.csv|.geojson`
- `figures/candidates/*.png`

## AOI-scoped pipeline

- Put exports in `data/exports/<prefix>_*` (e.g., `santarem_S1VV_delta_db.tif`)
- Stage downloads:  `make move-downloads PREFIX=santarem`
- Run pipeline:     `make santarem-pipeline`
- Outputs:          `data/candidates/<prefix>/` and `figures/<prefix>/`


**Tip:** You can force ID extraction for a specific feature with `make writeup PREFIX=santarem CAND=marajo-hot-0102`, which passes `--candidate-id`. Otherwise it falls back to entries matching the prefix (or recent logs).
