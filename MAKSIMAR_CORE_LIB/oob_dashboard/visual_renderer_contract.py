from __future__ import annotations

from dataclasses import dataclass

from MAKSIMAR_CORE_LIB.oob_dashboard.visual_render_surface_contract import (
    build_visual_render_surface_contract,
)
from MAKSIMAR_CORE_LIB.oob_dashboard.visual_shell_contract import (
    build_visual_shell_contract,
)


def _require_non_empty(value: str, field_name: str) -> None:
    if not value or not value.strip():
        raise ValueError(f"{field_name} must be a non-empty string.")


@dataclass(frozen=True, slots=True)
class VisualRendererContract:
    renderer_id: str
    shell_id: str
    render_surface_contract_id: str
    renderer_ready: bool
    semantic_leakage_allowed: bool
    operator_visible: bool
    truth_bound: bool
    description: str

    def __post_init__(self) -> None:
        _require_non_empty(self.renderer_id, "renderer_id")
        _require_non_empty(self.shell_id, "shell_id")
        _require_non_empty(self.render_surface_contract_id, "render_surface_contract_id")
        _require_non_empty(self.description, "description")

        if not self.renderer_ready:
            raise ValueError(
                "renderer_ready must remain true for canonical visual renderer contract."
            )
        if self.semantic_leakage_allowed:
            raise ValueError(
                "semantic_leakage_allowed must remain false for canonical visual renderer contract."
            )
        if not self.operator_visible:
            raise ValueError(
                "operator_visible must remain true for canonical visual renderer contract."
            )
        if not self.truth_bound:
            raise ValueError(
                "truth_bound must remain true for canonical visual renderer contract."
            )


def build_visual_renderer_contract() -> VisualRendererContract:
    shell_contract = build_visual_shell_contract()
    render_surface_contract = build_visual_render_surface_contract()

    return VisualRendererContract(
        renderer_id="visual_renderer_contract_001",
        shell_id=shell_contract.shell_id,
        render_surface_contract_id=render_surface_contract.contract_id,
        renderer_ready=True,
        semantic_leakage_allowed=False,
        operator_visible=True,
        truth_bound=True,
        description="Canonical visual renderer contract for basic HUD rendering.",
    )
