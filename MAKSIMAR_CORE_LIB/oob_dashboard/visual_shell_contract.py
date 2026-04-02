from __future__ import annotations

from dataclasses import dataclass

from MAKSIMAR_CORE_LIB.oob_dashboard.main_operator_dashboard_contract import (
    build_main_operator_dashboard_contract,
)
from MAKSIMAR_CORE_LIB.oob_dashboard.main_operator_dashboard_read_model_contract import (
    build_main_operator_dashboard_read_model_contract,
)
from MAKSIMAR_CORE_LIB.oob_dashboard.visual_shell_canonical_panel_contract import (
    build_visual_shell_canonical_panel_contract,
)
from MAKSIMAR_CORE_LIB.oob_dashboard.workspace_registry_contract import (
    build_workspace_registry_contract,
)


@dataclass(frozen=True, slots=True)
class VisualShellEntry:
    """Canonical visual-shell entry."""

    shell_id: str
    dashboard_id: str
    workspace_id: str
    display_target_id: str
    total_panels: int
    canonical_panel_entries: int
    renderer_ready: bool
    read_only: bool
    interactive: bool
    visual_mode: str
    description: str


@dataclass(frozen=True, slots=True)
class VisualShellContract:
    """Canonical visual-shell contract."""

    contract_id: str
    total_entries: int
    renderer_ready_entries: int
    read_only_entries: int
    interactive_entries: int
    total_canonical_panel_entries: int
    entries: tuple[VisualShellEntry, ...]


def build_visual_shell_contract() -> VisualShellContract:
    """Build canonical visual-shell contract."""
    main_operator_dashboard = build_main_operator_dashboard_contract()
    main_operator_read_model = build_main_operator_dashboard_read_model_contract()
    visual_shell_panel_contract = build_visual_shell_canonical_panel_contract()
    workspace_registry = build_workspace_registry_contract()

    workspace_registry_map = {
        entry.workspace_id: entry for entry in workspace_registry.entries
    }
    read_model_map = {
        entry.workspace_id: entry for entry in main_operator_read_model.entries
    }

    entries = tuple(
        VisualShellEntry(
            shell_id="visual_shell_001",
            dashboard_id=dashboard_entry.dashboard_id,
            workspace_id=dashboard_entry.workspace_id,
            display_target_id=dashboard_entry.display_target_id,
            total_panels=read_model_map[dashboard_entry.workspace_id].total_panels,
            canonical_panel_entries=visual_shell_panel_contract.total_entries,
            renderer_ready=(
                visual_shell_panel_contract.legacy_alias_entries == 0
                and visual_shell_panel_contract.total_entries > 0
            ),
            read_only=workspace_registry_map[dashboard_entry.workspace_id].read_only,
            interactive=not workspace_registry_map[dashboard_entry.workspace_id].read_only,
            visual_mode="operator_hud",
            description=(
                f"Canonical visual shell entry for "
                f"{dashboard_entry.workspace_id} on "
                f"{dashboard_entry.display_target_id}."
            ),
        )
        for dashboard_entry in main_operator_dashboard.entries
        if dashboard_entry.workspace_id in read_model_map
        and dashboard_entry.workspace_id in workspace_registry_map
    )

    return VisualShellContract(
        contract_id="visual_shell_contract_001",
        total_entries=len(entries),
        renderer_ready_entries=sum(1 for entry in entries if entry.renderer_ready),
        read_only_entries=sum(1 for entry in entries if entry.read_only),
        interactive_entries=sum(1 for entry in entries if entry.interactive),
        total_canonical_panel_entries=visual_shell_panel_contract.total_entries,
        entries=entries,
    )
