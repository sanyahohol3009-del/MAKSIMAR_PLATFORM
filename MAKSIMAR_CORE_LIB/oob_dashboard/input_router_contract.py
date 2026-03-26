from __future__ import annotations

from dataclasses import dataclass
from typing import Optional, Tuple

from MAKSIMAR_CORE_LIB.oob_dashboard.input_models import InputEvent
from MAKSIMAR_CORE_LIB.oob_dashboard.navigation_models import NavigationItem


@dataclass(frozen=True)
class RoutedAction:
    """
    Result of routing input into a system-level action.

    This is abstraction layer between raw input and system behavior.
    """
    action: str
    target: Optional[str]
    navigation_target: Optional[NavigationItem]


@dataclass(frozen=True)
class DashboardInputRouterContract:
    """
    Defines how input events are translated into actions and navigation.

    This is a pure contract — no execution logic.
    """
    supported_actions: Tuple[str, ...]
    supports_navigation_routing: bool
    supports_context_routing: bool


def build_dashboard_input_router_contract() -> DashboardInputRouterContract:
    """
    Build routing contract between input layer and system orchestration.
    """
    return DashboardInputRouterContract(
        supported_actions=(
            "select",
            "navigate",
            "execute",
            "scroll",
            "switch_panel",
            "drag",
        ),
        supports_navigation_routing=True,
        supports_context_routing=True,
    )
