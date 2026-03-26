from __future__ import annotations

from MAKSIMAR_CORE_LIB.oob_dashboard import (
    CanonicalPanelIdentity,
    CanonicalPanelIdentityContract,
)


def test_panel_identity_models_build() -> None:
    """Canonical panel identity models should build successfully."""
    contract = CanonicalPanelIdentityContract(
        total_panels=7,
        panels=(
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
        ),
    )

    assert contract.total_panels == 7
    assert len(contract.panels) == 7
    assert contract.panels[0].panel_id == "panel_queue_load"
    assert contract.panels[-1].panel_id == "panel_version_control_dashboard"
