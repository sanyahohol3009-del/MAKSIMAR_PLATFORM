from __future__ import annotations

from dataclasses import dataclass

from MAKSIMAR_CORE_LIB.oob_dashboard.base_family_manifest_contract import (
    build_base_family_manifest_contract,
)
from MAKSIMAR_CORE_LIB.oob_dashboard.module_mount_eligibility_contract import (
    build_module_mount_eligibility_contract,
)


def _require_non_empty(value: str, field_name: str) -> None:
    if not value or not value.strip():
        raise ValueError(f"{field_name} must be a non-empty string.")


@dataclass(frozen=True, slots=True)
class BaseFamilyMountPlanEntry:
    mount_plan_id: str
    module_id: str
    mount_planned: bool
    mount_allowed: bool
    permission_valid: bool
    operator_visible: bool
    truth_bound: bool
    description: str

    def __post_init__(self) -> None:
        _require_non_empty(self.mount_plan_id, "mount_plan_id")
        _require_non_empty(self.module_id, "module_id")
        _require_non_empty(self.description, "description")

        if not self.mount_planned:
            raise ValueError(
                "mount_planned must remain true for canonical base family mount plan entries."
            )
        if not self.mount_allowed:
            raise ValueError(
                "mount_allowed must remain true for canonical base family mount plan entries."
            )
        if not self.permission_valid:
            raise ValueError(
                "permission_valid must remain true for canonical base family mount plan entries."
            )
        if not self.operator_visible:
            raise ValueError(
                "operator_visible must remain true for canonical base family mount plan entries."
            )
        if not self.truth_bound:
            raise ValueError(
                "truth_bound must remain true for canonical base family mount plan entries."
            )


@dataclass(frozen=True, slots=True)
class BaseFamilyMountPlanContract:
    contract_id: str
    total_entries: int
    mount_planned_entries: int
    operator_visible_entries: int
    truth_bound_entries: int
    entries: tuple[BaseFamilyMountPlanEntry, ...]

    def __post_init__(self) -> None:
        _require_non_empty(self.contract_id, "contract_id")
        if self.total_entries != len(self.entries):
            raise ValueError("total_entries must match len(entries).")
        if self.mount_planned_entries != sum(
            1 for entry in self.entries if entry.mount_planned
        ):
            raise ValueError(
                "mount_planned_entries must match mount_planned count."
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


def build_base_family_mount_plan_contract() -> BaseFamilyMountPlanContract:
    base_manifest = build_base_family_manifest_contract()
    mount_contract = build_module_mount_eligibility_contract()
    mount_map = {entry.module_id: entry for entry in mount_contract.entries}

    entries = tuple(
        BaseFamilyMountPlanEntry(
            mount_plan_id=f"base_family_mount_plan_{index:03d}",
            module_id=entry.module_id,
            mount_planned=True,
            mount_allowed=mount_map[entry.module_id].mount_allowed,
            permission_valid=mount_map[entry.module_id].permission_valid,
            operator_visible=True,
            truth_bound=True,
            description=f"Canonical base family mount plan entry for {entry.module_id}.",
        )
        for index, entry in enumerate(base_manifest.entries, start=1)
    )

    return BaseFamilyMountPlanContract(
        contract_id="base_family_mount_plan_contract_001",
        total_entries=len(entries),
        mount_planned_entries=sum(1 for entry in entries if entry.mount_planned),
        operator_visible_entries=sum(1 for entry in entries if entry.operator_visible),
        truth_bound_entries=sum(1 for entry in entries if entry.truth_bound),
        entries=entries,
    )
