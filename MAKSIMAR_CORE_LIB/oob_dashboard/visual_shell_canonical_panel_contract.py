from __future__ import annotations

from dataclasses import dataclass
from typing import Tuple


@dataclass(frozen=True)
class VisualShellCanonicalPanelEntry:
    """Canonical visual-shell panel entry used before renderer composition."""

    panel_id: str
    canonical_panel_kind: str
    panel_semantics: str
    renderer_semantics_leakage_allowed: bool
    read_only: bool
    operator_visible: bool
    description: str


@dataclass(frozen=True)
class VisualShellCanonicalPanelContract:
    """Canonical visual-shell panel contract."""

    contract_id: str
    total_entries: int
    read_only_entries: int
    operator_visible_entries: int
    no_renderer_leakage_entries: int
    entries: Tuple[VisualShellCanonicalPanelEntry, ...]
    operator_visible: bool
    description: str


def build_visual_shell_canonical_panel_contract() -> VisualShellCanonicalPanelContract:
    """Build canonical visual-shell panel contract."""
    entries = (
        VisualShellCanonicalPanelEntry(
            panel_id="panel_foundation_runtime_status_001",
            canonical_panel_kind="foundation_runtime_status",
            panel_semantics="runtime_truth_surface",
            renderer_semantics_leakage_allowed=False,
            read_only=True,
            operator_visible=True,
            description="Canonical visual-shell panel entry for runtime foundation status.",
        ),
        VisualShellCanonicalPanelEntry(
            panel_id="panel_navigation",
            canonical_panel_kind="navigation_surface",
            panel_semantics="operator_navigation_surface",
            renderer_semantics_leakage_allowed=False,
            read_only=True,
            operator_visible=True,
            description="Canonical visual-shell panel entry for navigation surface.",
        ),
        VisualShellCanonicalPanelEntry(
            panel_id="panel_consistency",
            canonical_panel_kind="consistency_surface",
            panel_semantics="diagnostic_consistency_surface",
            renderer_semantics_leakage_allowed=False,
            read_only=True,
            operator_visible=True,
            description="Canonical visual-shell panel entry for consistency surface.",
        ),
    )

    return VisualShellCanonicalPanelContract(
        contract_id="visual_shell_canonical_panel_contract_001",
        total_entries=len(entries),
        read_only_entries=sum(1 for entry in entries if entry.read_only),
        operator_visible_entries=sum(1 for entry in entries if entry.operator_visible),
        no_renderer_leakage_entries=sum(
            1 for entry in entries if entry.renderer_semantics_leakage_allowed is False
        ),
        entries=entries,
        operator_visible=True,
        description="Canonical visual-shell panel contract used to prevent semantic leakage into renderer.",
    )
