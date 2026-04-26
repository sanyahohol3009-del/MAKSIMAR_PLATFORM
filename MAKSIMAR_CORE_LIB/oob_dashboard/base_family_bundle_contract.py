from __future__ import annotations

from dataclasses import dataclass

from MAKSIMAR_CORE_LIB.oob_dashboard.base_family_manifest_contract import (
    build_base_family_manifest_contract,
)
from MAKSIMAR_CORE_LIB.oob_dashboard.module_dashboard_surface_contract import (
    build_module_dashboard_surface_contract,
)


def _require_non_empty(value: str, field_name: str) -> None:
    if not value or not value.strip():
        raise ValueError(f"{field_name} must be a non-empty string.")


@dataclass(frozen=True, slots=True)
class BaseFamilyBundleEntry:
    base_family_bundle_id: str
    module_id: str
    surface_id: str
    bundled: bool
    operator_visible: bool
    truth_bound: bool
    description: str

    def __post_init__(self) -> None:
        _require_non_empty(self.base_family_bundle_id, "base_family_bundle_id")
        _require_non_empty(self.module_id, "module_id")
        _require_non_empty(self.surface_id, "surface_id")
        _require_non_empty(self.description, "description")

        if not self.bundled:
            raise ValueError(
                "bundled must remain true for canonical base family bundle entries."
            )
        if not self.operator_visible:
            raise ValueError(
                "operator_visible must remain true for canonical base family bundle entries."
            )
        if not self.truth_bound:
            raise ValueError(
                "truth_bound must remain true for canonical base family bundle entries."
            )


@dataclass(frozen=True, slots=True)
class BaseFamilyBundleContract:
    contract_id: str
    total_entries: int
    bundled_entries: int
    operator_visible_entries: int
    truth_bound_entries: int
    entries: tuple[BaseFamilyBundleEntry, ...]

    def __post_init__(self) -> None:
        _require_non_empty(self.contract_id, "contract_id")
        if self.total_entries != len(self.entries):
            raise ValueError("total_entries must match len(entries).")
        if self.bundled_entries != sum(1 for entry in self.entries if entry.bundled):
            raise ValueError("bundled_entries must match bundled count.")
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


def build_base_family_bundle_contract() -> BaseFamilyBundleContract:
    base_manifest = build_base_family_manifest_contract()
    surface_contract = build_module_dashboard_surface_contract()
    surface_map = {entry.module_id: entry.surface_id for entry in surface_contract.entries}

    entries = tuple(
        BaseFamilyBundleEntry(
            base_family_bundle_id=f"base_family_bundle_{index:03d}",
            module_id=entry.module_id,
            surface_id=surface_map[entry.module_id],
            bundled=True,
            operator_visible=True,
            truth_bound=True,
            description=f"Canonical base family bundle entry for {entry.module_id}.",
        )
        for index, entry in enumerate(base_manifest.entries, start=1)
    )

    return BaseFamilyBundleContract(
        contract_id="base_family_bundle_contract_001",
        total_entries=len(entries),
        bundled_entries=sum(1 for entry in entries if entry.bundled),
        operator_visible_entries=sum(1 for entry in entries if entry.operator_visible),
        truth_bound_entries=sum(1 for entry in entries if entry.truth_bound),
        entries=entries,
    )
