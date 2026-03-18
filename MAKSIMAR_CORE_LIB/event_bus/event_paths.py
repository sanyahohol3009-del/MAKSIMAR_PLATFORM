from __future__ import annotations

from pathlib import Path

from MAKSIMAR_CORE_LIB.shared_services.path_resolver import PATHS


def get_event_bus_root() -> Path:
    """Return canonical event bus root directory."""
    return PATHS.project_root / "EVENT_BUS"


def get_event_journal_path() -> Path:
    """Return canonical append-only event journal path."""
    return get_event_bus_root() / "event_journal.jsonl"
