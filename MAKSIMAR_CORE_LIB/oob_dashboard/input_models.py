from __future__ import annotations

from dataclasses import dataclass
from typing import Literal


InputType = Literal[
    "mouse",
    "keyboard",
    "voice",
    "gesture",
]


InputAction = Literal[
    "select",
    "navigate",
    "execute",
    "scroll",
    "switch_panel",
    "drag",
]


@dataclass(frozen=True, slots=True)
class InputEvent:
    """Unified input event from any control source."""

    input_type: InputType
    action: InputAction
    target: str | None
    value: str | None


@dataclass(frozen=True, slots=True)
class InputCapability:
    """Describes supported input type and its availability."""

    input_type: InputType
    enabled: bool
    latency_ms: int


@dataclass(frozen=True, slots=True)
class DashboardInputContract:
    """System-wide input abstraction contract."""

    capabilities: tuple[InputCapability, ...]
    supported_actions: tuple[InputAction, ...]
