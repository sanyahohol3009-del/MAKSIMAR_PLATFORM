from __future__ import annotations

from dataclasses import dataclass, field
from typing import Tuple


@dataclass(frozen=True)
class CanonicalPanelIdentity:
    """Canonical backward-compatible execution-panel identity."""

    panel_id: str
    panel_name: str
    category: str = "execution"
    panel_family: str = "execution_monitoring"
    panel_kind: str = "execution_panel"
    panel_role: str = "read_only_monitoring"
    read_only: bool = True
    operator_visible: bool = True


@dataclass(frozen=True)
class CanonicalPanelIdentityContract:
    """Canonical backward-compatible execution-panel identity contract."""

    total_panels: int
    panels: Tuple[CanonicalPanelIdentity, ...]
    read_only_panels: int = field(init=False)
    operator_visible_panels: int = field(init=False)

    def __post_init__(self) -> None:
        object.__setattr__(
            self,
            "read_only_panels",
            sum(1 for panel in self.panels if panel.read_only),
        )
        object.__setattr__(
            self,
            "operator_visible_panels",
            sum(1 for panel in self.panels if panel.operator_visible),
        )


def build_canonical_panel_identity_contract() -> CanonicalPanelIdentityContract:
    """Build canonical execution-panel identity contract."""
    panels = (
        CanonicalPanelIdentity(
            panel_id="panel_queue_load",
            panel_name="Queue & Load Panel",
        ),
        CanonicalPanelIdentity(
            panel_id="panel_node_topology",
            panel_name="Node Topology Panel",
        ),
        CanonicalPanelIdentity(
            panel_id="panel_degraded_mode",
            panel_name="Degraded Mode Panel",
        ),
        CanonicalPanelIdentity(
            panel_id="panel_project_map",
            panel_name="Project Map Panel",
        ),
        CanonicalPanelIdentity(
            panel_id="panel_data_flow",
            panel_name="Data Flow Panel",
        ),
        CanonicalPanelIdentity(
            panel_id="panel_dependency_map",
            panel_name="Dependency / Cube Map Panel",
        ),
        CanonicalPanelIdentity(
            panel_id="panel_version_control_dashboard",
            panel_name="Version Control Panel",
        ),
    )
    return CanonicalPanelIdentityContract(
        total_panels=len(panels),
        panels=panels,
    )
