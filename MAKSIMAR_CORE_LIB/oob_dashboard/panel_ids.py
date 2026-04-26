from __future__ import annotations

from typing import Final, Literal, get_args

PanelId = Literal[
    "system_status",
    "guard_chain",
    "incidents",
    "logs",
    "topology",
    "action_queue",
    "approval_queue",
    "audit_timeline",
]

CANONICAL_PANEL_IDS: Final[tuple[PanelId, ...]] = (
    "system_status",
    "guard_chain",
    "incidents",
    "logs",
    "topology",
    "action_queue",
    "approval_queue",
    "audit_timeline",
)


def build_canonical_panel_ids() -> tuple[PanelId, ...]:
    """Return the canonical ordered panel identifiers."""
    return CANONICAL_PANEL_IDS


def is_known_panel_id(value: str) -> bool:
    """Return whether a string is a known canonical panel id."""
    return value in get_args(PanelId)
