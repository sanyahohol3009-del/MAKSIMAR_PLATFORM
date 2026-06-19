from __future__ import annotations

from dataclasses import dataclass
from typing import Any


_CONFLICT_KINDS = {
    "heavy_gpu_parallel_blocked",
    "direct_swarm_execution_blocked",
    "unknown_tool_with_side_effects_blocked",
    "voice_unverified_direct_pc_action_blocked",
}


@dataclass(frozen=True, slots=True)
class SwarmConflictContract:
    conflict_id: str
    conflict_kind: str
    blocking: bool
    reason_codes: tuple[str, ...]
    heavy_gpu_conflict: bool
    direct_execution_conflict: bool
    unknown_tool_side_effect_conflict: bool
    voice_unverified_action_conflict: bool

    def __post_init__(self) -> None:
        if not isinstance(self.conflict_id, str) or not self.conflict_id.strip():
            raise ValueError("conflict_id must be a non-empty string")
        if self.conflict_kind not in _CONFLICT_KINDS:
            raise ValueError(f"unsupported conflict_kind: {self.conflict_kind!r}")
        if self.blocking is not True:
            raise ValueError("blocking must be True")
        if not self.reason_codes:
            raise ValueError("reason_codes must not be empty")
        if not any(
            (
                self.heavy_gpu_conflict,
                self.direct_execution_conflict,
                self.unknown_tool_side_effect_conflict,
                self.voice_unverified_action_conflict,
            )
        ):
            raise ValueError("at least one specific conflict flag must be True")

    def to_read_model(self) -> dict[str, Any]:
        return {
            "conflict_id": self.conflict_id,
            "conflict_kind": self.conflict_kind,
            "blocking": self.blocking,
            "reason_codes": self.reason_codes,
            "heavy_gpu_conflict": self.heavy_gpu_conflict,
            "direct_execution_conflict": self.direct_execution_conflict,
            "unknown_tool_side_effect_conflict": self.unknown_tool_side_effect_conflict,
            "voice_unverified_action_conflict": self.voice_unverified_action_conflict,
        }
