from __future__ import annotations

import re
from dataclasses import dataclass
from typing import Literal

from MAKSIMAR_CORE_LIB.payload_routing_contract import (
    build_payload_routing_contract,
)
from MAKSIMAR_CORE_LIB.validation_policy import (
    build_validation_payload_class_contract,
)


PayloadClass = Literal[
    "small_control",
    "medium_contract",
    "heavy_artifact",
]

PayloadRouteTarget = Literal[
    "control_plane",
    "data_plane",
]

ValidationTier = Literal[
    "L1_HEADER",
    "L2_SCHEMA",
    "L3_DEEP",
]

ArtifactReferenceRequirement = Literal[
    "forbidden",
    "optional",
    "required",
]

PayloadPolicyStatus = Literal[
    "hardened",
]


_POLICY_ENTRY_ID_PATTERN = re.compile(r"^payloadpolicy_[a-z][a-z0-9_]*$")
_PAYLOAD_CLASS_PATTERN = re.compile(r"^[a-z][a-z0-9_]*$")


@dataclass(frozen=True, slots=True)
class PayloadPolicyHardeningEntry:
    """Canonical hardened payload policy entry."""

    policy_entry_id: str
    payload_class: PayloadClass
    route_target: PayloadRouteTarget
    inline_payload_allowed: bool
    artifact_reference_requirement: ArtifactReferenceRequirement
    minimum_validation_tier: ValidationTier
    deep_validation_required_for_default_flow: bool
    control_plane_allowed: bool
    data_plane_required: bool
    split_valid: bool
    policy_status: PayloadPolicyStatus
    description: str

    def __post_init__(self) -> None:
        """Validate payload policy hardening invariants."""
        if not _POLICY_ENTRY_ID_PATTERN.fullmatch(self.policy_entry_id):
            raise ValueError(f"Invalid policy_entry_id: {self.policy_entry_id}")

        if not _PAYLOAD_CLASS_PATTERN.fullmatch(self.payload_class):
            raise ValueError(f"Invalid payload_class: {self.payload_class}")

        if not self.description.strip():
            raise ValueError(
                f"description must not be empty for {self.policy_entry_id}"
            )

        if not self.split_valid:
            raise ValueError(
                f"payload policy entry must be split-valid: {self.policy_entry_id}"
            )

        if self.policy_status != "hardened":
            raise ValueError(
                f"payload policy entry must be hardened: {self.policy_entry_id}"
            )

        if self.payload_class == "small_control":
            if self.route_target != "control_plane":
                raise ValueError(
                    f"small_control must route to control_plane: {self.policy_entry_id}"
                )
            if not self.inline_payload_allowed:
                raise ValueError(
                    f"small_control must allow inline payload: {self.policy_entry_id}"
                )
            if self.artifact_reference_requirement != "forbidden":
                raise ValueError(
                    f"small_control must forbid artifact references: {self.policy_entry_id}"
                )
            if self.minimum_validation_tier != "L1_HEADER":
                raise ValueError(
                    f"small_control must use L1_HEADER: {self.policy_entry_id}"
                )
            if self.deep_validation_required_for_default_flow:
                raise ValueError(
                    f"small_control must not require deep validation by default: {self.policy_entry_id}"
                )
            if not self.control_plane_allowed:
                raise ValueError(
                    f"small_control must allow control_plane: {self.policy_entry_id}"
                )
            if self.data_plane_required:
                raise ValueError(
                    f"small_control must not require data_plane: {self.policy_entry_id}"
                )

        if self.payload_class == "medium_contract":
            if self.route_target != "control_plane":
                raise ValueError(
                    f"medium_contract must route to control_plane: {self.policy_entry_id}"
                )
            if not self.inline_payload_allowed:
                raise ValueError(
                    f"medium_contract must allow inline payload: {self.policy_entry_id}"
                )
            if self.artifact_reference_requirement != "optional":
                raise ValueError(
                    f"medium_contract must use optional artifact reference: {self.policy_entry_id}"
                )
            if self.minimum_validation_tier != "L2_SCHEMA":
                raise ValueError(
                    f"medium_contract must use L2_SCHEMA: {self.policy_entry_id}"
                )
            if self.deep_validation_required_for_default_flow:
                raise ValueError(
                    f"medium_contract must not require deep validation by default: {self.policy_entry_id}"
                )
            if not self.control_plane_allowed:
                raise ValueError(
                    f"medium_contract must allow control_plane: {self.policy_entry_id}"
                )
            if self.data_plane_required:
                raise ValueError(
                    f"medium_contract must not require data_plane: {self.policy_entry_id}"
                )

        if self.payload_class == "heavy_artifact":
            if self.route_target != "data_plane":
                raise ValueError(
                    f"heavy_artifact must route to data_plane: {self.policy_entry_id}"
                )
            if self.inline_payload_allowed:
                raise ValueError(
                    f"heavy_artifact must not allow inline payload: {self.policy_entry_id}"
                )
            if self.artifact_reference_requirement != "required":
                raise ValueError(
                    f"heavy_artifact must require artifact reference: {self.policy_entry_id}"
                )
            if self.minimum_validation_tier != "L2_SCHEMA":
                raise ValueError(
                    f"heavy_artifact must use L2_SCHEMA minimum tier: {self.policy_entry_id}"
                )
            if not self.deep_validation_required_for_default_flow:
                raise ValueError(
                    f"heavy_artifact must require deep validation by default: {self.policy_entry_id}"
                )
            if self.control_plane_allowed:
                raise ValueError(
                    f"heavy_artifact must not allow control_plane transport: {self.policy_entry_id}"
                )
            if not self.data_plane_required:
                raise ValueError(
                    f"heavy_artifact must require data_plane: {self.policy_entry_id}"
                )


@dataclass(frozen=True, slots=True)
class PayloadPolicyHardeningContract:
    """Unified hardened payload policy contract."""

    total_entries: int
    control_plane_entries: int
    data_plane_entries: int
    deep_validation_entries: int
    hardened_entries: int
    entries: tuple[PayloadPolicyHardeningEntry, ...]

    def __post_init__(self) -> None:
        """Validate hardened payload policy contract invariants."""
        if self.total_entries != len(self.entries):
            raise ValueError("total_entries must match entries length")

        control_plane_entries = sum(
            1 for entry in self.entries if entry.route_target == "control_plane"
        )
        data_plane_entries = sum(
            1 for entry in self.entries if entry.route_target == "data_plane"
        )
        deep_validation_entries = sum(
            1
            for entry in self.entries
            if entry.deep_validation_required_for_default_flow
        )
        hardened_entries = sum(
            1 for entry in self.entries if entry.policy_status == "hardened"
        )

        if self.control_plane_entries != control_plane_entries:
            raise ValueError("control_plane_entries must match computed count")

        if self.data_plane_entries != data_plane_entries:
            raise ValueError("data_plane_entries must match computed count")

        if self.deep_validation_entries != deep_validation_entries:
            raise ValueError("deep_validation_entries must match computed count")

        if self.hardened_entries != hardened_entries:
            raise ValueError("hardened_entries must match computed count")

        payload_classes = tuple(entry.payload_class for entry in self.entries)
        policy_entry_ids = tuple(entry.policy_entry_id for entry in self.entries)

        if len(set(payload_classes)) != len(payload_classes):
            raise ValueError("Duplicate payload_class values detected")

        if len(set(policy_entry_ids)) != len(policy_entry_ids):
            raise ValueError("Duplicate policy_entry_id values detected")


def build_payload_policy_hardening_contract() -> PayloadPolicyHardeningContract:
    """Build canonical hardened payload policy contract."""
    routing_contract = build_payload_routing_contract()
    validation_contract = build_validation_payload_class_contract()

    routing_classes = {entry.payload_class for entry in routing_contract.rules}
    validation_classes = {
        entry.payload_class for entry in validation_contract.payload_classes
    }

    required_classes = {"small_control", "medium_contract", "heavy_artifact"}

    missing_routing = required_classes - routing_classes
    if missing_routing:
        raise ValueError(
            f"Missing payload classes in routing contract: {sorted(missing_routing)}"
        )

    missing_validation = required_classes - validation_classes
    if missing_validation:
        raise ValueError(
            f"Missing payload classes in validation contract: {sorted(missing_validation)}"
        )

    entries = (
        PayloadPolicyHardeningEntry(
            policy_entry_id="payloadpolicy_small_control_001",
            payload_class="small_control",
            route_target="control_plane",
            inline_payload_allowed=True,
            artifact_reference_requirement="forbidden",
            minimum_validation_tier="L1_HEADER",
            deep_validation_required_for_default_flow=False,
            control_plane_allowed=True,
            data_plane_required=False,
            split_valid=True,
            policy_status="hardened",
            description="Hardened payload policy for small control payloads.",
        ),
        PayloadPolicyHardeningEntry(
            policy_entry_id="payloadpolicy_medium_contract_001",
            payload_class="medium_contract",
            route_target="control_plane",
            inline_payload_allowed=True,
            artifact_reference_requirement="optional",
            minimum_validation_tier="L2_SCHEMA",
            deep_validation_required_for_default_flow=False,
            control_plane_allowed=True,
            data_plane_required=False,
            split_valid=True,
            policy_status="hardened",
            description="Hardened payload policy for medium contract payloads.",
        ),
        PayloadPolicyHardeningEntry(
            policy_entry_id="payloadpolicy_heavy_artifact_001",
            payload_class="heavy_artifact",
            route_target="data_plane",
            inline_payload_allowed=False,
            artifact_reference_requirement="required",
            minimum_validation_tier="L2_SCHEMA",
            deep_validation_required_for_default_flow=True,
            control_plane_allowed=False,
            data_plane_required=True,
            split_valid=True,
            policy_status="hardened",
            description="Hardened payload policy for heavy artifact payloads.",
        ),
    )

    control_plane_entries = sum(
        1 for entry in entries if entry.route_target == "control_plane"
    )
    data_plane_entries = sum(
        1 for entry in entries if entry.route_target == "data_plane"
    )
    deep_validation_entries = sum(
        1
        for entry in entries
        if entry.deep_validation_required_for_default_flow
    )
    hardened_entries = sum(
        1 for entry in entries if entry.policy_status == "hardened"
    )

    return PayloadPolicyHardeningContract(
        total_entries=len(entries),
        control_plane_entries=control_plane_entries,
        data_plane_entries=data_plane_entries,
        deep_validation_entries=deep_validation_entries,
        hardened_entries=hardened_entries,
        entries=entries,
    )
