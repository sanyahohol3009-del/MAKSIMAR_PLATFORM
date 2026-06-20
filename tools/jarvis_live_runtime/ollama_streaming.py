from __future__ import annotations

import json
import os
from typing import Any, Iterator

import httpx

from tools.jarvis_live_runtime.jarvis_live_response_mode import (
    build_ollama_options,
    classify_response_mode,
)
from tools.jarvis_live_runtime.ollama_transport import (
    OLLAMA_CHAT_URL,
    OLLAMA_FAST_CHAT_KEEP_ALIVE,
    OLLAMA_FAST_CHAT_NUM_PREDICT,
    OLLAMA_FAST_CHAT_TEMPERATURE,
    OLLAMA_FAST_CHAT_THINK,
    OLLAMA_FAST_CHAT_TOP_P,
    OLLAMA_URL,
    timeout_policy_for_model_id,
)


def _event(event: str, **payload: Any) -> dict[str, Any]:
    return {"event": event, **payload, "pc_control_allowed": False}


def _effective_timeout_seconds(model_id: str, timeout_seconds: float | None) -> float:
    if timeout_seconds is not None and timeout_seconds > 0:
        return float(timeout_seconds)
    return float(timeout_policy_for_model_id(model_id)["total_request_timeout_seconds"])


def _httpx_timeout_for_model(model_id: str, timeout_seconds: float | None) -> httpx.Timeout:
    policy = timeout_policy_for_model_id(model_id)
    total = _effective_timeout_seconds(model_id, timeout_seconds)
    return httpx.Timeout(
        total,
        connect=min(float(policy["model_load_timeout_seconds"]), total),
        read=min(float(policy["stream_idle_timeout_seconds"]), total),
        write=min(float(policy["model_load_timeout_seconds"]), total),
        pool=min(float(policy["model_load_timeout_seconds"]), total),
    )


def _stream_ollama_model(
    model_id: str,
    prompt: str,
    route_mode: str,
    timeout_seconds: float | None = None,
    response_mode_text: str | None = None,
) -> Iterator[dict[str, Any]]:
    transport_plan = _ollama_transport_plan(route_mode, prompt, response_mode_text or prompt)
    if route_mode != "FAST":
        yield from _stream_ollama_generate_model(
            model_id,
            prompt,
            route_mode,
            timeout_seconds=timeout_seconds,
            response_mode_text=response_mode_text,
        )
        return

    primary_endpoint = transport_plan["primary_endpoint"]
    fallback_endpoint = transport_plan["fallback_endpoint"]
    primary_error_reason: dict[str, Any] | None = None
    thinking_chunk_count = 0
    answer_chunk_count = 0
    tool_call_count = 0
    primary_done_event: dict[str, Any] = {}
    for event in _stream_ollama_chat_model(
        model_id,
        prompt,
        timeout_seconds=timeout_seconds,
        response_mode=transport_plan["response_mode"],
        response_mode_text=response_mode_text or prompt,
    ):
        event_type = str(event.get("event", ""))
        if event_type == "thinking":
            thinking_chunk_count += 1
            yield event
            continue
        if event_type == "tool_call":
            tool_call_count += int(event.get("tool_call_count", 0))
            yield event
            continue
        if event_type == "chunk":
            answer_chunk_count += 1
            yield event
            continue
        if event_type == "done":
            primary_done_event = event
            break
        if event_type == "error":
            primary_error_reason = {
                "error_kind": "ollama_chat_stream_error",
                "error_message": str(event.get("error_message", "ollama chat returned an error")),
                "ollama_model_used": model_id,
                "ollama_endpoint": primary_endpoint,
            }
            break

    if answer_chunk_count > 0 or tool_call_count > 0:
        primary_done_event = {
            **primary_done_event,
            "tool_call_count": tool_call_count,
            "tool_call_detected": bool(tool_call_count),
        }
        done_event = {
            **primary_done_event,
            "event": "done",
            "ollama_model_used": model_id,
            "ollama_endpoint": primary_endpoint,
            "primary_endpoint": primary_endpoint,
            "fallback_endpoint": fallback_endpoint,
            "ollama_endpoint_fallback_used": False,
            "think_mode": transport_plan["think_mode"],
            "ollama_num_predict": transport_plan["ollama_num_predict"],
            "ollama_temperature": transport_plan["ollama_temperature"],
            "ollama_top_p": transport_plan["ollama_top_p"],
        }
        yield done_event
        return

    fallback_reason = primary_error_reason
    if fallback_reason is None and thinking_chunk_count > 0:
        fallback_reason = {
            "error_kind": "ollama_thinking_without_final_response",
            "error_message": "model produced thinking but no final response; increase num_predict or disable thinking.",
            "ollama_model_used": model_id,
            "ollama_endpoint": primary_endpoint,
        }
    if fallback_reason is None and primary_done_event:
        fallback_reason = {
            "error_kind": "ollama_chat_empty_response",
            "error_message": "chat endpoint returned done without content",
            "ollama_model_used": model_id,
            "ollama_endpoint": primary_endpoint,
        }
    if fallback_reason is None:
        fallback_reason = {
            "error_kind": "ollama_chat_unavailable",
            "error_message": "chat endpoint unavailable",
            "ollama_model_used": model_id,
            "ollama_endpoint": primary_endpoint,
        }
    yield from _collect_generate_stream_events(
        model_id=model_id,
        prompt=prompt,
        route_mode=route_mode,
        timeout_seconds=timeout_seconds,
        response_mode_text=response_mode_text,
        fallback_reason=fallback_reason,
        primary_endpoint=primary_endpoint,
        fallback_endpoint=fallback_endpoint,
    )


def _build_ollama_chat_payload(
    model_id: str,
    system_prompt: str,
    user_text: str,
    think_mode: bool | str = OLLAMA_FAST_CHAT_THINK,
    num_predict: int = OLLAMA_FAST_CHAT_NUM_PREDICT,
    temperature: float = OLLAMA_FAST_CHAT_TEMPERATURE,
    top_p: float = OLLAMA_FAST_CHAT_TOP_P,
    keep_alive: str = OLLAMA_FAST_CHAT_KEEP_ALIVE,
    tools: list[dict[str, Any]] | None = None,
) -> dict[str, Any]:
    payload: dict[str, Any] = {
        "model": model_id,
        "stream": True,
        "messages": [
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_text},
        ],
        "think": think_mode,
        "keep_alive": keep_alive,
        "options": {
            "num_predict": num_predict,
            "temperature": temperature,
            "top_p": top_p,
        },
    }
    if tools:
        payload["tools"] = tools
    return payload


def _parse_ollama_chat_stream_event(payload: dict[str, Any], model_id: str) -> tuple[dict[str, Any], ...]:
    events: list[dict[str, Any]] = []
    if payload.get("error"):
        events.append(
            _event(
                "error",
                ollama_model_used=model_id,
                error_message=str(payload.get("error", "")),
            )
        )
        return tuple(events)
    message = payload.get("message") if isinstance(payload.get("message"), dict) else {}
    thinking = str(message.get("thinking", "") or payload.get("thinking", ""))
    content = str(message.get("content", "") or payload.get("response", "") or payload.get("content", ""))
    tool_calls = message.get("tool_calls") if isinstance(message, dict) else None
    if not isinstance(tool_calls, list):
        tool_calls = payload.get("tool_calls") if isinstance(payload.get("tool_calls"), list) else []
    if thinking:
        events.append(_event("thinking", text=thinking, ollama_model_used=model_id))
    if tool_calls:
        events.append(
            _event(
                "tool_call",
                ollama_model_used=model_id,
                tool_call_detected=True,
                tool_call_count=len(tool_calls),
                tool_calls=tuple(tool_calls),
                execution_allowed=False,
                approval_required=True,
                proposal_only=True,
            )
        )
    if content:
        events.append(_event("chunk", text=content, ollama_model_used=model_id))
    if payload.get("done") is True:
        events.append(_event("done", ollama_model_used=model_id))
    return tuple(events)


def _stream_ollama_chat_model(
    model_id: str,
    prompt: str,
    timeout_seconds: float | None = None,
    response_mode: Any | None = None,
    response_mode_text: str | None = None,
) -> Iterator[dict[str, Any]]:
    system_prompt, user_text = _split_chat_prompt(prompt, response_mode_text or prompt)
    payload = _build_ollama_chat_payload(
        model_id,
        system_prompt=system_prompt,
        user_text=user_text,
        think_mode=OLLAMA_FAST_CHAT_THINK,
        num_predict=OLLAMA_FAST_CHAT_NUM_PREDICT,
        temperature=OLLAMA_FAST_CHAT_TEMPERATURE,
        top_p=OLLAMA_FAST_CHAT_TOP_P,
        keep_alive=OLLAMA_FAST_CHAT_KEEP_ALIVE,
    )
    timeout = _httpx_timeout_for_model(model_id, timeout_seconds)
    try:
        with httpx.Client(timeout=timeout) as client:
            with client.stream("POST", OLLAMA_CHAT_URL, json=payload) as response:
                response.raise_for_status()
                for line in response.iter_lines():
                    if not line:
                        continue
                    try:
                        chat_payload = json.loads(line)
                    except json.JSONDecodeError as exc:
                        yield _event(
                            "error",
                            ollama_model_used=model_id,
                            error_message=f"json_decode_error: {exc}",
                            ollama_endpoint=OLLAMA_CHAT_URL,
                            primary_endpoint=OLLAMA_CHAT_URL,
                            fallback_endpoint=OLLAMA_URL,
                            ollama_endpoint_fallback_used=False,
                            think_mode="false",
                            ollama_num_predict=OLLAMA_FAST_CHAT_NUM_PREDICT,
                            ollama_temperature=OLLAMA_FAST_CHAT_TEMPERATURE,
                            ollama_top_p=OLLAMA_FAST_CHAT_TOP_P,
                        )
                        return
                    for event in _parse_ollama_chat_stream_event(chat_payload, model_id):
                        event.setdefault("ollama_endpoint", OLLAMA_CHAT_URL)
                        event.setdefault("primary_endpoint", OLLAMA_CHAT_URL)
                        event.setdefault("fallback_endpoint", OLLAMA_URL)
                        event.setdefault("ollama_endpoint_fallback_used", False)
                        event.setdefault("think_mode", "false")
                        event.setdefault("ollama_num_predict", OLLAMA_FAST_CHAT_NUM_PREDICT)
                        event.setdefault("ollama_temperature", OLLAMA_FAST_CHAT_TEMPERATURE)
                        event.setdefault("ollama_top_p", OLLAMA_FAST_CHAT_TOP_P)
                        yield event
    except (httpx.HTTPError, TimeoutError, BrokenPipeError, ConnectionResetError, ConnectionAbortedError) as exc:
        yield _event(
            "error",
            ollama_model_used=model_id,
            error_message=f"{exc.__class__.__name__}: {exc}",
            ollama_endpoint=OLLAMA_CHAT_URL,
            primary_endpoint=OLLAMA_CHAT_URL,
            fallback_endpoint=OLLAMA_URL,
            ollama_endpoint_fallback_used=False,
            think_mode="false",
            ollama_num_predict=OLLAMA_FAST_CHAT_NUM_PREDICT,
            ollama_temperature=OLLAMA_FAST_CHAT_TEMPERATURE,
            ollama_top_p=OLLAMA_FAST_CHAT_TOP_P,
        )


def _stream_ollama_generate_model(
    model_id: str,
    prompt: str,
    route_mode: str,
    timeout_seconds: float | None = None,
    response_mode_text: str | None = None,
) -> Iterator[dict[str, Any]]:
    response_mode = classify_response_mode(response_mode_text or prompt)
    options = build_ollama_options(response_mode)
    request_payload: dict[str, Any] = {
        "model": model_id,
        "prompt": prompt,
        "stream": True,
        "options": options,
        "keep_alive": os.environ.get("JARVIS_LIVE_OLLAMA_KEEP_ALIVE", "30m"),
    }
    try:
        timeout = _httpx_timeout_for_model(model_id, timeout_seconds)
        with httpx.Client(timeout=timeout) as client:
            with client.stream("POST", OLLAMA_URL, json=request_payload) as response:
                response.raise_for_status()
                for line in response.iter_lines():
                    if not line:
                        continue
                    try:
                        payload = json.loads(line)
                    except json.JSONDecodeError:
                        continue
                    if payload.get("error"):
                        yield _event(
                            "error",
                            ollama_model_used=model_id,
                            error_message=str(payload.get("error", "")),
                            ollama_endpoint=OLLAMA_URL,
                            primary_endpoint=OLLAMA_URL,
                            fallback_endpoint="",
                            ollama_endpoint_fallback_used=False,
                            think_mode="generate",
                            ollama_num_predict=options.get("num_predict", 0),
                            ollama_temperature=options.get("temperature", 0.0),
                            ollama_top_p=options.get("top_p", 0.0),
                        )
                        return
                    thinking = str(payload.get("thinking", ""))
                    if thinking:
                        yield _event("thinking", text=thinking, ollama_model_used=model_id, ollama_endpoint=OLLAMA_URL)
                    chunk = str(payload.get("response", ""))
                    if chunk:
                        yield _event("chunk", text=chunk, ollama_model_used=model_id, ollama_endpoint=OLLAMA_URL)
                    if payload.get("done") is True:
                        yield _event(
                            "done",
                            ollama_model_used=model_id,
                            ollama_endpoint=OLLAMA_URL,
                            primary_endpoint=OLLAMA_URL,
                            fallback_endpoint="",
                            ollama_endpoint_fallback_used=False,
                            think_mode="generate",
                            ollama_num_predict=options.get("num_predict", 0),
                            ollama_temperature=options.get("temperature", 0.0),
                            ollama_top_p=options.get("top_p", 0.0),
                        )
                        return
    except (httpx.HTTPError, TimeoutError, BrokenPipeError, ConnectionResetError, ConnectionAbortedError) as exc:
        yield _event(
            "error",
            ollama_model_used=model_id,
            error_message=f"{exc.__class__.__name__}: {exc}",
            ollama_endpoint=OLLAMA_URL,
            primary_endpoint=OLLAMA_URL,
            fallback_endpoint="",
            ollama_endpoint_fallback_used=False,
            think_mode="generate",
            ollama_num_predict=options.get("num_predict", 0),
            ollama_temperature=options.get("temperature", 0.0),
            ollama_top_p=options.get("top_p", 0.0),
        )


def _ollama_transport_plan(
    route_mode: str,
    prompt: str,
    response_mode_text: str,
) -> dict[str, Any]:
    response_mode = classify_response_mode(response_mode_text or prompt)
    if route_mode == "FAST":
        return {
            "response_mode": response_mode,
            "primary_endpoint": OLLAMA_CHAT_URL,
            "fallback_endpoint": OLLAMA_URL,
            "think_mode": "false",
            "ollama_num_predict": OLLAMA_FAST_CHAT_NUM_PREDICT,
            "ollama_temperature": OLLAMA_FAST_CHAT_TEMPERATURE,
            "ollama_top_p": OLLAMA_FAST_CHAT_TOP_P,
            "keep_alive": OLLAMA_FAST_CHAT_KEEP_ALIVE,
        }
    options = build_ollama_options(response_mode)
    return {
        "response_mode": response_mode,
        "primary_endpoint": OLLAMA_URL,
        "fallback_endpoint": "",
        "think_mode": "generate",
        "ollama_num_predict": int(options.get("num_predict", 0)),
        "ollama_temperature": float(options.get("temperature", 0.0)),
        "ollama_top_p": float(options.get("top_p", 0.0)),
        "keep_alive": os.environ.get("JARVIS_LIVE_OLLAMA_KEEP_ALIVE", "30m"),
    }


def _split_chat_prompt(prompt: str, fallback_user_text: str) -> tuple[str, str]:
    marker = "\nUSER_MESSAGE: "
    if marker in prompt:
        system_prompt, user_text = prompt.rsplit(marker, 1)
        user_text = user_text.strip() or fallback_user_text
        return system_prompt.strip(), user_text
    return prompt.strip(), fallback_user_text


def _collect_chat_stream_events(
    model_id: str,
    prompt: str,
    timeout_seconds: float | None,
    response_mode: Any | None,
    response_mode_text: str,
) -> dict[str, Any]:
    events: list[dict[str, Any]] = []
    thinking_chunk_count = 0
    answer_chunk_count = 0
    tool_call_count = 0
    primary_error_event: dict[str, Any] | None = None
    done_event: dict[str, Any] = {}
    for event in _stream_ollama_chat_model(
        model_id,
        prompt,
        timeout_seconds=timeout_seconds,
        response_mode=response_mode,
        response_mode_text=response_mode_text,
    ):
        event_type = str(event.get("event", ""))
        if event_type == "thinking":
            thinking_chunk_count += 1
            events.append(event)
            continue
        if event_type == "tool_call":
            tool_call_count += int(event.get("tool_call_count", 0))
            events.append(event)
            continue
        if event_type == "chunk":
            answer_chunk_count += 1
            events.append(event)
            continue
        if event_type == "error":
            primary_error_event = {
                "error_kind": "ollama_chat_stream_error",
                "error_message": str(event.get("error_message", "ollama chat returned an error")),
                "ollama_model_used": model_id,
                "ollama_endpoint": OLLAMA_CHAT_URL,
            }
            break
        if event_type == "done":
            done_event = event
            break
    return {
        "events": tuple(events),
        "done_event": done_event,
        "thinking_chunk_count": thinking_chunk_count,
        "answer_chunk_count": answer_chunk_count,
        "tool_call_count": tool_call_count,
        "primary_error_event": primary_error_event,
        "ollama_endpoint": OLLAMA_CHAT_URL,
        "primary_endpoint": OLLAMA_CHAT_URL,
        "fallback_endpoint": OLLAMA_URL,
        "think_mode": "false",
        "ollama_num_predict": OLLAMA_FAST_CHAT_NUM_PREDICT,
        "ollama_temperature": OLLAMA_FAST_CHAT_TEMPERATURE,
        "ollama_top_p": OLLAMA_FAST_CHAT_TOP_P,
        "ollama_endpoint_fallback_used": False,
    }


def _collect_generate_stream_events(
    model_id: str,
    prompt: str,
    route_mode: str,
    timeout_seconds: float | None,
    response_mode_text: str | None,
    fallback_reason: dict[str, Any] | None,
    primary_endpoint: str,
    fallback_endpoint: str,
) -> Iterator[dict[str, Any]]:
    response_mode = classify_response_mode(response_mode_text or prompt)
    options = build_ollama_options(response_mode)
    for event in _stream_ollama_generate_model(
        model_id,
        prompt,
        route_mode,
        timeout_seconds=timeout_seconds,
        response_mode_text=response_mode_text,
    ):
        if fallback_reason:
            enriched = {
                **event,
                "primary_endpoint": primary_endpoint,
                "fallback_endpoint": fallback_endpoint,
                "ollama_endpoint_fallback_used": True,
                "primary_error_kind": str(fallback_reason.get("error_kind", "")),
                "primary_error_message": str(fallback_reason.get("error_message", "")),
                "think_mode": "generate",
                "ollama_num_predict": options.get("num_predict", 0),
                "ollama_temperature": options.get("temperature", 0.0),
                "ollama_top_p": options.get("top_p", 0.0),
            }
            if event.get("event") == "error":
                enriched.setdefault("error_kind", str(fallback_reason.get("error_kind", "ollama_stream_error")))
            if event.get("event") == "done" and not enriched.get("error_kind"):
                enriched["error_kind"] = ""
            yield enriched
        else:
            yield event
