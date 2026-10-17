from __future__ import annotations

import tempfile

from MAKSIMAR_CORE_LIB.memory_engine.history_ingestion.live_import_write_writer import (
    execute_live_import_write,
)


def test_live_import_write_writer_smoke() -> None:
    with tempfile.TemporaryDirectory() as tmpdir:
        result = execute_live_import_write(
            import_root_path="runtime_imports/chatgpt_export_01",
            write_root_path=tmpdir,
        )
    assert result.write_ready is True



def test_live_import_skips_only_matching_files_and_preserves_conflicting_evidence(tmp_path, monkeypatch):
    import json
    import pytest
    from MAKSIMAR_CORE_LIB.memory_engine.history_ingestion import live_import_write_writer as writer
    from MAKSIMAR_CORE_LIB.memory_engine.history_ingestion.live_import_write_summary_builder import build_live_import_write_summary
    plan = {"session": {"session_id": "isolated-session", "manifest_kind": "live_import_session_manifest"},
        "conversation_manifests": (), "normalized_records": (), "message_units": (), "attachment_roots": ("isolated-source",)}
    monkeypatch.setattr(writer, "build_live_import_write_plan", lambda _: plan)
    first = build_live_import_write_summary("isolated", str(tmp_path))
    manifest = tmp_path / "registry/import_sessions/isolated-session.json"
    preserved = manifest.read_bytes()
    before_stat = manifest.stat()
    second = build_live_import_write_summary("isolated", str(tmp_path))
    assert first["session_manifest_written"] is True
    assert second["session_manifest_written"] is False
    assert first["session_manifest_available"] is second["session_manifest_available"] is True
    assert manifest.read_bytes() == preserved and manifest.stat().st_mtime_ns == before_stat.st_mtime_ns
    for broken in ('{broken', json.dumps({"session_id": "other-session"})):
        manifest.write_text(broken)
        with pytest.raises((ValueError, json.JSONDecodeError)):
            writer.execute_live_import_write("isolated", str(tmp_path))
        assert manifest.read_text() == broken


def test_live_import_conflicting_child_payload_is_not_success_or_overwritten(tmp_path, monkeypatch):
    import pytest
    from MAKSIMAR_CORE_LIB.memory_engine.history_ingestion import live_import_write_writer as writer
    path = tmp_path / "child.json"
    assert writer._write_json_if_missing(path, {"value": 1}) is True
    assert writer._write_json_if_missing(path, {"value": 1}) is False
    with pytest.raises(ValueError, match="existing_payload_conflict"):
        writer._write_json_if_missing(path, {"value": 2})
    assert path.read_text().strip().endswith('1\n}')
