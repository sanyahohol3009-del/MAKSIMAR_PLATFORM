from __future__ import annotations

from dataclasses import dataclass
from typing import Tuple


def _require_non_empty(value: str, field_name: str) -> None:
    if not value or not value.strip():
        raise ValueError(f"{field_name} must be a non-empty string.")


@dataclass(frozen=True, slots=True)
class ExportStatusPanelEntry:
    export_target_id: str
    export_state: str
    artifact_kind: str
    operator_visible: bool
    description: str

    def __post_init__(self) -> None:
        _require_non_empty(self.export_target_id, "export_target_id")
        _require_non_empty(self.export_state, "export_state")
        _require_non_empty(self.artifact_kind, "artifact_kind")
        _require_non_empty(self.description, "description")

        if not self.operator_visible:
            raise ValueError(
                "operator_visible must remain true for canonical export-status panel entries."
            )


@dataclass(frozen=True, slots=True)
class ExportStatusPanelContract:
    panel_id: str
    total_entries: int
    operator_visible_entries: int
    entries: Tuple[ExportStatusPanelEntry, ...]
    operator_visible: bool
    description: str

    def __post_init__(self) -> None:
        _require_non_empty(self.panel_id, "panel_id")
        _require_non_empty(self.description, "description")

        if self.total_entries != len(self.entries):
            raise ValueError("total_entries must match len(entries).")
        if self.operator_visible_entries != sum(
            1 for entry in self.entries if entry.operator_visible
        ):
            raise ValueError(
                "operator_visible_entries must match operator_visible count."
            )
        if not self.operator_visible:
            raise ValueError(
                "operator_visible must remain true for canonical export-status panel contract."
            )


def build_export_status_panel_contract() -> ExportStatusPanelContract:
    entries = (
        ExportStatusPanelEntry(
            export_target_id="project_snapshot_bundle",
            export_state="ready_for_export",
            artifact_kind="snapshot_bundle",
            operator_visible=True,
            description="Canonical project snapshot bundle export status.",
        ),
        ExportStatusPanelEntry(
            export_target_id="validation_report_bundle",
            export_state="ready_for_export",
            artifact_kind="validation_report",
            operator_visible=True,
            description="Canonical validation report export status.",
        ),
        ExportStatusPanelEntry(
            export_target_id="preview_render_bundle",
            export_state="ready_for_export",
            artifact_kind="preview_render",
            operator_visible=True,
            description="Canonical preview render export status.",
        ),
    )

    return ExportStatusPanelContract(
        panel_id="panel_export_status",
        total_entries=len(entries),
        operator_visible_entries=sum(1 for entry in entries if entry.operator_visible),
        entries=entries,
        operator_visible=True,
        description="Canonical export-status panel contract.",
    )
