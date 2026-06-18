from __future__ import annotations

import inspect

from tools.jarvis_live_runtime import jarvis_live_brain_loop
from tools.jarvis_live_runtime import jarvis_live_guarded_answer_engine


def test_brain_loop_uses_extracted_guarded_answer_boundary() -> None:
    assert inspect.getmodule(jarvis_live_brain_loop._answer_conversation_style_complaint_if_grounded).__name__ == (
        "tools.jarvis_live_runtime.jarvis_live_guarded_answer_engine"
    )
    assert inspect.getmodule(jarvis_live_brain_loop._answer_style_memory_recall_if_grounded).__name__ == (
        "tools.jarvis_live_runtime.jarvis_live_guarded_answer_engine"
    )
    assert inspect.getmodule(jarvis_live_brain_loop._asks_pc_action).__name__ == (
        "tools.jarvis_live_runtime.jarvis_live_guarded_answer_engine"
    )


def test_guarded_answer_engine_keeps_pc_actions_blocked() -> None:
    assert jarvis_live_guarded_answer_engine._asks_pc_action("джарвис открой браузер") is True
    assert jarvis_live_guarded_answer_engine._asks_pc_action("джарвис привет") is False


def test_guarded_answer_engine_detects_template_complaints() -> None:
    assert jarvis_live_guarded_answer_engine._asks_template_style_complaint("ты опять отвечаешь шаблоном") is True
    assert jarvis_live_guarded_answer_engine._asks_template_style_complaint("покажи статус проекта") is False
