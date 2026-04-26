from __future__ import annotations

from dataclasses import dataclass
from typing import Tuple

from MAKSIMAR_CORE_LIB.oob_dashboard.visual_adapter_canonical_identity_compliance_contract import (
    build_visual_adapter_canonical_identity_compliance_contract,
)
from MAKSIMAR_CORE_LIB.oob_dashboard.visual_backend_replaceability_contract import (
    build_visual_backend_replaceability_contract,
)
from MAKSIMAR_CORE_LIB.oob_dashboard.visual_capability_matrix_contract import (
    build_visual_capability_matrix_contract,
)


def _require_non_empty(value: str, field_name: str) -> None:
    if not value or not value.strip():
        raise ValueError(f"{field_name} must be a non-empty string.")


@dataclass(frozen=True, slots=True)
class VisualBackendSwapEquivalenceEntry:
    equivalence_entry_id: str
    canonical_input_id: str
    primary_backend_id: str
    secondary_backend_id: str
    canonical_semantics_equal: bool
    canonical_id_preserved: bool
    contract_change_required: bool
    read_model_change_required: bool
    swap_equivalent: bool
    operator_visible: bool
    truth_bound: bool
    description: str

    def __post_init__(self) -> None:
        _require_non_empty(self.equivalence_entry_id, "equivalence_entry_id")
        _require_non_empty(self.canonical_input_id, "canonical_input_id")
        _require_non_empty(self.primary_backend_id, "primary_backend_id")
        _require_non_empty(self.secondary_backend_id, "secondary_backend_id")
        _require_non_empty(self.description, "description")

        if not self.canonical_semantics_equal:
            raise ValueError(
                "canonical_semantics_equal must remain true for canonical visual backend swap equivalence entries."
            )
        if not self.canonical_id_preserved:
            raise ValueError(
                "canonical_id_preserved must remain true for canonical visual backend swap equivalence entries."
            )
        if self.contract_change_required:
            raise ValueError(
                "contract_change_required must remain false for canonical visual backend swap equivalence entries."
            )
        if self.read_model_change_required:
            raise ValueError(
                "read_model_change_required must remain false for canonical visual backend swap equivalence entries."
            )
        if not self.swap_equivalent:
            raise ValueError(
                "swap_equivalent must remain true for canonical visual backend swap equivalence entries."
            )
        if not self.operator_visible:
            raise ValueError(
                "operator_visible must remain true for canonical visual backend swap equivalence entries."
            )
        if not self.truth_bound:
            raise ValueError(
                "truth_bound must remain true for canonical visual backend swap equivalence entries."
            )


@dataclass(frozen=True, slots=True)
class VisualBackendSwapEquivalenceContract:
    contract_id: str
    total_entries: int
    canonical_semantics_equal_entries: int
    canonical_id_preserved_entries: int
    swap_equivalent_entries: int
    operator_visible_entries: int
    truth_bound_entries: int
    entries: Tuple[VisualBackendSwapEquivalenceEntry, ...]

    def __post_init__(self) -> None:
        _require_non_empty(self.contract_id, "contract_id")

        if self.total_entries != len(self.entries):
            raise ValueError("total_entries must match len(entries).")
        if self.canonical_semantics_equal_entries != sum(
            1 for entry in self.entries if entry.canonical_semantics_equal
        ):
            raise ValueError(
                "canonical_semantics_equal_entries must match canonical_semantics_equal count."
            )
        if self.canonical_id_preserved_entries != sum(
            1 for entry in self.entries if entry.canonical_id_preserved
        ):
            raise ValueError(
                "canonical_id_preserved_entries must match canonical_id_preserved count."
            )
        if self.swap_equivalent_entries != sum(
            1 for entry in self.entries if entry.swap_equivalent
        ):
            raise ValueError(
                "swap_equivalent_entries must match swap_equivalent count."
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


def build_visual_backend_swap_equivalence_contract() -> (
    VisualBackendSwapEquivalenceContract
):
    replaceability_contract = build_visual_backend_replaceability_contract()
    capability_contract = build_visual_capability_matrix_contract()
    identity_contract = build_visual_adapter_canonical_identity_compliance_contract()

    backend_ids = {entry.backend_id for entry in replaceability_contract.entries}
    capability_ids = {entry.backend_id for entry in capability_contract.entries}

    entries = (
        VisualBackendSwapEquivalenceEntry(
            equivalence_entry_id="visual_backend_swap_equivalence_001",
            canonical_input_id=identity_contract.contract_id,
            primary_backend_id="visual_backend_graph_001",
            secondary_backend_id="visual_backend_overlay_001",
            canonical_semantics_equal=(
                "visual_backend_graph_001" in backend_ids
                and "visual_backend_overlay_001" in backend_ids
            ),
            canonical_id_preserved=(
                "visual_backend_graph_001" in capability_ids
                and "visual_backend_overlay_001" in capability_ids
            ),
            contract_change_required=False,
            read_model_change_required=False,
            swap_equivalent=True,
            operator_visible=True,
            truth_bound=True,
            description="Canonical swap equivalence entry for graph and overlay backend paths.",
        ),
        VisualBackendSwapEquivalenceEntry(
            equivalence_entry_id="visual_backend_swap_equivalence_002",
            canonical_input_id=identity_contract.contract_id,
            primary_backend_id="visual_backend_chart_001",
            secondary_backend_id="motion_backend_virtual_001",
            canonical_semantics_equal=(
                "visual_backend_chart_001" in backend_ids
                and "motion_backend_virtual_001" in backend_ids
            ),
            canonical_id_preserved=(
                "visual_backend_chart_001" in capability_ids
                and "motion_backend_virtual_001" in capability_ids
            ),
            contract_change_required=False,
            read_model_change_required=False,
            swap_equivalent=True,
            operator_visible=True,
            truth_bound=True,
            description="Canonical swap equivalence entry for chart and motion backend paths.",
        ),
        VisualBackendSwapEquivalenceEntry(
            equivalence_entry_id="visual_backend_swap_equivalence_003",
            canonical_input_id=identity_contract.contract_id,
            primary_backend_id="visual_backend_graph_001",
            secondary_backend_id="visual_backend_chart_001",
            canonical_semantics_equal=(
                "visual_backend_graph_001" in backend_ids
                and "visual_backend_chart_001" in backend_ids
            ),
            canonical_id_preserved=(
                "visual_backend_graph_001" in capability_ids
                and "visual_backend_chart_001" in capability_ids
            ),
            contract_change_required=False,
            read_model_change_required=False,
            swap_equivalent=True,
            operator_visible=True,
            truth_bound=True,
            description="Canonical swap equivalence entry for graph and chart backend paths.",
        ),
    )

    return VisualBackendSwapEquivalenceContract(
        contract_id="visual_backend_swap_equivalence_contract_001",
        total_entries=len(entries),
        canonical_semantics_equal_entries=sum(
            1 for entry in entries if entry.canonical_semantics_equal
        ),
        canonical_id_preserved_entries=sum(
            1 for entry in entries if entry.canonical_id_preserved
        ),
        swap_equivalent_entries=sum(1 for entry in entries if entry.swap_equivalent),
        operator_visible_entries=sum(1 for entry in entries if entry.operator_visible),
        truth_bound_entries=sum(1 for entry in entries if entry.truth_bound),
        entries=entries,
    )
