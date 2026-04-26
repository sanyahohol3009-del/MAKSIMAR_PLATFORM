from __future__ import annotations

from dataclasses import dataclass

from MAKSIMAR_CORE_LIB.oob_dashboard.panel_exposure_policy_contract import (
    build_panel_exposure_policy_contract,
)
from MAKSIMAR_CORE_LIB.oob_dashboard.panel_metadata_contract import (
    build_panel_metadata_contract,
)


@dataclass(frozen=True, slots=True)
class PanelVisibilityPolicyEntry:
    """Canonical visibility-policy entry for a panel."""

    panel_id: str
    visibility_policy: str
    operator_visible: bool
    visible_in_navigation: bool
    visible_in_oob_dashboard: bool
    visible_in_main_dashboard: bool
    description: str

    def __post_init__(self) -> None:
        """Validate visibility-policy entry invariants."""
        if not self.panel_id.strip():
            raise ValueError("panel_id must not be empty")
        if not self.visibility_policy.strip():
            raise ValueError("visibility_policy must not be empty")
        if not self.description.strip():
            raise ValueError("description must not be empty")


@dataclass(frozen=True, slots=True)
class PanelVisibilityPolicyContract:
    """Canonical ordered visibility-policy contract."""

    entries: tuple[PanelVisibilityPolicyEntry, ...]

    def __post_init__(self) -> None:
        """Validate contract invariants."""
        if not self.entries:
            raise ValueError("entries must not be empty")

        seen_ids: set[str] = set()
        for entry in self.entries:
            if entry.panel_id in seen_ids:
                raise ValueError(f"duplicate panel_id detected: {entry.panel_id}")
            seen_ids.add(entry.panel_id)


def build_panel_visibility_policy_contract() -> PanelVisibilityPolicyContract:
    """Build the canonical panel visibility policy contract."""
    metadata_contract = build_panel_metadata_contract()
    exposure_contract = build_panel_exposure_policy_contract()

    exposure_map = {entry.panel_id: entry for entry in exposure_contract.entries}

    entries = tuple(
        PanelVisibilityPolicyEntry(
            panel_id=entry.panel_id,
            visibility_policy=exposure_map[entry.panel_id].visibility_policy,
            operator_visible=entry.operator_visible,
            visible_in_navigation=exposure_map[entry.panel_id].visible_in_navigation,
            visible_in_oob_dashboard=exposure_map[entry.panel_id].visible_in_oob_dashboard,
            visible_in_main_dashboard=exposure_map[entry.panel_id].visible_in_main_dashboard,
            description=(
                f"Canonical visibility policy for {entry.title}: "
                f"{exposure_map[entry.panel_id].description}"
            ),
        )
        for entry in metadata_contract.entries
    )

    return PanelVisibilityPolicyContract(entries=entries)
