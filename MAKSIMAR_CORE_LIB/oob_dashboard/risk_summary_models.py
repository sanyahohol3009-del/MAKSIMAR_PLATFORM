from __future__ import annotations

from dataclasses import dataclass
from typing import Literal


RiskSummaryState = Literal[
    "risk_summary_ready",
]

RiskSummaryClass = Literal[
    "read_only_risk_summary",
    "approval_bound_risk_summary",
]

RiskSummaryMode = Literal[
    "preview_review_simulation_replay_sandbox_risk_summary",
    "preview_review_approval_simulation_replay_sandbox_risk_summary",
]

ALL_RISK_SUMMARY_STATES: tuple[RiskSummaryState, ...] = (
    "risk_summary_ready",
)

ALL_RISK_SUMMARY_CLASSES: tuple[RiskSummaryClass, ...] = (
    "read_only_risk_summary",
    "approval_bound_risk_summary",
)

ALL_RISK_SUMMARY_MODES: tuple[RiskSummaryMode, ...] = (
    "preview_review_simulation_replay_sandbox_risk_summary",
    "preview_review_approval_simulation_replay_sandbox_risk_summary",
)


def _require_non_empty(value: str, field_name: str) -> None:
    """Validate that a string field is present and not blank."""
    if not value or not value.strip():
        raise ValueError(f"{field_name} must be a non-empty string.")


@dataclass(frozen=True, slots=True)
class RiskSummaryEntry:
    """Canonical risk summary entry."""

    risk_summary_id: str
    operator_intent_id: str
    panel_id: str
    workspace_id: str
    risk_summary_state: RiskSummaryState
    risk_summary_class: RiskSummaryClass
    risk_summary_mode: RiskSummaryMode
    approval_required: bool
    handoff_ready: bool
    risk_visible: bool
    operator_visible: bool
    trace_id: str
    description: str

    def __post_init__(self) -> None:
        _require_non_empty(self.risk_summary_id, "risk_summary_id")
        _require_non_empty(self.operator_intent_id, "operator_intent_id")
        _require_non_empty(self.panel_id, "panel_id")
        _require_non_empty(self.workspace_id, "workspace_id")
        _require_non_empty(self.trace_id, "trace_id")
        _require_non_empty(self.description, "description")

        if self.risk_summary_state not in ALL_RISK_SUMMARY_STATES:
            raise ValueError(
                "risk_summary_state must be one of "
                f"{ALL_RISK_SUMMARY_STATES}, got {self.risk_summary_state!r}."
            )

        if self.risk_summary_class not in ALL_RISK_SUMMARY_CLASSES:
            raise ValueError(
                "risk_summary_class must be one of "
                f"{ALL_RISK_SUMMARY_CLASSES}, got {self.risk_summary_class!r}."
            )

        if self.risk_summary_mode not in ALL_RISK_SUMMARY_MODES:
            raise ValueError(
                "risk_summary_mode must be one of "
                f"{ALL_RISK_SUMMARY_MODES}, got {self.risk_summary_mode!r}."
            )

        if not self.handoff_ready:
            raise ValueError(
                "handoff_ready must remain true for canonical risk summaries."
            )

        if not self.risk_visible:
            raise ValueError(
                "risk_visible must remain true for canonical risk summaries."
            )

        if not self.operator_visible:
            raise ValueError(
                "operator_visible must remain true for canonical risk summaries."
            )

        if (
            self.risk_summary_class == "approval_bound_risk_summary"
            and not self.approval_required
        ):
            raise ValueError(
                "approval_bound_risk_summary must have approval_required=True."
            )

        if (
            self.risk_summary_class == "read_only_risk_summary"
            and self.approval_required
        ):
            raise ValueError(
                "read_only_risk_summary must have approval_required=False."
            )

        if (
            self.risk_summary_class == "approval_bound_risk_summary"
            and self.risk_summary_mode
            != "preview_review_approval_simulation_replay_sandbox_risk_summary"
        ):
            raise ValueError(
                "approval_bound_risk_summary must use preview_review_approval_simulation_replay_sandbox_risk_summary."
            )

        if (
            self.risk_summary_class == "read_only_risk_summary"
            and self.risk_summary_mode
            != "preview_review_simulation_replay_sandbox_risk_summary"
        ):
            raise ValueError(
                "read_only_risk_summary must use preview_review_simulation_replay_sandbox_risk_summary."
            )


@dataclass(frozen=True, slots=True)
class RiskSummaryContract:
    """Canonical risk summary contract."""

    contract_id: str
    total_entries: int
    read_only_risk_entries: int
    approval_bound_risk_entries: int
    risk_visible_entries: int
    operator_visible_entries: int
    entries: tuple[RiskSummaryEntry, ...]

    def __post_init__(self) -> None:
        _require_non_empty(self.contract_id, "contract_id")

        if self.total_entries != len(self.entries):
            raise ValueError("total_entries must match len(entries).")

        if self.read_only_risk_entries != sum(
            1
            for entry in self.entries
            if entry.risk_summary_class == "read_only_risk_summary"
        ):
            raise ValueError(
                "read_only_risk_entries must match read_only_risk_summary count."
            )

        if self.approval_bound_risk_entries != sum(
            1
            for entry in self.entries
            if entry.risk_summary_class == "approval_bound_risk_summary"
        ):
            raise ValueError(
                "approval_bound_risk_entries must match approval_bound_risk_summary count."
            )

        if self.risk_visible_entries != sum(
            1 for entry in self.entries if entry.risk_visible
        ):
            raise ValueError(
                "risk_visible_entries must match risk_visible count."
            )

        if self.operator_visible_entries != sum(
            1 for entry in self.entries if entry.operator_visible
        ):
            raise ValueError(
                "operator_visible_entries must match operator_visible count."
            )
