from __future__ import annotations

from dataclasses import dataclass
from typing import Literal


ChatInputMode = Literal[
    "text",
    "voice",
    "gesture",
]

ChatOutputMode = Literal[
    "text",
    "code",
    "diagnostic",
]


@dataclass(frozen=True, slots=True)
class DashboardChatInputBinding:
    """Binding between chat pane and unified input abstraction."""

    input_mode: ChatInputMode
    enabled: bool
    routed_through_input_contract: bool


@dataclass(frozen=True, slots=True)
class DashboardChatInputContract:
    """Unified chat-input contract for OOB dashboard."""

    bindings: tuple[DashboardChatInputBinding, ...]
    output_modes: tuple[ChatOutputMode, ...]
