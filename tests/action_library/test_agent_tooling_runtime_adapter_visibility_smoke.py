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


def test_agent_tooling_visibility_and_probe_share_one_observation(monkeypatch) -> None:
    import MAKSIMAR_CORE_LIB.action_library_adapters.agent_tooling_runtime_adapter as module

    observation = {
        "runtime_python": "/canonical/runtime/python",
        "probe_results": (),
        "installed": (),
        "import_probe_passed": (),
        "errors": (),
    }
    calls = []

    def observe():
        calls.append("probe")
        return observation

    def visibility(probe_read_model=None):
        calls.append("visibility")
        assert probe_read_model is observation
        return {"registry": {"tools": ()}, "probe": probe_read_model}

    monkeypatch.setattr(module, "build_agent_tooling_runtime_probe_read_model", observe)
    monkeypatch.setattr(module, "build_jarvis_external_adapter_visibility_read_model", visibility)
    result = module.build_agent_tooling_runtime_adapter_read_model()

    assert calls == ["probe", "visibility"]
    assert result["probe"] is observation
    assert result["runtime_python"] == observation["runtime_python"]
    assert result["execution_allowed"] is False
