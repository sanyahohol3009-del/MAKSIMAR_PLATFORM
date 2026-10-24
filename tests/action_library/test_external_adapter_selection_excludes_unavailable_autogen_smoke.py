from __future__ import annotations

from MAKSIMAR_CORE_LIB.action_library_adapters.external_tool_library_adapter import (
    normalize_external_adapter_tool_ids,
)
def test_external_adapter_selection_excludes_unavailable_autogen_smoke(monkeypatch) -> None:
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

    selected_tool_ids = normalize_external_adapter_tool_ids((
        "external_adapter:autogen", "external_adapter:autogen_agentchat",
        "external_adapter:autogen_ext", "external_adapter:mcp_python_sdk",
    ))
    assert "external_adapter:autogen" not in selected_tool_ids
    assert "external_adapter:autogen_agentchat" in selected_tool_ids
    assert "external_adapter:autogen_ext" in selected_tool_ids
    assert "external_adapter:mcp_python_sdk" in selected_tool_ids
