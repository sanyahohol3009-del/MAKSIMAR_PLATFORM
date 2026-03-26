from __future__ import annotations

import re
from dataclasses import dataclass
from typing import Literal

from MAKSIMAR_SERVER.MEMORY_REGISTRY import (
    build_memory_registry_contract,
)
from MAKSIMAR_SERVER.REGISTRY_AUTO_ENROLLMENT import (
    build_registry_auto_enrollment_contract,
)
from MAKSIMAR_SERVER.SKILL_ADAPTER_REGISTRY import (
    build_skill_adapter_registry_contract,
)


DisplayTargetRole = Literal[
    "primary_dashboard_display",
    "monitoring_display",
    "engineering_display",
    "presentation_display",
    "mobile_display_proxy",
    "simulation_display",
    "wall_display",
    "wrist_projection_zone",
    "ar_glasses_display",
]

DisplayCapability = Literal[
    "render_panels",
    "render_explanations",
    "multi_window",
    "spatial_overlay",
    "mobile_proxy",
    "private_display",
    "wall_projection",
    "gesture_input",
]

DisplayVisibilityMode = Literal[
    "private",
    "shared",
]

DisplayAvailabilityStatus = Literal[
    "active",
]


DISPLAY_ID_PATTERN = re.compile(r"^display_[a-z][a-z0-9_]*$")
ZONE_ID_PATTERN = re.compile(r"^zone_[a-z][a-z0-9_]*$")
PANEL_ID_PATTERN = re.compile(r"^panel_[a-z][a-z0-9_]*$")


def _validate_unique_non_empty_str_tuple(
    *,
    values: tuple[str, ...],
    field_name: str,
    owner_id: str,
) -> None:
    """Validate tuple items are non-empty and unique."""
    if len(set(values)) != len(values):
        raise ValueError(f"Duplicate values in {field_name} for {owner_id}")

    for value in values:
        if not value.strip():
            raise ValueError(f"{field_name} contains empty value for {owner_id}")


@dataclass(frozen=True, slots=True)
class DisplayTopologyEntry:
    """Canonical display topology entry."""

    display_id: str
    display_role: DisplayTargetRole
    zone_ids: tuple[str, ...]
    default_panel_ids: tuple[str, ...]
    capabilities: tuple[DisplayCapability, ...]
    visibility_mode: DisplayVisibilityMode
    supports_multilingual_rendering: bool
    supports_explainable_views: bool
    supports_registry_routing: bool
    availability_status: DisplayAvailabilityStatus
    description: str

    def __post_init__(self) -> None:
        """Validate display topology invariants."""
        if not DISPLAY_ID_PATTERN.fullmatch(self.display_id):
            raise ValueError(f"Invalid display_id: {self.display_id}")

        if not self.description.strip():
            raise ValueError(f"description must not be empty for {self.display_id}")

        if not self.zone_ids:
            raise ValueError(f"zone_ids must not be empty for {self.display_id}")

        if not self.default_panel_ids:
            raise ValueError(
                f"default_panel_ids must not be empty for {self.display_id}"
            )

        if not self.capabilities:
            raise ValueError(f"capabilities must not be empty for {self.display_id}")

        _validate_unique_non_empty_str_tuple(
            values=self.zone_ids,
            field_name="zone_ids",
            owner_id=self.display_id,
        )
        _validate_unique_non_empty_str_tuple(
            values=self.default_panel_ids,
            field_name="default_panel_ids",
            owner_id=self.display_id,
        )

        if len(set(self.capabilities)) != len(self.capabilities):
            raise ValueError(f"Duplicate capabilities detected for {self.display_id}")

        for zone_id in self.zone_ids:
            if not ZONE_ID_PATTERN.fullmatch(zone_id):
                raise ValueError(f"Invalid zone_id: {zone_id}")

        for panel_id in self.default_panel_ids:
            if not PANEL_ID_PATTERN.fullmatch(panel_id):
                raise ValueError(f"Invalid panel_id: {panel_id}")

        if not self.supports_multilingual_rendering:
            raise ValueError(
                f"display must support multilingual rendering: {self.display_id}"
            )

        if not self.supports_explainable_views:
            raise ValueError(
                f"display must support explainable views: {self.display_id}"
            )

        if not self.supports_registry_routing:
            raise ValueError(
                f"display must support registry routing: {self.display_id}"
            )

        if self.availability_status != "active":
            raise ValueError(f"display must be active: {self.display_id}")

        if self.display_role == "primary_dashboard_display":
            if "multi_window" not in self.capabilities:
                raise ValueError(
                    f"primary_dashboard_display must support multi_window: {self.display_id}"
                )

        if self.display_role == "engineering_display":
            if "spatial_overlay" not in self.capabilities:
                raise ValueError(
                    f"engineering_display must support spatial_overlay: {self.display_id}"
                )

        if self.display_role == "mobile_display_proxy":
            if self.visibility_mode != "private":
                raise ValueError(
                    f"mobile_display_proxy must be private: {self.display_id}"
                )
            if "mobile_proxy" not in self.capabilities:
                raise ValueError(
                    f"mobile_display_proxy must expose mobile_proxy capability: {self.display_id}"
                )
            if "private_display" not in self.capabilities:
                raise ValueError(
                    f"mobile_display_proxy must expose private_display capability: {self.display_id}"
                )


@dataclass(frozen=True, slots=True)
class DisplayTopologyContract:
    """Unified display topology contract."""

    total_displays: int
    private_displays: int
    shared_displays: int
    multilingual_ready_displays: int
    entries: tuple[DisplayTopologyEntry, ...]

    def __post_init__(self) -> None:
        """Validate display topology contract invariants."""
        if self.total_displays != len(self.entries):
            raise ValueError("total_displays must match entries length")

        private_displays = sum(
            1 for entry in self.entries if entry.visibility_mode == "private"
        )
        shared_displays = sum(
            1 for entry in self.entries if entry.visibility_mode == "shared"
        )
        multilingual_ready_displays = sum(
            1 for entry in self.entries if entry.supports_multilingual_rendering
        )

        if self.private_displays != private_displays:
            raise ValueError("private_displays must match computed count")

        if self.shared_displays != shared_displays:
            raise ValueError("shared_displays must match computed count")

        if self.multilingual_ready_displays != multilingual_ready_displays:
            raise ValueError(
                "multilingual_ready_displays must match computed count"
            )

        display_ids = tuple(entry.display_id for entry in self.entries)
        display_roles = tuple(entry.display_role for entry in self.entries)

        if len(set(display_ids)) != len(display_ids):
            raise ValueError("Duplicate display_id values detected")

        if len(set(display_roles)) != len(display_roles):
            raise ValueError("Duplicate display_role values detected")


def build_display_topology_contract() -> DisplayTopologyContract:
    """Build canonical display topology contract."""
    memory_registry = build_memory_registry_contract()
    skill_registry = build_skill_adapter_registry_contract()
    auto_enrollment = build_registry_auto_enrollment_contract()

    memory_panel_id = memory_registry.entries[0].panel_ids[0]
    skill_panel_id = skill_registry.entries[0].panel_ids[0]

    monitoring_entries = [
        entry
        for entry in auto_enrollment.entries
        if entry.module_slug == "monitoring_panel"
    ]
    if len(monitoring_entries) != 1:
        raise ValueError("Expected exactly one monitoring_panel registry entry")

    monitoring_panel_id = monitoring_entries[0].panel_ids[0]

    entries = (
        DisplayTopologyEntry(
            display_id="display_primary_dashboard_001",
            display_role="primary_dashboard_display",
            zone_ids=(
                "zone_dashboard_main",
                "zone_dashboard_sidebar",
                "zone_dashboard_explanation",
            ),
            default_panel_ids=(
                monitoring_panel_id,
                memory_panel_id,
            ),
            capabilities=(
                "render_panels",
                "render_explanations",
                "multi_window",
            ),
            visibility_mode="shared",
            supports_multilingual_rendering=True,
            supports_explainable_views=True,
            supports_registry_routing=True,
            availability_status="active",
            description=(
                "Primary dashboard display for registry-backed monitoring and memory views."
            ),
        ),
        DisplayTopologyEntry(
            display_id="display_engineering_001",
            display_role="engineering_display",
            zone_ids=(
                "zone_engineering_main",
                "zone_engineering_sidebar",
                "zone_engineering_explanation",
            ),
            default_panel_ids=(
                skill_panel_id,
            ),
            capabilities=(
                "render_panels",
                "render_explanations",
                "multi_window",
                "spatial_overlay",
            ),
            visibility_mode="shared",
            supports_multilingual_rendering=True,
            supports_explainable_views=True,
            supports_registry_routing=True,
            availability_status="active",
            description=(
                "Engineering display for simulation skill panels and explainable overlays."
            ),
        ),
        DisplayTopologyEntry(
            display_id="display_mobile_proxy_001",
            display_role="mobile_display_proxy",
            zone_ids=(
                "zone_mobile_main",
                "zone_mobile_overlay",
            ),
            default_panel_ids=(
                memory_panel_id,
            ),
            capabilities=(
                "render_panels",
                "render_explanations",
                "mobile_proxy",
                "private_display",
            ),
            visibility_mode="private",
            supports_multilingual_rendering=True,
            supports_explainable_views=True,
            supports_registry_routing=True,
            availability_status="active",
            description=(
                "Private mobile proxy display for registry-backed memory views."
            ),
        ),
    )

    private_displays = sum(
        1 for entry in entries if entry.visibility_mode == "private"
    )
    shared_displays = sum(
        1 for entry in entries if entry.visibility_mode == "shared"
    )
    multilingual_ready_displays = sum(
        1 for entry in entries if entry.supports_multilingual_rendering
    )

    return DisplayTopologyContract(
        total_displays=len(entries),
        private_displays=private_displays,
        shared_displays=shared_displays,
        multilingual_ready_displays=multilingual_ready_displays,
        entries=entries,
    )
