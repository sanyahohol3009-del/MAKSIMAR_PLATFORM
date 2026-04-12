from __future__ import annotations

from dataclasses import dataclass

from MAKSIMAR_CORE_LIB.oob_dashboard.workspace_registry_contract import (
    build_workspace_registry_contract,
)


def _require_non_empty(value: str, field_name: str) -> None:
    """Validate that a string field is present and not blank."""
    if not value or not value.strip():
        raise ValueError(f"{field_name} must be a non-empty string.")


@dataclass(frozen=True, slots=True)
class ViewCompositionModelEntry:
    """Canonical view composition model entry."""

    view_id: str
    workspace_id: str
    composition_family: str
    operator_visible: bool
    description: str

    def __post_init__(self) -> None:
        _require_non_empty(self.view_id, "view_id")
        _require_non_empty(self.workspace_id, "workspace_id")
        _require_non_empty(self.composition_family, "composition_family")
        _require_non_empty(self.description, "description")

        if not self.operator_visible:
            raise ValueError(
                "operator_visible must remain true for canonical view composition model entries."
            )


@dataclass(frozen=True, slots=True)
class ViewCompositionModel:
    """Canonical view composition model."""

    model_id: str
    total_entries: int
    operator_visible_entries: int
    entries: tuple[ViewCompositionModelEntry, ...]

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


def _resolve_composition_family(workspace_id: str) -> str:
    """Resolve canonical composition family from workspace id."""
    if workspace_id == "workspace_foundation_001":
        return "foundation_view_family"
    if workspace_id == "workspace_operator_001":
        return "operator_view_family"
    return "expansion_view_family"


def build_view_composition_model() -> ViewCompositionModel:
    """Build canonical view composition model."""
    workspace_registry_contract = build_workspace_registry_contract()

    entries = tuple(
        ViewCompositionModelEntry(
            view_id=f"view_composition_{index + 1:03d}",
            workspace_id=entry.workspace_id,
            composition_family=_resolve_composition_family(entry.workspace_id),
            operator_visible=True,
            description=(
                "Canonical view composition model entry derived from "
                f"{entry.workspace_id}."
            ),
        )
        for index, entry in enumerate(workspace_registry_contract.entries)
    )

    return ViewCompositionModel(
        model_id="view_composition_model_001",
        total_entries=len(entries),
        operator_visible_entries=sum(
            1 for entry in entries if entry.operator_visible
        ),
        entries=entries,
    )
