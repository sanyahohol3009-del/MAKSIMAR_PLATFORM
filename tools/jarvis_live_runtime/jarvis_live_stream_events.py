from __future__ import annotations

import os
from typing import Any, Iterator

from MAKSIMAR_SERVER.AI_ORCHESTRATION.jarvis_live_brain_loop_server_adapter import write_stream_event_safely
from MAKSIMAR_SERVER.AI_ORCHESTRATION.ollama_transport import timeout_policy_for_model_role
from tools.jarvis_live_runtime.voice_response_cleaner import strip_reasoning_blocks




def _command_timeout_seconds(value: float | None, selected_model_role_id: str = "jarvis_chat_model") -> float:
    if value is not None and value > 0:
        return float(value)
    raw = os.environ.get(
        "JARVIS_LIVE_COMMAND_TIMEOUT_SECONDS",
        str(timeout_policy_for_model_role(selected_model_role_id)["total_request_timeout_seconds"]),
    )
    try:
        parsed = float(raw)
    except ValueError:
        return float(timeout_policy_for_model_role(selected_model_role_id)["total_request_timeout_seconds"])
    return max(1.0, parsed)


def _sanitize_model_output(text: str) -> str:
    return strip_reasoning_blocks(text)


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
