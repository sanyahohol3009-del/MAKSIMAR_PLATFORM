from __future__ import annotations

from dataclasses import dataclass
from typing import Literal, Tuple

from MAKSIMAR_CORE_LIB.oob_dashboard.visual_graph_backend_contract import (
    build_visual_graph_backend_contract,
)

GraphAdapterMode = Literal[
    "canonical_to_graph_backend",
]

_ALLOWED_GRAPH_ADAPTER_MODES: tuple[GraphAdapterMode, ...] = (
    "canonical_to_graph_backend",
)


def _require_non_empty(value: str, field_name: str) -> None:
    if not value or not value.strip():
        raise ValueError(f"{field_name} must be a non-empty string.")


@dataclass(frozen=True, slots=True)
class GraphRenderAdapterEntry:
    adapter_entry_id: str
    backend_id: str
    adapter_target: str
    adapter_mode: GraphAdapterMode
    canonical_id_preserved: bool
    vendor_id_exposed: bool
    truth_leakage_allowed: bool
    replaceable: bool
    operator_visible: bool
    truth_bound: bool
    description: str

    def __post_init__(self) -> None:
        _require_non_empty(self.adapter_entry_id, "adapter_entry_id")
        _require_non_empty(self.backend_id, "backend_id")
        _require_non_empty(self.adapter_target, "adapter_target")
        _require_non_empty(self.description, "description")

        if self.adapter_mode not in _ALLOWED_GRAPH_ADAPTER_MODES:
            raise ValueError(
                f"adapter_mode must be one of {_ALLOWED_GRAPH_ADAPTER_MODES}, got {self.adapter_mode!r}."
            )
        if not self.canonical_id_preserved:
            raise ValueError(
                "canonical_id_preserved must remain true for canonical graph render adapter entries."
            )
        if self.vendor_id_exposed:
            raise ValueError(
                "vendor_id_exposed must remain false for canonical graph render adapter entries."
            )
        if self.truth_leakage_allowed:
            raise ValueError(
                "truth_leakage_allowed must remain false for canonical graph render adapter entries."
            )
        if not self.replaceable:
            raise ValueError(
                "replaceable must remain true for canonical graph render adapter entries."
            )
        if not self.operator_visible:
            raise ValueError(
                "operator_visible must remain true for canonical graph render adapter entries."
            )
        if not self.truth_bound:
            raise ValueError(
                "truth_bound must remain true for canonical graph render adapter entries."
            )


@dataclass(frozen=True, slots=True)
class GraphRenderAdapterContract:
    contract_id: str
    total_entries: int
    canonical_id_preserved_entries: int
    replaceable_entries: int
    operator_visible_entries: int
    truth_bound_entries: int
    entries: Tuple[GraphRenderAdapterEntry, ...]

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


def build_graph_render_adapter_contract() -> GraphRenderAdapterContract:
    graph_backend = build_visual_graph_backend_contract()

    entries = (
        GraphRenderAdapterEntry(
            adapter_entry_id="graph_render_adapter_001",
            backend_id=graph_backend.backend_id,
            adapter_target="topology_family_graph_projection",
            adapter_mode="canonical_to_graph_backend",
            canonical_id_preserved=True,
            vendor_id_exposed=False,
            truth_leakage_allowed=False,
            replaceable=True,
            operator_visible=True,
            truth_bound=True,
            description="Canonical graph adapter entry for topology family projection.",
        ),
        GraphRenderAdapterEntry(
            adapter_entry_id="graph_render_adapter_002",
            backend_id=graph_backend.backend_id,
            adapter_target="dependency_dataflow_graph_projection",
            adapter_mode="canonical_to_graph_backend",
            canonical_id_preserved=True,
            vendor_id_exposed=False,
            truth_leakage_allowed=False,
            replaceable=True,
            operator_visible=True,
            truth_bound=True,
            description="Canonical graph adapter entry for dependency/dataflow projection.",
        ),
        GraphRenderAdapterEntry(
            adapter_entry_id="graph_render_adapter_003",
            backend_id=graph_backend.backend_id,
            adapter_target="module_graph_projection",
            adapter_mode="canonical_to_graph_backend",
            canonical_id_preserved=True,
            vendor_id_exposed=False,
            truth_leakage_allowed=False,
            replaceable=True,
            operator_visible=True,
            truth_bound=True,
            description="Canonical graph adapter entry for module graph projection.",
        ),
    )

    return GraphRenderAdapterContract(
        contract_id="graph_render_adapter_contract_001",
        total_entries=len(entries),
        canonical_id_preserved_entries=sum(
            1 for entry in entries if entry.canonical_id_preserved
        ),
        replaceable_entries=sum(1 for entry in entries if entry.replaceable),
        operator_visible_entries=sum(1 for entry in entries if entry.operator_visible),
        truth_bound_entries=sum(1 for entry in entries if entry.truth_bound),
        entries=entries,
    )
