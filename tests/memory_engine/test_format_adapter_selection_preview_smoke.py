from __future__ import annotations

from MAKSIMAR_CORE_LIB.memory_engine.history_ingestion.adapter_registry_builder import (
    build_format_selection_preview,
)


def test_format_adapter_selection_preview_smoke() -> None:
    preview = build_format_selection_preview("pdf")

    assert preview["source_type"] == "pdf"
    assert preview["selected_adapter_id"] == "HADAPTER-PDF-001"
    assert preview["binary_input_supported"] is True
    assert preview["parallel_safe_by_design"] is True
    assert preview["selection_ready"] is True
