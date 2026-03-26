from __future__ import annotations

from dataclasses import dataclass

from MAKSIMAR_CORE_LIB.payload_policy_models import (
    PayloadClass,
)
from MAKSIMAR_CORE_LIB.payload_routing_contract import (
    PayloadRoutingRule,
    build_payload_routing_contract,
)


@dataclass(frozen=True, slots=True)
class PayloadValidationResult:
    """Validation result for payload routing policy."""

    valid: bool
    payload_class: PayloadClass
    route_target: str
    reason: str


def _find_rule(payload_class: PayloadClass) -> PayloadRoutingRule:
    """Find routing rule for payload class."""
    contract = build_payload_routing_contract()

    for rule in contract.rules:
        if rule.payload_class == payload_class:
            return rule

    raise ValueError(f"Unsupported payload class: {payload_class}")


def validate_payload_policy(
    *,
    payload_class: PayloadClass,
    payload_size_kb: int,
    artifact_ref: str,
    owner_task_id: str,
) -> PayloadValidationResult:
    """Validate payload against canonical payload routing policy."""
    rule = _find_rule(payload_class)

    if payload_size_kb < 0:
        return PayloadValidationResult(
            valid=False,
            payload_class=payload_class,
            route_target=rule.route_target,
            reason="negative_payload_size",
        )

    if (
        rule.max_inline_size_kb > 0
        and payload_size_kb > rule.max_inline_size_kb
        and rule.route_target == "control_plane"
    ):
        return PayloadValidationResult(
            valid=False,
            payload_class=payload_class,
            route_target=rule.route_target,
            reason="payload_exceeds_inline_limit",
        )

    if rule.artifact_reference_requirement == "required" and not artifact_ref:
        return PayloadValidationResult(
            valid=False,
            payload_class=payload_class,
            route_target=rule.route_target,
            reason="artifact_reference_required",
        )

    if rule.owner_task_id_required and not owner_task_id:
        return PayloadValidationResult(
            valid=False,
            payload_class=payload_class,
            route_target=rule.route_target,
            reason="owner_task_id_required",
        )

    return PayloadValidationResult(
        valid=True,
        payload_class=payload_class,
        route_target=rule.route_target,
        reason="payload_policy_valid",
    )
