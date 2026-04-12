from __future__ import annotations

from dataclasses import dataclass
from typing import Literal

WorkspaceRole = Literal[
    "foundation_monitoring",
    "operator_surface",
    "expansion_surface",
]

ALL_WORKSPACE_ROLES: tuple[WorkspaceRole, ...] = (
    "foundation_monitoring",
    "operator_surface",
    "expansion_surface",
)


def _require_non_empty(value: str, field_name: str) -> None:
    """Validate that a string field is present and not blank."""
    if not value or not value.strip():
        raise ValueError(f"{field_name} must be a non-empty string.")


@dataclass(frozen=True, slots=True)
class WorkspaceModelEntry:
    """Canonical workspace model entry."""

    workspace_id: str
    workspace_role: WorkspaceRole
    display_target_id: str
    default_panel_count: int
    read_only: bool
    description: str

    def __post_init__(self) -> None:
        _require_non_empty(self.workspace_id, "workspace_id")
        _require_non_empty(self.workspace_role, "workspace_role")
        _require_non_empty(self.display_target_id, "display_target_id")
        _require_non_empty(self.description, "description")

        if self.workspace_role not in ALL_WORKSPACE_ROLES:
            raise ValueError(
                f"workspace_role must be one of {ALL_WORKSPACE_ROLES}, got {self.workspace_role!r}."
            )

        if self.default_panel_count < 0:
            raise ValueError("default_panel_count must be >= 0.")


@dataclass(frozen=True, slots=True)
class WorkspaceModel:
    """Canonical workspace model."""

    model_id: str
    total_entries: int
    read_only_entries: int
    entries: tuple[WorkspaceModelEntry, ...]

    def __post_init__(self) -> None:
        _require_non_empty(self.model_id, "model_id")

        if self.total_entries != len(self.entries):
            raise ValueError(
                "total_entries must match the number of entries in the model."
            )

        if self.read_only_entries != sum(
            1 for entry in self.entries if entry.read_only
        ):
            raise ValueError(
                "read_only_entries must match read_only count."
            )


def build_workspace_model() -> WorkspaceModel:
    """Build canonical workspace model."""
    entries = (
        WorkspaceModelEntry(
            workspace_id="workspace_foundation_001",
            workspace_role="foundation_monitoring",
            display_target_id="display_primary_operator",
            default_panel_count=4,
            read_only=True,
            description=(
                "Canonical foundation monitoring workspace for truth, incidents, "
                "guard chain, and diagnostics surfaces."
            ),
        ),
        WorkspaceModelEntry(
            workspace_id="workspace_operator_001",
            workspace_role="operator_surface",
            display_target_id="display_secondary_diagnostics",
            default_panel_count=3,
            read_only=False,
            description=(
                "Canonical operator workspace for controlled operator-facing "
                "surfaces and guarded interaction."
            ),
        ),
        WorkspaceModelEntry(
            workspace_id="workspace_expansion_001",
            workspace_role="expansion_surface",
            display_target_id="display_tertiary_expansion",
            default_panel_count=2,
            read_only=True,
            description=(
                "Canonical expansion workspace for auxiliary observability and "
                "overflow surfaces."
            ),
        ),
    )

    return WorkspaceModel(
        model_id="workspace_model_001",
        total_entries=len(entries),
        read_only_entries=sum(1 for entry in entries if entry.read_only),
        entries=entries,
    )
