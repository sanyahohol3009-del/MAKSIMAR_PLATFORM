from __future__ import annotations

from MAKSIMAR_CORE_LIB.module_manifest import (
    build_module_manifest_flow_preview,
)


def test_module_manifest_flow_entries_smoke() -> None:
    preview = build_module_manifest_flow_preview()
    entries = preview["entries"]

    for entry in entries:
        assert entry["module_slug"]
        assert entry["storage_profile"]
        assert entry["retrieval_profile"]
        assert entry["enrollment_allowed"] is True
        assert entry["dashboard_exposure_allowed"] is True
        assert entry["manifest_flow"] == preview["flow"]
