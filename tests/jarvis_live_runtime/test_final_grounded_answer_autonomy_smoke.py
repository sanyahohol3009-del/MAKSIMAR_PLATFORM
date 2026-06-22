from __future__ import annotations

import json

from tools.jarvis_live_runtime.jarvis_live_brain_loop import stream_jarvis_live_brain_response
from tools.jarvis_live_runtime.wsl_project_operator import build_project_wide_autonomy_audit_read_model


def _prepare_runtime(monkeypatch) -> None:
    import tools.jarvis_live_runtime.jarvis_live_brain_loop as brain_loop
    import tools.jarvis_live_runtime.memory_context_builder as builder

    monkeypatch.setattr(brain_loop, "SESSION_MEMORY_ROOT", brain_loop.PROJECT_ROOT)
    monkeypatch.setattr(brain_loop, "_load_session_state", lambda: brain_loop._empty_session_state())
    monkeypatch.setattr(brain_loop, "_save_session_state", lambda state: None)
    monkeypatch.setattr(brain_loop, "_append_local_chat_memory_record", lambda state, response, context: None)
    monkeypatch.setattr(builder, "_retrieve_memory_federation_snippets", lambda *args, **kwargs: ((), ("session_memory",)))
    monkeypatch.setattr(builder, "_retrieve_local_chat_memory_snippets", lambda *args, **kwargs: ())


def test_project_blocker_audit_routes_to_final_llm(monkeypatch) -> None:
    import tools.jarvis_live_runtime.jarvis_live_brain_loop as brain_loop
    import tools.jarvis_live_runtime.jarvis_live_project_answer_engine as answer_engine

    _prepare_runtime(monkeypatch)
    monkeypatch.setattr(
        answer_engine,
        "build_project_wide_autonomy_audit_read_model",
        lambda _text: {
            "inspected_files": (
                "tools/jarvis_live_runtime/read_only_tool_router.py",
                "tools/jarvis_live_runtime/jarvis_live_project_answer_engine.py",
                "tools/jarvis_live_runtime/jarvis_live_terminal_chat.py",
                "tools/jarvis_live_runtime/jarvis_live_brain_loop.py",
            ),
            "inspected_import_edges": (
                {"from": "tools/jarvis_live_runtime/jarvis_live_brain_loop.py", "to": "tools.jarvis_live_runtime.jarvis_live_project_answer_engine"},
            ),
            "detected_blockers": ("grounded observations were replacing the final answer layer",),
            "misplaced_logic": ("terminal renderer owned too much answer visibility logic",),
            "missing_connections": ("tool observations were not being passed into the final answer model",),
            "wrong_intent_routes": ("blocker questions were collapsing into PROJECT_SEARCH",),
            "answer_layer_issues": ("raw [work] blocks could reach the terminal as if they were the answer",),
            "permission_flag_issues": ("execution flags were shown as user-facing blockers for read-only work",),
            "final_answer_blockers": ("ollama_called=false branch was winning too early",),
            "recommended_patch_plan": (
                "route blocker audits into project-wide diagnostics",
                "always synthesize a final Russian answer through the local model",
            ),
            "read_project_allowed": True,
            "final_answer_generation_allowed": True,
            "write_allowed": False,
        },
    )

    def fake_stream(model_id: str, prompt: str, route_mode: str, timeout_seconds=None, response_mode_text=None):
        assert model_id
        assert route_mode
        assert response_mode_text
        assert "PROJECT_WIDE_DIAGNOSTICS" in prompt
        assert "grounded observations were replacing the final answer layer" in prompt
        assert "SELECTED_AGENT_ROLES: architect_agent, project_coder_agent" in prompt
        assert "tools/jarvis_live_runtime/jarvis_live_brain_loop.py" in prompt
        yield {"event": "chunk", "text": "Я проверил ключевые runtime-файлы. Основная проблема была в том, что технические observations подменяли финальный ответ модели. Читать, анализировать и готовить патч-предложение JARVIS может автоматически, а запись файлов и git-действия остаются только по одобрению."}
        yield {"event": "done", "ollama_model_used": model_id}

    monkeypatch.setattr(brain_loop, "_stream_ollama_model", fake_stream)

    events = list(
        stream_jarvis_live_brain_response(
            "джарвис проверь весь проект и скажи что мешает тебе пользоваться агентами скилами и инструментами",
            session_id="project_blocker_audit",
        )
    )
    done = events[-1]
    text = str(done["response_text"])

    assert done["intent_family"] == "PROJECT_WIDE_DIAGNOSTICS"
    assert done["ollama_called"] is True
    assert done["grounded_answer"] is True
    assert done["read_only"] is True
    assert done["execution_allowed"] is False
    assert "execution_allowed=false" not in text
    assert "proposal_only=true" not in text
    assert "[work]" not in text
    assert "Читать, анализировать" in text


def test_catalog_question_uses_final_llm_even_when_helper_invalid(monkeypatch) -> None:
    import tools.jarvis_live_runtime.jarvis_live_brain_loop as brain_loop
    import tools.jarvis_live_runtime.jarvis_live_project_answer_engine as answer_engine
    import tools.jarvis_live_runtime.memory_context_builder as builder

    _prepare_runtime(monkeypatch)
    monkeypatch.setattr(
        builder,
        "_call_helper_orchestration_probe",
        lambda *args, **kwargs: (_ for _ in ()).throw(RuntimeError("helper invalid")),
    )
    monkeypatch.setattr(
        answer_engine,
        "build_jarvis_live_tool_catalog_read_model",
        lambda: {
            "read_only": True,
            "execution_allowed": False,
            "read_tools": ("repo_git_status", "repo_search"),
            "proposal_tools": ("operator_proposal",),
            "project_repo_read_only_tools": ("repo_git_status", "repo_tree", "repo_files"),
            "memory_history_read_only_tools": ("session_memory",),
            "model_status_read_only_tools": ("model_runtime_status",),
            "roadmap_safety_read_only_tools": ("status_tools",),
            "memory_definition_count": 3,
            "external_adapter_runtime_status": (),
            "external_adapter_tools": ("external_adapter:mcp_python_sdk",),
            "external_adapter_unavailable_tools": ("external_adapter:autogen",),
            "external_adapter_legacy_tools": ("external_adapter:autogen",),
            "runtime_library_packages": (
                {"package_name": "langgraph", "module_name": "langgraph", "version": "1.0", "import_ok": True, "category": "agents", "runtime_only": True},
                {"package_name": "llama-index", "module_name": "llama_index", "version": "0.1", "import_ok": True, "category": "skills_rag", "runtime_only": True},
            ),
            "action_proposal_only_tools": ("operator_proposal",),
            "mgrep_status": {"usable_now": True, "source_present": True, "selected_tool": "mgrep_readonly"},
            "sqlite_vec_status": {"usable_now": False, "source_present": False, "selected_tool": "repo_search"},
            "qdrant_status": {"usable_now": False, "source_present": False, "selected_tool": "qdrant_readonly_status"},
            "qdrant_server_runtime_enabled": False,
            "active_retrieval_surfaces": ("session_memory",),
            "sandbox_only_memory_surfaces": (),
            "disabled_memory_surfaces": (),
            "enterprise_memory_preview_ready": False,
            "regulatory_routing_preview_ready": False,
            "mempalace_routing_ready": False,
            "all_existing_read_tools_connected": True,
        },
    )

    def fake_stream(model_id: str, prompt: str, route_mode: str, timeout_seconds=None, response_mode_text=None):
        assert "TOOL_CATALOG" in prompt
        assert "langgraph" in prompt
        assert "repo_git_status" in prompt
        yield {"event": "chunk", "text": "Я вижу read-only инструменты проекта, runtime libraries и внешние адаптеры. Могу автоматически читать проект, искать по коду, смотреть git status и подбирать runtime-библиотеки по смыслу запроса."}
        yield {"event": "done", "ollama_model_used": model_id}

    monkeypatch.setattr(brain_loop, "_stream_ollama_model", fake_stream)

    done = list(stream_jarvis_live_brain_response("какие инструменты ты видишь", session_id="catalog_final_llm"))[-1]

    assert done["intent_family"] == "TOOL_CATALOG"
    assert done["ollama_called"] is True
    assert "runtime libraries" in done["response_text"]
    assert "execution_allowed=false" not in str(done["response_text"])


def test_model_unavailable_grounded_path_uses_clear_fallback(monkeypatch) -> None:
    import tools.jarvis_live_runtime.jarvis_live_brain_loop as brain_loop
    import tools.jarvis_live_runtime.jarvis_live_project_answer_engine as answer_engine

    _prepare_runtime(monkeypatch)
    monkeypatch.setattr(
        answer_engine,
        "build_project_wide_autonomy_audit_read_model",
        lambda _text: {
            "inspected_files": ("tools/jarvis_live_runtime/jarvis_live_brain_loop.py",),
            "detected_blockers": ("final answer model is unavailable in this test",),
            "recommended_patch_plan": ("retry local Ollama after warmup",),
            "read_project_allowed": True,
            "final_answer_generation_allowed": True,
            "write_allowed": False,
        },
    )

    def unavailable_stream(model_id: str, prompt: str, route_mode: str, timeout_seconds=None, response_mode_text=None):
        yield {"event": "error", "error_message": "connection refused", "ollama_model_used": model_id}

    monkeypatch.setattr(brain_loop, "_stream_ollama_model", unavailable_stream)

    done = list(
        stream_jarvis_live_brain_response(
            "что мешает тебе работать",
            session_id="project_blocker_audit_fallback",
        )
    )[-1]

    assert done["intent_family"] == "PROJECT_WIDE_DIAGNOSTICS"
    assert done["ollama_called"] is False
    assert "Модель ответа недоступна, показываю технический fallback." in str(done["response_text"])
    assert "retry local Ollama after warmup" in str(done["response_text"])


def test_wsl_project_diagnostics_produces_final_human_answer(monkeypatch) -> None:
    import tools.jarvis_live_runtime.jarvis_live_brain_loop as brain_loop
    import tools.jarvis_live_runtime.jarvis_live_project_answer_engine as answer_engine

    _prepare_runtime(monkeypatch)
    monkeypatch.setattr(
        answer_engine,
        "build_wsl_project_diagnostics_read_model",
        lambda _text: {
            "git_probe": {"command": ("git", "status", "-sb"), "returncode": 0},
            "selected_scope": ("tests/jarvis_live_runtime/test_read_only_tool_router_boundary_smoke.py",),
            "selection_reason": "nearest tests mapped from changed python files",
            "pytest_probe": {"command": ("python", "-m", "pytest"), "returncode": 1, "timed_out": False},
            "failing_tests": ("tests/jarvis_live_runtime/test_read_only_tool_router_boundary_smoke.py::test_route",),
            "related_file_refs": ({"path": "tools/jarvis_live_runtime/read_only_tool_router.py", "line": 31},),
            "related_snippets": (
                {"path": "tools/jarvis_live_runtime/read_only_tool_router.py", "line_hint": 31, "functions": ("_build_read_only_tool_plan:19",), "snippet": ("31: intent_family = \"WSL_PROJECT_DIAGNOSTICS\"",)},
            ),
            "diagnosis": ("failing tests were detected in the bounded pytest scope",),
            "fix_plan": ("align router behavior with the bounded diagnostics route",),
            "git_status_stdout": "## main\n M tools/jarvis_live_runtime/read_only_tool_router.py",
            "pytest_stdout": "FAILED test_route",
            "pytest_stderr": "",
        },
    )

    def fake_stream(model_id: str, prompt: str, route_mode: str, timeout_seconds=None, response_mode_text=None):
        assert "WSL_PROJECT_DIAGNOSTICS" in prompt
        assert "test_read_only_tool_router_boundary_smoke.py::test_route" in prompt
        yield {"event": "chunk", "text": "Я запустил ограниченную pytest-диагностику и увидел падение в выбранном smoke scope. Проблема локализуется вокруг read_only_tool_router, а дальше нужен патч-предложение и повторный прогон того же ограниченного scope."}
        yield {"event": "done", "ollama_model_used": model_id}

    monkeypatch.setattr(brain_loop, "_stream_ollama_model", fake_stream)

    done = list(
        stream_jarvis_live_brain_response(
            "найди почему тесты падают и предложи план",
            session_id="wsl_project_final_answer",
        )
    )[-1]

    assert done["intent_family"] == "WSL_PROJECT_DIAGNOSTICS"
    assert done["ollama_called"] is True
    assert "[work]" not in str(done["response_text"])
    assert "pytest-диагностику" in str(done["response_text"])


def test_project_wide_audit_read_model_inspects_multiple_files_and_flags_permissions() -> None:
    payload = build_project_wide_autonomy_audit_read_model("что мешает тебе работать и почему ты не пользуешься агентами")

    assert payload["intent_family"] == "PROJECT_WIDE_DIAGNOSTICS"
    assert len(payload["inspected_files"]) >= 5
    assert len(payload["inspected_import_edges"]) >= 1
    assert "detected_blockers" in payload
    assert "permission_flag_issues" in payload
    assert "final_answer_blockers" in payload
    assert payload["read_project_allowed"] is True
    assert payload["final_answer_generation_allowed"] is True
    assert payload["write_allowed"] is False


def test_code_draft_request_returns_patch_proposal_text_without_writes(monkeypatch) -> None:
    import tools.jarvis_live_runtime.jarvis_live_brain_loop as brain_loop
    import tools.jarvis_live_runtime.jarvis_live_project_answer_engine as answer_engine

    _prepare_runtime(monkeypatch)
    monkeypatch.setattr(
        answer_engine,
        "build_project_wide_autonomy_audit_read_model",
        lambda _text: {
            "inspected_files": ("tools/jarvis_live_runtime/jarvis_live_brain_loop.py",),
            "recommended_patch_plan": ("move grounded observations into the final model-answer stage",),
            "read_project_allowed": True,
            "final_answer_generation_allowed": True,
            "write_allowed": False,
        },
    )

    def fake_stream(model_id: str, prompt: str, route_mode: str, timeout_seconds=None, response_mode_text=None):
        assert "CODE_DRAFT_PROPOSAL" in prompt
        yield {
            "event": "chunk",
            "text": "Предлагаю патч без применения:\n```diff\n- return grounded_tool_answer\n+ return final_grounded_answer\n```",
        }
        yield {"event": "done", "ollama_model_used": model_id}

    monkeypatch.setattr(brain_loop, "_stream_ollama_model", fake_stream)

    done = list(
        stream_jarvis_live_brain_response(
            "напиши код исправления, но не применяй",
            session_id="code_draft_only",
        )
    )[-1]

    assert done["intent_family"] == "CODE_DRAFT_PROPOSAL"
    assert done["ollama_called"] is True
    assert "```diff" in str(done["response_text"])
    assert done["execution_allowed"] is False


def test_terminal_normal_mode_hides_route_and_operator_infra(capsys) -> None:
    import tools.jarvis_live_runtime.jarvis_live_terminal_chat as terminal_chat

    terminal_chat._set_chat_mode("detailed")
    terminal_chat._print_stream_event(
        json.dumps(
            {
                "event": "route_selected",
                "intent_family": "PROJECT_WIDE_DIAGNOSTICS",
                "selected_tools": ["repo_import_graph"],
                "execution_allowed": False,
                "read_only": True,
            },
            ensure_ascii=False,
        )
    )
    terminal_chat._print_stream_event(
        json.dumps(
            {
                "event": "operator_trace",
                "intent_family": "PROJECT_WIDE_DIAGNOSTICS",
                "selected_tools": ["repo_import_graph"],
                "execution_allowed": False,
                "read_only": True,
            },
            ensure_ascii=False,
        )
    )
    output = capsys.readouterr().out

    assert "[infra]" not in output
    assert "execution_allowed=false" not in output
