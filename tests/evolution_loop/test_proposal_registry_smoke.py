from __future__ import annotations

from MAKSIMAR_CORE_LIB.evolution_loop import (
    build_proposal_registry_summary,
)


def test_proposal_registry_summary_builds() -> None:
    """Proposal registry summary should build successfully."""
    summary = build_proposal_registry_summary()

    assert summary.total_proposals >= 1
    assert len(summary.records) == summary.total_proposals


def test_proposal_registry_contains_known_proposal() -> None:
    """Proposal registry should contain at least one known proposal contract."""
    summary = build_proposal_registry_summary()

    assert any(
    record.proposal_id
    in {
        "simulation_proposal_package.v1",
        "codegen_proposal_package.v1",
    }
    for record in summary.records
)
