from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
from typing import Dict, Literal, Tuple

from MAKSIMAR_SERVER.CLIENT_LEARNING_INPUT import build_client_learning_input_preview
from MAKSIMAR_SERVER.POLYGLOT_MODEL_WORKER_BRIDGE.language_bridge_models import (
    build_language_bridge_contract,
)


PROJECT_ROOT = Path(__file__).resolve().parents[2]

ModelWorkerRole = Literal[
    "analysis_worker",
    "codegen_worker",
    "test_worker",
    "review_worker",
    "documentation_worker",
]

REQUIRED_MODEL_WORKER_SURFACES: Tuple[str, ...] = (
    "MAKSIMAR_CORE_LIB/ai_services/service_models.py",
    "MAKSIMAR_CORE_LIB/ai_services/query_models.py",
    "MAKSIMAR_CORE_LIB/real_ai_services_model_adapters/__init__.py",
    "MAKSIMAR_CORE_LIB/execution_control/router_models.py",
    "MAKSIMAR_CORE_LIB/node_roles/workload_models.py",
    "MAKSIMAR_SERVER/EXECUTION_CONTROL/artifact_routing/artifact_routing_binding.py",
    "MAKSIMAR_SERVER/CLIENT_LEARNING_INPUT/client_learning_input_preview_builder.py",
)


@dataclass(frozen=True, slots=True)
class ModelWorkerBridgeEntry:
    bridge_id: str
    worker_role: ModelWorkerRole
    model_routing_required: bool
    worker_boundary_required: bool
    artifact_ref_required: bool
    build_test_required: bool
    human_review_required: bool
    direct_model_mutation_allowed: bool
    runtime_mutation_allowed: bool
    deployment_allowed: bool
    productization_allowed_now: bool
    bridge_ready: bool

    def __post_init__(self) -> None:
        if not self.bridge_id:
            raise ValueError("bridge_id must be non-empty")
        if self.model_routing_required is not True:
            raise ValueError("model_routing_required must be True")
        if self.worker_boundary_required is not True:
            raise ValueError("worker_boundary_required must be True")
        if self.artifact_ref_required is not True:
            raise ValueError("artifact_ref_required must be True")
        if self.build_test_required is not True:
            raise ValueError("build_test_required must be True")
        if self.human_review_required is not True:
            raise ValueError("human_review_required must be True")
        if self.direct_model_mutation_allowed:
            raise ValueError("direct_model_mutation_allowed must be False")
        if self.runtime_mutation_allowed:
            raise ValueError("runtime_mutation_allowed must be False")
        if self.deployment_allowed:
            raise ValueError("deployment_allowed must be False")
        if self.productization_allowed_now:
            raise ValueError("productization_allowed_now must be False")
        if self.bridge_ready is not True:
            raise ValueError("bridge_ready must be True")


@dataclass(frozen=True, slots=True)
class ModelWorkerBridgeContract:
    contract_id: str
    bridges: Tuple[ModelWorkerBridgeEntry, ...]
    language_bridge_ready: bool
    client_learning_input_ready: bool
    missing_required_surfaces: Tuple[str, ...]
    model_worker_bridge_models_ready: bool
    build_test_bridge_required: bool
    human_review_required: bool
    direct_model_mutation_allowed: bool
    runtime_mutation_allowed: bool
    deployment_allowed: bool
    productization_allowed_now: bool
    productization_allowed_next: bool

    def __post_init__(self) -> None:
        if not self.contract_id:
            raise ValueError("contract_id must be non-empty")
        if not self.bridges:
            raise ValueError("bridges must be non-empty")
        if self.language_bridge_ready is not True:
            raise ValueError("language_bridge_ready must be True")
        if self.client_learning_input_ready is not True:
            raise ValueError("client_learning_input_ready must be True")
        if self.missing_required_surfaces:
            raise ValueError(f"missing required surfaces: {self.missing_required_surfaces}")
        if self.model_worker_bridge_models_ready is not True:
            raise ValueError("model_worker_bridge_models_ready must be True")
        if self.build_test_bridge_required is not True:
            raise ValueError("build_test_bridge_required must be True")
        if self.human_review_required is not True:
            raise ValueError("human_review_required must be True")
        if self.direct_model_mutation_allowed:
            raise ValueError("direct_model_mutation_allowed must be False")
        if self.runtime_mutation_allowed:
            raise ValueError("runtime_mutation_allowed must be False")
        if self.deployment_allowed:
            raise ValueError("deployment_allowed must be False")
        if self.productization_allowed_now:
            raise ValueError("productization_allowed_now must be False")
        if self.productization_allowed_next is not True:
            raise ValueError("productization_allowed_next must be True")
        if not all(bridge.bridge_ready for bridge in self.bridges):
            raise ValueError("all model worker bridges must be ready")


def _missing(paths: Tuple[str, ...]) -> Tuple[str, ...]:
    return tuple(path for path in paths if not (PROJECT_ROOT / path).exists())


def build_model_worker_bridge_contract() -> ModelWorkerBridgeContract:
    language_bridge = build_language_bridge_contract()
    client_learning = build_client_learning_input_preview()
    missing = _missing(REQUIRED_MODEL_WORKER_SURFACES)

    bridges = (
        ModelWorkerBridgeEntry(
            bridge_id="model_worker_bridge_analysis_001",
            worker_role="analysis_worker",
            model_routing_required=True,
            worker_boundary_required=True,
            artifact_ref_required=True,
            build_test_required=True,
            human_review_required=True,
            direct_model_mutation_allowed=False,
            runtime_mutation_allowed=False,
            deployment_allowed=False,
            productization_allowed_now=False,
            bridge_ready=True,
        ),
        ModelWorkerBridgeEntry(
            bridge_id="model_worker_bridge_codegen_001",
            worker_role="codegen_worker",
            model_routing_required=True,
            worker_boundary_required=True,
            artifact_ref_required=True,
            build_test_required=True,
            human_review_required=True,
            direct_model_mutation_allowed=False,
            runtime_mutation_allowed=False,
            deployment_allowed=False,
            productization_allowed_now=False,
            bridge_ready=True,
        ),
        ModelWorkerBridgeEntry(
            bridge_id="model_worker_bridge_test_001",
            worker_role="test_worker",
            model_routing_required=True,
            worker_boundary_required=True,
            artifact_ref_required=True,
            build_test_required=True,
            human_review_required=True,
            direct_model_mutation_allowed=False,
            runtime_mutation_allowed=False,
            deployment_allowed=False,
            productization_allowed_now=False,
            bridge_ready=True,
        ),
        ModelWorkerBridgeEntry(
            bridge_id="model_worker_bridge_review_001",
            worker_role="review_worker",
            model_routing_required=True,
            worker_boundary_required=True,
            artifact_ref_required=True,
            build_test_required=True,
            human_review_required=True,
            direct_model_mutation_allowed=False,
            runtime_mutation_allowed=False,
            deployment_allowed=False,
            productization_allowed_now=False,
            bridge_ready=True,
        ),
    )

    return ModelWorkerBridgeContract(
        contract_id="model_worker_bridge_contract_phase_6_7_001",
        bridges=bridges,
        language_bridge_ready=language_bridge.language_bridge_models_ready,
        client_learning_input_ready=client_learning["preview_ready"],
        missing_required_surfaces=missing,
        model_worker_bridge_models_ready=missing == (),
        build_test_bridge_required=True,
        human_review_required=True,
        direct_model_mutation_allowed=False,
        runtime_mutation_allowed=False,
        deployment_allowed=False,
        productization_allowed_now=False,
        productization_allowed_next=True,
    )


def build_model_worker_bridge_preview() -> Dict[str, object]:
    contract = build_model_worker_bridge_contract()

    return {
        "preview_id": "model_worker_bridge_preview_phase_6_7_001",
        "preview_ready": contract.model_worker_bridge_models_ready,
        "required_surfaces": REQUIRED_MODEL_WORKER_SURFACES,
        "missing_required_surfaces": contract.missing_required_surfaces,
        "bridge_count": len(contract.bridges),
        "language_bridge_ready": contract.language_bridge_ready,
        "client_learning_input_ready": contract.client_learning_input_ready,
        "build_test_bridge_required": contract.build_test_bridge_required,
        "human_review_required": contract.human_review_required,
        "direct_model_mutation_allowed": contract.direct_model_mutation_allowed,
        "runtime_mutation_allowed": contract.runtime_mutation_allowed,
        "deployment_allowed": contract.deployment_allowed,
        "productization_allowed_now": contract.productization_allowed_now,
        "productization_allowed_next": contract.productization_allowed_next,
    }
