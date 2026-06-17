from __future__ import annotations

from tools.jarvis_live_runtime.ollama_transport import (
    OLLAMA_CHAT_URL,
    OLLAMA_URL,
    PRIMARY_CONVERSATION_MODEL_ID,
    ollama_transport_read_model,
)


def test_ollama_transport_is_model_engine_not_edge_brain() -> None:
    model = ollama_transport_read_model()

    assert model["model_engine_only"] is True
    assert model["control_plane_required"] is True
    assert model["direct_edge_to_ollama_allowed"] is False
    assert "127.0.0.1:11434" in OLLAMA_URL
    assert OLLAMA_CHAT_URL.endswith("/api/chat")
    assert PRIMARY_CONVERSATION_MODEL_ID == "jarvis:chat8b"


def test_ollama_transport_read_model_has_required_roles() -> None:
    model = ollama_transport_read_model()

    assert model["primary_conversation_model"] == "jarvis:chat8b"
    assert model["fallback_model"] == "jarvis-live:qwen14b"
    assert model["heavy_coder_model"] == "jarvis:coder14b"
    assert model["base_heavy_coder_model"] == "qwen2.5-coder:14b"
