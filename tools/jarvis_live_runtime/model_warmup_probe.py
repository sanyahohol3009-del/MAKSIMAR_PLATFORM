from __future__ import annotations

import argparse
import json
import os
from typing import Any

from tools.jarvis_live_runtime.ollama_transport import (
    DAILY_CODER_MODEL_ID,
    HEAVY_CODER_MODEL_ID,
    HELPER_CLASSIFIER_MODEL_ID,
    PRIMARY_CONVERSATION_MODEL_ID,
    build_model_timeout_policy_read_model,
    ollama_get_json,
    ollama_post_json,
)


def build_model_warmup_probe_read_model(
    *,
    include_heavy: bool = False,
    warmup_enabled: bool | None = None,
) -> dict[str, Any]:
    timeout_policy = build_model_timeout_policy_read_model()
    warmup_allowed = warmup_enabled if warmup_enabled is not None else os.environ.get("JARVIS_LIVE_WARMUP_ENABLED", "0") == "1"
    selected_models = [
        HELPER_CLASSIFIER_MODEL_ID,
        PRIMARY_CONVERSATION_MODEL_ID,
        DAILY_CODER_MODEL_ID,
    ]
    if include_heavy or os.environ.get("JARVIS_LIVE_WARMUP_INCLUDE_HEAVY", "0") == "1":
        selected_models.append(HEAVY_CODER_MODEL_ID)

    ps_payload = ollama_get_json("/api/ps", timeout_seconds=30.0)
    running_models = {
        str(model.get("name", "") or model.get("model", "")).strip()
        for model in ps_payload.get("models", ())
        if isinstance(model, dict)
    }

    results: list[dict[str, Any]] = []
    for model_id in selected_models:
        probe_timeout = float(
            timeout_policy["model_roles"]["heavy_coder_model"]["model_load_timeout_seconds"]
            if model_id == HEAVY_CODER_MODEL_ID
            else timeout_policy["model_roles"]["jarvis_chat_model"]["model_load_timeout_seconds"]
        )
        if model_id == HELPER_CLASSIFIER_MODEL_ID:
            probe_timeout = float(timeout_policy["model_roles"]["helper_classifier_model"]["model_load_timeout_seconds"])
        show_payload = ollama_post_json("/api/show", {"model": model_id}, timeout_seconds=probe_timeout)
        warm_payload = (
            ollama_post_json("/api/generate", {"model": model_id, "prompt": "", "keep_alive": "10m"}, timeout_seconds=probe_timeout)
            if warmup_allowed
            else {"ok": False, "message": "warmup_disabled"}
        )
        results.append(
            {
                "model_id": model_id,
                "running_now": model_id in running_models,
                "show_ok": bool(show_payload) and show_payload.get("ok", True) is not False,
                "warmup_attempted": warmup_allowed,
                "warmup_ok": bool(warm_payload) and warm_payload.get("ok", True) is not False if warmup_allowed else False,
                "probe_timeout_seconds": probe_timeout,
            }
        )

    return {
        "probe_id": "jarvis_model_warmup_probe_v1",
        "warmup_enabled": warmup_allowed,
        "include_heavy": include_heavy,
        "models": tuple(results),
        "timeout_policy": timeout_policy,
        "read_only": True,
        "execution_allowed": False,
    }


def main() -> int:
    parser = argparse.ArgumentParser(description="Read-only warm/check probe for local JARVIS Ollama models.")
    parser.add_argument("--include-heavy", action="store_true")
    parser.add_argument("--warm", action="store_true")
    args = parser.parse_args()
    payload = build_model_warmup_probe_read_model(
        include_heavy=args.include_heavy,
        warmup_enabled=args.warm,
    )
    print(json.dumps(payload, indent=2, ensure_ascii=False, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
