from __future__ import annotations

from dataclasses import dataclass
from typing import Tuple


def _require_non_empty(value: str, field_name: str) -> None:
    if not value or not value.strip():
        raise ValueError(f"{field_name} must be a non-empty string.")


@dataclass(frozen=True, slots=True)
class ValidationAssetsPanelEntry:
    asset_id: str
    validation_state: str
    asset_kind: str
    operator_visible: bool
    description: str

    def __post_init__(self) -> None:
        _require_non_empty(self.asset_id, "asset_id")
        _require_non_empty(self.validation_state, "validation_state")
        _require_non_empty(self.asset_kind, "asset_kind")
        _require_non_empty(self.description, "description")

        if not self.operator_visible:
            raise ValueError(
                "operator_visible must remain true for canonical validation-assets panel entries."
            )


@dataclass(frozen=True, slots=True)
class ValidationAssetsPanelContract:
    panel_id: str
    total_entries: int
    validated_entries: int
    operator_visible_entries: int
    entries: Tuple[ValidationAssetsPanelEntry, ...]
    operator_visible: bool
    description: str

    def __post_init__(self) -> None:
        _require_non_empty(self.panel_id, "panel_id")
        _require_non_empty(self.description, "description")

        if self.total_entries != len(self.entries):
            raise ValueError("total_entries must match len(entries).")
        if self.validated_entries != sum(
            1 for entry in self.entries if entry.validation_state == "validated"
        ):
            raise ValueError("validated_entries must match validated count.")
        if self.operator_visible_entries != sum(
            1 for entry in self.entries if entry.operator_visible
        ):
            raise ValueError(
                "operator_visible_entries must match operator_visible count."
            )
        if not self.operator_visible:
            raise ValueError(
                "operator_visible must remain true for canonical validation-assets panel contract."
            )


def build_validation_assets_panel_contract() -> ValidationAssetsPanelContract:
    entries = (
        ValidationAssetsPanelEntry(
            asset_id="validation_asset_surface_map",
            validation_state="validated",
            asset_kind="surface_map",
            operator_visible=True,
            description="Canonical validated surface-map asset.",
        ),
        ValidationAssetsPanelEntry(
            asset_id="validation_asset_toolpath_data",
            validation_state="validated",
            asset_kind="toolpath_data",
            operator_visible=True,
            description="Canonical validated toolpath asset.",
        ),
        ValidationAssetsPanelEntry(
            asset_id="validation_asset_material_profile",
            validation_state="validated",
            asset_kind="material_profile",
            operator_visible=True,
            description="Canonical validated material-profile asset.",
        ),
    )

    return ValidationAssetsPanelContract(
        panel_id="panel_validation_assets",
        total_entries=len(entries),
        validated_entries=sum(
            1 for entry in entries if entry.validation_state == "validated"
        ),
        operator_visible_entries=sum(1 for entry in entries if entry.operator_visible),
        entries=entries,
        operator_visible=True,
        description="Canonical validation-assets panel contract.",
    )
