from __future__ import annotations

from dataclasses import dataclass
from typing import Literal, Tuple


SandboxReviewStage = Literal[
    "sandbox_binding",
    "sandbox_result_read",
    "simulation_result_read",
    "evaluation_result_read",
    "owner_review_package",
    "owner_review_preview",
]

SandboxReviewSurfaceKind = Literal[
    "controlled_codegen_context",
    "proposal_audit_spine",
    "evolution_debug_sandbox",
    "simulation_integration",
    "evaluation_integration",
    "oob_dashboard_review_contracts",
    "artifact_routing",
    "sandbox_review",
]


@dataclass(frozen=True, slots=True)
class SandboxReviewSurface:
    surface_id: str
    surface_kind: SandboxReviewSurfaceKind
    source_path: str
    reused_existing_surface: bool
    read_only: bool
    sandbox_execution_started_here: bool
    simulation_execution_started_here: bool
    direct_core_write_allowed: bool
    deployment_allowed: bool
    auto_apply_allowed: bool
    runtime_mutation_allowed: bool
    surface_ready: bool

    def __post_init__(self) -> None:
        if not self.surface_id:
            raise ValueError("surface_id must be non-empty")
        if not self.source_path:
            raise ValueError("source_path must be non-empty")
        if self.read_only is not True:
            raise ValueError("read_only must be True")
        if self.sandbox_execution_started_here:
            raise ValueError("sandbox_execution_started_here must be False")
        if self.simulation_execution_started_here:
            raise ValueError("simulation_execution_started_here must be False")
        if self.direct_core_write_allowed:
            raise ValueError("direct_core_write_allowed must be False")
        if self.deployment_allowed:
            raise ValueError("deployment_allowed must be False")
        if self.auto_apply_allowed:
            raise ValueError("auto_apply_allowed must be False")
        if self.runtime_mutation_allowed:
            raise ValueError("runtime_mutation_allowed must be False")
        if self.surface_ready is not True:
            raise ValueError("surface_ready must be True")


@dataclass(frozen=True, slots=True)
class SandboxReviewContract:
    contract_id: str
    roadmap_family: str
    phase_id: str
    track_scope: str
    stages: Tuple[SandboxReviewStage, ...]
    surfaces: Tuple[SandboxReviewSurface, ...]
    existing_surfaces_reused: bool
    sandbox_binding_ready: bool
    sandbox_result_reader_ready: bool
    simulation_result_reader_ready: bool
    evaluation_result_reader_ready: bool
    owner_review_package_ready: bool
    owner_review_required: bool
    owner_approval_required: bool
    owner_approval_granted_by_default: bool
    direct_core_write_allowed: bool
    deployment_allowed: bool
    auto_apply_allowed: bool
    self_expansion_allowed_now: bool
    productization_allowed_now: bool
    sandbox_review_ready: bool

    def __post_init__(self) -> None:
        if not self.contract_id:
            raise ValueError("contract_id must be non-empty")
        if self.roadmap_family != "memory_roadmap_v5_1":
            raise ValueError("roadmap_family must be memory_roadmap_v5_1")
        if self.phase_id != "PHASE 6.4":
            raise ValueError("phase_id must be PHASE 6.4")
        if self.track_scope != "sandbox_simulation_owner_review":
            raise ValueError("track_scope must be sandbox_simulation_owner_review")
        required_stages = {
            "sandbox_binding",
            "sandbox_result_read",
            "simulation_result_read",
            "evaluation_result_read",
            "owner_review_package",
            "owner_review_preview",
        }
        if set(self.stages) != required_stages:
            raise ValueError("stages must match sandbox/simulation/owner review stages")
        if not self.surfaces:
            raise ValueError("surfaces must be non-empty")
        surface_ids = {surface.surface_id for surface in self.surfaces}
        if len(surface_ids) != len(self.surfaces):
            raise ValueError("surface_id values must be unique")
        if self.existing_surfaces_reused is not True:
            raise ValueError("existing_surfaces_reused must be True")
        if self.sandbox_binding_ready is not True:
            raise ValueError("sandbox_binding_ready must be True")
        if self.sandbox_result_reader_ready is not True:
            raise ValueError("sandbox_result_reader_ready must be True")
        if self.simulation_result_reader_ready is not True:
            raise ValueError("simulation_result_reader_ready must be True")
        if self.evaluation_result_reader_ready is not True:
            raise ValueError("evaluation_result_reader_ready must be True")
        if self.owner_review_package_ready is not True:
            raise ValueError("owner_review_package_ready must be True")
        if self.owner_review_required is not True:
            raise ValueError("owner_review_required must be True")
        if self.owner_approval_required is not True:
            raise ValueError("owner_approval_required must be True")
        if self.owner_approval_granted_by_default:
            raise ValueError("owner_approval_granted_by_default must be False")
        if self.direct_core_write_allowed:
            raise ValueError("direct_core_write_allowed must be False")
        if self.deployment_allowed:
            raise ValueError("deployment_allowed must be False")
        if self.auto_apply_allowed:
            raise ValueError("auto_apply_allowed must be False")
        if self.self_expansion_allowed_now:
            raise ValueError("self_expansion_allowed_now must be False")
        if self.productization_allowed_now:
            raise ValueError("productization_allowed_now must be False")
        if not all(surface.surface_ready for surface in self.surfaces):
            raise ValueError("all surfaces must be ready")
        if self.sandbox_review_ready is not True:
            raise ValueError("sandbox_review_ready must be True")


def build_sandbox_review_contract() -> SandboxReviewContract:
    stages: Tuple[SandboxReviewStage, ...] = (
        "sandbox_binding",
        "sandbox_result_read",
        "simulation_result_read",
        "evaluation_result_read",
        "owner_review_package",
        "owner_review_preview",
    )

    surfaces = (
        SandboxReviewSurface(
            surface_id="surface_controlled_codegen_context",
            surface_kind="controlled_codegen_context",
            source_path="MAKSIMAR_SERVER/CODEGEN_CONTEXT",
            reused_existing_surface=True,
            read_only=True,
            sandbox_execution_started_here=False,
            simulation_execution_started_here=False,
            direct_core_write_allowed=False,
            deployment_allowed=False,
            auto_apply_allowed=False,
            runtime_mutation_allowed=False,
            surface_ready=True,
        ),
        SandboxReviewSurface(
            surface_id="surface_proposal_audit_spine",
            surface_kind="proposal_audit_spine",
            source_path="MAKSIMAR_SERVER/PROPOSAL_AUDIT",
            reused_existing_surface=True,
            read_only=True,
            sandbox_execution_started_here=False,
            simulation_execution_started_here=False,
            direct_core_write_allowed=False,
            deployment_allowed=False,
            auto_apply_allowed=False,
            runtime_mutation_allowed=False,
            surface_ready=True,
        ),
        SandboxReviewSurface(
            surface_id="surface_evolution_debug_sandbox",
            surface_kind="evolution_debug_sandbox",
            source_path="MAKSIMAR_CORE_LIB/evolution_debug",
            reused_existing_surface=True,
            read_only=True,
            sandbox_execution_started_here=False,
            simulation_execution_started_here=False,
            direct_core_write_allowed=False,
            deployment_allowed=False,
            auto_apply_allowed=False,
            runtime_mutation_allowed=False,
            surface_ready=True,
        ),
        SandboxReviewSurface(
            surface_id="surface_simulation_integration",
            surface_kind="simulation_integration",
            source_path="MAKSIMAR_CORE_LIB/simulation_integration",
            reused_existing_surface=True,
            read_only=True,
            sandbox_execution_started_here=False,
            simulation_execution_started_here=False,
            direct_core_write_allowed=False,
            deployment_allowed=False,
            auto_apply_allowed=False,
            runtime_mutation_allowed=False,
            surface_ready=True,
        ),
        SandboxReviewSurface(
            surface_id="surface_evaluation_integration",
            surface_kind="evaluation_integration",
            source_path="MAKSIMAR_CORE_LIB/evaluation_integration",
            reused_existing_surface=True,
            read_only=True,
            sandbox_execution_started_here=False,
            simulation_execution_started_here=False,
            direct_core_write_allowed=False,
            deployment_allowed=False,
            auto_apply_allowed=False,
            runtime_mutation_allowed=False,
            surface_ready=True,
        ),
        SandboxReviewSurface(
            surface_id="surface_oob_review_contracts",
            surface_kind="oob_dashboard_review_contracts",
            source_path="MAKSIMAR_CORE_LIB/oob_dashboard",
            reused_existing_surface=True,
            read_only=True,
            sandbox_execution_started_here=False,
            simulation_execution_started_here=False,
            direct_core_write_allowed=False,
            deployment_allowed=False,
            auto_apply_allowed=False,
            runtime_mutation_allowed=False,
            surface_ready=True,
        ),
        SandboxReviewSurface(
            surface_id="surface_artifact_routing",
            surface_kind="artifact_routing",
            source_path="MAKSIMAR_SERVER/EXECUTION_CONTROL/artifact_routing",
            reused_existing_surface=True,
            read_only=True,
            sandbox_execution_started_here=False,
            simulation_execution_started_here=False,
            direct_core_write_allowed=False,
            deployment_allowed=False,
            auto_apply_allowed=False,
            runtime_mutation_allowed=False,
            surface_ready=True,
        ),
        SandboxReviewSurface(
            surface_id="surface_sandbox_review",
            surface_kind="sandbox_review",
            source_path="MAKSIMAR_SERVER/SANDBOX_REVIEW",
            reused_existing_surface=False,
            read_only=True,
            sandbox_execution_started_here=False,
            simulation_execution_started_here=False,
            direct_core_write_allowed=False,
            deployment_allowed=False,
            auto_apply_allowed=False,
            runtime_mutation_allowed=False,
            surface_ready=True,
        ),
    )

    return SandboxReviewContract(
        contract_id="sandbox_review_contract_phase_6_4_001",
        roadmap_family="memory_roadmap_v5_1",
        phase_id="PHASE 6.4",
        track_scope="sandbox_simulation_owner_review",
        stages=stages,
        surfaces=surfaces,
        existing_surfaces_reused=True,
        sandbox_binding_ready=True,
        sandbox_result_reader_ready=True,
        simulation_result_reader_ready=True,
        evaluation_result_reader_ready=True,
        owner_review_package_ready=True,
        owner_review_required=True,
        owner_approval_required=True,
        owner_approval_granted_by_default=False,
        direct_core_write_allowed=False,
        deployment_allowed=False,
        auto_apply_allowed=False,
        self_expansion_allowed_now=False,
        productization_allowed_now=False,
        sandbox_review_ready=True,
    )
