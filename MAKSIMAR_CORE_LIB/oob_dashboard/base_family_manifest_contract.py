from __future__ import annotations

from dataclasses import dataclass

from MAKSIMAR_CORE_LIB.oob_dashboard.module_manifest_contract import (
    build_module_manifest_contract,
)


def _require_non_empty(value: str, field_name: str) -> None:
    if not value or not value.strip():
        raise ValueError(f"{field_name} must be a non-empty string.")


@dataclass(frozen=True, slots=True)
class BaseFamilyManifestEntry:
    base_family_manifest_id: str
    module_id: str
    module_name: str
    included_in_base_family: bool
    mount_required: bool
    operator_visible: bool
    truth_bound: bool
    description: str

    def __post_init__(self) -> None:
        _require_non_empty(self.base_family_manifest_id, "base_family_manifest_id")
        _require_non_empty(self.module_id, "module_id")
        _require_non_empty(self.module_name, "module_name")
        _require_non_empty(self.description, "description")

        if not self.included_in_base_family:
            raise ValueError(
                "included_in_base_family must remain true for canonical base family manifest entries."
            )
        if not self.operator_visible:
            raise ValueError(
                "operator_visible must remain true for canonical base family manifest entries."
            )
        if not self.truth_bound:
            raise ValueError(
                "truth_bound must remain true for canonical base family manifest entries."
            )


@dataclass(frozen=True, slots=True)
class BaseFamilyManifestContract:
    contract_id: str
    total_entries: int
    mount_required_entries: int
    operator_visible_entries: int
    truth_bound_entries: int
    entries: tuple[BaseFamilyManifestEntry, ...]

    def __post_init__(self) -> None:
        _require_non_empty(self.contract_id, "contract_id")
        if self.total_entries != len(self.entries):
            raise ValueError("total_entries must match len(entries).")
        if self.mount_required_entries != sum(
            1 for entry in self.entries if entry.mount_required
        ):
            raise ValueError(
                "mount_required_entries must match mount_required count."
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


def build_base_family_manifest_contract() -> BaseFamilyManifestContract:
    manifest_contract = build_module_manifest_contract()

    entries = tuple(
        BaseFamilyManifestEntry(
            base_family_manifest_id=f"base_family_manifest_{index:03d}",
            module_id=entry.module_id,
            module_name=entry.module_name,
            included_in_base_family=True,
            mount_required=(entry.mount_mode == "mount_required"),
            operator_visible=True,
            truth_bound=True,
            description=f"Canonical base family manifest entry for {entry.module_id}.",
        )
        for index, entry in enumerate(manifest_contract.entries, start=1)
        if entry.module_role != "optional_product_module"
    )

    return BaseFamilyManifestContract(
        contract_id="base_family_manifest_contract_001",
        total_entries=len(entries),
        mount_required_entries=sum(1 for entry in entries if entry.mount_required),
        operator_visible_entries=sum(1 for entry in entries if entry.operator_visible),
        truth_bound_entries=sum(1 for entry in entries if entry.truth_bound),
        entries=entries,
    )
