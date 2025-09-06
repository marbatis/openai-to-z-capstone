**test(geoutils): high‑latitude coverage for `bbox_from_center`**

**Why**
- Harden CI by exercising `bbox_from_center` near ±60° where longitudinal degree spans inflate (1/cos φ).
- Prevent regressions in the spherical‑approximation math used for coarse AOIs (~100 km scale).

**What’s included**
- `tests/test_geoutils.py` with three checks:
  - **Center & size fidelity** at lat ∈ {0°, ±60°} for ~100 km half‑size
  - **Longitude scaling property**: dlon(60°) ≈ 2 × dlon(0°)
  - **Latitude scaling property**: dlat is latitude‑independent under the function’s approximation

**How to run**
```bash
pip install -r requirements.txt -r requirements-dev.txt
pytest -q tests/test_geoutils.py
```

**Notes**
- Tests avoid wrap‑around cases near ±180° and very large half‑sizes, since the helper does not clip/normalize longitudes.
