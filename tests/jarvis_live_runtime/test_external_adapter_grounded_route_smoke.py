from __future__ import annotations

from tools.jarvis_live_runtime.jarvis_live_brain_loop import stream_jarvis_live_brain_response


def _fake_probe_payload() -> dict[str, object]:
    return {
        "runtime_python": "/tmp/agent_tooling_python",
        "probe_results": (
            {
                "package_name": "openai-agents-python",
                "import_name": "agents",
                "installed": True,
                "import_probe_passed": True,
                "runtime_python": "/tmp/agent_tooling_python",
                "version_if_available": "1.0.0",
                "errors": (),
            },
            {
                "package_name": "mcp",
                "import_name": "mcp",
                "installed": True,
                "import_probe_passed": True,
                "runtime_python": "/tmp/agent_tooling_python",
                "version_if_available": "1.0.0",
                "errors": (),
            },
            {
                "package_name": "autogen-agentchat",
                "import_name": "autogen_agentchat",
                "installed": True,
                "import_probe_passed": True,
                "runtime_python": "/tmp/agent_tooling_python",
                "version_if_available": "1.0.0",
                "errors": (),
            },
            {
                "package_name": "autogen-ext",
                "import_name": "autogen_ext",
                "installed": True,
                "import_probe_passed": True,
                "runtime_python": "/tmp/agent_tooling_python",
                "version_if_available": "1.0.0",
                "errors": (),
            },
            {
                "package_name": "langgraph",
                "import_name": "langgraph",
                "installed": True,
                "import_probe_passed": True,
                "runtime_python": "/tmp/agent_tooling_python",
                "version_if_available": "1.0.0",
                "errors": (),
            },
            {
                "package_name": "pyautogen",
                "import_name": "autogen",
                "installed": False,
                "import_probe_passed": False,
                "runtime_python": "/tmp/agent_tooling_python",
                "version_if_available": "",
                "errors": ("ModuleNotFoundError:autogen",),
            },
        ),
        "installed": (
            "openai-agents-python",
            "mcp",
            "autogen-agentchat",
            "autogen-ext",
            "langgraph",
        ),
        "import_probe_passed": (
            "openai-agents-python",
            "mcp",
            "autogen-agentchat",
            "autogen-ext",
            "langgraph",
        ),
        "errors": (("ModuleNotFoundError:autogen",),),
    }


def _disable_ollama_and_patch_probe(monkeypatch) -> None:
    import tools.jarvis_live_runtime.jarvis_live_brain_loop as brain_loop

    def fail_stream(*args: object, **kwargs: object):
        raise AssertionError("external adapter grounded route must answer before free Ollama generation")
        yield {}

    monkeypatch.setattr(brain_loop, "_stream_ollama_model", fail_stream)
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


def test_external_adapter_grounded_route_smoke(monkeypatch) -> None:
    _disable_ollama_and_patch_probe(monkeypatch)

    events = list(stream_jarvis_live_brain_response("нужен MCP tool", session_id="external_adapter_grounded"))
    done = events[-1]
    response = str(done["response_text"])

    assert done["intent_family"] == "EXTERNAL_ADAPTER_SELECTION"
    assert done["ollama_called"] is False
    assert done["grounded_answer"] is True
    assert done["selected_tools"] == ("external_adapter:mcp_python_sdk",)
    assert "selected_agent_roles=tool_selector_agent" in response
    assert "external_adapter:mcp_python_sdk" in response
    assert "selection_enabled=true" in response
    assert "import_probe_passed=true" in response
    assert "risk_class=risk_gate" in response
    assert "proposal_only=true" in response
    assert "execution_allowed=false" in response
    assert "Makefile" not in response


def test_external_adapter_grounded_comparison_route_smoke(monkeypatch) -> None:
    _disable_ollama_and_patch_probe(monkeypatch)

    events = list(
        stream_jarvis_live_brain_response(
            "сравни LangGraph и AutoGen для задачи",
            session_id="external_adapter_comparison",
        )
    )
    done = events[-1]
    response = str(done["response_text"])

    assert done["intent_family"] == "AGENT_ENGINE_COMPARISON"
    assert done["ollama_called"] is False
    assert "external_adapter:langgraph" in done["selected_tools"]
    assert "external_adapter:autogen_agentchat" in done["selected_tools"]
    assert "external_adapter:autogen_ext" in done["selected_tools"]
    assert "external_adapter:autogen" not in done["selected_tools"]
    assert "Legacy alias status: external_adapter:autogen availability_status=legacy_unavailable" in response
