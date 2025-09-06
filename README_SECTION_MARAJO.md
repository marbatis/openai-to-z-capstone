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
