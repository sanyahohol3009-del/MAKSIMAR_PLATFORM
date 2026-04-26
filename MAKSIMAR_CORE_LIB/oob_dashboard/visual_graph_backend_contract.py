from __future__ import annotations

from dataclasses import dataclass

from MAKSIMAR_CORE_LIB.oob_dashboard.visual_backend_contract import (
    build_visual_backend_contract,
)


def _require_non_empty(value: str, field_name: str) -> None:
    if not value or not value.strip():
        raise ValueError(f"{field_name} must be a non-empty string.")


@dataclass(frozen=True, slots=True)
class VisualGraphBackendContract:
    contract_id: str
    backend_id: str
    graph_backend_name: str
    supports_node_rendering: bool
    supports_edge_rendering: bool
    supports_pan_zoom: bool
    supports_selection: bool
    replaceable: bool
    operator_visible: bool
    truth_bound: bool
    description: str

    def __post_init__(self) -> None:
        _require_non_empty(self.contract_id, "contract_id")
        _require_non_empty(self.backend_id, "backend_id")
        _require_non_empty(self.graph_backend_name, "graph_backend_name")
        _require_non_empty(self.description, "description")

        if not self.supports_node_rendering:
            raise ValueError(
                "supports_node_rendering must remain true for canonical visual graph backend contract."
            )
        if not self.supports_edge_rendering:
            raise ValueError(
                "supports_edge_rendering must remain true for canonical visual graph backend contract."
            )
        if not self.supports_pan_zoom:
            raise ValueError(
                "supports_pan_zoom must remain true for canonical visual graph backend contract."
            )
        if not self.supports_selection:
            raise ValueError(
                "supports_selection must remain true for canonical visual graph backend contract."
            )
        if not self.replaceable:
            raise ValueError(
                "replaceable must remain true for canonical visual graph backend contract."
            )
        if not self.operator_visible:
            raise ValueError(
                "operator_visible must remain true for canonical visual graph backend contract."
            )
        if not self.truth_bound:
            raise ValueError(
                "truth_bound must remain true for canonical visual graph backend contract."
            )


def build_visual_graph_backend_contract() -> VisualGraphBackendContract:
    backend_contract = build_visual_backend_contract()
    graph_entry = next(
        entry for entry in backend_contract.entries if entry.backend_type == "graph_backend"
    )

    return VisualGraphBackendContract(
        contract_id="visual_graph_backend_contract_001",
        backend_id=graph_entry.backend_id,
        graph_backend_name=graph_entry.backend_name,
        supports_node_rendering=True,
        supports_edge_rendering=True,
        supports_pan_zoom=True,
        supports_selection=True,
        replaceable=True,
        operator_visible=True,
        truth_bound=True,
        description="Canonical visual graph backend boundary contract.",
    )
