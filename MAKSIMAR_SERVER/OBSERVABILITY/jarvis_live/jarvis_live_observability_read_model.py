from __future__ import annotations

import os
from MAKSIMAR_SERVER.AI_ORCHESTRATION.jarvis_live_read_models import build_provider_observation_context
import threading
import time
import json
from contextvars import ContextVar
from pathlib import Path
from collections import deque
from typing import Any

from MAKSIMAR_CORE_LIB.oob_dashboard.jarvis_live_status_panel_contract import (
    build_jarvis_live_status_panel_contract,
)
from MAKSIMAR_CORE_LIB.oob_dashboard.jarvis_model_status_panel_contract import (
    build_jarvis_model_status_panel_contract,
)
from MAKSIMAR_CORE_LIB.oob_dashboard.jarvis_queue_status_panel_contract import (
    build_jarvis_queue_status_panel_contract,
)
from MAKSIMAR_CORE_LIB.oob_dashboard.jarvis_resource_status_panel_contract import (
    build_jarvis_resource_status_panel_contract,
)
from MAKSIMAR_SERVER.OBSERVABILITY.memory_skill_metrics.jarvis_live_full_roadmap_status_builder import (
    build_jarvis_live_full_roadmap_status,
)
from MAKSIMAR_SERVER.AI_ORCHESTRATION.ollama_transport import (
    HELPER_INPUT_CORRECTION_MODEL_ID,
    OLLAMA_BASE_URL,
    OLLAMA_LIVE_MODEL_IDLE_TIMEOUT_SECONDS,
    PRIMARY_CONVERSATION_MODEL_ID,
    ollama_get_json,
)
from MAKSIMAR_CORE_LIB.ai_orchestration.model_profile_registry_contract import (
    resident_context_tokens_for_jarvis_model,
)
from MAKSIMAR_SERVER.WORKFLOW_AUTOMATION_RUNTIME.jarvis_pc_action_adapter_contract import (
    DIRECT_PC_ACTION_FAMILIES, ExistingWindowsEdgeAdapter, WINDOWS_EDGE_HEALTH_URL,
)


STT_SERVER_URL = os.environ.get("JARVIS_LIVE_STT_URL", "http://127.0.0.1:8777/transcribe")

_IN_FLIGHT_TRACES: deque[dict[str, Any]] = deque(maxlen=64)
_TRACE_LOCK = threading.Lock()
_TRACE_WRITE_FAILURES = 0
_CURRENT_TRACE_ID: ContextVar[str] = ContextVar("jarvis_trace_id", default="")
_TRACE_MODEL_ORDINALS: dict[str, int] = {}
_TRACE_TRANSPORT_ORDINALS: dict[str, int] = {}


def set_in_flight_trace(trace_id: str) -> None:
    _CURRENT_TRACE_ID.set(str(trace_id))


def trace_stage(stage: str, status: str = "STARTED", **metadata: Any) -> None:
    trace_id = _CURRENT_TRACE_ID.get()
    if trace_id:
        record_in_flight_trace_event(trace_id, stage, status, **metadata)
_IN_FLIGHT_TRACE_FILE = Path(os.environ.get("JARVIS_IN_FLIGHT_TRACE_FILE", ".runtime/jarvis_live/inflight_trace.jsonl"))


def record_in_flight_trace_event(trace_id: str, stage: str, status: str = "STARTED", **metadata: Any) -> dict[str, Any]:
    """Bounded observability-only stage projection; never stores prompts or secrets."""
    event = {"trace_id": str(trace_id), "stage": str(stage), "status": str(status), "timestamp": time.time(), **{
        key: value for key, value in metadata.items() if key in {
            "elapsed_ms", "caller", "error_class", "deadline_remaining", "ordinal",
            "purpose", "model_role", "model_id", "prompt_chars", "estimated_input_tokens",
            "num_predict", "latency_ms", "stream", "think", "num_ctx", "payload_chars",
            "timeout_seconds", "http_status", "response_bytes",
            "prompt_eval_count", "prompt_eval_duration", "eval_count", "eval_duration",
            "load_duration", "total_duration", "done_reason",
            "transport_ordinal", "keep_alive",
            "candidate_stage", "failure_type", "failure_code", "repair_attempt",
            "safe_structure",
            "binding_attempt", "binding_goal", "binding_projection_id",
            "binding_direct_capability_ids", "binding_operation_ids",
            "binding_semantic_owner_ids", "binding_status", "binding_capability_id",
            "binding_reason_present", "binding_reason_class",
            "source_text_sha256", "system_prompt_sha256", "user_prompt_sha256",
            "goalframe_projection_sha256", "combined_model_input_sha256",
            "model_payload_sha256",
            "source_text_length", "system_prompt_length", "user_prompt_length",
            "projection_entry_count", "temperature", "seed_present",
        }
    }}
    with _TRACE_LOCK:
        _IN_FLIGHT_TRACES.append(event)
        try:
            _IN_FLIGHT_TRACE_FILE.parent.mkdir(parents=True, exist_ok=True)
            if _IN_FLIGHT_TRACE_FILE.exists() and _IN_FLIGHT_TRACE_FILE.stat().st_size > 1_000_000:
                lines = _IN_FLIGHT_TRACE_FILE.read_text(encoding="utf-8").splitlines()[-256:]
                _IN_FLIGHT_TRACE_FILE.write_text("\n".join(lines) + "\n", encoding="utf-8")
            with _IN_FLIGHT_TRACE_FILE.open("a", encoding="utf-8") as handle:
                handle.write(json.dumps(event, ensure_ascii=False, separators=(",", ":")) + "\n")
        except OSError:
            global _TRACE_WRITE_FAILURES
            _TRACE_WRITE_FAILURES += 1
    return event


def trace_model_call_started(*, purpose: str, caller: str, model_role: str,
                             model_id: str, prompt_chars: int, num_predict: int,
                             deadline_remaining: float | None = None) -> tuple[str, int, float]:
    """Record bounded metadata for one canonical model transport call."""
    trace_id = _CURRENT_TRACE_ID.get()
    started = time.monotonic()
    if not trace_id:
        return "", 0, started
    with _TRACE_LOCK:
        ordinal = _TRACE_MODEL_ORDINALS.get(trace_id, 0) + 1
        _TRACE_MODEL_ORDINALS[trace_id] = ordinal
    record_in_flight_trace_event(
        trace_id, "MODEL_CALL", "STARTED", ordinal=ordinal, purpose=purpose,
        caller=caller, model_role=model_role, model_id=model_id,
        prompt_chars=prompt_chars, num_predict=num_predict,
        deadline_remaining=deadline_remaining,
    )
    return trace_id, ordinal, started


def trace_model_call_completed(*, trace_id: str, ordinal: int, started: float,
                               status: str, deadline_remaining: float | None = None,
                               error_class: str | None = None) -> None:
    if not trace_id:
        return
    record_in_flight_trace_event(
        trace_id, "MODEL_CALL", status,
        ordinal=ordinal, elapsed_ms=round((time.monotonic() - started) * 1000, 3),
        latency_ms=round((time.monotonic() - started) * 1000, 3),
        deadline_remaining=deadline_remaining,
        **({"error_class": error_class} if error_class else {}),
    )


def next_transport_ordinal(trace_id: str) -> int:
    if not trace_id:
        return 0
    with _TRACE_LOCK:
        ordinal = _TRACE_TRANSPORT_ORDINALS.get(trace_id, 0) + 1
        _TRACE_TRANSPORT_ORDINALS[trace_id] = ordinal
    return ordinal


def in_flight_trace_read_model(trace_id: str | None = None) -> dict[str, Any]:
    with _TRACE_LOCK:
        events = tuple(_IN_FLIGHT_TRACES)
    if trace_id:
        events = tuple(item for item in events if item.get("trace_id") == trace_id)
    return {"read_only": True, "retention": "BOUNDED", "events": events,
            "persistence_write_failures": _TRACE_WRITE_FAILURES}


def build_jarvis_live_observability_read_model() -> dict[str, Any]:
    roadmap_status = build_jarvis_live_full_roadmap_status()
    live_panel = build_jarvis_live_status_panel_contract(roadmap_status).to_read_model()
    model_panel = build_jarvis_model_status_panel_contract().to_read_model()
    resource_panel = build_jarvis_resource_status_panel_contract().to_read_model()
    queue_panel = build_jarvis_queue_status_panel_contract().to_read_model()

    return {
        "summary_id": "jarvis_live_observability_read_model_v0_1",
        "read_only": True,
        "dashboard_safe": True,
        "dashboard_execution_allowed": False,
        "runtime_start_allowed": bool(roadmap_status["runtime_start_allowed_now"]),
        "model_download_allowed": bool(roadmap_status["model_download_allowed_now"]),
        "live_status_panel": live_panel,
        "model_status_panel": model_panel,
        "resource_status_panel": resource_panel,
        "queue_status_panel": queue_panel,
        "ready_batches": roadmap_status["ready_batches"],
        "next_batch": roadmap_status["next_batch"],
        "gates": {
            "model_download_allowed": bool(roadmap_status["model_download_allowed_now"]),
            "runtime_start_allowed": bool(roadmap_status["runtime_start_allowed_now"]),
            "voice_allowed": bool(roadmap_status["voice_allowed_now"]),
            "pc_control_allowed": bool(roadmap_status["pc_control_allowed_now"]),
        },
    }


def build_runtime_readiness_payload(control_plane_alive: bool = True) -> dict[str, Any]:
    """Publish only directly observed runtime facts from the existing observability owner."""
    model_free = build_provider_observation_context()["model_free_startup"]  # Validate before any provider observation.
    if model_free:
        # None means unobserved, not a failed probe or an absent installation.
        ollama_alive = stt_alive = windows_edge_alive = None
        installed_models, running_models = set(), {}
    else:
        ollama_alive = _http_alive(f"{OLLAMA_BASE_URL}/api/tags")
        stt_alive = _http_alive(STT_SERVER_URL)
        windows_edge_health = ExistingWindowsEdgeAdapter().health()
        windows_edge_alive = windows_edge_health.get("status") == "AVAILABLE"
        installed_models, running_models = _ollama_model_state() if ollama_alive else (set(), {})
    model_ids = (PRIMARY_CONVERSATION_MODEL_ID, HELPER_INPUT_CORRECTION_MODEL_ID)
    model_residency = {
        model_id: _model_residency_truth(model_id, installed_models, running_models.get(model_id))
        for model_id in model_ids
    }
    if model_free:
        for state in model_residency.values():
            state.update(installed=None, resident=None)
    primary_model = model_residency[PRIMARY_CONVERSATION_MODEL_ID]
    expected_context = resident_context_tokens_for_jarvis_model(PRIMARY_CONVERSATION_MODEL_ID)
    model_ready = bool(
        primary_model["resident"]
        and int(primary_model.get("context_length") or 0) >= expected_context
    )
    return {
        "control_plane_alive": bool(control_plane_alive),
        "model_free_startup": model_free,
        "stt_server_alive": stt_alive,
        "ollama_alive": ollama_alive,
        "chat_model_resident": model_residency[PRIMARY_CONVERSATION_MODEL_ID]["resident"],
        "chat_model_ready": model_ready,
        "chat_model_ready_context_tokens": expected_context,
        "helper_model_resident": model_residency[HELPER_INPUT_CORRECTION_MODEL_ID]["resident"],
        "model_residency": model_residency,
        "windows_edge_alive": windows_edge_alive,
        "pc_executor_available": False if model_free else windows_edge_alive,
        "pc_executor_status": "UNKNOWN" if model_free else "available" if windows_edge_alive else "executor_unreachable",
        "direct_pc_action_families": DIRECT_PC_ACTION_FAMILIES,
        "stt_server_url": STT_SERVER_URL,
        "ollama_base_url": OLLAMA_BASE_URL,
        "windows_edge_health_url": WINDOWS_EDGE_HEALTH_URL,
    }


def _ollama_model_state() -> tuple[set[str], dict[str, dict[str, Any]]]:
    installed_payload = ollama_get_json("/api/tags", timeout_seconds=5.0)
    running_payload = ollama_get_json("/api/ps", timeout_seconds=5.0)
    installed = {
        str(entry.get("name", "") or entry.get("model", "")).strip()
        for entry in installed_payload.get("models", ()) if isinstance(entry, dict)
    }
    running: dict[str, dict[str, Any]] = {}
    for entry in running_payload.get("models", ()):
        if isinstance(entry, dict):
            name = str(entry.get("name", "") or entry.get("model", "")).strip()
            if name:
                running[name] = dict(entry)
    return installed, running


def _model_residency_truth(
    model_id: str,
    installed: set[str],
    running: dict[str, Any] | None,
) -> dict[str, Any]:
    resident = running is not None
    size = int(running.get("size", 0)) if running else None
    size_vram = int(running.get("size_vram", 0)) if running else None
    processor = None
    if running and size is not None and size_vram is not None:
        processor = "GPU" if size > 0 and size_vram >= size else "PARTIAL_GPU" if size_vram > 0 else "CPU"
    expires_at = str(running.get("expires_at", "")).strip() if running else ""
    return {
        "model_id": model_id,
        "installed": model_id in installed,
        "requested": None,
        "loading": None,
        "resident": resident,
        "processor": processor,
        "size": size,
        "size_vram": size_vram,
        "context_length": int(running.get("context_length", 0)) if running else None,
        "expires_at": expires_at or None,
        "configured_idle_timeout_seconds": OLLAMA_LIVE_MODEL_IDLE_TIMEOUT_SECONDS,
        "unload_due_at": expires_at or None,
        "model_last_used_at": None,
        "model_idle_seconds": None,
        "model_load_failure": None,
        "model_evicted_for_vram_pressure": None,
        "eviction_reason": None,
    }


def _http_alive(url: str) -> bool:
    payload = ollama_get_json(url, timeout_seconds=2.5)
    return payload.get("ok", True) is not False


def observe_runtime_preflight() -> dict[str, Any]:
    """Fresh canonical runtime observations; no start, repair or permission decision."""
    from SUPERVISOR.runtime_preflight import inspect_runtime_state
    return inspect_runtime_state()


def observe_model_provider_identity(endpoint: str, *, check_request, proc_root=None) -> dict[str, Any]:
    """Endpoint-bound physical read port; identity never grants management rights."""
    from MAKSIMAR_SERVER.EXECUTION_CONTROL.node_runtime.hardware_detection_adapter import observe_provider_process_identity
    return observe_provider_process_identity(endpoint, check_request=check_request, proc_root=proc_root)


def observe_model_provider_hardware(provider_identity: dict, *, check_request) -> dict[str, Any]:
    """Collect resource facts only for a proven provider PID, never client scope."""
    from MAKSIMAR_SERVER.EXECUTION_CONTROL.node_runtime.hardware_detection_adapter import detect_model_resource_observation
    if provider_identity.get("status") != "PROVEN":
        raise ValueError("provider_process_identity_unproven")
    pid = provider_identity.get("identity", {}).get("pid")
    if type(pid) is not int or pid <= 0:
        raise ValueError("provider_pid_unproven")
    check_request()
    observation = detect_model_resource_observation(provider_pid=pid)
    check_request()
    return observation


def classify_observed_runtime(observation: dict) -> dict[str, Any]:
    """Reuse the canonical pure classifier for the same collected snapshot."""
    from SUPERVISOR.runtime_preflight import classify_runtime_observation
    return classify_runtime_observation(observation)


def build_foundation_panel_payloads() -> dict[str, Any]:
    """Compose the three existing pure payloads from one canonical observation."""
    from MAKSIMAR_SERVER.AI_ORCHESTRATION.jarvis_live_read_models import observe_foundation_consistency
    from MAKSIMAR_CORE_LIB.oob_dashboard.system_status_panel_payload_builder import build_system_status_panel_payload
    from MAKSIMAR_CORE_LIB.oob_dashboard.topology_panel_payload_builder import build_topology_panel_payload
    from MAKSIMAR_CORE_LIB.oob_dashboard.guard_chain_panel_payload_builder import build_guard_chain_panel_payload
    observation = observe_foundation_consistency()
    # Explicit empty input prevents legacy/no-argument acquisition after unavailable observation.
    if not isinstance(observation, dict):
        observation = {}
    return {
        "system_status": build_system_status_panel_payload(observation=observation),
        "topology": build_topology_panel_payload(observation=observation),
        "guard_chain": build_guard_chain_panel_payload(observation=observation),
    }


def build_system_status_panel_payload() -> dict[str, Any]:
    return build_foundation_panel_payloads()["system_status"]


def build_topology_panel_payload() -> dict[str, Any]:
    return build_foundation_panel_payloads()["topology"]


def build_guard_chain_panel_payload() -> dict[str, Any]:
    return build_foundation_panel_payloads()["guard_chain"]
