from __future__ import annotations

from dataclasses import dataclass
from typing import Tuple


_ALLOWED_ROOM_KINDS = ("direct", "family", "operator", "system", "adapter_bridge")
_ALLOWED_ROOM_MODES = ("private", "shared", "read_only_bridge")


def _ensure_non_empty(value: str, field_name: str) -> str:
    if not isinstance(value, str) or not value.strip():
        raise ValueError(f"{field_name} must be a non-empty string")
    return value.strip()


def _ensure_allowed(value: str, field_name: str, allowed: Tuple[str, ...]) -> str:
    value = _ensure_non_empty(value, field_name)
    if value not in allowed:
        raise ValueError(f"{field_name} must be one of {allowed}: {value}")
    return value


def _ensure_non_empty_tuple(values: Tuple[str, ...], field_name: str) -> Tuple[str, ...]:
    if not isinstance(values, tuple) or not values:
        raise ValueError(f"{field_name} must be a non-empty tuple")
    normalized = tuple(_ensure_non_empty(value, field_name) for value in values)
    if len(set(normalized)) != len(normalized):
        raise ValueError(f"{field_name} must not contain duplicates")
    return normalized


@dataclass(frozen=True)
class ChatRoomContract:
    """Canonical chat room contract.

    Contract only. It defines routing boundaries and room policy metadata.
    It does not create rooms in a server, OpenIM, mobile app, or database.
    """

    room_id: str
    room_kind: str
    room_mode: str
    participant_identity_ids: Tuple[str, ...]
    command_intents_allowed: bool
    direct_execution_allowed: bool
    external_adapter_room: bool = False

    def __post_init__(self) -> None:
        object.__setattr__(self, "room_id", _ensure_non_empty(self.room_id, "room_id"))
        object.__setattr__(self, "room_kind", _ensure_allowed(self.room_kind, "room_kind", _ALLOWED_ROOM_KINDS))
        object.__setattr__(self, "room_mode", _ensure_allowed(self.room_mode, "room_mode", _ALLOWED_ROOM_MODES))
        object.__setattr__(
            self,
            "participant_identity_ids",
            _ensure_non_empty_tuple(self.participant_identity_ids, "participant_identity_ids"),
        )

        if self.direct_execution_allowed:
            raise ValueError("direct_execution_allowed must be False for chat room contracts")

        if self.room_kind == "adapter_bridge" and not self.external_adapter_room:
            raise ValueError("adapter_bridge room_kind requires external_adapter_room=True")

        if self.external_adapter_room and self.command_intents_allowed:
            raise ValueError("external adapter rooms must not allow command intents")
