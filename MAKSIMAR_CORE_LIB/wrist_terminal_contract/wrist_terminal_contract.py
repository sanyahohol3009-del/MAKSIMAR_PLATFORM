from __future__ import annotations

import re
from dataclasses import dataclass
from typing import Literal

from MAKSIMAR_CORE_LIB.node_runtime_split import (
    build_node_runtime_split_contract,
)
from MAKSIMAR_CORE_LIB.optics_light_field_engine import (
    build_optics_light_field_engine_contract,
)


WristTerminalId = Literal[
    "wrist_terminal_core_001",
]

WristRole = Literal[
    "sensor_node",
    "control_node",
    "display_proxy",
    "future_autonomous_ai_node",
]

CommunicationChannel = Literal[
    "wifi",
    "uwb",
    "bluetooth",
]

SecurityBinding = Literal[
    "owner_bound",
]

AutonomyStage = Literal[
    "hybrid_ready",
]

WristContractStatus = Literal[
    "defined",
]


_TERMINAL_ID_PATTERN = re.compile(r"^wrist_[a-z][a-z0-9_]*$")
_ROLE_PATTERN = re.compile(r"^[a-z][a-z0-9_]*$")
_CHANNEL_PATTERN = re.compile(r"^[a-z][a-z0-9_]*$")
_DISPLAY_ENGINE_ID_PATTERN = re.compile(r"^opticsengine_[a-z][a-z0-9_]*$")


def _validate_unique_non_empty_str_tuple(
    *,
    values: tuple[str, ...],
    field_name: str,
    owner_id: str,
) -> None:
    """Validate tuple items are non-empty and unique."""
    if len(set(values)) != len(values):
        raise ValueError(f"Duplicate values in {field_name} for {owner_id}")
    for value in values:
        if not value.strip():
            raise ValueError(f"{field_name} contains empty value for {owner_id}")


@dataclass(frozen=True, slots=True)
class WristTerminalEntry:
    """Canonical wrist terminal contract entry."""

    wrist_terminal_id: WristTerminalId
    role_stack: tuple[WristRole, ...]
    communication_channels: tuple[CommunicationChannel, ...]
    secure_element_required: bool
    identity_binding_required: bool
    haptic_feedback_required: bool
    gesture_input_required: bool
    microphone_array_required: bool
    local_display_logic_required: bool
    heavy_compute_local: bool
    display_engine_entry_id: str
    security_binding: SecurityBinding
    autonomy_stage: AutonomyStage
    production_path_allowed: bool
    contract_status: WristContractStatus
    description: str

    def __post_init__(self) -> None:
        """Validate wrist terminal invariants."""
        if not _TERMINAL_ID_PATTERN.fullmatch(self.wrist_terminal_id):
            raise ValueError(f"Invalid wrist_terminal_id: {self.wrist_terminal_id}")

        if not _DISPLAY_ENGINE_ID_PATTERN.fullmatch(self.display_engine_entry_id):
            raise ValueError(
                f"Invalid display_engine_entry_id: {self.display_engine_entry_id}"
            )

        if not self.description.strip():
            raise ValueError(
                f"description must not be empty for {self.wrist_terminal_id}"
            )

        _validate_unique_non_empty_str_tuple(
            values=self.role_stack,
            field_name="role_stack",
            owner_id=self.wrist_terminal_id,
        )
        _validate_unique_non_empty_str_tuple(
            values=self.communication_channels,
            field_name="communication_channels",
            owner_id=self.wrist_terminal_id,
        )

        for role in self.role_stack:
            if not _ROLE_PATTERN.fullmatch(role):
                raise ValueError(
                    f"Invalid role '{role}' for {self.wrist_terminal_id}"
                )

        for channel in self.communication_channels:
            if not _CHANNEL_PATTERN.fullmatch(channel):
                raise ValueError(
                    f"Invalid channel '{channel}' for {self.wrist_terminal_id}"
                )

        required_roles = (
            "sensor_node",
            "control_node",
            "display_proxy",
            "future_autonomous_ai_node",
        )
        if self.role_stack != required_roles:
            raise ValueError(
                f"wrist terminal must preserve canonical role_stack: {self.wrist_terminal_id}"
            )

        required_channels = ("wifi", "uwb", "bluetooth")
        if self.communication_channels != required_channels:
            raise ValueError(
                f"wrist terminal must preserve canonical communication channels: {self.wrist_terminal_id}"
            )

        if not self.secure_element_required:
            raise ValueError(
                f"secure_element_required must be True: {self.wrist_terminal_id}"
            )
        if not self.identity_binding_required:
            raise ValueError(
                f"identity_binding_required must be True: {self.wrist_terminal_id}"
            )
        if not self.haptic_feedback_required:
            raise ValueError(
                f"haptic_feedback_required must be True: {self.wrist_terminal_id}"
            )
        if not self.gesture_input_required:
            raise ValueError(
                f"gesture_input_required must be True: {self.wrist_terminal_id}"
            )
        if not self.microphone_array_required:
            raise ValueError(
                f"microphone_array_required must be True: {self.wrist_terminal_id}"
            )
        if not self.local_display_logic_required:
            raise ValueError(
                f"local_display_logic_required must be True: {self.wrist_terminal_id}"
            )

        if self.heavy_compute_local:
            raise ValueError(
                f"heavy_compute_local must be False at hybrid_ready stage: {self.wrist_terminal_id}"
            )

        if self.security_binding != "owner_bound":
            raise ValueError(
                f"security_binding must be owner_bound: {self.wrist_terminal_id}"
            )

        if self.autonomy_stage != "hybrid_ready":
            raise ValueError(
                f"autonomy_stage must be hybrid_ready: {self.wrist_terminal_id}"
            )

        if not self.production_path_allowed:
            raise ValueError(
                f"production_path_allowed must be True: {self.wrist_terminal_id}"
            )

        if self.contract_status != "defined":
            raise ValueError(
                f"contract_status must be defined: {self.wrist_terminal_id}"
            )


@dataclass(frozen=True, slots=True)
class WristTerminalContract:
    """Unified wrist terminal contract."""

    total_entries: int
    secure_element_entries: int
    production_allowed_entries: int
    hybrid_ready_entries: int
    defined_entries: int
    entries: tuple[WristTerminalEntry, ...]

    def __post_init__(self) -> None:
        """Validate wrist terminal contract invariants."""
        if self.total_entries != len(self.entries):
            raise ValueError("total_entries must match entries length")

        secure_element_entries = sum(
            1 for entry in self.entries if entry.secure_element_required
        )
        production_allowed_entries = sum(
            1 for entry in self.entries if entry.production_path_allowed
        )
        hybrid_ready_entries = sum(
            1 for entry in self.entries if entry.autonomy_stage == "hybrid_ready"
        )
        defined_entries = sum(
            1 for entry in self.entries if entry.contract_status == "defined"
        )

        if self.secure_element_entries != secure_element_entries:
            raise ValueError("secure_element_entries must match computed count")

        if self.production_allowed_entries != production_allowed_entries:
            raise ValueError("production_allowed_entries must match computed count")

        if self.hybrid_ready_entries != hybrid_ready_entries:
            raise ValueError("hybrid_ready_entries must match computed count")

        if self.defined_entries != defined_entries:
            raise ValueError("defined_entries must match computed count")

        entry_ids = tuple(entry.wrist_terminal_id for entry in self.entries)
        if len(set(entry_ids)) != len(entry_ids):
            raise ValueError("Duplicate wrist_terminal_id values detected")


def build_wrist_terminal_contract() -> WristTerminalContract:
    """Build canonical wrist terminal contract."""
    node_split = build_node_runtime_split_contract()
    optics_contract = build_optics_light_field_engine_contract()

    node_ids = {entry.node_id for entry in node_split.entries}
    optics_ids = {entry.engine_entry_id for entry in optics_contract.entries}

    if "mobile_001" not in node_ids:
        raise ValueError("Expected mobile_001 in node runtime split contract")

    if "opticsengine_ar_glasses_projection_001" not in optics_ids:
        raise ValueError(
            "Expected opticsengine_ar_glasses_projection_001 in optics engine contract"
        )

    entries = (
        WristTerminalEntry(
            wrist_terminal_id="wrist_terminal_core_001",
            role_stack=(
                "sensor_node",
                "control_node",
                "display_proxy",
                "future_autonomous_ai_node",
            ),
            communication_channels=("wifi", "uwb", "bluetooth"),
            secure_element_required=True,
            identity_binding_required=True,
            haptic_feedback_required=True,
            gesture_input_required=True,
            microphone_array_required=True,
            local_display_logic_required=True,
            heavy_compute_local=False,
            display_engine_entry_id="opticsengine_ar_glasses_projection_001",
            security_binding="owner_bound",
            autonomy_stage="hybrid_ready",
            production_path_allowed=True,
            contract_status="defined",
            description="Canonical wrist terminal contract for hybrid sensor/control/display node.",
        ),
    )

    secure_element_entries = sum(
        1 for entry in entries if entry.secure_element_required
    )
    production_allowed_entries = sum(
        1 for entry in entries if entry.production_path_allowed
    )
    hybrid_ready_entries = sum(
        1 for entry in entries if entry.autonomy_stage == "hybrid_ready"
    )
    defined_entries = sum(
        1 for entry in entries if entry.contract_status == "defined"
    )

    return WristTerminalContract(
        total_entries=len(entries),
        secure_element_entries=secure_element_entries,
        production_allowed_entries=production_allowed_entries,
        hybrid_ready_entries=hybrid_ready_entries,
        defined_entries=defined_entries,
        entries=entries,
    )
