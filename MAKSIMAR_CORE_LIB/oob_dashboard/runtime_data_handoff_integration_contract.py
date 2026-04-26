from __future__ import annotations

from dataclasses import dataclass
from typing import Tuple

from MAKSIMAR_CORE_LIB.oob_dashboard.visual_backend_import_policy_contract import (
    build_visual_backend_import_policy_contract,
)
from MAKSIMAR_CORE_LIB.oob_dashboard.visual_capability_matrix_contract import (
    build_visual_capability_matrix_contract,
)


def _require_non_empty(value: str, field_name: str) -> None:
    if not value or not value.strip():
        raise ValueError(f"{field_name} must be a non-empty string.")


@dataclass(frozen=True, slots=True)
class RuntimeDataHandoffIntegrationEntry:
    integration_entry_id: str
    producer_id: str
    consumer_id: str
    handoff_scope: str
    payload_consistent: bool
    canonical_id_preserved: bool
    handoff_complete: bool
    operator_visible: bool
    truth_bound: bool
    description: str

    def __post_init__(self) -> None:
        _require_non_empty(self.integration_entry_id, "integration_entry_id")
        _require_non_empty(self.producer_id, "producer_id")
        _require_non_empty(self.consumer_id, "consumer_id")
        _require_non_empty(self.handoff_scope, "handoff_scope")
        _require_non_empty(self.description, "description")

        if not self.payload_consistent:
            raise ValueError(
                "payload_consistent must remain true for canonical runtime data handoff integration entries."
            )
        if not self.canonical_id_preserved:
            raise ValueError(
                "canonical_id_preserved must remain true for canonical runtime data handoff integration entries."
            )
        if not self.handoff_complete:
            raise ValueError(
                "handoff_complete must remain true for canonical runtime data handoff integration entries."
            )
        if not self.operator_visible:
            raise ValueError(
                "operator_visible must remain true for canonical runtime data handoff integration entries."
            )
        if not self.truth_bound:
            raise ValueError(
                "truth_bound must remain true for canonical runtime data handoff integration entries."
            )


@dataclass(frozen=True, slots=True)
class RuntimeDataHandoffIntegrationContract:
    contract_id: str
    total_entries: int
    payload_consistent_entries: int
    canonical_id_preserved_entries: int
    handoff_complete_entries: int
    operator_visible_entries: int
    truth_bound_entries: int
    entries: Tuple[RuntimeDataHandoffIntegrationEntry, ...]

    def __post_init__(self) -> None:
        _require_non_empty(self.contract_id, "contract_id")

        if self.total_entries != len(self.entries):
            raise ValueError("total_entries must match len(entries).")
        if self.payload_consistent_entries != sum(
            1 for entry in self.entries if entry.payload_consistent
        ):
            raise ValueError(
                "payload_consistent_entries must match payload_consistent count."
            )
        if self.canonical_id_preserved_entries != sum(
            1 for entry in self.entries if entry.canonical_id_preserved
        ):
            raise ValueError(
                "canonical_id_preserved_entries must match canonical_id_preserved count."
            )
        if self.handoff_complete_entries != sum(
            1 for entry in self.entries if entry.handoff_complete
        ):
            raise ValueError(
                "handoff_complete_entries must match handoff_complete count."
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


def build_runtime_data_handoff_integration_contract() -> (
    RuntimeDataHandoffIntegrationContract
):
    capability_contract = build_visual_capability_matrix_contract()
    import_policy_contract = build_visual_backend_import_policy_contract()

    entries = (
        RuntimeDataHandoffIntegrationEntry(
            integration_entry_id="runtime_data_handoff_integration_001",
            producer_id=capability_contract.contract_id,
            consumer_id=import_policy_contract.contract_id,
            handoff_scope="capability_matrix_to_import_policy",
            payload_consistent=True,
            canonical_id_preserved=True,
            handoff_complete=True,
            operator_visible=True,
            truth_bound=True,
            description="Canonical runtime handoff from capability matrix to import policy.",
        ),
        RuntimeDataHandoffIntegrationEntry(
            integration_entry_id="runtime_data_handoff_integration_002",
            producer_id=import_policy_contract.contract_id,
            consumer_id="replaceability_guard_preview_consumer",
            handoff_scope="import_policy_to_preview_consumer",
            payload_consistent=True,
            canonical_id_preserved=True,
            handoff_complete=True,
            operator_visible=True,
            truth_bound=True,
            description="Canonical runtime handoff from import policy to preview consumer.",
        ),
        RuntimeDataHandoffIntegrationEntry(
            integration_entry_id="runtime_data_handoff_integration_003",
            producer_id=capability_contract.contract_id,
            consumer_id="visual_adapter_runtime_summary",
            handoff_scope="capability_matrix_to_runtime_summary",
            payload_consistent=True,
            canonical_id_preserved=True,
            handoff_complete=True,
            operator_visible=True,
            truth_bound=True,
            description="Canonical runtime handoff from capability matrix to runtime summary.",
        ),
    )

    return RuntimeDataHandoffIntegrationContract(
        contract_id="runtime_data_handoff_integration_contract_001",
        total_entries=len(entries),
        payload_consistent_entries=sum(
            1 for entry in entries if entry.payload_consistent
        ),
        canonical_id_preserved_entries=sum(
            1 for entry in entries if entry.canonical_id_preserved
        ),
        handoff_complete_entries=sum(
            1 for entry in entries if entry.handoff_complete
        ),
        operator_visible_entries=sum(1 for entry in entries if entry.operator_visible),
        truth_bound_entries=sum(1 for entry in entries if entry.truth_bound),
        entries=entries,
    )
