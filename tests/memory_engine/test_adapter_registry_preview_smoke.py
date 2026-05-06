from __future__ import annotations

from MAKSIMAR_CORE_LIB.memory_engine.history_ingestion.adapter_registry_builder import (
    build_adapter_registry_preview,
)


def test_adapter_registry_preview_smoke() -> None:
    preview = build_adapter_registry_preview()

    assert preview["parallel_safe_registry"] is True
    assert preview["deterministic_registry"] is True
    assert preview["supported_source_type_matrix"] == (
        "html",
        "pdf",
        "txt",
        "md",
        "json",
    )
    assert preview["adapter_index"]["html"] == "HADAPTER-HTML-001"
    assert preview["adapter_index"]["pdf"] == "HADAPTER-PDF-001"
