from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True, slots=True)
class RootCauseHint:
    """One root-cause hint for dashboard diagnostics."""

    source_name: str
    status: str
    probable_location: str
    hint_text: str


@dataclass(frozen=True, slots=True)
class DiagnosticsIndex:
    """Read-only diagnostics index for OOB dashboard."""

    total_hints: int
    hints: list[RootCauseHint]
