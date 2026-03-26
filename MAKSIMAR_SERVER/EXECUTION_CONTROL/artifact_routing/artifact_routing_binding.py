from __future__ import annotations

from dataclasses import dataclass

from MAKSIMAR_CORE_LIB.artifact_reference_models import (
    ArtifactReferenceEntry,
)
from MAKSIMAR_SERVER.CONTROL_PLANE.payload_classification import (
    build_server_payload_classification_contract,
)
from MAKSIMAR_SERVER.EXECUTION_CONTROL.artifact_routing.artifact_routing_models import (
    ArtifactRoutingBindingContract,
    ArtifactRoutingBindingEntry,
)


@dataclass(frozen=True, slots=True)
class _ArtifactRoutingInput:
    """Internal routing input metadata for classified payloads."""

    request_id: str
    artifact_ref: str
    owner_task_id: str
    artifact_type: str
    storage_policy: str
    integrity_policy: str


def build_artifact_routing_binding_contract() -> ArtifactRoutingBindingContract:
    """Build artifact routing binding contract from server-side payload classification."""
    classification = build_server_payload_classification_contract()

    routing_inputs = {
        "payload_req_001": _ArtifactRoutingInput(
            request_id="payload_req_001",
            artifact_ref="",
            owner_task_id="",
            artifact_type="",
            storage_policy="ephemeral",
            integrity_policy="checksum_required",
        ),
        "payload_req_002": _ArtifactRoutingInput(
            request_id="payload_req_002",
            artifact_ref="",
            owner_task_id="",
            artifact_type="",
            storage_policy="ephemeral",
            integrity_policy="checksum_required",
        ),
        "payload_req_003": _ArtifactRoutingInput(
            request_id="payload_req_003",
            artifact_ref="artifact://simulation/output_001",
            owner_task_id="task_art_001",
            artifact_type="simulation_output",
            storage_policy="retained",
            integrity_policy="checksum_required",
        ),
    }

    entries = []
    for classified in classification.entries:
        routing_input = routing_inputs[classified.request_id]

        if classified.route_target == "data_plane":
            if not routing_input.artifact_ref or not routing_input.owner_task_id:
                entries.append(
                    ArtifactRoutingBindingEntry(
                        request_id=classified.request_id,
                        detected_payload_class=classified.detected_payload_class,
                        route_target=classified.route_target,
                        artifact_ref=routing_input.artifact_ref,
                        owner_task_id=routing_input.owner_task_id,
                        binding_status="rejected",
                        artifact_declared=False,
                        binding_reason="artifact_metadata_missing",
                    )
                )
                continue

            artifact_reference = ArtifactReferenceEntry(
                artifact_ref=routing_input.artifact_ref,
                artifact_type=routing_input.artifact_type,
                artifact_size_kb=classified.payload_size_kb,
                owner_task_id=routing_input.owner_task_id,
                storage_policy=routing_input.storage_policy,  # type: ignore[arg-type]
                integrity_policy=routing_input.integrity_policy,  # type: ignore[arg-type]
            )

            entries.append(
                ArtifactRoutingBindingEntry(
                    request_id=classified.request_id,
                    detected_payload_class=classified.detected_payload_class,
                    route_target=classified.route_target,
                    artifact_ref=artifact_reference.artifact_ref,
                    owner_task_id=artifact_reference.owner_task_id,
                    binding_status="bound_to_data_plane",
                    artifact_declared=True,
                    binding_reason="artifact_reference_bound",
                )
            )
            continue

        entries.append(
            ArtifactRoutingBindingEntry(
                request_id=classified.request_id,
                detected_payload_class=classified.detected_payload_class,
                route_target=classified.route_target,
                artifact_ref="",
                owner_task_id="",
                binding_status="inline_control_route",
                artifact_declared=False,
                binding_reason="inline_control_payload",
            )
        )

    return ArtifactRoutingBindingContract(
        total_entries=len(entries),
        entries=tuple(entries),
    )
