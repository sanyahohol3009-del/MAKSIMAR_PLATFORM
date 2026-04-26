from __future__ import annotations

from dataclasses import dataclass
from typing import Literal

from MAKSIMAR_CORE_LIB.oob_dashboard.module_manifest_contract import (
    build_module_manifest_contract,
)

WidgetKind = Literal[
    "foundation_status_widget",
    "interaction_status_widget",
    "optional_status_widget",
]


def _require_non_empty(value: str, field_name: str) -> None:
    if not value or not value.strip():
        raise ValueError(f"{field_name} must be a non-empty string.")


@dataclass(frozen=True, slots=True)
class ModuleStatusWidgetEntry:
    widget_entry_id: str
    module_id: str
    widget_id: str
    widget_kind: WidgetKind
    operator_visible: bool
    truth_bound: bool
    description: str

    def __post_init__(self) -> None:
        _require_non_empty(self.widget_entry_id, "widget_entry_id")
        _require_non_empty(self.module_id, "module_id")
        _require_non_empty(self.widget_id, "widget_id")
        _require_non_empty(self.description, "description")

        if not self.operator_visible:
            raise ValueError(
                "operator_visible must remain true for canonical module status widget entries."
            )
        if not self.truth_bound:
            raise ValueError(
                "truth_bound must remain true for canonical module status widget entries."
            )


@dataclass(frozen=True, slots=True)
class ModuleStatusWidgetContract:
    contract_id: str
    total_entries: int
    operator_visible_entries: int
    truth_bound_entries: int
    entries: tuple[ModuleStatusWidgetEntry, ...]

    def __post_init__(self) -> None:
        _require_non_empty(self.contract_id, "contract_id")
        if self.total_entries != len(self.entries):
            raise ValueError("total_entries must match len(entries).")
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


def build_module_status_widget_contract() -> ModuleStatusWidgetContract:
    manifest_contract = build_module_manifest_contract()

    kind_map = {
        "base_family_module": "foundation_status_widget",
        "operator_module": "interaction_status_widget",
        "optional_product_module": "optional_status_widget",
    }

    entries = tuple(
        ModuleStatusWidgetEntry(
            widget_entry_id=f"module_status_widget_{index:03d}",
            module_id=entry.module_id,
            widget_id=f"{entry.module_name}_widget",
            widget_kind=kind_map[entry.module_role],
            operator_visible=True,
            truth_bound=True,
            description=f"Canonical status widget entry for {entry.module_id}.",
        )
        for index, entry in enumerate(manifest_contract.entries, start=1)
    )

    return ModuleStatusWidgetContract(
        contract_id="module_status_widget_contract_001",
        total_entries=len(entries),
        operator_visible_entries=sum(1 for entry in entries if entry.operator_visible),
        truth_bound_entries=sum(1 for entry in entries if entry.truth_bound),
        entries=entries,
    )
