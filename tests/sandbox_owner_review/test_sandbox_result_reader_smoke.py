from __future__ import annotations

from MAKSIMAR_SERVER.SANDBOX_REVIEW import build_sandbox_result_reader


def test_sandbox_result_reader_smoke() -> None:
    reader = build_sandbox_result_reader()

    assert reader["sandbox_result_reader_ready"] is True
    assert reader["missing_surfaces"] == ()
    assert reader["sandbox_result_read_only"] is True
    assert reader["sandbox_passed"] is True
    assert reader["sandbox_failure_count"] == 0
