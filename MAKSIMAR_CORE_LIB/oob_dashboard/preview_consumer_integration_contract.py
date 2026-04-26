from __future__ import annotations

from dataclasses import dataclass
from typing import Tuple

from MAKSIMAR_CORE_LIB.oob_dashboard.runtime_data_handoff_integration_contract import (
    build_runtime_data_handoff_integration_contract,
)
from MAKSIMAR_CORE_LIB.oob_dashboard.visual_degraded_mode_capability_contract import (
    build_visual_degraded_mode_capability_contract,
)


def _require_non_empty(value: str, field_name: str) -> None:
    if not value or not value.strip():
        raise ValueError(f"{field_name} must be a non-empty string.")


@dataclass(frozen=True, slots=True)
class PreviewConsumerIntegrationEntry:
    integration_entry_id: str
    producer_contract_id: str
    consumer_surface_id: str
    preview_ready: bool
    canonical_id_preserved: bool
    readable_operator_state_preserved: bool
    handoff_complete: bool
    operator_visible: bool
    truth_bound: bool
    description: str

    def __post_init__(self) -> None:
        _require_non_empty(self.integration_entry_id, "integration_entry_id")
        _require_non_empty(self.producer_contract_id, "producer_contract_id")
        _require_non_empty(self.consumer_surface_id, "consumer_surface_id")
        _require_non_empty(self.description, "description")

        if not self.preview_ready:
            raise ValueError(
                "preview_ready must remain true for canonical preview consumer integration entries."
            )
        if not self.canonical_id_preserved:
            raise ValueError(
                "canonical_id_preserved must remain true for canonical preview consumer integration entries."
            )
        if not self.readable_operator_state_preserved:
            raise ValueError(
                "readable_operator_state_preserved must remain true for canonical preview consumer integration entries."
            )
        if not self.handoff_complete:
            raise ValueError(
                "handoff_complete must remain true for canonical preview consumer integration entries."
            )
        if not self.operator_visible:
            raise ValueError(
                "operator_visible must remain true for canonical preview consumer integration entries."
            )
        if not self.truth_bound:
            raise ValueError(
                "truth_bound must remain true for canonical preview consumer integration entries."
            )


@dataclass(frozen=True, slots=True)
class PreviewConsumerIntegrationContract:
    contract_id: str
    total_entries: int
    preview_ready_entries: int
    canonical_id_preserved_entries: int
    readable_operator_state_preserved_entries: int
    handoff_complete_entries: int
    operator_visible_entries: int
    truth_bound_entries: int
    entries: Tuple[PreviewConsumerIntegrationEntry, ...]

    def __post_init__(self) -> None:
        _require_non_empty(self.contract_id, "contract_id")

        if self.total_entries != len(self.entries):
            raise ValueError("total_entries must match len(entries).")
        if self.preview_ready_entries != sum(
            1 for entry in self.entries if entry.preview_ready
        ):
            raise ValueError("preview_ready_entries must match preview_ready count.")
        if self.canonical_id_preserved_entries != sum(
            1 for entry in self.entries if entry.canonical_id_preserved
        ):
            raise ValueError(
                "canonical_id_preserved_entries must match canonical_id_preserved count."
            )
        if self.readable_operator_state_preserved_entries != sum(
            1 for entry in self.entries if entry.readable_operator_state_preserved
        ):
            raise ValueError(
                "readable_operator_state_preserved_entries must match readable_operator_state_preserved count."
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


def build_preview_consumer_integration_contract() -> PreviewConsumerIntegrationContract:
    runtime_handoff_contract = build_runtime_data_handoff_integration_contract()
    degraded_contract = build_visual_degraded_mode_capability_contract()

    entries = (
        PreviewConsumerIntegrationEntry(
            integration_entry_id="preview_consumer_integration_001",
            producer_contract_id=runtime_handoff_contract.contract_id,
            consumer_surface_id="runtime_data_handoff_preview_surface",
            preview_ready=True,
            canonical_id_preserved=True,
            readable_operator_state_preserved=True,
            handoff_complete=True,
            operator_visible=True,
            truth_bound=True,
            description="Canonical preview consumer integration for runtime handoff preview.",
        ),
        PreviewConsumerIntegrationEntry(
            integration_entry_id="preview_consumer_integration_002",
            producer_contract_id=degraded_contract.contract_id,
            consumer_surface_id="degraded_capability_preview_surface",
            preview_ready=True,
            canonical_id_preserved=True,
            readable_operator_state_preserved=True,
            handoff_complete=True,
            operator_visible=True,
            truth_bound=True,
            description="Canonical preview consumer integration for degraded capability preview.",
        ),
        PreviewConsumerIntegrationEntry(
            integration_entry_id="preview_consumer_integration_003",
            producer_contract_id=runtime_handoff_contract.contract_id,
            consumer_surface_id="visual_adapter_runtime_summary_surface",
            preview_ready=True,
            canonical_id_preserved=True,
            readable_operator_state_preserved=True,
            handoff_complete=True,
            operator_visible=True,
            truth_bound=True,
            description="Canonical preview consumer integration for runtime summary preview.",
        ),
    )

    return PreviewConsumerIntegrationContract(
        contract_id="preview_consumer_integration_contract_001",
        total_entries=len(entries),
        preview_ready_entries=sum(1 for entry in entries if entry.preview_ready),
        canonical_id_preserved_entries=sum(
            1 for entry in entries if entry.canonical_id_preserved
        ),
        readable_operator_state_preserved_entries=sum(
            1 for entry in entries if entry.readable_operator_state_preserved
        ),
        handoff_complete_entries=sum(
            1 for entry in entries if entry.handoff_complete
        ),
        operator_visible_entries=sum(1 for entry in entries if entry.operator_visible),
        truth_bound_entries=sum(1 for entry in entries if entry.truth_bound),
        entries=entries,
    )
