from __future__ import annotations

import os
from typing import Any

import httpx


OLLAMA_URL = os.environ.get(
    "JARVIS_LIVE_OLLAMA_URL",
    "http://127.0.0.1:11434/api/generate",
)
OLLAMA_CHAT_URL = os.environ.get(
    "JARVIS_LIVE_OLLAMA_CHAT_URL",
    OLLAMA_URL.replace("/api/generate", "/api/chat"),
)
OLLAMA_BASE_URL = OLLAMA_URL.rsplit("/api/", 1)[0] if "/api/" in OLLAMA_URL else OLLAMA_URL.rstrip("/")

PRIMARY_CONVERSATION_MODEL_ID = "jarvis:chat8b"
DEFAULT_OLLAMA_MODEL_ID = os.environ.get(
    "JARVIS_LIVE_OLLAMA_MODEL",
    PRIMARY_CONVERSATION_MODEL_ID,
)
FALLBACK_OLLAMA_MODEL_ID = "jarvis-live:qwen14b"
HEAVY_CODER_MODEL_ID = "jarvis:coder14b"
BASE_HEAVY_CODER_MODEL_ID = "qwen2.5-coder:14b"

OLLAMA_FAST_CHAT_NUM_PREDICT = 160
OLLAMA_FAST_CHAT_TEMPERATURE = 0.8
OLLAMA_FAST_CHAT_TOP_P = 0.95
OLLAMA_FAST_CHAT_KEEP_ALIVE = "30m"
OLLAMA_FAST_CHAT_THINK = False


def ollama_get_json(path: str, timeout_seconds: float = 5.0) -> dict[str, Any]:
    url = path if path.startswith("http") else f"{OLLAMA_BASE_URL}{path}"
    try:
        response = httpx.get(url, timeout=timeout_seconds)
        response.raise_for_status()
        payload = response.json()
    except Exception as exc:
        return {"ok": False, "error": type(exc).__name__, "message": str(exc)}
    return payload if isinstance(payload, dict) else {"ok": False, "payload": payload}


def ollama_post_json(path: str, payload: dict[str, Any], timeout_seconds: float = 10.0) -> dict[str, Any]:
    url = path if path.startswith("http") else f"{OLLAMA_BASE_URL}{path}"
    try:
        response = httpx.post(url, json=payload, timeout=timeout_seconds)
        response.raise_for_status()
        result = response.json()
    except Exception as exc:
        return {"ok": False, "error": type(exc).__name__, "message": str(exc)}
    return result if isinstance(result, dict) else {"ok": False, "payload": result}


def ollama_transport_read_model() -> dict[str, object]:
    return {
        "transport_id": "ollama_local_model_engine_transport_v1",
        "ollama_url": OLLAMA_URL,
        "ollama_chat_url": OLLAMA_CHAT_URL,
        "ollama_base_url": OLLAMA_BASE_URL,
        "primary_conversation_model": PRIMARY_CONVERSATION_MODEL_ID,
        "default_model": DEFAULT_OLLAMA_MODEL_ID,
        "fallback_model": FALLBACK_OLLAMA_MODEL_ID,
        "heavy_coder_model": HEAVY_CODER_MODEL_ID,
        "base_heavy_coder_model": BASE_HEAVY_CODER_MODEL_ID,
        "direct_edge_to_ollama_allowed": False,
        "model_engine_only": True,
        "control_plane_required": True,
    }
