from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True, slots=True)
class FlowStep:
    """Canonical architecture flow step."""

    step_order: int
    source_component: str
    target_component: str
    flow_name: str


@dataclass(frozen=True, slots=True)
class FlowMapContract:
    """Unified architecture flow map contract."""

    total_steps: int
    steps: tuple[FlowStep, ...]
