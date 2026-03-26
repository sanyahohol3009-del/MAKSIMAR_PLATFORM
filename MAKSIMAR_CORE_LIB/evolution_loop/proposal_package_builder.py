from __future__ import annotations

from MAKSIMAR_CORE_LIB.evolution_loop.proposal_package_models import (
    ProposalPackage,
)
from MAKSIMAR_CORE_LIB.evolution_loop.ranking_models import (
    RankingSelectionResult,
)


def build_proposal_package(
    selection: RankingSelectionResult,
) -> ProposalPackage:
    """Build canonical proposal package from ranking selection result."""
    package_id = f"proposal_pkg_{selection.selected_execution_id}"

    return ProposalPackage(
        package_id=package_id,
        selected_execution_id=selection.selected_execution_id,
        selected_evaluation_id=selection.selected_evaluation_id,
        selected_score=selection.selected_score,
        selected_passed=selection.selected_passed,
        status="proposed",
    )
