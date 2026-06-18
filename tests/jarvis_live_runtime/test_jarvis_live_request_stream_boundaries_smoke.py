from __future__ import annotations

import inspect

from tools.jarvis_live_runtime import jarvis_live_brain_loop
from tools.jarvis_live_runtime import jarvis_live_request_planner
from tools.jarvis_live_runtime import jarvis_live_stream_events


def test_brain_loop_uses_request_planner_boundary() -> None:
    assert inspect.getmodule(jarvis_live_brain_loop._plan_jarvis_request).__name__ == (
        "tools.jarvis_live_runtime.jarvis_live_request_planner"
    )
    assert jarvis_live_request_planner._route_mode("джарвис привет") == "FAST"
    assert jarvis_live_request_planner._plan_jarvis_request("джарвис запусти браузер")["request_route"] == "pc_action_proposal"


def test_brain_loop_uses_stream_events_boundary() -> None:
    assert inspect.getmodule(jarvis_live_brain_loop._event).__name__ == (
        "tools.jarvis_live_runtime.jarvis_live_stream_events"
    )
    event = jarvis_live_stream_events._event("done", ok=True)
    assert event["event"] == "done"
    assert event["ok"] is True
    assert event["pc_control_allowed"] is False


def test_stream_reasoning_filter_hides_thinking() -> None:
    state = {"inside_reasoning": False}
    assert jarvis_live_stream_events._filter_reasoning_chunk("<think>hidden</think>visible", state) == "visible"
