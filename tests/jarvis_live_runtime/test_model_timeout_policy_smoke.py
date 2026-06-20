from __future__ import annotations

from tools.jarvis_live_runtime.jarvis_live_brain_loop import _command_timeout_seconds
from tools.jarvis_live_runtime.ollama_transport import (
    OLLAMA_FAST_CHAT_KEEP_ALIVE,
    build_model_timeout_policy_read_model,
    timeout_policy_for_model_id,
    timeout_policy_for_model_role,
)


def test_model_timeout_policy_smoke() -> None:
    policy = build_model_timeout_policy_read_model()

    assert policy["model_roles"]["helper_classifier_model"]["total_request_timeout_seconds"] >= 90.0
    assert policy["model_roles"]["jarvis_chat_model"]["total_request_timeout_seconds"] >= 180.0
    assert policy["model_roles"]["daily_coder_model"]["total_request_timeout_seconds"] >= 180.0
    assert policy["model_roles"]["heavy_coder_model"]["total_request_timeout_seconds"] >= 300.0
    assert policy["external_import_probe_timeout_seconds"] >= 60.0
    assert OLLAMA_FAST_CHAT_KEEP_ALIVE.endswith("m")

    assert timeout_policy_for_model_role("heavy_coder_model")["model_load_timeout_seconds"] >= 300.0
    assert timeout_policy_for_model_id("jarvis:helper3b")["total_request_timeout_seconds"] >= 90.0
    assert _command_timeout_seconds(None) >= 180.0
    assert _command_timeout_seconds(None, "heavy_coder_model") >= 300.0
