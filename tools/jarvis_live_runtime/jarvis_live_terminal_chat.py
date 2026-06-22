#!/usr/bin/env python3
from __future__ import annotations

import atexit
import json
import re
import shutil
import subprocess
import sys
import time
from pathlib import Path
from typing import Any

import httpx

try:
    import readline
except ImportError:
    readline = None


PROJECT_ROOT = Path(__file__).resolve().parents[2]
API_LOG_FILE = PROJECT_ROOT / ".runtime" / "jarvis_live" / "api.log"
HISTORY_FILE = PROJECT_ROOT / ".runtime" / "jarvis_live" / ".chat_history"

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
LOCAL_TEST_TIMEOUT_SECONDS = 900
LOCAL_READ_TIMEOUT_SECONDS = 60

_LAST_API_ERROR = ""
_THINKING_ACTIVE = False
_TRACE_ENABLED = False
_DEBUG_ENABLED = False
_CHAT_RENDER_MODE = "detailed"  # compact | detailed | debug

_IN_CODE_BLOCK = False
_CODE_BUFFER = ""
_LAST_ROUTE_EVENT: dict[str, Any] = {}
_LAST_OPERATOR_EVENT: dict[str, Any] = {}

ANSI = {
    "reset": "\033[0m",
    "bold": "\033[1m",
    "dim": "\033[2m",
    "red": "\033[31m",
    "green": "\033[32m",
    "yellow": "\033[33m",
    "blue": "\033[34m",
    "magenta": "\033[35m",
    "cyan": "\033[36m",
    "white": "\033[37m",
    "gray": "\033[90m",
    "bg_red": "\033[41m",
}

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
    _setup_readline()
    print(_color("green", "JARVIS terminal ready"))
    print(_color("bold", _color("cyan", "==================================================")))
    print(_color("bold", _color("cyan", "  🤖 MAKSIMAR / JARVIS TERMINAL")))
    print(_color("bold", _color("cyan", "==================================================")))
    print(_color("dim", "  /m — вставка логов/кода · /help — команды · /mode debug — полный trace"))
    while True:
        user_text = _get_user_input()
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
            print(_color("dim", "\nОтключение терминала JARVIS."))
            return 0


def _dispatch_user_text(user_text: str) -> bool:
    aliases = {
        "st": "/status",
        "g": "/git",
        "m": "/memory",
        "p": "/project",
        "t": "/tools",
        "mdl": "/models",
        "ag": "/agents",
        "sk": "/skills",
        "ts": "/tests",
        "h": "/help",
        "df": "/diff",
    }
    user_text = aliases.get(user_text, user_text)

    if user_text == "/exit":
        return True
    if user_text == "/ping":
        _print_ping()
        return False
    if user_text == "/status":
        _print_full_status()
        return False
    if user_text == "/git":
        _print_git_status()
        return False
    if user_text == "/diff":
        _print_diff()
        return False
    if user_text == "/tests":
        _print_tests(("pytest", "-q", "--tb=short", "--maxfail=20", "tests/"))
        return False
    if user_text.startswith("/tests "):
        _handle_tests_command(user_text[len("/tests "):].strip())
        return False
    if user_text.startswith("/show "):
        _show_file(user_text[len("/show "):].strip())
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
    if user_text == "/agents":
        _print_agents()
        return False
    if user_text == "/skills":
        _print_skills()
        return False
    if user_text == "/debug ollama":
        _print_models(verbose=True)
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
    if user_text in {"/режим кратко", "/mode compact"}:
        _set_chat_mode("compact")
        return False
    if user_text in {"/режим подробно", "/mode detailed"}:
        _set_chat_mode("detailed")
        return False
    if user_text in {"/режим debug", "/mode debug"}:
        _set_chat_mode("debug")
        return False
    if user_text in {"/помощь", "/help"}:
        _print_chat_help()
        return False
    if user_text.startswith("/command "):
        _print_command_response(user_text[len("/command "):].strip())
        return False
    if user_text.startswith("/stream "):
        _run_jarvis_turn(user_text[len("/stream "):].strip())
        return False
    if user_text == "/project" or user_text.startswith("/project "):
        _run_jarvis_turn(user_text)
        return False

    _run_jarvis_turn(user_text)
    return False


def _run_jarvis_turn(text: str) -> None:
    print(_color("blue", "\n╭─[") + _color("bold", " JARVIS ") + _color("blue", "]─"))
    print(_color("blue", "│"), end=" ")
    _print_stream_response(text)
    print(_color("blue", "\n╰" + "─" * 64))


def _get_user_input() -> str:
    try:
        print()
        print(_color("green", "╭─[") + _color("bold", " АЛЕКСАНДР ") + _color("green", "]─"))
        line = input(_color("green", "╰─► ")).strip()
        if line in {"/m", "/multi"}:
            print(_color("yellow", "  [ Режим вставки. Введи '/end' отдельной строкой ]"))
            pasted: list[str] = []
            while True:
                part = input(_color("dim", "  │ "))
                if part.strip() == "/end":
                    break
                pasted.append(part)
            return "\n".join(pasted).strip()
        return line
    except (EOFError, KeyboardInterrupt):
        return "/exit"


def _setup_readline() -> None:
    if readline is None:
        return
    HISTORY_FILE.parent.mkdir(parents=True, exist_ok=True)
    try:
        readline.read_history_file(str(HISTORY_FILE))
    except FileNotFoundError:
        pass
    atexit.register(readline.write_history_file, str(HISTORY_FILE))


def _color(name: str, text: str) -> str:
    if not sys.stdout.isatty():
        return str(text)
    return f"{ANSI.get(name, '')}{text}{ANSI['reset']}"


def _term_width() -> int:
    return max(70, min(120, shutil.get_terminal_size((100, 24)).columns - 2))


def _box(title: str, lines: tuple[str, ...] | list[str], color: str = "cyan") -> None:
    clean_lines = [str(line) for line in lines if str(line).strip()]
    width = _term_width()
    print(_color(color, f"\n╭─ {title} " + "─" * max(0, width - len(title) - 5) + "╮"))
    for line in clean_lines:
        for part in _wrap_line(line, width - 4):
            print(_color(color, "│ ") + part.ljust(width - 2) + _color(color, "│"))
    print(_color(color, "╰" + "─" * width + "╯"))


def _wrap_line(text: str, width: int) -> tuple[str, ...]:
    value = str(text)
    if len(value) <= width:
        return (value,)
    parts: list[str] = []
    current = value
    while len(current) > width:
        cut = current.rfind(" ", 0, width)
        if cut <= 0:
            cut = width
        parts.append(current[:cut].rstrip())
        current = current[cut:].lstrip()
    if current:
        parts.append(current)
    return tuple(parts)


def _chat_mode() -> str:
    return _CHAT_RENDER_MODE


def _set_chat_mode(mode: str) -> None:
    global _CHAT_RENDER_MODE, _TRACE_ENABLED, _DEBUG_ENABLED
    if mode not in {"compact", "detailed", "debug"}:
        print(_color("red", "Неизвестный режим. Доступно: compact, detailed, debug"))
        return
    _CHAT_RENDER_MODE = mode
    _TRACE_ENABLED = mode == "debug"
    _DEBUG_ENABLED = mode == "debug"
    print(_color("green", f"Режим чата: {mode}"))


def _print_full_status() -> None:
    _print_git_status()
    print()
    _print_status()


def _print_git_status() -> None:
    _box("GIT STATUS", ("Команда: git status -sb",), "cyan")
    _run_local_command(("git", "status", "-sb"), timeout=LOCAL_READ_TIMEOUT_SECONDS)

    _box("LAST COMMITS", ("Команда: git log --oneline -5",), "cyan")
    _run_local_command(("git", "log", "--oneline", "-5"), timeout=LOCAL_READ_TIMEOUT_SECONDS)


def _print_diff() -> None:
    _box("GIT DIFF", ("Команда: git diff --stat",), "cyan")
    stat_result = _run_local_command(("git", "diff", "--stat"), timeout=LOCAL_READ_TIMEOUT_SECONDS)
    if stat_result.returncode == 0 and not stat_result.stdout.strip():
        print(_color("green", "Нет изменений в tracked files."))

    _box("FULL DIFF", ("Команда: git diff -U5 --color=always",), "cyan")
    _run_local_command(("git", "diff", "-U5", "--color=always"), timeout=LOCAL_READ_TIMEOUT_SECONDS)


def _handle_tests_command(argument: str) -> None:
    if not argument:
        _print_tests(("pytest", "-q", "--tb=short", "--maxfail=20", "tests/"))
        return
    if argument == "all":
        _print_tests(("pytest", "-q", "--tb=short", "--maxfail=20", "tests/"))
        return
    if argument == "jarvis":
        _print_tests(("pytest", "-q", "--tb=short", "--maxfail=20", "tests/jarvis_live_runtime"))
        return
    if argument.startswith("tests/"):
        _print_tests(("pytest", "-q", "--tb=short", "--maxfail=20", argument))
        return
    print(_color("red", "Формат: /tests, /tests all, /tests jarvis, /tests tests/<path>"))


def _print_tests(command: tuple[str, ...]) -> None:
    _box("PYTEST", (f"Команда: {' '.join(command)}", f"CWD: {PROJECT_ROOT}"), "cyan")
    start = time.monotonic()
    result = _run_local_command(command, timeout=LOCAL_TEST_TIMEOUT_SECONDS, print_header=False)
    elapsed = time.monotonic() - start

    summary = _extract_pytest_summary(result.stdout + "\n" + result.stderr)
    color = "green" if result.returncode == 0 else "red"
    _box(
        "PYTEST SUMMARY",
        (
            f"returncode: {result.returncode}",
            f"elapsed: {elapsed:.2f}s",
            f"summary: {summary or 'summary не найден'}",
        ),
        color,
    )


def _run_local_command(
    command: tuple[str, ...],
    *,
    timeout: int,
    print_header: bool = True,
) -> subprocess.CompletedProcess[str]:
    if print_header:
        print(_color("dim", f"$ {' '.join(command)}"))
    try:
        result = subprocess.run(
            list(command),
            cwd=str(PROJECT_ROOT),
            capture_output=True,
            text=True,
            timeout=timeout,
        )
    except subprocess.TimeoutExpired as exc:
        stdout = exc.stdout if isinstance(exc.stdout, str) else ""
        stderr = exc.stderr if isinstance(exc.stderr, str) else ""
        result = subprocess.CompletedProcess(list(command), 124, stdout, stderr + f"\n[TIMEOUT after {timeout}s]")
    except FileNotFoundError as exc:
        result = subprocess.CompletedProcess(list(command), 127, "", str(exc))

    if result.stdout:
        print(result.stdout.rstrip())
    if result.stderr:
        print(_color("yellow", result.stderr.rstrip()))
    print(_color("dim", f"[exit={result.returncode}]"))
    return result


def _show_file(file_path: str) -> None:
    rel = file_path.strip()
    if not rel:
        print(_color("red", "Формат: /show path/to/file.py"))
        return
    root = PROJECT_ROOT.resolve()
    target = (PROJECT_ROOT / rel).resolve()
    try:
        # БАГФИКС #5: startswith(str(root)) пропускал соседние папки вида
        # "MAKSIMAR_PLATFORM_secrets" из-за совпадения префикса без учёта
        # границы каталога. relative_to() проверяет это корректно.
        target.relative_to(root)
    except ValueError:
        print(_color("red", f"Запрещён путь вне проекта: {rel}"))
        return
    if not target.exists() or not target.is_file():
        print(_color("red", f"Файл не найден: {rel}"))
        return
    lines = target.read_text(encoding="utf-8", errors="replace").splitlines()
    _box("SHOW FILE", (f"Файл: {rel}", f"Строк: {len(lines)}"), "cyan")
    for index, line in enumerate(lines, 1):
        print(f"{index:5d}  {line}")


def _print_command_response(text: str) -> None:
    payload = {"text": _sanitize_text(text), "session_id": SESSION_ID, "pc_control_allowed": False}
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
        _print_response_trace(response | result)


def _print_status() -> None:
    payload = _get_json(STATUS_URL) or _get_json(HEALTH_URL)
    if payload is None:
        _print_api_not_running()
        return
    lines = (
        f"api_ok={str(bool(payload.get('ok', False))).lower()}",
        f"default_model={payload.get('default_model', '')}",
        f"primary_conversation_model={payload.get('primary_conversation_model', '')}",
        f"memory_federation_available={str(bool(payload.get('memory_federation_available', False))).lower()}",
        f"pc_control_allowed={str(bool(payload.get('pc_control_allowed', False))).lower()}",
        "canonical_memory_write_allowed="
        f"{str(bool(payload.get('canonical_memory_write_allowed', False))).lower()}",
    )
    _box("API STATUS", lines, "cyan")


def _print_memory() -> None:
    payload = _get_json(STATUS_URL) or _get_json(HEALTH_URL)
    if payload is None:
        _print_api_not_running()
        return
    session = payload.get("session") if isinstance(payload.get("session"), dict) else payload
    _box(
        "MEMORY",
        (
            f"recent_turn_count={session.get('recent_turn_count', payload.get('recent_turn_count', 0))}",
            f"rolling_summary={session.get('rolling_summary', '')}",
            f"active_topics={_csv(session.get('active_topics', ())) }",
            f"session_memory_path={session.get('session_memory_path', payload.get('session_memory_path', ''))}",
            f"local_chat_memory_path={session.get('local_chat_memory_path', payload.get('local_chat_memory_path', ''))}",
        ),
        "cyan",
    )


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
    _box("STYLE", tuple(f"{key}={value}" for key, value in profile.items()), "cyan")


def _print_memory_sources() -> None:
    payload = _get_json(HEALTH_URL)
    if payload is None:
        _print_api_not_running()
        return
    _box(
        "MEMORY SOURCES",
        (
            f"active_retrieval_surfaces={_csv(payload.get('active_retrieval_surfaces', ())) }",
            f"sandbox_only_memory_surfaces={_csv(payload.get('sandbox_only_memory_surfaces', ())) }",
            f"disabled_memory_surfaces={_csv(payload.get('disabled_memory_surfaces', ())) }",
            f"mempalace_status={payload.get('mempalace_status', '')}",
        ),
        "cyan",
    )


def _print_models(verbose: bool = False) -> None:
    payload = _get_json(MODELS_URL) or _get_json(HEALTH_URL)
    if payload is None:
        _print_api_not_running()
        return
    models = payload.get("models") if isinstance(payload.get("models"), dict) else payload
    _box(
        "MODELS",
        (
            f"ollama_version={models.get('ollama_version', 'unavailable')}",
            f"ollama_tags={models.get('ollama_tags', 'unavailable')}",
            f"ollama_ps={models.get('ollama_ps', 'unavailable')}",
            f"ollama_show_primary_model={models.get('ollama_show_primary_model', 'unavailable')}",
            f"ollama_is_local_model_engine={models.get('ollama_is_local_model_engine', 'true')}",
            f"pc_control_allowed={str(bool(models.get('pc_control_allowed', False))).lower()}",
        ),
        "cyan",
    )
    if verbose:
        print("debug_mode=ollama")
        print(_color("dim", f"api_log={API_LOG_FILE}"))


def _print_tools() -> None:
    payload = _get_json(TOOLS_URL) or _get_json(STATUS_URL) or _get_json(HEALTH_URL)
    if payload is None:
        _print_api_not_running()
        return
    tools = payload.get("tools") if isinstance(payload.get("tools"), dict) else payload
    read_tools = _as_tuple(tools.get("read_tools", ()))
    proposal_tools = _as_tuple(tools.get("proposal_tools", ()))
    memory_surfaces = _as_tuple(tools.get("memory_surfaces", ()))
    active_surfaces = _as_tuple(tools.get("active_retrieval_surfaces", ()))

    _box(
        "TOOLS",
        (
            f"read_tools={_csv(read_tools)}",
            f"proposal_tools={_csv(proposal_tools)}",
            f"memory_surfaces={_csv(memory_surfaces)}",
            f"active_retrieval_surfaces={_csv(active_surfaces)}",
            f"execution_allowed={str(bool(tools.get('execution_allowed', False))).lower()}",
            f"approval_required_for_actions={str(bool(tools.get('approval_required_for_actions', True))).lower()}",
            f"pc_control_allowed={str(bool(tools.get('pc_control_allowed', False))).lower()}",
        ),
        "cyan",
    )


def _print_agents() -> None:
    payload = _get_json(TOOLS_URL) or _get_json(STATUS_URL) or _get_json(HEALTH_URL) or {}
    root = payload.get("tools") if isinstance(payload.get("tools"), dict) else payload
    agents = (
        root.get("agents")
        or root.get("agent_roles")
        or root.get("available_agents")
        or root.get("selected_agent_roles")
        or ()
    )
    agents_tuple = _as_tuple(agents)
    if not agents_tuple:
        _box(
            "AGENTS",
            (
                "Runtime API пока не отдаёт отдельный каталог agents.",
                "Это не заглушка: терминал не рисует фейковых агентов.",
                f"Доступные ключи API: {_csv(sorted(root.keys())) if isinstance(root, dict) else 'unknown'}",
            ),
            "yellow",
        )
        return
    _box("AGENTS", tuple(str(item) for item in agents_tuple), "cyan")


def _print_skills() -> None:
    payload = _get_json(TOOLS_URL) or _get_json(STATUS_URL) or _get_json(HEALTH_URL) or {}
    root = payload.get("tools") if isinstance(payload.get("tools"), dict) else payload
    skills = root.get("skills") or root.get("skill_catalog") or root.get("available_skills") or ()
    skills_tuple = _as_tuple(skills)
    if not skills_tuple:
        read_tools = _as_tuple(root.get("read_tools", ())) if isinstance(root, dict) else ()
        proposal_tools = _as_tuple(root.get("proposal_tools", ())) if isinstance(root, dict) else ()
        memory_surfaces = _as_tuple(root.get("memory_surfaces", ())) if isinstance(root, dict) else ()
        _box(
            "SKILLS / RUNTIME SURFACES",
            (
                "Runtime API пока не отдаёт отдельный каталог skills.",
                "Показываю реальные tools/surfaces вместо фейкового списка.",
                f"read_tools={_csv(read_tools)}",
                f"proposal_tools={_csv(proposal_tools)}",
                f"memory_surfaces={_csv(memory_surfaces)}",
            ),
            "yellow",
        )
        return
    _box("SKILLS", tuple(str(item) for item in skills_tuple), "cyan")


def _print_logs() -> None:
    print(f"api_log={API_LOG_FILE}")


def _set_trace(enabled: bool) -> None:
    global _TRACE_ENABLED
    _TRACE_ENABLED = enabled
    print(f"trace={str(enabled).lower()}")


def _set_debug(enabled: bool) -> None:
    global _DEBUG_ENABLED, _TRACE_ENABLED, _CHAT_RENDER_MODE
    _DEBUG_ENABLED = enabled
    _TRACE_ENABLED = enabled
    if enabled:
        _CHAT_RENDER_MODE = "debug"
    elif _CHAT_RENDER_MODE == "debug":
        # БАГФИКС #1: раньше /debug off не возвращал режим чата из "debug",
        # из-за чего полный trace и thinking-дамп продолжали показываться.
        _CHAT_RENDER_MODE = "detailed"
    print(f"debug={str(enabled).lower()}")


def _trace_enabled() -> bool:
    return _TRACE_ENABLED or _DEBUG_ENABLED


def _print_ping(startup: bool = False) -> None:
    payload = _get_json(HEALTH_URL)
    prefix = "startup_ping" if startup else "ping"
    if payload is None:
        print(f"{prefix}=failed")
        _print_api_not_running()
        return
    print(f"{prefix}=ok")
    print(f"default_model={payload.get('default_model', '')}")
    print(f"pc_control_allowed={str(bool(payload.get('pc_control_allowed', False))).lower()}")
    print(
        "canonical_memory_write_allowed="
        f"{str(bool(payload.get('canonical_memory_write_allowed', False))).lower()}"
    )


def _print_chat_help() -> None:
    _box(
        "COMMANDS",
        (
            "/m, /multi                 многострочная вставка; завершение: /end",
            "/status, st                git status + API status",
            "/git, g                    git status -sb + git log -5",
            "/diff, df                  git diff --stat + полный git diff",
            "/tests, ts                 полный pytest tests/",
            "/tests all                 полный pytest tests/",
            "/tests jarvis              pytest tests/jarvis_live_runtime",
            "/tests tests/<path>        pytest по конкретному пути",
            "/show <file>               показать файл с номерами строк",
            "/tools, t                  реальные tools из API",
            "/agents, ag                реальные agents из API, если endpoint отдаёт",
            "/skills, sk                реальные skills или runtime surfaces",
            "/models, mdl               модели из API/Ollama status",
            "/memory                    память сессии",
            "/memory recent             последние реплики",
            "/memory style              стиль",
            "/memory sources            поверхности памяти",
            "/mode compact              короткий режим",
            "/mode detailed             подробный режим",
            "/mode debug                полный trace/work metadata",
            "/trace on|off              trace",
            "/debug on|off              debug",
            "/command <text>            non-stream command route",
            "/stream <text>             stream route",
            "/project ...               " + ", ".join(PROJECT_COMMANDS[1:]),
            "/exit                      выход",
        ),
        "cyan",
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


def _print_stream_response(text: str) -> None:
    global _IN_CODE_BLOCK, _CODE_BUFFER, _LAST_ROUTE_EVENT, _LAST_OPERATOR_EVENT
    _IN_CODE_BLOCK = False
    _CODE_BUFFER = ""
    _LAST_ROUTE_EVENT = {}
    _LAST_OPERATOR_EVENT = {}
    if not text:
        print("stream_error=empty_text")
        return
    payload = {"text": _sanitize_text(text), "session_id": SESSION_ID, "pc_control_allowed": False}
    try:
        if _stream_json_lines(STREAM_URL, payload) is None:
            _print_command_unavailable()
    except Exception as exc:
        _print_terminal_runtime_error(text, exc)


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
    global _LAST_ROUTE_EVENT, _LAST_OPERATOR_EVENT
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
        _LAST_ROUTE_EVENT = dict(event)
        if _trace_enabled():
            _print_stream_route_trace(event)
        if _should_show_infra(event):
            _print_usage_table(event, label="выбрано")
        return event

    if event_type == "operator_trace":
        _LAST_OPERATOR_EVENT = dict(event)
        _print_operator_trace_event(event)
        return event

    if event_type in {"command_start", "command_output", "command_done", "test_start", "test_output", "test_result"}:
        _print_runtime_command_event(event)
        return event

    if event_type in {"file_patch", "file_change", "diff", "patch"}:
        _print_file_change_event(event)
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
        _render_chunk(str(chunk))
        return event

    if event_type and event_type != "done" and _trace_enabled():
        print(f"\nstream_event={event_type}")

    return event


def _should_show_infra(event: dict[str, Any]) -> bool:
    if _chat_mode() == "debug":
        return True
    intent = str(event.get("intent_family") or "")
    tools = _as_tuple(event.get("selected_tools", ()))
    if not intent or intent == "CONVERSATION":
        return False
    return bool(tools or intent)


def _print_usage_table(event: dict[str, Any], *, label: str) -> None:
    model = str(event.get("selected_model_id") or event.get("ollama_model_used") or "unknown")
    intent = str(event.get("intent_family") or "unknown")
    tools = _as_tuple(event.get("selected_tools", ()))
    agents = _as_tuple(
        event.get("selected_agent_roles")
        or event.get("selected_agent_role")
        or event.get("agent_roles")
        or ()
    )
    read_only = str(bool(event.get("read_only", True))).lower()
    execution_allowed = str(bool(event.get("execution_allowed", False))).lower()
    parts = [
        f"{label}",
        f"model={model}",
        f"intent={intent}",
        f"agents={_csv(agents) or 'нет данных'}",
        f"tools={_csv(tools) or 'нет'}",
        f"read_only={read_only}",
        f"execution_allowed={execution_allowed}",
    ]
    print(_color("dim", "  [infra] " + " | ".join(parts)))


def _print_operator_trace_event(event: dict[str, Any]) -> None:
    _print_usage_table(event, label="operator")
    if _trace_enabled():
        print(_color("dim", "  [raw_operator_trace] " + json.dumps(event, ensure_ascii=False, sort_keys=True)))
    print(_color("blue", "│"), end=" ")


def _print_runtime_command_event(event: dict[str, Any]) -> None:
    event_type = str(event.get("event") or event.get("type") or "")
    command = event.get("command") or event.get("cmd") or event.get("test_command") or ""
    output = event.get("output") or event.get("stdout") or event.get("stderr") or event.get("text") or ""
    returncode = event.get("returncode", event.get("exit_code", ""))

    if event_type in {"command_start", "test_start"}:
        _box("COMMAND START", (f"command={command}",), "cyan")
        return
    if event_type in {"command_output", "test_output"}:
        if output:
            print(str(output), end="" if str(output).endswith("\n") else "\n")
        return
    if event_type in {"command_done", "test_result"}:
        _box("COMMAND DONE", (f"command={command}", f"returncode={returncode}"), "green" if returncode in {0, "0", ""} else "red")
        if output:
            print(str(output))
        return


def _print_file_change_event(event: dict[str, Any]) -> None:
    file_path = str(event.get("path") or event.get("file") or event.get("file_path") or "unknown")
    _box("FILE CHANGE", (f"file={file_path}",), "magenta")
    diff_text = event.get("diff") or event.get("patch") or ""
    if diff_text:
        print(str(diff_text))
        return
    removed = event.get("removed_lines", ()) or event.get("deleted_lines", ()) or ()
    added = event.get("added_lines", ()) or ()
    for item in removed:
        print(_color("red", f"- {item}"))
    for item in added:
        print(_color("green", f"+ {item}"))


def _render_chunk(chunk: str) -> None:
    global _IN_CODE_BLOCK, _CODE_BUFFER
    _CODE_BUFFER += chunk
    if "```" not in _CODE_BUFFER:
        _print_text_fragment(_CODE_BUFFER)
        _CODE_BUFFER = ""
        return

    parts = _CODE_BUFFER.split("```")
    for index, part in enumerate(parts):
        if index > 0:
            _IN_CODE_BLOCK = not _IN_CODE_BLOCK
            if _IN_CODE_BLOCK:
                print(_color("yellow", "\n  ┌───[ CODE ]" + "─" * 48))
                print(_color("yellow", "  │ "), end="")
            else:
                print(_color("yellow", "\n  └" + "─" * 58) + "\n" + _color("blue", "│ "), end="")
        if part:
            _print_text_fragment(part)
    _CODE_BUFFER = ""


def _print_text_fragment(text: str) -> None:
    if _IN_CODE_BLOCK:
        print(_color("cyan", text.replace("\n", "\n  │ ")), end="", flush=True)
    else:
        print(text.replace("\n", "\n" + _color("blue", "│ ")), end="", flush=True)


def _print_stream_metadata(event: dict[str, Any]) -> None:
    _finish_thinking_if_active()
    print()

    if event.get("error_kind"):
        _print_stream_error(event)

    if _trace_enabled():
        _print_response_trace(event)
        return

    if _should_show_infra(event) and _chat_mode() == "detailed":
        model = event.get("selected_model_id", "")
        role = event.get("selected_model_role", "")
        snippets = event.get("retrieved_snippet_count", 0)
        surfaces = _csv(event.get("retrieval_surfaces_used", ()))
        print(_color("dim", f"  [result] model={model} role={role} snippets={snippets} surfaces={surfaces}"))


def _print_response_trace(event: dict[str, Any]) -> None:
    print(
        _color("dim", "[trace] ")
        + f"first_token={_seconds(event.get('first_chunk_elapsed_seconds', ''))} "
        f"ollama={_seconds(event.get('ollama_elapsed_seconds', ''))} "
        f"total={_seconds(event.get('total_elapsed_seconds', ''))} "
        f"chunks={event.get('stream_chunk_count', 0)}"
    )
    print(
        _color("dim", "[trace] ")
        + f"endpoint={event.get('ollama_endpoint', '')} "
        f"primary={event.get('primary_endpoint', '')} "
        f"fallback={event.get('fallback_endpoint', '')} "
        f"fallback_used={str(bool(event.get('ollama_endpoint_fallback_used', False))).lower()} "
        f"think_mode={event.get('think_mode', '')} "
        f"num_predict={event.get('ollama_num_predict', '')} "
        f"temperature={event.get('ollama_temperature', '')} "
        f"top_p={event.get('ollama_top_p', '')}"
    )
    if event.get("intent_family"):
        print(
            _color("dim", "[trace] ")
            + f"intent_family={event.get('intent_family', '')} "
            f"selected_tools={_csv(event.get('selected_tools', ()))} "
            f"read_only={str(bool(event.get('read_only', True))).lower()} "
            f"execution_allowed={str(bool(event.get('execution_allowed', False))).lower()} "
            f"evidence_count={event.get('evidence_count', 0)} "
            f"grounded_answer={str(bool(event.get('grounded_answer', False))).lower()} "
            f"ollama_called={str(bool(event.get('ollama_called', False))).lower()}"
        )
    print(_color("dim", f"selected_model_id={event.get('selected_model_id', '')}"))
    print(_color("dim", f"selected_model_role={event.get('selected_model_role', '')}"))
    print(_color("dim", f"retrieved_snippet_count={event.get('retrieved_snippet_count', 0)}"))
    print(_color("dim", f"retrieval_surfaces_used={_csv(event.get('retrieval_surfaces_used', ()))}"))
    print(_color("dim", f"mempalace_status={event.get('mempalace_status', '')}"))
    print(_color("dim", f"pc_control_allowed={str(bool(event.get('pc_control_allowed', False))).lower()}"))
    print(_color("dim", f"canonical_memory_write_allowed={str(bool(event.get('canonical_memory_write_allowed', False))).lower()}"))


def _print_stream_error(event: dict[str, Any]) -> None:
    error_kind = str(event.get("error_kind") or "ollama_stream_error")
    model_id = str(event.get("ollama_model_used") or event.get("selected_model_id") or "")
    elapsed = event.get("ollama_elapsed_seconds", "")
    # БАГФИКС #3: раньше все error_kind схлопывались в один generic текст.
    # Возвращены конкретные подсказки — особенно важно перед переключением
    # на DeepSeek-R1, где ошибки thinking-блоков будут встречаться чаще.
    if error_kind == "ollama_empty_response":
        print(_color("bg_red", f"\n[ERROR] ollama_empty_response model={model_id} elapsed={_seconds(elapsed)}"))
        return
    if error_kind == "ollama_thinking_without_final_response":
        print(_color("bg_red", f"\n[ERROR] ollama_thinking_without_final_response model={model_id} elapsed={_seconds(elapsed)}"))
        print(_color("yellow", "Модель показала thinking, но не дала финальный ответ. Повтори короче или отключи thinking для FAST."))
        return
    message = str(event.get("error_message") or "")
    print(_color("bg_red", f"\n[ERROR] {error_kind} model={model_id} elapsed={_seconds(elapsed)} {message}".rstrip()))


def _print_thinking_event(event: dict[str, Any]) -> None:
    global _THINKING_ACTIVE
    text = str(event.get("text") or "")
    if not text:
        return
    mode = _chat_mode()
    if mode == "compact":
        # В compact режиме осознанно тихо — чистый чат без шума.
        return
    if not _THINKING_ACTIVE:
        if mode == "debug":
            print(_color("dim", "\n  [thinking]\n  "), end="", flush=True)
        else:
            # БАГФИКС #2: раньше в detailed/compact thinking не показывался вообще,
            # из-за чего долгая генерация (особенно у reasoning-моделей вроде
            # DeepSeek-R1) выглядела как зависание. Теперь — лёгкий индикатор
            # без полного дампа рассуждений.
            print(_color("dim", "\n  [ 🧠 думает... ]"), end="", flush=True)
        _THINKING_ACTIVE = True
        return
    if mode == "debug":
        print(_color("dim", text.replace("\n", "\n  ")), end="", flush=True)


def _finish_thinking_if_active() -> None:
    global _THINKING_ACTIVE
    if not _THINKING_ACTIVE:
        return
    mode = _chat_mode()
    if mode == "debug":
        print(_color("green", "\n  [done thinking]\n") + _color("blue", "│ "), end="")
    elif mode == "detailed":
        print(_color("green", " готово.\n") + _color("blue", "│ "), end="")
    _THINKING_ACTIVE = False


def _print_stream_start_trace(event: dict[str, Any]) -> None:
    print(
        _color("dim", "[trace] ")
        + f"route={event.get('request_route', '')} "
        f"mode={event.get('route_mode', '')} "
        f"memory={event.get('retrieval_mode', '')} "
        f"model={event.get('selected_model_id', '')} "
        f"status={event.get('selected_model_status', '')}"
    )


def _print_stream_route_trace(event: dict[str, Any]) -> None:
    print(
        _color("dim", "[trace] ")
        + f"context={_seconds(event.get('context_elapsed_seconds', ''))} "
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
            _color("dim", "[trace] ")
            + f"intent_family={event.get('intent_family', '')} "
            f"selected_tools={_csv(event.get('selected_tools', ()))} "
            f"read_only={str(bool(event.get('read_only', True))).lower()} "
            f"execution_allowed={str(bool(event.get('execution_allowed', False))).lower()} "
            f"evidence_required={str(bool(event.get('evidence_required', False))).lower()}"
        )


def _print_command_unavailable() -> None:
    global _LAST_API_ERROR
    command_error = _LAST_API_ERROR
    if _api_is_available():
        if "timeout" in command_error:
            print(_color("red", "JARVIS command timed out. API is running, but route did not answer before timeout."))
        else:
            print(_color("red", "JARVIS command route failed."))
        if command_error:
            print(f"api_error={command_error}")
        return
    _LAST_API_ERROR = command_error or _LAST_API_ERROR
    _print_api_not_running()


def _print_terminal_runtime_error(user_text: str, exc: Exception) -> None:
    print(_color("bg_red", f"\n[TERMINAL ERROR] command={user_text!r} type={exc.__class__.__name__}: {exc}"))
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
    print(_color("red", "JARVIS API не запущен."))
    print("Старт API:")
    print("python -m uvicorn CONTROL_PLANE.api_server:app --host 127.0.0.1 --port 8765")
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


def _extract_pytest_summary(text: str) -> str:
    for line in reversed(text.splitlines()):
        if re.search(r"\b(passed|failed|skipped|error|errors|xfailed|xpassed)\b", line):
            return line.strip()
    return ""


def _as_tuple(value: Any) -> tuple[Any, ...]:
    if value is None:
        return ()
    if isinstance(value, tuple):
        return value
    if isinstance(value, list):
        return tuple(value)
    if isinstance(value, set):
        return tuple(sorted(value))
    if isinstance(value, str):
        return (value,) if value else ()
    return (value,)


def _csv(value: Any) -> str:
    if isinstance(value, (list, tuple, set)):
        return ", ".join(str(item) for item in value)
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
