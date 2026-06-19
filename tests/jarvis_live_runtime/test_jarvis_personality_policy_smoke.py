from __future__ import annotations

from pathlib import Path

import pytest

from tools.jarvis_live_runtime.jarvis_personality_policy import (
    assert_no_generic_tail,
    resolve_response_mode,
)
from tools.jarvis_live_runtime.memory_context_builder import build_jarvis_live_brain_context


def test_canonical_personality_prompt_is_active() -> None:
    context = build_jarvis_live_brain_context(
        "Джарвис, просто поговори со мной.",
        {
            "recent_turns": [{"role": "user", "text": "Мне нравится спокойный стиль общения."}],
            "rolling_summary": "owner prefers calm conversation",
            "active_topics": ["conversation"],
        },
    )
    prompt = context.to_prompt()

    assert "JARVIS_PERSONALITY_CANONICAL_POLICY_V1" in prompt
    assert "second brain" in prompt
    assert "engineering companion" in prompt
    assert "not a slave" in prompt
    assert "not a template chatbot" in prompt
    assert "THINKING_FREEDOM" in prompt
    assert "ACTION_SAFETY" in prompt
    assert "ANTI_TEMPLATE_RULES" in prompt
    assert "RESPONSE_MODE: conversation" in prompt
    assert "pc_control_allowed=false" in prompt
    assert "canonical_memory_write_allowed=false" in prompt
    assert "approval_required=true" in prompt
    assert "owner prefers calm conversation" in prompt


def test_runtime_uses_canonical_personality_source() -> None:
    memory_builder = Path("tools/jarvis_live_runtime/memory_context_builder.py").read_text(
        encoding="utf-8"
    )
    brain_loop = Path("tools/jarvis_live_runtime/jarvis_live_brain_loop.py").read_text(
        encoding="utf-8"
    )

    assert "build_jarvis_personality_prompt" in memory_builder
    assert "jarvis_personality_policy" in brain_loop or "build_jarvis_personality_prompt" in memory_builder


def test_project_question_gets_project_engineer_mode() -> None:
    context = build_jarvis_live_brain_context(
        "Брат, проверь проект и найди риск в control-plane.",
        {"recent_turns": [], "rolling_summary": "", "active_topics": []},
    )
    prompt = context.to_prompt()

    assert "RESPONSE_MODE: project_engineer" in prompt
    assert "MODEL_SELECTION_TRACE" in prompt
    assert "ACTION_SAFETY" in prompt


def test_action_request_requires_approval_mode() -> None:
    mode = resolve_response_mode(
        request_route="conversation",
        user_text="Джарвис, открой браузер",
        selected_model_role={"route_reason": "pc_action_request_proposal_only"},
    )
    assert mode == "approval_required"


def test_generic_tails_are_rejected() -> None:
    with pytest.raises(ValueError, match="Forbidden generic"):
        assert_no_generic_tail("Скажи, что нужно")
