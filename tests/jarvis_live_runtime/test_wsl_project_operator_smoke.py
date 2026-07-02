from __future__ import annotations

from tools.jarvis_live_runtime.jarvis_live_brain_loop import stream_jarvis_live_brain_response


def test_wsl_project_operator_routes_to_bounded_diagnostics_smoke(monkeypatch) -> None:
    import tools.jarvis_live_runtime.jarvis_live_brain_loop as brain_loop
    import tools.jarvis_live_runtime.jarvis_live_project_answer_engine as answer_engine

    prompts: list[str] = []

    def fake_stream(model_id: str, prompt: str, *args: object, **kwargs: object):
        prompts.append(str(prompt))

        assert "GROUNDING_INTENT_FAMILY: WSL_PROJECT_DIAGNOSTICS" in str(prompt)
        assert "build_wsl_project_diagnostics_read_model" in str(prompt)
        assert "tests/jarvis_live_runtime/test_read_only_tool_router_boundary_smoke.py" in str(prompt)
        assert "tools/jarvis_live_runtime/read_only_tool_router.py" in str(prompt)

        yield {
            "event": "chunk",
            "text": (
                "Я проверил WSL/project diagnostics в read-only режиме и отвечаю своими словами. "
                "Вижу failing pytest scope: tests/jarvis_live_runtime/test_read_only_tool_router_boundary_smoke.py. "
                "Проблемная зона: tools/jarvis_live_runtime/read_only_tool_router.py. "
                "План: сверить route вокруг WSL_PROJECT_DIAGNOSTICS, предложить patch, затем повторить bounded pytest. "
                "proposal_only=true, git_write_allowed=false, install_allowed=false, pc_control_allowed=false."
            ),
        }
        yield {"event": "done", "ollama_model_used": model_id}

    monkeypatch.setattr(brain_loop, "_stream_ollama_model", fake_stream)
    monkeypatch.setattr(brain_loop, "SESSION_MEMORY_ROOT", brain_loop.PROJECT_ROOT)
    monkeypatch.setattr(brain_loop, "_load_session_state", lambda: brain_loop._empty_session_state())
    monkeypatch.setattr(brain_loop, "_save_session_state", lambda state: None)
    monkeypatch.setattr(brain_loop, "_append_local_chat_memory_record", lambda state, response, context: None)

    monkeypatch.setattr(
        answer_engine,
        "build_wsl_project_diagnostics_read_model",
        lambda user_text: {
            "git_probe": {"command": ("git", "status", "-sb"), "returncode": 0},
            "pytest_probe": {
                "command": (
                    "python",
                    "-m",
                    "pytest",
                    "tests/jarvis_live_runtime/test_read_only_tool_router_boundary_smoke.py",
                    "-q",
                    "--tb=short",
                    "--maxfail=8",
                ),
                "returncode": 1,
                "timed_out": False,
            },
            "selected_scope": (
                "tests/jarvis_live_runtime/test_read_only_tool_router_boundary_smoke.py",
            ),
            "selection_reason": "nearest tests mapped from changed python files",
            "git_status_stdout": (
                "## voice-edge-v2-clean-reset\n"
                " M tools/jarvis_live_runtime/read_only_tool_router.py"
            ),
            "pytest_stdout": (
                "FAILED tests/jarvis_live_runtime/"
                "test_read_only_tool_router_boundary_smoke.py::test_route"
            ),
            "pytest_stderr": "",
            "failing_tests": (
                "tests/jarvis_live_runtime/test_read_only_tool_router_boundary_smoke.py::test_route",
            ),
            "related_file_refs": (
                {
                    "path": "tests/jarvis_live_runtime/test_read_only_tool_router_boundary_smoke.py",
                    "line": 24,
                },
                {
                    "path": "tools/jarvis_live_runtime/read_only_tool_router.py",
                    "line": 31,
                },
            ),
            "related_snippets": (
                {
                    "path": "tools/jarvis_live_runtime/read_only_tool_router.py",
                    "line_hint": 31,
                    "functions": (
                        "_build_read_only_tool_plan:14",
                        "_asks_wsl_project_diagnostic_question:278",
                    ),
                    "snippet": (
                        "28: if _asks_action_request(lowered):",
                        '31: intent_family = "WSL_PROJECT_DIAGNOSTICS"',
                    ),
                },
            ),
            "diagnosis": (
                "failing tests were detected in the bounded pytest scope",
                "first_error=AssertionError: expected WSL_PROJECT_DIAGNOSTICS route",
            ),
            "fix_plan": (
                "inspect and align behavior around tools/jarvis_live_runtime/read_only_tool_router.py near line 31",
                "rerun the same bounded pytest scope after the patch proposal",
            ),
        },
    )

    events = list(
        stream_jarvis_live_brain_response(
            "Джарвис, найди где ломаются тесты и предложи план фикса.",
            session_id="wsl_project_operator",
        )
    )
    done = events[-1]
    response = str(done["response_text"])

    assert done["intent_family"] == "WSL_PROJECT_DIAGNOSTICS"
    assert done["grounded_answer"] is True
    assert done["ollama_called"] is True
    assert done["read_only"] is True
    assert done["execution_allowed"] is False
    assert done["pc_control_allowed"] is False
    assert done["canonical_memory_write_allowed"] is False

    assert "отвечаю своими словами" in response
    assert "test_read_only_tool_router_boundary_smoke.py" in response
    assert "read_only_tool_router.py" in response
    assert "proposal_only=true" in response
    assert "git_write_allowed=false" in response
    assert "install_allowed=false" in response
    assert "pc_control_allowed=false" in response

    forbidden_user_visible_markers = (
        "[work] intent=",
        "WSL project diagnostics:",
        "git_status_command=",
        "pytest_scope=",
        "чем могу помочь",
        "готов помочь",
        "скажи, что нужно",
    )
    for marker in forbidden_user_visible_markers:
        assert marker not in response

    assert prompts
