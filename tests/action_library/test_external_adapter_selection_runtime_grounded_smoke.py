from __future__ import annotations

from MAKSIMAR_CORE_LIB.action_library_adapters.external_tool_library_adapter import (
    build_external_adapter_semantic_route,
    rank_external_adapter_candidates_for_text,
)


def _fake_probe_payload() -> dict[str, object]:
    return {
        "runtime_python": "/tmp/agent_tooling_python",
        "probe_results": (
            {"package_name": "openai-agents-python", "import_name": "agents", "installed": True, "import_probe_passed": True, "runtime_python": "/tmp/agent_tooling_python", "version_if_available": "1.0.0", "errors": ()},
            {"package_name": "mcp", "import_name": "mcp", "installed": True, "import_probe_passed": True, "runtime_python": "/tmp/agent_tooling_python", "version_if_available": "1.0.0", "errors": ()},
            {"package_name": "autogen-agentchat", "import_name": "autogen_agentchat", "installed": True, "import_probe_passed": True, "runtime_python": "/tmp/agent_tooling_python", "version_if_available": "1.0.0", "errors": ()},
            {"package_name": "autogen-ext", "import_name": "autogen_ext", "installed": True, "import_probe_passed": True, "runtime_python": "/tmp/agent_tooling_python", "version_if_available": "1.0.0", "errors": ()},
            {"package_name": "langgraph", "import_name": "langgraph", "installed": True, "import_probe_passed": True, "runtime_python": "/tmp/agent_tooling_python", "version_if_available": "1.0.0", "errors": ()},
            {"package_name": "pyautogen", "import_name": "autogen", "installed": False, "import_probe_passed": False, "runtime_python": "/tmp/agent_tooling_python", "version_if_available": "", "errors": ("ModuleNotFoundError:autogen",)},
        ),
        "installed": ("openai-agents-python", "mcp", "autogen-agentchat", "autogen-ext", "langgraph"),
        "import_probe_passed": ("openai-agents-python", "mcp", "autogen-agentchat", "autogen-ext", "langgraph"),
        "errors": (("ModuleNotFoundError:autogen",),),
    }


def test_external_adapter_selection_runtime_grounded_smoke(monkeypatch) -> None:
    monkeypatch.setattr(
        "MAKSIMAR_CORE_LIB.action_library_adapters.external_tool_library_adapter._load_agent_tooling_runtime_probe_read_model",
        _fake_probe_payload,
    )

    selection = build_external_adapter_semantic_route("подключи протокол инструментов для внешнего агента")
    comparison = build_external_adapter_semantic_route("сравнение graph workflow и autogen")
    candidates = rank_external_adapter_candidates_for_text("подключи протокол инструментов для внешнего агента")

    assert selection["matched"] is True
    assert selection["intent_family"] == "EXTERNAL_ADAPTER_SELECTION"
    assert selection["selected_tools"] == ("external_adapter:mcp_python_sdk",)
    assert candidates[0]["tool_id"] == "external_adapter:mcp_python_sdk"
    assert "protocol" in candidates[0]["reason"] or "tool" in candidates[0]["reason"]

    assert comparison["intent_family"] == "AGENT_ENGINE_COMPARISON"
    assert "external_adapter:langgraph" in comparison["selected_tools"]
    assert "external_adapter:autogen_agentchat" in comparison["selected_tools"]
    assert "external_adapter:autogen_ext" in comparison["selected_tools"]
    assert "external_adapter:autogen" not in comparison["selected_tools"]
