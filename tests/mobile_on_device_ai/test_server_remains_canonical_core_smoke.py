from __future__ import annotations

from MAKSIMAR_SERVER.MEMORY_SYNC.mobile_capability_summary_builder import (
    build_mobile_capability_summary,
)


def test_server_remains_canonical_core_in_mobile_capability_summary() -> None:
    summary = build_mobile_capability_summary()

    assert summary["server_remains_canonical_core"] is True
    assert summary["junior_is_canonical_truth"] is False
    assert summary["mirror_is_read_only"] is True
    assert summary["junior_can_execute_core_actions"] is False
    assert summary["junior_can_write_canonical_memory"] is False
    assert summary["windows_voice_edge_parked"] is True
    assert summary["push_to_talk_stt_live_parked"] is True
