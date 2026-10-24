from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True, slots=True)
class ProposalPackage:
    """Canonical proposal package produced by evolution loop."""

    package_id: str
    selected_execution_id: str
    selected_evaluation_id: str
    selected_score: float
    selected_passed: bool
    status: str
    # Optional bounded engineering-proposal projection.  The selected
    # evaluation fields remain the legacy compatibility core.
    proposal_kind: str = "ARCHITECTURE"
    target_scope: str = "bounded_platform_scope"
    observed_problem_refs: tuple[str, ...] = ()
    affected_components: tuple[str, ...] = ()
    required_capabilities: tuple[str, ...] = ()
    required_permissions: tuple[str, ...] = ()
    migration_plan: str = ""
    rollback_plan: str = ""
    validation_plan: str = ""
    provenance: str = ""

    def __post_init__(self) -> None:
        allowed = {
            "ARCHITECTURE", "OPTIMIZATION", "PERFORMANCE", "SECURITY",
            "REFACTOR", "MIGRATION", "CONTAINERIZATION", "CAPABILITY_EXPANSION",
            "PROVIDER_CHANGE", "DEPENDENCY_CHANGE", "TEST_STRATEGY", "MODEL_IMPROVEMENT",
        }
        if self.proposal_kind not in allowed:
            raise ValueError("unsupported proposal_kind")
        for name in ("target_scope", "migration_plan", "rollback_plan", "validation_plan", "provenance"):
            if not isinstance(getattr(self, name), str):
                raise TypeError(f"{name} must be a string")
