from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True, slots=True)
class DiagnosticsFeedbackItem:
    """One diagnostics item routed into chat feedback channel."""

    source_name: str
    probable_location: str
    hint_text: str


@dataclass(frozen=True, slots=True)
class DashboardFeedbackContract:
    """Unified diagnostics-to-chat feedback contract."""

    total_items: int
    items: tuple[DiagnosticsFeedbackItem, ...]
