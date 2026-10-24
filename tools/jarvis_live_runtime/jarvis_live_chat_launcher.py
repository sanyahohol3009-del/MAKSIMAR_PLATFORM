from __future__ import annotations

import argparse
import os
import subprocess
import sys
from pathlib import Path


PROJECT_ROOT = Path(__file__).resolve().parents[2]
TERMINAL_CHAT_COMMAND = (
    sys.executable,
    "tools/jarvis_live_runtime/jarvis_live_terminal_chat.py",
)


def main(argv: list[str] | None = None) -> int:
    """Open terminal chat against the Control Plane owned by ./tools/work."""
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--restart",
        action="store_true",
        help="legacy no-op; runtime lifecycle belongs to ./tools/work and ./tools/rest",
    )
    args = parser.parse_args(argv)
    if args.restart:
        print("[chat] --restart ignored: use ./tools/rest and ./tools/work for runtime lifecycle")
    return _run_terminal_chat(_launcher_env())


def _launcher_env() -> dict[str, str]:
    env = dict(os.environ)
    env.setdefault("JARVIS_LIVE_FAST_FALLBACK_ENABLED", "0")
    env.setdefault("JARVIS_HELPER_INPUT_CORRECTION_ENABLED", "true")
    env.setdefault("JARVIS_HELPER_MODEL", "jarvis:helper3b")
    env.setdefault("OLLAMA_NUM_PARALLEL", "1")
    env.setdefault("OLLAMA_MAX_LOADED_MODELS", "1")
    return env


def _run_terminal_chat(env: dict[str, str]) -> int:
    result = subprocess.run(
        list(TERMINAL_CHAT_COMMAND),
        cwd=str(PROJECT_ROOT),
        env=env,
        check=False,
    )
    return int(result.returncode)


if __name__ == "__main__":
    raise SystemExit(main())
