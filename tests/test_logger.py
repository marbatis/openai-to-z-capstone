from pathlib import Path

from zexplorer.data_id_logger import DataSource, log_evidence


def test_log_evidence(tmp_path: Path, monkeypatch):
    log_path = tmp_path / "evidence.jsonl"
    monkeypatch.setenv("ZEXP_LOG_PATH", str(log_path))
    log_evidence(
        lat=-10.0,
        lon=-52.0,
        candidate_id="test-0001",
        sources=[DataSource(type="Sentinel-2", id="S2A_TEST_TILE")],
        notes="unit-test",
    )
    assert log_path.exists()
    txt = log_path.read_text().strip()
    assert '"candidate_id": "test-0001"' in txt
    assert '"id": "S2A_TEST_TILE"' in txt
