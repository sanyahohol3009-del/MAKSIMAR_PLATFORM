from __future__ import annotations

from dataclasses import dataclass

from MAKSIMAR_CORE_LIB.oob_dashboard.module_compatibility_contract import (
    build_module_compatibility_contract,
)
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
class ModuleRegistryAuditEntry:
    registry_audit_id: str
    module_id: str
    registry_present: bool
    permission_present: bool
    compatibility_present: bool
    audit_visible: bool
    operator_visible: bool
    truth_bound: bool
    description: str

    def __post_init__(self) -> None:
        _require_non_empty(self.registry_audit_id, "registry_audit_id")
        _require_non_empty(self.module_id, "module_id")
        _require_non_empty(self.description, "description")

        if not self.registry_present:
            raise ValueError(
                "registry_present must remain true for canonical module registry audit entries."
            )
        if not self.permission_present:
            raise ValueError(
                "permission_present must remain true for canonical module registry audit entries."
            )
        if not self.compatibility_present:
            raise ValueError(
                "compatibility_present must remain true for canonical module registry audit entries."
            )
        if not self.audit_visible:
            raise ValueError(
                "audit_visible must remain true for canonical module registry audit entries."
            )
        if not self.operator_visible:
            raise ValueError(
                "operator_visible must remain true for canonical module registry audit entries."
            )
        if not self.truth_bound:
            raise ValueError(
                "truth_bound must remain true for canonical module registry audit entries."
            )


@dataclass(frozen=True, slots=True)
class ModuleRegistryAuditContract:
    contract_id: str
    total_entries: int
    audit_visible_entries: int
    operator_visible_entries: int
    truth_bound_entries: int
    entries: tuple[ModuleRegistryAuditEntry, ...]

    def __post_init__(self) -> None:
        _require_non_empty(self.contract_id, "contract_id")
        if self.total_entries != len(self.entries):
            raise ValueError("total_entries must match len(entries).")
        if self.audit_visible_entries != sum(
            1 for entry in self.entries if entry.audit_visible
        ):
            raise ValueError(
                "audit_visible_entries must match audit_visible count."
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


def build_module_registry_audit_contract() -> ModuleRegistryAuditContract:
    manifest_contract = build_module_manifest_contract()
    permission_contract = build_module_permission_matrix_contract()
    compatibility_contract = build_module_compatibility_contract()

    permission_ids = {entry.module_id for entry in permission_contract.entries}
    compatibility_ids = {entry.module_id for entry in compatibility_contract.entries}

    entries = tuple(
        ModuleRegistryAuditEntry(
            registry_audit_id=f"module_registry_audit_{index:03d}",
            module_id=entry.module_id,
            registry_present=True,
            permission_present=entry.module_id in permission_ids,
            compatibility_present=entry.module_id in compatibility_ids,
            audit_visible=True,
            operator_visible=True,
            truth_bound=True,
            description=f"Canonical registry audit entry for {entry.module_id}.",
        )
        for index, entry in enumerate(manifest_contract.entries, start=1)
    )

    return ModuleRegistryAuditContract(
        contract_id="module_registry_audit_contract_001",
        total_entries=len(entries),
        audit_visible_entries=sum(1 for entry in entries if entry.audit_visible),
        operator_visible_entries=sum(1 for entry in entries if entry.operator_visible),
        truth_bound_entries=sum(1 for entry in entries if entry.truth_bound),
        entries=entries,
    )
