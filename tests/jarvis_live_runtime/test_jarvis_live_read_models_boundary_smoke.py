from __future__ import annotations

import inspect

from tools.jarvis_live_runtime import jarvis_live_brain_loop
from MAKSIMAR_SERVER.AI_ORCHESTRATION import jarvis_live_read_models


def test_brain_loop_uses_extracted_read_model_facade() -> None:
    assert inspect.getmodule(jarvis_live_brain_loop.build_project_workspace_read_model).__name__ == (
        "MAKSIMAR_SERVER.AI_ORCHESTRATION.jarvis_live_read_models"
    )
    assert inspect.getmodule(jarvis_live_brain_loop.model_runtime_status).__name__ == (
        "MAKSIMAR_SERVER.AI_ORCHESTRATION.jarvis_live_read_models"
    )
    assert inspect.getmodule(jarvis_live_brain_loop.build_jarvis_live_tool_catalog_read_model).__name__ == (
        "MAKSIMAR_SERVER.AI_ORCHESTRATION.jarvis_live_read_models"
    )


def test_read_models_remain_read_only() -> None:
    payload = jarvis_live_read_models.build_jarvis_live_project_status_read_model()
    assert payload["read_only"] is True
    assert payload["read_project_allowed"] is True
    assert payload["runtime_probe_allowed"] is True
    assert payload["pc_control_allowed"] is False
    assert payload["canonical_memory_write_allowed"] is False


def test_memory_federation_read_model_blocks_mutation() -> None:
    payload = jarvis_live_read_models.build_jarvis_live_memory_federation_status()
    assert payload["memory_federation_available"] is True
    assert payload["read_memory_allowed"] is True
    assert payload["mempalace_query_allowed"] is True
    assert payload["sandbox_execution_allowed"] is True
    assert payload["canonical_memory_write_allowed"] is False
    assert payload["pc_control_allowed"] is False


def test_cli_memory_projection_uses_the_canonical_live_owner():
    from tools.jarvis_live_runtime import memory_context_builder as compatibility
    from tools.jarvis_live_runtime import jarvis_live_brain_loop as cli_brain
    from tools.jarvis_live_runtime import jarvis_skill_visibility as visibility
    from MAKSIMAR_SERVER.AI_ORCHESTRATION import jarvis_live_read_models as canonical
    from MAKSIMAR_SERVER.AI_ORCHESTRATION.session_memory_store import _session_turn_log_path
    assert compatibility.build_jarvis_live_memory_federation_status is canonical.build_jarvis_live_memory_federation_status
    assert cli_brain.build_jarvis_live_memory_federation_status is canonical.build_jarvis_live_memory_federation_status
    assert visibility.build_jarvis_live_memory_federation_status is canonical.build_jarvis_live_memory_federation_status
    assert compatibility.RUNTIME_HISTORY_STORE == _session_turn_log_path()
    result = compatibility.build_jarvis_live_memory_federation_status()
    assert result["inventory_coverage"] == "REGISTERED_NATIVE_SURFACES_ONLY"
    assert result["whole_organism_inventory_complete"] is False
    assert result["physical_store_count"] == len(result["physical_stores"])
    assert "canonical_session_health" in result


def test_tool_catalog_mempalace_readiness_uses_live_truth_without_historical_probe(monkeypatch):
    from types import SimpleNamespace
    module = jarvis_live_read_models
    for name in ("inspect_mgrep_readonly_availability", "inspect_sqlite_vec_readonly_availability", "inspect_qdrant_readonly_availability"):
        monkeypatch.setattr(module, name, lambda *a: SimpleNamespace(to_read_model=lambda: {}))
    monkeypatch.setattr(module, "list_memory_definitions", lambda: ())
    monkeypatch.setattr(module, "build_enterprise_memory_preview", lambda: {})
    monkeypatch.setattr(module, "build_regulatory_routing_preview", lambda: {})
    monkeypatch.setattr(module, "build_jarvis_external_adapter_visibility_read_model", lambda: {
        "active_adapter_ids": (), "registry": {"tools": ()}, "adapters": (),
        "unavailable_adapter_ids": (), "legacy_adapter_ids": (), "runtime_python": "test", "probe": {}})
    monkeypatch.setattr(module, "build_runtime_library_store_read_model", lambda: dict.fromkeys((
        "packages", "available_packages", "package_names", "available_package_names", "module_names", "agents",
        "skills_rag", "tools_browser", "categories", "probe_reports_read"), ()))
    def forbidden_historical_probe():
        raise AssertionError("Historical probe report cannot determine live provider readiness")
    monkeypatch.setattr(module, "build_mempalace_read_only_routing_integration_preview", forbidden_historical_probe, raising=False)
    for runtime_status, health_status, expected in (("LIVE_READ_ONLY", "LIVE_READ_ONLY", True),
            ("ENVIRONMENT_BLOCKED", "ENVIRONMENT_BLOCKED", False),
            ("LIVE_READ_ONLY", "NOT_CONFIGURED", False), ("NOT_CONFIGURED", "LIVE_READ_ONLY", False)):
        calls = []
        snapshot = {"surfaces": (
            {"surface_id": "mempalace_search", "runtime_status": runtime_status, "health": {"status": health_status}},
            {"surface_id": "mempalace_read_only_sandbox", "runtime_status": "SUPERSEDED_BY_CANONICAL_OWNER"}),
            "disabled_memory_surfaces": (), "active_retrieval_surfaces": (), "sandbox_only_memory_surfaces": (),
            "inventory_coverage": "REGISTERED_NATIVE_SURFACES_ONLY"}
        monkeypatch.setattr(module, "build_jarvis_live_memory_federation_status", lambda: calls.append(True) or snapshot)
        result = module.build_jarvis_live_tool_catalog_read_model()
        assert calls == [True]
        assert result["mempalace_routing_ready"] is expected
        assert result["mempalace_routing_readiness_scope"] == snapshot["inventory_coverage"]
        for key in ("read_tools", "memory_history_read_only_tools"):
            assert "mempalace_read_only_sandbox" not in result[key]
            assert "mempalace_search" in result[key]
        assert result["superseded_read_model_tools"] == ("mempalace_read_only_sandbox",)


def test_compat_health_and_session_use_current_canonical_journal_not_stale_cache(monkeypatch):
    import MAKSIMAR_SERVER.AI_ORCHESTRATION.jarvis_live_brain_loop_server_adapter as server
    module = jarvis_live_read_models
    health = {'owner': 'CanonicalSessionContextStore', 'path': '/canonical/live_turns.jsonl',
        'status': 'LIVE_READ_ONLY', 'canonical_turn_count': 7, 'last_append_at': '2026-10-13T12:00:00Z'}
    snapshot = {'canonical_session_health': health, 'surfaces': (),
                'inventory_coverage': 'REGISTERED_NATIVE_SURFACES_ONLY'}
    monkeypatch.setattr(module, 'build_jarvis_live_memory_federation_status', lambda: snapshot)
    def stale_cache():
        raise AssertionError('compatibility cache must not own canonical journal health')
    monkeypatch.setattr(jarvis_live_brain_loop, '_load_session_state', stale_cache)
    for builder in (jarvis_live_brain_loop.build_jarvis_live_brain_health,
                    jarvis_live_brain_loop.build_jarvis_live_session_status,
                    server.build_jarvis_live_brain_health, server.build_jarvis_live_session_status):
        result = builder()
        assert result['canonical_session_health'] == health
        assert result['status'] == 'LIVE_READ_ONLY'
        assert result['canonical_turn_count'] == 7
        assert result['session_memory_path'] == '/canonical/live_turns.jsonl'
        assert result['memory_federation'] == snapshot
        assert result['read_only'] is True and result['canonical_memory_write_allowed'] is False
        health['status'] = 'ENVIRONMENT_BLOCKED'
        assert builder()['status'] == 'ENVIRONMENT_BLOCKED'
        health['status'] = 'LIVE_READ_ONLY'



def test_federation_recent_count_uses_eligible_journal_not_compatibility_cache(monkeypatch, tmp_path):
    from MAKSIMAR_SERVER.AI_ORCHESTRATION import session_memory_store as store
    from MAKSIMAR_SERVER.AI_ORCHESTRATION import jarvis_live_read_models as models
    import json
    monkeypatch.setattr(store, "SESSION_MEMORY_ROOT", tmp_path)
    monkeypatch.setattr(models, "SESSION_STATE_PATH", tmp_path / "cache.json")
    monkeypatch.setattr(models, "_load_session_state", lambda: {"recent_turns":[{}] * 19})
    user = {"source":"jarvis_terminal_chat", "trace_id":"user", "persisted_at":"2026-10-15T10:00:00Z"}
    fixture = {**user, "trace_id":"fixture"}
    store._session_turn_log_path().write_text(json.dumps(user)+"\n"+json.dumps(fixture)+"\n")
    store.CanonicalSessionContextStore().exclude_persisted_records(
        record_sha256s=(store.session_record_sha256(fixture),), classification="TEST_FIXTURE",
        evidence_refs=("audit://retained/qualification",))
    before = store._session_turn_log_path().read_bytes()
    federation = models.build_jarvis_live_memory_federation_status()
    health = models.build_jarvis_live_brain_health()
    assert federation["recent_turn_count"] == health["recent_turn_count"] == 1
    assert federation["recent_turn_count_scope"] == "BOUNDED_ELIGIBLE_CANONICAL_JOURNAL_READBACK"
    assert federation["canonical_session_health"]["record_count"] == 3
    assert federation["canonical_session_health"]["canonical_turn_count"] == 1
    assert store._session_turn_log_path().read_bytes() == before


def test_federation_session_presence_uses_canonical_journal_in_both_cache_states(monkeypatch, tmp_path):
    from MAKSIMAR_SERVER.AI_ORCHESTRATION import session_memory_store as store
    from MAKSIMAR_SERVER.AI_ORCHESTRATION import jarvis_live_read_models as models
    import json
    monkeypatch.setattr(store, "SESSION_MEMORY_ROOT", tmp_path)
    cache = tmp_path / "cache.json"
    monkeypatch.setattr(models, "SESSION_STATE_PATH", cache)
    monkeypatch.setattr(models, "_load_session_state", lambda: {"recent_turns":[]})
    # Existing cache cannot manufacture presence of the canonical session store.
    cache.write_text("{}")
    assert models.build_jarvis_live_memory_federation_status()["session_memory_exists"] is False
    # Missing compatibility cache cannot hide an actual canonical journal.
    cache.unlink()
    store._session_turn_log_path().write_text(json.dumps({"source":"jarvis_terminal_chat", "trace_id":"user"})+"\n")
    assert models.build_jarvis_live_memory_federation_status()["session_memory_exists"] is True


def test_component_inventory_projection_is_shared_by_api_map_and_cli(monkeypatch):
    from dataclasses import asdict
    from CONTROL_PLANE import api_server
    from MAKSIMAR_SERVER.MEMORY_REGISTRY.global_registry_projection_builder import build_memory_component_inventory_projection
    from MAKSIMAR_SERVER.DASHBOARD_READ_ONLY_VIEWS.final_memory_map import build_final_memory_graph
    from tools.jarvis_live_runtime import jarvis_live_terminal_chat as terminal
    # Host/runtime probes do not participate in this projection-only contract.
    monkeypatch.setattr(api_server, "_legacy_runtime_readiness_payload", lambda: {})
    adapter = type("ReadOnlyAdapter", (), {"build_jarvis_live_session_status": staticmethod(lambda: {"recent_turn_count": 2})})()
    monkeypatch.setattr(api_server, "_legacy_readonly_adapter", lambda: adapter)
    status = api_server.jarvis_live_status()
    components = build_memory_component_inventory_projection()
    graph = build_final_memory_graph()
    assert status["logical_components"] == tuple(asdict(item) for item in graph.logical_components)
    assert status["logical_component_count"] == len(components)
    assert status["component_inventory_scope"] == graph.component_inventory_scope
    monkeypatch.setattr(terminal, "_get_json", lambda url: status)
    rendered = []
    monkeypatch.setattr(terminal, "_box", lambda title, lines, color: rendered.extend(lines))
    terminal._print_memory()
    assert "logical_component_count=" + str(len(components)) in rendered
    assert "component_inventory_scope=" + graph.component_inventory_scope in rendered
