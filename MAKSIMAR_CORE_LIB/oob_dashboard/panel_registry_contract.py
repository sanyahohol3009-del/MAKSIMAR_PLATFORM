from __future__ import annotations

from dataclasses import dataclass

from MAKSIMAR_CORE_LIB.oob_dashboard.panel_id_vocabulary_normalization import (
    normalize_panel_id,
)


def _require_non_empty(value: str, field_name: str) -> None:
    if not value or not value.strip():
        raise ValueError(f"{field_name} must be a non-empty string.")


@dataclass(frozen=True, slots=True)
class PanelRegistryEntry:
    """Canonical panel registry entry."""

    panel_id: str
    normalized_panel_id: str
    label: str
    category: str
    panel_family: str
    panel_kind: str
    panel_role: str
    workspace_id: str
    default_display_target_id: str
    visible_in_sidebar: bool
    operator_visible: bool
    description: str

    def __post_init__(self) -> None:
        _require_non_empty(self.panel_id, "panel_id")
        _require_non_empty(self.normalized_panel_id, "normalized_panel_id")
        _require_non_empty(self.label, "label")
        _require_non_empty(self.category, "category")
        _require_non_empty(self.panel_family, "panel_family")
        _require_non_empty(self.panel_kind, "panel_kind")
        _require_non_empty(self.panel_role, "panel_role")
        _require_non_empty(self.workspace_id, "workspace_id")
        _require_non_empty(self.default_display_target_id, "default_display_target_id")
        _require_non_empty(self.description, "description")

        if self.normalized_panel_id != normalize_panel_id(self.panel_id):
            raise ValueError(
                "normalized_panel_id must match normalize_panel_id(panel_id)."
            )

        if not self.operator_visible:
            raise ValueError("operator_visible must remain true for canonical entries.")


@dataclass(frozen=True, slots=True)
class PanelRegistryContract:
    """Canonical panel registry contract."""

    contract_id: str
    total_panels: int
    visible_in_sidebar_panels: int
    operator_visible_panels: int
    panels: tuple[PanelRegistryEntry, ...]

    def __post_init__(self) -> None:
        _require_non_empty(self.contract_id, "contract_id")

        if self.total_panels != len(self.panels):
            raise ValueError("total_panels must match len(panels).")
        if self.visible_in_sidebar_panels != sum(
            1 for panel in self.panels if panel.visible_in_sidebar
        ):
            raise ValueError(
                "visible_in_sidebar_panels must match visible_in_sidebar count."
            )
        if self.operator_visible_panels != sum(
            1 for panel in self.panels if panel.operator_visible
        ):
            raise ValueError(
                "operator_visible_panels must match operator_visible count."
            )


def build_panel_registry_contract() -> PanelRegistryContract:
    """Build canonical panel registry contract."""
    panels = (
        PanelRegistryEntry(
            panel_id="panel_consistency",
            normalized_panel_id=normalize_panel_id("panel_consistency"),
            label="Consistency",
            category="core",
            panel_family="read_only_monitoring",
            panel_kind="summary",
            panel_role="read_only_monitoring",
            workspace_id="workspace_foundation_001",
            default_display_target_id="display_secondary_diagnostics",
            visible_in_sidebar=True,
            operator_visible=True,
            description="Canonical consistency panel.",
        ),
        PanelRegistryEntry(
            panel_id="panel_snapshot",
            normalized_panel_id=normalize_panel_id("panel_snapshot"),
            label="Snapshot",
            category="core",
            panel_family="read_only_monitoring",
            panel_kind="summary",
            panel_role="read_only_monitoring",
            workspace_id="workspace_foundation_001",
            default_display_target_id="display_primary_operator",
            visible_in_sidebar=True,
            operator_visible=True,
            description="Canonical snapshot panel.",
        ),
        PanelRegistryEntry(
            panel_id="panel_incident",
            normalized_panel_id=normalize_panel_id("panel_incident"),
            label="Incident",
            category="core",
            panel_family="read_only_monitoring",
            panel_kind="details",
            panel_role="read_only_monitoring",
            workspace_id="workspace_foundation_001",
            default_display_target_id="display_secondary_diagnostics",
            visible_in_sidebar=True,
            operator_visible=True,
            description="Canonical incident panel.",
        ),
        PanelRegistryEntry(
            panel_id="panel_diagnostics",
            normalized_panel_id=normalize_panel_id("panel_diagnostics"),
            label="Diagnostics",
            category="core",
            panel_family="read_only_monitoring",
            panel_kind="details",
            panel_role="read_only_monitoring",
            workspace_id="workspace_expansion_observability",
            default_display_target_id="display_secondary_diagnostics",
            visible_in_sidebar=True,
            operator_visible=True,
            description="Canonical diagnostics panel.",
        ),
        PanelRegistryEntry(
            panel_id="panel_chat",
            normalized_panel_id=normalize_panel_id("panel_chat"),
            label="Chat",
            category="control",
            panel_family="control",
            panel_kind="conversation",
            panel_role="control_surface",
            workspace_id="workspace_operator_main",
            default_display_target_id="display_primary_operator",
            visible_in_sidebar=True,
            operator_visible=True,
            description="Canonical chat panel.",
        ),
        PanelRegistryEntry(
            panel_id="panel_settings",
            normalized_panel_id=normalize_panel_id("panel_settings"),
            label="Settings",
            category="control",
            panel_family="control",
            panel_kind="settings",
            panel_role="control_surface",
            workspace_id="workspace_operator_main",
            default_display_target_id="display_primary_operator",
            visible_in_sidebar=True,
            operator_visible=True,
            description="Canonical settings panel.",
        ),
        PanelRegistryEntry(
            panel_id="panel_gesture_control",
            normalized_panel_id=normalize_panel_id("panel_gesture_control"),
            label="Gesture Control",
            category="control",
            panel_family="control",
            panel_kind="gesture",
            panel_role="control_surface",
            workspace_id="workspace_operator_main",
            default_display_target_id="display_primary_operator",
            visible_in_sidebar=True,
            operator_visible=True,
            description="Canonical gesture control panel.",
        ),
    )

    return PanelRegistryContract(
        contract_id="panel_registry_contract_001",
        total_panels=len(panels),
        visible_in_sidebar_panels=sum(
            1 for panel in panels if panel.visible_in_sidebar
        ),
        operator_visible_panels=sum(
            1 for panel in panels if panel.operator_visible
        ),
        panels=panels,
    )


def build_dashboard_panel_registry_contract() -> PanelRegistryContract:
    return build_panel_registry_contract()
