from __future__ import annotations

from MAKSIMAR_SERVER.MEMORY_ACCEPTANCE import build_memory_acceptance_gate_report


def test_memory_acceptance_gates_smoke() -> None:
    report = build_memory_acceptance_gate_report()

    assert report.acceptance_gates_ready is True
    assert report.total_gates >= 6
    assert report.passed_gates == report.total_gates
    assert report.failed_gates == 0
    assert report.duplicate_write_allowed is False
    assert report.canonical_write_allowed is False
    assert report.runtime_mutation_allowed is False
