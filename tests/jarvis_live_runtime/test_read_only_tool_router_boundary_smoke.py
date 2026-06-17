from __future__ import annotations

import inspect

from tools.jarvis_live_runtime import jarvis_live_brain_loop
from tools.jarvis_live_runtime import read_only_tool_router


def test_read_only_tool_plan_router_moved_out_of_brain_loop() -> None:
    assert inspect.getmodule(jarvis_live_brain_loop._build_read_only_tool_plan).__name__ == (
        "tools.jarvis_live_runtime.read_only_tool_router"
    )


def test_project_search_is_read_only_and_does_not_need_ollama() -> None:
    plan = read_only_tool_router._build_read_only_tool_plan("где у нас terminal chat?", object())
    assert plan["intent_family"] == "PROJECT_SEARCH"
    assert plan["read_only"] is True
    assert plan["execution_allowed"] is False
    assert plan["needs_ollama"] is False
    assert "repo_search" in plan["selected_tools"]


def test_action_request_is_proposal_only_not_execution() -> None:
    plan = read_only_tool_router._build_read_only_tool_plan("Джарвис сделай коммит", object())
    assert plan["intent_family"] == "ACTION_REQUEST"
    assert plan["read_only"] is True
    assert plan["execution_allowed"] is False
    assert plan["needs_ollama"] is False
    assert "operator_proposal" in plan["selected_tools"]


def test_model_status_routes_to_read_only_model_tools() -> None:
    plan = read_only_tool_router._build_read_only_tool_plan("что по моделям ollama runtime?", object())
    assert plan["intent_family"] == "MODEL_STATUS"
    assert plan["read_only"] is True
    assert plan["execution_allowed"] is False
    assert plan["needs_ollama"] is False
    assert "model_runtime_status" in plan["selected_tools"]
