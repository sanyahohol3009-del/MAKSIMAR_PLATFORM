from __future__ import annotations

from MAKSIMAR_SERVER.MEMORY_SYNC import (
    build_memory_sync_phase_preview,
    build_memory_sync_preview,
)


def test_phase_4_3_visible_preview_smoke() -> None:
    preview = build_memory_sync_preview()
    phase_preview = build_memory_sync_phase_preview()

    assert preview["preview_ready"] is True
    assert preview["summary_ready"] is True
    assert preview["node_scopes"] == 3
    assert preview["sync_links"] == 3
    assert preview["sync_manifests"] == 3
    assert preview["sync_routes"] == 3
    assert preview["conflict_guards"] == 3

    assert phase_preview["preview_ready"] is True
    assert phase_preview["phase_ready"] is True
    assert phase_preview["no_parallel_truth"] is True
    assert phase_preview["no_client_canonical_write"] is True
    assert phase_preview["no_mobile_security_root"] is True
