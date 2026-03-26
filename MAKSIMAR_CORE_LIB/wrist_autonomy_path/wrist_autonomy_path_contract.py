from __future__ import annotations

import re
from dataclasses import dataclass
from typing import Literal

from MAKSIMAR_CORE_LIB.wrist_terminal_contract import (
    build_wrist_terminal_contract,
)


AutonomyStage = Literal[
    "stage_1_thin_client",
    "stage_2_hybrid_inference",
    "stage_3_autonomous_node",
]

ComputePlacement = Literal[
    "remote_heavy_compute",
    "hybrid_local_and_remote",
    "local_primary_compute",
]

InferenceMode = Literal[
    "remote_only",
    "hybrid_inference",
    "local_inference",
]

ExecutionAuthority = Literal[
    "remote_authority",
    "shared_authority",
    "local_authority_with_policy",
]

AutonomyPathStatus = Literal[
    "defined",
]


_STAGE_ENTRY_ID_PATTERN = re.compile(r"^wristautonomy_[a-z][a-z0-9_]*$")
_TERMINAL_ID_PATTERN = re.compile(r"^wrist_[a-z][a-z0-9_]*$")


@dataclass(frozen=True, slots=True)
class WristAutonomyPathEntry:
    """Canonical wrist terminal autonomy path entry."""

    autonomy_entry_id: str
    wrist_terminal_id: str
    autonomy_stage: AutonomyStage
    compute_placement: ComputePlacement
    inference_mode: InferenceMode
    execution_authority: ExecutionAuthority
    local_sensor_stack_required: bool
    local_ui_logic_required: bool
    local_inference_required: bool
    remote_heavy_compute_allowed: bool
    policy_binding_required: bool
    production_path_allowed: bool
    autonomy_path_status: AutonomyPathStatus
    description: str

    def __post_init__(self) -> None:
        """Validate wrist autonomy path invariants."""
        if not _STAGE_ENTRY_ID_PATTERN.fullmatch(self.autonomy_entry_id):
            raise ValueError(f"Invalid autonomy_entry_id: {self.autonomy_entry_id}")

        if not _TERMINAL_ID_PATTERN.fullmatch(self.wrist_terminal_id):
            raise ValueError(f"Invalid wrist_terminal_id: {self.wrist_terminal_id}")

        if not self.description.strip():
            raise ValueError(
                f"description must not be empty for {self.autonomy_entry_id}"
            )

        if not self.local_sensor_stack_required:
            raise ValueError(
                f"local_sensor_stack_required must be True: {self.autonomy_entry_id}"
            )

        if not self.local_ui_logic_required:
            raise ValueError(
                f"local_ui_logic_required must be True: {self.autonomy_entry_id}"
            )

        if not self.policy_binding_required:
            raise ValueError(
                f"policy_binding_required must be True: {self.autonomy_entry_id}"
            )

        if not self.production_path_allowed:
            raise ValueError(
                f"production_path_allowed must be True: {self.autonomy_entry_id}"
            )

        if self.autonomy_path_status != "defined":
            raise ValueError(
                f"autonomy_path_status must be defined: {self.autonomy_entry_id}"
            )

        if self.autonomy_stage == "stage_1_thin_client":
            if self.compute_placement != "remote_heavy_compute":
                raise ValueError(
                    f"stage_1_thin_client must use remote_heavy_compute: {self.autonomy_entry_id}"
                )
            if self.inference_mode != "remote_only":
                raise ValueError(
                    f"stage_1_thin_client must use remote_only inference: {self.autonomy_entry_id}"
                )
            if self.execution_authority != "remote_authority":
                raise ValueError(
                    f"stage_1_thin_client must use remote_authority: {self.autonomy_entry_id}"
                )
            if self.local_inference_required:
                raise ValueError(
                    f"stage_1_thin_client must not require local inference: {self.autonomy_entry_id}"
                )
            if not self.remote_heavy_compute_allowed:
                raise ValueError(
                    f"stage_1_thin_client must allow remote heavy compute: {self.autonomy_entry_id}"
                )

        if self.autonomy_stage == "stage_2_hybrid_inference":
            if self.compute_placement != "hybrid_local_and_remote":
                raise ValueError(
                    f"stage_2_hybrid_inference must use hybrid_local_and_remote: {self.autonomy_entry_id}"
                )
            if self.inference_mode != "hybrid_inference":
                raise ValueError(
                    f"stage_2_hybrid_inference must use hybrid_inference: {self.autonomy_entry_id}"
                )
            if self.execution_authority != "shared_authority":
                raise ValueError(
                    f"stage_2_hybrid_inference must use shared_authority: {self.autonomy_entry_id}"
                )
            if not self.local_inference_required:
                raise ValueError(
                    f"stage_2_hybrid_inference must require local inference: {self.autonomy_entry_id}"
                )
            if not self.remote_heavy_compute_allowed:
                raise ValueError(
                    f"stage_2_hybrid_inference must allow remote heavy compute: {self.autonomy_entry_id}"
                )

        if self.autonomy_stage == "stage_3_autonomous_node":
            if self.compute_placement != "local_primary_compute":
                raise ValueError(
                    f"stage_3_autonomous_node must use local_primary_compute: {self.autonomy_entry_id}"
                )
            if self.inference_mode != "local_inference":
                raise ValueError(
                    f"stage_3_autonomous_node must use local_inference: {self.autonomy_entry_id}"
                )
            if self.execution_authority != "local_authority_with_policy":
                raise ValueError(
                    f"stage_3_autonomous_node must use local_authority_with_policy: {self.autonomy_entry_id}"
                )
            if not self.local_inference_required:
                raise ValueError(
                    f"stage_3_autonomous_node must require local inference: {self.autonomy_entry_id}"
                )
            if self.remote_heavy_compute_allowed:
                raise ValueError(
                    f"stage_3_autonomous_node must not require remote heavy compute allowance in canonical autonomous stage: {self.autonomy_entry_id}"
                )


@dataclass(frozen=True, slots=True)
class WristAutonomyPathContract:
    """Unified wrist terminal autonomy path contract."""

    total_entries: int
    local_inference_entries: int
    remote_heavy_compute_entries: int
    autonomous_stage_entries: int
    defined_entries: int
    entries: tuple[WristAutonomyPathEntry, ...]

    def __post_init__(self) -> None:
        """Validate wrist autonomy path contract invariants."""
        if self.total_entries != len(self.entries):
            raise ValueError("total_entries must match entries length")

        local_inference_entries = sum(
            1 for entry in self.entries if entry.local_inference_required
        )
        remote_heavy_compute_entries = sum(
            1 for entry in self.entries if entry.remote_heavy_compute_allowed
        )
        autonomous_stage_entries = sum(
            1 for entry in self.entries if entry.autonomy_stage == "stage_3_autonomous_node"
        )
        defined_entries = sum(
            1 for entry in self.entries if entry.autonomy_path_status == "defined"
        )

        if self.local_inference_entries != local_inference_entries:
            raise ValueError("local_inference_entries must match computed count")

        if self.remote_heavy_compute_entries != remote_heavy_compute_entries:
            raise ValueError("remote_heavy_compute_entries must match computed count")

        if self.autonomous_stage_entries != autonomous_stage_entries:
            raise ValueError("autonomous_stage_entries must match computed count")

        if self.defined_entries != defined_entries:
            raise ValueError("defined_entries must match computed count")

        entry_ids = tuple(entry.autonomy_entry_id for entry in self.entries)
        stages = tuple(entry.autonomy_stage for entry in self.entries)

        if len(set(entry_ids)) != len(entry_ids):
            raise ValueError("Duplicate autonomy_entry_id values detected")

        if len(set(stages)) != len(stages):
            raise ValueError("Duplicate autonomy_stage values detected")


def build_wrist_autonomy_path_contract() -> WristAutonomyPathContract:
    """Build canonical wrist terminal autonomy path contract."""
    wrist_contract = build_wrist_terminal_contract()
    terminal_ids = {entry.wrist_terminal_id for entry in wrist_contract.entries}

    if "wrist_terminal_core_001" not in terminal_ids:
        raise ValueError("Expected wrist_terminal_core_001 in wrist terminal contract")

    entries = (
        WristAutonomyPathEntry(
            autonomy_entry_id="wristautonomy_stage_1_001",
            wrist_terminal_id="wrist_terminal_core_001",
            autonomy_stage="stage_1_thin_client",
            compute_placement="remote_heavy_compute",
            inference_mode="remote_only",
            execution_authority="remote_authority",
            local_sensor_stack_required=True,
            local_ui_logic_required=True,
            local_inference_required=False,
            remote_heavy_compute_allowed=True,
            policy_binding_required=True,
            production_path_allowed=True,
            autonomy_path_status="defined",
            description="Stage 1 wrist path: thin client with remote heavy compute.",
        ),
        WristAutonomyPathEntry(
            autonomy_entry_id="wristautonomy_stage_2_001",
            wrist_terminal_id="wrist_terminal_core_001",
            autonomy_stage="stage_2_hybrid_inference",
            compute_placement="hybrid_local_and_remote",
            inference_mode="hybrid_inference",
            execution_authority="shared_authority",
            local_sensor_stack_required=True,
            local_ui_logic_required=True,
            local_inference_required=True,
            remote_heavy_compute_allowed=True,
            policy_binding_required=True,
            production_path_allowed=True,
            autonomy_path_status="defined",
            description="Stage 2 wrist path: hybrid local inference with remote heavy compute fallback.",
        ),
        WristAutonomyPathEntry(
            autonomy_entry_id="wristautonomy_stage_3_001",
            wrist_terminal_id="wrist_terminal_core_001",
            autonomy_stage="stage_3_autonomous_node",
            compute_placement="local_primary_compute",
            inference_mode="local_inference",
            execution_authority="local_authority_with_policy",
            local_sensor_stack_required=True,
            local_ui_logic_required=True,
            local_inference_required=True,
            remote_heavy_compute_allowed=False,
            policy_binding_required=True,
            production_path_allowed=True,
            autonomy_path_status="defined",
            description="Stage 3 wrist path: autonomous AI node with local primary compute.",
        ),
    )

    local_inference_entries = sum(
        1 for entry in entries if entry.local_inference_required
    )
    remote_heavy_compute_entries = sum(
        1 for entry in entries if entry.remote_heavy_compute_allowed
    )
    autonomous_stage_entries = sum(
        1 for entry in entries if entry.autonomy_stage == "stage_3_autonomous_node"
    )
    defined_entries = sum(
        1 for entry in entries if entry.autonomy_path_status == "defined"
    )

    return WristAutonomyPathContract(
        total_entries=len(entries),
        local_inference_entries=local_inference_entries,
        remote_heavy_compute_entries=remote_heavy_compute_entries,
        autonomous_stage_entries=autonomous_stage_entries,
        defined_entries=defined_entries,
        entries=entries,
    )
