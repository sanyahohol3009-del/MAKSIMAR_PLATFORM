from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True, slots=True)
class WorkerRegistryShellContract:
    """Final shell contract for worker registry layer."""

    shell_id: str
    total_workers: int
    total_capabilities: int
    total_io_entries: int
