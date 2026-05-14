from __future__ import annotations

from typing import Dict

from MAKSIMAR_SERVER.ROADMAP_CLOSURE.current_state_handoff import (
    build_current_state_handoff_preview,
)
from MAKSIMAR_SERVER.ROADMAP_CLOSURE.final_acceptance_index import (
    build_final_acceptance_index_preview,
)
from MAKSIMAR_SERVER.ROADMAP_CLOSURE.final_continuity_summary import (
    build_final_continuity_preview,
)
from MAKSIMAR_SERVER.ROADMAP_CLOSURE.next_roadmap_entrypoint import (
    build_next_roadmap_entrypoint_preview,
)


def build_final_closure_preview() -> Dict[str, object]:
    acceptance = build_final_acceptance_index_preview()
    continuity = build_final_continuity_preview()
    handoff = build_current_state_handoff_preview()
    entrypoint = build_next_roadmap_entrypoint_preview()

    preview_path = (
        "final_acceptance_index",
        "final_continuity_summary",
        "current_state_handoff",
        "next_roadmap_entrypoint",
        "project_memory_savepoint_next",
    )

    preview_ready = (
        acceptance["preview_ready"] is True
        and continuity["preview_ready"] is True
        and handoff["preview_ready"] is True
        and entrypoint["preview_ready"] is True
    )

    return {
        "preview_id": "final_closure_preview_memory_roadmap_v5_1_001",
        "preview_ready": preview_ready,
        "roadmap_family": "memory_roadmap_v5_1",
        "closed_phase": "PHASE 6.8",
        "next_step": "project_memory_savepoint_after_full_roadmap",
        "preview_path": preview_path,
        "acceptance": acceptance,
        "continuity": continuity,
        "handoff": handoff,
        "entrypoint": entrypoint,
        "direct_core_write_allowed": False,
        "auto_apply_allowed": False,
        "runtime_mutation_allowed": False,
        "deployment_allowed_now": False,
        "external_release_allowed_now": False,
        "final_closure_ready": preview_ready,
    }
