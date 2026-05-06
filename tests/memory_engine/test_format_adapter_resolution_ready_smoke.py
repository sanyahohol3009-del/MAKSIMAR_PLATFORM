from __future__ import annotations

from MAKSIMAR_CORE_LIB.memory_engine.history_ingestion.adapter_registry_builder import (
    build_default_adapter_registry,
)


def test_format_adapter_resolution_ready_smoke() -> None:
    registry = build_default_adapter_registry()

    html_capability = registry.get_capability_for_source_type("html")
    pdf_capability = registry.get_capability_for_source_type("pdf")

    assert html_capability.adapter_id == "HADAPTER-HTML-001"
    assert pdf_capability.adapter_id == "HADAPTER-PDF-001"
    assert registry.parallel_safe_registry is True
    assert registry.deterministic_registry is True
