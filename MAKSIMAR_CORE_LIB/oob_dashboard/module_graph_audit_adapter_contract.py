from __future__ import annotations

from dataclasses import dataclass
from typing import Tuple

from MAKSIMAR_CORE_LIB.oob_dashboard.graph_render_adapter_contract import (
    build_graph_render_adapter_contract,
)
from MAKSIMAR_CORE_LIB.oob_dashboard.module_registry_audit_contract import (
    build_module_registry_audit_contract,
)


def _require_non_empty(value: str, field_name: str) -> None:
    if not value or not value.strip():
        raise ValueError(f"{field_name} must be a non-empty string.")


@dataclass(frozen=True, slots=True)
class ModuleGraphAuditAdapterEntry:
    adapter_entry_id: str
    module_id: str
    registry_audit_id: str
    graph_adapter_contract_id: str
    graph_projection_id: str
    audit_visible: bool
    canonical_id_preserved: bool
    vendor_audit_id_exposed: bool
    audit_projection_ready: bool
    operator_visible: bool
    truth_bound: bool
    description: str

    def __post_init__(self) -> None:
        _require_non_empty(self.adapter_entry_id, "adapter_entry_id")
        _require_non_empty(self.module_id, "module_id")
        _require_non_empty(self.registry_audit_id, "registry_audit_id")
        _require_non_empty(self.graph_adapter_contract_id, "graph_adapter_contract_id")
        _require_non_empty(self.graph_projection_id, "graph_projection_id")
        _require_non_empty(self.description, "description")

        if not self.audit_visible:
            raise ValueError(
                "audit_visible must remain true for canonical module graph audit adapter entries."
            )
        if not self.canonical_id_preserved:
            raise ValueError(
                "canonical_id_preserved must remain true for canonical module graph audit adapter entries."
            )
        if self.vendor_audit_id_exposed:
            raise ValueError(
                "vendor_audit_id_exposed must remain false for canonical module graph audit adapter entries."
            )
        if not self.audit_projection_ready:
            raise ValueError(
                "audit_projection_ready must remain true for canonical module graph audit adapter entries."
            )
        if not self.operator_visible:
            raise ValueError(
                "operator_visible must remain true for canonical module graph audit adapter entries."
            )
        if not self.truth_bound:
            raise ValueError(
                "truth_bound must remain true for canonical module graph audit adapter entries."
            )


@dataclass(frozen=True, slots=True)
class ModuleGraphAuditAdapterContract:
    contract_id: str
    total_entries: int
    canonical_id_preserved_entries: int
    audit_projection_ready_entries: int
    operator_visible_entries: int
    truth_bound_entries: int
    entries: Tuple[ModuleGraphAuditAdapterEntry, ...]

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
        if self.audit_projection_ready_entries != sum(
            1 for entry in self.entries if entry.audit_projection_ready
        ):
            raise ValueError(
                "audit_projection_ready_entries must match audit_projection_ready count."
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


def build_module_graph_audit_adapter_contract() -> ModuleGraphAuditAdapterContract:
    audit_contract = build_module_registry_audit_contract()
    graph_adapter = build_graph_render_adapter_contract()

    entries = tuple(
        ModuleGraphAuditAdapterEntry(
            adapter_entry_id=f"module_graph_audit_adapter_{index:03d}",
            module_id=entry.module_id,
            registry_audit_id=entry.registry_audit_id,
            graph_adapter_contract_id=graph_adapter.contract_id,
            graph_projection_id=f"{entry.module_id}_audit_graph_projection",
            audit_visible=entry.audit_visible,
            canonical_id_preserved=True,
            vendor_audit_id_exposed=False,
            audit_projection_ready=True,
            operator_visible=True,
            truth_bound=True,
            description=f"Canonical module graph audit adapter entry for {entry.module_id}.",
        )
        for index, entry in enumerate(audit_contract.entries, start=1)
    )

    return ModuleGraphAuditAdapterContract(
        contract_id="module_graph_audit_adapter_contract_001",
        total_entries=len(entries),
        canonical_id_preserved_entries=sum(
            1 for entry in entries if entry.canonical_id_preserved
        ),
        audit_projection_ready_entries=sum(
            1 for entry in entries if entry.audit_projection_ready
        ),
        operator_visible_entries=sum(1 for entry in entries if entry.operator_visible),
        truth_bound_entries=sum(1 for entry in entries if entry.truth_bound),
        entries=entries,
    )
