from __future__ import annotations

from dataclasses import dataclass
from typing import Literal, Tuple

from MAKSIMAR_SERVER.CLIENT_LEARNING_INPUT.client_metrics_filter_models import (
    build_client_metrics_filter_policy,
)
from MAKSIMAR_SERVER.CLIENT_LEARNING_INPUT.privacy_tenant_boundary_models import (
    build_privacy_tenant_boundary_contract,
)
from MAKSIMAR_SERVER.SELF_EXPANSION_GATE import build_self_expansion_preview


LearningInputKind = Literal[
    "usage_learning_signal",
    "operator_feedback_learning_signal",
    "quality_learning_signal",
    "error_learning_signal",
    "feature_request_learning_signal",
]


@dataclass(frozen=True, slots=True)
class LearningInputItem:
    item_id: str
    input_kind: LearningInputKind
    source_metric_id: str
    source_bound: bool
    tenant_bound: bool
    pii_redacted: bool
    human_review_required: bool
    proposal_route_required: bool
    automatic_training_allowed: bool
    runtime_mutation_allowed: bool
    item_ready: bool

    def __post_init__(self) -> None:
        if not self.item_id:
            raise ValueError("item_id must be non-empty")
        if not self.source_metric_id:
            raise ValueError("source_metric_id must be non-empty")
        if self.source_bound is not True:
            raise ValueError("source_bound must be True")
        if self.tenant_bound is not True:
            raise ValueError("tenant_bound must be True")
        if self.pii_redacted is not True:
            raise ValueError("pii_redacted must be True")
        if self.human_review_required is not True:
            raise ValueError("human_review_required must be True")
        if self.proposal_route_required is not True:
            raise ValueError("proposal_route_required must be True")
        if self.automatic_training_allowed:
            raise ValueError("automatic_training_allowed must be False")
        if self.runtime_mutation_allowed:
            raise ValueError("runtime_mutation_allowed must be False")
        if self.item_ready is not True:
            raise ValueError("item_ready must be True")


@dataclass(frozen=True, slots=True)
class LearningInputPack:
    pack_id: str
    roadmap_family: str
    phase_id: str
    track_scope: str
    items: Tuple[LearningInputItem, ...]
    source_bound: bool
    tenant_boundary_ready: bool
    privacy_boundary_ready: bool
    self_expansion_gate_ready: bool
    proposal_route_required: bool
    human_review_required: bool
    automatic_training_allowed: bool
    direct_model_mutation_allowed: bool
    runtime_mutation_allowed: bool
    productization_allowed_now: bool
    polyglot_model_worker_allowed_next: bool
    pack_ready: bool

    def __post_init__(self) -> None:
        if not self.pack_id:
            raise ValueError("pack_id must be non-empty")
        if self.roadmap_family != "memory_roadmap_v5_1":
            raise ValueError("roadmap_family must be memory_roadmap_v5_1")
        if self.phase_id != "PHASE 6.6":
            raise ValueError("phase_id must be PHASE 6.6")
        if self.track_scope != "client_metrics_learning_input":
            raise ValueError("track_scope must be client_metrics_learning_input")
        if not self.items:
            raise ValueError("items must be non-empty")
        item_ids = {item.item_id for item in self.items}
        if len(item_ids) != len(self.items):
            raise ValueError("item_id values must be unique")
        if self.source_bound is not True:
            raise ValueError("source_bound must be True")
        if self.tenant_boundary_ready is not True:
            raise ValueError("tenant_boundary_ready must be True")
        if self.privacy_boundary_ready is not True:
            raise ValueError("privacy_boundary_ready must be True")
        if self.self_expansion_gate_ready is not True:
            raise ValueError("self_expansion_gate_ready must be True")
        if self.proposal_route_required is not True:
            raise ValueError("proposal_route_required must be True")
        if self.human_review_required is not True:
            raise ValueError("human_review_required must be True")
        if self.automatic_training_allowed:
            raise ValueError("automatic_training_allowed must be False")
        if self.direct_model_mutation_allowed:
            raise ValueError("direct_model_mutation_allowed must be False")
        if self.runtime_mutation_allowed:
            raise ValueError("runtime_mutation_allowed must be False")
        if self.productization_allowed_now:
            raise ValueError("productization_allowed_now must be False")
        if self.polyglot_model_worker_allowed_next is not True:
            raise ValueError("polyglot_model_worker_allowed_next must be True")
        if not all(item.item_ready for item in self.items):
            raise ValueError("all items must be ready")
        if self.pack_ready is not True:
            raise ValueError("pack_ready must be True")


def build_learning_input_pack() -> LearningInputPack:
    filter_policy = build_client_metrics_filter_policy()
    boundary = build_privacy_tenant_boundary_contract()
    self_expansion = build_self_expansion_preview()

    items = tuple(
        LearningInputItem(
            item_id=f"learning_input_{signal.metric_kind}_001",
            input_kind={
                "usage_signal": "usage_learning_signal",
                "operator_feedback": "operator_feedback_learning_signal",
                "quality_signal": "quality_learning_signal",
                "error_signal": "error_learning_signal",
                "latency_signal": "quality_learning_signal",
                "feature_request_signal": "feature_request_learning_signal",
            }[signal.metric_kind],
            source_metric_id=signal.signal_id,
            source_bound=signal.source_bound,
            tenant_bound=signal.tenant_bound,
            pii_redacted=signal.pii_redacted,
            human_review_required=True,
            proposal_route_required=True,
            automatic_training_allowed=False,
            runtime_mutation_allowed=False,
            item_ready=signal.learning_input_allowed,
        )
        for signal in filter_policy.signals
    )

    return LearningInputPack(
        pack_id="learning_input_pack_phase_6_6_001",
        roadmap_family="memory_roadmap_v5_1",
        phase_id="PHASE 6.6",
        track_scope="client_metrics_learning_input",
        items=items,
        source_bound=filter_policy.source_bound_required,
        tenant_boundary_ready=boundary.tenant_isolation_required and boundary.boundary_ready,
        privacy_boundary_ready=boundary.personal_data_redaction_required and boundary.boundary_ready,
        self_expansion_gate_ready=self_expansion["preview_ready"],
        proposal_route_required=True,
        human_review_required=True,
        automatic_training_allowed=False,
        direct_model_mutation_allowed=False,
        runtime_mutation_allowed=False,
        productization_allowed_now=False,
        polyglot_model_worker_allowed_next=True,
        pack_ready=True,
    )
