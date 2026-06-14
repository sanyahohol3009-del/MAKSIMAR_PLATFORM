from __future__ import annotations

from tools.jarvis_live_runtime.jarvis_live_brain_loop import stream_jarvis_live_brain_response


def _disable_ollama(monkeypatch) -> None:
    import tools.jarvis_live_runtime.jarvis_live_brain_loop as brain_loop

    def fail_stream(*args: object, **kwargs: object):
        raise AssertionError("semantic retrieval route must answer before Ollama free generation")
        yield {}

    monkeypatch.setattr(brain_loop, "_stream_ollama_model", fail_stream)
    monkeypatch.setattr(brain_loop, "SESSION_MEMORY_ROOT", brain_loop.PROJECT_ROOT)
    monkeypatch.setattr(brain_loop, "_load_session_state", lambda: brain_loop._empty_session_state())
    monkeypatch.setattr(brain_loop, "_save_session_state", lambda state: None)
    monkeypatch.setattr(brain_loop, "_append_local_chat_memory_record", lambda state, response, context: None)


def _done_for(text: str, monkeypatch) -> dict[str, object]:
    _disable_ollama(monkeypatch)
    events = list(stream_jarvis_live_brain_response(text, session_id="retrieval_semantic_router"))
    return events[-1]


def test_retrieval_backend_status_routes_by_typo_without_ollama(monkeypatch) -> None:
    done = _done_for("что по qdrnt и aqlite-vec status?", monkeypatch)
    response = str(done["response_text"])

    assert done["intent_family"] == "RETRIEVAL_BACKEND_STATUS"
    assert "qdrant_readonly_status" in done["selected_tools"]
    assert done["ollama_called"] is False
    assert "Retrieval backend status read-only" in response
    assert "vendor_acquired=true" in response
    assert "read_only_tool_routing_enabled=true" in response
    assert "auto_routing_readonly_enabled=true" in response
    assert "backend_runtime_enabled=false" in response
    assert "qdrant_network_service_adapter_candidate=true" in response
    assert "qdrant_runtime_readonly: source_present=true usable_now=false selected_tool=qdrant_readonly_status" in response
    assert "runtime_enabled=false" in response
    assert "direct_execution_allowed=false" in response
    assert done["canonical_memory_write_allowed"] is False


def test_retrieval_container_boundary_routes_without_ollama(monkeypatch) -> None:
    done = _done_for("docker можно запускать, qdrant container включен?", monkeypatch)
    response = str(done["response_text"])

    assert done["intent_family"] == "CONTAINER_STATUS"
    assert done["ollama_called"] is False
    assert "container_ready=true" in response
    assert "runtime_enabled=false" in response
    assert "qdrant_container_enabled=false" in response


def test_retrieval_similarity_route_returns_create_extend_adapter_recommendation(monkeypatch) -> None:
    done = _done_for("проверь semantic duplicate risk для retrieval adapter, CREATE или EXTEND?", monkeypatch)
    response = str(done["response_text"])

    assert done["intent_family"] == "SEMANTIC_SIMILARITY"
    assert done["selected_tools"][0] == "sqlite_vec_readonly"
    assert done["ollama_called"] is False
    assert "primary_tool=sqlite_vec_readonly" in response
    assert "effective_tool=repo_search" in response or "effective_tool=sqlite_vec_readonly" in response
    assert "sqlite_vec_source_present=true" in response
    assert "CREATE_EXTEND_ADAPTER_RECOMMENDATION=" in response
    assert "direct_execution_allowed=false" in response


def test_retrieval_project_search_uses_mgrep_or_repo_search_fallback(monkeypatch) -> None:
    done = _done_for("найди где source_ref", monkeypatch)
    response = str(done["response_text"])

    assert done["intent_family"] == "PROJECT_SEARCH"
    assert done["selected_tools"][0] == "mgrep_readonly"
    assert done["ollama_called"] is False
    assert "primary_tool=mgrep_readonly" in response
    assert "effective_tool=repo_search" in response or "effective_tool=mgrep_readonly" in response
    assert "mgrep_source_present=true" in response
    assert "source_ref" in response
    assert done["canonical_memory_write_allowed"] is False
