from __future__ import annotations

import re
from dataclasses import dataclass
from typing import Literal

from MAKSIMAR_CORE_LIB.execution_pressure import (
    build_admission_pressure_rules_contract,
    build_degraded_trigger_contract,
    build_pressure_decision_contract,
    build_pressure_level_contract,
    build_pressure_signal_contract,
)
from MAKSIMAR_SERVER.EXECUTION_CONTROL.backpressure import (
    build_server_backpressure_runtime_contract,
)
from MAKSIMAR_SERVER.EXECUTION_CONTROL.degraded_mode import (
    build_degraded_mode_runtime_contract,
)
from MAKSIMAR_SERVER.RUNTIME.pressure_state import (
    build_pressure_state_runtime_contract,
)


PressureLevel = Literal[
    "normal",
    "elevated",
    "high",
    "critical",
]

PressureCompletionStatus = Literal[
    "completed",
]

PressureRuntimeState = Literal[
    "open",
    "throttled",
    "restricted",
    "blocked",
]

AdmissionDecision = Literal[
    "accept",
    "accept_with_throttle",
    "reject_new_work",
    "reject",
]

PrimaryAction = Literal[
    "allow",
    "throttle",
    "restrict",
    "reject",
]


_COMPLETION_ENTRY_ID_PATTERN = re.compile(r"^pressurecompletion_[a-z][a-z0-9_]*$")
_PRESSURE_LEVEL_PATTERN = re.compile(r"^[a-z][a-z0-9_]*$")


@dataclass(frozen=True, slots=True)
class ExecutionPressureCompletionEntry:
    """Canonical execution pressure completion entry."""

    completion_entry_id: str
    pressure_level: PressureLevel
    primary_action: PrimaryAction
    admission_decision: AdmissionDecision
    runtime_state: PressureRuntimeState
    throttling_required: bool
    degraded_mode_candidate: bool
    degraded_trigger_enabled: bool
    total_signal_kinds: int
    runtime_entries_observed: int
    completion_valid: bool
    completion_status: PressureCompletionStatus
    description: str

    def __post_init__(self) -> None:
        """Validate execution pressure completion invariants."""
        if not _COMPLETION_ENTRY_ID_PATTERN.fullmatch(self.completion_entry_id):
            raise ValueError(
                f"Invalid completion_entry_id: {self.completion_entry_id}"
            )

        if not _PRESSURE_LEVEL_PATTERN.fullmatch(self.pressure_level):
            raise ValueError(f"Invalid pressure_level: {self.pressure_level}")

        if not self.description.strip():
            raise ValueError(
                f"description must not be empty for {self.completion_entry_id}"
            )

        if self.total_signal_kinds <= 0:
            raise ValueError(
                f"total_signal_kinds must be positive: {self.completion_entry_id}"
            )

        if self.runtime_entries_observed <= 0:
            raise ValueError(
                f"runtime_entries_observed must be positive: {self.completion_entry_id}"
            )

        if not self.completion_valid:
            raise ValueError(
                f"execution pressure completion entry must be valid: {self.completion_entry_id}"
            )

        if self.completion_status != "completed":
            raise ValueError(
                f"execution pressure completion entry must be completed: {self.completion_entry_id}"
            )

        if self.pressure_level == "normal":
            if self.primary_action != "allow":
                raise ValueError(
                    f"normal must map to allow: {self.completion_entry_id}"
                )
            if self.admission_decision != "accept":
                raise ValueError(
                    f"normal must map to accept: {self.completion_entry_id}"
                )
            if self.runtime_state != "open":
                raise ValueError(
                    f"normal must map to open runtime_state: {self.completion_entry_id}"
                )
            if self.throttling_required:
                raise ValueError(
                    f"normal must not require throttling: {self.completion_entry_id}"
                )
            if self.degraded_mode_candidate:
                raise ValueError(
                    f"normal must not be degraded candidate: {self.completion_entry_id}"
                )
            if self.degraded_trigger_enabled:
                raise ValueError(
                    f"normal must not enable degraded trigger: {self.completion_entry_id}"
                )

        if self.pressure_level == "elevated":
            if self.primary_action != "throttle":
                raise ValueError(
                    f"elevated must map to throttle: {self.completion_entry_id}"
                )
            if self.admission_decision != "accept_with_throttle":
                raise ValueError(
                    f"elevated must map to accept_with_throttle: {self.completion_entry_id}"
                )
            if self.runtime_state != "throttled":
                raise ValueError(
                    f"elevated must map to throttled runtime_state: {self.completion_entry_id}"
                )
            if not self.throttling_required:
                raise ValueError(
                    f"elevated must require throttling: {self.completion_entry_id}"
                )
            if self.degraded_mode_candidate:
                raise ValueError(
                    f"elevated must not be degraded candidate: {self.completion_entry_id}"
                )
            if self.degraded_trigger_enabled:
                raise ValueError(
                    f"elevated must not enable degraded trigger: {self.completion_entry_id}"
                )

        if self.pressure_level == "high":
            if self.primary_action != "restrict":
                raise ValueError(
                    f"high must map to restrict: {self.completion_entry_id}"
                )
            if self.admission_decision != "reject_new_work":
                raise ValueError(
                    f"high must map to reject_new_work: {self.completion_entry_id}"
                )
            if self.runtime_state != "restricted":
                raise ValueError(
                    f"high must map to restricted runtime_state: {self.completion_entry_id}"
                )
            if not self.throttling_required:
                raise ValueError(
                    f"high must require throttling: {self.completion_entry_id}"
                )
            if not self.degraded_mode_candidate:
                raise ValueError(
                    f"high must be degraded candidate: {self.completion_entry_id}"
                )
            if not self.degraded_trigger_enabled:
                raise ValueError(
                    f"high must enable degraded trigger: {self.completion_entry_id}"
                )

        if self.pressure_level == "critical":
            if self.primary_action != "reject":
                raise ValueError(
                    f"critical must map to reject: {self.completion_entry_id}"
                )
            if self.admission_decision != "reject":
                raise ValueError(
                    f"critical must map to reject admission: {self.completion_entry_id}"
                )
            if self.runtime_state != "blocked":
                raise ValueError(
                    f"critical must map to blocked runtime_state: {self.completion_entry_id}"
                )
            if not self.throttling_required:
                raise ValueError(
                    f"critical must require throttling: {self.completion_entry_id}"
                )
            if not self.degraded_mode_candidate:
                raise ValueError(
                    f"critical must be degraded candidate: {self.completion_entry_id}"
                )
            if not self.degraded_trigger_enabled:
                raise ValueError(
                    f"critical must enable degraded trigger: {self.completion_entry_id}"
                )


@dataclass(frozen=True, slots=True)
class ExecutionPressureCompletionContract:
    """Unified execution pressure completion contract."""

    total_entries: int
    throttled_or_higher_entries: int
    degraded_candidate_entries: int
    completed_entries: int
    entries: tuple[ExecutionPressureCompletionEntry, ...]

    def __post_init__(self) -> None:
        """Validate execution pressure completion contract invariants."""
        if self.total_entries != len(self.entries):
            raise ValueError("total_entries must match entries length")

        throttled_or_higher_entries = sum(
            1
            for entry in self.entries
            if entry.runtime_state in ("throttled", "restricted", "blocked")
        )
        degraded_candidate_entries = sum(
            1 for entry in self.entries if entry.degraded_mode_candidate
        )
        completed_entries = sum(
            1 for entry in self.entries if entry.completion_status == "completed"
        )

        if self.throttled_or_higher_entries != throttled_or_higher_entries:
            raise ValueError(
                "throttled_or_higher_entries must match computed count"
            )

        if self.degraded_candidate_entries != degraded_candidate_entries:
            raise ValueError(
                "degraded_candidate_entries must match computed count"
            )

        if self.completed_entries != completed_entries:
            raise ValueError("completed_entries must match computed count")

        entry_ids = tuple(entry.completion_entry_id for entry in self.entries)
        pressure_levels = tuple(entry.pressure_level for entry in self.entries)

        if len(set(entry_ids)) != len(entry_ids):
            raise ValueError("Duplicate completion_entry_id values detected")

        if len(set(pressure_levels)) != len(pressure_levels):
            raise ValueError("Duplicate pressure_level values detected")


def build_execution_pressure_completion_contract() -> ExecutionPressureCompletionContract:
    """Build canonical execution pressure completion contract."""
    level_contract = build_pressure_level_contract()
    signal_contract = build_pressure_signal_contract()
    decision_contract = build_pressure_decision_contract()
    degraded_contract = build_degraded_trigger_contract()
    admission_contract = build_admission_pressure_rules_contract()

    backpressure_runtime = build_server_backpressure_runtime_contract()
    degraded_runtime = build_degraded_mode_runtime_contract()
    pressure_state_runtime = build_pressure_state_runtime_contract()

    level_names = {entry.pressure_level for entry in level_contract.levels}
    decision_levels = {entry.pressure_level for entry in decision_contract.rules}
    degraded_levels = {entry.pressure_level for entry in degraded_contract.triggers}
    admission_levels = {entry.pressure_level for entry in admission_contract.rules}

    required_levels = {"normal", "elevated", "high", "critical"}

    missing_level_entries = required_levels - level_names
    if missing_level_entries:
        raise ValueError(
            f"Missing pressure levels in level contract: {sorted(missing_level_entries)}"
        )

    missing_decision_entries = required_levels - decision_levels
    if missing_decision_entries:
        raise ValueError(
            f"Missing pressure levels in decision contract: {sorted(missing_decision_entries)}"
        )

    missing_degraded_entries = required_levels - degraded_levels
    if missing_degraded_entries:
        raise ValueError(
            f"Missing pressure levels in degraded trigger contract: {sorted(missing_degraded_entries)}"
        )

    missing_admission_entries = required_levels - admission_levels
    if missing_admission_entries:
        raise ValueError(
            f"Missing pressure levels in admission contract: {sorted(missing_admission_entries)}"
        )

    if level_contract.total_levels != 4:
        raise ValueError("Expected 4 canonical pressure levels")

    if signal_contract.total_signals <= 0:
        raise ValueError("Pressure signal contract must expose signals")

    runtime_entries_observed = (
        backpressure_runtime.total_entries
        + degraded_runtime.total_entries
        + pressure_state_runtime.total_entries
    )

    canonical_mapping = {
        "normal": {
            "primary_action": "allow",
            "admission_decision": "accept",
            "runtime_state": "open",
            "throttling_required": False,
            "degraded_mode_candidate": False,
            "degraded_trigger_enabled": False,
        },
        "elevated": {
            "primary_action": "throttle",
            "admission_decision": "accept_with_throttle",
            "runtime_state": "throttled",
            "throttling_required": True,
            "degraded_mode_candidate": False,
            "degraded_trigger_enabled": False,
        },
        "high": {
            "primary_action": "restrict",
            "admission_decision": "reject_new_work",
            "runtime_state": "restricted",
            "throttling_required": True,
            "degraded_mode_candidate": True,
            "degraded_trigger_enabled": True,
        },
        "critical": {
            "primary_action": "reject",
            "admission_decision": "reject",
            "runtime_state": "blocked",
            "throttling_required": True,
            "degraded_mode_candidate": True,
            "degraded_trigger_enabled": True,
        },
    }

    entries = []
    for pressure_level in ("normal", "elevated", "high", "critical"):
        mapping = canonical_mapping[pressure_level]

        entries.append(
            ExecutionPressureCompletionEntry(
                completion_entry_id=f"pressurecompletion_{pressure_level}_001",
                pressure_level=pressure_level,
                primary_action=mapping["primary_action"],  # type: ignore[arg-type]
                admission_decision=mapping["admission_decision"],  # type: ignore[arg-type]
                runtime_state=mapping["runtime_state"],  # type: ignore[arg-type]
                throttling_required=mapping["throttling_required"],
                degraded_mode_candidate=mapping["degraded_mode_candidate"],
                degraded_trigger_enabled=mapping["degraded_trigger_enabled"],
                total_signal_kinds=signal_contract.total_signals,
                runtime_entries_observed=runtime_entries_observed,
                completion_valid=True,
                completion_status="completed",
                description=(
                    f"Completed execution pressure policy mapping for level {pressure_level}."
                ),
            )
        )

    throttled_or_higher_entries = sum(
        1
        for entry in entries
        if entry.runtime_state in ("throttled", "restricted", "blocked")
    )
    degraded_candidate_entries = sum(
        1 for entry in entries if entry.degraded_mode_candidate
    )
    completed_entries = sum(
        1 for entry in entries if entry.completion_status == "completed"
    )

    return ExecutionPressureCompletionContract(
        total_entries=len(entries),
        throttled_or_higher_entries=throttled_or_higher_entries,
        degraded_candidate_entries=degraded_candidate_entries,
        completed_entries=completed_entries,
        entries=tuple(entries),
    )
