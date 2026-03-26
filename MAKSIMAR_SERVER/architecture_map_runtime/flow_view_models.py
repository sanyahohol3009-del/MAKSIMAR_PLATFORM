from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True, slots=True)
class ServerFlowViewEntry:
    """Server-side read-only flow view entry."""

    step_order: int
    source_component: str
    target_component: str
    flow_name: str
    source_contract_bound: bool


@dataclass(frozen=True, slots=True)
class ServerFlowViewContract:
    """Unified server-side flow view contract."""

    total_steps: int
    steps: tuple[ServerFlowViewEntry, ...]
