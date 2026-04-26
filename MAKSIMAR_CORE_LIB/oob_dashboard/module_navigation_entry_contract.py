from __future__ import annotations

from dataclasses import dataclass
from typing import Literal

from MAKSIMAR_CORE_LIB.oob_dashboard.module_manifest_contract import (
    build_module_manifest_contract,
)

NavigationGroup = Literal[
    "foundation_navigation_group",
    "interaction_navigation_group",
    "optional_navigation_group",
]


def _require_non_empty(value: str, field_name: str) -> None:
    if not value or not value.strip():
        raise ValueError(f"{field_name} must be a non-empty string.")


@dataclass(frozen=True, slots=True)
class ModuleNavigationEntry:
    navigation_entry_id: str
    module_id: str
    navigation_id: str
    navigation_group: NavigationGroup
    visible_in_menu: bool
    operator_visible: bool
    truth_bound: bool
    description: str

    def __post_init__(self) -> None:
        _require_non_empty(self.navigation_entry_id, "navigation_entry_id")
        _require_non_empty(self.module_id, "module_id")
        _require_non_empty(self.navigation_id, "navigation_id")
        _require_non_empty(self.description, "description")

        if not self.visible_in_menu:
            raise ValueError(
                "visible_in_menu must remain true for canonical module navigation entries."
            )
        if not self.operator_visible:
            raise ValueError(
                "operator_visible must remain true for canonical module navigation entries."
            )
        if not self.truth_bound:
            raise ValueError(
                "truth_bound must remain true for canonical module navigation entries."
            )


@dataclass(frozen=True, slots=True)
class ModuleNavigationEntryContract:
    contract_id: str
    total_entries: int
    visible_in_menu_entries: int
    operator_visible_entries: int
    truth_bound_entries: int
    entries: tuple[ModuleNavigationEntry, ...]

    def __post_init__(self) -> None:
        _require_non_empty(self.contract_id, "contract_id")
        if self.total_entries != len(self.entries):
            raise ValueError("total_entries must match len(entries).")
        if self.visible_in_menu_entries != sum(
            1 for entry in self.entries if entry.visible_in_menu
        ):
            raise ValueError(
                "visible_in_menu_entries must match visible_in_menu count."
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


def build_module_navigation_entry_contract() -> ModuleNavigationEntryContract:
    manifest_contract = build_module_manifest_contract()

    group_map = {
        "base_family_module": "foundation_navigation_group",
        "operator_module": "interaction_navigation_group",
        "optional_product_module": "optional_navigation_group",
    }

    entries = tuple(
        ModuleNavigationEntry(
            navigation_entry_id=f"module_navigation_entry_{index:03d}",
            module_id=entry.module_id,
            navigation_id=f"{entry.module_name}_nav",
            navigation_group=group_map[entry.module_role],
            visible_in_menu=True,
            operator_visible=True,
            truth_bound=True,
            description=f"Canonical navigation entry for {entry.module_id}.",
        )
        for index, entry in enumerate(manifest_contract.entries, start=1)
    )

    return ModuleNavigationEntryContract(
        contract_id="module_navigation_entry_contract_001",
        total_entries=len(entries),
        visible_in_menu_entries=sum(1 for entry in entries if entry.visible_in_menu),
        operator_visible_entries=sum(1 for entry in entries if entry.operator_visible),
        truth_bound_entries=sum(1 for entry in entries if entry.truth_bound),
        entries=entries,
    )
