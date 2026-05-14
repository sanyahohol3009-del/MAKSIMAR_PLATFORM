from __future__ import annotations

from dataclasses import dataclass
from typing import Dict, Tuple

from MAKSIMAR_SERVER.ROADMAP_CLOSURE.current_state_handoff import (
    build_current_state_handoff_preview,
)


NEXT_ROADMAP_CANDIDATES: Tuple[str, ...] = (
    "visual_operator_dashboard_track",
    "multi_tenant_multi_country_regulatory_memory_track",
    "network_security_deployment_boundary_track",
    "repository_document_intelligence_track",
    "real_product_operator_documentation_track",
)


@dataclass(frozen=True, slots=True)
class NextRoadmapEntrypoint:
    entrypoint_id: str
    candidates: Tuple[str, ...]
    recommended_first: str
    current_state_handoff_ready: bool
    entrypoint_ready: bool

    def __post_init__(self) -> None:
        if not self.entrypoint_id:
            raise ValueError("entrypoint_id must be non-empty")
        if not self.candidates:
            raise ValueError("candidates must be non-empty")
        if self.recommended_first not in self.candidates:
            raise ValueError("recommended_first must exist in candidates")
        if self.current_state_handoff_ready is not True:
            raise ValueError("current_state_handoff_ready must be True")
        if self.entrypoint_ready is not True:
            raise ValueError("entrypoint_ready must be True")


def build_next_roadmap_entrypoint() -> NextRoadmapEntrypoint:
    handoff = build_current_state_handoff_preview()

    return NextRoadmapEntrypoint(
        entrypoint_id="next_roadmap_entrypoint_memory_roadmap_v5_1_001",
        candidates=NEXT_ROADMAP_CANDIDATES,
        recommended_first="multi_tenant_multi_country_regulatory_memory_track",
        current_state_handoff_ready=handoff["preview_ready"],
        entrypoint_ready=handoff["preview_ready"] is True,
    )


def build_next_roadmap_entrypoint_preview() -> Dict[str, object]:
    entrypoint = build_next_roadmap_entrypoint()

    return {
        "preview_id": "next_roadmap_entrypoint_preview_memory_roadmap_v5_1_001",
        "preview_ready": entrypoint.entrypoint_ready,
        "entrypoint_id": entrypoint.entrypoint_id,
        "candidates": entrypoint.candidates,
        "recommended_first": entrypoint.recommended_first,
        "current_state_handoff_ready": entrypoint.current_state_handoff_ready,
    }
