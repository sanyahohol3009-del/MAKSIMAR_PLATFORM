from __future__ import annotations

from dataclasses import dataclass
from typing import Tuple

from MAKSIMAR_CORE_LIB.oob_dashboard.chart_render_adapter_contract import (
    build_chart_render_adapter_contract,
)
from MAKSIMAR_CORE_LIB.oob_dashboard.graph_render_adapter_contract import (
    build_graph_render_adapter_contract,
)
from MAKSIMAR_CORE_LIB.oob_dashboard.motion_render_adapter_contract import (
    build_motion_render_adapter_contract,
)
from MAKSIMAR_CORE_LIB.oob_dashboard.overlay_render_adapter_contract import (
    build_overlay_render_adapter_contract,
)


def _require_non_empty(value: str, field_name: str) -> None:
    if not value or not value.strip():
        raise ValueError(f"{field_name} must be a non-empty string.")


@dataclass(frozen=True, slots=True)
class VisualAdapterVendorLeakageComplianceEntry:
    compliance_entry_id: str
    adapter_contract_id: str
    compliance_scope: str
    vendor_identifier_exposed: bool
    vendor_payload_exposed: bool
    truth_leakage_allowed: bool
    compliance_passed: bool
    operator_visible: bool
    truth_bound: bool
    description: str

    def __post_init__(self) -> None:
        _require_non_empty(self.compliance_entry_id, "compliance_entry_id")
        _require_non_empty(self.adapter_contract_id, "adapter_contract_id")
        _require_non_empty(self.compliance_scope, "compliance_scope")
        _require_non_empty(self.description, "description")

        if self.vendor_identifier_exposed:
            raise ValueError(
                "vendor_identifier_exposed must remain false for canonical visual adapter vendor leakage compliance entries."
            )
        if self.vendor_payload_exposed:
            raise ValueError(
                "vendor_payload_exposed must remain false for canonical visual adapter vendor leakage compliance entries."
            )
        if self.truth_leakage_allowed:
            raise ValueError(
                "truth_leakage_allowed must remain false for canonical visual adapter vendor leakage compliance entries."
            )
        if not self.compliance_passed:
            raise ValueError(
                "compliance_passed must remain true for canonical visual adapter vendor leakage compliance entries."
            )
        if not self.operator_visible:
            raise ValueError(
                "operator_visible must remain true for canonical visual adapter vendor leakage compliance entries."
            )
        if not self.truth_bound:
            raise ValueError(
                "truth_bound must remain true for canonical visual adapter vendor leakage compliance entries."
            )


@dataclass(frozen=True, slots=True)
class VisualAdapterVendorLeakageComplianceContract:
    contract_id: str
    total_entries: int
    compliance_passed_entries: int
    operator_visible_entries: int
    truth_bound_entries: int
    entries: Tuple[VisualAdapterVendorLeakageComplianceEntry, ...]

    def __post_init__(self) -> None:
        _require_non_empty(self.contract_id, "contract_id")

        if self.total_entries != len(self.entries):
            raise ValueError("total_entries must match len(entries).")
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


def build_visual_adapter_vendor_leakage_compliance_contract() -> (
    VisualAdapterVendorLeakageComplianceContract
):
    graph_adapter = build_graph_render_adapter_contract()
    chart_adapter = build_chart_render_adapter_contract()
    overlay_adapter = build_overlay_render_adapter_contract()
    motion_adapter = build_motion_render_adapter_contract()

    entries = (
        VisualAdapterVendorLeakageComplianceEntry(
            compliance_entry_id="visual_adapter_vendor_leakage_compliance_001",
            adapter_contract_id=graph_adapter.contract_id,
            compliance_scope="graph_adapter_vendor_leakage",
            vendor_identifier_exposed=False,
            vendor_payload_exposed=False,
            truth_leakage_allowed=False,
            compliance_passed=True,
            operator_visible=True,
            truth_bound=True,
            description="Canonical vendor leakage compliance entry for graph adapter.",
        ),
        VisualAdapterVendorLeakageComplianceEntry(
            compliance_entry_id="visual_adapter_vendor_leakage_compliance_002",
            adapter_contract_id=chart_adapter.contract_id,
            compliance_scope="chart_adapter_vendor_leakage",
            vendor_identifier_exposed=False,
            vendor_payload_exposed=False,
            truth_leakage_allowed=False,
            compliance_passed=True,
            operator_visible=True,
            truth_bound=True,
            description="Canonical vendor leakage compliance entry for chart adapter.",
        ),
        VisualAdapterVendorLeakageComplianceEntry(
            compliance_entry_id="visual_adapter_vendor_leakage_compliance_003",
            adapter_contract_id=overlay_adapter.contract_id,
            compliance_scope="overlay_adapter_vendor_leakage",
            vendor_identifier_exposed=False,
            vendor_payload_exposed=False,
            truth_leakage_allowed=False,
            compliance_passed=True,
            operator_visible=True,
            truth_bound=True,
            description="Canonical vendor leakage compliance entry for overlay adapter.",
        ),
        VisualAdapterVendorLeakageComplianceEntry(
            compliance_entry_id="visual_adapter_vendor_leakage_compliance_004",
            adapter_contract_id=motion_adapter.contract_id,
            compliance_scope="motion_adapter_vendor_leakage",
            vendor_identifier_exposed=False,
            vendor_payload_exposed=False,
            truth_leakage_allowed=False,
            compliance_passed=True,
            operator_visible=True,
            truth_bound=True,
            description="Canonical vendor leakage compliance entry for motion adapter.",
        ),
    )

    return VisualAdapterVendorLeakageComplianceContract(
        contract_id="visual_adapter_vendor_leakage_compliance_contract_001",
        total_entries=len(entries),
        compliance_passed_entries=sum(
            1 for entry in entries if entry.compliance_passed
        ),
        operator_visible_entries=sum(1 for entry in entries if entry.operator_visible),
        truth_bound_entries=sum(1 for entry in entries if entry.truth_bound),
        entries=entries,
    )
