from __future__ import annotations

from MAKSIMAR_CORE_LIB.architecture_map import (
    build_flow_map_contract,
)
from MAKSIMAR_CORE_LIB.oob_dashboard.data_flow_panel_models import (
    DataFlowPanelContract,
    DataFlowPanelEntry,
)


def build_data_flow_panel_contract() -> DataFlowPanelContract:
    """Build unified read-only data flow panel contract."""
    flow_contract = build_flow_map_contract()

    entries = tuple(
        DataFlowPanelEntry(
            step_order=step.step_order,
            source_component=step.source_component,
            target_component=step.target_component,
            flow_name=step.flow_name,
        )
        for step in flow_contract.steps
    )

    return DataFlowPanelContract(
        panel_id="panel_data_flow",
        total_entries=len(entries),
        entries=entries,
    )
