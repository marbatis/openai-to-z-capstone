from __future__ import annotations

import hashlib
import json
import os
from dataclasses import asdict, dataclass, field
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Dict, List, Optional

DEFAULT_LOG_PATH = Path("logs/evidence_log.jsonl")


def _log_path() -> Path:
    # Allow override for tests
    env_path = os.getenv("ZEXP_LOG_PATH")
    if env_path:
        return Path(env_path)
    return DEFAULT_LOG_PATH


def sha256_hex(s: str) -> str:
    return hashlib.sha256(s.encode("utf-8")).hexdigest()


@dataclass
class DataSource:
    type: str
    id: str
    url: Optional[str] = None


@dataclass
class ModelInfo:
    name: str
    version: str


@dataclass
class EvidenceRecord:
    timestamp: str
    candidate_id: str
    lat: float
    lon: float
    bbox: Optional[List[float]] = None  # [minlon, minlat, maxlon, maxlat]
    sources: List[DataSource] = field(default_factory=list)
    model: Optional[ModelInfo] = None
    prompt_sha256: Optional[str] = None
    output_sha256: Optional[str] = None
    notes: Optional[str] = None
    extra: Dict[str, Any] = field(default_factory=dict)


def log_evidence(
    lat: float,
    lon: float,
    candidate_id: str,
    sources: List[DataSource],
    bbox: Optional[List[float]] = None,
    model: Optional[ModelInfo] = None,
    prompt_text: Optional[str] = None,
    output_text: Optional[str] = None,
    notes: Optional[str] = None,
    extra: Optional[Dict[str, Any]] = None,
) -> EvidenceRecord:
    rec = EvidenceRecord(
        timestamp=datetime.now(timezone.utc).isoformat(),
        candidate_id=candidate_id,
        lat=lat,
        lon=lon,
        bbox=bbox,
        sources=sources,
        model=model,
        prompt_sha256=sha256_hex(prompt_text) if prompt_text else None,
        output_sha256=sha256_hex(output_text) if output_text else None,
        notes=notes,
        extra=extra or {},
    )
    path = _log_path()
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("a", encoding="utf-8") as f:
        f.write(json.dumps(asdict(rec), ensure_ascii=False) + "\n")
    return rec
