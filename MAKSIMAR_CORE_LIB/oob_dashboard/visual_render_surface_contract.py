from __future__ import annotations

from dataclasses import dataclass

from MAKSIMAR_CORE_LIB.oob_dashboard.layout_composition_contract import (
    build_layout_composition_contract,
)
from MAKSIMAR_CORE_LIB.oob_dashboard.visual_shell_contract import (
    build_visual_shell_contract,
)
from MAKSIMAR_CORE_LIB.oob_dashboard.visual_shell_canonical_panel_contract import (
    build_visual_shell_canonical_panel_contract,
)


@dataclass(frozen=True, slots=True)
class VisualRenderSurfaceEntry:
    """Canonical visual render surface entry."""

    render_surface_id: str
    shell_id: str
    dashboard_id: str
    workspace_id: str
    display_target_id: str
    layout_mode: str
    total_render_panels: int
    canonical_render_panels: int
    hud_mode: str
    renderer_ready: bool
    read_only_render_surface: bool
    interactive_render_surface: bool
    description: str


@dataclass(frozen=True, slots=True)
class VisualRenderSurfaceContract:
    """Canonical visual render surface contract."""

    contract_id: str
    total_entries: int
    renderer_ready_entries: int
    total_render_panels: int
    total_canonical_render_panels: int
    read_only_render_surfaces: int
    interactive_render_surfaces: int
    entries: tuple[VisualRenderSurfaceEntry, ...]


def build_visual_render_surface_contract() -> VisualRenderSurfaceContract:
    """Build canonical visual render surface contract."""
    visual_shell_contract = build_visual_shell_contract()
    canonical_panel_contract = build_visual_shell_canonical_panel_contract()
    layout_contract = build_layout_composition_contract()

    layout_panel_count_by_workspace: dict[str, int] = {}
    for entry in layout_contract.entries:
        layout_panel_count_by_workspace[entry.workspace_id] = (
            layout_panel_count_by_workspace.get(entry.workspace_id, 0) + 1
        )

    entries = tuple(
        VisualRenderSurfaceEntry(
            render_surface_id=f"render_surface_{shell_entry.workspace_id}_001",
            shell_id=shell_entry.shell_id,
            dashboard_id=shell_entry.dashboard_id,
            workspace_id=shell_entry.workspace_id,
            display_target_id=shell_entry.display_target_id,
            layout_mode="hud_grid",
            total_render_panels=layout_panel_count_by_workspace.get(
                shell_entry.workspace_id,
                0,
            ),
            canonical_render_panels=canonical_panel_contract.total_entries,
            hud_mode=shell_entry.visual_mode,
            renderer_ready=(
                shell_entry.renderer_ready
                and canonical_panel_contract.legacy_alias_entries == 0
            ),
            read_only_render_surface=shell_entry.read_only,
            interactive_render_surface=shell_entry.interactive,
            description=(
                f"Canonical visual render surface entry for "
                f"{shell_entry.workspace_id} on "
                f"{shell_entry.display_target_id}."
            ),
        )
        for shell_entry in visual_shell_contract.entries
    )

    return VisualRenderSurfaceContract(
        contract_id="visual_render_surface_contract_001",
        total_entries=len(entries),
        renderer_ready_entries=sum(1 for entry in entries if entry.renderer_ready),
        total_render_panels=sum(entry.total_render_panels for entry in entries),
        total_canonical_render_panels=sum(
            entry.canonical_render_panels for entry in entries
        ),
        read_only_render_surfaces=sum(
            1 for entry in entries if entry.read_only_render_surface
        ),
        interactive_render_surfaces=sum(
            1 for entry in entries if entry.interactive_render_surface
        ),
        entries=entries,
    )
