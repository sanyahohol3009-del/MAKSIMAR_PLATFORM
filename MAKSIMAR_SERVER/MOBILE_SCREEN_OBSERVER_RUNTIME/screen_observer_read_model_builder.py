from __future__ import annotations

from dataclasses import dataclass

from MAKSIMAR_SERVER.MOBILE_SCREEN_OBSERVER_RUNTIME.mobile_screen_observer_session_registry import (
    MobileScreenObserverSessionRegistry,
)
from MAKSIMAR_SERVER.MOBILE_SCREEN_OBSERVER_RUNTIME.screen_frame_ingest_runtime import (
    ScreenFrameIngestRuntime,
)


@dataclass(frozen=True)
class ScreenObserverReadModelBuilder:
    session_registry: MobileScreenObserverSessionRegistry
    frame_runtime: ScreenFrameIngestRuntime

    def build(self) -> dict[str, object]:
        return {
            "panel": "phone_window",
            "runtime": "MOBILE_SCREEN_OBSERVER_RUNTIME",
            "read_only": True,
            "child_control_enabled": False,
            "remote_control_enabled": False,
            "screen_capture_runtime_enabled": False,
            "touch_keyboard_runtime_enabled": False,
            "session_registry": self.session_registry.to_read_model(),
            "frame_ingest": self.frame_runtime.to_read_model(),
        }
