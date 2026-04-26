from __future__ import annotations

from dataclasses import dataclass
from typing import Literal


RollbackReadinessState = Literal[
    "rollback_readiness_ready",
]

RollbackReadinessClass = Literal[
    "read_only_rollback_readiness",
    "approval_bound_rollback_readiness",
]

RollbackReadinessMode = Literal[
    "preview_review_simulation_replay_sandbox_risk_rollback_readiness",
    "preview_review_approval_simulation_replay_sandbox_risk_rollback_readiness",
]

ALL_ROLLBACK_READINESS_STATES: tuple[RollbackReadinessState, ...] = (
    "rollback_readiness_ready",
)

ALL_ROLLBACK_READINESS_CLASSES: tuple[RollbackReadinessClass, ...] = (
    "read_only_rollback_readiness",
    "approval_bound_rollback_readiness",
)

ALL_ROLLBACK_READINESS_MODES: tuple[RollbackReadinessMode, ...] = (
    "preview_review_simulation_replay_sandbox_risk_rollback_readiness",
    "preview_review_approval_simulation_replay_sandbox_risk_rollback_readiness",
)


def _require_non_empty(value: str, field_name: str) -> None:
    """Validate that a string field is present and not blank."""
    if not value or not value.strip():
        raise ValueError(f"{field_name} must be a non-empty string.")


@dataclass(frozen=True, slots=True)
class RollbackReadinessEntry:
    """Canonical rollback readiness entry."""

    rollback_readiness_id: str
    operator_intent_id: str
    panel_id: str
    workspace_id: str
    rollback_readiness_state: RollbackReadinessState
    rollback_readiness_class: RollbackReadinessClass
    rollback_readiness_mode: RollbackReadinessMode
    approval_required: bool
    handoff_ready: bool
    rollback_visible: bool
    operator_visible: bool
    trace_id: str
    description: str

    def __post_init__(self) -> None:
        _require_non_empty(self.rollback_readiness_id, "rollback_readiness_id")
        _require_non_empty(self.operator_intent_id, "operator_intent_id")
        _require_non_empty(self.panel_id, "panel_id")
        _require_non_empty(self.workspace_id, "workspace_id")
        _require_non_empty(self.trace_id, "trace_id")
        _require_non_empty(self.description, "description")

        if self.rollback_readiness_state not in ALL_ROLLBACK_READINESS_STATES:
            raise ValueError(
                "rollback_readiness_state must be one of "
                f"{ALL_ROLLBACK_READINESS_STATES}, got {self.rollback_readiness_state!r}."
            )

        if self.rollback_readiness_class not in ALL_ROLLBACK_READINESS_CLASSES:
            raise ValueError(
                "rollback_readiness_class must be one of "
                f"{ALL_ROLLBACK_READINESS_CLASSES}, got {self.rollback_readiness_class!r}."
            )

        if self.rollback_readiness_mode not in ALL_ROLLBACK_READINESS_MODES:
            raise ValueError(
                "rollback_readiness_mode must be one of "
                f"{ALL_ROLLBACK_READINESS_MODES}, got {self.rollback_readiness_mode!r}."
            )

        if not self.handoff_ready:
            raise ValueError(
                "handoff_ready must remain true for canonical rollback readiness entries."
            )

        if not self.rollback_visible:
            raise ValueError(
                "rollback_visible must remain true for canonical rollback readiness entries."
            )

        if not self.operator_visible:
            raise ValueError(
                "operator_visible must remain true for canonical rollback readiness entries."
            )

        if (
            self.rollback_readiness_class == "approval_bound_rollback_readiness"
            and not self.approval_required
        ):
            raise ValueError(
                "approval_bound_rollback_readiness must have approval_required=True."
            )

        if (
            self.rollback_readiness_class == "read_only_rollback_readiness"
            and self.approval_required
        ):
            raise ValueError(
                "read_only_rollback_readiness must have approval_required=False."
            )

        if (
            self.rollback_readiness_class == "approval_bound_rollback_readiness"
            and self.rollback_readiness_mode
            != "preview_review_approval_simulation_replay_sandbox_risk_rollback_readiness"
        ):
            raise ValueError(
                "approval_bound_rollback_readiness must use preview_review_approval_simulation_replay_sandbox_risk_rollback_readiness."
            )

        if (
            self.rollback_readiness_class == "read_only_rollback_readiness"
            and self.rollback_readiness_mode
            != "preview_review_simulation_replay_sandbox_risk_rollback_readiness"
        ):
            raise ValueError(
                "read_only_rollback_readiness must use preview_review_simulation_replay_sandbox_risk_rollback_readiness."
            )


@dataclass(frozen=True, slots=True)
class RollbackReadinessContract:
    """Canonical rollback readiness contract."""

    contract_id: str
    total_entries: int
    read_only_rollback_entries: int
    approval_bound_rollback_entries: int
    rollback_visible_entries: int
    operator_visible_entries: int
    entries: tuple[RollbackReadinessEntry, ...]

    def __post_init__(self) -> None:
        _require_non_empty(self.contract_id, "contract_id")

        if self.total_entries != len(self.entries):
            raise ValueError("total_entries must match len(entries).")

        if self.read_only_rollback_entries != sum(
            1
            for entry in self.entries
            if entry.rollback_readiness_class == "read_only_rollback_readiness"
        ):
            raise ValueError(
                "read_only_rollback_entries must match read_only_rollback_readiness count."
            )

        if self.approval_bound_rollback_entries != sum(
            1
            for entry in self.entries
            if entry.rollback_readiness_class == "approval_bound_rollback_readiness"
        ):
            raise ValueError(
                "approval_bound_rollback_entries must match approval_bound_rollback_readiness count."
            )

        if self.rollback_visible_entries != sum(
            1 for entry in self.entries if entry.rollback_visible
        ):
            raise ValueError(
                "rollback_visible_entries must match rollback_visible count."
            )

        if self.operator_visible_entries != sum(
            1 for entry in self.entries if entry.operator_visible
        ):
            raise ValueError(
                "operator_visible_entries must match operator_visible count."
            )
