from __future__ import annotations

from dataclasses import dataclass
from typing import Literal

from MAKSIMAR_CORE_LIB.payload_policy_models import (
    PayloadClass,
    PayloadDirection,
    build_payload_class_contract,
)


ArtifactReferenceRequirement = Literal[
    "not_required",
    "required",
]


@dataclass(frozen=True, slots=True)
class PayloadRoutingRule:
    """Canonical payload routing rule derived from payload classes."""

    payload_class: PayloadClass
    route_target: PayloadDirection
    artifact_reference_requirement: ArtifactReferenceRequirement
    owner_task_id_required: bool
    artifact_size_declaration_required: bool
    max_inline_size_kb: int
    description: str


@dataclass(frozen=True, slots=True)
class PayloadRoutingContract:
    """Unified canonical payload routing contract."""

    total_rules: int
    rules: tuple[PayloadRoutingRule, ...]


def build_payload_routing_contract() -> PayloadRoutingContract:
    """Build canonical payload routing contract from payload class policy."""
    payload_classes = build_payload_class_contract()

    rules = tuple(
        PayloadRoutingRule(
            payload_class=entry.payload_class,
            route_target=entry.routing_direction,
            artifact_reference_requirement=(
                "required"
                if entry.embedding_policy == "reference_required"
                else "not_required"
            ),
            owner_task_id_required=(entry.payload_class == "heavy_artifact"),
            artifact_size_declaration_required=(entry.payload_class == "heavy_artifact"),
            max_inline_size_kb=entry.max_inline_size_kb,
            description=entry.description,
        )
        for entry in payload_classes.classes
    )

    return PayloadRoutingContract(
        total_rules=len(rules),
        rules=rules,
    )
