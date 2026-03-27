from __future__ import annotations

from dataclasses import dataclass
from typing import Literal

from MAKSIMAR_CORE_LIB.oob_dashboard.display_target_vocabulary_contract import (
    build_display_target_vocabulary_contract,
)
from MAKSIMAR_CORE_LIB.oob_dashboard.panel_view_display_chain_contract import (
    build_panel_view_display_chain_contract,
)


WorkspaceId = Literal[
    "workspace_foundation_monitoring",
    "workspace_operator_main",
    "workspace_expansion_observability",
]

WorkspaceRole = Literal[
    "foundation_monitoring",
    "operator_surface",
    "expansion_surface",
]


@dataclass(frozen=True, slots=True)
class WorkspaceRegistryEntry:
    """Canonical workspace registry entry."""

    workspace_id: WorkspaceId
    workspace_role: WorkspaceRole
    display_target_id: str
    default_panel_count: int
    read_only: bool
    description: str


@dataclass(frozen=True, slots=True)
class WorkspaceRegistryContract:
    """Canonical workspace registry contract."""

    total_entries: int
    read_only_entries: int
    operator_surface_entries: int
    entries: tuple[WorkspaceRegistryEntry, ...]


def build_workspace_registry_contract() -> WorkspaceRegistryContract:
    """Build canonical workspace registry contract."""
    display_contract = build_display_target_vocabulary_contract()
    chain_contract = build_panel_view_display_chain_contract()

    display_ids = {entry.display_target_id for entry in display_contract.entries}

    workspace_specs: tuple[tuple[WorkspaceId, WorkspaceRole, str, bool, str], ...] = (
        (
            "workspace_foundation_monitoring",
            "foundation_monitoring",
            "display_secondary_diagnostics",
            True,
            "Canonical workspace for foundation and diagnostics monitoring surfaces.",
        ),
        (
            "workspace_operator_main",
            "operator_surface",
            "display_primary_operator",
            False,
            "Canonical workspace for main operator interaction surfaces.",
        ),
        (
            "workspace_expansion_observability",
            "expansion_surface",
            "display_tertiary_expansion",
            True,
            "Canonical workspace for expansion and observability surfaces.",
        ),
    )

    entries = tuple(
        WorkspaceRegistryEntry(
            workspace_id=workspace_id,
            workspace_role=workspace_role,
            display_target_id=display_target_id,
            default_panel_count=sum(
                1
                for chain_entry in chain_contract.entries
                if chain_entry.display_target_id == display_target_id
            ),
            read_only=read_only,
            description=description,
        )
        for workspace_id, workspace_role, display_target_id, read_only, description in workspace_specs
        if display_target_id in display_ids
    )

    return WorkspaceRegistryContract(
        total_entries=len(entries),
        read_only_entries=sum(1 for entry in entries if entry.read_only),
        operator_surface_entries=sum(
            1 for entry in entries if entry.workspace_role == "operator_surface"
        ),
        entries=entries,
    )
