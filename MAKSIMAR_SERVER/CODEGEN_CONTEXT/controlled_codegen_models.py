from __future__ import annotations

from dataclasses import dataclass
from typing import Literal, Tuple


CodegenStage = Literal[
    "intent_classification",
    "boundary_check",
    "artifact_context",
    "proposal_package",
    "read_summary",
    "operator_preview",
]

CodegenSurfaceKind = Literal[
    "proposal_audit_spine",
    "evolution_loop",
    "evolution_debug",
    "data_plane",
    "artifact_routing",
    "governed_action_docs",
    "controlled_codegen_context",
]


@dataclass(frozen=True, slots=True)
class ControlledCodegenSurface:
    surface_id: str
    surface_kind: CodegenSurfaceKind
    source_path: str
    reused_existing_surface: bool
    read_only: bool
    code_generation_execution_allowed: bool
    direct_core_write_allowed: bool
    deployment_allowed: bool
    sandbox_execution_allowed_now: bool
    runtime_mutation_allowed: bool
    surface_ready: bool

    def __post_init__(self) -> None:
        if not self.surface_id:
            raise ValueError("surface_id must be non-empty")
        if not self.source_path:
            raise ValueError("source_path must be non-empty")
        if self.read_only is not True:
            raise ValueError("read_only must be True")
        if self.code_generation_execution_allowed:
            raise ValueError("code_generation_execution_allowed must be False")
        if self.direct_core_write_allowed:
            raise ValueError("direct_core_write_allowed must be False")
        if self.deployment_allowed:
            raise ValueError("deployment_allowed must be False")
        if self.sandbox_execution_allowed_now:
            raise ValueError("sandbox_execution_allowed_now must be False")
        if self.runtime_mutation_allowed:
            raise ValueError("runtime_mutation_allowed must be False")
        if self.surface_ready is not True:
            raise ValueError("surface_ready must be True")


@dataclass(frozen=True, slots=True)
class ControlledCodegenContextContract:
    contract_id: str
    roadmap_family: str
    phase_id: str
    track_scope: str
    stages: Tuple[CodegenStage, ...]
    surfaces: Tuple[ControlledCodegenSurface, ...]
    existing_surfaces_reused: bool
    intent_models_ready: bool
    boundary_models_ready: bool
    artifact_context_ready: bool
    proposal_package_ready: bool
    read_summary_ready: bool
    operator_preview_required: bool
    direct_core_write_allowed: bool
    deployment_allowed: bool
    sandbox_execution_allowed_now: bool
    self_expansion_allowed_now: bool
    productization_allowed_now: bool
    controlled_codegen_context_ready: bool

    def __post_init__(self) -> None:
        if not self.contract_id:
            raise ValueError("contract_id must be non-empty")
        if self.roadmap_family != "memory_roadmap_v5_1":
            raise ValueError("roadmap_family must be memory_roadmap_v5_1")
        if self.phase_id != "PHASE 6.3":
            raise ValueError("phase_id must be PHASE 6.3")
        if self.track_scope != "controlled_codegen_context":
            raise ValueError("track_scope must be controlled_codegen_context")
        required_stages = {
            "intent_classification",
            "boundary_check",
            "artifact_context",
            "proposal_package",
            "read_summary",
            "operator_preview",
        }
        if set(self.stages) != required_stages:
            raise ValueError("stages must match controlled codegen context stages")
        if not self.surfaces:
            raise ValueError("surfaces must be non-empty")
        surface_ids = {surface.surface_id for surface in self.surfaces}
        if len(surface_ids) != len(self.surfaces):
            raise ValueError("surface_id values must be unique")
        if self.existing_surfaces_reused is not True:
            raise ValueError("existing_surfaces_reused must be True")
        if self.intent_models_ready is not True:
            raise ValueError("intent_models_ready must be True")
        if self.boundary_models_ready is not True:
            raise ValueError("boundary_models_ready must be True")
        if self.artifact_context_ready is not True:
            raise ValueError("artifact_context_ready must be True")
        if self.proposal_package_ready is not True:
            raise ValueError("proposal_package_ready must be True")
        if self.read_summary_ready is not True:
            raise ValueError("read_summary_ready must be True")
        if self.operator_preview_required is not True:
            raise ValueError("operator_preview_required must be True")
        if self.direct_core_write_allowed:
            raise ValueError("direct_core_write_allowed must be False")
        if self.deployment_allowed:
            raise ValueError("deployment_allowed must be False")
        if self.sandbox_execution_allowed_now:
            raise ValueError("sandbox_execution_allowed_now must be False")
        if self.self_expansion_allowed_now:
            raise ValueError("self_expansion_allowed_now must be False")
        if self.productization_allowed_now:
            raise ValueError("productization_allowed_now must be False")
        if not all(surface.surface_ready for surface in self.surfaces):
            raise ValueError("all surfaces must be ready")
        if self.controlled_codegen_context_ready is not True:
            raise ValueError("controlled_codegen_context_ready must be True")


def build_controlled_codegen_context_contract() -> ControlledCodegenContextContract:
    stages: Tuple[CodegenStage, ...] = (
        "intent_classification",
        "boundary_check",
        "artifact_context",
        "proposal_package",
        "read_summary",
        "operator_preview",
    )

    surfaces = (
        ControlledCodegenSurface(
            surface_id="surface_proposal_audit_spine",
            surface_kind="proposal_audit_spine",
            source_path="MAKSIMAR_SERVER/PROPOSAL_AUDIT",
            reused_existing_surface=True,
            read_only=True,
            code_generation_execution_allowed=False,
            direct_core_write_allowed=False,
            deployment_allowed=False,
            sandbox_execution_allowed_now=False,
            runtime_mutation_allowed=False,
            surface_ready=True,
        ),
        ControlledCodegenSurface(
            surface_id="surface_evolution_loop",
            surface_kind="evolution_loop",
            source_path="MAKSIMAR_CORE_LIB/evolution_loop",
            reused_existing_surface=True,
            read_only=True,
            code_generation_execution_allowed=False,
            direct_core_write_allowed=False,
            deployment_allowed=False,
            sandbox_execution_allowed_now=False,
            runtime_mutation_allowed=False,
            surface_ready=True,
        ),
        ControlledCodegenSurface(
            surface_id="surface_evolution_debug",
            surface_kind="evolution_debug",
            source_path="MAKSIMAR_CORE_LIB/evolution_debug",
            reused_existing_surface=True,
            read_only=True,
            code_generation_execution_allowed=False,
            direct_core_write_allowed=False,
            deployment_allowed=False,
            sandbox_execution_allowed_now=False,
            runtime_mutation_allowed=False,
            surface_ready=True,
        ),
        ControlledCodegenSurface(
            surface_id="surface_data_plane",
            surface_kind="data_plane",
            source_path="MAKSIMAR_CORE_LIB/data_plane",
            reused_existing_surface=True,
            read_only=True,
            code_generation_execution_allowed=False,
            direct_core_write_allowed=False,
            deployment_allowed=False,
            sandbox_execution_allowed_now=False,
            runtime_mutation_allowed=False,
            surface_ready=True,
        ),
        ControlledCodegenSurface(
            surface_id="surface_artifact_routing",
            surface_kind="artifact_routing",
            source_path="MAKSIMAR_SERVER/EXECUTION_CONTROL/artifact_routing",
            reused_existing_surface=True,
            read_only=True,
            code_generation_execution_allowed=False,
            direct_core_write_allowed=False,
            deployment_allowed=False,
            sandbox_execution_allowed_now=False,
            runtime_mutation_allowed=False,
            surface_ready=True,
        ),
        ControlledCodegenSurface(
            surface_id="surface_governed_action_docs",
            surface_kind="governed_action_docs",
            source_path="docs/security_governance/governed_action_model",
            reused_existing_surface=True,
            read_only=True,
            code_generation_execution_allowed=False,
            direct_core_write_allowed=False,
            deployment_allowed=False,
            sandbox_execution_allowed_now=False,
            runtime_mutation_allowed=False,
            surface_ready=True,
        ),
        ControlledCodegenSurface(
            surface_id="surface_controlled_codegen_context",
            surface_kind="controlled_codegen_context",
            source_path="MAKSIMAR_SERVER/CODEGEN_CONTEXT",
            reused_existing_surface=False,
            read_only=True,
            code_generation_execution_allowed=False,
            direct_core_write_allowed=False,
            deployment_allowed=False,
            sandbox_execution_allowed_now=False,
            runtime_mutation_allowed=False,
            surface_ready=True,
        ),
    )

    return ControlledCodegenContextContract(
        contract_id="controlled_codegen_context_contract_phase_6_3_001",
        roadmap_family="memory_roadmap_v5_1",
        phase_id="PHASE 6.3",
        track_scope="controlled_codegen_context",
        stages=stages,
        surfaces=surfaces,
        existing_surfaces_reused=True,
        intent_models_ready=True,
        boundary_models_ready=True,
        artifact_context_ready=True,
        proposal_package_ready=True,
        read_summary_ready=True,
        operator_preview_required=True,
        direct_core_write_allowed=False,
        deployment_allowed=False,
        sandbox_execution_allowed_now=False,
        self_expansion_allowed_now=False,
        productization_allowed_now=False,
        controlled_codegen_context_ready=True,
    )
