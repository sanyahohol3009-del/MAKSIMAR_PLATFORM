from __future__ import annotations

from dataclasses import dataclass

from MAKSIMAR_CORE_LIB.payload_policy_models import (
    PayloadClass,
)
from MAKSIMAR_CORE_LIB.payload_routing_contract import (
    build_payload_routing_contract,
)
from MAKSIMAR_CORE_LIB.payload_validators import (
    validate_payload_policy,
)


@dataclass(frozen=True, slots=True)
class BuiltPayloadEnvelope:
    """Canonical payload envelope derived from routing policy."""

    payload_class: PayloadClass
    route_target: str
    payload_size_kb: int
    artifact_ref: str
    owner_task_id: str
    valid: bool
    validation_reason: str


def build_payload_envelope(
    *,
    payload_class: PayloadClass,
    payload_size_kb: int,
    artifact_ref: str = "",
    owner_task_id: str = "",
) -> BuiltPayloadEnvelope:
    """Build validated payload envelope from canonical routing policy."""
    routing_contract = build_payload_routing_contract()

    validation = validate_payload_policy(
        payload_class=payload_class,
        payload_size_kb=payload_size_kb,
        artifact_ref=artifact_ref,
        owner_task_id=owner_task_id,
    )

    route_target = next(
        rule.route_target
        for rule in routing_contract.rules
        if rule.payload_class == payload_class
    )

    return BuiltPayloadEnvelope(
        payload_class=payload_class,
        route_target=route_target,
        payload_size_kb=payload_size_kb,
        artifact_ref=artifact_ref,
        owner_task_id=owner_task_id,
        valid=validation.valid,
        validation_reason=validation.reason,
    )
