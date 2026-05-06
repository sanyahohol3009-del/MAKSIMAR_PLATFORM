from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True)
class PreLiveImportGateState:
    live_import_eligibility_ready: bool
    live_source_acceptance_ready: bool
    live_dedup_before_write_ready: bool
    live_target_readiness_ready: bool
    live_rollback_safe_session_ready: bool
    live_noncanonical_only_ready: bool
    prelive_gate_ready: bool

    def __post_init__(self) -> None:
        if not self.live_import_eligibility_ready:
            raise ValueError("live_import_eligibility_ready must be True")
        if not self.live_source_acceptance_ready:
            raise ValueError("live_source_acceptance_ready must be True")
        if not self.live_dedup_before_write_ready:
            raise ValueError("live_dedup_before_write_ready must be True")
        if not self.live_target_readiness_ready:
            raise ValueError("live_target_readiness_ready must be True")
        if not self.live_rollback_safe_session_ready:
            raise ValueError("live_rollback_safe_session_ready must be True")
        if not self.live_noncanonical_only_ready:
            raise ValueError("live_noncanonical_only_ready must be True")
        if not self.prelive_gate_ready:
            raise ValueError("prelive_gate_ready must be True")
