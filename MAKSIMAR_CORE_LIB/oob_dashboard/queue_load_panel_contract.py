from __future__ import annotations

from dataclasses import dataclass
from typing import Tuple


@dataclass(frozen=True)
class QueueLoadPanelEntry:
    """Canonical queue/load panel entry."""

    metric_name: str
    metric_value: str
    operator_visible: bool
    description: str


@dataclass(frozen=True)
class QueueLoadPanelContract:
    """Canonical queue/load panel contract."""

    panel_id: str
    total_entries: int
    entries: Tuple[QueueLoadPanelEntry, ...]
    operator_visible: bool
    description: str


def build_queue_load_panel_contract() -> QueueLoadPanelContract:
    """Build canonical queue/load panel contract."""
    entries = (
        QueueLoadPanelEntry(
            metric_name="execution_routes",
            metric_value="3",
            operator_visible=True,
            description="Canonical execution routes metric.",
        ),
        QueueLoadPanelEntry(
            metric_name="lease_count",
            metric_value="0",
            operator_visible=True,
            description="Canonical lease count metric.",
        ),
        QueueLoadPanelEntry(
            metric_name="queue_depth",
            metric_value="0",
            operator_visible=True,
            description="Canonical queue depth metric.",
        ),
        QueueLoadPanelEntry(
            metric_name="load_state",
            metric_value="nominal",
            operator_visible=True,
            description="Canonical load-state metric.",
        ),
        QueueLoadPanelEntry(
            metric_name="worker_capacity",
            metric_value="available",
            operator_visible=True,
            description="Canonical worker capacity metric.",
        ),
    )

    return QueueLoadPanelContract(
        panel_id="panel_queue_load",
        total_entries=len(entries),
        entries=entries,
        operator_visible=True,
        description="Canonical queue/load panel contract.",
    )
