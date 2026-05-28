from __future__ import annotations

from dataclasses import dataclass, field

from MAKSIMAR_CORE_LIB.mobile_screen_observer.mobile_screen_session_contract import (
    MobileScreenSessionContract,
)


@dataclass(frozen=True)
class ScreenObserverSessionRecord:
    session: MobileScreenSessionContract

    def __post_init__(self) -> None:
        if self.session.remote_control_allowed:
            raise ValueError("normal observer session cannot allow remote control")
        if not self.session.read_only:
            raise ValueError("normal observer session must be read-only")
        if not self.session.frame_reference_only:
            raise ValueError("normal observer session must be frame-reference-only")


@dataclass
class MobileScreenObserverSessionRegistry:
    _records: dict[str, ScreenObserverSessionRecord] = field(default_factory=dict)

    def register(self, session: MobileScreenSessionContract) -> ScreenObserverSessionRecord:
        record = ScreenObserverSessionRecord(session=session)
        if session.session_id in self._records:
            raise ValueError(f"session already registered: {session.session_id}")
        self._records[session.session_id] = record
        return record

    def get(self, session_id: str) -> ScreenObserverSessionRecord:
        if session_id not in self._records:
            raise KeyError(f"unknown screen observer session: {session_id}")
        return self._records[session_id]

    def contains(self, session_id: str) -> bool:
        return session_id in self._records

    def list_session_ids(self) -> tuple[str, ...]:
        return tuple(sorted(self._records))

    def to_read_model(self) -> dict[str, object]:
        return {
            "runtime": "MOBILE_SCREEN_OBSERVER_RUNTIME",
            "read_only": True,
            "child_control_enabled": False,
            "session_count": len(self._records),
            "session_ids": self.list_session_ids(),
        }
