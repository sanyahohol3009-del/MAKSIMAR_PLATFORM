from tools.jarvis_live_runtime.jarvis_live_brain_loop import (
    build_jarvis_live_brain_context,
    build_jarvis_live_project_status_read_model,
)


def test_brain_context_includes_session_history_project_boundaries() -> None:
    state = {
        "recent_turns": [
            {"role": "user", "text": "Джарвис, кто ты?"},
            {"role": "assistant", "text": "Я JARVIS."},
        ],
        "rolling_summary": "owner asked identity",
        "active_topics": ["identity"],
    }

    context = build_jarvis_live_brain_context("Что я спрашивал до этого?", state)
    read_model = context.to_read_model()
    prompt = context.to_prompt()

    assert read_model["recent_turn_count"] == 2
    assert read_model["pc_control_allowed"] is False
    assert read_model["canonical_memory_write_allowed"] is False
    assert "RECENT_SESSION_TURNS" in prompt
    assert "ROLLING_SESSION_SUMMARY" in prompt
    assert "RETRIEVED_LONG_TERM_MEMORY" in prompt or read_model["retrieved_snippets"] == ()


def test_fast_conversation_uses_session_memory_without_deep_retrieval() -> None:
    state = {
        "recent_turns": [
            {"role": "user", "text": "Мне нравится спокойный стиль общения."},
            {"role": "assistant", "text": "Понял, буду отвечать спокойно."},
        ],
        "rolling_summary": "owner prefers calm conversation",
        "active_topics": ["conversation"],
    }

    context = build_jarvis_live_brain_context("Джарвис, просто поговори со мной.", state)
    read_model = context.to_read_model()
    prompt = context.to_prompt()

    assert read_model["request_route"] == "conversation"
    assert read_model["route_mode"] == "FAST"
    assert read_model["retrieval_mode"] == "session_only"
    assert read_model["selected_model_role"]["model_id"] == "jarvis:chat8b"
    assert read_model["retrieval_surfaces_used"] == ("session_memory",)
    assert read_model["retrieved_snippet_count"] == 0
    assert "RECENT_SESSION_TURNS" in prompt
    assert "owner prefers calm conversation" in prompt
    assert read_model["pc_control_allowed"] is False


def test_project_status_read_model_is_read_only() -> None:
    payload = build_jarvis_live_project_status_read_model()

    assert payload["read_only"] is True
    assert payload["pc_control_allowed"] is False
    assert payload["canonical_memory_write_allowed"] is False
    assert "runtime_history_store" in payload["project_status"]
