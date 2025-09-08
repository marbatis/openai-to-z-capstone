#!/usr/bin/env python3
import argparse
import json
from pathlib import Path
import re

import pandas as pd


def nice_name(px: str) -> str:
    m = {"marajo": "Marajó", "santarem": "Santarém–Óbidos", "tapajos": "Tapajós"}
    return m.get(px.lower(), px.title())


def extract_scene_ids(
    prefix: str | None, candidate_id: str | None
) -> tuple[list[str], list[str], list[str]]:
    """Return (alos_ids, s1_wet, s1_dry) from logs/evidence_log.jsonl, filtered by prefix/candidate_id if possible."""
    log = Path("logs/evidence_log.jsonl")
    if not log.exists():
        return [], [], []
    lines = log.read_text(encoding="utf-8").strip().splitlines()

    # Heuristics for matching:
    def matches(j: dict) -> bool:
        cid = (j.get("candidate_id") or "").lower()
        notes = (j.get("notes") or "").lower()
        if candidate_id and j.get("candidate_id") == candidate_id:
            return True
        if prefix:
            if prefix.lower() in cid or prefix.lower() in notes:
                return True
        return False

    alos, s1w, s1d, s1raw = [], [], [], []

    # Pass 1: filter by desired criteria; else fallback to last 20
    chosen = []
    for line in lines:
        try:
            j = json.loads(line)
        except Exception:
            continue
        if matches(j):
            chosen.append(j)
    if not chosen:
        chosen = [json.loads(l) for l in lines[-20:] if l.strip().startswith("{")]

    for j in chosen:
        srcs = j.get("sources") or []
        if not srcs:
            continue
        t = (srcs[0].get("type") or "").lower()
        ids = srcs[0].get("id") or ""
        # ALOS-2
        if "alos2" in t or "alos-2" in t or "palsar" in t:
            alos += re.findall(r"ALOS[0-9A-Z_\-]+", ids)
        # Sentinel-1
        if "sentinel-1" in t or "sentinel-1" in ids or "s1" in ids.lower():
            # Try to split WET/DRY if present in the id string:
            wet = re.search(r"WET:\s*([^;]+)", ids)
            dry = re.search(r"DRY:\s*([^;]+)", ids)
            if wet:
                s1w += re.findall(r"S1[A-Z0-9_]+", wet.group(1))
            if dry:
                s1d += re.findall(r"S1[A-Z0-9_]+", dry.group(1))
            if not wet and not dry:
                s1raw += re.findall(r"S1[A-Z0-9_]+", ids)

    # De-duplicate order-preserving
    def dedup(seq):
        seen = set()
        out = []
        for x in seq:
            if x not in seen:
                seen.add(x)
                out.append(x)
        return out

    alos = dedup(alos)[:4]
    s1w = dedup(s1w)[:3]
    s1d = dedup(s1d)[:3]
    if not s1w and not s1d and s1raw:
        # Fallback: first half "wet", second half "dry"
        half = max(1, len(s1raw) // 2)
        s1w, s1d = dedup(s1raw[:half])[:3], dedup(s1raw[half:])[:3]
    return alos, s1w, s1d


def main():
    ap = argparse.ArgumentParser(description="Write-up stub generator (prefix-aware)")
    ap.add_argument("--prefix", required=True, help="AOI prefix, e.g. marajo, santarem, tapajos")
    ap.add_argument(
        "--candidate-id",
        default=None,
        help="Exact candidate_id to anchor scene IDs, e.g. marajo-hot-0103",
    )
    ap.add_argument("--outfile", default=None)
    args = ap.parse_args()
    px = args.prefix

    scores = Path("data/candidates") / px / "hotspots_scores.csv"
    if not scores.exists():
        raise SystemExit(f"Missing {scores}. Run the pipeline first.")
    df = pd.read_csv(scores)
    if df.empty:
        raise SystemExit("Scores CSV is empty.")

    # pick best by frac_ok
    top = df.sort_values("frac_ok", ascending=False).iloc[0]
    idx = int(top["idx"])
    area = float(top.get("area_ha", float("nan")))
    frac = float(top.get("frac_ok", float("nan")))

    # Figure path (written by pipeline)
    figdir = Path("figures") / px
    expected = figdir / f"marajo-hot-01{idx:02d}_overview.png"
    if not expected.exists():
        # fallback to any overview
        cand = sorted(figdir.glob("*_overview.png"))
        expected = cand[0] if cand else expected

    # Scene ID samples from log (filtered by prefix/candidate-id)
    alos_ids, s1w, s1d = extract_scene_ids(prefix=px, candidate_id=args.candidate_id)
    alos_txt = ", ".join(alos_ids) if alos_ids else "see evidence log"
    s1w_txt = ", ".join(s1w) if s1w else "see evidence log"
    s1d_txt = ", ".join(s1d) if s1d else "see evidence log"

    outdir = Path("reports")
    outdir.mkdir(parents=True, exist_ok=True)
    out = Path(args.outfile) if args.outfile else outdir / f"{px}-candidate.md"

    md = f"""# {nice_name(px)} — Seasonal Δ Candidate Package (v1)

**Selected candidate:** rank {idx} — area ≈ {area:.2f} ha — hydro score frac_ok ≈ {frac:.3f}

## Methods
- Built wet–dry seasonal composites and Δ = wet − dry for ALOS-2 (HH, γ⁰ dB) and Sentinel-1 VV.
- Thresholded / denoised / coarsened S1 Δ → hotspots; kept Top-N by area.
- Simple plausibility: Δ>0 & relative elevation ≤ 5 m (DEM 30 m, HAND-like).

**Scene ID samples**
- **ALOS-2:** {alos_txt}
- **S1 wet:** {s1w_txt}
- **S1 dry:** {s1d_txt}

**Figure**
![Overview]({expected.as_posix()})

*Left:* ALOS-2 Δ (colorized) — if exported. *Right:* S1 VV Δ (RGB or dB). Yellow outline = candidate.

## Evidence & Reproducibility
- Evidence lines: `logs/evidence_log.jsonl` (filter by prefix or candidate_id).
- AOI inputs: `data/exports/{px}_*`
- Outputs: `data/candidates/{px}/` and `figures/{px}/`
"""
    out.write_text(md, encoding="utf-8")
    print("Wrote", out)


if __name__ == "__main__":
    main()
