from __future__ import annotations

import inspect
from pathlib import Path

from tools.jarvis_live_runtime import jarvis_live_brain_loop
from tools.jarvis_live_runtime import jarvis_live_stream_events


def test_brain_loop_uses_canonical_semantic_boundary_without_text_planner() -> None:
    source = Path(jarvis_live_brain_loop.__file__).read_text(encoding="utf-8")
    assert "run_canonical_brain_once" in source
    assert "stream_canonical_brain_response" in source
    assert "jarvis_live_request_planner" not in source
    assert "_plan_jarvis_request" not in source


def test_brain_loop_uses_stream_events_boundary() -> None:
    event = jarvis_live_stream_events._event("done", ok=True)
    assert event["event"] == "done"
    assert event["ok"] is True
    assert event["pc_control_allowed"] is False


def test_stream_reasoning_filter_hides_thinking() -> None:
    state = {"inside_reasoning": False}
    assert jarvis_live_stream_events._filter_reasoning_chunk("<think>hidden</think>visible", state) == "visible"
