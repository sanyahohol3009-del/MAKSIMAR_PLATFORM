from __future__ import annotations

from MAKSIMAR_CORE_LIB.memory_engine.history_ingestion.txt_adapter import (
    build_txt_adapter_capability,
    build_txt_adapter_protocol,
)


def test_txt_adapter_smoke() -> None:
    capability = build_txt_adapter_capability()
    protocol = build_txt_adapter_protocol()

    assert capability.source_type == "txt"
    assert capability.text_first_input is True
    assert capability.binary_input_supported is False
    assert protocol.supported_source_type == "txt"
