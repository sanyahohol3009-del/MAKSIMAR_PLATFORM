from __future__ import annotations

from MAKSIMAR_CORE_LIB.memory_engine.history_ingestion.json_adapter import (
    build_json_adapter_capability,
    build_json_adapter_protocol,
)


def test_json_adapter_smoke() -> None:
    capability = build_json_adapter_capability()
    protocol = build_json_adapter_protocol()

    assert capability.source_type == "json"
    assert capability.text_first_input is True
    assert capability.binary_input_supported is False
    assert protocol.supported_source_type == "json"
