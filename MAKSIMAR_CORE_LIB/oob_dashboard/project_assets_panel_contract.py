from __future__ import annotations

from dataclasses import dataclass
from typing import Tuple


def _require_non_empty(value: str, field_name: str) -> None:
    if not value or not value.strip():
        raise ValueError(f"{field_name} must be a non-empty string.")


@dataclass(frozen=True, slots=True)
class ProjectAssetsPanelEntry:
    project_asset_id: str
    asset_state: str
    asset_kind: str
    operator_visible: bool
    description: str

    def __post_init__(self) -> None:
        _require_non_empty(self.project_asset_id, "project_asset_id")
        _require_non_empty(self.asset_state, "asset_state")
        _require_non_empty(self.asset_kind, "asset_kind")
        _require_non_empty(self.description, "description")

        if not self.operator_visible:
            raise ValueError(
                "operator_visible must remain true for canonical project-assets panel entries."
            )


@dataclass(frozen=True, slots=True)
class ProjectAssetsPanelContract:
    panel_id: str
    total_entries: int
    ready_entries: int
    operator_visible_entries: int
    entries: Tuple[ProjectAssetsPanelEntry, ...]
    operator_visible: bool
    description: str

    def __post_init__(self) -> None:
        _require_non_empty(self.panel_id, "panel_id")
        _require_non_empty(self.description, "description")

        if self.total_entries != len(self.entries):
            raise ValueError("total_entries must match len(entries).")
        if self.ready_entries != sum(
            1 for entry in self.entries if entry.asset_state == "ready"
        ):
            raise ValueError("ready_entries must match ready count.")
        if self.operator_visible_entries != sum(
            1 for entry in self.entries if entry.operator_visible
        ):
            raise ValueError(
                "operator_visible_entries must match operator_visible count."
            )
        if not self.operator_visible:
            raise ValueError(
                "operator_visible must remain true for canonical project-assets panel contract."
            )


def build_project_assets_panel_contract() -> ProjectAssetsPanelContract:
    entries = (
        ProjectAssetsPanelEntry(
            project_asset_id="project_asset_description_txt",
            asset_state="ready",
            asset_kind="description_file",
            operator_visible=True,
            description="Canonical project description asset.",
        ),
        ProjectAssetsPanelEntry(
            project_asset_id="project_asset_system_overview_md",
            asset_state="ready",
            asset_kind="system_overview",
            operator_visible=True,
            description="Canonical system-overview asset.",
        ),
        ProjectAssetsPanelEntry(
            project_asset_id="project_asset_preview_render_png",
            asset_state="ready",
            asset_kind="preview_render",
            operator_visible=True,
            description="Canonical preview-render project asset.",
        ),
    )

    return ProjectAssetsPanelContract(
        panel_id="panel_project_assets",
        total_entries=len(entries),
        ready_entries=sum(1 for entry in entries if entry.asset_state == "ready"),
        operator_visible_entries=sum(1 for entry in entries if entry.operator_visible),
        entries=entries,
        operator_visible=True,
        description="Canonical project-assets panel contract.",
    )
