from __future__ import annotations

from dataclasses import dataclass
from typing import Tuple

from MAKSIMAR_CORE_LIB.oob_dashboard.panel_registry_contract import (
    build_panel_registry_contract,
)


@dataclass(frozen=True)
class ViewCompositionEntry:
    """Canonical backward-compatible view composition entry."""

    view_id: str
    workspace_id: str
    panel_count: int
    active_panel_id: str
    composition_state: str
    operator_visible: bool
    description: str


@dataclass(frozen=True)
class ViewCompositionContract:
    """Canonical backward-compatible view composition contract."""

    contract_id: str
    total_entries: int
    total_panels: int
    composed_panels: Tuple[str, ...]
    entries: Tuple[ViewCompositionEntry, ...]
    active_panel_id: str
    operator_visible: bool
    description: str


def _resolve_panel_entries(panel_registry_contract: object) -> tuple[object, ...]:
    """Resolve panel registry entries from backward-compatible shapes."""
    if hasattr(panel_registry_contract, "panels"):
        return tuple(getattr(panel_registry_contract, "panels"))
    if hasattr(panel_registry_contract, "entries"):
        return tuple(getattr(panel_registry_contract, "entries"))
    return ()


def build_dashboard_view_composition_contract() -> ViewCompositionContract:
    """Build canonical backward-compatible view composition contract."""
    panel_registry_contract = build_panel_registry_contract()
    registry_entries = _resolve_panel_entries(panel_registry_contract)

    active_panel_id = "panel_consistency"

    panel_count_by_workspace: dict[str, int] = {}
    composed_panels = []

    for entry in registry_entries:
        panel_id = getattr(entry, "panel_id", "")
        workspace_id = getattr(entry, "workspace_id", "workspace_operator_main")
        panel_count_by_workspace[workspace_id] = (
            panel_count_by_workspace.get(workspace_id, 0) + 1
        )
        if isinstance(panel_id, str) and panel_id:
            composed_panels.append(panel_id)

    workspace_ids = sorted(set(panel_count_by_workspace) or {"workspace_operator_main"})

    entries = tuple(
        ViewCompositionEntry(
            view_id=f"view_composition_{index:03d}",
            workspace_id=workspace_id,
            panel_count=panel_count_by_workspace.get(workspace_id, 0),
            active_panel_id=active_panel_id,
            composition_state="view_composition_ready",
            operator_visible=True,
            description=f"Canonical view composition entry for {workspace_id}.",
        )
        for index, workspace_id in enumerate(workspace_ids, start=1)
    )

    return ViewCompositionContract(
        contract_id="view_composition_contract_001",
        total_entries=len(entries),
        total_panels=len(registry_entries),
        composed_panels=tuple(composed_panels),
        entries=entries,
        active_panel_id=active_panel_id,
        operator_visible=True,
        description="Canonical backward-compatible view composition contract.",
    )


def build_view_composition_contract() -> ViewCompositionContract:
    """Backward-compatible alias."""
    return build_dashboard_view_composition_contract()
