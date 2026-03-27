from __future__ import annotations

from dataclasses import dataclass
from typing import Literal

from MAKSIMAR_CORE_LIB.oob_dashboard.panel_id_vocabulary_normalization import (
    CanonicalPanelId,
    PanelFamily,
    PanelKind,
    PanelRole,
)


ReadMode = Literal[
    "read_only",
    "interactive_controlled",
    "interactive_restricted",
    "hidden_internal",
]

SourceDomain = Literal[
    "foundation",
    "diagnostics",
    "interaction",
    "control",
    "execution_observability",
    "navigation",
]

PanelStateClass = Literal[
    "foundation",
    "diagnostics",
    "operator",
    "topology",
    "module_surface",
    "admin",
    "client_surface",
]


@dataclass(frozen=True, slots=True)
class PanelMetadataEntry:
    """Canonical panel metadata entry."""

    panel_id: CanonicalPanelId
    display_title: str
    description: str
    priority: int
    source_domain: SourceDomain
    read_mode: ReadMode
    panel_state_class: PanelStateClass
    panel_family: PanelFamily
    panel_kind: PanelKind
    panel_role: PanelRole


@dataclass(frozen=True, slots=True)
class PanelMetadataContract:
    """Canonical panel metadata contract."""

    total_entries: int
    read_only_entries: int
    interactive_controlled_entries: int
    interactive_restricted_entries: int
    hidden_internal_entries: int
    entries: tuple[PanelMetadataEntry, ...]
