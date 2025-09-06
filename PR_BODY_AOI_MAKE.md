**feat(aoi/make): Marajó convenience targets + README section**

**Why**
- Make it one-command easy to work on the **Ilha do Marajó** AOI.
- Surface AOI docs and commands in the README for contributors.

**Changes**
- Makefile targets:
  - `marajo-preview` → saves an HTML bbox map to `data/`
  - `marajo` → opens ALOS-2 ΔdB notebook (`10a_ALOS2_MARAJO.ipynb`)
  - `marajo-gedi` → opens GEDI WSCI notebook (`11a_GEDI_MARAJO.ipynb`)
  - `marajo-all` → opens both notebooks
- README section “AOI: Ilha do Marajó (Pará)” with links & quick commands.

**How to use**
```bash
make marajo-preview
make marajo
make marajo-gedi
make marajo-all
```
