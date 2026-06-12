from __future__ import annotations

import json
import sys
import urllib.error
import urllib.request
from typing import Any


API_BASE_URL = "http://127.0.0.1:8765"
COMMAND_URL = f"{API_BASE_URL}/jarvis-live/command"
STREAM_URL = f"{API_BASE_URL}/jarvis-live/chat/stream"
HEALTH_URL = f"{API_BASE_URL}/jarvis-live/health"
STATUS_URL = f"{API_BASE_URL}/jarvis-live/status"
SESSION_ID = "terminal_chat"
HEALTH_TIMEOUT_SECONDS = 10
COMMAND_TIMEOUT_SECONDS = 240
_LAST_API_ERROR = ""


def main() -> int:
    _configure_utf8_stdio()
    print(
        "JARVIS terminal chat ready. API: http://127.0.0.1:8765  "
        "Commands: /ping /status /memory /models /stream /command /exit"
    )
    _print_ping(startup=True)
    while True:
        try:
            user_text = _sanitize_text(input("JARVIS> ")).strip()
        except (EOFError, KeyboardInterrupt):
            print()
            return 0
        if not user_text:
            continue
        try:
            should_exit = _dispatch_user_text(user_text)
        except KeyboardInterrupt:
            print("\nrequest_interrupted=true")
            continue
        if should_exit:
            return 0


def _dispatch_user_text(user_text: str) -> bool:
    if user_text == "/exit":
        return True
    if user_text == "/ping":
        _print_ping()
        return False
    if user_text == "/status":
        _print_status()
        return False
    if user_text == "/memory":
        _print_memory()
        return False
    if user_text == "/models":
        _print_models()
        return False
    if user_text.startswith("/command "):
        _print_command_response(user_text[len("/command ") :].strip())
        return False
    if user_text.startswith("/stream "):
        _print_stream_response(user_text[len("/stream ") :].strip())
        return False
    _print_stream_response(user_text)
    return False


def _print_command_response(text: str) -> None:
    payload = {
        "text": _sanitize_text(text),
        "session_id": SESSION_ID,
        "pc_control_allowed": False,
    }
    response = _post_json(COMMAND_URL, payload)
    if response is None:
        _print_command_unavailable()
        return
    result = response.get("result") if isinstance(response.get("result"), dict) else {}
    llm_response = response.get("llm_response") or result.get("llm_response") or ""
    print(str(llm_response))
    print(f"selected_model_id={response.get('selected_model_id') or result.get('selected_model_id', '')}")
    print(f"selected_model_role={response.get('selected_model_role') or result.get('selected_model_role', '')}")
    print(f"retrieved_snippet_count={response.get('retrieved_snippet_count') or result.get('retrieved_snippet_count', 0)}")
    print(f"retrieval_surfaces_used={_csv(response.get('retrieval_surfaces_used') or result.get('retrieval_surfaces_used', ())) }")
    print(f"mempalace_status={response.get('mempalace_status') or result.get('mempalace_status', '')}")
    print(f"pc_control_allowed={str(bool(response.get('pc_control_allowed', False))).lower()}")
    print(
        "canonical_memory_write_allowed="
        f"{str(bool(response.get('canonical_memory_write_allowed', False))).lower()}"
    )


def _print_stream_response(text: str) -> None:
    if not text:
        print("stream_error=empty_text")
        return
    payload = {
        "text": _sanitize_text(text),
        "session_id": SESSION_ID,
        "pc_control_allowed": False,
    }
    if _stream_json_lines(STREAM_URL, payload) is None:
        _print_command_unavailable()


def _print_status() -> None:
    payload = _get_json(STATUS_URL) or _get_json(HEALTH_URL)
    if payload is None:
        _print_api_not_running()
        return
    print(f"api_ok={str(bool(payload.get('ok', False))).lower()}")
    print(f"default_model={payload.get('default_model', '')}")
    print(f"primary_conversation_model={payload.get('primary_conversation_model', '')}")
    print(f"memory_federation_available={str(bool(payload.get('memory_federation_available', False))).lower()}")
    print(f"pc_control_allowed={str(bool(payload.get('pc_control_allowed', False))).lower()}")
    print(
        "canonical_memory_write_allowed="
        f"{str(bool(payload.get('canonical_memory_write_allowed', False))).lower()}"
    )


def _print_memory() -> None:
    payload = _get_json(HEALTH_URL)
    if payload is None:
        _print_api_not_running()
        return
    print(f"active_retrieval_surfaces={_csv(payload.get('active_retrieval_surfaces', ())) }")
    print(f"sandbox_only_memory_surfaces={_csv(payload.get('sandbox_only_memory_surfaces', ())) }")
    print(f"disabled_memory_surfaces={_csv(payload.get('disabled_memory_surfaces', ())) }")
    print(f"mempalace_status={payload.get('mempalace_status', '')}")


def _print_models() -> None:
    payload = _get_json(HEALTH_URL)
    if payload is None:
        _print_api_not_running()
        return
    print("jarvis:chat8b = primary conversation")
    print("jarvis:helper3b = classifier/summary/router helper")
    print("jarvis:coder7b = daily/simple coder")
    print("jarvis:coder14b = heavy coder/architecture/traceback")


def _print_ping(startup: bool = False) -> None:
    payload = _get_json(HEALTH_URL)
    if payload is None:
        prefix = "startup_ping" if startup else "ping"
        print(f"{prefix}=failed")
        _print_api_not_running()
        return
    prefix = "startup_ping" if startup else "ping"
    print(f"{prefix}=ok")
    print(f"default_model={payload.get('default_model', '')}")
    print(f"pc_control_allowed={str(bool(payload.get('pc_control_allowed', False))).lower()}")
    print(
        "canonical_memory_write_allowed="
        f"{str(bool(payload.get('canonical_memory_write_allowed', False))).lower()}"
    )


def _post_json(url: str, payload: dict[str, Any]) -> dict[str, Any] | None:
    request = urllib.request.Request(
        url,
        data=json.dumps(payload, ensure_ascii=False).encode("utf-8"),
        headers={"Content-Type": "application/json; charset=utf-8"},
        method="POST",
    )
    return _request_json(request, timeout=COMMAND_TIMEOUT_SECONDS)


def _get_json(url: str) -> dict[str, Any] | None:
    request = urllib.request.Request(url, method="GET")
    return _request_json(request, timeout=HEALTH_TIMEOUT_SECONDS)


def _request_json(request: urllib.request.Request, timeout: int) -> dict[str, Any] | None:
    global _LAST_API_ERROR
    _LAST_API_ERROR = ""
    try:
        with urllib.request.urlopen(request, timeout=timeout) as response:
            raw = response.read().decode("utf-8", errors="replace")
    except urllib.error.HTTPError as exc:
        _LAST_API_ERROR = f"http_error status={exc.code} url={request.full_url}"
        return None
    except urllib.error.URLError as exc:
        _LAST_API_ERROR = _describe_url_error(exc, request.full_url)
        return None
    except TimeoutError:
        _LAST_API_ERROR = f"timeout url={request.full_url}"
        return None
    except OSError as exc:
        _LAST_API_ERROR = f"os_error {exc.__class__.__name__}: {exc} url={request.full_url}"
        return None
    try:
        payload = json.loads(raw)
    except json.JSONDecodeError:
        _LAST_API_ERROR = f"invalid_json url={request.full_url}"
        return None
    return payload if isinstance(payload, dict) else None


def _stream_json_lines(url: str, payload: dict[str, Any]) -> dict[str, Any] | None:
    global _LAST_API_ERROR
    _LAST_API_ERROR = ""
    done_event: dict[str, Any] = {}
    request = urllib.request.Request(
        url,
        data=json.dumps(payload, ensure_ascii=False).encode("utf-8"),
        headers={"Content-Type": "application/json; charset=utf-8"},
        method="POST",
    )
    try:
        with urllib.request.urlopen(request, timeout=COMMAND_TIMEOUT_SECONDS) as response:
            for raw_line in response:
                line = raw_line.decode("utf-8", errors="replace").strip()
                if not line:
                    continue
                event = _print_stream_event(line)
                if isinstance(event, dict) and str(event.get("event") or event.get("type") or "") == "done":
                    done_event = event
    except urllib.error.HTTPError as exc:
        _LAST_API_ERROR = f"http_error status={exc.code} url={url}"
        return None
    except urllib.error.URLError as exc:
        _LAST_API_ERROR = _describe_url_error(exc, url)
        return None
    except TimeoutError:
        _LAST_API_ERROR = f"timeout url={url}"
        return None
    except OSError as exc:
        _LAST_API_ERROR = f"os_error {exc.__class__.__name__}: {exc} url={url}"
        return None
    if done_event:
        _print_stream_metadata(done_event)
    return done_event or {}


def _print_stream_event(line: str) -> dict[str, Any]:
    try:
        event = json.loads(line)
    except json.JSONDecodeError:
        print(line)
        return {}
    if not isinstance(event, dict):
        print(str(event))
        return {}
    event_type = str(event.get("event") or event.get("type") or "")
    if event_type == "start":
        _print_stream_start_trace(event)
        return event
    if event_type == "route_selected":
        _print_stream_route_trace(event)
        return event
    chunk = event.get("chunk") or event.get("text") or event.get("llm_response") or ""
    if chunk:
        print(str(chunk), end="", flush=True)
        return event
    if event_type and event_type != "done":
        print(f"\nstream_event={event_type}")
    return event


def _print_stream_metadata(event: dict[str, Any]) -> None:
    print()
    print(
        "[trace] "
        f"first_token={_seconds(event.get('first_chunk_elapsed_seconds', ''))} "
        f"ollama={_seconds(event.get('ollama_elapsed_seconds', ''))} "
        f"total={_seconds(event.get('total_elapsed_seconds', ''))} "
        f"chunks={event.get('stream_chunk_count', 0)}"
    )
    print(f"selected_model_id={event.get('selected_model_id', '')}")
    print(f"selected_model_role={event.get('selected_model_role', '')}")
    print(f"retrieved_snippet_count={event.get('retrieved_snippet_count', 0)}")
    print(f"retrieval_surfaces_used={_csv(event.get('retrieval_surfaces_used', ())) }")
    print(f"mempalace_status={event.get('mempalace_status', '')}")
    print(f"pc_control_allowed={str(bool(event.get('pc_control_allowed', False))).lower()}")
    print(
        "canonical_memory_write_allowed="
        f"{str(bool(event.get('canonical_memory_write_allowed', False))).lower()}"
    )


def _print_stream_start_trace(event: dict[str, Any]) -> None:
    print(
        "[trace] "
        f"route={event.get('request_route', '')} "
        f"mode={event.get('route_mode', '')} "
        f"memory={event.get('retrieval_mode', '')} "
        f"model={event.get('selected_model_id', '')} "
        f"status={event.get('selected_model_status', '')}"
    )


def _print_stream_route_trace(event: dict[str, Any]) -> None:
    print(
        "[trace] "
        f"context={_seconds(event.get('context_elapsed_seconds', ''))} "
        f"snippets={event.get('retrieved_snippet_count', 0)} "
        f"surfaces={_csv(event.get('retrieval_surfaces_used', ())) }"
    )


def _print_command_unavailable() -> None:
    global _LAST_API_ERROR
    command_error = _LAST_API_ERROR
    if _api_is_available():
        if "timeout" in command_error:
            print("JARVIS command timed out. API is running, but the model/command route did not return in time.")
        else:
            print("JARVIS command route failed. API is running, but /jarvis-live/command did not return a usable response.")
        if command_error:
            print(f"api_error={command_error}")
        return
    _LAST_API_ERROR = command_error or _LAST_API_ERROR
    _print_api_not_running()


def _api_is_available() -> bool:
    current_error = _LAST_API_ERROR
    payload = _get_json(HEALTH_URL)
    health_error = _LAST_API_ERROR
    _set_last_api_error(current_error or health_error)
    return bool(payload and payload.get("ok"))


def _set_last_api_error(value: str) -> None:
    global _LAST_API_ERROR
    _LAST_API_ERROR = value


def _print_api_not_running() -> None:
    print(
        "JARVIS API is not running. Start it with: "
        "python -m uvicorn CONTROL_PLANE.api_server:app --host 127.0.0.1 --port 8765"
    )
    if _LAST_API_ERROR:
        print(f"api_error={_LAST_API_ERROR}")


def _describe_url_error(exc: urllib.error.URLError, url: str) -> str:
    reason = getattr(exc, "reason", exc)
    if isinstance(reason, ConnectionRefusedError):
        return f"connection_refused url={url}"
    if isinstance(reason, TimeoutError):
        return f"timeout url={url}"
    return f"url_error {reason.__class__.__name__}: {reason} url={url}"


def _csv(value: Any) -> str:
    if isinstance(value, (list, tuple)):
        return ",".join(str(item) for item in value)
    return str(value)


def _seconds(value: Any) -> str:
    if value == "" or value is None:
        return ""
    try:
        return f"{float(value):.3f}s"
    except (TypeError, ValueError):
        return f"{value}s"


def _sanitize_text(value: str) -> str:
    return value.encode("utf-8", "replace").decode("utf-8")


def _configure_utf8_stdio() -> None:
    for stream_name in ("stdout", "stderr"):
        stream = getattr(sys, stream_name)
        reconfigure = getattr(stream, "reconfigure", None)
        if callable(reconfigure):
            reconfigure(encoding="utf-8", errors="replace")


if __name__ == "__main__":
    raise SystemExit(main())
