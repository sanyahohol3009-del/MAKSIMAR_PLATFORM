from __future__ import annotations

from dataclasses import dataclass
from typing import Literal, Tuple


SelfExpansionStage = Literal[
    "gap_detection",
    "proposal_preparation",
    "audit_required",
    "codegen_context_required",
    "sandbox_owner_review_required",
    "human_approval_required",
]

SelfExpansionSurfaceKind = Literal[
    "memory_drift_detection",
    "evolution_loop",
    "proposal_audit_spine",
    "controlled_codegen_context",
    "sandbox_owner_review",
    "memory_acceptance",
    "governed_action_docs",
    "self_expansion_gate",
]


@dataclass(frozen=True, slots=True)
class SelfExpansionSurface:
    surface_id: str
    surface_kind: SelfExpansionSurfaceKind
    source_path: str
    reused_existing_surface: bool
    read_only: bool
    proposal_only: bool
    direct_core_write_allowed: bool
    auto_apply_allowed: bool
    deployment_allowed: bool
    runtime_mutation_allowed: bool
    productization_allowed: bool
    surface_ready: bool

    def __post_init__(self) -> None:
        if not self.surface_id:
            raise ValueError("surface_id must be non-empty")
        if not self.source_path:
            raise ValueError("source_path must be non-empty")
        if self.read_only is not True:
            raise ValueError("read_only must be True")
        if self.proposal_only is not True:
            raise ValueError("proposal_only must be True")
        if self.direct_core_write_allowed:
            raise ValueError("direct_core_write_allowed must be False")
        if self.auto_apply_allowed:
            raise ValueError("auto_apply_allowed must be False")
        if self.deployment_allowed:
            raise ValueError("deployment_allowed must be False")
        if self.runtime_mutation_allowed:
            raise ValueError("runtime_mutation_allowed must be False")
        if self.productization_allowed:
            raise ValueError("productization_allowed must be False")
        if self.surface_ready is not True:
            raise ValueError("surface_ready must be True")


@dataclass(frozen=True, slots=True)
class SelfExpansionReadinessContract:
    contract_id: str
    roadmap_family: str
    phase_id: str
    track_scope: str
    stages: Tuple[SelfExpansionStage, ...]
    surfaces: Tuple[SelfExpansionSurface, ...]
    existing_surfaces_reused: bool
    gap_detection_ready: bool
    proposal_preparation_ready: bool
    audit_required: bool
    codegen_context_required: bool
    sandbox_owner_review_required: bool
    human_approval_required: bool
    proposal_only_self_expansion_allowed: bool
    autonomous_self_expansion_allowed: bool
    direct_core_write_allowed: bool
    auto_apply_allowed: bool
    deployment_allowed: bool
    runtime_mutation_allowed: bool
    productization_allowed_now: bool
    readiness_ready: bool

    def __post_init__(self) -> None:
        if not self.contract_id:
            raise ValueError("contract_id must be non-empty")
        if self.roadmap_family != "memory_roadmap_v5_1":
            raise ValueError("roadmap_family must be memory_roadmap_v5_1")
        if self.phase_id != "PHASE 6.5":
            raise ValueError("phase_id must be PHASE 6.5")
        if self.track_scope != "bootstrapped_self_expansion_gate":
            raise ValueError("track_scope must be bootstrapped_self_expansion_gate")

        required_stages = {
            "gap_detection",
            "proposal_preparation",
            "audit_required",
            "codegen_context_required",
            "sandbox_owner_review_required",
            "human_approval_required",
        }
        if set(self.stages) != required_stages:
            raise ValueError("stages must match self-expansion gate stages")
        if not self.surfaces:
            raise ValueError("surfaces must be non-empty")

        surface_ids = {surface.surface_id for surface in self.surfaces}
        if len(surface_ids) != len(self.surfaces):
            raise ValueError("surface_id values must be unique")

        if self.existing_surfaces_reused is not True:
            raise ValueError("existing_surfaces_reused must be True")
        if self.gap_detection_ready is not True:
            raise ValueError("gap_detection_ready must be True")
        if self.proposal_preparation_ready is not True:
            raise ValueError("proposal_preparation_ready must be True")
        if self.audit_required is not True:
            raise ValueError("audit_required must be True")
        if self.codegen_context_required is not True:
            raise ValueError("codegen_context_required must be True")
        if self.sandbox_owner_review_required is not True:
            raise ValueError("sandbox_owner_review_required must be True")
        if self.human_approval_required is not True:
            raise ValueError("human_approval_required must be True")
        if self.proposal_only_self_expansion_allowed is not True:
            raise ValueError("proposal_only_self_expansion_allowed must be True")
        if self.autonomous_self_expansion_allowed:
            raise ValueError("autonomous_self_expansion_allowed must be False")
        if self.direct_core_write_allowed:
            raise ValueError("direct_core_write_allowed must be False")
        if self.auto_apply_allowed:
            raise ValueError("auto_apply_allowed must be False")
        if self.deployment_allowed:
            raise ValueError("deployment_allowed must be False")
        if self.runtime_mutation_allowed:
            raise ValueError("runtime_mutation_allowed must be False")
        if self.productization_allowed_now:
            raise ValueError("productization_allowed_now must be False")
        if not all(surface.surface_ready for surface in self.surfaces):
            raise ValueError("all surfaces must be ready")
        if self.readiness_ready is not True:
            raise ValueError("readiness_ready must be True")


def build_self_expansion_readiness_contract() -> SelfExpansionReadinessContract:
    stages: Tuple[SelfExpansionStage, ...] = (
        "gap_detection",
        "proposal_preparation",
        "audit_required",
        "codegen_context_required",
        "sandbox_owner_review_required",
        "human_approval_required",
    )

    surfaces = (
        SelfExpansionSurface(
            surface_id="surface_memory_drift_detection",
            surface_kind="memory_drift_detection",
            source_path="MAKSIMAR_CORE_LIB/memory_engine/drift_detection",
            reused_existing_surface=True,
            read_only=True,
            proposal_only=True,
            direct_core_write_allowed=False,
            auto_apply_allowed=False,
            deployment_allowed=False,
            runtime_mutation_allowed=False,
            productization_allowed=False,
            surface_ready=True,
        ),
        SelfExpansionSurface(
            surface_id="surface_evolution_loop",
            surface_kind="evolution_loop",
            source_path="MAKSIMAR_CORE_LIB/evolution_loop",
            reused_existing_surface=True,
            read_only=True,
            proposal_only=True,
            direct_core_write_allowed=False,
            auto_apply_allowed=False,
            deployment_allowed=False,
            runtime_mutation_allowed=False,
            productization_allowed=False,
            surface_ready=True,
        ),
        SelfExpansionSurface(
            surface_id="surface_proposal_audit_spine",
            surface_kind="proposal_audit_spine",
            source_path="MAKSIMAR_SERVER/PROPOSAL_AUDIT",
            reused_existing_surface=True,
            read_only=True,
            proposal_only=True,
            direct_core_write_allowed=False,
            auto_apply_allowed=False,
            deployment_allowed=False,
            runtime_mutation_allowed=False,
            productization_allowed=False,
            surface_ready=True,
        ),
        SelfExpansionSurface(
            surface_id="surface_controlled_codegen_context",
            surface_kind="controlled_codegen_context",
            source_path="MAKSIMAR_SERVER/CODEGEN_CONTEXT",
            reused_existing_surface=True,
            read_only=True,
            proposal_only=True,
            direct_core_write_allowed=False,
            auto_apply_allowed=False,
            deployment_allowed=False,
            runtime_mutation_allowed=False,
            productization_allowed=False,
            surface_ready=True,
        ),
        SelfExpansionSurface(
            surface_id="surface_sandbox_owner_review",
            surface_kind="sandbox_owner_review",
            source_path="MAKSIMAR_SERVER/SANDBOX_REVIEW",
            reused_existing_surface=True,
            read_only=True,
            proposal_only=True,
            direct_core_write_allowed=False,
            auto_apply_allowed=False,
            deployment_allowed=False,
            runtime_mutation_allowed=False,
            productization_allowed=False,
            surface_ready=True,
        ),
        SelfExpansionSurface(
            surface_id="surface_memory_acceptance",
            surface_kind="memory_acceptance",
            source_path="MAKSIMAR_SERVER/MEMORY_ACCEPTANCE",
            reused_existing_surface=True,
            read_only=True,
            proposal_only=True,
            direct_core_write_allowed=False,
            auto_apply_allowed=False,
            deployment_allowed=False,
            runtime_mutation_allowed=False,
            productization_allowed=False,
            surface_ready=True,
        ),
        SelfExpansionSurface(
            surface_id="surface_governed_action_docs",
            surface_kind="governed_action_docs",
            source_path="docs/security_governance/governed_action_model",
            reused_existing_surface=True,
            read_only=True,
            proposal_only=True,
            direct_core_write_allowed=False,
            auto_apply_allowed=False,
            deployment_allowed=False,
            runtime_mutation_allowed=False,
            productization_allowed=False,
            surface_ready=True,
        ),
        SelfExpansionSurface(
            surface_id="surface_self_expansion_gate",
            surface_kind="self_expansion_gate",
            source_path="MAKSIMAR_SERVER/SELF_EXPANSION_GATE",
            reused_existing_surface=False,
            read_only=True,
            proposal_only=True,
            direct_core_write_allowed=False,
            auto_apply_allowed=False,
            deployment_allowed=False,
            runtime_mutation_allowed=False,
            productization_allowed=False,
            surface_ready=True,
        ),
    )

    return SelfExpansionReadinessContract(
        contract_id="self_expansion_readiness_contract_phase_6_5_001",
        roadmap_family="memory_roadmap_v5_1",
        phase_id="PHASE 6.5",
        track_scope="bootstrapped_self_expansion_gate",
        stages=stages,
        surfaces=surfaces,
        existing_surfaces_reused=True,
        gap_detection_ready=True,
        proposal_preparation_ready=True,
        audit_required=True,
        codegen_context_required=True,
        sandbox_owner_review_required=True,
        human_approval_required=True,
        proposal_only_self_expansion_allowed=True,
        autonomous_self_expansion_allowed=False,
        direct_core_write_allowed=False,
        auto_apply_allowed=False,
        deployment_allowed=False,
        runtime_mutation_allowed=False,
        productization_allowed_now=False,
        readiness_ready=True,
    )
