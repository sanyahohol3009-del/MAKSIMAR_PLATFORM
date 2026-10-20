"""Strict existing-owner readiness contract; no real provider or runtime effects."""
import asyncio
import builtins
import importlib
import json
import socket
import subprocess

import pytest

from CORE_ROOT import run_context
from MAKSIMAR_SERVER.OBSERVABILITY.jarvis_live import jarvis_live_observability_read_model as obs
from MAKSIMAR_SERVER.SKILL_ADAPTER_REGISTRY import existing_capability_inventory as inventory


@pytest.fixture
def guarded(monkeypatch):
    monkeypatch.setenv(run_context.MODEL_FREE_STARTUP_ENV, "1")
    effects = []
    def forbidden(*args, **kwargs):
        effects.append("forbidden_provider_or_process_effect")
        raise AssertionError("unexpected provider, model, network or process effect")
    monkeypatch.setattr(socket.socket, "connect", forbidden)
    monkeypatch.setattr(socket, "create_connection", forbidden)
    monkeypatch.setattr(subprocess, "Popen", forbidden)
    monkeypatch.setattr(obs, "ollama_get_json", forbidden)
    monkeypatch.setattr(obs.ExistingWindowsEdgeAdapter, "health", forbidden)
    from MAKSIMAR_SERVER.AI_ORCHESTRATION import ollama_transport as transport
    monkeypatch.setattr(transport, "ollama_post_json", forbidden)
    monkeypatch.setattr(transport, "ollama_chat_once", forbidden)
    monkeypatch.setattr(transport, "grounded_final_brain_call", forbidden)
    real_import = builtins.__import__
    real_dynamic = importlib.import_module
    denied = {"torch", "transformers", "llama_cpp", "smolagents", "playwright"}
    def checked_import(name, *args, **kwargs):
        if name.split(".")[0] in denied:
            forbidden()
        return real_import(name, *args, **kwargs)
    def checked_dynamic(name, *args, **kwargs):
        if name.split(".")[0] in denied:
            forbidden()
        return real_dynamic(name, *args, **kwargs)
    monkeypatch.setattr(builtins, "__import__", checked_import)
    monkeypatch.setattr(importlib, "import_module", checked_dynamic)
    inventory._inventory_records.cache_clear()
    yield forbidden
    inventory._inventory_records.cache_clear()
    assert effects == []


def test_model_free_readiness_is_unobserved_not_failed(guarded):
    for _ in range(2):
        payload = obs.build_runtime_readiness_payload()
        assert payload["model_free_startup"] is True
        assert payload["control_plane_alive"] is True
        for key in ("ollama_alive", "stt_server_alive", "windows_edge_alive",
                    "chat_model_resident", "helper_model_resident"):
            assert payload[key] is None
        assert payload["chat_model_ready"] is False
        assert payload["pc_executor_available"] is False
        assert payload["pc_executor_status"] == "UNKNOWN"
        assert payload["chat_model_ready_context_tokens"] == 4096
        for state in payload["model_residency"].values():
            assert state["installed"] is None and state["resident"] is None
            assert state["model_load_failure"] is None
            assert state["processor"] is None
        wire = json.loads(json.dumps(payload))
        assert wire.pop("direct_pc_action_families") == list(payload["direct_pc_action_families"])
        assert wire == {k: v for k, v in payload.items() if k != "direct_pc_action_families"}


@pytest.mark.parametrize("supplied", [None, {}, {"model_free_startup": False,
    "ollama_alive": True, "model_residency": {"jarvis:chat8b": {"installed": True, "resident": True}}}])
def test_inventory_cannot_promote_installed_or_payload_override(guarded, supplied):
    projection = inventory.build_semantic_capability_registry_projection(readiness=supplied)
    assert projection["model_free_startup"] is True
    model_entries = [e for e in projection["entries"] if e["kind"] == "model_role"
                     or inventory.MODEL_ROLE_PROVIDER_ID in e.get("provider_ids", ())]
    assert model_entries
    for entry in model_entries:
        assert entry["provider_available"] is False
        assert entry["availability_status"] == "UNAVAILABLE"
        assert entry["executed"] is False and entry["execution_receipt_present"] is False
        assert entry["policy_metadata"]["turn_policy_execution_allowed"] is None
    ids = {e["capability_id"] for e in model_entries}
    assert set(inventory.MODEL_ROLE_OPERATION_CONTRACTS) <= ids
    roles = [e for e in model_entries if e["kind"] == "model_role"]
    assert roles and all(e["adapter_installed"] is True for e in roles)


def test_real_api_lifespan_and_readiness_serialization_without_provider_io(guarded):
    from CONTROL_PLANE import api_server as api
    from fastapi.testclient import TestClient
    canonical_owners = (api.PROJECT_READ_PERMISSION, api.FINAL_BRAIN_ADAPTER, api.CANONICAL_SESSION_CONTEXT)
    with TestClient(api.app) as client:
        assert client.get("/health").status_code == 200
        for _ in range(2):
            response = client.get("/jarvis-live/readiness")
            assert response.status_code == 200
            payload = response.json()["readiness"]
            assert payload["model_free_startup"] is True
            assert payload["ollama_alive"] is None
            assert payload["browser_provider_available"] is False
            projection = api._semantic_capability_projection()
            assert projection["capability_count"] > 0
            assert all(e["provider_available"] is False for e in projection["entries"]
                       if inventory.MODEL_ROLE_PROVIDER_ID in e.get("provider_ids", ()))
        for route in ("/jarvis-live/models", "/jarvis-live/project/models"):
            response = client.get(route)
            assert response.status_code == 503
            assert response.json()["detail"] == {"status": "UNAVAILABLE", "reason": "model_free_startup"}
        assert client.get("/operator-shell/read-model").status_code in (401, 403)
        assert api._payload_text({"text": "readiness", "model_free": False}) == "readiness"
    assert canonical_owners == (api.PROJECT_READ_PERMISSION, api.FINAL_BRAIN_ADAPTER, api.CANONICAL_SESSION_CONTEXT)
    assert run_context.model_free_startup() is True


@pytest.mark.parametrize("value", ["true", "false", "", "2", " 1", "1 ", "0\n"])
def test_invalid_flag_fails_before_io_or_inventory(guarded, monkeypatch, value):
    monkeypatch.setenv(run_context.MODEL_FREE_STARTUP_ENV, value)
    with pytest.raises(ValueError):
        obs.build_runtime_readiness_payload()
    with pytest.raises(ValueError):
        inventory.build_semantic_capability_registry_projection()
    from CONTROL_PLANE import api_server as api
    for endpoint in (api.jarvis_live_models, api.jarvis_live_project_models):
        with pytest.raises(ValueError):
            endpoint()


def normal_providers(monkeypatch, *, reachable=True, resident=False):
    calls = []
    def get(url, **kwargs):
        calls.append(url)
        if not reachable:
            return {"ok": False, "error": "fixture_provider_unreachable"}
        if url.endswith("/api/ps"):
            return {"models": [{"name": "jarvis:chat8b", "context_length": 4096,
                "size": 100, "size_vram": 100}] if resident else []}
        return {"ok": True, "models": [{"name": "jarvis:chat8b"}, {"name": "jarvis:helper3b"}]}
    monkeypatch.setattr(obs, "ollama_get_json", get)
    monkeypatch.setattr(obs.ExistingWindowsEdgeAdapter, "health",
        lambda self: calls.append("windows_health") or {"status": "AVAILABLE" if reachable else "UNAVAILABLE"})
    monkeypatch.setenv(run_context.MODEL_FREE_STARTUP_ENV, "0")
    return calls


@pytest.mark.parametrize("resident", [False, True])
def test_normal_mode_real_builder_keeps_metadata_and_residency(guarded, monkeypatch, resident):
    # Populate unrelated installed-adapter inventory in guarded mode first.
    # Normal-mode assertions below exercise the real model projection, not
    # external package discovery (covered by the existing probe tests).
    inventory._inventory_records()
    calls = normal_providers(monkeypatch, resident=resident)
    payload = obs.build_runtime_readiness_payload()
    assert calls == [f"{obs.OLLAMA_BASE_URL}/api/tags", obs.STT_SERVER_URL,
                     "windows_health", "/api/tags", "/api/ps"]
    assert payload["model_free_startup"] is False
    assert payload["ollama_alive"] is True and payload["stt_server_alive"] is True
    assert payload["pc_executor_available"] is True and payload["pc_executor_status"] == "available"
    assert payload["chat_model_ready"] is resident
    assert payload["model_residency"]["jarvis:chat8b"]["installed"] is True
    assert payload["chat_model_resident"] is resident
    projection = inventory.build_semantic_capability_registry_projection(readiness=payload)
    generated = [e for e in projection["entries"] if inventory.MODEL_ROLE_PROVIDER_ID in e.get("provider_ids", ())]
    assert generated and all(e["provider_available"] is True for e in generated)
    # Installed but cold remains load-on-demand in normal mode.
    assert all(e["execution_contract_available"] is True for e in generated)


def test_normal_provider_failure_is_not_ready(guarded, monkeypatch):
    calls = normal_providers(monkeypatch, reachable=False)
    payload = obs.build_runtime_readiness_payload()
    assert calls == [f"{obs.OLLAMA_BASE_URL}/api/tags", obs.STT_SERVER_URL, "windows_health"]
    assert payload["ollama_alive"] is False and payload["stt_server_alive"] is False
    assert payload["chat_model_ready"] is False
    assert payload["windows_edge_alive"] is False
    assert payload["pc_executor_available"] is False
    assert payload["pc_executor_status"] == "executor_unreachable"


def test_mode_is_not_cached_across_real_builder_and_projection(guarded, monkeypatch):
    calls = normal_providers(monkeypatch)
    assert obs.build_runtime_readiness_payload()["model_free_startup"] is False
    count = len(calls)
    monkeypatch.setenv(run_context.MODEL_FREE_STARTUP_ENV, "1")
    assert obs.build_runtime_readiness_payload()["ollama_alive"] is None
    projection = inventory.build_semantic_capability_registry_projection()
    assert projection["model_free_startup"] is True
    assert len(calls) == count


@pytest.mark.parametrize("endpoint", ["jarvis_live_models", "jarvis_live_project_models"])
def test_normal_model_diagnostic_routes_keep_existing_read_model(guarded, monkeypatch, endpoint):
    from types import SimpleNamespace
    from CONTROL_PLANE import api_server as api
    monkeypatch.setenv(run_context.MODEL_FREE_STARTUP_ENV, "0")
    calls = []
    original = {"ollama_version": "fixture_version", "ollama_tags": "fixture_tags"}
    monkeypatch.setattr(api, "_legacy_readonly_adapter", lambda: SimpleNamespace(
        model_runtime_status=lambda: calls.append("existing_owner") or original))
    payload = getattr(api, endpoint)()
    assert calls == ["existing_owner"]
    assert payload == {"ok": True, "surface": "CONTROL_PLANE/api_server.py", "models": original, "read_only": True}
