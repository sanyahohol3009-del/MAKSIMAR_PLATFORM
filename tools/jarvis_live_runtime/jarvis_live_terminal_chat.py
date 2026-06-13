from __future__ import annotations

import json
import sys
from pathlib import Path
from typing import Any

import httpx


PROJECT_ROOT = Path(__file__).resolve().parents[2]
API_LOG_FILE = PROJECT_ROOT / ".runtime" / "jarvis_live" / "api.log"
API_BASE_URL = "http://127.0.0.1:8765"
COMMAND_URL = f"{API_BASE_URL}/jarvis-live/command"
STREAM_URL = f"{API_BASE_URL}/jarvis-live/chat/stream"
HEALTH_URL = f"{API_BASE_URL}/jarvis-live/health"
STATUS_URL = f"{API_BASE_URL}/jarvis-live/status"
MODELS_URL = f"{API_BASE_URL}/jarvis-live/models"
TOOLS_URL = f"{API_BASE_URL}/jarvis-live/tools"
SESSION_ID = "terminal_chat"
HEALTH_TIMEOUT_SECONDS = 10
COMMAND_TIMEOUT_SECONDS = 240
_LAST_API_ERROR = ""
_THINKING_ACTIVE = False
_TRACE_ENABLED = False
_DEBUG_ENABLED = False
PROJECT_COMMANDS = (
    "/project",
    "/project status",
    "/project tree",
    "/project files",
    "/project dirty",
    "/project search",
    "/project file",
    "/project outline",
    "/project imports",
    "/project tests",
    "/project roadmap",
    "/project models",
    "/project safety",
)


def main() -> int:
    _configure_utf8_stdio()
    print("JARVIS terminal ready")
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
            print()
            continue
        except Exception as exc:
            _print_terminal_runtime_error(user_text, exc)
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
    if user_text == "/memory recent":
        _print_memory_recent()
        return False
    if user_text == "/memory style":
        _print_memory_style()
        return False
    if user_text == "/memory sources":
        _print_memory_sources()
        return False
    if user_text == "/models":
        _print_models()
        return False
    if user_text == "/tools":
        _print_tools()
        return False
    if user_text == "/debug ollama":
        _print_models(verbose=True)
        return False
    if user_text == "/project" or user_text.startswith("/project "):
        _print_stream_response(user_text)
        return False
    if user_text == "/logs":
        _print_logs()
        return False
    if user_text == "/trace on":
        _set_trace(True)
        return False
    if user_text == "/trace off":
        _set_trace(False)
        return False
    if user_text == "/debug on":
        _set_debug(True)
        return False
    if user_text == "/debug off":
        _set_debug(False)
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
    error_kind = response.get("error_kind") or result.get("error_kind") or ""
    if error_kind:
        _print_stream_error(
            {
                "error_kind": error_kind,
                "error_message": response.get("error_message") or result.get("error_message") or "",
                "selected_model_id": response.get("selected_model_id") or result.get("selected_model_id", ""),
                "ollama_model_used": response.get("ollama_model_used") or result.get("ollama_model_used", ""),
            }
        )
    if _trace_enabled():
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
    try:
        if _stream_json_lines(STREAM_URL, payload) is None:
            _print_command_unavailable()
    except Exception as exc:
        _print_terminal_runtime_error(text, exc)


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
    payload = _get_json(STATUS_URL) or _get_json(HEALTH_URL)
    if payload is None:
        _print_api_not_running()
        return
    session = payload.get("session") if isinstance(payload.get("session"), dict) else payload
    print(f"recent_turn_count={session.get('recent_turn_count', payload.get('recent_turn_count', 0))}")
    print(f"rolling_summary={session.get('rolling_summary', '')}")
    print(f"active_topics={_csv(session.get('active_topics', ())) }")
    print(f"session_memory_path={session.get('session_memory_path', payload.get('session_memory_path', ''))}")
    print(f"local_chat_memory_path={session.get('local_chat_memory_path', payload.get('local_chat_memory_path', ''))}")


def _print_memory_recent() -> None:
    payload = _get_json(STATUS_URL) or _get_json(HEALTH_URL)
    if payload is None:
        _print_api_not_running()
        return
    session = payload.get("session") if isinstance(payload.get("session"), dict) else payload
    path = Path(str(session.get("session_memory_path", "")))
    if not path.exists():
        print("recent_turns=none")
        return
    try:
        state = json.loads(path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError):
        print("recent_turns=unavailable")
        return
    turns = state.get("recent_turns", [])
    if not isinstance(turns, list) or not turns:
        print("recent_turns=none")
        return
    for turn in turns[-6:]:
        if isinstance(turn, dict):
            print(f"{turn.get('role', '')}: {turn.get('text', '')}")


def _print_memory_style() -> None:
    payload = _get_json(STATUS_URL) or _get_json(HEALTH_URL)
    if payload is None:
        _print_api_not_running()
        return
    session = payload.get("session") if isinstance(payload.get("session"), dict) else payload
    profile = session.get("stable_style_profile", {})
    if not isinstance(profile, dict):
        print("stable_style_profile=unavailable")
        return
    for key, value in profile.items():
        print(f"{key}={value}")


def _print_memory_sources() -> None:
    payload = _get_json(HEALTH_URL)
    if payload is None:
        _print_api_not_running()
        return
    print(f"active_retrieval_surfaces={_csv(payload.get('active_retrieval_surfaces', ())) }")
    print(f"sandbox_only_memory_surfaces={_csv(payload.get('sandbox_only_memory_surfaces', ())) }")
    print(f"disabled_memory_surfaces={_csv(payload.get('disabled_memory_surfaces', ())) }")
    print(f"mempalace_status={payload.get('mempalace_status', '')}")


def _print_models(verbose: bool = False) -> None:
    payload = _get_json(MODELS_URL) or _get_json(HEALTH_URL)
    if payload is None:
        _print_api_not_running()
        return
    models = payload.get("models") if isinstance(payload.get("models"), dict) else payload
    print(f"ollama_version={models.get('ollama_version', 'unavailable')}")
    print(f"ollama_tags={models.get('ollama_tags', 'unavailable')}")
    print(f"ollama_ps={models.get('ollama_ps', 'unavailable')}")
    print(f"ollama_show_primary_model={models.get('ollama_show_primary_model', 'unavailable')}")
    print(f"ollama_is_local_model_engine={models.get('ollama_is_local_model_engine', 'true')}")
    print(f"pc_control_allowed={str(bool(models.get('pc_control_allowed', False))).lower()}")
    print(
        "canonical_memory_write_allowed="
        f"{str(bool(payload.get('canonical_memory_write_allowed', False))).lower()}"
    )
    if verbose:
        print("debug_mode=ollama")
        print(f"api_log={API_LOG_FILE}")


def _print_tools() -> None:
    payload = _get_json(TOOLS_URL) or _get_json(STATUS_URL) or _get_json(HEALTH_URL)
    if payload is None:
        _print_api_not_running()
        return
    tools = payload.get("tools") if isinstance(payload.get("tools"), dict) else payload
    print(f"read_tools={_csv(tools.get('read_tools', ())) }")
    print(f"proposal_tools={_csv(tools.get('proposal_tools', ())) }")
    print(f"memory_surfaces={_csv(tools.get('memory_surfaces', ())) }")
    print(f"active_retrieval_surfaces={_csv(tools.get('active_retrieval_surfaces', ())) }")
    print(f"execution_allowed={str(bool(tools.get('execution_allowed', False))).lower()}")
    print(f"approval_required_for_actions={str(bool(tools.get('approval_required_for_actions', True))).lower()}")
    print(f"pc_control_allowed={str(bool(tools.get('pc_control_allowed', False))).lower()}")


def _print_logs() -> None:
    print(f"api_log={API_LOG_FILE}")


def _set_trace(enabled: bool) -> None:
    global _TRACE_ENABLED
    _TRACE_ENABLED = enabled
    print(f"trace={str(enabled).lower()}")


def _set_debug(enabled: bool) -> None:
    global _DEBUG_ENABLED
    _DEBUG_ENABLED = enabled
    print(f"debug={str(enabled).lower()}")


def _trace_enabled() -> bool:
    return _TRACE_ENABLED or _DEBUG_ENABLED


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
    timeout = httpx.Timeout(COMMAND_TIMEOUT_SECONDS, connect=min(10.0, COMMAND_TIMEOUT_SECONDS))
    try:
        with httpx.Client(timeout=timeout) as client:
            response = client.post(url, json=payload)
            response.raise_for_status()
            payload_json = response.json()
            return payload_json if isinstance(payload_json, dict) else None
    except httpx.HTTPStatusError as exc:
        _set_last_api_error(f"http_error status={exc.response.status_code} url={url}")
        return None
    except httpx.TimeoutException:
        _set_last_api_error(f"timeout url={url}")
        return None
    except httpx.RequestError as exc:
        _set_last_api_error(_describe_httpx_error(exc, url))
        return None
    except ValueError:
        _set_last_api_error(f"invalid_json url={url}")
        return None


def _get_json(url: str) -> dict[str, Any] | None:
    global _LAST_API_ERROR
    _LAST_API_ERROR = ""
    try:
        timeout = httpx.Timeout(HEALTH_TIMEOUT_SECONDS, connect=min(10.0, HEALTH_TIMEOUT_SECONDS))
        with httpx.Client(timeout=timeout) as client:
            response = client.get(url)
            response.raise_for_status()
            payload = response.json()
    except httpx.HTTPStatusError as exc:
        _LAST_API_ERROR = f"http_error status={exc.response.status_code} url={url}"
        return None
    except httpx.TimeoutException:
        _LAST_API_ERROR = f"timeout url={url}"
        return None
    except httpx.RequestError as exc:
        _LAST_API_ERROR = _describe_httpx_error(exc, url)
        return None
    except ValueError:
        _LAST_API_ERROR = f"invalid_json url={url}"
        return None
    return payload if isinstance(payload, dict) else None


def _stream_json_lines(url: str, payload: dict[str, Any]) -> dict[str, Any] | None:
    global _LAST_API_ERROR, _THINKING_ACTIVE
    _LAST_API_ERROR = ""
    _THINKING_ACTIVE = False
    done_event: dict[str, Any] = {}
    try:
        timeout = httpx.Timeout(COMMAND_TIMEOUT_SECONDS, connect=min(10.0, COMMAND_TIMEOUT_SECONDS))
        with httpx.Client(timeout=timeout) as client:
            with client.stream("POST", url, json=payload) as response:
                response.raise_for_status()
                for line in response.iter_lines():
                    if not line:
                        continue
                    event = _print_stream_event(line)
                    if isinstance(event, dict) and str(event.get("event") or event.get("type") or "") == "done":
                        done_event = event
    except httpx.HTTPStatusError as exc:
        _LAST_API_ERROR = f"http_error status={exc.response.status_code} url={url}"
        return None
    except httpx.TimeoutException:
        _LAST_API_ERROR = f"timeout url={url}"
        return None
    except httpx.RequestError as exc:
        _LAST_API_ERROR = _describe_httpx_error(exc, url)
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
        if _trace_enabled():
            _print_stream_start_trace(event)
        return event
    if event_type == "route_selected":
        if _trace_enabled():
            _print_stream_route_trace(event)
        return event
    if event_type == "operator_trace":
        _print_operator_trace_event(event)
        return event
    if event_type == "thinking":
        _print_thinking_event(event)
        return event
    if event_type == "error":
        _print_stream_error(event)
        return event
    chunk = event.get("chunk") or event.get("text") or event.get("llm_response") or ""
    if chunk:
        _finish_thinking_if_active()
        print(str(chunk), end="", flush=True)
        return event
    if event_type and event_type != "done":
        if _trace_enabled():
            print(f"\nstream_event={event_type}")
    return event


def _print_stream_metadata(event: dict[str, Any]) -> None:
    _finish_thinking_if_active()
    print()
    if event.get("error_kind"):
        _print_stream_error(event)
    if _trace_enabled():
        print(
            "[trace] "
            f"first_token={_seconds(event.get('first_chunk_elapsed_seconds', ''))} "
            f"ollama={_seconds(event.get('ollama_elapsed_seconds', ''))} "
            f"total={_seconds(event.get('total_elapsed_seconds', ''))} "
            f"chunks={event.get('stream_chunk_count', 0)}"
        )
        print(
            "[trace] "
            f"endpoint={event.get('ollama_endpoint', '')} "
            f"primary={event.get('primary_endpoint', '')} "
            f"fallback={event.get('fallback_endpoint', '')} "
            f"fallback_used={str(bool(event.get('ollama_endpoint_fallback_used', False))).lower()} "
            f"think_mode={event.get('think_mode', '')} "
            f"num_predict={event.get('ollama_num_predict', '')} "
            f"temperature={event.get('ollama_temperature', '')}"
        )
        if event.get("intent_family"):
            print(
                "[trace] "
                f"intent_family={event.get('intent_family', '')} "
                f"selected_tools={_csv(event.get('selected_tools', ())) } "
                f"read_only={str(bool(event.get('read_only', True))).lower()} "
                f"execution_allowed={str(bool(event.get('execution_allowed', False))).lower()} "
                f"evidence_count={event.get('evidence_count', 0)} "
                f"grounded_answer={str(bool(event.get('grounded_answer', False))).lower()} "
                f"ollama_called={str(bool(event.get('ollama_called', False))).lower()}"
            )
        if event.get("primary_error_kind"):
            print(f"[trace] primary_error_kind={event.get('primary_error_kind', '')}")
        if event.get("tool_call_detected"):
            print(
                "[trace] "
                f"tool_call_detected={str(bool(event.get('tool_call_detected', False))).lower()} "
                f"tool_call_count={event.get('tool_call_count', 0)} "
                f"execution_allowed={str(bool(event.get('execution_allowed', False))).lower()} "
                f"approval_required={str(bool(event.get('approval_required', False))).lower()} "
                f"proposal_only={str(bool(event.get('proposal_only', False))).lower()}"
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


def _print_stream_error(event: dict[str, Any]) -> None:
    error_kind = str(event.get("error_kind") or "ollama_stream_error")
    model_id = str(
        event.get("ollama_model_used")
        or event.get("selected_model_id")
        or ""
    )
    elapsed = event.get("ollama_elapsed_seconds", "")
    if error_kind == "ollama_empty_response":
        print(f"[error] ollama_empty_response model={model_id} elapsed={_seconds(elapsed)}")
        return
    if error_kind == "ollama_thinking_without_final_response":
        print(f"[error] ollama_thinking_without_final_response model={model_id} elapsed={_seconds(elapsed)}")
        print("Модель показала thinking, но не дала финальный ответ. Повтори короче или отключи thinking для FAST.")
        return
    message = str(event.get("error_message") or "")
    print(f"[error] {error_kind} model={model_id} {message}".rstrip())


def _print_operator_trace_event(event: dict[str, Any]) -> None:
    print(
        "[work] "
        f"intent={event.get('intent_family', '')} "
        f"tools={_csv(event.get('selected_tools', ())) } "
        f"read_only={str(bool(event.get('read_only', True))).lower()} "
        f"execution_allowed={str(bool(event.get('execution_allowed', False))).lower()}"
    )


def _print_thinking_event(event: dict[str, Any]) -> None:
    global _THINKING_ACTIVE
    text = str(event.get("text") or "")
    if not text:
        return
    if not _THINKING_ACTIVE:
        print("Thinking...")
        _THINKING_ACTIVE = True
    print(text, end="", flush=True)


def _finish_thinking_if_active() -> None:
    global _THINKING_ACTIVE
    if not _THINKING_ACTIVE:
        return
    print("\n...done thinking.")
    _THINKING_ACTIVE = False


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
        f"surfaces={_csv(event.get('retrieval_surfaces_used', ())) } "
        f"local_memory={event.get('local_chat_memory_snippet_count', 0)} "
        f"endpoint={event.get('ollama_endpoint', '')} "
        f"think_mode={event.get('think_mode', '')} "
        f"fallback_used={str(bool(event.get('ollama_endpoint_fallback_used', False))).lower()} "
        f"num_predict={event.get('ollama_num_predict', '')}"
    )
    if event.get("intent_family"):
        print(
            "[trace] "
            f"intent_family={event.get('intent_family', '')} "
            f"selected_tools={_csv(event.get('selected_tools', ())) } "
            f"read_only={str(bool(event.get('read_only', True))).lower()} "
            f"execution_allowed={str(bool(event.get('execution_allowed', False))).lower()} "
            f"evidence_required={str(bool(event.get('evidence_required', False))).lower()}"
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


def _print_terminal_runtime_error(user_text: str, exc: Exception) -> None:
    print(f"[error] terminal_runtime_error command={user_text!r} type={exc.__class__.__name__}: {exc}")
    if _LAST_API_ERROR:
        print(f"api_error={_LAST_API_ERROR}")
    print(f"api_log={API_LOG_FILE}")


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


def _describe_httpx_error(exc: httpx.RequestError, url: str) -> str:
    if isinstance(exc, httpx.ConnectError):
        return f"connection_refused url={url}"
    if isinstance(exc, httpx.ReadTimeout):
        return f"timeout url={url}"
    reason = getattr(exc, "args", (exc,))
    detail = reason[0] if reason else exc
    return f"url_error {detail.__class__.__name__}: {detail} url={url}"


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
