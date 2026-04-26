from __future__ import annotations

from dataclasses import dataclass
from typing import Literal


ModuleRole = Literal[
    "base_family_module",
    "operator_module",
    "optional_product_module",
]

ModuleMountMode = Literal[
    "mount_required",
    "mount_optional",
]

AllowedWorkspace = Literal[
    "workspace_foundation_monitoring",
    "workspace_operator_interaction",
]


def _require_non_empty(value: str, field_name: str) -> None:
    if not value or not value.strip():
        raise ValueError(f"{field_name} must be a non-empty string.")


@dataclass(frozen=True, slots=True)
class ModuleManifestEntry:
    """Canonical module manifest entry."""

    module_id: str
    module_name: str
    module_role: ModuleRole
    mount_mode: ModuleMountMode
    allowed_workspace: AllowedWorkspace
    operator_visible: bool
    truth_bound: bool
    description: str

    def __post_init__(self) -> None:
        _require_non_empty(self.module_id, "module_id")
        _require_non_empty(self.module_name, "module_name")
        _require_non_empty(self.description, "description")

        if not self.operator_visible:
            raise ValueError(
                "operator_visible must remain true for canonical module manifest entries."
            )

        if not self.truth_bound:
            raise ValueError(
                "truth_bound must remain true for canonical module manifest entries."
            )


@dataclass(frozen=True, slots=True)
class ModuleManifestContract:
    """Canonical module manifest contract."""

    contract_id: str
    total_entries: int
    required_mount_entries: int
    optional_mount_entries: int
    operator_visible_entries: int
    truth_bound_entries: int
    entries: tuple[ModuleManifestEntry, ...]

    def __post_init__(self) -> None:
        _require_non_empty(self.contract_id, "contract_id")

        if self.total_entries != len(self.entries):
            raise ValueError("total_entries must match len(entries).")

        if self.required_mount_entries != sum(
            1 for entry in self.entries if entry.mount_mode == "mount_required"
        ):
            raise ValueError(
                "required_mount_entries must match mount_required count."
            )

        if self.optional_mount_entries != sum(
            1 for entry in self.entries if entry.mount_mode == "mount_optional"
        ):
            raise ValueError(
                "optional_mount_entries must match mount_optional count."
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


def build_module_manifest_contract() -> ModuleManifestContract:
    """Build canonical module manifest contract."""
    entries = (
        ModuleManifestEntry(
            module_id="module_manifest_001",
            module_name="foundation_monitoring_module",
            module_role="base_family_module",
            mount_mode="mount_required",
            allowed_workspace="workspace_foundation_monitoring",
            operator_visible=True,
            truth_bound=True,
            description="Canonical manifest entry for foundation monitoring module.",
        ),
        ModuleManifestEntry(
            module_id="module_manifest_002",
            module_name="operator_interaction_module",
            module_role="operator_module",
            mount_mode="mount_required",
            allowed_workspace="workspace_operator_interaction",
            operator_visible=True,
            truth_bound=True,
            description="Canonical manifest entry for operator interaction module.",
        ),
        ModuleManifestEntry(
            module_id="module_manifest_003",
            module_name="optional_product_module",
            module_role="optional_product_module",
            mount_mode="mount_optional",
            allowed_workspace="workspace_operator_interaction",
            operator_visible=True,
            truth_bound=True,
            description="Canonical manifest entry for optional product module.",
        ),
    )

    return ModuleManifestContract(
        contract_id="module_manifest_contract_001",
        total_entries=len(entries),
        required_mount_entries=sum(
            1 for entry in entries if entry.mount_mode == "mount_required"
        ),
        optional_mount_entries=sum(
            1 for entry in entries if entry.mount_mode == "mount_optional"
        ),
        operator_visible_entries=sum(
            1 for entry in entries if entry.operator_visible
        ),
        truth_bound_entries=sum(
            1 for entry in entries if entry.truth_bound
        ),
        entries=entries,
    )
