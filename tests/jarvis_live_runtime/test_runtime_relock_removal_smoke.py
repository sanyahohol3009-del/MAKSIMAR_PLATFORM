from __future__ import annotations

import json

from tools.jarvis_live_runtime.jarvis_live_brain_loop import stream_jarvis_live_brain_response
from tools.jarvis_live_runtime.jarvis_live_read_models import (
    build_jarvis_live_project_status_read_model,
    build_jarvis_live_tool_catalog_read_model,
)
from tools.jarvis_live_runtime.jarvis_runtime_library_store import build_runtime_library_store_read_model
from tools.jarvis_live_runtime.memory_context_builder import build_jarvis_live_brain_context
from tools.jarvis_live_runtime.read_only_tool_router import _build_read_only_tool_plan


class _Probe:
    def __init__(self, payload):
        self._payload = payload

    def to_read_model(self):
        return self._payload


def _prepare_stream_runtime(monkeypatch) -> None:
    import tools.jarvis_live_runtime.jarvis_live_brain_loop as brain_loop
    import tools.jarvis_live_runtime.memory_context_builder as builder

    monkeypatch.setenv("JARVIS_HELPER_CLASSIFIER_ENABLED", "false")
    monkeypatch.setattr(brain_loop, "SESSION_MEMORY_ROOT", brain_loop.PROJECT_ROOT)
    monkeypatch.setattr(brain_loop, "_load_session_state", lambda: brain_loop._empty_session_state())
    monkeypatch.setattr(brain_loop, "_save_session_state", lambda state: None)
    monkeypatch.setattr(brain_loop, "_append_local_chat_memory_record", lambda state, response, context: None)
    monkeypatch.setattr(builder, "_retrieve_memory_federation_snippets", lambda *args, **kwargs: ((), ("session_memory",)))
    monkeypatch.setattr(builder, "_retrieve_local_chat_memory_snippets", lambda *args, **kwargs: ())


def _force_grounded_fallback(monkeypatch) -> None:
    import tools.jarvis_live_runtime.jarvis_live_brain_loop as brain_loop

    def unavailable_stream(model_id: str, prompt: str, route_mode: str, timeout_seconds=None, response_mode_text=None):
        yield {"event": "error", "error_message": "runtime unavailable", "ollama_model_used": model_id}

    monkeypatch.setattr(brain_loop, "_stream_ollama_model", unavailable_stream)


def test_restart_rebuild_does_not_relock_operator_capabilities(monkeypatch, tmp_path) -> None:
    import tools.jarvis_live_runtime.memory_context_builder as builder
    import tools.jarvis_live_runtime.jarvis_live_read_models as read_models

    monkeypatch.setenv("JARVIS_HELPER_CLASSIFIER_ENABLED", "false")
    monkeypatch.setattr(builder, "_retrieve_memory_federation_snippets", lambda *args, **kwargs: ((), ("session_memory",)))
    monkeypatch.setattr(builder, "_retrieve_local_chat_memory_snippets", lambda *args, **kwargs: ())

    store_root = tmp_path / "jarvis_library"
    manifests_dir = store_root / "manifests"
    reports_dir = store_root / "probe_reports"
    manifests_dir.mkdir(parents=True)
    reports_dir.mkdir(parents=True)
    report_path = reports_dir / "agent_tooling_import_probe.json"
    report_path.write_text(
        json.dumps(
            {
                "venv_name": "agent_tooling",
                "python": "/tmp/venvs/agent_tooling/bin/python",
                "packages": [
                    {
                        "pip_name": "autogen-agentchat",
                        "module_name": "autogen_agentchat",
                        "category": "agents",
                        "import_ok": True,
                        "version": "0.7.5",
                        "error": "",
                    }
                ],
            }
        ),
        encoding="utf-8",
    )
    (manifests_dir / "autogen-agentchat.json").write_text(
        json.dumps(
            {
                "manifest_id": "autogen-agentchat",
                "category": "agents",
                "runtime_only": True,
                "direct_execution_allowed": False,
                "approval_required_for_write_or_action": True,
                "report_file": str(report_path),
            }
        ),
        encoding="utf-8",
    )

    runtime_status = build_runtime_library_store_read_model(store_root)
    monkeypatch.setattr(
        read_models,
        "build_runtime_library_store_read_model",
        lambda: runtime_status,
    )
    monkeypatch.setattr(
        read_models,
        "build_jarvis_external_adapter_visibility_read_model",
        lambda: {
            "active_adapter_ids": ("external_adapter:autogen_agentchat",),
            "registry": {"tools": (), "safe_direct_tool_ids": (), "risk_gated_tool_ids": ()},
            "adapters": (),
            "unavailable_adapter_ids": (),
            "legacy_adapter_ids": (),
            "runtime_python": "/tmp/venv/bin/python",
            "probe": {"probe_results": ()},
        },
    )
    monkeypatch.setattr(read_models, "inspect_mgrep_readonly_availability", lambda *_args, **_kwargs: _Probe({"usable_now": True, "source_present": True, "selected_tool": "mgrep_readonly"}))
    monkeypatch.setattr(read_models, "inspect_sqlite_vec_readonly_availability", lambda *_args, **_kwargs: _Probe({"usable_now": False, "source_present": False, "selected_tool": "repo_search"}))
    monkeypatch.setattr(read_models, "inspect_qdrant_readonly_availability", lambda *_args, **_kwargs: _Probe({"usable_now": False, "source_present": False, "selected_tool": "qdrant_readonly_status"}))
    monkeypatch.setattr(read_models, "list_memory_definitions", lambda: ())
    monkeypatch.setattr(read_models, "build_enterprise_memory_preview", lambda: {"preview_ready": False})
    monkeypatch.setattr(read_models, "build_regulatory_routing_preview", lambda: {"preview_ready": False})
    monkeypatch.setattr(read_models, "build_mempalace_read_only_routing_integration_preview", lambda: {"routing_integration_ready": False})

    context = build_jarvis_live_brain_context(
        "проверь проект",
        {"recent_turns": [], "rolling_summary": "", "active_topics": []},
        session_id="relock_context",
    )
    read_model = context.to_read_model()
    plan = _build_read_only_tool_plan("проверь проект", context)
    tool_catalog = build_jarvis_live_tool_catalog_read_model()
    project_status = build_jarvis_live_project_status_read_model()

    assert read_model["read_project_allowed"] is True
    assert read_model["runtime_probe_allowed"] is True
    assert read_model["sandbox_execution_allowed"] is True
    assert read_model["canonical_write_allowed"] is False
    assert read_model["auto_apply_allowed"] is False
    assert read_model["auto_git_push_allowed"] is False
    assert read_model["auto_install_allowed"] is False
    assert read_model["auto_download_allowed"] is False

    assert plan["read_project_allowed"] is True
    assert plan["tool_selection_allowed"] is True
    assert plan["external_adapter_selection_allowed"] is True
    assert plan["runtime_probe_allowed"] is True
    assert plan["sandbox_execution_allowed"] is True
    assert plan["core_write_allowed"] is False
    assert plan["auto_apply_allowed"] is False

    assert runtime_status["runtime_library_visibility_allowed"] is True
    assert runtime_status["runtime_import_probe_allowed"] is True
    assert runtime_status["runtime_probe_allowed"] is True
    assert runtime_status["sandbox_execution_allowed"] is True
    assert runtime_status["canonical_write_allowed"] is False
    assert runtime_status["auto_git_push_allowed"] is False
    assert runtime_status["auto_install_allowed"] is False
    assert runtime_status["auto_download_allowed"] is False

    assert tool_catalog["read_project_allowed"] is True
    assert tool_catalog["runtime_library_execution_allowed"] is True
    assert tool_catalog["sandbox_execution_allowed"] is True
    assert tool_catalog["canonical_write_allowed"] is False
    assert tool_catalog["auto_apply_allowed"] is False
    assert tool_catalog["auto_git_push_allowed"] is False

    assert project_status["read_project_allowed"] is True
    assert project_status["runtime_probe_allowed"] is True
    assert project_status["canonical_write_allowed"] is False


def test_autogen_agentchat_request_returns_probe_and_sandbox_plan_not_fake_code(monkeypatch) -> None:
    _prepare_stream_runtime(monkeypatch)
    _force_grounded_fallback(monkeypatch)

    done = list(
        stream_jarvis_live_brain_response(
            "запусти агента autogen-agentchat и поприветствуй пользователя",
            session_id="autogen_agentchat_probe_plan",
        )
    )[-1]
    text = str(done["response_text"])

    assert done["intent_family"] == "EXTERNAL_ADAPTER_SELECTION"
    assert "external_adapter:autogen_agentchat" in done["selected_tools"]
    assert "operator_plan_kind=external_adapter_runtime_probe_and_sandbox_plan" in text
    assert "proposal_path=operator_proposal -> runtime_import_probe -> runtime_probe -> sandbox_probe" in text
    assert "operator_proposal=operator_proposal" in text
    assert "по одобрению" in text.lower()
    assert "direct_execution_allowed=false" not in text
    assert "```python" not in text
    assert "import autogen_agentchat" not in text
    assert done["core_write_allowed"] is False
    assert done["auto_apply_allowed"] is False
    assert done["auto_git_push_allowed"] is False


def test_project_visibility_request_uses_repo_access_and_does_not_ask_for_upload(monkeypatch) -> None:
    _prepare_stream_runtime(monkeypatch)
    _force_grounded_fallback(monkeypatch)

    done = list(stream_jarvis_live_brain_response("видишь ли ты проект?", session_id="project_visibility"))[-1]
    text = str(done["response_text"]).casefold()

    assert done["intent_family"] in {"PROJECT_STATUS", "PROJECT_STRUCTURE"}
    assert any(
        tool in done["selected_tools"]
        for tool in ("repo_git_status", "build_project_workspace_read_model", "repo_tree", "repo_files")
    )
    assert "upload files" not in text
    assert "загрузи" not in text
    assert "project_root=" in text or "вижу проект" in text


def test_what_is_available_distinguishes_allowed_operator_capabilities_from_blocked_mutation(monkeypatch) -> None:
    _prepare_stream_runtime(monkeypatch)
    _force_grounded_fallback(monkeypatch)

    done = list(stream_jarvis_live_brain_response("что тебе доступно?", session_id="what_available"))[-1]
    text = str(done["response_text"])

    assert done["intent_family"] == "TOOL_CATALOG"
    assert "operator_capabilities=read/analyze/select/propose/probe/sandbox" in text
    assert "approval_only_for=core_write,auto_apply,git_add,git_commit,git_push,install,download" in text
    assert "upload files" not in text.casefold()
