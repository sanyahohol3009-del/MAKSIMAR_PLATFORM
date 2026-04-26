from __future__ import annotations

from dataclasses import dataclass
from typing import Literal


SimulationResultState = Literal[
    "simulation_result_ready",
]

SimulationResultClass = Literal[
    "read_only_simulation_result",
    "approval_bound_simulation_result",
]

SimulationEvidenceMode = Literal[
    "preview_review_simulation_evidence",
    "preview_review_approval_simulation_evidence",
]

ALL_SIMULATION_RESULT_STATES: tuple[SimulationResultState, ...] = (
    "simulation_result_ready",
)

ALL_SIMULATION_RESULT_CLASSES: tuple[SimulationResultClass, ...] = (
    "read_only_simulation_result",
    "approval_bound_simulation_result",
)

ALL_SIMULATION_EVIDENCE_MODES: tuple[SimulationEvidenceMode, ...] = (
    "preview_review_simulation_evidence",
    "preview_review_approval_simulation_evidence",
)


def _require_non_empty(value: str, field_name: str) -> None:
    """Validate that a string field is present and not blank."""
    if not value or not value.strip():
        raise ValueError(f"{field_name} must be a non-empty string.")


@dataclass(frozen=True, slots=True)
class SimulationResultEntry:
    """Canonical simulation result entry."""

    simulation_result_id: str
    operator_intent_id: str
    panel_id: str
    workspace_id: str
    simulation_result_state: SimulationResultState
    simulation_result_class: SimulationResultClass
    simulation_evidence_mode: SimulationEvidenceMode
    approval_required: bool
    handoff_ready: bool
    review_visible: bool
    operator_visible: bool
    trace_id: str
    description: str

    def __post_init__(self) -> None:
        _require_non_empty(self.simulation_result_id, "simulation_result_id")
        _require_non_empty(self.operator_intent_id, "operator_intent_id")
        _require_non_empty(self.panel_id, "panel_id")
        _require_non_empty(self.workspace_id, "workspace_id")
        _require_non_empty(self.trace_id, "trace_id")
        _require_non_empty(self.description, "description")

        if self.simulation_result_state not in ALL_SIMULATION_RESULT_STATES:
            raise ValueError(
                "simulation_result_state must be one of "
                f"{ALL_SIMULATION_RESULT_STATES}, got {self.simulation_result_state!r}."
            )

        if self.simulation_result_class not in ALL_SIMULATION_RESULT_CLASSES:
            raise ValueError(
                "simulation_result_class must be one of "
                f"{ALL_SIMULATION_RESULT_CLASSES}, got {self.simulation_result_class!r}."
            )

        if self.simulation_evidence_mode not in ALL_SIMULATION_EVIDENCE_MODES:
            raise ValueError(
                "simulation_evidence_mode must be one of "
                f"{ALL_SIMULATION_EVIDENCE_MODES}, got {self.simulation_evidence_mode!r}."
            )

        if not self.handoff_ready:
            raise ValueError(
                "handoff_ready must remain true for canonical simulation results."
            )

        if not self.review_visible:
            raise ValueError(
                "review_visible must remain true for canonical simulation results."
            )

        if not self.operator_visible:
            raise ValueError(
                "operator_visible must remain true for canonical simulation results."
            )

        if (
            self.simulation_result_class == "approval_bound_simulation_result"
            and not self.approval_required
        ):
            raise ValueError(
                "approval_bound_simulation_result must have approval_required=True."
            )

        if (
            self.simulation_result_class == "read_only_simulation_result"
            and self.approval_required
        ):
            raise ValueError(
                "read_only_simulation_result must have approval_required=False."
            )

        if (
            self.simulation_result_class == "approval_bound_simulation_result"
            and self.simulation_evidence_mode
            != "preview_review_approval_simulation_evidence"
        ):
            raise ValueError(
                "approval_bound_simulation_result must use preview_review_approval_simulation_evidence."
            )

        if (
            self.simulation_result_class == "read_only_simulation_result"
            and self.simulation_evidence_mode
            != "preview_review_simulation_evidence"
        ):
            raise ValueError(
                "read_only_simulation_result must use preview_review_simulation_evidence."
            )


@dataclass(frozen=True, slots=True)
class SimulationResultContract:
    """Canonical simulation result contract."""

    contract_id: str
    total_entries: int
    read_only_simulation_entries: int
    approval_bound_simulation_entries: int
    review_visible_entries: int
    operator_visible_entries: int
    entries: tuple[SimulationResultEntry, ...]

    def __post_init__(self) -> None:
        _require_non_empty(self.contract_id, "contract_id")

        if self.total_entries != len(self.entries):
            raise ValueError("total_entries must match len(entries).")

        if self.read_only_simulation_entries != sum(
            1
            for entry in self.entries
            if entry.simulation_result_class == "read_only_simulation_result"
        ):
            raise ValueError(
                "read_only_simulation_entries must match read_only_simulation_result count."
            )

        if self.approval_bound_simulation_entries != sum(
            1
            for entry in self.entries
            if entry.simulation_result_class == "approval_bound_simulation_result"
        ):
            raise ValueError(
                "approval_bound_simulation_entries must match approval_bound_simulation_result count."
            )

        if self.review_visible_entries != sum(
            1 for entry in self.entries if entry.review_visible
        ):
            raise ValueError(
                "review_visible_entries must match review_visible count."
            )

        if self.operator_visible_entries != sum(
            1 for entry in self.entries if entry.operator_visible
        ):
            raise ValueError(
                "operator_visible_entries must match operator_visible count."
            )
