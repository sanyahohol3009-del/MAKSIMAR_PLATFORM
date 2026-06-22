from __future__ import annotations

from tools.jarvis_live_runtime.jarvis_live_brain_loop import stream_jarvis_live_brain_response


def test_helper_primary_route_survives_to_final_events(monkeypatch) -> None:
    import tools.jarvis_live_runtime.jarvis_live_brain_loop as brain_loop
    import tools.jarvis_live_runtime.jarvis_live_project_answer_engine as answer_engine
    import tools.jarvis_live_runtime.memory_context_builder as builder

    def fake_helper_probe(text, *, input_channel, owner_identity_claim, require_live_helper=False):
        assert "тест" in text.casefold()
        assert input_channel == "text"
        return {
            "helper_model_status": "ready",
            "helper_model_called": True,
            "helper_model_used": True,
            "helper_model_id": "jarvis:helper3b",
            "helper_decision_confidence": 0.97,
            "fallback_used": False,
            "selection_source": "helper_model",
            "normalized_intent": "code_debug",
            "task_complexity": "medium",
            "selected_model_role_id": "daily_coder_model",
            "selected_model_id": "jarvis:coder7b",
            "selected_agent_roles": ("project_coder_agent",),
            "selected_tools": (
                "repo_git_status",
                "pytest_report_read",
                "repo_search",
                "read_file_snippet",
                "read_file_outline",
            ),
            "selected_skills": ("project_workspace_analysis",),
            "workflow_steps": ("inspect_failure_context", "locate_relevant_code", "propose_fix"),
            "risk_class": "read_only",
            "selected_tool_reason": "helper picked bounded project diagnostics",
            "risk_gate_required": False,
            "safe_direct_action_allowed": False,
            "pc_tool_direct_allowed": False,
            "heavy_model_selected": False,
            "parallel_heavy_model_allowed": True,
            "selected_model_role": {
                "role_id": "daily_coder_model",
                "selected_model_role": "daily_coder_model",
                "model_id": "jarvis:coder7b",
                "status": "available",
                "load_policy": "keep_warm",
            },
        }

    def fake_diagnostics(*_args, **_kwargs):
        return {
            "git_probe": {"command": ("git", "status", "-sb"), "returncode": 0},
            "git_status_stdout": "## main\n M tools/jarvis_live_runtime/jarvis_live_brain_loop.py\n",
            "selected_scope": ("tests/jarvis_live_runtime/test_helper_primary_runtime_smoke.py",),
            "selection_reason": "nearest smoke scope",
            "pytest_probe": {
                "command": (
                    "python",
                    "-m",
                    "pytest",
                    "tests/jarvis_live_runtime/test_helper_primary_runtime_smoke.py",
                    "-q",
                ),
                "returncode": 1,
                "timed_out": False,
            },
            "pytest_stdout": "F",
            "pytest_stderr": "",
            "failing_tests": ("tests/jarvis_live_runtime/test_helper_primary_runtime_smoke.py::test_helper_primary_route_survives_to_final_events",),
            "related_file_refs": ({"path": "tools/jarvis_live_runtime/jarvis_live_brain_loop.py", "line": 549},),
            "related_snippets": (
                {
                    "path": "tools/jarvis_live_runtime/jarvis_live_brain_loop.py",
                    "line_hint": 549,
                    "functions": ("stream_jarvis_live_brain_response",),
                    "snippet": ("selected_agent_roles missing in done event",),
                },
            ),
            "diagnosis": ("helper path selected diagnostics, but final event propagation is under test",),
            "fix_plan": ("propagate helper-selected agents/skills to route and done events",),
            "read_only": True,
            "execution_allowed": False,
            "proposal_only": True,
        }

    monkeypatch.setenv("JARVIS_HELPER_CLASSIFIER_ENABLED", "true")
    monkeypatch.setattr(builder, "_call_helper_orchestration_probe", fake_helper_probe)
    monkeypatch.setattr(builder, "_retrieve_memory_federation_snippets", lambda *args, **kwargs: ((), ("session_memory",)))
    monkeypatch.setattr(builder, "_retrieve_local_chat_memory_snippets", lambda *args, **kwargs: ())
    monkeypatch.setattr(brain_loop, "SESSION_MEMORY_ROOT", brain_loop.PROJECT_ROOT)
    monkeypatch.setattr(brain_loop, "_load_session_state", lambda: brain_loop._empty_session_state())
    monkeypatch.setattr(brain_loop, "_save_session_state", lambda state: None)
    monkeypatch.setattr(answer_engine, "build_wsl_project_diagnostics_read_model", fake_diagnostics)

    events = list(
        stream_jarvis_live_brain_response(
            "Джарвис, найди почему тесты падают и предложи план исправления.",
            session_id="helper_primary_runtime",
        )
    )
    route = next(event for event in events if event.get("event") == "route_selected")
    done = events[-1]

    assert route["selection_source"] == "helper_model"
    assert route["fallback_used"] is False
    assert route["intent_family"] == "WSL_PROJECT_DIAGNOSTICS"
    assert route["selected_agent_roles"] == ("project_coder_agent",)
    assert "project_workspace_analysis" in route["selected_skills"]

    assert done["intent_family"] == "WSL_PROJECT_DIAGNOSTICS"
    assert done["selected_agent_roles"] == ("project_coder_agent",)
    assert "project_workspace_analysis" in done["selected_skills"]
    assert done["selection_source"] == "helper_model"
    assert done["fallback_used"] is False
    assert done["ollama_called"] is False


def test_marker_fallback_still_works_when_helper_is_unavailable(monkeypatch) -> None:
    import tools.jarvis_live_runtime.jarvis_live_brain_loop as brain_loop
    import tools.jarvis_live_runtime.memory_context_builder as builder

    monkeypatch.setenv("JARVIS_HELPER_CLASSIFIER_ENABLED", "true")
    monkeypatch.setattr(
        builder,
        "_call_helper_orchestration_probe",
        lambda *args, **kwargs: (_ for _ in ()).throw(RuntimeError("helper offline")),
    )
    monkeypatch.setattr(builder, "_retrieve_memory_federation_snippets", lambda *args, **kwargs: ((), ("session_memory",)))
    monkeypatch.setattr(builder, "_retrieve_local_chat_memory_snippets", lambda *args, **kwargs: ())
    monkeypatch.setattr(brain_loop, "SESSION_MEMORY_ROOT", brain_loop.PROJECT_ROOT)
    monkeypatch.setattr(brain_loop, "_load_session_state", lambda: brain_loop._empty_session_state())
    monkeypatch.setattr(brain_loop, "_save_session_state", lambda state: None)

    events = list(stream_jarvis_live_brain_response("какие инструменты ты видишь", session_id="helper_fallback_runtime"))
    route = next(event for event in events if event.get("event") == "route_selected")
    done = events[-1]

    assert route["selection_source"] == "deterministic_fallback"
    assert route["fallback_used"] is True
    assert route["intent_family"] == "TOOL_CATALOG"
    assert done["intent_family"] == "TOOL_CATALOG"
