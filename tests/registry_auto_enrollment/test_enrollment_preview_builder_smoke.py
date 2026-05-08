from __future__ import annotations

from MAKSIMAR_SERVER.REGISTRY_AUTO_ENROLLMENT import (
    build_registry_auto_enrollment_preview,
)


def test_enrollment_preview_builder_smoke() -> None:
    preview = build_registry_auto_enrollment_preview()

    assert preview["preview_ready"] is True
    assert preview["flow"] == (
        "module_discovered",
        "id_assigned",
        "storage_node_id_assigned",
        "retrieval_source_id_assigned",
        "registry_entry_ready",
        "dashboard_exposure_ready",
        "observability_binding_ready",
    )
    assert preview["existing_domain_entries"] == len(preview["entries"])
    assert preview["minimal_manifest_preview_entries"] == preview["existing_domain_entries"]

    for entry in preview["entries"]:
        assert entry["storage_node_id"].startswith("storage_node_")
        assert entry["retrieval_source_id"].startswith("retrieval_source_")
        assert entry["dashboard_exposure_id"].startswith("panel_")
        assert entry["observability_binding_id"].startswith("observability_")
