from __future__ import annotations

import argparse
import json
import os
from typing import Any

from MAKSIMAR_SERVER.AI_ORCHESTRATION.ollama_transport import (
    DAILY_CODER_MODEL_ID,
    HEAVY_CODER_MODEL_ID,
    HELPER_INPUT_CORRECTION_MODEL_ID,
    OLLAMA_LIVE_MODEL_KEEP_ALIVE,
    PRIMARY_CONVERSATION_MODEL_ID,
    build_model_timeout_policy_read_model,
    ollama_get_json,
    ollama_post_json,
)
from MAKSIMAR_CORE_LIB.ai_orchestration.model_profile_registry_contract import (
    resident_context_tokens_for_jarvis_model,
    resolve_runtime_model_profile,
)


def build_model_warmup_probe_read_model(
    *,
    include_heavy: bool = False,
    warmup_enabled: bool | None = None,
    primary_only: bool = False,
) -> dict[str, Any]:
    for name, value in (("include_heavy", include_heavy), ("primary_only", primary_only)):
        if type(value) is not bool:
            raise ValueError(name + " must be bool")
    if warmup_enabled is not None and type(warmup_enabled) is not bool:
        raise ValueError("warmup_enabled must be bool or None")
    flags = {}
    for name in ("JARVIS_LIVE_WARMUP_ENABLED", "JARVIS_LIVE_WARMUP_INCLUDE_HEAVY", "JARVIS_LIVE_WARMUP_INCLUDE_DAILY"):
        value = os.environ.get(name, "0")
        if value not in ("0", "1"):
            raise ValueError(name + " must be 0 or 1")
        flags[name] = value == "1"
    heavy_requested = include_heavy or flags["JARVIS_LIVE_WARMUP_INCLUDE_HEAVY"]
    daily_requested = flags["JARVIS_LIVE_WARMUP_INCLUDE_DAILY"]
    if primary_only and (heavy_requested or daily_requested):
        raise ValueError("primary_only conflicts with heavy/daily warmup selection")
    if heavy_requested and daily_requested:
        raise ValueError("heavy and daily warmup selection conflict")
    timeout_policy = build_model_timeout_policy_read_model()
    # Explicit caller/CLI warmup permission takes precedence over the environment.
    warmup_allowed = warmup_enabled if warmup_enabled is not None else flags["JARVIS_LIVE_WARMUP_ENABLED"]
    selected_roles = ["jarvis_chat_model"] if primary_only else [
        "helper_input_correction_model", "jarvis_chat_model",
    ]
    if heavy_requested:
        selected_roles.append("heavy_coder_model")
    elif daily_requested:
        selected_roles.append("daily_coder_model")
    selected_profiles = tuple(resolve_runtime_model_profile(role_id=role) for role in selected_roles)

    from CORE_ROOT.run_context import model_free_startup
    if model_free_startup():
        return {
            "probe_id": "jarvis_model_warmup_probe_v1", "warmup_enabled": False,
            "include_heavy": include_heavy, "primary_only": primary_only,
            "models": tuple({"model_id": p.model_id, "model_role": p.role_id,
                "installed": None, "running_now": None, "show_ok": None,
                "warmup_attempted": False, "warmup_ok": False, "model_ready": False,
                "context_tokens": None, "status": "disabled_model_free",
                "resource_admission": None,
                "probe_timeout_seconds": float(timeout_policy["model_roles"][p.role_id]["model_load_timeout_seconds"])}
                for p in selected_profiles),
            "timeout_policy": timeout_policy, "read_only": True, "execution_allowed": False,
        }

    ps_payload = ollama_get_json("/api/ps", timeout_seconds=30.0)
    tags_payload = ollama_get_json("/api/tags", timeout_seconds=30.0)
    installed_models = {
        str(model.get("name", "") or model.get("model", "")).strip()
        for model in tags_payload.get("models", ())
        if isinstance(model, dict)
    }

    results: list[dict[str, Any]] = []
    for profile in selected_profiles:
        model_id = profile.model_id
        probe_timeout = float(timeout_policy["model_roles"][profile.role_id]["model_load_timeout_seconds"])
        installed = model_id in installed_models
        show_payload = (
            ollama_post_json("/api/show", {"model": model_id}, timeout_seconds=probe_timeout)
            if installed
            else {"ok": False, "message": "missing_model"}
        )
        warm_payload = (
            ollama_post_json(
                "/api/generate",
                {
                    "model": model_id,
                    "prompt": "ready",
                    "stream": False,
                    "think": False,
                    "keep_alive": OLLAMA_LIVE_MODEL_KEEP_ALIVE,
                    "options": {
                        "num_ctx": resident_context_tokens_for_jarvis_model(model_id),
                        "num_predict": 4,
                    },
                },
                timeout_seconds=probe_timeout,
            )
            if warmup_allowed and installed
            else {"ok": False, "message": "warmup_disabled"}
        )
        post_ps_payload = ollama_get_json("/api/ps", timeout_seconds=30.0) if warmup_allowed and installed else ps_payload
        post_running = {
            str(model.get("name", "") or model.get("model", "")).strip(): model
            for model in post_ps_payload.get("models", ()) if isinstance(model, dict)
        }
        resident_entry = post_running.get(model_id)
        expected_context = resident_context_tokens_for_jarvis_model(model_id)
        context_ok = bool(resident_entry) and int(resident_entry.get("context_length", 0) or 0) >= expected_context
        warm_ok = bool(warm_payload) and warm_payload.get("ok", True) is not False and (
            warm_payload.get("done") is True and warm_payload.get("model") == model_id
        )
        # Installation, residency, compatible context and completed warmup are
        # distinct observations. Never publish readiness from installation alone.
        ready = bool(installed and resident_entry and context_ok and (not warmup_allowed or warm_ok))
        status = (
            "missing_model" if not installed else
            "admission_denied" if warmup_allowed and installed and warm_payload.get("model_call_attempted") is False else
            "warmup_failed" if warmup_allowed and not warm_ok else
            "not_resident" if resident_entry is None else
            "context_mismatch" if not context_ok else "resident"
        )
        results.append(
            {
                "model_id": model_id,
                "model_role": profile.role_id,
                "installed": installed,
                "running_now": resident_entry is not None,
                "show_ok": bool(show_payload) and show_payload.get("ok", True) is not False,
                "warmup_attempted": warmup_allowed and installed and warm_payload.get("model_call_attempted", True) is not False,
                "resource_admission": warm_payload.get("resource_admission"),
                "warmup_ok": warm_ok if warmup_allowed else False,
                "model_ready": ready,
                "context_tokens": resident_entry.get("context_length") if resident_entry else None,
                "status": status,
                "probe_timeout_seconds": probe_timeout,
            }
        )

    return {
        "probe_id": "jarvis_model_warmup_probe_v1",
        "warmup_enabled": warmup_allowed,
        "include_heavy": include_heavy,
        "primary_only": primary_only,
        "models": tuple(results),
        "timeout_policy": timeout_policy,
        "read_only": True,
        "execution_allowed": False,
    }


def main() -> int:
    parser = argparse.ArgumentParser(description="Read-only warm/check probe for local JARVIS Ollama models.")
    parser.add_argument("--include-heavy", action="store_true")
    parser.add_argument("--warm", action="store_true")
    parser.add_argument("--primary-only", action="store_true")
    args = parser.parse_args()
    payload = build_model_warmup_probe_read_model(
        include_heavy=args.include_heavy,
        warmup_enabled=args.warm,
        primary_only=args.primary_only,
    )
    print(json.dumps(payload, indent=2, ensure_ascii=False, sort_keys=True))
    primary = next((item for item in payload["models"] if item["model_role"] == "jarvis_chat_model"), None)
    return 0 if not args.warm or bool(primary and primary.get("model_ready")) else 1


if __name__ == "__main__":
    raise SystemExit(main())
