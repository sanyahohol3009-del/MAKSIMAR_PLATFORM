from __future__ import annotations

import pytest

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


def _disable_ollama_and_patch_probe(monkeypatch) -> None:
    import tools.jarvis_live_runtime.jarvis_live_brain_loop as brain_loop

    def fail_stream(*args: object, **kwargs: object):
        raise AssertionError("known external adapter requests must not call free Ollama")
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


@pytest.mark.parametrize(
    ("prompt", "expected_intent"),
    (
        ("нужен MCP tool", "EXTERNAL_ADAPTER_SELECTION"),
        ("подключи протокол инструментов для внешнего агента", "EXTERNAL_ADAPTER_SELECTION"),
        ("сравни LangGraph и AutoGen для задачи", "AGENT_ENGINE_COMPARISON"),
        ("построй агентный workflow", "EXTERNAL_AGENT_WORKFLOW_PLAN"),
        ("сделай последовательность агентов для этой задачи", "EXTERNAL_AGENT_WORKFLOW_PLAN"),
    ),
)
def test_external_adapter_requests_do_not_call_free_ollama_smoke(monkeypatch, prompt: str, expected_intent: str) -> None:
    _disable_ollama_and_patch_probe(monkeypatch)

    events = list(stream_jarvis_live_brain_response(prompt, session_id="external_adapter_no_free_ollama"))
    done = events[-1]

    assert done["intent_family"] == expected_intent
    assert done["ollama_called"] is False
    assert done["grounded_answer"] is True
    assert done["execution_allowed"] is False
    assert done["read_only"] is True
