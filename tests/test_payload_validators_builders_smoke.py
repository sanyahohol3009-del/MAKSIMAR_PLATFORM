from __future__ import annotations

from MAKSIMAR_CORE_LIB.payload_builders import (
    build_payload_envelope,
)
from MAKSIMAR_CORE_LIB.payload_validators import (
    validate_payload_policy,
)


def test_payload_validator_accepts_small_control() -> None:
    """Payload validator should accept valid small control payload."""
    result = validate_payload_policy(
        payload_class="small_control",
        payload_size_kb=16,
        artifact_ref="",
        owner_task_id="",
    )

    assert result.valid is True
    assert result.route_target == "control_plane"
    assert result.reason == "payload_policy_valid"


def test_payload_validator_rejects_oversized_inline_payload() -> None:
    """Payload validator should reject oversized inline control payload."""
    result = validate_payload_policy(
        payload_class="medium_contract",
        payload_size_kb=300,
        artifact_ref="",
        owner_task_id="",
    )

    assert result.valid is False
    assert result.reason == "payload_exceeds_inline_limit"


def test_payload_builder_enforces_heavy_artifact_requirements() -> None:
    """Payload builder should enforce heavy artifact reference routing."""
    invalid_envelope = build_payload_envelope(
        payload_class="heavy_artifact",
        payload_size_kb=2048,
        artifact_ref="",
        owner_task_id="task_art_001",
    )

    valid_envelope = build_payload_envelope(
        payload_class="heavy_artifact",
        payload_size_kb=2048,
        artifact_ref="artifact://simulation/output_001",
        owner_task_id="task_art_001",
    )

    assert invalid_envelope.valid is False
    assert invalid_envelope.validation_reason == "artifact_reference_required"

    assert valid_envelope.valid is True
    assert valid_envelope.route_target == "data_plane"
    assert valid_envelope.validation_reason == "payload_policy_valid"
