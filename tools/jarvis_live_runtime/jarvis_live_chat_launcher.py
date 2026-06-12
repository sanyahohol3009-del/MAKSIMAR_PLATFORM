from __future__ import annotations

import argparse
import json
import os
import signal
import subprocess
import sys
import time
import urllib.error
import urllib.request
from pathlib import Path
from typing import Any


PROJECT_ROOT = Path(__file__).resolve().parents[2]
API_HOST = "127.0.0.1"
API_PORT = "8765"
API_BASE_URL = f"http://{API_HOST}:{API_PORT}"
HEALTH_URL = f"{API_BASE_URL}/health"
UVICORN_COMMAND = (
    sys.executable,
    "-m",
    "uvicorn",
    "CONTROL_PLANE.api_server:app",
    "--host",
    API_HOST,
    "--port",
    API_PORT,
)
TERMINAL_CHAT_COMMAND = (
    sys.executable,
    "tools/jarvis_live_runtime/jarvis_live_terminal_chat.py",
)
STARTUP_TIMEOUT_SECONDS = 20.0


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--restart", action="store_true")
    args = parser.parse_args(argv)

    env = _launcher_env()
    started_process: subprocess.Popen[str] | None = None

    if _api_is_healthy():
        if args.restart:
            _stop_matching_project_api_processes()
        else:
            print("[launcher] api ready")
            print("[launcher] opening JARVIS terminal chat")
            return _run_terminal_chat(env)
    else:
        _stop_matching_project_api_processes()

    print("[launcher] starting CONTROL_PLANE api on 127.0.0.1:8765")
    started_process = subprocess.Popen(  # noqa: S603 - controlled canonical local API.
        list(UVICORN_COMMAND),
        cwd=str(PROJECT_ROOT),
        env=env,
        start_new_session=False,
    )
    try:
        if not _wait_until_api_ready():
            print("[launcher] api failed to become ready")
            return 1
        print("[launcher] api ready")
        print("[launcher] opening JARVIS terminal chat")
        return _run_terminal_chat(env)
    finally:
        if started_process is not None:
            _stop_started_process(started_process)


def _launcher_env() -> dict[str, str]:
    env = dict(os.environ)
    env.setdefault("JARVIS_LIVE_FAST_FALLBACK_ENABLED", "0")
    env.setdefault("OLLAMA_KEEP_ALIVE", "30m")
    env.setdefault("OLLAMA_NUM_PARALLEL", "1")
    env.setdefault("OLLAMA_MAX_LOADED_MODELS", "1")
    return env


def _api_is_healthy() -> bool:
    try:
        with urllib.request.urlopen(HEALTH_URL, timeout=1.0) as response:
            payload = json.loads(response.read().decode("utf-8", errors="replace"))
    except (OSError, TimeoutError, urllib.error.URLError, json.JSONDecodeError):
        return False
    return isinstance(payload, dict) and bool(payload.get("ok"))


def _wait_until_api_ready() -> bool:
    deadline = time.monotonic() + STARTUP_TIMEOUT_SECONDS
    while time.monotonic() < deadline:
        if _api_is_healthy():
            return True
        time.sleep(0.25)
    return False


def _run_terminal_chat(env: dict[str, str]) -> int:
    result = subprocess.run(  # noqa: S603 - controlled canonical terminal client.
        list(TERMINAL_CHAT_COMMAND),
        cwd=str(PROJECT_ROOT),
        env=env,
        check=False,
    )
    return int(result.returncode)


def _stop_matching_project_api_processes() -> None:
    pids = tuple(_matching_project_api_pids())
    if not pids:
        return
    print("[launcher] stopping stale jarvis api...")
    for pid in pids:
        _terminate_pid(pid)


def _matching_project_api_pids() -> tuple[int, ...]:
    proc_root = Path("/proc")
    if not proc_root.exists():
        return ()
    current_pid = os.getpid()
    matches: list[int] = []
    for path in proc_root.iterdir():
        if not path.name.isdigit():
            continue
        pid = int(path.name)
        if pid == current_pid:
            continue
        if _process_matches_project_api(path):
            matches.append(pid)
    return tuple(matches)


def _process_matches_project_api(proc_path: Path) -> bool:
    cmdline = _read_proc_cmdline(proc_path)
    if not cmdline:
        return False
    joined = " ".join(cmdline)
    if "uvicorn" not in joined:
        return False
    if "CONTROL_PLANE.api_server:app" not in joined:
        return False
    if API_PORT not in cmdline:
        return False
    try:
        cwd = proc_path.joinpath("cwd").resolve()
    except OSError:
        return False
    return cwd == PROJECT_ROOT


def _read_proc_cmdline(proc_path: Path) -> tuple[str, ...]:
    try:
        raw = proc_path.joinpath("cmdline").read_bytes()
    except OSError:
        return ()
    return tuple(part.decode("utf-8", errors="replace") for part in raw.split(b"\0") if part)


def _terminate_pid(pid: int) -> None:
    try:
        os.kill(pid, signal.SIGTERM)
    except ProcessLookupError:
        return
    deadline = time.monotonic() + 5.0
    while time.monotonic() < deadline:
        if not _pid_exists(pid):
            return
        time.sleep(0.1)
    try:
        os.kill(pid, signal.SIGKILL)
    except ProcessLookupError:
        return


def _stop_started_process(process: subprocess.Popen[str]) -> None:
    if process.poll() is not None:
        return
    process.terminate()
    try:
        process.wait(timeout=5.0)
    except subprocess.TimeoutExpired:
        process.kill()
        process.wait(timeout=5.0)


def _pid_exists(pid: int) -> bool:
    try:
        os.kill(pid, 0)
    except ProcessLookupError:
        return False
    except PermissionError:
        return True
    return True


if __name__ == "__main__":
    raise SystemExit(main())
