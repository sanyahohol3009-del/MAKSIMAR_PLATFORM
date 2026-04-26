from __future__ import annotations

from dataclasses import dataclass

from MAKSIMAR_CORE_LIB.oob_dashboard.base_family_bundle_contract import (
    build_base_family_bundle_contract,
)
from MAKSIMAR_CORE_LIB.oob_dashboard.base_family_manifest_contract import (
    build_base_family_manifest_contract,
)
from MAKSIMAR_CORE_LIB.oob_dashboard.base_family_mount_plan_contract import (
    build_base_family_mount_plan_contract,
)


def _require_non_empty(value: str, field_name: str) -> None:
    if not value or not value.strip():
        raise ValueError(f"{field_name} must be a non-empty string.")


@dataclass(frozen=True, slots=True)
class BaseFamilyReadinessEntry:
    readiness_entry_id: str
    module_id: str
    manifest_ready: bool
    bundle_ready: bool
    mount_plan_ready: bool
    operator_visible: bool
    truth_bound: bool
    description: str

    def __post_init__(self) -> None:
        _require_non_empty(self.readiness_entry_id, "readiness_entry_id")
        _require_non_empty(self.module_id, "module_id")
        _require_non_empty(self.description, "description")

        if not self.manifest_ready:
            raise ValueError(
                "manifest_ready must remain true for canonical base family readiness entries."
            )
        if not self.bundle_ready:
            raise ValueError(
                "bundle_ready must remain true for canonical base family readiness entries."
            )
        if not self.mount_plan_ready:
            raise ValueError(
                "mount_plan_ready must remain true for canonical base family readiness entries."
            )
        if not self.operator_visible:
            raise ValueError(
                "operator_visible must remain true for canonical base family readiness entries."
            )
        if not self.truth_bound:
            raise ValueError(
                "truth_bound must remain true for canonical base family readiness entries."
            )


@dataclass(frozen=True, slots=True)
class BaseFamilyReadinessContract:
    contract_id: str
    total_entries: int
    ready_entries: int
    operator_visible_entries: int
    truth_bound_entries: int
    entries: tuple[BaseFamilyReadinessEntry, ...]

    def __post_init__(self) -> None:
        _require_non_empty(self.contract_id, "contract_id")
        if self.total_entries != len(self.entries):
            raise ValueError("total_entries must match len(entries).")
        if self.ready_entries != sum(
            1
            for entry in self.entries
            if entry.manifest_ready and entry.bundle_ready and entry.mount_plan_ready
        ):
            raise ValueError("ready_entries must match readiness count.")
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


def build_base_family_readiness_contract() -> BaseFamilyReadinessContract:
    manifest = build_base_family_manifest_contract()
    bundle = build_base_family_bundle_contract()
    mount = build_base_family_mount_plan_contract()

    bundle_ids = {entry.module_id for entry in bundle.entries}
    mount_ids = {entry.module_id for entry in mount.entries}

    entries = tuple(
        BaseFamilyReadinessEntry(
            readiness_entry_id=f"base_family_readiness_{index:03d}",
            module_id=entry.module_id,
            manifest_ready=True,
            bundle_ready=entry.module_id in bundle_ids,
            mount_plan_ready=entry.module_id in mount_ids,
            operator_visible=True,
            truth_bound=True,
            description=f"Canonical base family readiness entry for {entry.module_id}.",
        )
        for index, entry in enumerate(manifest.entries, start=1)
    )

    return BaseFamilyReadinessContract(
        contract_id="base_family_readiness_contract_001",
        total_entries=len(entries),
        ready_entries=sum(
            1
            for entry in entries
            if entry.manifest_ready and entry.bundle_ready and entry.mount_plan_ready
        ),
        operator_visible_entries=sum(1 for entry in entries if entry.operator_visible),
        truth_bound_entries=sum(1 for entry in entries if entry.truth_bound),
        entries=entries,
    )
