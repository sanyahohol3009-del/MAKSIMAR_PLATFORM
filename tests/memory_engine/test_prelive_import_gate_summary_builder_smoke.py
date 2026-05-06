from __future__ import annotations

from MAKSIMAR_CORE_LIB.memory_engine.history_ingestion.prelive_import_gate_summary_builder import (
    build_prelive_import_gate_summary,
)


def test_prelive_import_gate_summary_builder_smoke() -> None:
    summary = build_prelive_import_gate_summary()
    assert summary["prelive_gate_ready"] is True
