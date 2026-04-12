from __future__ import annotations

from dataclasses import dataclass
from typing import Tuple


@dataclass(frozen=True)
class DegradedModePanelEntry:
    """Canonical degraded mode panel entry."""

    disabled_feature: str
    degradation_status: str
    fallback_mode: str
    safety_critical: bool
    remains_active: bool
    operator_visible: bool
    description: str


@dataclass(frozen=True)
class DegradedModePanelContract:
    """Canonical degraded mode panel contract."""

    panel_id: str
    total_entries: int
    entries: Tuple[DegradedModePanelEntry, ...]
    operator_visible: bool
    description: str


def build_degraded_mode_panel_contract() -> DegradedModePanelContract:
    """Build canonical degraded mode panel contract."""
    entries = (
        DegradedModePanelEntry(
            disabled_feature="heavy_simulation",
            degradation_status="disabled_in_degraded_mode",
            fallback_mode="deferred_execution",
            safety_critical=False,
            remains_active=False,
            operator_visible=True,
            description="Heavy simulation is deferred under degraded mode.",
        ),
        DegradedModePanelEntry(
            disabled_feature="chat_and_safety",
            degradation_status="kept_active",
            fallback_mode="read_only_and_guarded",
            safety_critical=True,
            remains_active=True,
            operator_visible=True,
            description="Chat and safety remain active under degraded mode.",
        ),
        DegradedModePanelEntry(
            disabled_feature="background_analytics",
            degradation_status="disabled_in_degraded_mode",
            fallback_mode="minimal_metrics",
            safety_critical=False,
            remains_active=False,
            operator_visible=True,
            description="Background analytics are minimized under degraded mode.",
        ),
        DegradedModePanelEntry(
            disabled_feature="premium_visualization",
            degradation_status="disabled_in_degraded_mode",
            fallback_mode="minimal_operator_surface",
            safety_critical=False,
            remains_active=False,
            operator_visible=True,
            description="Premium visualization is disabled under degraded mode.",
        ),
    )

    return DegradedModePanelContract(
        panel_id="panel_degraded_mode",
        total_entries=len(entries),
        entries=entries,
        operator_visible=True,
        description="Canonical degraded mode panel contract.",
    )
