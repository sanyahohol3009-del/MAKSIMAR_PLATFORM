from __future__ import annotations

from dataclasses import dataclass, field

from MAKSIMAR_CORE_LIB.mobile_screen_observer.mobile_screen_frame_contract import (
    MobileScreenFrameContract,
)


@dataclass(frozen=True)
class ScreenFrameIngestResult:
    session_id: str
    frame_ref: str
    accepted: bool
    reason: str

    def to_dict(self) -> dict[str, object]:
        return {
            "session_id": self.session_id,
            "frame_ref": self.frame_ref,
            "accepted": self.accepted,
            "reason": self.reason,
        }


@dataclass
class ScreenFrameIngestRuntime:
    _accepted_refs: dict[str, tuple[str, ...]] = field(default_factory=dict)

    def ingest_reference(self, frame: MobileScreenFrameContract) -> ScreenFrameIngestResult:
        if not frame.frame_ref.strip():
            raise ValueError("frame_ref must be non-empty")
        if frame.inline_binary_payload_present:
            raise ValueError("inline binary payload is forbidden")
        if frame.pixel_decode_allowed:
            raise ValueError("pixel decode is forbidden")
        if frame.screenshot_capture_allowed:
            raise ValueError("screenshot capture is forbidden")
        if frame.screen_recording_allowed:
            raise ValueError("screen recording is forbidden")

        refs = self._accepted_refs.get(frame.session_id, tuple())
        self._accepted_refs[frame.session_id] = refs + (frame.frame_ref,)

        return ScreenFrameIngestResult(
            session_id=frame.session_id,
            frame_ref=frame.frame_ref,
            accepted=True,
            reason="metadata_reference_accepted",
        )

    def list_refs_for_session(self, session_id: str) -> tuple[str, ...]:
        return self._accepted_refs.get(session_id, tuple())

    def to_read_model(self) -> dict[str, object]:
        return {
            "runtime": "SCREEN_FRAME_INGEST_RUNTIME",
            "metadata_reference_only": True,
            "pixel_payloads_accepted": False,
            "sessions": {
                session_id: list(refs)
                for session_id, refs in sorted(self._accepted_refs.items())
            },
        }
