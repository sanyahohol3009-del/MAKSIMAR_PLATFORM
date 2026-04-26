from __future__ import annotations

from dataclasses import dataclass

from MAKSIMAR_CORE_LIB.oob_dashboard.panel_metadata_contract import (
    build_panel_metadata_contract,
)


@dataclass(frozen=True, slots=True)
class PanelExposureEntry:
    """Canonical exposure policy entry for a panel."""

    panel_id: str
    exposure_level: str
    visibility_policy: str
    visible_in_oob_dashboard: bool
    visible_in_main_dashboard: bool
    visible_in_navigation: bool
    description: str

    def __post_init__(self) -> None:
        """Validate exposure entry invariants."""
        if not self.panel_id.strip():
            raise ValueError("panel_id must not be empty")
        if not self.exposure_level.strip():
            raise ValueError("exposure_level must not be empty")
        if not self.visibility_policy.strip():
            raise ValueError("visibility_policy must not be empty")
        if not self.description.strip():
            raise ValueError("description must not be empty")


@dataclass(frozen=True, slots=True)
class PanelExposurePolicyContract:
    """Canonical exposure policy contract."""

    entries: tuple[PanelExposureEntry, ...]

    def __post_init__(self) -> None:
        """Validate contract invariants."""
        if not self.entries:
            raise ValueError("entries must not be empty")

        seen_ids: set[str] = set()
        for entry in self.entries:
            if entry.panel_id in seen_ids:
                raise ValueError(f"duplicate panel_id detected: {entry.panel_id}")
            seen_ids.add(entry.panel_id)


def build_panel_exposure_policy_contract() -> PanelExposurePolicyContract:
    """Build the canonical panel exposure policy contract."""
    metadata_contract = build_panel_metadata_contract()

    exposure_map: dict[str, tuple[str, str, bool, bool, bool, str]] = {
        "system_status": (
            "operator_visible",
            "always_visible",
            True,
            True,
            True,
            "System status is always visible to the operator.",
        ),
        "guard_chain": (
            "operator_visible",
            "always_visible",
            True,
            True,
            True,
            "Guard chain visibility is always available to the operator.",
        ),
        "incidents": (
            "operator_visible",
            "always_visible",
            True,
            True,
            True,
            "Incident visibility is always available to the operator.",
        ),
        "logs": (
            "operator_visible",
            "always_visible",
            True,
            True,
            True,
            "Logs visibility is always available to the operator.",
        ),
        "topology": (
            "operator_visible",
            "always_visible",
            True,
            True,
            True,
            "Topology visibility is always available to the operator.",
        ),
        "action_queue": (
            "operator_visible",
            "policy_visible",
            True,
            True,
            True,
            "Action queue is visible through the operator interaction path.",
        ),
        "approval_queue": (
            "operator_visible",
            "policy_visible",
            True,
            True,
            True,
            "Approval queue is visible through the operator interaction path.",
        ),
        "audit_timeline": (
            "operator_visible",
            "policy_visible",
            True,
            True,
            True,
            "Audit timeline is visible through the operator interaction path.",
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
        for entry in metadata_contract.entries
    )

    return PanelExposurePolicyContract(entries=entries)
