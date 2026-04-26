from __future__ import annotations

from dataclasses import dataclass
from typing import Tuple

from MAKSIMAR_CORE_LIB.oob_dashboard.preview_consumer_integration_contract import (
    build_preview_consumer_integration_contract,
)
from MAKSIMAR_CORE_LIB.oob_dashboard.runtime_data_handoff_integration_contract import (
    build_runtime_data_handoff_integration_contract,
)
from MAKSIMAR_CORE_LIB.oob_dashboard.visual_adapter_vendor_leakage_compliance_contract import (
    build_visual_adapter_vendor_leakage_compliance_contract,
)


def _require_non_empty(value: str, field_name: str) -> None:
    if not value or not value.strip():
        raise ValueError(f"{field_name} must be a non-empty string.")


@dataclass(frozen=True, slots=True)
class VisualAdapterCanonicalIdentityComplianceEntry:
    compliance_entry_id: str
    producer_contract_id: str
    consumer_contract_id: str
    compliance_scope: str
    canonical_id_preserved: bool
    canonical_semantics_preserved: bool
    compliance_passed: bool
    operator_visible: bool
    truth_bound: bool
    description: str

    def __post_init__(self) -> None:
        _require_non_empty(self.compliance_entry_id, "compliance_entry_id")
        _require_non_empty(self.producer_contract_id, "producer_contract_id")
        _require_non_empty(self.consumer_contract_id, "consumer_contract_id")
        _require_non_empty(self.compliance_scope, "compliance_scope")
        _require_non_empty(self.description, "description")

        if not self.canonical_id_preserved:
            raise ValueError(
                "canonical_id_preserved must remain true for canonical identity compliance entries."
            )
        if not self.canonical_semantics_preserved:
            raise ValueError(
                "canonical_semantics_preserved must remain true for canonical identity compliance entries."
            )
        if not self.compliance_passed:
            raise ValueError(
                "compliance_passed must remain true for canonical identity compliance entries."
            )
        if not self.operator_visible:
            raise ValueError(
                "operator_visible must remain true for canonical identity compliance entries."
            )
        if not self.truth_bound:
            raise ValueError(
                "truth_bound must remain true for canonical identity compliance entries."
            )


@dataclass(frozen=True, slots=True)
class VisualAdapterCanonicalIdentityComplianceContract:
    contract_id: str
    total_entries: int
    canonical_id_preserved_entries: int
    canonical_semantics_preserved_entries: int
    compliance_passed_entries: int
    operator_visible_entries: int
    truth_bound_entries: int
    entries: Tuple[VisualAdapterCanonicalIdentityComplianceEntry, ...]

    def __post_init__(self) -> None:
        _require_non_empty(self.contract_id, "contract_id")

        if self.total_entries != len(self.entries):
            raise ValueError("total_entries must match len(entries).")
        if self.canonical_id_preserved_entries != sum(
            1 for entry in self.entries if entry.canonical_id_preserved
        ):
            raise ValueError(
                "canonical_id_preserved_entries must match canonical_id_preserved count."
            )
        if self.canonical_semantics_preserved_entries != sum(
            1 for entry in self.entries if entry.canonical_semantics_preserved
        ):
            raise ValueError(
                "canonical_semantics_preserved_entries must match canonical_semantics_preserved count."
            )
        if self.compliance_passed_entries != sum(
            1 for entry in self.entries if entry.compliance_passed
        ):
            raise ValueError(
                "compliance_passed_entries must match compliance_passed count."
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


def build_visual_adapter_canonical_identity_compliance_contract() -> (
    VisualAdapterCanonicalIdentityComplianceContract
):
    runtime_handoff = build_runtime_data_handoff_integration_contract()
    preview_consumer = build_preview_consumer_integration_contract()
    vendor_leakage = build_visual_adapter_vendor_leakage_compliance_contract()

    entries = (
        VisualAdapterCanonicalIdentityComplianceEntry(
            compliance_entry_id="visual_adapter_canonical_identity_compliance_001",
            producer_contract_id=runtime_handoff.contract_id,
            consumer_contract_id=vendor_leakage.contract_id,
            compliance_scope="runtime_to_vendor_leakage_compliance",
            canonical_id_preserved=True,
            canonical_semantics_preserved=True,
            compliance_passed=True,
            operator_visible=True,
            truth_bound=True,
            description="Canonical identity compliance entry from runtime handoff to vendor leakage compliance.",
        ),
        VisualAdapterCanonicalIdentityComplianceEntry(
            compliance_entry_id="visual_adapter_canonical_identity_compliance_002",
            producer_contract_id=preview_consumer.contract_id,
            consumer_contract_id=vendor_leakage.contract_id,
            compliance_scope="preview_to_vendor_leakage_compliance",
            canonical_id_preserved=True,
            canonical_semantics_preserved=True,
            compliance_passed=True,
            operator_visible=True,
            truth_bound=True,
            description="Canonical identity compliance entry from preview consumer to vendor leakage compliance.",
        ),
        VisualAdapterCanonicalIdentityComplianceEntry(
            compliance_entry_id="visual_adapter_canonical_identity_compliance_003",
            producer_contract_id=runtime_handoff.contract_id,
            consumer_contract_id=preview_consumer.contract_id,
            compliance_scope="runtime_to_preview_identity_compliance",
            canonical_id_preserved=True,
            canonical_semantics_preserved=True,
            compliance_passed=True,
            operator_visible=True,
            truth_bound=True,
            description="Canonical identity compliance entry from runtime handoff to preview consumer.",
        ),
    )

    return VisualAdapterCanonicalIdentityComplianceContract(
        contract_id="visual_adapter_canonical_identity_compliance_contract_001",
        total_entries=len(entries),
        canonical_id_preserved_entries=sum(
            1 for entry in entries if entry.canonical_id_preserved
        ),
        canonical_semantics_preserved_entries=sum(
            1 for entry in entries if entry.canonical_semantics_preserved
        ),
        compliance_passed_entries=sum(
            1 for entry in entries if entry.compliance_passed
        ),
        operator_visible_entries=sum(1 for entry in entries if entry.operator_visible),
        truth_bound_entries=sum(1 for entry in entries if entry.truth_bound),
        entries=entries,
    )
