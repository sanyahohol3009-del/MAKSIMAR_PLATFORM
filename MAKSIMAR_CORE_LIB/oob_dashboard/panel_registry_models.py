from __future__ import annotations

from dataclasses import dataclass

from MAKSIMAR_CORE_LIB.oob_dashboard.panel_id_vocabulary_normalization import (
    normalize_panel_id,
)


def _require_non_empty(value: str, field_name: str) -> None:
    """Validate that a string field is present and not blank."""
    if not value or not value.strip():
        raise ValueError(f"{field_name} must be a non-empty string.")


@dataclass(frozen=True, slots=True)
class PanelRegistryEntry:
    """Canonical panel registry entry."""

    panel_id: str
    panel_family: str
    workspace_id: str
    default_display_target_id: str
    operator_visible: bool
    description: str

    def __post_init__(self) -> None:
        _require_non_empty(self.panel_id, "panel_id")
        _require_non_empty(self.panel_family, "panel_family")
        _require_non_empty(self.workspace_id, "workspace_id")
        _require_non_empty(self.default_display_target_id, "default_display_target_id")
        _require_non_empty(self.description, "description")

        normalized = normalize_panel_id(self.panel_id)
        if normalized != self.panel_id:
            raise ValueError(
                f"panel_id must already be normalized: expected {normalized!r}, got {self.panel_id!r}."
            )

        if not self.operator_visible:
            raise ValueError(
                "operator_visible must remain true for canonical panel registry entries."
            )


@dataclass(frozen=True, slots=True)
class PanelRegistryModel:
    """Canonical panel registry model."""

    model_id: str
    total_entries: int
    operator_visible_entries: int
    entries: tuple[PanelRegistryEntry, ...]

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


def build_panel_registry_model() -> PanelRegistryModel:
    """Build canonical panel registry model."""
    entries = (
        PanelRegistryEntry(
            panel_id="panel_system_status_001",
            panel_family="foundation_status",
            workspace_id="workspace_foundation_001",
            default_display_target_id="display_primary_operator",
            operator_visible=True,
            description="Canonical system-status panel registry entry.",
        ),
        PanelRegistryEntry(
            panel_id="panel_guard_chain_001",
            panel_family="foundation_guard",
            workspace_id="workspace_foundation_001",
            default_display_target_id="display_primary_operator",
            operator_visible=True,
            description="Canonical guard-chain panel registry entry.",
        ),
        PanelRegistryEntry(
            panel_id="panel_incidents_001",
            panel_family="foundation_incidents",
            workspace_id="workspace_foundation_001",
            default_display_target_id="display_secondary_diagnostics",
            operator_visible=True,
            description="Canonical incidents panel registry entry.",
        ),
        PanelRegistryEntry(
            panel_id="panel_logs_001",
            panel_family="foundation_logs",
            workspace_id="workspace_foundation_001",
            default_display_target_id="display_tertiary_expansion",
            operator_visible=True,
            description="Canonical logs panel registry entry.",
        ),
        PanelRegistryEntry(
            panel_id="panel_topology_001",
            panel_family="foundation_topology",
            workspace_id="workspace_operator_001",
            default_display_target_id="display_secondary_diagnostics",
            operator_visible=True,
            description="Canonical topology panel registry entry.",
        ),
    )

    return PanelRegistryModel(
        model_id="panel_registry_model_001",
        total_entries=len(entries),
        operator_visible_entries=sum(
            1 for entry in entries if entry.operator_visible
        ),
        entries=entries,
    )
