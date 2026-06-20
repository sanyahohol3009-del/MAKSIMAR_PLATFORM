from __future__ import annotations

from tools.jarvis_live_runtime.model_warmup_probe import build_model_warmup_probe_read_model


def test_model_warmup_probe_smoke(monkeypatch) -> None:
    monkeypatch.setattr(
        "tools.jarvis_live_runtime.model_warmup_probe.ollama_get_json",
        lambda path, timeout_seconds=30.0: {"models": [{"name": "jarvis:chat8b"}]},
    )
    monkeypatch.setattr(
        "tools.jarvis_live_runtime.model_warmup_probe.ollama_post_json",
        lambda path, payload, timeout_seconds=30.0: {"ok": True, "model": payload.get("model", "")},
    )

    payload = build_model_warmup_probe_read_model(include_heavy=True, warmup_enabled=False)

    model_ids = tuple(item["model_id"] for item in payload["models"])
    assert payload["probe_id"] == "jarvis_model_warmup_probe_v1"
    assert payload["warmup_enabled"] is False
    assert "jarvis:helper3b" in model_ids
    assert "jarvis:chat8b" in model_ids
    assert "jarvis:coder7b" in model_ids
    assert "jarvis:coder14b" in model_ids
    assert all(item["show_ok"] is True for item in payload["models"])
    assert all(item["warmup_attempted"] is False for item in payload["models"])
