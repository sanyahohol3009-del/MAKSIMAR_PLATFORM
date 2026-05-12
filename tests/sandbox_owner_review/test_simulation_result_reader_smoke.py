from __future__ import annotations

from MAKSIMAR_SERVER.SANDBOX_REVIEW import build_simulation_result_reader


def test_simulation_result_reader_smoke() -> None:
    reader = build_simulation_result_reader()

    assert reader["simulation_result_reader_ready"] is True
    assert reader["missing_surfaces"] == ()
    assert reader["simulation_result_read_only"] is True
    assert reader["simulation_passed"] is True
    assert reader["simulation_failure_count"] == 0
