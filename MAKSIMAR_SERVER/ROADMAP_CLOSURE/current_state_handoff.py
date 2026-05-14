from __future__ import annotations

from dataclasses import dataclass
from typing import Dict, Tuple

from MAKSIMAR_SERVER.ROADMAP_CLOSURE.final_continuity_summary import (
    build_final_continuity_preview,
)


STATE_HANDOFF_ITEMS: Tuple[str, ...] = (
    "primary_current_track=memory_roadmap_v5_1",
    "current_closed_phase=PHASE_6_8",
    "next_step=Roadmap_v5_1_Final_Closure_Continuity_Savepoint",
    "sale_ready_claim_allowed=True",
    "operator_approval_required=True",
    "operator_approval_granted=False",
    "direct_core_write_allowed=False",
    "auto_apply_allowed=False",
    "runtime_mutation_allowed=False",
    "deployment_allowed_now=False",
    "external_release_allowed_now=False",
)


@dataclass(frozen=True, slots=True)
class CurrentStateHandoff:
    handoff_id: str
    state_items: Tuple[str, ...]
    continuity_ready: bool
    handoff_ready: bool

    def __post_init__(self) -> None:
        if not self.handoff_id:
            raise ValueError("handoff_id must be non-empty")
        if not self.state_items:
            raise ValueError("state_items must be non-empty")
        if self.continuity_ready is not True:
            raise ValueError("continuity_ready must be True")
        if self.handoff_ready is not True:
            raise ValueError("handoff_ready must be True")


def build_current_state_handoff() -> CurrentStateHandoff:
    continuity = build_final_continuity_preview()

    return CurrentStateHandoff(
        handoff_id="current_state_handoff_memory_roadmap_v5_1_001",
        state_items=STATE_HANDOFF_ITEMS,
        continuity_ready=continuity["preview_ready"],
        handoff_ready=continuity["preview_ready"] is True,
    )


def build_current_state_handoff_preview() -> Dict[str, object]:
    handoff = build_current_state_handoff()

    return {
        "preview_id": "current_state_handoff_preview_memory_roadmap_v5_1_001",
        "preview_ready": handoff.handoff_ready,
        "handoff_id": handoff.handoff_id,
        "state_items": handoff.state_items,
        "state_item_count": len(handoff.state_items),
        "continuity_ready": handoff.continuity_ready,
    }
