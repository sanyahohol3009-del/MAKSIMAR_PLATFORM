from __future__ import annotations

from dataclasses import dataclass

from MAKSIMAR_CORE_LIB.oob_dashboard.workspace_contract import (
    build_workspace_contract,
)


def _require_non_empty(value: str, field_name: str) -> None:
    """Validate that a string field is present and not blank."""
    if not value or not value.strip():
        raise ValueError(f"{field_name} must be a non-empty string.")


@dataclass(frozen=True, slots=True)
class PanelOrchestrationEntry:
    """Canonical panel orchestration entry."""

    orchestration_id: str
    workspace_id: str
    orchestration_state: str
    operator_visible: bool
    description: str

    def __post_init__(self) -> None:
        _require_non_empty(self.orchestration_id, "orchestration_id")
        _require_non_empty(self.workspace_id, "workspace_id")
        _require_non_empty(self.orchestration_state, "orchestration_state")
        _require_non_empty(self.description, "description")
        if not self.operator_visible:
            raise ValueError(
                "operator_visible must remain true for canonical panel orchestration entries."
            )


@dataclass(frozen=True, slots=True)
class PanelOrchestrationModel:
    """Canonical panel orchestration model."""

    model_id: str
    total_entries: int
    operator_visible_entries: int
    entries: tuple[PanelOrchestrationEntry, ...]

    def __post_init__(self) -> None:
        _require_non_empty(self.model_id, "model_id")
        if self.total_entries != len(self.entries):
            raise ValueError(
                "total_entries must match the number of entries in the model."
            )
        if self.operator_visible_entries != sum(
            1 for entry in self.entries if entry.operator_visible
        ):
            raise ValueError(
                "operator_visible_entries must match operator_visible count."
            )


def build_panel_orchestration_model() -> PanelOrchestrationModel:
    """Build canonical panel orchestration model.

    After demolition, orchestration is rebuilt only from surviving workspace truth.
    """
    workspace_contract = build_workspace_contract()

    entries = tuple(
        PanelOrchestrationEntry(
            orchestration_id=f"panel_orchestration_{index + 1:03d}",
            workspace_id=entry.workspace_id,
            orchestration_state="panel_orchestration_active",
            operator_visible=True,
            description=(
                "Canonical panel orchestration entry derived from "
                f"{entry.workspace_id}."
            ),
        )
        for index, entry in enumerate(workspace_contract.entries)
    )

    return PanelOrchestrationModel(
        model_id="panel_orchestration_model_001",
        total_entries=len(entries),
        operator_visible_entries=sum(
            1 for entry in entries if entry.operator_visible
        ),
        entries=entries,
    )
