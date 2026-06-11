from __future__ import annotations

import importlib
from typing import Any, Iterator


def build_jarvis_live_brain_health() -> dict[str, Any]:
    return _brain_loop().build_jarvis_live_brain_health()


def build_jarvis_live_session_status() -> dict[str, Any]:
    return _brain_loop().build_jarvis_live_session_status()


def run_jarvis_live_brain_once(user_text: str, session_id: str = "windows_voice_edge") -> dict[str, Any]:
    return _brain_loop().run_jarvis_live_brain_once(user_text, session_id=session_id)


def stream_jarvis_live_brain_response(
    user_text: str,
    session_id: str = "windows_voice_edge",
) -> Iterator[dict[str, Any]]:
    yield from _brain_loop().stream_jarvis_live_brain_response(user_text, session_id=session_id)


def write_stream_event_safely(write_callable: Any, event: dict[str, Any]) -> bool:
    return _brain_loop().write_stream_event_safely(write_callable, event)


def _brain_loop() -> Any:
    return importlib.import_module("tools.jarvis_live_runtime.jarvis_live_brain_loop")
