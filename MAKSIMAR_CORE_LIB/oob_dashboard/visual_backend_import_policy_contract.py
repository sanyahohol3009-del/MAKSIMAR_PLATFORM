from __future__ import annotations

from dataclasses import dataclass
from typing import Tuple

from MAKSIMAR_CORE_LIB.oob_dashboard.visual_backend_replaceability_contract import (
    build_visual_backend_replaceability_contract,
)


def _require_non_empty(value: str, field_name: str) -> None:
    if not value or not value.strip():
        raise ValueError(f"{field_name} must be a non-empty string.")


@dataclass(frozen=True, slots=True)
class VisualBackendImportPolicyEntry:
    policy_entry_id: str
    protected_layer: str
    direct_oss_import_allowed: bool
    adapter_boundary_required: bool
    canonical_id_only: bool
    swap_safe: bool
    operator_visible: bool
    truth_bound: bool
    description: str

    def __post_init__(self) -> None:
        _require_non_empty(self.policy_entry_id, "policy_entry_id")
        _require_non_empty(self.protected_layer, "protected_layer")
        _require_non_empty(self.description, "description")

        if self.direct_oss_import_allowed:
            raise ValueError(
                "direct_oss_import_allowed must remain false for canonical visual backend import policy entries."
            )
        if not self.adapter_boundary_required:
            raise ValueError(
                "adapter_boundary_required must remain true for canonical visual backend import policy entries."
            )
        if not self.canonical_id_only:
            raise ValueError(
                "canonical_id_only must remain true for canonical visual backend import policy entries."
            )
        if not self.swap_safe:
            raise ValueError(
                "swap_safe must remain true for canonical visual backend import policy entries."
            )
        if not self.operator_visible:
            raise ValueError(
                "operator_visible must remain true for canonical visual backend import policy entries."
            )
        if not self.truth_bound:
            raise ValueError(
                "truth_bound must remain true for canonical visual backend import policy entries."
            )


@dataclass(frozen=True, slots=True)
class VisualBackendImportPolicyContract:
    contract_id: str
    total_entries: int
    adapter_boundary_required_entries: int
    canonical_id_only_entries: int
    swap_safe_entries: int
    operator_visible_entries: int
    truth_bound_entries: int
    entries: Tuple[VisualBackendImportPolicyEntry, ...]

    def __post_init__(self) -> None:
        _require_non_empty(self.contract_id, "contract_id")

        if self.total_entries != len(self.entries):
            raise ValueError("total_entries must match len(entries).")
        if self.adapter_boundary_required_entries != sum(
            1 for entry in self.entries if entry.adapter_boundary_required
        ):
            raise ValueError(
                "adapter_boundary_required_entries must match adapter_boundary_required count."
            )
        if self.canonical_id_only_entries != sum(
            1 for entry in self.entries if entry.canonical_id_only
        ):
            raise ValueError(
                "canonical_id_only_entries must match canonical_id_only count."
            )
        if self.swap_safe_entries != sum(
            1 for entry in self.entries if entry.swap_safe
        ):
            raise ValueError("swap_safe_entries must match swap_safe count.")
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


def build_visual_backend_import_policy_contract() -> (
    VisualBackendImportPolicyContract
):
    replaceability_contract = build_visual_backend_replaceability_contract()

    layer_ids = (
        "canonical_contract_layer",
        "read_model_layer",
        "preview_contract_layer",
        "visual_family_projection_layer",
    )

    entries = tuple(
        VisualBackendImportPolicyEntry(
            policy_entry_id=f"visual_backend_import_policy_{index:03d}",
            protected_layer=layer_id,
            direct_oss_import_allowed=False,
            adapter_boundary_required=True,
            canonical_id_only=True,
            swap_safe=(replaceability_contract.swap_ready_entries == 4),
            operator_visible=True,
            truth_bound=True,
            description=f"Canonical import policy entry for {layer_id}.",
        )
        for index, layer_id in enumerate(layer_ids, start=1)
    )

    return VisualBackendImportPolicyContract(
        contract_id="visual_backend_import_policy_contract_001",
        total_entries=len(entries),
        adapter_boundary_required_entries=sum(
            1 for entry in entries if entry.adapter_boundary_required
        ),
        canonical_id_only_entries=sum(1 for entry in entries if entry.canonical_id_only),
        swap_safe_entries=sum(1 for entry in entries if entry.swap_safe),
        operator_visible_entries=sum(1 for entry in entries if entry.operator_visible),
        truth_bound_entries=sum(1 for entry in entries if entry.truth_bound),
        entries=entries,
    )
