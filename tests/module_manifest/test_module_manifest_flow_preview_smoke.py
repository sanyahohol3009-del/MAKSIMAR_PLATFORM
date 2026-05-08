from __future__ import annotations

from MAKSIMAR_CORE_LIB.module_manifest import (
    build_module_manifest_flow_preview,
)


def test_module_manifest_flow_preview_smoke() -> None:
    preview = build_module_manifest_flow_preview()

    assert preview["preview_ready"] is True
    assert preview["flow"] == (
        "manifest_schema",
        "canonical_id_generation",
        "registry_auto_enrollment",
        "dashboard_read_only_exposure",
    )
    assert preview["total_manifests"] == 3
    assert len(preview["entries"]) == 3
