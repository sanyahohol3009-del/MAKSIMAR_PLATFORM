from __future__ import annotations

from dataclasses import dataclass
from typing import Literal

from MAKSIMAR_CORE_LIB.oob_dashboard.panel_metadata_contract import (
    build_panel_metadata_contract,
)
from MAKSIMAR_CORE_LIB.oob_dashboard.panel_metadata_models import (
    PanelMetadataEntry,
)


ExposureLevel = Literal[
    "oob_only",
    "main_dashboard_visible",
    "shared_visible",
    "hidden_internal",
]

VisibilityPolicy = Literal[
    "read_only_public",
    "restricted_operator",
    "hidden_internal",
]


@dataclass(frozen=True, slots=True)
class PanelExposureEntry:
    """Canonical exposure policy entry for one panel."""

    panel_id: str
    exposure_level: ExposureLevel
    visibility_policy: VisibilityPolicy
    visible_in_oob_dashboard: bool
    visible_in_main_dashboard: bool
    visible_in_navigation: bool
    description: str


@dataclass(frozen=True, slots=True)
class PanelExposurePolicyContract:
    """Canonical exposure/visibility policy contract for panels."""

    total_entries: int
    oob_only_entries: int
    main_dashboard_visible_entries: int
    shared_visible_entries: int
    hidden_internal_entries: int
    entries: tuple[PanelExposureEntry, ...]
    metadata_entries: tuple[PanelMetadataEntry, ...]


def build_panel_exposure_policy_contract() -> PanelExposurePolicyContract:
    """Build canonical panel exposure/visibility policy contract."""
    metadata_contract = build_panel_metadata_contract()
    metadata_entries = metadata_contract.entries

    exposure_map: dict[str, tuple[ExposureLevel, VisibilityPolicy, bool, bool, bool, str]] = {
        "panel_consistency": (
            "shared_visible",
            "read_only_public",
            True,
            True,
            True,
            "Consistency panel is visible in OOB and main dashboard surfaces.",
        ),
        "panel_snapshot": (
            "shared_visible",
            "read_only_public",
            True,
            True,
            True,
            "Snapshot panel is visible in OOB and main dashboard surfaces.",
        ),
        "panel_incident": (
            "shared_visible",
            "read_only_public",
            True,
            True,
            True,
            "Incident panel is visible in OOB and main dashboard surfaces.",
        ),
        "panel_diagnostics": (
            "shared_visible",
            "read_only_public",
            True,
            True,
            True,
            "Diagnostics panel is visible in OOB and main dashboard surfaces.",
        ),
        "panel_chat": (
            "main_dashboard_visible",
            "restricted_operator",
            False,
            True,
            True,
            "Chat panel is restricted to main dashboard operator surfaces.",
        ),
        "panel_settings": (
            "main_dashboard_visible",
            "restricted_operator",
            False,
            True,
            True,
            "Settings panel is restricted to main dashboard operator surfaces.",
        ),
        "panel_gesture_control": (
            "main_dashboard_visible",
            "restricted_operator",
            False,
            True,
            True,
            "Gesture control panel is restricted to main dashboard operator surfaces.",
        ),
        "panel_queue_load": (
            "main_dashboard_visible",
            "read_only_public",
            False,
            True,
            True,
            "Queue/load panel is visible in main dashboard observability surfaces.",
        ),
        "panel_node_topology": (
            "main_dashboard_visible",
            "read_only_public",
            False,
            True,
            True,
            "Node topology panel is visible in main dashboard observability surfaces.",
        ),
        "panel_degraded_mode": (
            "shared_visible",
            "read_only_public",
            True,
            True,
            True,
            "Degraded mode panel is visible in OOB and main dashboard surfaces.",
        ),
        "panel_project_map": (
            "main_dashboard_visible",
            "read_only_public",
            False,
            True,
            True,
            "Project map panel is visible in main dashboard observability surfaces.",
        ),
        "panel_data_flow": (
            "main_dashboard_visible",
            "read_only_public",
            False,
            True,
            True,
            "Data flow panel is visible in main dashboard observability surfaces.",
        ),
        "panel_dependency_map": (
            "main_dashboard_visible",
            "read_only_public",
            False,
            True,
            True,
            "Dependency map panel is visible in main dashboard observability surfaces.",
        ),
        "panel_version_control_dashboard": (
            "main_dashboard_visible",
            "read_only_public",
            False,
            True,
            True,
            "Version control panel is visible in main dashboard observability surfaces.",
        ),
        "panel_foundation_runtime_status_001": (
            "shared_visible",
            "read_only_public",
            True,
            True,
            True,
            "Foundation runtime status panel is visible in both monitoring worlds.",
        ),
        "panel_foundation_guard_status_001": (
            "shared_visible",
            "read_only_public",
            True,
            True,
            True,
            "Foundation guard status panel is visible in both monitoring worlds.",
        ),
        "panel_foundation_core_guard_status_001": (
            "shared_visible",
            "read_only_public",
            True,
            True,
            True,
            "Foundation core guard status panel is visible in both monitoring worlds.",
        ),
        "panel_foundation_kernel_guard_status_001": (
            "shared_visible",
            "read_only_public",
            True,
            True,
            True,
            "Foundation kernel guard status panel is visible in both monitoring worlds.",
        ),
        "panel_navigation": (
            "hidden_internal",
            "hidden_internal",
            False,
            False,
            False,
            "Navigation panel remains internal and is not exposed directly.",
        ),
    }

    entries = tuple(
        PanelExposureEntry(
            panel_id=entry.panel_id,
            exposure_level=exposure_map[entry.panel_id][0],
            visibility_policy=exposure_map[entry.panel_id][1],
            visible_in_oob_dashboard=exposure_map[entry.panel_id][2],
            visible_in_main_dashboard=exposure_map[entry.panel_id][3],
            visible_in_navigation=exposure_map[entry.panel_id][4],
            description=exposure_map[entry.panel_id][5],
        )
        for entry in metadata_entries
    )

    return PanelExposurePolicyContract(
        total_entries=len(entries),
        oob_only_entries=sum(
            1 for entry in entries if entry.exposure_level == "oob_only"
        ),
        main_dashboard_visible_entries=sum(
            1 for entry in entries if entry.exposure_level == "main_dashboard_visible"
        ),
        shared_visible_entries=sum(
            1 for entry in entries if entry.exposure_level == "shared_visible"
        ),
        hidden_internal_entries=sum(
            1 for entry in entries if entry.exposure_level == "hidden_internal"
        ),
        entries=entries,
        metadata_entries=metadata_entries,
    )
