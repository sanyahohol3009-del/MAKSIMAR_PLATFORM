from __future__ import annotations

from MAKSIMAR_CORE_LIB.action_library_adapters.external_tool_library_adapter import (
    build_external_tool_registry,
    probe_external_tool_adapters,
)


def test_external_tool_library_adapter_smoke() -> None:
    registry = build_external_tool_registry().to_read_model()
    statuses = tuple(status.to_read_model() for status in probe_external_tool_adapters())

    assert len(registry["tools"]) == 6
    assert all(tool["adapter_mode"] == "external_adapter" for tool in registry["tools"])
    assert all(tool["not_canonical_truth"] is True for tool in registry["tools"])
    assert all(status["visible_to_jarvis"] is True for status in statuses)
    assert all(status["risk_gate_required"] is True for status in statuses)
