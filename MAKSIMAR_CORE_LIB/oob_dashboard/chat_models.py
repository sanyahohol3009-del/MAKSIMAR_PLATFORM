from __future__ import annotations

from dataclasses import dataclass
from typing import Literal


ChatRole = Literal[
    "user",
    "jarvis",
    "system",
]

ChatContentType = Literal[
    "text",
    "code",
    "diagnostic",
]


@dataclass(frozen=True, slots=True)
class DashboardChatMessage:
    """One chat-pane message for OOB dashboard."""

    message_id: str
    role: ChatRole
    content_type: ChatContentType
    content: str


@dataclass(frozen=True, slots=True)
class DashboardChatContract:
    """Read-only contract for dashboard text/code exchange pane."""

    total_messages: int
    messages: list[DashboardChatMessage]
    copy_enabled: bool
    input_enabled: bool
