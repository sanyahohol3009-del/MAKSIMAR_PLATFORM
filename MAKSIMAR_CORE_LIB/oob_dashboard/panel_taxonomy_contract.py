from __future__ import annotations

from dataclasses import dataclass

from MAKSIMAR_CORE_LIB.oob_dashboard.panel_metadata_contract import (
    build_panel_metadata_contract,
)
from MAKSIMAR_CORE_LIB.oob_dashboard.panel_metadata_models import (
    PanelMetadataEntry,
)
from MAKSIMAR_CORE_LIB.oob_dashboard.panel_id_vocabulary_normalization import (
    PanelFamily,
    PanelKind,
    PanelRole,
)


@dataclass(frozen=True, slots=True)
class PanelFamilySummary:
    """Normalized summary for one canonical panel family."""

    panel_family: PanelFamily
    total_entries: int


@dataclass(frozen=True, slots=True)
class PanelKindSummary:
    """Normalized summary for one canonical panel kind."""

    panel_kind: PanelKind
    total_entries: int


@dataclass(frozen=True, slots=True)
class PanelRoleSummary:
    """Normalized summary for one canonical panel role."""

    panel_role: PanelRole
    total_entries: int


@dataclass(frozen=True, slots=True)
class PanelTaxonomyContract:
    """Canonical taxonomy contract for panel family/kind/role."""

    total_entries: int
    unique_families: int
    unique_kinds: int
    unique_roles: int
    family_summaries: tuple[PanelFamilySummary, ...]
    kind_summaries: tuple[PanelKindSummary, ...]
    role_summaries: tuple[PanelRoleSummary, ...]
    entries: tuple[PanelMetadataEntry, ...]


def build_panel_taxonomy_contract() -> PanelTaxonomyContract:
    """Build canonical taxonomy contract for normalized panels."""
    metadata_contract = build_panel_metadata_contract()
    entries = metadata_contract.entries

    family_order: tuple[PanelFamily, ...] = (
        "foundation_status",
        "read_only_monitoring",
        "diagnostics",
        "interaction",
        "control",
        "execution_observability",
        "navigation",
    )
    kind_order: tuple[PanelKind, ...] = (
        "status",
        "summary",
        "incident",
        "diagnostics",
        "chat",
        "settings",
        "gesture",
        "queue",
        "topology",
        "mode",
        "map",
        "flow",
        "version_control",
        "navigation",
    )
    role_order: tuple[PanelRole, ...] = (
        "foundation_read_only",
        "read_only_monitoring",
        "diagnostics_surface",
        "interaction_surface",
        "control_surface",
        "execution_surface",
        "navigation_surface",
    )

    family_summaries = tuple(
        PanelFamilySummary(
            panel_family=panel_family,
            total_entries=sum(
                1 for entry in entries if entry.panel_family == panel_family
            ),
        )
        for panel_family in family_order
        if any(entry.panel_family == panel_family for entry in entries)
    )

    kind_summaries = tuple(
        PanelKindSummary(
            panel_kind=panel_kind,
            total_entries=sum(1 for entry in entries if entry.panel_kind == panel_kind),
        )
        for panel_kind in kind_order
        if any(entry.panel_kind == panel_kind for entry in entries)
    )

    role_summaries = tuple(
        PanelRoleSummary(
            panel_role=panel_role,
            total_entries=sum(1 for entry in entries if entry.panel_role == panel_role),
        )
        for panel_role in role_order
        if any(entry.panel_role == panel_role for entry in entries)
    )

    return PanelTaxonomyContract(
        total_entries=len(entries),
        unique_families=len(family_summaries),
        unique_kinds=len(kind_summaries),
        unique_roles=len(role_summaries),
        family_summaries=family_summaries,
        kind_summaries=kind_summaries,
        role_summaries=role_summaries,
        entries=entries,
    )
