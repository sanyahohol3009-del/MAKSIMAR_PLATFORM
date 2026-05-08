from __future__ import annotations

from MAKSIMAR_SERVER.MEMORY_REGISTRY import (
    build_global_registry_preview,
)


def test_global_registry_preview_builder_smoke() -> None:
    preview = build_global_registry_preview()

    assert preview["preview_ready"] is True
    assert preview["total_entries"] == len(preview["entries"])
    assert preview["flow"] == (
        "module_manifest",
        "canonical_id_generation",
        "registry_projection",
        "dashboard_read_only_visibility",
    )
