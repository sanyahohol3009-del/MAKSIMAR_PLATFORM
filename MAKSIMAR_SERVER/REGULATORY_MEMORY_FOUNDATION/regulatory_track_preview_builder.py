from __future__ import annotations

from typing import Dict

from MAKSIMAR_SERVER.REGULATORY_MEMORY_FOUNDATION.regulatory_surface_inventory import (
    build_regulatory_surface_inventory_preview,
)
from MAKSIMAR_SERVER.REGULATORY_MEMORY_FOUNDATION.regulatory_track_models import (
    build_regulatory_track_contract,
)


def build_regulatory_track_entry_preview() -> Dict[str, object]:
    contract = build_regulatory_track_contract()
    inventory = build_regulatory_surface_inventory_preview()

    preview_path = (
        "closed_memory_roadmap_v5_1_reference",
        "regulatory_track_contract",
        "regulatory_surface_inventory",
        "country_jurisdiction_registry_next",
    )

    preview_ready = (
        contract.regulatory_track_ready
        and inventory["preview_ready"] is True
        and contract.reopen_memory_v5_1_allowed is False
    )

    return {
        "preview_id": "regulatory_track_entry_preview_step_1_001",
        "preview_ready": preview_ready,
        "roadmap_family": contract.roadmap_family,
        "track_id": contract.track_id,
        "current_step": contract.current_step,
        "next_step": "STEP 2 — Country / Jurisdiction Registry Binding",
        "preview_path": preview_path,
        "stage_count": len(contract.stages),
        "rule_count": len(contract.rules),
        "surface_inventory": inventory,
        "memory_v5_1_closed_reference": contract.memory_v5_1_closed_reference,
        "reopen_memory_v5_1_allowed": contract.reopen_memory_v5_1_allowed,
        "hardening_binding_closure_track": contract.hardening_binding_closure_track,
        "no_second_memory_world": True,
        "mempalace_source_of_truth_allowed": False,
        "cross_tenant_merge_allowed": False,
        "cross_jurisdiction_merge_allowed": False,
        "runtime_mutation_allowed": False,
        "direct_core_write_allowed": False,
        "deployment_allowed_now": False,
    }
