from __future__ import annotations

from MAKSIMAR_CORE_LIB.oob_dashboard.input_models import (
    DashboardInputContract,
    InputCapability,
)


def build_dashboard_input_contract() -> DashboardInputContract:
    """Build unified input abstraction contract."""

    capabilities = (
        InputCapability("mouse", True, 1),
        InputCapability("keyboard", True, 1),
        InputCapability("voice", True, 120),
        InputCapability("gesture", True, 80),
    )

    supported_actions = (
        "select",
        "navigate",
        "execute",
        "scroll",
        "switch_panel",
        "drag",
    )

    return DashboardInputContract(
        capabilities=capabilities,
        supported_actions=supported_actions,
    )
