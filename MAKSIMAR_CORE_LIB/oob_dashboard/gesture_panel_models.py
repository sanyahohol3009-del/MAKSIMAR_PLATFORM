from __future__ import annotations

from dataclasses import dataclass
from typing import Literal


GestureType = Literal[
    "swipe",
    "pinch",
    "tap",
    "drag",
    "custom",
]


@dataclass(frozen=True, slots=True)
class GestureBinding:
    """One gesture → action binding."""

    gesture: GestureType
    action: str
    enabled: bool


@dataclass(frozen=True, slots=True)
class DashboardGesturePanel:
    """Gesture control panel contract."""

    panel_id: str
    bindings: tuple[GestureBinding, ...]
