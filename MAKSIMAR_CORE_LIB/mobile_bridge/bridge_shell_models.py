from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True, slots=True)
class MobileBridgeShellContract:
    """Final shell contract for mobile bridge."""

    shell_id: str
    total_requests: int
    total_envelopes: int
    total_results: int
    core_write_allowed: bool
    heavy_execution_allowed_on_mobile: bool
