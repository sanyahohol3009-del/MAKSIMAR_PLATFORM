from __future__ import annotations

from dataclasses import dataclass

from MAKSIMAR_CORE_LIB.payload_builders import (
    build_payload_envelope,
)
from MAKSIMAR_CORE_LIB.payload_policy_models import (
    PayloadClass,
    build_payload_class_contract,
)
from MAKSIMAR_SERVER.CONTROL_PLANE.payload_classification.payload_classifier_models import (
    ServerPayloadClassificationContract,
    ServerPayloadClassificationEntry,
)


@dataclass(frozen=True, slots=True)
class _PayloadClassificationInput:
    """Internal server-side payload classification input."""

    request_id: str
    payload_size_kb: int
    artifact_ref: str
    owner_task_id: str


def _detect_payload_class(payload_size_kb: int) -> PayloadClass:
    """Detect payload class by canonical inline size limits."""
    contract = build_payload_class_contract()

    small_limit = next(
        entry.max_inline_size_kb
        for entry in contract.classes
        if entry.payload_class == "small_control"
    )
    medium_limit = next(
        entry.max_inline_size_kb
        for entry in contract.classes
        if entry.payload_class == "medium_contract"
    )

    if payload_size_kb <= small_limit:
        return "small_control"
    if payload_size_kb <= medium_limit:
        return "medium_contract"
    return "heavy_artifact"


def build_server_payload_classification_contract() -> (
    ServerPayloadClassificationContract
):
    """Build server-side payload classification contract."""
    inputs = (
        _PayloadClassificationInput(
            request_id="payload_req_001",
            payload_size_kb=16,
            artifact_ref="",
            owner_task_id="",
        ),
        _PayloadClassificationInput(
            request_id="payload_req_002",
            payload_size_kb=180,
            artifact_ref="",
            owner_task_id="",
        ),
        _PayloadClassificationInput(
            request_id="payload_req_003",
            payload_size_kb=2048,
            artifact_ref="artifact://simulation/output_001",
            owner_task_id="task_art_001",
        ),
    )

    entries = []
    for item in inputs:
        detected_payload_class = _detect_payload_class(item.payload_size_kb)
        built = build_payload_envelope(
            payload_class=detected_payload_class,
            payload_size_kb=item.payload_size_kb,
            artifact_ref=item.artifact_ref,
            owner_task_id=item.owner_task_id,
        )

        entries.append(
            ServerPayloadClassificationEntry(
                request_id=item.request_id,
                payload_size_kb=item.payload_size_kb,
                detected_payload_class=detected_payload_class,
                route_target=built.route_target,
                inline_allowed=built.route_target == "control_plane",
                valid=built.valid,
                classification_reason=built.validation_reason,
            )
        )

    return ServerPayloadClassificationContract(
        total_entries=len(entries),
        entries=tuple(entries),
    )
