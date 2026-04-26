from __future__ import annotations

from dataclasses import dataclass


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
        if not self.entries:
            raise ValueError("entries must not be empty")

        seen_ids: set[str] = set()
        for entry in self.entries:
            if entry.panel_id in seen_ids:
                raise ValueError(f"duplicate panel_id detected: {entry.panel_id}")
            seen_ids.add(entry.panel_id)
