from __future__ import annotations

from tools.jarvis_live_runtime.jarvis_live_brain_loop import stream_jarvis_live_brain_response


def test_skill_visibility_grounded_response_smoke(monkeypatch) -> None:
    import tools.jarvis_live_runtime.jarvis_live_brain_loop as brain_loop

    prompts: list[str] = []

    def fake_stream(model_id: str, prompt: str, *args: object, **kwargs: object):
        prompts.append(str(prompt))

        assert "GROUNDING_INTENT_FAMILY: SKILL_VISIBILITY" in str(prompt)
        assert "build_jarvis_skill_visibility_read_model" in str(prompt) or "SKILL_VISIBILITY" in str(prompt)

        yield {
            "event": "chunk",
            "text": (
                "Вижу read-only карту навыков и отвечаю своими словами. "
                "Навыки доступны только как безопасная видимость/подсказка: "
                "execution_allowed=false, pc_control_allowed=false, "
                "canonical_memory_write_allowed=false."
            ),
        }
        yield {"event": "done", "ollama_model_used": model_id}

    monkeypatch.setattr(brain_loop, "_stream_ollama_model", fake_stream)
    monkeypatch.setattr(brain_loop, "_load_session_state", lambda: brain_loop._empty_session_state())
    monkeypatch.setattr(brain_loop, "_save_session_state", lambda state: None)
    monkeypatch.setattr(brain_loop, "_append_local_chat_memory_record", lambda state, response, context: None)

    events = list(
        stream_jarvis_live_brain_response(
            "какие навыки доступны",
            session_id="skill_visibility_grounded",
        )
    )
    done = events[-1]
    response = str(done["response_text"])

    assert done["intent_family"] == "SKILL_VISIBILITY"
    assert done["grounded_answer"] is True
    assert done["ollama_called"] is True
    assert done["read_only"] is True
    assert done["execution_allowed"] is False
    assert done["pc_control_allowed"] is False
    assert done["canonical_memory_write_allowed"] is False

    assert "отвечаю своими словами" in response
    assert "execution_allowed=false" in response
    assert "pc_control_allowed=false" in response
    assert "canonical_memory_write_allowed=false" in response

    forbidden_user_visible_markers = (
        "[work] intent=",
        "Skill visibility read-only",
        "Project / repo read-only:",
        "чем могу помочь",
        "готов помочь",
        "скажи, что нужно",
    )
    for marker in forbidden_user_visible_markers:
        assert marker not in response

    assert prompts
