from __future__ import annotations

from tools.jarvis_live_runtime.jarvis_live_read_models import build_jarvis_live_tool_catalog_read_model


def test_tool_catalog_includes_external_adapters_smoke(monkeypatch) -> None:
    monkeypatch.setattr(
        "tools.jarvis_live_runtime.jarvis_live_read_models.build_jarvis_external_adapter_visibility_read_model",
        lambda: {
            "registry": {
                "tools": (
                    {"tool_id": "external_adapter:openai_agents_sdk"},
                    {"tool_id": "external_adapter:mcp_python_sdk"},
                    {"tool_id": "external_adapter:autogen_agentchat"},
                    {"tool_id": "external_adapter:autogen_ext"},
                    {"tool_id": "external_adapter:langgraph"},
                    {"tool_id": "external_adapter:autogen"},
                )
            },
            "adapters": (
                {
                    "tool_id": "external_adapter:openai_agents_sdk",
                    "availability_status": "available",
                    "selection_enabled": True,
                    "import_probe_worked": True,
                    "runtime_package_name": "openai-agents-python",
                    "runtime_import_name": "agents",
                    "activation_blocked_reason": "",
                },
                {
                    "tool_id": "external_adapter:mcp_python_sdk",
                    "availability_status": "available",
                    "selection_enabled": True,
                    "import_probe_worked": True,
                    "runtime_package_name": "mcp",
                    "runtime_import_name": "mcp",
                    "activation_blocked_reason": "",
                },
                {
                    "tool_id": "external_adapter:autogen_agentchat",
                    "availability_status": "available",
                    "selection_enabled": True,
                    "import_probe_worked": True,
                    "runtime_package_name": "autogen-agentchat",
                    "runtime_import_name": "autogen_agentchat",
                    "activation_blocked_reason": "",
                },
                {
                    "tool_id": "external_adapter:autogen_ext",
                    "availability_status": "available",
                    "selection_enabled": True,
                    "import_probe_worked": True,
                    "runtime_package_name": "autogen-ext",
                    "runtime_import_name": "autogen_ext",
                    "activation_blocked_reason": "",
                },
                {
                    "tool_id": "external_adapter:langgraph",
                    "availability_status": "available",
                    "selection_enabled": True,
                    "import_probe_worked": True,
                    "runtime_package_name": "langgraph",
                    "runtime_import_name": "langgraph",
                    "activation_blocked_reason": "",
                },
                {
                    "tool_id": "external_adapter:autogen",
                    "availability_status": "legacy_unavailable",
                    "selection_enabled": False,
                    "import_probe_worked": False,
                    "runtime_package_name": "pyautogen",
                    "runtime_import_name": "autogen",
                    "activation_blocked_reason": "legacy_alias_requires_importable_autogen_runtime",
                },
            ),
            "active_adapter_ids": (
                "external_adapter:openai_agents_sdk",
                "external_adapter:mcp_python_sdk",
                "external_adapter:autogen_agentchat",
                "external_adapter:autogen_ext",
                "external_adapter:langgraph",
            ),
            "visible_adapter_ids": (
                "external_adapter:openai_agents_sdk",
                "external_adapter:mcp_python_sdk",
                "external_adapter:autogen_agentchat",
                "external_adapter:autogen_ext",
                "external_adapter:langgraph",
            ),
            "unavailable_adapter_ids": ("external_adapter:autogen",),
            "legacy_adapter_ids": ("external_adapter:autogen",),
            "runtime_python": "/tmp/agent_tooling_python",
            "probe": {"runtime_python": "/tmp/agent_tooling_python", "probe_results": ()},
        },
    )

    catalog = build_jarvis_live_tool_catalog_read_model()

    assert catalog["external_adapter_tools"] == (
        "external_adapter:openai_agents_sdk",
        "external_adapter:mcp_python_sdk",
        "external_adapter:autogen_agentchat",
        "external_adapter:autogen_ext",
        "external_adapter:langgraph",
    )
    assert "external_adapter:autogen" in catalog["external_adapter_unavailable_tools"]
    assert "external_adapter:autogen" in catalog["external_adapter_legacy_tools"]
    assert "external_adapter:autogen" in catalog["external_adapter_registry_tools"]
    assert any(
        adapter["tool_id"] == "external_adapter:autogen" and adapter["availability_status"] == "legacy_unavailable"
        for adapter in catalog["external_adapter_runtime_status"]
    )
