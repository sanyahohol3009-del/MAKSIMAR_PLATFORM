from __future__ import annotations

from MAKSIMAR_CORE_LIB.action_library_adapters.external_tool_library_adapter import (
    build_jarvis_external_adapter_visibility_read_model,
)


def test_agent_tooling_adapters_visible_to_jarvis_smoke(monkeypatch) -> None:
    monkeypatch.setattr(
        "MAKSIMAR_CORE_LIB.action_library_adapters.external_tool_library_adapter._load_agent_tooling_runtime_probe_read_model",
        lambda: {
            "runtime_python": "/tmp/agent_tooling_python",
            "probe_results": (
                {
                    "package_name": "openai-agents-python",
                    "import_name": "agents",
                    "installed": True,
                    "import_probe_passed": True,
                    "runtime_python": "/tmp/agent_tooling_python",
                    "version_if_available": "1.0.0",
                    "errors": (),
                },
                {
                    "package_name": "mcp",
                    "import_name": "mcp",
                    "installed": True,
                    "import_probe_passed": True,
                    "runtime_python": "/tmp/agent_tooling_python",
                    "version_if_available": "1.0.0",
                    "errors": (),
                },
                {
                    "package_name": "autogen-agentchat",
                    "import_name": "autogen_agentchat",
                    "installed": True,
                    "import_probe_passed": True,
                    "runtime_python": "/tmp/agent_tooling_python",
                    "version_if_available": "1.0.0",
                    "errors": (),
                },
                {
                    "package_name": "autogen-ext",
                    "import_name": "autogen_ext",
                    "installed": True,
                    "import_probe_passed": True,
                    "runtime_python": "/tmp/agent_tooling_python",
                    "version_if_available": "1.0.0",
                    "errors": (),
                },
                {
                    "package_name": "langgraph",
                    "import_name": "langgraph",
                    "installed": True,
                    "import_probe_passed": True,
                    "runtime_python": "/tmp/agent_tooling_python",
                    "version_if_available": "1.0.0",
                    "errors": (),
                },
                {
                    "package_name": "pyautogen",
                    "import_name": "autogen",
                    "installed": False,
                    "import_probe_passed": False,
                    "runtime_python": "/tmp/agent_tooling_python",
                    "version_if_available": "",
                    "errors": ("ModuleNotFoundError:autogen",),
                },
            ),
            "installed": (
                "openai-agents-python",
                "mcp",
                "autogen-agentchat",
                "autogen-ext",
                "langgraph",
            ),
            "import_probe_passed": (
                "openai-agents-python",
                "mcp",
                "autogen-agentchat",
                "autogen-ext",
                "langgraph",
            ),
            "errors": (("ModuleNotFoundError:autogen",),),
        },
    )

    payload = build_jarvis_external_adapter_visibility_read_model()
    assert len(payload["registry"]["tools"]) >= 6
    assert "external_adapter:autogen_agentchat" in tuple(tool["tool_id"] for tool in payload["registry"]["tools"])
    assert "external_adapter:autogen_ext" in tuple(tool["tool_id"] for tool in payload["registry"]["tools"])
    assert all(adapter["visible_to_jarvis"] is True for adapter in payload["adapters"])
    assert payload["active_adapter_ids"] == (
        "external_adapter:openai_agents_sdk",
        "external_adapter:mcp_python_sdk",
        "external_adapter:autogen_agentchat",
        "external_adapter:autogen_ext",
        "external_adapter:langgraph",
    )
    assert payload["legacy_adapter_ids"] == ("external_adapter:autogen",)
