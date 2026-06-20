from __future__ import annotations

from MAKSIMAR_CORE_LIB.action_library_adapters.external_tool_library_adapter import (
    select_external_adapter_tools_for_text,
)
from tools.jarvis_live_runtime.autonomous_tool_model_router import build_autonomous_tool_model_decision
from tools.jarvis_live_runtime.owner_identity_claim import OwnerIdentityClaim


def _verified_terminal_claim() -> OwnerIdentityClaim:
    return OwnerIdentityClaim(
        claim_id="external_adapter_visibility_verified_terminal_v1",
        source="local_terminal_session",
        verified=True,
        verification_method="test_override",
        session_token_present=False,
        process_owner_matches_os_user=True,
        reason_codes=("os_user_verified",),
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

    selected = select_external_adapter_tools_for_text("Use AutoGen and LangGraph with MCP.")
    selected_tool_ids = tuple(tool.tool_id for tool in selected)
    decision = build_autonomous_tool_model_decision(
        "сравни LangGraph и AutoGen для задачи",
        input_channel="text",
        owner_identity_claim=_verified_terminal_claim(),
    )

    assert "external_adapter:autogen" not in selected_tool_ids
    assert "external_adapter:autogen_agentchat" in selected_tool_ids
    assert "external_adapter:autogen_ext" in selected_tool_ids
    assert "external_adapter:mcp_python_sdk" in selected_tool_ids
    assert "external_adapter:autogen" not in decision["selected_tools"]
    assert "external_adapter:autogen_agentchat" in decision["selected_tools"]
    assert "external_adapter:autogen_ext" in decision["selected_tools"]
