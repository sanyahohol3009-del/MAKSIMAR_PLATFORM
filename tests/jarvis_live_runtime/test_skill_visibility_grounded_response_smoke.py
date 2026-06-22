from __future__ import annotations

from tools.jarvis_live_runtime.jarvis_live_brain_loop import stream_jarvis_live_brain_response


def _disable_ollama(monkeypatch) -> None:
    import tools.jarvis_live_runtime.jarvis_live_brain_loop as brain_loop

    def fail_stream(*args: object, **kwargs: object):
        raise AssertionError("skill visibility route must answer before Ollama free generation")
        yield {}

    monkeypatch.setattr(brain_loop, "_stream_ollama_model", fail_stream)
    monkeypatch.setattr(brain_loop, "SESSION_MEMORY_ROOT", brain_loop.PROJECT_ROOT)
    monkeypatch.setattr(brain_loop, "_load_session_state", lambda: brain_loop._empty_session_state())
    monkeypatch.setattr(brain_loop, "_save_session_state", lambda state: None)
    monkeypatch.setattr(brain_loop, "_append_local_chat_memory_record", lambda state, response, context: None)


def test_skill_visibility_grounded_response_smoke(monkeypatch) -> None:
    import tools.jarvis_live_runtime.jarvis_live_project_answer_engine as answer_engine

    _disable_ollama(monkeypatch)
    monkeypatch.setattr(
        answer_engine,
        "build_jarvis_skill_visibility_read_model",
        lambda: {
            "project_workspace_tools": ("repo_git_status", "build_project_workspace_read_model", "repo_tree"),
            "repo_introspection_tools": ("repo_search", "read_file_snippet", "read_file_outline", "repo_import_graph"),
            "memory_retrieval_tools": ("session_memory", "runtime_history_store", "mgrep_readonly"),
            "tests_roadmap_drift_tools": ("status_tools", "roadmap_post_step_drift_check", "jarvis_live_ci_status"),
            "model_runtime_tools": ("model_runtime_status", "build_jarvis_live_session_status"),
            "external_adapter_statuses": (
                {
                    "tool_id": "external_adapter:openai_agents_sdk",
                    "availability_status": "available",
                    "selection_enabled": True,
                    "import_probe_worked": True,
                },
                {
                    "tool_id": "external_adapter:mcp_python_sdk",
                    "availability_status": "available",
                    "selection_enabled": True,
                    "import_probe_worked": True,
                },
                {
                    "tool_id": "external_adapter:autogen_agentchat",
                    "availability_status": "available",
                    "selection_enabled": True,
                    "import_probe_worked": True,
                },
                {
                    "tool_id": "external_adapter:autogen_ext",
                    "availability_status": "available",
                    "selection_enabled": True,
                    "import_probe_worked": True,
                },
                {
                    "tool_id": "external_adapter:langgraph",
                    "availability_status": "available",
                    "selection_enabled": True,
                    "import_probe_worked": True,
                },
                {
                    "tool_id": "external_adapter:autogen",
                    "availability_status": "legacy_unavailable",
                    "selection_enabled": False,
                    "import_probe_worked": False,
                },
            ),
            "action_proposal_tools": ("operator_proposal", "pytest_run_proposal"),
            "runtime_library_packages": (
                {
                    "package_name": "autogen-agentchat",
                    "module_name": "autogen_agentchat",
                    "version": "0.7.5",
                    "import_ok": True,
                    "category": "agents",
                    "runtime_only": True,
                },
                {
                    "package_name": "llama-index",
                    "module_name": "llama_index",
                    "version": "0.14.22",
                    "import_ok": True,
                    "category": "skills_rag",
                    "runtime_only": True,
                },
                {
                    "package_name": "playwright",
                    "module_name": "playwright",
                    "version": "1.60.0",
                    "import_ok": True,
                    "category": "tools_browser",
                    "runtime_only": True,
                },
            ),
            "visible_agents": (
                "tool_selector_agent",
                "project_coder_agent",
                "architect_agent",
                "safety_guard_agent",
                "action_worker_agent",
            ),
            "external_adapter_tools": (
                "external_adapter:openai_agents_sdk",
                "external_adapter:mcp_python_sdk",
                "external_adapter:autogen_agentchat",
                "external_adapter:autogen_ext",
                "external_adapter:langgraph",
            ),
            "external_adapter_unavailable_tools": ("external_adapter:autogen",),
            "windows_gui_bridge_enabled": False,
            "pc_control_allowed": False,
            "visible_tools": ("repo_git_status", "repo_search"),
        },
    )

    events = list(stream_jarvis_live_brain_response("какие навыки доступны", session_id="skill_visibility_grounded"))
    done = events[-1]
    response = str(done["response_text"])

    assert done["intent_family"] == "SKILL_VISIBILITY"
    assert done["ollama_called"] is False
    assert "Project workspace tools:" in response
    assert "Repo read/search/outline/import graph:" in response
    assert "Memory/history/retrieval:" in response
    assert "Tests/roadmap/drift:" in response
    assert "Model/runtime status:" in response
    assert "External adapters:" in response
    assert "external_adapter:autogen status=legacy_unavailable selection_enabled=false import_probe_passed=false" in response
    assert "Action proposals:" in response
    assert "Runtime library store:" in response
    assert "autogen-agentchat module=autogen_agentchat version=0.7.5 import_ok=true runtime_only=true execution_enabled=false" in response
    assert "llama-index module=llama_index version=0.14.22 import_ok=true runtime_only=true execution_enabled=false" in response
    assert "playwright module=playwright version=1.60.0 import_ok=true runtime_only=true execution_enabled=false" in response
    assert "PC-control status:" in response
    assert "- windows_gui_bridge_enabled=false" in response
    assert "- pc_control_allowed=false" in response
