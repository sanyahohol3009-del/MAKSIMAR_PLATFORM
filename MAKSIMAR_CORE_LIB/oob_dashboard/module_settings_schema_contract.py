from __future__ import annotations

from dataclasses import dataclass
from typing import Literal

from MAKSIMAR_CORE_LIB.oob_dashboard.module_manifest_contract import (
    build_module_manifest_contract,
)

SettingsScope = Literal[
    "foundation_settings_scope",
    "interaction_settings_scope",
    "optional_settings_scope",
]


def _require_non_empty(value: str, field_name: str) -> None:
    if not value or not value.strip():
        raise ValueError(f"{field_name} must be a non-empty string.")


@dataclass(frozen=True, slots=True)
class ModuleSettingsSchemaEntry:
    settings_entry_id: str
    module_id: str
    schema_id: str
    settings_scope: SettingsScope
    approval_required: bool
    operator_visible: bool
    truth_bound: bool
    description: str

    def __post_init__(self) -> None:
        _require_non_empty(self.settings_entry_id, "settings_entry_id")
        _require_non_empty(self.module_id, "module_id")
        _require_non_empty(self.schema_id, "schema_id")
        _require_non_empty(self.description, "description")

        if not self.operator_visible:
            raise ValueError(
                "operator_visible must remain true for canonical module settings schema entries."
            )
        if not self.truth_bound:
            raise ValueError(
                "truth_bound must remain true for canonical module settings schema entries."
            )


@dataclass(frozen=True, slots=True)
class ModuleSettingsSchemaContract:
    contract_id: str
    total_entries: int
    approval_required_entries: int
    operator_visible_entries: int
    truth_bound_entries: int
    entries: tuple[ModuleSettingsSchemaEntry, ...]

    def __post_init__(self) -> None:
        _require_non_empty(self.contract_id, "contract_id")
        if self.total_entries != len(self.entries):
            raise ValueError("total_entries must match len(entries).")
        if self.approval_required_entries != sum(
            1 for entry in self.entries if entry.approval_required
        ):
            raise ValueError(
                "approval_required_entries must match approval_required count."
            )
        if self.operator_visible_entries != sum(
            1 for entry in self.entries if entry.operator_visible
        ):
            raise ValueError(
                "operator_visible_entries must match operator_visible count."
            )
        if self.truth_bound_entries != sum(
            1 for entry in self.entries if entry.truth_bound
        ):
            raise ValueError("truth_bound_entries must match truth_bound count.")


def build_module_settings_schema_contract() -> ModuleSettingsSchemaContract:
    manifest_contract = build_module_manifest_contract()

    scope_map = {
        "base_family_module": "foundation_settings_scope",
        "operator_module": "interaction_settings_scope",
        "optional_product_module": "optional_settings_scope",
    }

    entries = tuple(
        ModuleSettingsSchemaEntry(
            settings_entry_id=f"module_settings_schema_{index:03d}",
            module_id=entry.module_id,
            schema_id=f"{entry.module_name}_settings_schema",
            settings_scope=scope_map[entry.module_role],
            approval_required=(entry.module_role == "optional_product_module"),
            operator_visible=True,
            truth_bound=True,
            description=f"Canonical settings schema entry for {entry.module_id}.",
        )
        for index, entry in enumerate(manifest_contract.entries, start=1)
    )

    return ModuleSettingsSchemaContract(
        contract_id="module_settings_schema_contract_001",
        total_entries=len(entries),
        approval_required_entries=sum(1 for entry in entries if entry.approval_required),
        operator_visible_entries=sum(1 for entry in entries if entry.operator_visible),
        truth_bound_entries=sum(1 for entry in entries if entry.truth_bound),
        entries=entries,
    )
