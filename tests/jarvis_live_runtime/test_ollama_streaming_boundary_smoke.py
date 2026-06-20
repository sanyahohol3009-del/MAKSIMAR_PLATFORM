from __future__ import annotations

import inspect

from tools.jarvis_live_runtime import jarvis_live_brain_loop
from tools.jarvis_live_runtime.ollama_streaming import (
    _build_ollama_chat_payload,
    _ollama_transport_plan,
    _split_chat_prompt,
    _stream_ollama_model,
)


def test_brain_loop_uses_extracted_ollama_streaming_module() -> None:
    assert inspect.getmodule(jarvis_live_brain_loop._stream_ollama_model).__name__ == (
        "tools.jarvis_live_runtime.ollama_streaming"
    )
    assert inspect.getmodule(_stream_ollama_model).__name__ == (
        "tools.jarvis_live_runtime.ollama_streaming"
    )


def test_split_chat_prompt_keeps_legacy_prompt_when_no_response_mode_text() -> None:
    system, user = _split_chat_prompt("SYSTEM\n\nUSER", "fallback")
    assert system == "SYSTEM\n\nUSER"
    assert user == "fallback"

    system2, user2 = _split_chat_prompt("ONLY USER", "fallback text")
    assert system2 == "ONLY USER"
    assert user2 == "fallback text"


def test_ollama_chat_payload_keeps_fast_policy() -> None:
    payload = _build_ollama_chat_payload("jarvis:chat8b", "system", "hello")

    assert payload["model"] == "jarvis:chat8b"
    assert payload["stream"] is True
    assert payload["messages"][0]["role"] == "system"
    assert payload["messages"][1]["role"] == "user"
    assert payload["options"]["num_predict"] == 1024


def test_ollama_transport_plan_fast_uses_chat_endpoint() -> None:
    plan = _ollama_transport_plan("FAST", "prompt", "hello")

    assert plan["primary_endpoint"].endswith("/api/chat")
    assert plan["fallback_endpoint"].endswith("/api/generate")
    assert plan["ollama_num_predict"] == 1024
