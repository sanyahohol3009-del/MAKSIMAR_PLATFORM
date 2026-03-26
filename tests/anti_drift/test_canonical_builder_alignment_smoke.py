from __future__ import annotations

from MAKSIMAR_CORE_LIB.architecture_map import (
    build_module_registry_contract,
)
from MAKSIMAR_CORE_LIB.data_plane import (
    build_artifact_ownership_contract,
    build_data_plane_shell_contract,
)
from MAKSIMAR_CORE_LIB.node_roles import (
    build_node_role_contract,
)
from MAKSIMAR_CORE_LIB.oob_dashboard import (
    build_node_topology_panel_contract,
    build_project_map_panel_contract,
)
from MAKSIMAR_CORE_LIB.workers_registry import (
    build_worker_registry_contract,
    build_worker_registry_shell_contract,
)


def test_node_topology_panel_matches_canonical_node_builder() -> None:
    """Node topology panel must match canonical node role builder."""
    nodes = build_node_role_contract()
    panel = build_node_topology_panel_contract()

    assert panel.total_entries == nodes.total_nodes
    assert tuple(entry.node_id for entry in panel.entries) == tuple(
        node.node_id for node in nodes.nodes
    )


def test_project_map_panel_matches_canonical_module_registry() -> None:
    """Project map panel must match canonical module registry builder."""
    registry = build_module_registry_contract()
    panel = build_project_map_panel_contract()

    assert panel.total_entries == registry.total_modules
    assert tuple(entry.module_id for entry in panel.entries) == tuple(
        module.module_id for module in registry.modules
    )


def test_worker_shell_matches_canonical_worker_registry() -> None:
    """Worker shell must match canonical worker registry builder."""
    registry = build_worker_registry_contract()
    shell = build_worker_registry_shell_contract()

    assert shell.total_workers == registry.total_workers


def test_data_plane_shell_matches_canonical_artifact_ownership() -> None:
    """Data plane shell must match canonical artifact ownership builder."""
    ownership = build_artifact_ownership_contract()
    shell = build_data_plane_shell_contract()

    assert shell.total_ownership_entries == ownership.total_artifacts
