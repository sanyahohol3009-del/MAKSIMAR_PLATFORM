from __future__ import annotations

from dataclasses import dataclass
from typing import Literal


ReplayArtifactState = Literal[
    "replay_artifact_ready",
]

ReplayArtifactClass = Literal[
    "read_only_replay_artifact",
    "approval_bound_replay_artifact",
]

ReplayEvidenceMode = Literal[
    "preview_review_simulation_replay_evidence",
    "preview_review_approval_simulation_replay_evidence",
]

ALL_REPLAY_ARTIFACT_STATES: tuple[ReplayArtifactState, ...] = (
    "replay_artifact_ready",
)

ALL_REPLAY_ARTIFACT_CLASSES: tuple[ReplayArtifactClass, ...] = (
    "read_only_replay_artifact",
    "approval_bound_replay_artifact",
)

ALL_REPLAY_EVIDENCE_MODES: tuple[ReplayEvidenceMode, ...] = (
    "preview_review_simulation_replay_evidence",
    "preview_review_approval_simulation_replay_evidence",
)


def _require_non_empty(value: str, field_name: str) -> None:
    """Validate that a string field is present and not blank."""
    if not value or not value.strip():
        raise ValueError(f"{field_name} must be a non-empty string.")


@dataclass(frozen=True, slots=True)
class ReplayArtifactEntry:
    """Canonical replay artifact entry."""

    replay_artifact_id: str
    operator_intent_id: str
    panel_id: str
    workspace_id: str
    replay_artifact_state: ReplayArtifactState
    replay_artifact_class: ReplayArtifactClass
    replay_evidence_mode: ReplayEvidenceMode
    approval_required: bool
    handoff_ready: bool
    replay_visible: bool
    operator_visible: bool
    trace_id: str
    description: str

    def __post_init__(self) -> None:
        _require_non_empty(self.replay_artifact_id, "replay_artifact_id")
        _require_non_empty(self.operator_intent_id, "operator_intent_id")
        _require_non_empty(self.panel_id, "panel_id")
        _require_non_empty(self.workspace_id, "workspace_id")
        _require_non_empty(self.trace_id, "trace_id")
        _require_non_empty(self.description, "description")

        if self.replay_artifact_state not in ALL_REPLAY_ARTIFACT_STATES:
            raise ValueError(
                "replay_artifact_state must be one of "
                f"{ALL_REPLAY_ARTIFACT_STATES}, got {self.replay_artifact_state!r}."
            )

        if self.replay_artifact_class not in ALL_REPLAY_ARTIFACT_CLASSES:
            raise ValueError(
                "replay_artifact_class must be one of "
                f"{ALL_REPLAY_ARTIFACT_CLASSES}, got {self.replay_artifact_class!r}."
            )

        if self.replay_evidence_mode not in ALL_REPLAY_EVIDENCE_MODES:
            raise ValueError(
                "replay_evidence_mode must be one of "
                f"{ALL_REPLAY_EVIDENCE_MODES}, got {self.replay_evidence_mode!r}."
            )

        if not self.handoff_ready:
            raise ValueError(
                "handoff_ready must remain true for canonical replay artifacts."
            )

        if not self.replay_visible:
            raise ValueError(
                "replay_visible must remain true for canonical replay artifacts."
            )

        if not self.operator_visible:
            raise ValueError(
                "operator_visible must remain true for canonical replay artifacts."
            )

        if (
            self.replay_artifact_class == "approval_bound_replay_artifact"
            and not self.approval_required
        ):
            raise ValueError(
                "approval_bound_replay_artifact must have approval_required=True."
            )

        if (
            self.replay_artifact_class == "read_only_replay_artifact"
            and self.approval_required
        ):
            raise ValueError(
                "read_only_replay_artifact must have approval_required=False."
            )

        if (
            self.replay_artifact_class == "approval_bound_replay_artifact"
            and self.replay_evidence_mode
            != "preview_review_approval_simulation_replay_evidence"
        ):
            raise ValueError(
                "approval_bound_replay_artifact must use preview_review_approval_simulation_replay_evidence."
            )

        if (
            self.replay_artifact_class == "read_only_replay_artifact"
            and self.replay_evidence_mode
            != "preview_review_simulation_replay_evidence"
        ):
            raise ValueError(
                "read_only_replay_artifact must use preview_review_simulation_replay_evidence."
            )


@dataclass(frozen=True, slots=True)
class ReplayArtifactContract:
    """Canonical replay artifact contract."""

    contract_id: str
    total_entries: int
    read_only_replay_entries: int
    approval_bound_replay_entries: int
    replay_visible_entries: int
    operator_visible_entries: int
    entries: tuple[ReplayArtifactEntry, ...]

    def __post_init__(self) -> None:
        _require_non_empty(self.contract_id, "contract_id")

        if self.total_entries != len(self.entries):
            raise ValueError("total_entries must match len(entries).")

        if self.read_only_replay_entries != sum(
            1
            for entry in self.entries
            if entry.replay_artifact_class == "read_only_replay_artifact"
        ):
            raise ValueError(
                "read_only_replay_entries must match read_only_replay_artifact count."
            )

        if self.approval_bound_replay_entries != sum(
            1
            for entry in self.entries
            if entry.replay_artifact_class == "approval_bound_replay_artifact"
        ):
            raise ValueError(
                "approval_bound_replay_entries must match approval_bound_replay_artifact count."
            )

        if self.replay_visible_entries != sum(
            1 for entry in self.entries if entry.replay_visible
        ):
            raise ValueError(
                "replay_visible_entries must match replay_visible count."
            )

        if self.operator_visible_entries != sum(
            1 for entry in self.entries if entry.operator_visible
        ):
            raise ValueError(
                "operator_visible_entries must match operator_visible count."
            )
