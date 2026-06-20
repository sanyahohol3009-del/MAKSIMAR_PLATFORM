from __future__ import annotations

from MAKSIMAR_CORE_LIB.action_library_adapters.external_tool_library_adapter import (
    build_jarvis_external_adapter_visibility_read_model,
    select_external_adapter_tools_for_text,
)


def test_agent_tooling_adapters_visible_to_jarvis_smoke() -> None:
    payload = build_jarvis_external_adapter_visibility_read_model()
    selected = select_external_adapter_tools_for_text(
        "Use LangGraph or AutoGen for a graph agent experiment, and inspect MCP support."
    )
    tool_ids = tuple(tool.tool_id for tool in selected)

    assert len(payload["registry"]["tools"]) == 6
    assert "external_adapter:langgraph" in tool_ids
    assert "external_adapter:autogen" in tool_ids
    assert "external_adapter:autogen_agentchat" in tuple(tool["tool_id"] for tool in payload["registry"]["tools"])
    assert "external_adapter:autogen_ext" in tuple(tool["tool_id"] for tool in payload["registry"]["tools"])
    assert "external_adapter:mcp_python_sdk" in tool_ids
    assert all(adapter["visible_to_jarvis"] is True for adapter in payload["adapters"])
