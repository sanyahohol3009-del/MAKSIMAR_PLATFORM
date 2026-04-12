from __future__ import annotations

from dataclasses import dataclass
from typing import Tuple


@dataclass(frozen=True)
class DataFlowPanelEntry:
    """Canonical data flow panel entry."""

    source_component: str
    target_component: str
    flow_class: str
    operator_visible: bool
    description: str


@dataclass(frozen=True)
class DataFlowPanelContract:
    """Canonical data flow panel contract."""

    panel_id: str
    total_entries: int
    entries: Tuple[DataFlowPanelEntry, ...]
    operator_visible: bool
    description: str


def build_data_flow_panel_contract() -> DataFlowPanelContract:
    """Build canonical data flow panel contract."""
    entries = (
        DataFlowPanelEntry(
            source_component="control_plane",
            target_component="execution_control",
            flow_class="control_to_execution",
            operator_visible=True,
            description="Canonical control-plane to execution-control path.",
        ),
        DataFlowPanelEntry(
            source_component="execution_control",
            target_component="workers",
            flow_class="execution_to_workers",
            operator_visible=True,
            description="Canonical execution-control to workers path.",
        ),
        DataFlowPanelEntry(
            source_component="workers",
            target_component="data_plane",
            flow_class="workers_to_data_plane",
            operator_visible=True,
            description="Canonical workers to data-plane path.",
        ),
        DataFlowPanelEntry(
            source_component="execution_observability",
            target_component="oob_dashboard",
            flow_class="observability_projection",
            operator_visible=True,
            description="Canonical execution-observability to dashboard path.",
        ),
        DataFlowPanelEntry(
            source_component="control_plane",
            target_component="execution_observability",
            flow_class="control_to_observability",
            operator_visible=True,
            description="Canonical control-plane to execution-observability path.",
        ),
    )

    return DataFlowPanelContract(
        panel_id="panel_data_flow",
        total_entries=len(entries),
        entries=entries,
        operator_visible=True,
        description="Canonical data flow panel contract.",
    )
