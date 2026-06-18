from __future__ import annotations

import json
import os
from typing import Any, Iterator

from MAKSIMAR_CORE_LIB.ai_orchestration.model_profile_registry_contract import (
    build_jarvis_live_runtime_model_role_read_model,
    select_jarvis_live_model_role,
)
from tools.jarvis_live_runtime.ollama_transport import (
    BASE_HEAVY_CODER_MODEL_ID,
    DEFAULT_OLLAMA_MODEL_ID,
    FALLBACK_OLLAMA_MODEL_ID,
    HEAVY_CODER_MODEL_ID,
)
from tools.jarvis_live_runtime.voice_response_cleaner import clean_voice_response


def write_stream_event_safely(write_callable: Any, event: dict[str, Any]) -> bool:
    try:
        write_callable(json.dumps(event, ensure_ascii=False) + "\n")
    except (BrokenPipeError, ConnectionResetError, ConnectionAbortedError):
        print("[WARNING] Client disconnected before receiving response")
        return False
    return True


def _command_timeout_seconds(value: float | None) -> float:
    if value is not None and value > 0:
        return float(value)
    raw = os.environ.get("JARVIS_LIVE_COMMAND_TIMEOUT_SECONDS", "120")
    try:
        parsed = float(raw)
    except ValueError:
        return 120.0
    return max(1.0, parsed)


def _command_error_payload(user_text: str, error_kind: str) -> dict[str, Any]:
    selected = select_jarvis_live_model_role(user_text)
    memory = build_jarvis_live_memory_federation_status()
    return {
        "event": "done",
        "response_text": "JARVIS command runtime не успел вернуть модельный ответ. Запрос не выполнен как действие; можно повторить или проверить Ollama статус.",
        "ollama_model_used": "",
        "route_mode": _route_mode(user_text),
        "stream_chunk_count": 0,
        "retrieved_snippet_count": 0,
        "retrieval_surfaces_used": (),
        "memory_federation_available": memory["memory_federation_available"],
        "mempalace_status": memory["mempalace_status"],
        "selected_model_role": selected["selected_model_role"],
        "selected_model_id": selected["model_id"],
        "selected_model_status": selected["status"],
        "admission_allowed": False,
        "resource_gate_surface": "MAKSIMAR_CORE_LIB/execution_control/admission_contract.py",
        "session_memory_path": str(SESSION_STATE_PATH),
        "local_chat_memory_path": str(_session_turn_log_path()),
        "runtime_history_store_path": str(RUNTIME_HISTORY_STORE),
        "runtime_history_store_exists": RUNTIME_HISTORY_STORE.exists(),
        "memory_truth_split": _memory_truth_split(),
        "dangerous_mutation_flags": dict(DANGEROUS_MEMORY_FLAGS),
        "error_kind": error_kind,
        "canonical_memory_write_allowed": False,
        "pc_control_allowed": False,
    }


def _candidate_model_ids_for_context(context: JarvisBrainContext) -> tuple[str, ...]:
    selected_model_id = str(context.selected_model_role["model_id"])
    role_id = context.selected_model_role["selected_model_role"]
    candidates = [selected_model_id]
    if context.route_mode == "FAST" and os.environ.get("JARVIS_LIVE_FAST_FALLBACK_ENABLED") != "1":
        return tuple(candidates)
    if role_id == "heavy_coder_model":
        candidates.extend((HEAVY_CODER_MODEL_ID, BASE_HEAVY_CODER_MODEL_ID, FALLBACK_OLLAMA_MODEL_ID))
    elif role_id == "daily_coder_model":
        candidates.extend(("jarvis:coder7b", FALLBACK_OLLAMA_MODEL_ID))
    elif role_id == "helper_classifier_model":
        candidates.extend(("jarvis:helper3b", DEFAULT_OLLAMA_MODEL_ID))
    else:
        candidates.extend((DEFAULT_OLLAMA_MODEL_ID, FALLBACK_OLLAMA_MODEL_ID))
    return tuple(dict.fromkeys(candidates))


def _build_admission_status(selected_model_role: dict[str, Any]) -> dict[str, Any]:
    role_id = str(selected_model_role["selected_model_role"])
    exclusive_gpu_required = role_id == "heavy_coder_model"
    return {
        "admission_allowed": True,
        "enqueue_required": True,
        "queue_surface": "MAKSIMAR_CORE_LIB/execution_control",
        "resource_gate_surface": "MAKSIMAR_CORE_LIB/execution_control/admission_contract.py",
        "worker_registry_surface": "MAKSIMAR_CORE_LIB/workers_registry",
        "exclusive_gpu_required": exclusive_gpu_required,
        "concurrent_heavy_jobs_allowed": False,
        "agents_enabled": False,
        "agents_may_call_14b_directly": False,
        "pc_control_allowed": False,
    }


def _sanitize_model_output(text: str) -> str:
    return clean_voice_response(text)


def _filter_reasoning_chunk(chunk: str, state: dict[str, bool]) -> str:
    text = chunk
    visible = ""
    while text:
        lowered = text.casefold()
        if state.get("inside_reasoning", False):
            end_positions = [
                pos
                for marker in ("</think>", "</thinking>")
                if (pos := lowered.find(marker)) != -1
            ]
            if not end_positions:
                return visible
            end = min(end_positions)
            marker = "</think>" if lowered.startswith("</think>", end) else "</thinking>"
            text = text[end + len(marker) :]
            state["inside_reasoning"] = False
            continue
        start_positions = [
            pos
            for marker in ("<think>", "<thinking>", "thinking:", "reasoning:", "мысли:", "рассуждение:")
            if (pos := lowered.find(marker)) != -1
        ]
        if not start_positions:
            visible += text
            break
        start = min(start_positions)
        visible += text[:start]
        if lowered.startswith("thinking:", start) or lowered.startswith("reasoning:", start) or lowered.startswith("мысли:", start) or lowered.startswith("рассуждение:", start):
            paragraph_end = text.find("\n\n", start)
            if paragraph_end == -1:
                return visible
            text = text[paragraph_end + 2 :]
            continue
        state["inside_reasoning"] = True
        text = text[start:]
    return visible


def _sentence_chunks(text: str) -> Iterator[str]:
    buffer = ""
    for char in text:
        buffer += char
        if char in ".!?…":
            yield buffer
            buffer = ""
    if buffer:
        yield buffer


def _event(event: str, **payload: Any) -> dict[str, Any]:
    return {"event": event, **payload, "pc_control_allowed": False}
