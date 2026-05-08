from __future__ import annotations

from typing import Dict

from MAKSIMAR_SERVER.MEMORY_REGISTRY.global_registry_projection_builder import (
    build_global_registry_projection_contract,
)
from MAKSIMAR_SERVER.MEMORY_REGISTRY.global_registry_projection_models import (
    GlobalRegistryProjectionContract,
)


def build_global_registry_preview(
    contract: GlobalRegistryProjectionContract | None = None,
) -> Dict[str, object]:
    """Build deterministic read-only preview for global registry projection."""

    selected_contract = contract or build_global_registry_projection_contract()

    return {
        "total_entries": selected_contract.total_entries,
        "dashboard_visible_entries": selected_contract.dashboard_visible_entries,
        "retrieval_visible_entries": selected_contract.retrieval_visible_entries,
        "observability_visible_entries": selected_contract.observability_visible_entries,
        "entry_kinds": tuple(sorted({entry.entry_kind for entry in selected_contract.entries})),
        "flow": (
            "module_manifest",
            "canonical_id_generation",
            "registry_projection",
            "dashboard_read_only_visibility",
        ),
        "entries": tuple(
            {
                "entry_kind": entry.entry_kind,
                "registry_id": entry.registry_id,
                "module_slug": entry.module_slug,
                "module_id": entry.module_id,
                "source_layer": entry.source_layer,
                "dashboard_visible": entry.dashboard_visible,
                "retrieval_visible": entry.retrieval_visible,
                "observability_visible": entry.observability_visible,
                "flow_stages": entry.flow_stages,
            }
            for entry in selected_contract.entries
        ),
        "preview_ready": True,
    }
