from __future__ import annotations

from dataclasses import dataclass
from typing import Literal


PanelFamily = Literal[
    "foundation_status",
    "read_only_monitoring",
    "diagnostics",
    "interaction",
    "control",
    "execution_observability",
    "navigation",
]

PanelKind = Literal[
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
]

PanelRole = Literal[
    "foundation_read_only",
    "read_only_monitoring",
    "diagnostics_surface",
    "interaction_surface",
    "control_surface",
    "execution_surface",
    "navigation_surface",
]


CanonicalPanelId = Literal[
    "panel_consistency",
    "panel_snapshot",
    "panel_incident",
    "panel_diagnostics",
    "panel_chat",
    "panel_settings",
    "panel_gesture_control",
    "panel_queue_load",
    "panel_node_topology",
    "panel_degraded_mode",
    "panel_project_map",
    "panel_data_flow",
    "panel_dependency_map",
    "panel_version_control_dashboard",
    "panel_foundation_runtime_status_001",
    "panel_foundation_guard_status_001",
    "panel_foundation_core_guard_status_001",
    "panel_foundation_kernel_guard_status_001",
    "panel_navigation",
]


@dataclass(frozen=True, slots=True)
class PanelVocabularyEntry:
    """Canonical normalized panel vocabulary entry."""

    canonical_panel_id: CanonicalPanelId
    panel_family: PanelFamily
    panel_kind: PanelKind
    panel_role: PanelRole
    display_title: str
    description: str


@dataclass(frozen=True, slots=True)
class PanelIdAliasEntry:
    """Alias entry mapping legacy or drifted ids to canonical panel ids."""

    alias_panel_id: str
    canonical_panel_id: CanonicalPanelId
    reason: str


@dataclass(frozen=True, slots=True)
class PanelIdVocabularyNormalizationModel:
    """Canonical normalized panel-id vocabulary model."""

    total_entries: int
    foundation_status_entries: int
    read_only_monitoring_entries: int
    diagnostics_entries: int
    interaction_entries: int
    control_entries: int
    execution_observability_entries: int
    navigation_entries: int
    total_aliases: int
    entries: tuple[PanelVocabularyEntry, ...]
    aliases: tuple[PanelIdAliasEntry, ...]


def build_panel_id_vocabulary_normalization_model() -> (
    PanelIdVocabularyNormalizationModel
):
    """Build canonical normalized panel-id vocabulary model."""
    entries = (
        PanelVocabularyEntry(
            canonical_panel_id="panel_consistency",
            panel_family="read_only_monitoring",
            panel_kind="summary",
            panel_role="read_only_monitoring",
            display_title="Consistency",
            description="Canonical read-only consistency monitoring panel.",
        ),
        PanelVocabularyEntry(
            canonical_panel_id="panel_snapshot",
            panel_family="read_only_monitoring",
            panel_kind="status",
            panel_role="read_only_monitoring",
            display_title="Snapshot",
            description="Canonical runtime snapshot monitoring panel.",
        ),
        PanelVocabularyEntry(
            canonical_panel_id="panel_incident",
            panel_family="diagnostics",
            panel_kind="incident",
            panel_role="diagnostics_surface",
            display_title="Incident",
            description="Canonical incident localization and inspection panel.",
        ),
        PanelVocabularyEntry(
            canonical_panel_id="panel_diagnostics",
            panel_family="diagnostics",
            panel_kind="diagnostics",
            panel_role="diagnostics_surface",
            display_title="Diagnostics",
            description="Canonical diagnostics and correlation panel.",
        ),
        PanelVocabularyEntry(
            canonical_panel_id="panel_chat",
            panel_family="interaction",
            panel_kind="chat",
            panel_role="interaction_surface",
            display_title="Chat",
            description="Canonical operator chat interaction panel.",
        ),
        PanelVocabularyEntry(
            canonical_panel_id="panel_settings",
            panel_family="interaction",
            panel_kind="settings",
            panel_role="interaction_surface",
            display_title="Settings",
            description="Canonical dashboard settings panel.",
        ),
        PanelVocabularyEntry(
            canonical_panel_id="panel_gesture_control",
            panel_family="control",
            panel_kind="gesture",
            panel_role="control_surface",
            display_title="Gesture Control",
            description="Canonical gesture control panel.",
        ),
        PanelVocabularyEntry(
            canonical_panel_id="panel_queue_load",
            panel_family="execution_observability",
            panel_kind="queue",
            panel_role="execution_surface",
            display_title="Queue & Load",
            description="Canonical execution queue and load panel.",
        ),
        PanelVocabularyEntry(
            canonical_panel_id="panel_node_topology",
            panel_family="execution_observability",
            panel_kind="topology",
            panel_role="execution_surface",
            display_title="Node Topology",
            description="Canonical node topology panel.",
        ),
        PanelVocabularyEntry(
            canonical_panel_id="panel_degraded_mode",
            panel_family="execution_observability",
            panel_kind="mode",
            panel_role="execution_surface",
            display_title="Degraded Mode",
            description="Canonical degraded mode panel.",
        ),
        PanelVocabularyEntry(
            canonical_panel_id="panel_project_map",
            panel_family="execution_observability",
            panel_kind="map",
            panel_role="execution_surface",
            display_title="Project Map",
            description="Canonical project map panel.",
        ),
        PanelVocabularyEntry(
            canonical_panel_id="panel_data_flow",
            panel_family="execution_observability",
            panel_kind="flow",
            panel_role="execution_surface",
            display_title="Data Flow",
            description="Canonical data flow panel.",
        ),
        PanelVocabularyEntry(
            canonical_panel_id="panel_dependency_map",
            panel_family="execution_observability",
            panel_kind="map",
            panel_role="execution_surface",
            display_title="Dependency Map",
            description="Canonical dependency map panel.",
        ),
        PanelVocabularyEntry(
            canonical_panel_id="panel_version_control_dashboard",
            panel_family="execution_observability",
            panel_kind="version_control",
            panel_role="execution_surface",
            display_title="Version Control",
            description="Canonical version control dashboard panel.",
        ),
        PanelVocabularyEntry(
            canonical_panel_id="panel_foundation_runtime_status_001",
            panel_family="foundation_status",
            panel_kind="status",
            panel_role="foundation_read_only",
            display_title="Runtime Core",
            description="Canonical foundation runtime status panel instance.",
        ),
        PanelVocabularyEntry(
            canonical_panel_id="panel_foundation_guard_status_001",
            panel_family="foundation_status",
            panel_kind="status",
            panel_role="foundation_read_only",
            display_title="Stop-Gate Watcher",
            description="Canonical foundation stop-gate watcher status panel instance.",
        ),
        PanelVocabularyEntry(
            canonical_panel_id="panel_foundation_core_guard_status_001",
            panel_family="foundation_status",
            panel_kind="status",
            panel_role="foundation_read_only",
            display_title="Core Guard",
            description="Canonical foundation core guard status panel instance.",
        ),
        PanelVocabularyEntry(
            canonical_panel_id="panel_foundation_kernel_guard_status_001",
            panel_family="foundation_status",
            panel_kind="status",
            panel_role="foundation_read_only",
            display_title="Kernel Watchdog",
            description="Canonical foundation kernel watchdog status panel instance.",
        ),
        PanelVocabularyEntry(
            canonical_panel_id="panel_navigation",
            panel_family="navigation",
            panel_kind="navigation",
            panel_role="navigation_surface",
            display_title="Navigation",
            description="Canonical dashboard navigation panel.",
        ),
    )

    aliases = (
        PanelIdAliasEntry(
            alias_panel_id="dashboard_consistency_panel",
            canonical_panel_id="panel_consistency",
            reason="Legacy consistency panel id must normalize to registry id.",
        ),
        PanelIdAliasEntry(
            alias_panel_id="panel_gesture",
            canonical_panel_id="panel_gesture_control",
            reason="Navigation placement alias must normalize to gesture control id.",
        ),
    )

    return PanelIdVocabularyNormalizationModel(
        total_entries=len(entries),
        foundation_status_entries=sum(
            1 for entry in entries if entry.panel_family == "foundation_status"
        ),
        read_only_monitoring_entries=sum(
            1 for entry in entries if entry.panel_family == "read_only_monitoring"
        ),
        diagnostics_entries=sum(
            1 for entry in entries if entry.panel_family == "diagnostics"
        ),
        interaction_entries=sum(
            1 for entry in entries if entry.panel_family == "interaction"
        ),
        control_entries=sum(
            1 for entry in entries if entry.panel_family == "control"
        ),
        execution_observability_entries=sum(
            1 for entry in entries if entry.panel_family == "execution_observability"
        ),
        navigation_entries=sum(
            1 for entry in entries if entry.panel_family == "navigation"
        ),
        total_aliases=len(aliases),
        entries=entries,
        aliases=aliases,
    )


def normalize_panel_id(panel_id: str) -> str:
    """Normalize panel id through canonical alias mapping."""
    model = build_panel_id_vocabulary_normalization_model()

    for alias in model.aliases:
        if alias.alias_panel_id == panel_id:
            return alias.canonical_panel_id

    return panel_id


def is_canonical_panel_id(panel_id: str) -> bool:
    """Return True when panel id is already canonical."""
    model = build_panel_id_vocabulary_normalization_model()
    return any(entry.canonical_panel_id == panel_id for entry in model.entries)
