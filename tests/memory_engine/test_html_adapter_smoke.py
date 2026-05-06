from __future__ import annotations

from MAKSIMAR_CORE_LIB.memory_engine.history_ingestion.html_adapter import (
    build_html_adapter_capability,
    build_html_adapter_protocol,
)


def test_html_adapter_smoke() -> None:
    capability = build_html_adapter_capability()
    protocol = build_html_adapter_protocol()

    assert capability.source_type == "html"
    assert capability.text_first_input is True
    assert capability.binary_input_supported is False
    assert capability.parallel_safe_by_design is True
    assert protocol.supported_source_type == "html"
    assert protocol.required_output_kinds == ("raw_document", "structured_text")
