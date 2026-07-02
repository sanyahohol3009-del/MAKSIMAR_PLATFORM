from __future__ import annotations

from tools.jarvis_live_runtime.jarvis_live_brain_loop import stream_jarvis_live_brain_response


def _patch_final_brain(monkeypatch, expected_prompt_markers: tuple[str, ...] = ()) -> list[str]:
    import tools.jarvis_live_runtime.jarvis_live_brain_loop as brain_loop

    prompts: list[str] = []

    def fake_stream(model_id: str, prompt: str, *args: object, **kwargs: object):
        prompts.append(str(prompt))
        for marker in expected_prompt_markers:
            assert marker in str(prompt)

        yield {
            "event": "chunk",
            "text": (
                "Собрал read-only evidence по retrieval/tool route и отвечаю своими словами. "
                "Опасные действия не выполнялись: direct_execution_allowed=false, "
                "pc_control_allowed=false, canonical_memory_write_allowed=false. "
                "Вижу qdrant_readonly_status, sqlite_vec_readonly, mgrep_readonly, repo_search, "
                "retrieval_backend_status_read_model и retrieval_tool_registry_contract."
            ),
        }
        yield {"event": "done", "ollama_model_used": model_id}

    monkeypatch.setattr(brain_loop, "_stream_ollama_model", fake_stream)
    monkeypatch.setattr(brain_loop, "SESSION_MEMORY_ROOT", brain_loop.PROJECT_ROOT)
    monkeypatch.setattr(brain_loop, "_load_session_state", lambda: brain_loop._empty_session_state())
    monkeypatch.setattr(brain_loop, "_save_session_state", lambda state: None)
    monkeypatch.setattr(brain_loop, "_append_local_chat_memory_record", lambda state, response, context: None)

    return prompts


def _done_for(
    text: str,
    monkeypatch,
    expected_prompt_markers: tuple[str, ...] = (),
) -> tuple[dict[str, object], list[str]]:
    prompts = _patch_final_brain(monkeypatch, expected_prompt_markers)
    events = list(stream_jarvis_live_brain_response(text, session_id="retrieval_semantic_router"))
    return events[-1], prompts


def _assert_final_brain_read_only(done: dict[str, object]) -> str:
    response = str(done["response_text"])

    assert done["grounded_answer"] is True
    assert done["ollama_called"] is True
    assert done["execution_allowed"] is False
    assert done["pc_control_allowed"] is False
    assert done["canonical_memory_write_allowed"] is False
    assert "отвечаю своими словами" in response
    assert "direct_execution_allowed=false" in response
    assert "pc_control_allowed=false" in response

    forbidden_user_visible_markers = (
        "[work] intent=",
        "Retrieval backend status read-only",
        "Project / repo read-only:",
        "чем могу помочь",
        "готов помочь",
        "скажи, что нужно",
    )
    for marker in forbidden_user_visible_markers:
        assert marker not in response

    return response


def test_retrieval_backend_status_routes_by_typo_with_grounded_final_brain(monkeypatch) -> None:
    done, prompts = _done_for(
        "что по qdrnt и aqlite-vec status?",
        monkeypatch,
        (
            "GROUNDING_INTENT_FAMILY: RETRIEVAL_BACKEND_STATUS",
            "qdrant_readonly_status",
            "retrieval_backend_status_read_model",
            "retrieval_tool_registry_contract",
        ),
    )
    response = _assert_final_brain_read_only(done)

    assert done["intent_family"] == "RETRIEVAL_BACKEND_STATUS"
    assert "qdrant_readonly_status" in done["selected_tools"]
    assert "qdrant_readonly_status" in response
    assert prompts


def test_retrieval_container_boundary_routes_with_grounded_final_brain(monkeypatch) -> None:
    done, prompts = _done_for(
        "docker можно запускать, qdrant container включен?",
        monkeypatch,
        (
            "GROUNDING_INTENT_FAMILY: CONTAINER_STATUS",
            "retrieval_container_contract",
            "retrieval_runtime_profile",
            "qdrant_container_status",
        ),
    )
    response = _assert_final_brain_read_only(done)

    assert done["intent_family"] == "CONTAINER_STATUS"
    assert "qdrant_container_status" in done["selected_tools"]
    assert "qdrant_readonly_status" in response or "retrieval" in response
    assert prompts


def test_retrieval_similarity_route_extracts_query_and_uses_sqlite_vec_guard_with_final_brain(monkeypatch) -> None:
    done, prompts = _done_for(
        "найди похожее на retrieval adapter contract",
        monkeypatch,
        (
            "GROUNDING_INTENT_FAMILY: SEMANTIC_SIMILARITY",
            "sqlite_vec_readonly",
            "repo_search",
        ),
    )
    response = _assert_final_brain_read_only(done)

    assert done["intent_family"] == "SEMANTIC_SIMILARITY"
    assert done["selected_tools"][0] == "sqlite_vec_readonly"
    assert "sqlite_vec_readonly" in response
    assert prompts


def test_retrieval_project_search_uses_mgrep_or_repo_search_fallback_with_final_brain(monkeypatch) -> None:
    done, prompts = _done_for(
        "найди где source_ref",
        monkeypatch,
        (
            "GROUNDING_INTENT_FAMILY: PROJECT_SEARCH",
            "repo_search",
        ),
    )
    response = _assert_final_brain_read_only(done)

    assert done["intent_family"] == "PROJECT_SEARCH"
    assert done["selected_tools"][0] in {"mgrep_readonly", "repo_search"}
    assert "repo_search" in response or "mgrep_readonly" in response
    assert prompts


def test_tool_catalog_question_routes_with_grounded_final_brain(monkeypatch) -> None:
    done, prompts = _done_for(
        "какие tools тебе доступны",
        monkeypatch,
        (
            "GROUNDING_INTENT_FAMILY: TOOL_CATALOG",
            "mgrep_readonly",
            "sqlite_vec_readonly",
            "qdrant_readonly_status",
        ),
    )
    response = _assert_final_brain_read_only(done)

    assert done["intent_family"] == "TOOL_CATALOG"
    assert done["execution_allowed"] is False
    assert "mgrep_readonly" in response
    assert "sqlite_vec_readonly" in response
    assert "qdrant_readonly_status" in response
    assert prompts


def test_capabilities_question_routes_to_tool_catalog_with_grounded_final_brain(monkeypatch) -> None:
    done, prompts = _done_for(
        "что ты умеешь",
        monkeypatch,
        (
            "GROUNDING_INTENT_FAMILY: TOOL_CATALOG",
            "TOOL_CATALOG",
        ),
    )
    response = _assert_final_brain_read_only(done)

    assert done["intent_family"] == "TOOL_CATALOG"
    assert done["execution_allowed"] is False
    assert "отвечаю своими словами" in response
    assert prompts
