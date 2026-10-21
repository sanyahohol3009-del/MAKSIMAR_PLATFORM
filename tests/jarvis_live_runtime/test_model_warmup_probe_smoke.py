from __future__ import annotations

import pytest

from tools.jarvis_live_runtime.model_warmup_probe import build_model_warmup_probe_read_model


def test_model_warmup_probe_smoke(monkeypatch) -> None:
    def fake_get(path, timeout_seconds=30.0):
        if path == "/api/ps":
            return {"models": [{"name": "jarvis:chat8b"}, {"name": "jarvis:helper3b"}]}
        return {
            "models": [
                {"name": "jarvis:chat8b"},
                {"name": "jarvis:helper3b"},
                {"name": "jarvis:coder14b"},
            ]
        }

    monkeypatch.setattr(
        "tools.jarvis_live_runtime.model_warmup_probe.ollama_get_json",
        fake_get,
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
    assert "jarvis:coder14b" in model_ids
    assert all(item["installed"] is True for item in payload["models"])
    assert all(item["show_ok"] is True for item in payload["models"])
    assert all(item["warmup_attempted"] is False for item in payload["models"])


def test_primary_warmup_uses_profile_context_and_verifies_residency(monkeypatch) -> None:
    calls = []

    def fake_get(path, timeout_seconds=30.0):
        if path == "/api/tags":
            return {"models": [{"name": "jarvis:chat8b"}]}
        return {"models": [{"name": "jarvis:chat8b", "context_length": 4096}]}

    def fake_post(path, payload, timeout_seconds=30.0):
        calls.append((path, payload))
        return {"ok": True, "model": "jarvis:chat8b", "done": True}

    monkeypatch.setattr("tools.jarvis_live_runtime.model_warmup_probe.ollama_get_json", fake_get)
    monkeypatch.setattr("tools.jarvis_live_runtime.model_warmup_probe.ollama_post_json", fake_post)

    payload = build_model_warmup_probe_read_model(primary_only=True, warmup_enabled=True)
    item = payload["models"][0]
    assert item["model_ready"] is True
    assert item["context_tokens"] == 4096
    assert calls[0][0] == "/api/show"
    assert calls[1][1]["options"] == {"num_ctx": 4096, "num_predict": 4}
    assert calls[1][1]["think"] is False
    assert calls[1][1]["stream"] is False


def test_warmup_does_not_pass_with_incompatible_resident_context(monkeypatch) -> None:
    monkeypatch.setattr(
        "tools.jarvis_live_runtime.model_warmup_probe.ollama_get_json",
        lambda path, timeout_seconds=30.0: {"models": [{"name": "jarvis:chat8b", "context_length": 3072}]},
    )
    monkeypatch.setattr(
        "tools.jarvis_live_runtime.model_warmup_probe.ollama_post_json",
        lambda path, payload, timeout_seconds=30.0: {"ok": True, "model": "jarvis:chat8b", "done": True},
    )
    payload = build_model_warmup_probe_read_model(primary_only=True, warmup_enabled=True)
    assert payload["models"][0]["model_ready"] is False

def test_model_probe_status_preserves_observed_readiness(monkeypatch) -> None:
    import tools.jarvis_live_runtime.model_warmup_probe as probe
    cases = (
        (False, [], {}, False, "not_resident"),
        (False, [{"name": "jarvis:chat8b", "context_length": 4096}], {}, True, "resident"),
        (False, [{"name": "jarvis:chat8b", "context_length": 3072}], {}, False, "context_mismatch"),
        (True, [], {"ok": True, "model": "jarvis:chat8b", "done": True}, False, "not_resident"),
        (True, [{"name": "jarvis:chat8b", "context_length": 4096}], {"ok": False}, False, "warmup_failed"),
        (True, [{"name": "jarvis:chat8b", "context_length": 4096}], {"ok": True, "model": "another:model", "done": True}, False, "warmup_failed"),
        (True, [{"name": "jarvis:chat8b", "context_length": 4096}], {"ok": True, "model": "jarvis:chat8b", "done": False}, False, "warmup_failed"),
        (True, [{"name": "jarvis:chat8b", "context_length": 4096}], {"ok": True, "model": "jarvis:chat8b", "done": True}, True, "resident"),
    )
    for warm, resident, result, expected_ready, expected_status in cases:
        monkeypatch.setattr(probe, "ollama_get_json",
            lambda path, timeout_seconds=30.0: {"models": [{"name": "jarvis:chat8b"}] if path == "/api/tags" else resident})
        monkeypatch.setattr(probe, "ollama_post_json",
            lambda path, payload, timeout_seconds=30.0: {"ok": True} if path == "/api/show" else result)
        item = probe.build_model_warmup_probe_read_model(primary_only=True, warmup_enabled=warm)["models"][0]
        assert item["model_ready"] is expected_ready, (warm, resident, result, item)
        assert item["status"] == expected_status, (warm, resident, result, item)
        assert item["running_now"] is bool(resident)
        assert item["context_tokens"] == (resident[0]["context_length"] if resident else None)


def test_model_probe_reports_post_warmup_residency(monkeypatch) -> None:
    import tools.jarvis_live_runtime.model_warmup_probe as probe
    ps_calls = 0
    def get(path, timeout_seconds=30.0):
        nonlocal ps_calls
        if path == "/api/tags":
            return {"models": [{"name": "jarvis:chat8b"}]}
        ps_calls += 1
        return {"models": [] if ps_calls == 1 else [{"name": "jarvis:chat8b", "context_length": 4096}]}
    monkeypatch.setattr(probe, "ollama_get_json", get)
    monkeypatch.setattr(probe, "ollama_post_json",
        lambda path, payload, timeout_seconds=30.0: {"ok": True, "model": "jarvis:chat8b", "done": True})
    item = probe.build_model_warmup_probe_read_model(primary_only=True, warmup_enabled=True)["models"][0]
    assert item["model_ready"] is True
    assert item["running_now"] is True
    assert item["status"] == "resident"


def test_primary_cold_load_budget_is_separate_from_warm_inference(monkeypatch):
    from tools.jarvis_live_runtime import model_warmup_probe as probe
    from MAKSIMAR_SERVER.AI_ORCHESTRATION import ollama_transport as transport
    observed = []
    monkeypatch.setattr(probe, "ollama_get_json", lambda path, **kwargs: {"models": [
        {"name": transport.PRIMARY_CONVERSATION_MODEL_ID, "context_length": 4096}]})
    def post(path, payload, timeout_seconds):
        observed.append((path, timeout_seconds, payload))
        return {"model": payload["model"], "done": True}
    monkeypatch.setattr(probe, "ollama_post_json", post)
    result = probe.build_model_warmup_probe_read_model(primary_only=True, warmup_enabled=True)
    policy = transport.MODEL_TIMEOUT_POLICY["jarvis_chat_model"]
    assert 300 <= policy["model_load_timeout_seconds"] <= 600
    assert policy["inference_timeout_seconds"] == policy["total_request_timeout_seconds"] == 180
    assert observed[1][1] == policy["model_load_timeout_seconds"]
    assert observed[1][2]["options"] == {"num_ctx": 4096, "num_predict": 4}
    assert result["models"][0]["model_ready"] is True


@pytest.mark.parametrize("name", ["JARVIS_LIVE_WARMUP_ENABLED", "JARVIS_LIVE_WARMUP_INCLUDE_HEAVY", "JARVIS_LIVE_WARMUP_INCLUDE_DAILY"])
@pytest.mark.parametrize("value", ["true", "false", "", "banana", "2"])
def test_malformed_flags_fail_before_any_provider_io(monkeypatch, name, value):
    import tools.jarvis_live_runtime.model_warmup_probe as probe
    monkeypatch.setenv(name, value)
    monkeypatch.setattr(probe, "ollama_get_json", lambda *a, **k: pytest.fail("provider GET before valid configuration"))
    monkeypatch.setattr(probe, "ollama_post_json", lambda *a, **k: pytest.fail("provider POST before valid configuration"))
    with pytest.raises(ValueError, match="must be 0 or 1"):
        probe.build_model_warmup_probe_read_model(primary_only=True, warmup_enabled=True)


@pytest.mark.parametrize("env,arguments", [
    ({"JARVIS_LIVE_WARMUP_INCLUDE_HEAVY": "1"}, {"primary_only": True}),
    ({"JARVIS_LIVE_WARMUP_INCLUDE_DAILY": "1"}, {"primary_only": True}),
    ({}, {"primary_only": True, "include_heavy": True}),
    ({"JARVIS_LIVE_WARMUP_INCLUDE_HEAVY": "1", "JARVIS_LIVE_WARMUP_INCLUDE_DAILY": "1"}, {}),
])
def test_conflicting_selection_fails_before_provider_io(monkeypatch, env, arguments):
    import tools.jarvis_live_runtime.model_warmup_probe as probe
    for name in ("JARVIS_LIVE_WARMUP_ENABLED", "JARVIS_LIVE_WARMUP_INCLUDE_HEAVY", "JARVIS_LIVE_WARMUP_INCLUDE_DAILY"):
        monkeypatch.delenv(name, raising=False)
    for key, value in env.items(): monkeypatch.setenv(key, value)
    monkeypatch.setattr(probe, "ollama_get_json", lambda *a, **k: pytest.fail("unexpected provider GET"))
    monkeypatch.setattr(probe, "ollama_post_json", lambda *a, **k: pytest.fail("unexpected provider POST"))
    with pytest.raises(ValueError, match="conflict"):
        probe.build_model_warmup_probe_read_model(warmup_enabled=True, **arguments)


@pytest.mark.parametrize("arguments", [{"primary_only": 1}, {"include_heavy": "false"}, {"warmup_enabled": "false"}])
def test_invalid_typed_flag_cannot_enable_model_load(monkeypatch, arguments):
    import tools.jarvis_live_runtime.model_warmup_probe as probe
    monkeypatch.setattr(probe, "ollama_get_json", lambda *a, **k: pytest.fail("unexpected provider GET"))
    with pytest.raises(ValueError, match="must be bool"):
        probe.build_model_warmup_probe_read_model(**arguments)


@pytest.mark.parametrize("flags,primary_only,expected", [
    ({}, True, ("jarvis:chat8b",)),
    ({}, False, ("jarvis:helper3b", "jarvis:chat8b")),
    ({"JARVIS_LIVE_WARMUP_INCLUDE_DAILY": "1"}, False, ("jarvis:helper3b", "jarvis:chat8b", "jarvis:coder7b")),
    ({"JARVIS_LIVE_WARMUP_INCLUDE_HEAVY": "1"}, False, ("jarvis:helper3b", "jarvis:chat8b", "jarvis:coder14b")),
])
def test_supported_selection_is_exact_and_metadata_only_without_warm_permission(monkeypatch, flags, primary_only, expected):
    import tools.jarvis_live_runtime.model_warmup_probe as probe
    for name in ("JARVIS_LIVE_WARMUP_ENABLED", "JARVIS_LIVE_WARMUP_INCLUDE_HEAVY", "JARVIS_LIVE_WARMUP_INCLUDE_DAILY"):
        monkeypatch.delenv(name, raising=False)
    for key, value in flags.items(): monkeypatch.setenv(key, value)
    monkeypatch.setattr(probe, "ollama_get_json", lambda *a, **k: {"models": []})
    monkeypatch.setattr(probe, "ollama_post_json", lambda *a, **k: pytest.fail("no installed models; no POST"))
    result = probe.build_model_warmup_probe_read_model(primary_only=primary_only, warmup_enabled=False)
    assert tuple(item["model_id"] for item in result["models"]) == expected
    assert not any(item["warmup_attempted"] for item in result["models"])
