from __future__ import annotations

from dataclasses import dataclass
from typing import Tuple

from MAKSIMAR_CORE_LIB.oob_dashboard.preview_consumer_integration_contract import (
    build_preview_consumer_integration_contract,
)
from MAKSIMAR_CORE_LIB.oob_dashboard.runtime_data_handoff_integration_contract import (
    build_runtime_data_handoff_integration_contract,
)
from MAKSIMAR_CORE_LIB.oob_dashboard.visual_backend_swap_equivalence_contract import (
    build_visual_backend_swap_equivalence_contract,
)


def _require_non_empty(value: str, field_name: str) -> None:
    if not value or not value.strip():
        raise ValueError(f"{field_name} must be a non-empty string.")


@dataclass(frozen=True, slots=True)
class VisualBackendPathReplaceabilityEntry:
    replaceability_entry_id: str
    canonical_path_id: str
    producer_contract_id: str
    consumer_contract_id: str
    path_swap_safe: bool
    canonical_semantics_preserved: bool
    preview_consumer_compatible: bool
    contract_change_required: bool
    read_model_change_required: bool
    operator_visible: bool
    truth_bound: bool
    description: str

    def __post_init__(self) -> None:
        _require_non_empty(self.replaceability_entry_id, "replaceability_entry_id")
        _require_non_empty(self.canonical_path_id, "canonical_path_id")
        _require_non_empty(self.producer_contract_id, "producer_contract_id")
        _require_non_empty(self.consumer_contract_id, "consumer_contract_id")
        _require_non_empty(self.description, "description")

        if not self.path_swap_safe:
            raise ValueError(
                "path_swap_safe must remain true for canonical visual backend path replaceability entries."
            )
        if not self.canonical_semantics_preserved:
            raise ValueError(
                "canonical_semantics_preserved must remain true for canonical visual backend path replaceability entries."
            )
        if not self.preview_consumer_compatible:
            raise ValueError(
                "preview_consumer_compatible must remain true for canonical visual backend path replaceability entries."
            )
        if self.contract_change_required:
            raise ValueError(
                "contract_change_required must remain false for canonical visual backend path replaceability entries."
            )
        if self.read_model_change_required:
            raise ValueError(
                "read_model_change_required must remain false for canonical visual backend path replaceability entries."
            )
        if not self.operator_visible:
            raise ValueError(
                "operator_visible must remain true for canonical visual backend path replaceability entries."
            )
        if not self.truth_bound:
            raise ValueError(
                "truth_bound must remain true for canonical visual backend path replaceability entries."
            )


@dataclass(frozen=True, slots=True)
class VisualBackendPathReplaceabilityContract:
    contract_id: str
    total_entries: int
    path_swap_safe_entries: int
    canonical_semantics_preserved_entries: int
    preview_consumer_compatible_entries: int
    operator_visible_entries: int
    truth_bound_entries: int
    entries: Tuple[VisualBackendPathReplaceabilityEntry, ...]

    def __post_init__(self) -> None:
        _require_non_empty(self.contract_id, "contract_id")

        if self.total_entries != len(self.entries):
            raise ValueError("total_entries must match len(entries).")
        if self.path_swap_safe_entries != sum(
            1 for entry in self.entries if entry.path_swap_safe
        ):
            raise ValueError(
                "path_swap_safe_entries must match path_swap_safe count."
            )
        if self.canonical_semantics_preserved_entries != sum(
            1 for entry in self.entries if entry.canonical_semantics_preserved
        ):
            raise ValueError(
                "canonical_semantics_preserved_entries must match canonical_semantics_preserved count."
            )
        if self.preview_consumer_compatible_entries != sum(
            1 for entry in self.entries if entry.preview_consumer_compatible
        ):
            raise ValueError(
                "preview_consumer_compatible_entries must match preview_consumer_compatible count."
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


def build_visual_backend_path_replaceability_contract() -> (
    VisualBackendPathReplaceabilityContract
):
    swap_equivalence = build_visual_backend_swap_equivalence_contract()
    runtime_handoff = build_runtime_data_handoff_integration_contract()
    preview_consumer = build_preview_consumer_integration_contract()

    entries = (
        VisualBackendPathReplaceabilityEntry(
            replaceability_entry_id="visual_backend_path_replaceability_001",
            canonical_path_id="runtime_to_preview_path",
            producer_contract_id=runtime_handoff.contract_id,
            consumer_contract_id=preview_consumer.contract_id,
            path_swap_safe=(swap_equivalence.swap_equivalent_entries == 3),
            canonical_semantics_preserved=True,
            preview_consumer_compatible=True,
            contract_change_required=False,
            read_model_change_required=False,
            operator_visible=True,
            truth_bound=True,
            description="Canonical path replaceability entry for runtime to preview path.",
        ),
        VisualBackendPathReplaceabilityEntry(
            replaceability_entry_id="visual_backend_path_replaceability_002",
            canonical_path_id="runtime_to_runtime_summary_path",
            producer_contract_id=runtime_handoff.contract_id,
            consumer_contract_id="visual_adapter_runtime_summary_surface",
            path_swap_safe=(swap_equivalence.swap_equivalent_entries == 3),
            canonical_semantics_preserved=True,
            preview_consumer_compatible=True,
            contract_change_required=False,
            read_model_change_required=False,
            operator_visible=True,
            truth_bound=True,
            description="Canonical path replaceability entry for runtime summary path.",
        ),
        VisualBackendPathReplaceabilityEntry(
            replaceability_entry_id="visual_backend_path_replaceability_003",
            canonical_path_id="degraded_to_preview_path",
            producer_contract_id="visual_degraded_mode_capability_contract_001",
            consumer_contract_id=preview_consumer.contract_id,
            path_swap_safe=(swap_equivalence.swap_equivalent_entries == 3),
            canonical_semantics_preserved=True,
            preview_consumer_compatible=True,
            contract_change_required=False,
            read_model_change_required=False,
            operator_visible=True,
            truth_bound=True,
            description="Canonical path replaceability entry for degraded to preview path.",
        ),
    )

    return VisualBackendPathReplaceabilityContract(
        contract_id="visual_backend_path_replaceability_contract_001",
        total_entries=len(entries),
        path_swap_safe_entries=sum(1 for entry in entries if entry.path_swap_safe),
        canonical_semantics_preserved_entries=sum(
            1 for entry in entries if entry.canonical_semantics_preserved
        ),
        preview_consumer_compatible_entries=sum(
            1 for entry in entries if entry.preview_consumer_compatible
        ),
        operator_visible_entries=sum(1 for entry in entries if entry.operator_visible),
        truth_bound_entries=sum(1 for entry in entries if entry.truth_bound),
        entries=entries,
    )
