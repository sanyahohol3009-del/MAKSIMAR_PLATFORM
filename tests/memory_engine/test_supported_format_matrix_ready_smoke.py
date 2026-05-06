from __future__ import annotations

from MAKSIMAR_CORE_LIB.memory_engine.history_ingestion.adapter_registry_builder import (
    build_default_adapter_registry,
)


def test_supported_format_matrix_ready_smoke() -> None:
    registry = build_default_adapter_registry()

    assert registry.supported_source_type_matrix == (
        "html",
        "pdf",
        "txt",
        "md",
        "json",
    )
    assert registry.as_index() == {
        "html": "HADAPTER-HTML-001",
        "pdf": "HADAPTER-PDF-001",
        "txt": "HADAPTER-TXT-001",
        "md": "HADAPTER-MD-001",
        "json": "HADAPTER-JSON-001",
    }
