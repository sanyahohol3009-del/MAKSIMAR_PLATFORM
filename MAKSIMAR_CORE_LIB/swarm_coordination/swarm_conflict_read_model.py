from __future__ import annotations

from dataclasses import dataclass
from typing import Any


@dataclass(frozen=True, slots=True)
class SwarmConflictReadModel:
    read_model_id: str
    conflict_detected: bool
    blocking_conflict_kinds: tuple[str, ...]
    heavy_gpu_lock_status: str
    risk_gate_required: bool
    direct_execution_disabled_for_swarm: bool
    reason_codes: tuple[str, ...]

    def __post_init__(self) -> None:
        if not isinstance(self.read_model_id, str) or not self.read_model_id.strip():
            raise ValueError("read_model_id must be a non-empty string")
        if not isinstance(self.heavy_gpu_lock_status, str) or not self.heavy_gpu_lock_status.strip():
            raise ValueError("heavy_gpu_lock_status must be a non-empty string")
        if self.direct_execution_disabled_for_swarm is not True:
            raise ValueError("direct_execution_disabled_for_swarm must be True")
        if self.conflict_detected and not self.blocking_conflict_kinds:
            raise ValueError("blocking_conflict_kinds must not be empty when conflict_detected")

    def to_read_model(self) -> dict[str, Any]:
        return {
            "read_model_id": self.read_model_id,
            "conflict_detected": self.conflict_detected,
            "blocking_conflict_kinds": self.blocking_conflict_kinds,
            "heavy_gpu_lock_status": self.heavy_gpu_lock_status,
            "risk_gate_required": self.risk_gate_required,
            "direct_execution_disabled_for_swarm": self.direct_execution_disabled_for_swarm,
            "reason_codes": self.reason_codes,
        }
