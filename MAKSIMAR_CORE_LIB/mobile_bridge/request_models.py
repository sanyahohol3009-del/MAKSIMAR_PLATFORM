from __future__ import annotations

from dataclasses import dataclass
from typing import Literal


MobileRequestType = Literal[
    "query",
    "task_submission",
    "status_check",
    "notification_ack",
]

MobileClientType = Literal[
    "android",
    "ios",
]


@dataclass(frozen=True, slots=True)
class MobileRequest:
    """Canonical mobile request contract."""

    request_id: str
    client_type: MobileClientType
    request_type: MobileRequestType
    payload_ref: str
    core_write_allowed: bool
    heavy_execution_allowed: bool


@dataclass(frozen=True, slots=True)
class MobileRequestContract:
    """Unified mobile request contract set."""

    total_requests: int
    requests: tuple[MobileRequest, ...]
