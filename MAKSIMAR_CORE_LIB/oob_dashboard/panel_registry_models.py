from __future__ import annotations

from dataclasses import dataclass
from typing import Literal

from MAKSIMAR_CORE_LIB.oob_dashboard.panel_id_vocabulary_normalization import (
    CanonicalPanelId,
    PanelFamily,
    PanelKind,
    PanelRole,
)


PanelCategory = Literal[
    "core",
    "diagnostics",
    "interaction",
    "settings",
    "control",
]


@dataclass(frozen=True, slots=True)
class RegisteredPanel:
    """One dashboard panel registered in sidebar/panel registry."""

    panel_id: CanonicalPanelId
    label: str
    category: PanelCategory
    visible_in_sidebar: bool
    panel_family: PanelFamily = "read_only_monitoring"
    panel_kind: PanelKind = "summary"
    panel_role: PanelRole = "read_only_monitoring"


@dataclass(frozen=True, slots=True)
class DashboardPanelRegistryContract:
    """Unified registry of dashboard panels."""

    total_panels: int
    panels: tuple[RegisteredPanel, ...]
    visible_in_sidebar_panels: int = 0
