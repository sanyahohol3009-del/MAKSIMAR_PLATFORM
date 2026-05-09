from __future__ import annotations

from pathlib import Path


def test_storage_phase_1_5_no_server_data_plane_import_smoke() -> None:
    files = (
        Path("MAKSIMAR_SERVER/EXECUTION_CONTROL/artifact_routing/storage_registry_artifact_binding_builder.py"),
        Path("MAKSIMAR_SERVER/EXECUTION_CONTROL/artifact_routing/storage_registry_artifact_binding_preview.py"),
        Path("MAKSIMAR_SERVER/EXECUTION_CONTROL/artifact_routing/storage_artifact_readiness_gate.py"),
    )

    for path in files:
        source = path.read_text(encoding="utf-8")
        assert "MAKSIMAR_SERVER.DATA_PLANE" not in source
        assert "MAKSIMAR_SERVER/DATA_PLANE" not in source
