from __future__ import annotations

import sqlite3

import conftest


def test_pytest_monitor_duplicate_session_error_is_idempotent() -> None:
    exc = sqlite3.IntegrityError(
        "UNIQUE constraint failed: TEST_SESSIONS.SESSION_H"
    )

    assert conftest._is_pytest_monitor_duplicate_session_error(exc) is True


def test_pytest_monitor_handler_is_patched_when_available() -> None:
    import pytest_monitor.handler as handler

    patched = []
    for candidate in vars(handler).values():
        if isinstance(candidate, type):
            method = getattr(candidate, "insert_session", None)
            if callable(method) and getattr(
                method,
                "_maksimar_pytest_monitor_parallel_safe",
                False,
            ):
                patched.append(candidate)

    assert patched
