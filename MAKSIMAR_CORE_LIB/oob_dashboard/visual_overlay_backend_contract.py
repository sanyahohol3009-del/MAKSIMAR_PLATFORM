from __future__ import annotations

from dataclasses import dataclass

from MAKSIMAR_CORE_LIB.oob_dashboard.visual_backend_contract import (
    build_visual_backend_contract,
)


def _require_non_empty(value: str, field_name: str) -> None:
    if not value or not value.strip():
        raise ValueError(f"{field_name} must be a non-empty string.")


@dataclass(frozen=True, slots=True)
class VisualOverlayBackendContract:
    contract_id: str
    backend_id: str
    overlay_backend_name: str
    supports_signal_overlay: bool
    supports_topology_overlay: bool
    supports_explainability_overlay: bool
    supports_depth_layers: bool
    replaceable: bool
    operator_visible: bool
    truth_bound: bool
    description: str

    def __post_init__(self) -> None:
        _require_non_empty(self.contract_id, "contract_id")
        _require_non_empty(self.backend_id, "backend_id")
        _require_non_empty(self.overlay_backend_name, "overlay_backend_name")
        _require_non_empty(self.description, "description")

        if not self.supports_signal_overlay:
            raise ValueError(
                "supports_signal_overlay must remain true for canonical visual overlay backend contract."
            )
        if not self.supports_topology_overlay:
            raise ValueError(
                "supports_topology_overlay must remain true for canonical visual overlay backend contract."
            )
        if not self.supports_explainability_overlay:
            raise ValueError(
                "supports_explainability_overlay must remain true for canonical visual overlay backend contract."
            )
        if not self.supports_depth_layers:
            raise ValueError(
                "supports_depth_layers must remain true for canonical visual overlay backend contract."
            )
        if not self.replaceable:
            raise ValueError(
                "replaceable must remain true for canonical visual overlay backend contract."
            )
        if not self.operator_visible:
            raise ValueError(
                "operator_visible must remain true for canonical visual overlay backend contract."
            )
        if not self.truth_bound:
            raise ValueError(
                "truth_bound must remain true for canonical visual overlay backend contract."
            )


def build_visual_overlay_backend_contract() -> VisualOverlayBackendContract:
    backend_contract = build_visual_backend_contract()
    overlay_entry = next(
        entry for entry in backend_contract.entries if entry.backend_type == "overlay_backend"
    )

    return VisualOverlayBackendContract(
        contract_id="visual_overlay_backend_contract_001",
        backend_id=overlay_entry.backend_id,
        overlay_backend_name=overlay_entry.backend_name,
        supports_signal_overlay=True,
        supports_topology_overlay=True,
        supports_explainability_overlay=True,
        supports_depth_layers=True,
        replaceable=True,
        operator_visible=True,
        truth_bound=True,
        description="Canonical visual overlay backend boundary contract.",
    )
