from __future__ import annotations

from dataclasses import dataclass

from MAKSIMAR_CORE_LIB.oob_dashboard.module_compatibility_contract import (
    build_module_compatibility_contract,
)


def _require_non_empty(value: str, field_name: str) -> None:
    if not value or not value.strip():
        raise ValueError(f"{field_name} must be a non-empty string.")


@dataclass(frozen=True, slots=True)
class ModuleMountEligibilityEntry:
    mount_entry_id: str
    module_id: str
    mount_allowed: bool
    workspace_allowed: bool
    permission_valid: bool
    operator_visible: bool
    truth_bound: bool
    description: str

    def __post_init__(self) -> None:
        _require_non_empty(self.mount_entry_id, "mount_entry_id")
        _require_non_empty(self.module_id, "module_id")
        _require_non_empty(self.description, "description")

        if not self.mount_allowed:
            raise ValueError(
                "mount_allowed must remain true for canonical module mount eligibility entries."
            )
        if not self.workspace_allowed:
            raise ValueError(
                "workspace_allowed must remain true for canonical module mount eligibility entries."
            )
        if not self.permission_valid:
            raise ValueError(
                "permission_valid must remain true for canonical module mount eligibility entries."
            )
        if not self.operator_visible:
            raise ValueError(
                "operator_visible must remain true for canonical module mount eligibility entries."
            )
        if not self.truth_bound:
            raise ValueError(
                "truth_bound must remain true for canonical module mount eligibility entries."
            )


@dataclass(frozen=True, slots=True)
class ModuleMountEligibilityContract:
    contract_id: str
    total_entries: int
    mount_allowed_entries: int
    permission_valid_entries: int
    operator_visible_entries: int
    truth_bound_entries: int
    entries: tuple[ModuleMountEligibilityEntry, ...]

    def __post_init__(self) -> None:
        _require_non_empty(self.contract_id, "contract_id")
        if self.total_entries != len(self.entries):
            raise ValueError("total_entries must match len(entries).")
        if self.mount_allowed_entries != sum(
            1 for entry in self.entries if entry.mount_allowed
        ):
            raise ValueError(
                "mount_allowed_entries must match mount_allowed count."
            )
        if self.permission_valid_entries != sum(
            1 for entry in self.entries if entry.permission_valid
        ):
            raise ValueError(
                "permission_valid_entries must match permission_valid count."
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


def build_module_mount_eligibility_contract() -> ModuleMountEligibilityContract:
    compatibility_contract = build_module_compatibility_contract()

    entries = tuple(
        ModuleMountEligibilityEntry(
            mount_entry_id=f"module_mount_eligibility_{index:03d}",
            module_id=entry.module_id,
            mount_allowed=entry.mount_eligible,
            workspace_allowed=True,
            permission_valid=entry.permission_valid,
            operator_visible=True,
            truth_bound=True,
            description=f"Canonical mount eligibility entry for {entry.module_id}.",
        )
        for index, entry in enumerate(compatibility_contract.entries, start=1)
    )

    return ModuleMountEligibilityContract(
        contract_id="module_mount_eligibility_contract_001",
        total_entries=len(entries),
        mount_allowed_entries=sum(1 for entry in entries if entry.mount_allowed),
        permission_valid_entries=sum(1 for entry in entries if entry.permission_valid),
        operator_visible_entries=sum(1 for entry in entries if entry.operator_visible),
        truth_bound_entries=sum(1 for entry in entries if entry.truth_bound),
        entries=entries,
    )
