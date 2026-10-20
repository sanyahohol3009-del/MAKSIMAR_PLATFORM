from __future__ import annotations

from MAKSIMAR_SERVER.OBSERVABILITY.jarvis_live.jarvis_live_observability_read_model import (
    build_runtime_readiness_payload,
)


def test_runtime_readiness_exposes_required_flags(monkeypatch) -> None:
    monkeypatch.setenv("MAKSIMAR_MODEL_FREE_STARTUP", "0")
    monkeypatch.setattr(
        "MAKSIMAR_SERVER.OBSERVABILITY.jarvis_live.jarvis_live_observability_read_model.ExistingWindowsEdgeAdapter.health",
        lambda self: {"status": "AVAILABLE"},
    )
    monkeypatch.setattr(
        "MAKSIMAR_SERVER.OBSERVABILITY.jarvis_live.jarvis_live_observability_read_model._http_alive",
        lambda url: True,
    )
    monkeypatch.setattr(
        "MAKSIMAR_SERVER.OBSERVABILITY.jarvis_live.jarvis_live_observability_read_model._ollama_model_state",
        lambda: (
            {"jarvis:chat8b", "jarvis:helper3b"},
            {
                "jarvis:chat8b": {"size": 100, "size_vram": 100, "context_length": 4096,
                                   "expires_at": "2030-01-01T00:30:00Z"},
                "jarvis:helper3b": {"size": 50, "size_vram": 50, "context_length": 2048,
                                    "expires_at": "2030-01-01T00:30:00Z"},
            },
        ),
    )

    payload = build_runtime_readiness_payload(control_plane_alive=True)

    assert payload["control_plane_alive"] is True
    assert payload["stt_server_alive"] is True
    assert payload["ollama_alive"] is True
    assert payload["chat_model_resident"] is True
    assert payload["helper_model_resident"] is True
    assert payload["model_residency"]["jarvis:chat8b"]["installed"] is True
    assert payload["model_residency"]["jarvis:chat8b"]["processor"] == "GPU"
    helper = payload["model_residency"]["jarvis:helper3b"]
    assert helper["configured_idle_timeout_seconds"] == 1800
    assert helper["unload_due_at"] == "2030-01-01T00:30:00Z"
    assert helper["model_last_used_at"] is None
    assert helper["model_idle_seconds"] is None
    assert helper["requested"] is None
    assert payload["pc_executor_available"] is True
    assert payload["pc_executor_status"] == "available"
    assert "protected_mutation_gate_available" not in payload
