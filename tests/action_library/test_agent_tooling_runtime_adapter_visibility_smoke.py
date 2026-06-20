from __future__ import annotations

from MAKSIMAR_CORE_LIB.action_library_adapters.agent_tooling_runtime_adapter import (
    build_agent_tooling_runtime_adapter_read_model,
)


def test_agent_tooling_runtime_adapter_visibility_smoke(monkeypatch) -> None:
    monkeypatch.setattr(
        "MAKSIMAR_CORE_LIB.action_library_adapters.agent_tooling_runtime_adapter.build_agent_tooling_runtime_probe_read_model",
        lambda: {
            "runtime_python": "/dev/shm/agent_tooling_runtime_python",
            "probe_results": (),
            "installed": ("openai-agents-python", "mcp"),
            "import_probe_passed": ("openai-agents-python", "mcp"),
            "errors": (),
        },
    )

    payload = build_agent_tooling_runtime_adapter_read_model()

    assert payload["adapter_id"] == "agent_tooling_runtime_adapter_v1"
    assert payload["visible_to_jarvis"] is True
    assert payload["proposal_only"] is True
    assert payload["risk_gate_required"] is True
    assert payload["execution_allowed"] is False
    assert "external_adapter:openai_agents_sdk" in tuple(tool["tool_id"] for tool in payload["registry"]["tools"])
    assert "external_adapter:autogen_agentchat" in tuple(tool["tool_id"] for tool in payload["registry"]["tools"])
    assert "external_adapter:autogen_ext" in tuple(tool["tool_id"] for tool in payload["registry"]["tools"])
    assert "external_adapter:langgraph" in tuple(tool["tool_id"] for tool in payload["registry"]["tools"])
    assert "external_adapter:mcp_python_sdk" in tuple(tool["tool_id"] for tool in payload["registry"]["tools"])
