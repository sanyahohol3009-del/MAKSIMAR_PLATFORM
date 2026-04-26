from __future__ import annotations

from dataclasses import dataclass
from typing import Literal

from MAKSIMAR_CORE_LIB.oob_dashboard.module_manifest_contract import (
    build_module_manifest_contract,
)


PermissionLevel = Literal[
    "read_only",
    "operator_interaction",
    "optional_extension",
]


def _require_non_empty(value: str, field_name: str) -> None:
    if not value or not value.strip():
        raise ValueError(f"{field_name} must be a non-empty string.")


@dataclass(frozen=True, slots=True)
class ModulePermissionMatrixEntry:
    """Canonical module permission matrix entry."""

    permission_entry_id: str
    module_id: str
    permission_level: PermissionLevel
    approval_required: bool
    operator_visible: bool
    truth_bound: bool
    description: str

    def __post_init__(self) -> None:
        _require_non_empty(self.permission_entry_id, "permission_entry_id")
        _require_non_empty(self.module_id, "module_id")
        _require_non_empty(self.description, "description")

        if not self.operator_visible:
            raise ValueError(
                "operator_visible must remain true for canonical module permission entries."
            )

        if not self.truth_bound:
            raise ValueError(
                "truth_bound must remain true for canonical module permission entries."
            )

        if self.permission_level == "read_only" and self.approval_required:
            raise ValueError(
                "read_only permission entries must not require approval."
            )


@dataclass(frozen=True, slots=True)
class ModulePermissionMatrixContract:
    """Canonical module permission matrix contract."""

    contract_id: str
    total_entries: int
    approval_required_entries: int
    operator_visible_entries: int
    truth_bound_entries: int
    entries: tuple[ModulePermissionMatrixEntry, ...]

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
            raise ValueError(
                "truth_bound_entries must match truth_bound count."
            )


def build_module_permission_matrix_contract() -> ModulePermissionMatrixContract:
    """Build canonical module permission matrix contract."""
    manifest_contract = build_module_manifest_contract()

    entries = tuple(
        ModulePermissionMatrixEntry(
            permission_entry_id=f"module_permission_{index:03d}",
            module_id=entry.module_id,
            permission_level=(
                "read_only"
                if entry.module_role == "base_family_module"
                else (
                    "operator_interaction"
                    if entry.module_role == "operator_module"
                    else "optional_extension"
                )
            ),
            approval_required=(entry.module_role == "optional_product_module"),
            operator_visible=True,
            truth_bound=True,
            description=f"Canonical permission entry for {entry.module_id}.",
        )
        for index, entry in enumerate(manifest_contract.entries, start=1)
    )

    return ModulePermissionMatrixContract(
        contract_id="module_permission_matrix_contract_001",
        total_entries=len(entries),
        approval_required_entries=sum(
            1 for entry in entries if entry.approval_required
        ),
        operator_visible_entries=sum(
            1 for entry in entries if entry.operator_visible
        ),
        truth_bound_entries=sum(
            1 for entry in entries if entry.truth_bound
        ),
        entries=entries,
    )
