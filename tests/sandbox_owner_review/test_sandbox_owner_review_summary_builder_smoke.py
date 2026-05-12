from __future__ import annotations

from MAKSIMAR_SERVER.OBSERVABILITY.memory_skill_metrics.sandbox_owner_review_summary_builder import (
    build_sandbox_owner_review_summary,
)


def test_sandbox_owner_review_summary_builder_smoke() -> None:
    summary = build_sandbox_owner_review_summary()

    assert summary["summary_ready"] is True
    assert summary["phase_id"] == "PHASE 6.4"
    assert summary["sandbox_binding_ready"] is True
    assert summary["simulation_result_reader_ready"] is True
    assert summary["owner_review_package_ready"] is True
    assert summary["self_expansion_allowed_next"] is True
