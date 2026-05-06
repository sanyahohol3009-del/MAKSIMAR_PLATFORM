from __future__ import annotations

from MAKSIMAR_CORE_LIB.memory_engine.history_ingestion.pdf_adapter import (
    build_pdf_adapter_capability,
    build_pdf_adapter_protocol,
)


def test_pdf_adapter_smoke() -> None:
    capability = build_pdf_adapter_capability()
    protocol = build_pdf_adapter_protocol()

    assert capability.source_type == "pdf"
    assert capability.text_first_input is False
    assert capability.binary_input_supported is True
    assert capability.parallel_safe_by_design is True
    assert protocol.supported_source_type == "pdf"
    assert protocol.required_output_kinds == ("raw_document", "binary_document")
