from __future__ import annotations

from tools.jarvis_live_runtime.jarvis_live_brain_loop import stream_jarvis_live_brain_response


def _disable_ollama(monkeypatch) -> None:
    import tools.jarvis_live_runtime.jarvis_live_brain_loop as brain_loop

    def fail_stream(*args: object, **kwargs: object):
        raise AssertionError("agent catalog route must answer before Ollama free generation")
        yield {}

    monkeypatch.setattr(brain_loop, "_stream_ollama_model", fail_stream)
    monkeypatch.setattr(brain_loop, "SESSION_MEMORY_ROOT", brain_loop.PROJECT_ROOT)
    monkeypatch.setattr(brain_loop, "_load_session_state", lambda: brain_loop._empty_session_state())
    monkeypatch.setattr(brain_loop, "_save_session_state", lambda state: None)
    monkeypatch.setattr(brain_loop, "_append_local_chat_memory_record", lambda state, response, context: None)


def test_agent_catalog_grounded_response_smoke(monkeypatch) -> None:
    _disable_ollama(monkeypatch)

    events = list(stream_jarvis_live_brain_response("каких агентов ты видишь", session_id="agent_catalog_grounded"))
    done = events[-1]
    response = str(done["response_text"])

    assert done["intent_family"] == "AGENT_CATALOG"
    assert done["ollama_called"] is False
    assert "Grounded agent catalog:" in response
    assert "tool_selector_agent" in response
    assert "project_coder_agent" in response
    assert "architect_agent" in response
    assert "safety_guard_agent" in response
    assert "action_worker_agent" in response
    assert "external_adapter_selector_agent=not_present_in_canonical_swarm_roles" in response
    assert "pc_control_allowed=false" in response
