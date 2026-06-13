from tools.jarvis_live_runtime.jarvis_live_brain_loop import (
    build_jarvis_live_brain_context,
    build_jarvis_live_memory_federation_status,
    run_jarvis_live_brain_once,
    stream_jarvis_live_brain_response,
)


def test_memory_federation_inventory_reports_existing_surfaces() -> None:
    status = build_jarvis_live_memory_federation_status()
    surfaces = {surface["surface_id"]: surface for surface in status["surfaces"]}

    assert status["memory_federation_available"] is True
    assert status["memory_surfaces_detected_count"] >= 6
    assert "runtime_history_store" in surfaces
    assert "memory_engine_registry" in surfaces
    assert "enterprise_business_memory" in surfaces
    assert "regulatory_memory_foundation" in surfaces
    assert "mempalace_read_only_sandbox" in surfaces
    assert surfaces["mempalace_read_only_sandbox"]["status"] == "sandbox_only"
    assert status["mempalace_status"] in {
        "sandbox_only_read_only",
        "sandbox_only_manual_review_required",
        "not_connected",
    }
    assert status["canonical_memory_write_allowed"] is False
    assert status["pc_control_allowed"] is False


def test_context_assembly_includes_mocked_multiple_memory_surfaces(monkeypatch) -> None:
    import tools.jarvis_live_runtime.jarvis_live_brain_loop as brain_loop

    monkeypatch.setattr(
        brain_loop,
        "_retrieve_history_snippets",
        lambda text, deep: ["runtime_history_store: MAKSIMAR project history"],
    )
    monkeypatch.setattr(
        brain_loop,
        "_retrieve_enterprise_memory_snippets",
        lambda text: ["enterprise_business_memory: sovereign AI sales memory"],
    )
    monkeypatch.setattr(
        brain_loop,
        "_retrieve_regulatory_memory_snippets",
        lambda text: ["regulatory_memory_foundation: laws memory"],
    )
    monkeypatch.setattr(
        brain_loop,
        "_retrieve_mempalace_status_snippets",
        lambda text: ["mempalace_read_only_sandbox: sandbox only"],
    )

    context = build_jarvis_live_brain_context(
        "Что у нас есть по продаже суверенного ИИ и regulatory memory MemPalace?",
        {"recent_turns": [], "rolling_summary": "", "active_topics": []},
    )
    read_model = context.to_read_model()

    assert read_model["retrieved_snippet_count"] >= 4
    assert "runtime_history_store" in read_model["retrieval_surfaces_used"]
    assert "enterprise_business_memory" in read_model["retrieval_surfaces_used"]
    assert "regulatory_memory_foundation" in read_model["retrieval_surfaces_used"]
    assert "mempalace_read_only_sandbox" in read_model["retrieval_surfaces_used"]
    assert read_model["canonical_memory_write_allowed"] is False
    assert read_model["pc_control_allowed"] is False


def test_new_chat_context_loads_stable_style_profile() -> None:
    context = build_jarvis_live_brain_context(
        "Джарвис, привет",
        {"recent_turns": [], "rolling_summary": "", "active_topics": []},
    )
    read_model = context.to_read_model()
    profile = read_model["stable_style_profile"]

    assert profile["user_name"] == "Александр"
    assert profile["assistant_identity"] == "JARVIS"
    assert "брат" in profile["relation_style"]
    assert "not template-like" in profile["communication_style"]
    assert read_model["memory_truth_split"]["local_chat_memory"] == "append_only_terminal_chat_memory"
    assert read_model["dangerous_mutation_flags"]["direct_core_write_allowed"] is False
    assert read_model["dangerous_mutation_flags"]["pc_control_enabled"] is False


def test_fast_context_includes_rolling_summary_and_style_profile() -> None:
    context = build_jarvis_live_brain_context(
        "Джарвис, просто поговори",
        {
            "recent_turns": [{"role": "user", "text": "я люблю прямой стиль"}],
            "rolling_summary": "owner prefers direct garage partner style",
            "active_topics": ["style"],
        },
    )
    prompt = context.to_prompt()

    assert "STABLE_STYLE_PROFILE" in prompt
    assert "owner prefers direct garage partner style" in prompt
    assert "MEMORY_TRUTH_SPLIT" in prompt
    assert "Never claim 'I remember'" in prompt


def test_local_terminal_turns_are_append_only_persisted_by_existing_session_log() -> None:
    from pathlib import Path

    source = Path("tools/jarvis_live_runtime/jarvis_live_brain_loop.py").read_text(encoding="utf-8")

    assert 'SESSION_TURN_LOG_NAME = "jarvis_live_terminal_turns.jsonl"' in source
    assert '.open("a", encoding="utf-8")' in source
    assert '"source": "jarvis_terminal_chat"' in source
    assert '"thinking_stored": False' in source
    assert '"direct_global_memory_write": False' in source


def test_second_request_in_same_session_sees_first_exchange(monkeypatch) -> None:
    import tools.jarvis_live_runtime.jarvis_live_brain_loop as brain_loop

    state = brain_loop._empty_session_state()
    prompts: list[str] = []

    def fake_load():
        return state

    def fake_save(updated):
        import copy

        snapshot = copy.deepcopy(updated)
        state.clear()
        state.update(snapshot)

    def fake_stream(model_id, prompt, route_mode, timeout_seconds=None, response_mode_text=None):
        prompts.append(prompt)
        yield {"event": "chunk", "text": "Ответ.", "ollama_model_used": model_id, "pc_control_allowed": False}
        yield {"event": "done", "ollama_model_used": model_id, "pc_control_allowed": False}

    monkeypatch.setattr(brain_loop, "_load_session_state", fake_load)
    monkeypatch.setattr(brain_loop, "_save_session_state", fake_save)
    monkeypatch.setattr(brain_loop, "_append_local_chat_memory_record", lambda state, response, context: None)
    monkeypatch.setattr(brain_loop, "_stream_ollama_model", fake_stream)

    list(stream_jarvis_live_brain_response("Джарвис, мой стиль прямой.", session_id="terminal_a"))
    list(stream_jarvis_live_brain_response("Джарвис, продолжай разговор.", session_id="terminal_a"))

    assert "мой стиль прямой" in prompts[-1]
    assert "ROLLING_SESSION_SUMMARY" in prompts[-1]
    assert "RECENT_SESSION_TURNS" in prompts[-1]


def test_new_process_can_load_previous_local_chat_memory(monkeypatch) -> None:
    import tools.jarvis_live_runtime.jarvis_live_brain_loop as brain_loop

    monkeypatch.setattr(
        brain_loop,
        "_read_recent_local_chat_records",
        lambda limit=8: (
            {
                "source": "jarvis_terminal_chat",
                "day_bucket": "2026-06-13",
                "user_message": "Александр любит прямой стиль.",
                "jarvis_answer": "Принял прямой стиль.",
            },
        ),
    )

    context = build_jarvis_live_brain_context(
        "Напомни про прямой стиль",
        {"recent_turns": [], "rolling_summary": "", "active_topics": []},
        session_id="new_process",
    )

    assert context.local_chat_memory_snippets
    assert "прямой стиль" in context.local_chat_memory_snippets[0].casefold()


def test_style_memory_recall_returns_grounded_non_template_answer(monkeypatch) -> None:
    import tools.jarvis_live_runtime.jarvis_live_brain_loop as brain_loop

    monkeypatch.setattr(brain_loop, "_load_session_state", lambda: brain_loop._empty_session_state())
    monkeypatch.setattr(brain_loop, "_save_session_state", lambda state: None)
    monkeypatch.setattr(brain_loop, "_read_recent_local_chat_records", lambda limit=8: ())
    monkeypatch.setattr(brain_loop, "_append_local_chat_memory_record", lambda state, response, context: None)

    events = list(
        stream_jarvis_live_brain_response(
            "джарвис ты помнишь как я хочу чтобы ты со мной общался?",
            session_id="style_recall",
        )
    )
    done = events[-1]
    answer = done["response_text"]
    lowered = answer.casefold()

    assert "брат" in lowered
    assert "напарник" in lowered
    assert "гараж" in lowered
    assert "не слишком коротко" in lowered
    assert "Скажи, что нужно" not in answer
    assert "Нужна помощь?" not in answer
    assert done["canonical_memory_write_allowed"] is False
    assert done["pc_control_allowed"] is False


def test_project_workspace_question_returns_complete_grounded_answer_without_ollama(monkeypatch) -> None:
    import tools.jarvis_live_runtime.jarvis_live_brain_loop as brain_loop

    monkeypatch.setattr(brain_loop, "_load_session_state", lambda: brain_loop._empty_session_state())
    monkeypatch.setattr(brain_loop, "_save_session_state", lambda state: None)
    monkeypatch.setattr(brain_loop, "_append_local_chat_memory_record", lambda state, response, context: None)

    def fail_stream(*args, **kwargs):
        raise AssertionError("project workspace summary must not call Ollama")

    monkeypatch.setattr(brain_loop, "_stream_ollama_model", fail_stream)

    events = list(
        stream_jarvis_live_brain_response(
            "джарвис что ты видишь по структуре проекта и по ядру terminal chat?",
            session_id="project_workspace",
        )
    )
    done = events[-1]
    answer = done["response_text"]
    lowered = answer.casefold()

    assert "CONTROL_PLANE" in answer
    assert "MAKSIMAR_SERVER" in answer
    assert "tools/jarvis_live_runtime" in answer
    assert "terminal chat" in lowered
    assert "read-only" in lowered
    assert "direct_execution_allowed=false" in answer
    assert "canonical_write_allowed=false" in answer
    assert "pc_control_allowed=false" in answer
    assert not answer.rstrip().endswith("### 1")
    assert "Скажи, что нужно" not in answer
    assert "Нужна помощь" not in answer
    assert done["canonical_memory_write_allowed"] is False
    assert done["pc_control_allowed"] is False


def test_natural_project_read_questions_use_dynamic_tools_without_ollama(monkeypatch) -> None:
    import tools.jarvis_live_runtime.jarvis_live_brain_loop as brain_loop

    monkeypatch.setattr(brain_loop, "_load_session_state", lambda: brain_loop._empty_session_state())
    monkeypatch.setattr(brain_loop, "_save_session_state", lambda state: None)
    monkeypatch.setattr(brain_loop, "_append_local_chat_memory_record", lambda state, response, context: None)

    def fail_stream(*args, **kwargs):
        raise AssertionError("dynamic project read answers must not call Ollama")

    monkeypatch.setattr(brain_loop, "_stream_ollama_model", fail_stream)

    changed = list(stream_jarvis_live_brain_response("джарвис что изменено?", session_id="project_tools"))[-1]["response_text"]
    atlas = list(stream_jarvis_live_brain_response("покажи полностью весь проект", session_id="project_tools"))[-1]["response_text"]
    safety = list(stream_jarvis_live_brain_response("что у нас по core guard watchdog safety?", session_id="project_tools"))[-1]["response_text"]
    models = list(stream_jarvis_live_brain_response("что сделано для моделей и Ollama runtime?", session_id="project_tools"))[-1]["response_text"]

    assert "Project git status read-only" in changed
    assert "branch=" in changed
    assert "/project files 1" in atlas
    assert "/project search <term>" in atlas
    assert "Safety/security surfaces read-only" in safety
    assert "direct_execution_allowed=false" in safety
    assert "Ollama is local model engine" in models
    assert "CONTROL_PLANE" in models
    assert "tool_calls are proposals" in models
    assert "pc_control_allowed=false" in models


def test_imported_project_history_is_read_only_not_written_to_local_chat(monkeypatch) -> None:
    import tools.jarvis_live_runtime.jarvis_live_brain_loop as brain_loop

    captured: list[tuple[str, tuple[str, ...]]] = []
    monkeypatch.setattr(brain_loop, "_load_session_state", lambda: brain_loop._empty_session_state())
    monkeypatch.setattr(brain_loop, "_save_session_state", lambda state: None)
    monkeypatch.setattr(
        brain_loop,
        "_append_local_chat_memory_record",
        lambda state, response, context: captured.append((response, context.retrieved_snippets)),
    )
    monkeypatch.setattr(brain_loop, "_retrieve_history_snippets", lambda text, deep: ["history_query_match: imported GPT project history"])

    def fake_stream(model_id, prompt, route_mode, timeout_seconds=None, response_mode_text=None):
        assert "imported GPT project history" in prompt
        yield {"event": "chunk", "text": "История прочитана как read-only.", "ollama_model_used": model_id, "pc_control_allowed": False}
        yield {"event": "done", "ollama_model_used": model_id, "pc_control_allowed": False}

    monkeypatch.setattr(brain_loop, "_stream_ollama_model", fake_stream)

    list(stream_jarvis_live_brain_response("Что в project history по проекту?", session_id="terminal_a"))

    assert captured
    response, snippets = captured[0]
    assert response == "История прочитана как read-only."
    assert "history_query_match: imported GPT project history" in snippets
    assert any("project_workspace_read_model" in snippet for snippet in snippets)


def test_memory_recall_guard_does_not_claim_memory_without_record(monkeypatch) -> None:
    import tools.jarvis_live_runtime.jarvis_live_brain_loop as brain_loop

    monkeypatch.setattr(brain_loop, "_load_session_state", lambda: brain_loop._empty_session_state())
    monkeypatch.setattr(brain_loop, "_save_session_state", lambda state: None)
    monkeypatch.setattr(brain_loop, "_read_recent_local_chat_records", lambda limit=8: ())
    monkeypatch.setattr(brain_loop, "_append_local_chat_memory_record", lambda state, response, context: None)

    events = list(stream_jarvis_live_brain_response("Джарвис, ты помнишь мой любимый цвет?", session_id="empty"))
    done = events[-1]

    assert "Не буду выдумывать память" in done["response_text"]
    assert "помню" not in done["response_text"].casefold()
    assert done["canonical_memory_write_allowed"] is False


def test_permanent_memory_write_request_is_rejected_without_canonical_write(monkeypatch) -> None:
    import tools.jarvis_live_runtime.jarvis_live_brain_loop as brain_loop

    monkeypatch.setattr(brain_loop, "SESSION_MEMORY_ROOT", brain_loop.PROJECT_ROOT)
    monkeypatch.setattr(brain_loop, "_load_session_state", lambda: brain_loop._empty_session_state())
    monkeypatch.setattr(brain_loop, "_save_session_state", lambda state: None)

    payload = run_jarvis_live_brain_once("Джарвис, запиши это в постоянную память.", session_id="test")

    assert "canonical_memory_write_allowed=false" in payload["llm_response"]
    assert payload["canonical_memory_write_allowed"] is False
    assert payload["pc_control_allowed"] is False


def test_stream_start_and_done_include_memory_federation_fields(monkeypatch) -> None:
    import tools.jarvis_live_runtime.jarvis_live_brain_loop as brain_loop

    monkeypatch.setattr(brain_loop, "SESSION_MEMORY_ROOT", brain_loop.PROJECT_ROOT)
    monkeypatch.setattr(brain_loop, "_load_session_state", lambda: brain_loop._empty_session_state())
    monkeypatch.setattr(brain_loop, "_save_session_state", lambda state: None)

    events = list(stream_jarvis_live_brain_response("Джарвис, видишь ли ты runtime_history_store?", session_id="test"))
    start = events[0]
    done = events[-1]

    assert start["memory_federation_available"] is True
    assert "retrieval_surfaces_used" in start
    assert "mempalace_status" in start
    assert done["memory_federation_available"] is True
    assert "retrieval_surfaces_used" in done
    assert "mempalace_status" in done
    assert done["canonical_memory_write_allowed"] is False
    assert done["pc_control_allowed"] is False
