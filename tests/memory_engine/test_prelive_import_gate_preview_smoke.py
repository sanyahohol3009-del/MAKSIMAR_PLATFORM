from __future__ import annotations

from MAKSIMAR_CORE_LIB.memory_engine.history_ingestion.prelive_import_gate_builder import (
    build_prelive_import_gate_preview,
)


def test_prelive_import_gate_preview_smoke() -> None:
    preview = build_prelive_import_gate_preview()
    assert preview["prelive_gate_ready"] is True
