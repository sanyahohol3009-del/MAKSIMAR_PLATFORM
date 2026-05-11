from __future__ import annotations

import sqlite3
import sys
from functools import wraps
from pathlib import Path
from typing import Any, Callable


PROJECT_ROOT = Path(__file__).resolve().parent
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))


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
