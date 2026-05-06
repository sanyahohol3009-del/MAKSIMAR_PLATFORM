from __future__ import annotations

from MAKSIMAR_CORE_LIB.memory_engine.history_ingestion.md_adapter import (
    build_md_adapter_capability,
    build_md_adapter_protocol,
)


def test_md_adapter_smoke() -> None:
    capability = build_md_adapter_capability()
    protocol = build_md_adapter_protocol()

    assert capability.source_type == "md"
    assert capability.text_first_input is True
    assert capability.binary_input_supported is False
    assert protocol.supported_source_type == "md"
