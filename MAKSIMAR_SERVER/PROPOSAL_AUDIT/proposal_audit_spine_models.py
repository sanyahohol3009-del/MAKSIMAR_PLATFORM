from __future__ import annotations

from dataclasses import dataclass
from typing import Literal, Tuple


ProposalAuditStage = Literal[
    "proposal_inspection",
    "audit_inspection",
    "approval_read_model",
    "operator_review",
    "proposal_audit_summary",
    "proposal_audit_preview",
]

ProposalAuditSurfaceKind = Literal[
    "existing_evolution_loop",
    "existing_evolution_debug",
    "security_governance_doc",
    "memory_acceptance_surface",
    "proposal_audit_spine",
]


@dataclass(frozen=True, slots=True)
class ProposalAuditSurface:
    surface_id: str
    surface_kind: ProposalAuditSurfaceKind
    source_path: str
    reused_existing_surface: bool
    read_only: bool
    action_execution_allowed: bool
    code_write_allowed: bool
    runtime_mutation_allowed: bool
    surface_ready: bool

    def __post_init__(self) -> None:
        if not self.surface_id:
            raise ValueError("surface_id must be non-empty")
        if not self.source_path:
            raise ValueError("source_path must be non-empty")
        if self.read_only is not True:
            raise ValueError("read_only must be True")
        if self.action_execution_allowed:
            raise ValueError("action_execution_allowed must be False")
        if self.code_write_allowed:
            raise ValueError("code_write_allowed must be False")
        if self.runtime_mutation_allowed:
            raise ValueError("runtime_mutation_allowed must be False")
        if self.surface_ready is not True:
            raise ValueError("surface_ready must be True")


@dataclass(frozen=True, slots=True)
class ProposalAuditSpineContract:
    contract_id: str
    roadmap_family: str
    phase_id: str
    track_scope: str
    stages: Tuple[ProposalAuditStage, ...]
    surfaces: Tuple[ProposalAuditSurface, ...]
    existing_surfaces_reused: bool
    proposal_visible: bool
    audit_visible: bool
    approval_visible: bool
    operator_review_required: bool
    approval_granted_by_default: bool
    code_write_allowed: bool
    action_execution_allowed: bool
    sandbox_execution_allowed_now: bool
    self_expansion_allowed_now: bool
    productization_allowed_now: bool
    spine_ready: bool

    def __post_init__(self) -> None:
        if not self.contract_id:
            raise ValueError("contract_id must be non-empty")
        if self.roadmap_family != "memory_roadmap_v5_1":
            raise ValueError("roadmap_family must be memory_roadmap_v5_1")
        if self.phase_id != "PHASE 6.2":
            raise ValueError("phase_id must be PHASE 6.2")
        if self.track_scope != "proposal_audit_approval":
            raise ValueError("track_scope must be proposal_audit_approval")
        if not self.stages:
            raise ValueError("stages must be non-empty")
        if not self.surfaces:
            raise ValueError("surfaces must be non-empty")

        required_stages = {
            "proposal_inspection",
            "audit_inspection",
            "approval_read_model",
            "operator_review",
            "proposal_audit_summary",
            "proposal_audit_preview",
        }
        if set(self.stages) != required_stages:
            raise ValueError("stages must match required proposal/audit/approval spine stages")

        surface_ids = {surface.surface_id for surface in self.surfaces}
        if len(surface_ids) != len(self.surfaces):
            raise ValueError("surface_id values must be unique")

        if self.existing_surfaces_reused is not True:
            raise ValueError("existing_surfaces_reused must be True")
        if self.proposal_visible is not True:
            raise ValueError("proposal_visible must be True")
        if self.audit_visible is not True:
            raise ValueError("audit_visible must be True")
        if self.approval_visible is not True:
            raise ValueError("approval_visible must be True")
        if self.operator_review_required is not True:
            raise ValueError("operator_review_required must be True")
        if self.approval_granted_by_default:
            raise ValueError("approval_granted_by_default must be False")
        if self.code_write_allowed:
            raise ValueError("code_write_allowed must be False")
        if self.action_execution_allowed:
            raise ValueError("action_execution_allowed must be False")
        if self.sandbox_execution_allowed_now:
            raise ValueError("sandbox_execution_allowed_now must be False")
        if self.self_expansion_allowed_now:
            raise ValueError("self_expansion_allowed_now must be False")
        if self.productization_allowed_now:
            raise ValueError("productization_allowed_now must be False")
        if not all(surface.surface_ready for surface in self.surfaces):
            raise ValueError("all surfaces must be ready")
        if self.spine_ready is not True:
            raise ValueError("spine_ready must be True")


def build_proposal_audit_spine_contract() -> ProposalAuditSpineContract:
    stages: Tuple[ProposalAuditStage, ...] = (
        "proposal_inspection",
        "audit_inspection",
        "approval_read_model",
        "operator_review",
        "proposal_audit_summary",
        "proposal_audit_preview",
    )

    surfaces = (
        ProposalAuditSurface(
            surface_id="surface_evolution_loop",
            surface_kind="existing_evolution_loop",
            source_path="MAKSIMAR_CORE_LIB/evolution_loop",
            reused_existing_surface=True,
            read_only=True,
            action_execution_allowed=False,
            code_write_allowed=False,
            runtime_mutation_allowed=False,
            surface_ready=True,
        ),
        ProposalAuditSurface(
            surface_id="surface_evolution_debug",
            surface_kind="existing_evolution_debug",
            source_path="MAKSIMAR_CORE_LIB/evolution_debug",
            reused_existing_surface=True,
            read_only=True,
            action_execution_allowed=False,
            code_write_allowed=False,
            runtime_mutation_allowed=False,
            surface_ready=True,
        ),
        ProposalAuditSurface(
            surface_id="surface_security_governance",
            surface_kind="security_governance_doc",
            source_path="docs/security_governance",
            reused_existing_surface=True,
            read_only=True,
            action_execution_allowed=False,
            code_write_allowed=False,
            runtime_mutation_allowed=False,
            surface_ready=True,
        ),
        ProposalAuditSurface(
            surface_id="surface_governed_action_model",
            surface_kind="security_governance_doc",
            source_path="docs/security_governance/governed_action_model",
            reused_existing_surface=True,
            read_only=True,
            action_execution_allowed=False,
            code_write_allowed=False,
            runtime_mutation_allowed=False,
            surface_ready=True,
        ),
        ProposalAuditSurface(
            surface_id="surface_memory_acceptance",
            surface_kind="memory_acceptance_surface",
            source_path="MAKSIMAR_SERVER/MEMORY_ACCEPTANCE",
            reused_existing_surface=True,
            read_only=True,
            action_execution_allowed=False,
            code_write_allowed=False,
            runtime_mutation_allowed=False,
            surface_ready=True,
        ),
        ProposalAuditSurface(
            surface_id="surface_proposal_audit_spine",
            surface_kind="proposal_audit_spine",
            source_path="MAKSIMAR_SERVER/PROPOSAL_AUDIT",
            reused_existing_surface=False,
            read_only=True,
            action_execution_allowed=False,
            code_write_allowed=False,
            runtime_mutation_allowed=False,
            surface_ready=True,
        ),
    )

    return ProposalAuditSpineContract(
        contract_id="proposal_audit_spine_contract_phase_6_2_001",
        roadmap_family="memory_roadmap_v5_1",
        phase_id="PHASE 6.2",
        track_scope="proposal_audit_approval",
        stages=stages,
        surfaces=surfaces,
        existing_surfaces_reused=True,
        proposal_visible=True,
        audit_visible=True,
        approval_visible=True,
        operator_review_required=True,
        approval_granted_by_default=False,
        code_write_allowed=False,
        action_execution_allowed=False,
        sandbox_execution_allowed_now=False,
        self_expansion_allowed_now=False,
        productization_allowed_now=False,
        spine_ready=True,
    )
