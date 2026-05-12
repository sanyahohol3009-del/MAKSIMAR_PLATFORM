from __future__ import annotations

from pathlib import Path

from MAKSIMAR_CORE_LIB.memory_policy.governance_federation_gap_report_builder import (
    build_governance_federation_gap_report,
)
from MAKSIMAR_SERVER.OBSERVABILITY.memory_skill_metrics.governance_federation_gap_summary_builder import (
    build_governance_federation_gap_summary,
)


def test_governance_federation_gap_final_acceptance_smoke() -> None:
    report = build_governance_federation_gap_report()
    summary = build_governance_federation_gap_summary()
    doc = Path("docs/architecture/foundation/phase_6_1_governance_federation_gap_pass_acceptance_v1.md")

    assert doc.exists()
    assert report["gap_pass_ready"] is True
    assert summary["summary_ready"] is True
    assert report["existing_surfaces_reused"] is True
    assert report["runtime_mutation_allowed"] is False
