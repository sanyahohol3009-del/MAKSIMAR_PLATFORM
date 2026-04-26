from __future__ import annotations

from dataclasses import dataclass
from typing import Tuple


def _require_non_empty(value: str, field_name: str) -> None:
    if not value or not value.strip():
        raise ValueError(f"{field_name} must be a non-empty string.")


@dataclass(frozen=True, slots=True)
class AvatarStatePanelEntry:
    avatar_profile_id: str
    persona_mode: str
    consent_state: str
    operator_visible: bool
    description: str

    def __post_init__(self) -> None:
        _require_non_empty(self.avatar_profile_id, "avatar_profile_id")
        _require_non_empty(self.persona_mode, "persona_mode")
        _require_non_empty(self.consent_state, "consent_state")
        _require_non_empty(self.description, "description")

        if not self.operator_visible:
            raise ValueError(
                "operator_visible must remain true for canonical avatar-state panel entries."
            )


@dataclass(frozen=True, slots=True)
class AvatarStatePanelContract:
    panel_id: str
    total_entries: int
    operator_visible_entries: int
    entries: Tuple[AvatarStatePanelEntry, ...]
    operator_visible: bool
    description: str

    def __post_init__(self) -> None:
        _require_non_empty(self.panel_id, "panel_id")
        _require_non_empty(self.description, "description")

        if self.total_entries != len(self.entries):
            raise ValueError("total_entries must match len(entries).")
        if self.operator_visible_entries != sum(
            1 for entry in self.entries if entry.operator_visible
        ):
            raise ValueError(
                "operator_visible_entries must match operator_visible count."
            )
        if not self.operator_visible:
            raise ValueError(
                "operator_visible must remain true for canonical avatar-state panel contract."
            )


def build_avatar_state_panel_contract() -> AvatarStatePanelContract:
    entries = (
        AvatarStatePanelEntry(
            avatar_profile_id="avatar_profile_family_default",
            persona_mode="family_safe_persona",
            consent_state="consent_required",
            operator_visible=True,
            description="Canonical family-safe avatar persona state.",
        ),
        AvatarStatePanelEntry(
            avatar_profile_id="avatar_profile_operator_assist",
            persona_mode="operator_assist_persona",
            consent_state="consent_confirmed",
            operator_visible=True,
            description="Canonical operator-assist avatar persona state.",
        ),
        AvatarStatePanelEntry(
            avatar_profile_id="avatar_profile_child_guarded",
            persona_mode="child_guarded_persona",
            consent_state="guardian_consent_confirmed",
            operator_visible=True,
            description="Canonical child-guarded avatar persona state.",
        ),
    )

    return AvatarStatePanelContract(
        panel_id="panel_avatar_state",
        total_entries=len(entries),
        operator_visible_entries=sum(1 for entry in entries if entry.operator_visible),
        entries=entries,
        operator_visible=True,
        description="Canonical avatar-state panel contract.",
    )
