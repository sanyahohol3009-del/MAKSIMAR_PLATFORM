from __future__ import annotations

from tools.jarvis_live_runtime.jarvis_live_brain_loop import stream_jarvis_live_brain_response


def _fake_probe_payload() -> dict[str, object]:
    return {
        "runtime_python": "/tmp/agent_tooling_python",
        "probe_results": (
            {"package_name": "openai-agents-python", "import_name": "agents", "installed": True, "import_probe_passed": True, "runtime_python": "/tmp/agent_tooling_python", "version_if_available": "1.0.0", "errors": ()},
            {"package_name": "mcp", "import_name": "mcp", "installed": True, "import_probe_passed": True, "runtime_python": "/tmp/agent_tooling_python", "version_if_available": "1.0.0", "errors": ()},
            {"package_name": "autogen-agentchat", "import_name": "autogen_agentchat", "installed": True, "import_probe_passed": True, "runtime_python": "/tmp/agent_tooling_python", "version_if_available": "1.0.0", "errors": ()},
            {"package_name": "autogen-ext", "import_name": "autogen_ext", "installed": True, "import_probe_passed": True, "runtime_python": "/tmp/agent_tooling_python", "version_if_available": "1.0.0", "errors": ()},
            {"package_name": "langgraph", "import_name": "langgraph", "installed": True, "import_probe_passed": True, "runtime_python": "/tmp/agent_tooling_python", "version_if_available": "1.0.0", "errors": ()},
            {"package_name": "pyautogen", "import_name": "autogen", "installed": False, "import_probe_passed": False, "runtime_python": "/tmp/agent_tooling_python", "version_if_available": "", "errors": ("ModuleNotFoundError:autogen",)},
        ),
        "installed": ("openai-agents-python", "mcp", "autogen-agentchat", "autogen-ext", "langgraph"),
        "import_probe_passed": ("openai-agents-python", "mcp", "autogen-agentchat", "autogen-ext", "langgraph"),
        "errors": (("ModuleNotFoundError:autogen",),),
    }


def _patch_probe(monkeypatch) -> None:
    import tools.jarvis_live_runtime.jarvis_live_brain_loop as brain_loop
    monkeypatch.setattr(brain_loop, "SESSION_MEMORY_ROOT", brain_loop.PROJECT_ROOT)
    monkeypatch.setattr(brain_loop, "_load_session_state", lambda: brain_loop._empty_session_state())
    monkeypatch.setattr(brain_loop, "_save_session_state", lambda state: None)
    monkeypatch.setattr(brain_loop, "_append_local_chat_memory_record", lambda state, response, context: None)
    monkeypatch.setattr(
        "MAKSIMAR_CORE_LIB.action_library_adapters.external_tool_library_adapter._load_agent_tooling_runtime_probe_read_model",
        _fake_probe_payload,
    )
    monkeypatch.setattr(
        "MAKSIMAR_CORE_LIB.action_library_adapters.agent_tooling_runtime_adapter.build_agent_tooling_runtime_probe_read_model",
        _fake_probe_payload,
    )


def test_long_grounded_response_not_silently_truncated_smoke(monkeypatch) -> None:
    _patch_probe(monkeypatch)

    import tools.jarvis_live_runtime.jarvis_live_brain_loop as brain_loop

    prompts: list[str] = []

    def fake_stream(model_id: str, prompt: str, route_mode: str, timeout_seconds=None, response_mode_text=None):
        prompts.append(str(prompt))
        assert "TOOL_CATALOG" in prompt
        assert "external_adapter:openai_agents_sdk" in prompt
        assert "external_adapter:mcp_python_sdk" in prompt
        assert "external_adapter:autogen_agentchat" in prompt
        assert "external_adapter:autogen_ext" in prompt
        assert "external_adapter:langgraph" in prompt
        yield {
            "event": "chunk",
            "text": (
                "Вижу полный read-only каталог инструментов и отвечаю своими словами: "
                "доступны external_adapter:openai_agents_sdk, external_adapter:mcp_python_sdk, "
                "external_adapter:autogen_agentchat, external_adapter:autogen_ext и external_adapter:langgraph. "
                "Также вижу legacy/unavailable alias external_adapter:autogen, но не буду выдавать его за рабочий инструмент."
            ),
        }
        yield {"event": "done", "ollama_model_used": model_id}

    monkeypatch.setattr(brain_loop, "_stream_ollama_model", fake_stream)

    events = list(stream_jarvis_live_brain_response("какие инструменты ты видишь", session_id="grounded_catalog_long"))
    done = events[-1]
    response = str(done["response_text"])

    assert done["intent_family"] == "TOOL_CATALOG"
    assert done["grounded_answer"] is True
    assert done["ollama_called"] is True
    assert done["output_truncated"] is False
    assert "[output_truncated=true" not in response
    assert "external_adapter:openai_agents_sdk" in response
    assert "external_adapter:mcp_python_sdk" in response
    assert "external_adapter:autogen_agentchat" in response
    assert "external_adapter:autogen_ext" in response
    assert "external_adapter:langgraph" in response
    assert "external_adapter:autogen" in response

    forbidden_user_visible_markers = (
        "[work] intent=",
        "Project git status read-only",
        "Safety/security surfaces read-only",
        "Ollama/model runtime read-only",
        "Project-wide autonomy audit is proposal-only",
        "чем могу помочь",
        "готов помочь",
        "скажи, что нужно",
    )
    for marker in forbidden_user_visible_markers:
        assert marker not in response

    assert prompts
