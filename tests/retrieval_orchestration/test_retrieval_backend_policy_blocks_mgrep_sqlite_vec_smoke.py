from __future__ import annotations

from MAKSIMAR_SERVER.CONTROL_PLANE.memory_routing import (
    build_retrieval_backend_policy_gate,
)


def test_retrieval_backend_policy_blocks_mgrep_sqlite_vec_smoke() -> None:
    gate = build_retrieval_backend_policy_gate()

    by_candidate = {entry.backend_candidate: entry for entry in gate.entries}

    assert gate.mgrep_blocked is True
    assert gate.sqlite_vec_blocked is True

    assert by_candidate["mgrep"].approved_for_phase_1_7 is False
    assert by_candidate["mgrep"].adapter_required is True
    assert by_candidate["mgrep"].external_execution_required is True

    assert by_candidate["sqlite_vec"].approved_for_phase_1_7 is False
    assert by_candidate["sqlite_vec"].adapter_required is True
    assert by_candidate["sqlite_vec"].external_execution_required is True
