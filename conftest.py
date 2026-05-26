from __future__ import annotations

import sqlite3
import sys
from functools import wraps
from pathlib import Path
from typing import Any, Callable

PROJECT_ROOT = Path(__file__).resolve().parent
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from MAKSIMAR_CORE_LIB.architecture_map.pytest_report_gate import (  # noqa: E402
    FULL_PLATFORM_REPORTS_OPTION,
    is_maksimar_full_platform_report_enabled,
)

_PYTEST_MONITOR_PATCH_MARKER = "_maksimar_pytest_monitor_parallel_safe"


def _is_pytest_monitor_duplicate_session_error(exc: sqlite3.IntegrityError) -> bool:
    message = str(exc)
    return (
        "UNIQUE constraint failed" in message
        and "TEST_SESSIONS.SESSION_H" in message
    )


def _patch_pytest_monitor_insert_session() -> None:
    try:
        import pytest_monitor.handler as handler
    except Exception:
        return

    for candidate in vars(handler).values():
        if not isinstance(candidate, type):
            continue

        original = getattr(candidate, "insert_session", None)
        if not callable(original):
            continue

        if getattr(original, _PYTEST_MONITOR_PATCH_MARKER, False):
            continue

        @wraps(original)
        def wrapped_insert_session(
            self: object,
            *args: Any,
            __original: Callable[..., Any] = original,
            **kwargs: Any,
        ) -> Any:
            try:
                return __original(self, *args, **kwargs)
            except sqlite3.IntegrityError as exc:
                if _is_pytest_monitor_duplicate_session_error(exc):
                    return None
                raise

        setattr(wrapped_insert_session, _PYTEST_MONITOR_PATCH_MARKER, True)
        setattr(candidate, "insert_session", wrapped_insert_session)


_patch_pytest_monitor_insert_session()

# External vendor sandboxes are not part of MAKSIMAR test collection.
# They are validated only through explicit vendor acquisition smoke tests.
try:
    collect_ignore
except NameError:
    collect_ignore = []

for _external_path in ("EXTERNAL_BACKENDS",):
    if _external_path not in collect_ignore:
        collect_ignore.append(_external_path)


def pytest_addoption(parser):  # type: ignore[no-untyped-def]
    """Register MAKSIMAR pytest operator flags."""
    parser.addoption(
        FULL_PLATFORM_REPORTS_OPTION,
        action="store_true",
        default=False,
        help=(
            "Print MAKSIMAR full-platform terminal reports "
            "(Architecture Radar, X-Ray, Roadmap Next Step)."
        ),
    )


# MAKSIMAR pytest drift guard.
# Runs on every pytest session without spawning nested pytest.
def _maksimar_pytest_drift_guard_run(command: list[str], label: str) -> None:
    import subprocess

    root = Path(__file__).resolve().parent
    completed = subprocess.run(
        command,
        cwd=root,
        text=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        check=False,
    )
    if completed.returncode != 0:
        output = completed.stdout + completed.stderr
        raise RuntimeError(f"{label} failed:\n{output}")


def pytest_sessionstart(session):  # type: ignore[no-untyped-def]
    import os

    if os.environ.get("MAKSIMAR_SKIP_PYTEST_DRIFT_GUARD") == "1":
        return

    if os.environ.get("PYTEST_XDIST_WORKER"):
        return

    if getattr(session.config, "workerinput", None) is not None:
        return

    _maksimar_pytest_drift_guard_run(
        [sys.executable, "tools/git_stage_guard.py", "--staged", "--worktree-summary"],
        "pytest git stage guard",
    )
    _maksimar_pytest_drift_guard_run(
        [sys.executable, "tools/roadmap_pre_step_check.py", "--inventory-only"],
        "pytest roadmap pre-step inventory check",
    )
    _maksimar_pytest_drift_guard_run(
        [sys.executable, "tools/roadmap_post_step_drift_check.py"],
        "pytest roadmap post-step full drift check",
    )


# MAKSIMAR roadmap next-step summary.
def pytest_terminal_summary(terminalreporter, exitstatus, config):  # type: ignore[no-untyped-def]
    import os
    import subprocess

    if not is_maksimar_full_platform_report_enabled(config):
        return

    if os.environ.get("MAKSIMAR_SKIP_ROADMAP_NEXT_STEP_SUMMARY") == "1":
        return

    if os.environ.get("PYTEST_XDIST_WORKER"):
        return

    root = Path(__file__).resolve().parent
    tool = root / "tools" / "roadmap_next_step.py"
    if not tool.exists():
        return

    completed = subprocess.run(
        [sys.executable, str(tool)],
        cwd=root,
        text=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        check=False,
    )

    terminalreporter.write_sep("=", "MAKSIMAR ROADMAP NEXT STEP")
    terminalreporter.write(completed.stdout)
    if completed.returncode != 0:
        terminalreporter.write(completed.stderr)
