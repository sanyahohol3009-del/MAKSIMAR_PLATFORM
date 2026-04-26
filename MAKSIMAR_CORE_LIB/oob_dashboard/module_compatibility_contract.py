from __future__ import annotations

from dataclasses import dataclass

from MAKSIMAR_CORE_LIB.oob_dashboard.module_manifest_contract import (
    build_module_manifest_contract,
)
from MAKSIMAR_CORE_LIB.oob_dashboard.module_permission_matrix_contract import (
    build_module_permission_matrix_contract,
)


def _require_non_empty(value: str, field_name: str) -> None:
    if not value or not value.strip():
        raise ValueError(f"{field_name} must be a non-empty string.")


@dataclass(frozen=True, slots=True)
class ModuleCompatibilityEntry:
    """Canonical module compatibility entry."""

    compatibility_entry_id: str
    module_id: str
    mount_eligible: bool
    permission_valid: bool
    compatible_with_base_family: bool
    operator_visible: bool
    truth_bound: bool
    description: str

    def __post_init__(self) -> None:
        _require_non_empty(self.compatibility_entry_id, "compatibility_entry_id")
        _require_non_empty(self.module_id, "module_id")
        _require_non_empty(self.description, "description")

        if not self.mount_eligible:
            raise ValueError(
                "mount_eligible must remain true for canonical module compatibility entries."
            )

        if not self.permission_valid:
            raise ValueError(
                "permission_valid must remain true for canonical module compatibility entries."
            )

        if not self.compatible_with_base_family:
            raise ValueError(
                "compatible_with_base_family must remain true for canonical module compatibility entries."
            )

        if not self.operator_visible:
            raise ValueError(
                "operator_visible must remain true for canonical module compatibility entries."
            )

        if not self.truth_bound:
            raise ValueError(
                "truth_bound must remain true for canonical module compatibility entries."
            )


@dataclass(frozen=True, slots=True)
class ModuleCompatibilityContract:
    """Canonical module compatibility contract."""

    contract_id: str
    total_entries: int
    mount_eligible_entries: int
    permission_valid_entries: int
    compatible_entries: int
    operator_visible_entries: int
    truth_bound_entries: int
    entries: tuple[ModuleCompatibilityEntry, ...]

    def __post_init__(self) -> None:
        _require_non_empty(self.contract_id, "contract_id")

        if self.total_entries != len(self.entries):
            raise ValueError("total_entries must match len(entries).")

        if self.mount_eligible_entries != sum(
            1 for entry in self.entries if entry.mount_eligible
        ):
            raise ValueError(
                "mount_eligible_entries must match mount_eligible count."
            )

        if self.permission_valid_entries != sum(
            1 for entry in self.entries if entry.permission_valid
        ):
            raise ValueError(
                "permission_valid_entries must match permission_valid count."
            )

        if self.compatible_entries != sum(
            1 for entry in self.entries if entry.compatible_with_base_family
        ):
            raise ValueError(
                "compatible_entries must match compatible_with_base_family count."
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
            raise ValueError(
                "truth_bound_entries must match truth_bound count."
            )


def build_module_compatibility_contract() -> ModuleCompatibilityContract:
    """Build canonical module compatibility contract."""
    manifest_contract = build_module_manifest_contract()
    permission_contract = build_module_permission_matrix_contract()

    permission_map = {entry.module_id: entry for entry in permission_contract.entries}

    entries = tuple(
        ModuleCompatibilityEntry(
            compatibility_entry_id=f"module_compatibility_{index:03d}",
            module_id=entry.module_id,
            mount_eligible=True,
            permission_valid=entry.module_id in permission_map,
            compatible_with_base_family=True,
            operator_visible=True,
            truth_bound=True,
            description=f"Canonical compatibility entry for {entry.module_id}.",
        )
        for index, entry in enumerate(manifest_contract.entries, start=1)
    )

    return ModuleCompatibilityContract(
        contract_id="module_compatibility_contract_001",
        total_entries=len(entries),
        mount_eligible_entries=sum(
            1 for entry in entries if entry.mount_eligible
        ),
        permission_valid_entries=sum(
            1 for entry in entries if entry.permission_valid
        ),
        compatible_entries=sum(
            1 for entry in entries if entry.compatible_with_base_family
        ),
        operator_visible_entries=sum(
            1 for entry in entries if entry.operator_visible
        ),
        truth_bound_entries=sum(
            1 for entry in entries if entry.truth_bound
        ),
        entries=entries,
    )
