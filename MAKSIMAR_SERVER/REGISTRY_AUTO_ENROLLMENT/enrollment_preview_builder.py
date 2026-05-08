from __future__ import annotations

from typing import Dict

from MAKSIMAR_SERVER.REGISTRY_AUTO_ENROLLMENT.existing_domain_inventory import (
    build_existing_domain_inventory,
)
from MAKSIMAR_SERVER.REGISTRY_AUTO_ENROLLMENT.existing_domain_minimal_manifest_builder import (
    build_existing_domain_minimal_manifest_contract,
)
from MAKSIMAR_SERVER.REGISTRY_AUTO_ENROLLMENT.registry_auto_enrollment_contract import (
    build_registry_auto_enrollment_contract,
)


_ENROLLMENT_FLOW = (
    "module_discovered",
    "id_assigned",
    "storage_node_id_assigned",
    "retrieval_source_id_assigned",
    "registry_entry_ready",
    "dashboard_exposure_ready",
    "observability_binding_ready",
)


def build_registry_auto_enrollment_preview() -> Dict[str, object]:
    """Build read-only preview for registry auto-enrollment.

    This preview does not write manifests and does not mutate registry state.
    """
    base_contract = build_registry_auto_enrollment_contract()
    inventory = build_existing_domain_inventory()
    minimal_manifest = build_existing_domain_minimal_manifest_contract(inventory)

    return {
        "flow": _ENROLLMENT_FLOW,
        "base_manifest_entries": base_contract.total_entries,
        "existing_domain_entries": inventory.total_entries,
        "minimal_manifest_preview_entries": minimal_manifest.total_entries,
        "domain_cube_entries": inventory.domain_cube_entries,
        "platform_layer_entries": inventory.platform_layer_entries,
        "shell_adapter_entries": inventory.shell_adapter_entries,
        "server_registry_entries": inventory.server_registry_entries,
        "entries": tuple(
            {
                "module_slug": entry.domain_slug,
                "source_path": entry.source_path,
                "storage_node_id": entry.storage_node_id,
                "retrieval_source_id": entry.retrieval_source_id,
                "dashboard_exposure_id": entry.dashboard_exposure_id,
                "observability_binding_id": entry.observability_binding_id,
                "flow": _ENROLLMENT_FLOW,
            }
            for entry in inventory.entries
        ),
        "preview_ready": True,
    }
