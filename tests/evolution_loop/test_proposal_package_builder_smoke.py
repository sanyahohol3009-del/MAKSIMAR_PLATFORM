from __future__ import annotations

from MAKSIMAR_CORE_LIB.evolution_loop import (
    RankingSelectionResult,
    build_proposal_package,
)


def test_build_proposal_package() -> None:
    """Proposal package builder should create package from selection result."""
    package = build_proposal_package(
        RankingSelectionResult(
            total_candidates=2,
            selected_execution_id="eval_exec_002",
            selected_evaluation_id="codegen_eval",
            selected_score=0.9,
            selected_passed=True,
        )
    )

    assert package.package_id == "proposal_pkg_eval_exec_002"
    assert package.selected_execution_id == "eval_exec_002"
    assert package.selected_evaluation_id == "codegen_eval"
    assert package.selected_score == 0.9
    assert package.selected_passed is True
    assert package.status == "proposed"
