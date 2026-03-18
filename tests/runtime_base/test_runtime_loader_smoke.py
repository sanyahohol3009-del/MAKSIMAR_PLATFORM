from __future__ import annotations

from pathlib import Path

from MAKSIMAR_CORE_LIB.runtime_base.runtime_loader import load_runtime_document


def test_runtime_loader_rejects_missing_schema_version(tmp_path: Path) -> None:
    """Runtime loader should reject document without schema_version."""
    file_path = tmp_path / "runtime_state.json"
    file_path.write_text('{"run_id": "abc"}', encoding="utf-8")

    result = load_runtime_document(file_path)

    assert result.is_valid is False
    assert result.document is None
    assert result.error is not None


def test_runtime_loader_accepts_valid_json(tmp_path: Path) -> None:
    """Runtime loader should accept valid runtime JSON."""
    file_path = tmp_path / "runtime_state.json"
    file_path.write_text(
        '{"schema_version": "runtime_state.v1", "run_id": "abc"}',
        encoding="utf-8",
    )

    result = load_runtime_document(file_path)

    assert result.is_valid is True
    assert result.document is not None
    assert result.document.name == "runtime_state"
    assert result.document.version == "runtime_state.v1"
