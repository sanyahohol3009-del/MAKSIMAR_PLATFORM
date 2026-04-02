from __future__ import annotations

from dataclasses import dataclass

from MAKSIMAR_CORE_LIB.oob_dashboard.visual_render_surface_contract import (
    build_visual_render_surface_contract,
)


@dataclass(frozen=True, slots=True)
class VisualRendererEntry:
    """Canonical visual renderer entry."""

    renderer_id: str
    render_surface_id: str
    shell_id: str
    dashboard_id: str
    workspace_id: str
    display_target_id: str
    primary_visual_mode: str
    supported_visual_modes: tuple[str, ...]
    canonical_panel_only: bool
    signal_flow_overlay_enabled: bool
    topology_overlay_enabled: bool
    stalled_path_visibility_enabled: bool
    degraded_visual_fallback: str
    read_only_render_paths: bool
    interactive_render_paths: bool
    renderer_ready: bool
    description: str


@dataclass(frozen=True, slots=True)
class VisualRendererContract:
    """Canonical visual renderer contract."""

    contract_id: str
    total_entries: int
    renderer_ready_entries: int
    canonical_panel_only_entries: int
    signal_flow_overlay_entries: int
    topology_overlay_entries: int
    stalled_path_visibility_entries: int
    interactive_render_entries: int
    read_only_render_entries: int
    entries: tuple[VisualRendererEntry, ...]


def build_visual_renderer_contract() -> VisualRendererContract:
    """Build canonical visual renderer contract."""
    render_surface_contract = build_visual_render_surface_contract()

    entries = tuple(
        VisualRendererEntry(
            renderer_id="visual_renderer_001",
            render_surface_id=surface_entry.render_surface_id,
            shell_id=surface_entry.shell_id,
            dashboard_id=surface_entry.dashboard_id,
            workspace_id=surface_entry.workspace_id,
            display_target_id=surface_entry.display_target_id,
            primary_visual_mode=surface_entry.hud_mode,
            supported_visual_modes=(
                "operator_hud",
                "diagnostics_overlay",
                "topology_overlay",
                "degraded_fallback",
            ),
            canonical_panel_only=True,
            signal_flow_overlay_enabled=True,
            topology_overlay_enabled=True,
            stalled_path_visibility_enabled=True,
            degraded_visual_fallback="safe_minimal_overlay",
            read_only_render_paths=surface_entry.read_only_render_surface,
            interactive_render_paths=surface_entry.interactive_render_surface,
            renderer_ready=(
                surface_entry.renderer_ready
                and surface_entry.canonical_render_panels > 0
                and surface_entry.total_render_panels > 0
            ),
            description=(
                f"Canonical visual renderer entry for "
                f"{surface_entry.render_surface_id} on "
                f"{surface_entry.display_target_id}."
            ),
        )
        for surface_entry in render_surface_contract.entries
    )

    return VisualRendererContract(
        contract_id="visual_renderer_contract_001",
        total_entries=len(entries),
        renderer_ready_entries=sum(1 for entry in entries if entry.renderer_ready),
        canonical_panel_only_entries=sum(
            1 for entry in entries if entry.canonical_panel_only
        ),
        signal_flow_overlay_entries=sum(
            1 for entry in entries if entry.signal_flow_overlay_enabled
        ),
        topology_overlay_entries=sum(
            1 for entry in entries if entry.topology_overlay_enabled
        ),
        stalled_path_visibility_entries=sum(
            1 for entry in entries if entry.stalled_path_visibility_enabled
        ),
        interactive_render_entries=sum(
            1 for entry in entries if entry.interactive_render_paths
        ),
        read_only_render_entries=sum(
            1 for entry in entries if entry.read_only_render_paths
        ),
        entries=entries,
    )
