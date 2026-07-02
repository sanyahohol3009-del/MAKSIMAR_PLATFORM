from __future__ import annotations

import inspect

from tools.jarvis_live_runtime import jarvis_live_brain_loop
from tools.jarvis_live_runtime import jarvis_live_project_answer_engine


def test_brain_loop_uses_extracted_project_answer_engine() -> None:
    assert inspect.getmodule(jarvis_live_brain_loop._answer_with_read_only_tools_if_grounded).__name__ == (
        "tools.jarvis_live_runtime.jarvis_live_project_answer_engine"
    )
    assert inspect.getmodule(jarvis_live_brain_loop._format_project_status_answer).__name__ == (
        "tools.jarvis_live_runtime.jarvis_live_project_answer_engine"
    )
    assert inspect.getmodule(jarvis_live_brain_loop._format_tool_catalog_answer).__name__ == (
        "tools.jarvis_live_runtime.jarvis_live_project_answer_engine"
    )


def test_project_answer_engine_keeps_action_requests_proposal_only() -> None:
    answer = jarvis_live_project_answer_engine._format_action_request_proposal_answer(
        "джарвис запусти команду на пк"
    )
    assert "Operator proposal only" in answer
    assert "пока нет tool_result" in answer
    assert "PC control, shell execution, canonical writes, and deployment stay blocked" in answer


def test_project_answer_engine_help_is_read_command_surface() -> None:
    answer = jarvis_live_project_answer_engine._format_project_help()
    assert "/project status" in answer
    assert "/project file" in answer
    assert "/project safety" in answer
