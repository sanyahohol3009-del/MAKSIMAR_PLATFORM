from __future__ import annotations

from dataclasses import dataclass
from typing import Literal

from MAKSIMAR_CORE_LIB.oob_dashboard.module_manifest_contract import (
    build_module_manifest_contract,
)

SurfaceKind = Literal[
    "foundation_dashboard_surface",
    "interaction_dashboard_surface",
    "optional_dashboard_surface",
]


def _require_non_empty(value: str, field_name: str) -> None:
    if not value or not value.strip():
        raise ValueError(f"{field_name} must be a non-empty string.")


@dataclass(frozen=True, slots=True)
class ModuleDashboardSurfaceEntry:
    surface_entry_id: str
    module_id: str
    surface_id: str
    workspace_id: str
    surface_kind: SurfaceKind
    operator_visible: bool
    truth_bound: bool
    description: str

    def __post_init__(self) -> None:
        _require_non_empty(self.surface_entry_id, "surface_entry_id")
        _require_non_empty(self.module_id, "module_id")
        _require_non_empty(self.surface_id, "surface_id")
        _require_non_empty(self.workspace_id, "workspace_id")
        _require_non_empty(self.description, "description")

        if not self.operator_visible:
            raise ValueError(
                "operator_visible must remain true for canonical module dashboard surface entries."
            )
        if not self.truth_bound:
            raise ValueError(
                "truth_bound must remain true for canonical module dashboard surface entries."
            )


@dataclass(frozen=True, slots=True)
class ModuleDashboardSurfaceContract:
    contract_id: str
    total_entries: int
    operator_visible_entries: int
    truth_bound_entries: int
    entries: tuple[ModuleDashboardSurfaceEntry, ...]

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


def build_module_dashboard_surface_contract() -> ModuleDashboardSurfaceContract:
    manifest_contract = build_module_manifest_contract()

    kind_map = {
        "base_family_module": "foundation_dashboard_surface",
        "operator_module": "interaction_dashboard_surface",
        "optional_product_module": "optional_dashboard_surface",
    }

    entries = tuple(
        ModuleDashboardSurfaceEntry(
            surface_entry_id=f"module_dashboard_surface_{index:03d}",
            module_id=entry.module_id,
            surface_id=f"{entry.module_name}_surface",
            workspace_id=entry.allowed_workspace,
            surface_kind=kind_map[entry.module_role],
            operator_visible=True,
            truth_bound=True,
            description=f"Canonical dashboard surface entry for {entry.module_id}.",
        )
        for index, entry in enumerate(manifest_contract.entries, start=1)
    )

    return ModuleDashboardSurfaceContract(
        contract_id="module_dashboard_surface_contract_001",
        total_entries=len(entries),
        operator_visible_entries=sum(1 for entry in entries if entry.operator_visible),
        truth_bound_entries=sum(1 for entry in entries if entry.truth_bound),
        entries=entries,
    )
