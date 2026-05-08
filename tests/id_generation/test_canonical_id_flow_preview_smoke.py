from __future__ import annotations

from MAKSIMAR_CORE_LIB.id_generation import (
    build_canonical_id_flow_preview,
)


def test_canonical_id_flow_preview_smoke() -> None:
    preview = build_canonical_id_flow_preview()
    entries = preview["entries"]

    assert preview["preview_ready"] is True
    assert preview["flow"] == (
        "module_manifest_schema",
        "canonical_id_generation",
        "collision_check",
        "registry_auto_enrollment",
        "dashboard_read_only_binding",
    )

    assert preview["total_entries"] == len(entries)
    assert preview["total_storage_node_ids"] == sum(
        1 for entry in entries if entry["storage_node_id"]
    )
    assert preview["total_retrieval_source_ids"] == sum(
        1 for entry in entries if entry["retrieval_source_id"]
    )

    for entry in entries:
        assert entry["flow"] == preview["flow"]
        assert entry["module_id"]
        assert entry["storage_node_id"] == f"storage_node_{entry['module_slug']}"
        assert entry["collision_free"] is True
