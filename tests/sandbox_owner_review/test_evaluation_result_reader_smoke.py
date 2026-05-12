from __future__ import annotations

from MAKSIMAR_SERVER.SANDBOX_REVIEW import build_evaluation_result_reader


def test_evaluation_result_reader_smoke() -> None:
    reader = build_evaluation_result_reader()

    assert reader["evaluation_result_reader_ready"] is True
    assert reader["missing_surfaces"] == ()
    assert reader["evaluation_result_read_only"] is True
    assert reader["evaluation_passed"] is True
    assert reader["evaluation_failure_count"] == 0
