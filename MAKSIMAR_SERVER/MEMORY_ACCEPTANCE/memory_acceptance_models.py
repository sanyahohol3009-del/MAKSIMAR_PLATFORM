from __future__ import annotations

from dataclasses import dataclass
from typing import Literal, Tuple


AcceptanceCriterionKind = Literal[
    "visibility",
    "safety",
    "operator_review",
    "release_readiness",
    "drift_protection",
]


@dataclass(frozen=True, slots=True)
class MemoryAcceptanceCriterion:
    criterion_id: str
    label: str
    criterion_kind: AcceptanceCriterionKind
    required: bool
    passed: bool
    evidence_ref: str
    risk_if_missing: str

    def __post_init__(self) -> None:
        if not self.criterion_id:
            raise ValueError("criterion_id must be non-empty")
        if not self.label:
            raise ValueError("label must be non-empty")
        if not self.evidence_ref:
            raise ValueError("evidence_ref must be non-empty")
        if not self.risk_if_missing:
            raise ValueError("risk_if_missing must be non-empty")


@dataclass(frozen=True, slots=True)
class MemoryAcceptanceContract:
    contract_id: str
    roadmap_family: str
    phase_id: str
    track_scope: str
    criteria: Tuple[MemoryAcceptanceCriterion, ...]
    dashboard_read_only: bool
    duplicate_write_allowed: bool
    canonical_write_allowed: bool
    runtime_mutation_allowed: bool
    operator_review_required: bool
    release_preview_required: bool
    acceptance_ready: bool

    def __post_init__(self) -> None:
        if not self.contract_id:
            raise ValueError("contract_id must be non-empty")
        if self.roadmap_family != "memory_roadmap_v5_1":
            raise ValueError("roadmap_family must be memory_roadmap_v5_1")
        if self.phase_id != "PHASE 6.0":
            raise ValueError("phase_id must be PHASE 6.0")
        if self.track_scope != "memory":
            raise ValueError("track_scope must be memory")
        if not self.criteria:
            raise ValueError("criteria must be non-empty")

        criterion_ids = {criterion.criterion_id for criterion in self.criteria}
        if len(criterion_ids) != len(self.criteria):
            raise ValueError("criterion_id values must be unique")

        if self.dashboard_read_only is not True:
            raise ValueError("dashboard_read_only must be True")
        if self.duplicate_write_allowed:
            raise ValueError("duplicate_write_allowed must be False")
        if self.canonical_write_allowed:
            raise ValueError("canonical_write_allowed must be False")
        if self.runtime_mutation_allowed:
            raise ValueError("runtime_mutation_allowed must be False")
        if self.operator_review_required is not True:
            raise ValueError("operator_review_required must be True")
        if self.release_preview_required is not True:
            raise ValueError("release_preview_required must be True")

        if self.acceptance_ready:
            failed_required = [
                criterion.criterion_id
                for criterion in self.criteria
                if criterion.required and not criterion.passed
            ]
            if failed_required:
                raise ValueError(f"required criteria failed: {failed_required}")


def build_memory_acceptance_contract() -> MemoryAcceptanceContract:
    criteria = (
        MemoryAcceptanceCriterion(
            criterion_id="memory_full_visibility",
            label="Project memory is fully visible through dashboard read-only map.",
            criterion_kind="visibility",
            required=True,
            passed=True,
            evidence_ref="docs/architecture/foundation/phase_5_2_final_dashboard_memory_map_acceptance_v1.md",
            risk_if_missing="Operator cannot trust product readiness without full memory visibility.",
        ),
        MemoryAcceptanceCriterion(
            criterion_id="write_safety_policy",
            label="Memory write safety policy blocks direct canonical and runtime mutation.",
            criterion_kind="safety",
            required=True,
            passed=True,
            evidence_ref="MAKSIMAR_SERVER/MEMORY_ACCEPTANCE/memory_write_safety_models.py",
            risk_if_missing="Runtime may write directly into canonical memory without review.",
        ),
        MemoryAcceptanceCriterion(
            criterion_id="operator_review_path",
            label="Operator review package is required before release promotion.",
            criterion_kind="operator_review",
            required=True,
            passed=True,
            evidence_ref="MAKSIMAR_SERVER/MEMORY_ACCEPTANCE/memory_operator_review_builder.py",
            risk_if_missing="Owner may not see risk, diff, gates and release summary before promotion.",
        ),
        MemoryAcceptanceCriterion(
            criterion_id="release_candidate_path",
            label="Release candidate is assembled from gated read-only evidence.",
            criterion_kind="release_readiness",
            required=True,
            passed=True,
            evidence_ref="MAKSIMAR_SERVER/MEMORY_ACCEPTANCE/memory_release_candidate_builder.py",
            risk_if_missing="Memory layer cannot be promoted as product-ready safely.",
        ),
        MemoryAcceptanceCriterion(
            criterion_id="post_step_drift_guard",
            label="Post-step drift guard is active before roadmap continuation.",
            criterion_kind="drift_protection",
            required=True,
            passed=True,
            evidence_ref="tools/roadmap_post_step_drift_check.py",
            risk_if_missing="Roadmap drift may reappear after accepted phases.",
        ),
    )

    return MemoryAcceptanceContract(
        contract_id="memory_acceptance_contract_phase_6_0_001",
        roadmap_family="memory_roadmap_v5_1",
        phase_id="PHASE 6.0",
        track_scope="memory",
        criteria=criteria,
        dashboard_read_only=True,
        duplicate_write_allowed=False,
        canonical_write_allowed=False,
        runtime_mutation_allowed=False,
        operator_review_required=True,
        release_preview_required=True,
        acceptance_ready=True,
    )
