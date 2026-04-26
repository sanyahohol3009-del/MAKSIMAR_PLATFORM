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
from MAKSIMAR_CORE_LIB.oob_dashboard.visual_backend_contract import (
    build_visual_backend_contract,
)


def _require_non_empty(value: str, field_name: str) -> None:
    if not value or not value.strip():
        raise ValueError(f"{field_name} must be a non-empty string.")


@dataclass(frozen=True, slots=True)
class VisualBackendReplaceabilityEntry:
    replaceability_entry_id: str
    backend_id: str
    adapter_contract_id: str
    swap_ready: bool
    canonical_contract_change_required: bool
    read_model_change_required: bool
    direct_vendor_dependency_allowed: bool
    replaceable: bool
    operator_visible: bool
    truth_bound: bool
    description: str

    def __post_init__(self) -> None:
        _require_non_empty(self.replaceability_entry_id, "replaceability_entry_id")
        _require_non_empty(self.backend_id, "backend_id")
        _require_non_empty(self.adapter_contract_id, "adapter_contract_id")
        _require_non_empty(self.description, "description")

        if not self.swap_ready:
            raise ValueError(
                "swap_ready must remain true for canonical visual backend replaceability entries."
            )
        if self.canonical_contract_change_required:
            raise ValueError(
                "canonical_contract_change_required must remain false for canonical visual backend replaceability entries."
            )
        if self.read_model_change_required:
            raise ValueError(
                "read_model_change_required must remain false for canonical visual backend replaceability entries."
            )
        if self.direct_vendor_dependency_allowed:
            raise ValueError(
                "direct_vendor_dependency_allowed must remain false for canonical visual backend replaceability entries."
            )
        if not self.replaceable:
            raise ValueError(
                "replaceable must remain true for canonical visual backend replaceability entries."
            )
        if not self.operator_visible:
            raise ValueError(
                "operator_visible must remain true for canonical visual backend replaceability entries."
            )
        if not self.truth_bound:
            raise ValueError(
                "truth_bound must remain true for canonical visual backend replaceability entries."
            )


@dataclass(frozen=True, slots=True)
class VisualBackendReplaceabilityContract:
    contract_id: str
    total_entries: int
    swap_ready_entries: int
    replaceable_entries: int
    operator_visible_entries: int
    truth_bound_entries: int
    entries: Tuple[VisualBackendReplaceabilityEntry, ...]

    def __post_init__(self) -> None:
        _require_non_empty(self.contract_id, "contract_id")

        if self.total_entries != len(self.entries):
            raise ValueError("total_entries must match len(entries).")
        if self.swap_ready_entries != sum(
            1 for entry in self.entries if entry.swap_ready
        ):
            raise ValueError("swap_ready_entries must match swap_ready count.")
        if self.replaceable_entries != sum(
            1 for entry in self.entries if entry.replaceable
        ):
            raise ValueError("replaceable_entries must match replaceable count.")
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


def build_visual_backend_replaceability_contract() -> (
    VisualBackendReplaceabilityContract
):
    backend_contract = build_visual_backend_contract()
    graph_adapter = build_graph_render_adapter_contract()
    chart_adapter = build_chart_render_adapter_contract()
    overlay_adapter = build_overlay_render_adapter_contract()
    motion_adapter = build_motion_render_adapter_contract()

    adapter_map = {
        "visual_backend_graph_001": graph_adapter.contract_id,
        "visual_backend_chart_001": chart_adapter.contract_id,
        "visual_backend_overlay_001": overlay_adapter.contract_id,
        "motion_backend_virtual_001": motion_adapter.contract_id,
    }

    entries = (
        VisualBackendReplaceabilityEntry(
            replaceability_entry_id="visual_backend_replaceability_001",
            backend_id=backend_contract.entries[0].backend_id,
            adapter_contract_id=adapter_map[backend_contract.entries[0].backend_id],
            swap_ready=True,
            canonical_contract_change_required=False,
            read_model_change_required=False,
            direct_vendor_dependency_allowed=False,
            replaceable=True,
            operator_visible=True,
            truth_bound=True,
            description="Canonical replaceability entry for graph backend.",
        ),
        VisualBackendReplaceabilityEntry(
            replaceability_entry_id="visual_backend_replaceability_002",
            backend_id=backend_contract.entries[1].backend_id,
            adapter_contract_id=adapter_map[backend_contract.entries[1].backend_id],
            swap_ready=True,
            canonical_contract_change_required=False,
            read_model_change_required=False,
            direct_vendor_dependency_allowed=False,
            replaceable=True,
            operator_visible=True,
            truth_bound=True,
            description="Canonical replaceability entry for chart backend.",
        ),
        VisualBackendReplaceabilityEntry(
            replaceability_entry_id="visual_backend_replaceability_003",
            backend_id=backend_contract.entries[2].backend_id,
            adapter_contract_id=adapter_map[backend_contract.entries[2].backend_id],
            swap_ready=True,
            canonical_contract_change_required=False,
            read_model_change_required=False,
            direct_vendor_dependency_allowed=False,
            replaceable=True,
            operator_visible=True,
            truth_bound=True,
            description="Canonical replaceability entry for overlay backend.",
        ),
        VisualBackendReplaceabilityEntry(
            replaceability_entry_id="visual_backend_replaceability_004",
            backend_id="motion_backend_virtual_001",
            adapter_contract_id=adapter_map["motion_backend_virtual_001"],
            swap_ready=True,
            canonical_contract_change_required=False,
            read_model_change_required=False,
            direct_vendor_dependency_allowed=False,
            replaceable=True,
            operator_visible=True,
            truth_bound=True,
            description="Canonical replaceability entry for motion backend boundary.",
        ),
    )

    return VisualBackendReplaceabilityContract(
        contract_id="visual_backend_replaceability_contract_001",
        total_entries=len(entries),
        swap_ready_entries=sum(1 for entry in entries if entry.swap_ready),
        replaceable_entries=sum(1 for entry in entries if entry.replaceable),
        operator_visible_entries=sum(1 for entry in entries if entry.operator_visible),
        truth_bound_entries=sum(1 for entry in entries if entry.truth_bound),
        entries=entries,
    )
