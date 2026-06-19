from __future__ import annotations

from dataclasses import dataclass
from typing import Any

from MAKSIMAR_CORE_LIB.swarm_coordination import SwarmConflictContract, SwarmConflictReadModel
from MAKSIMAR_SERVER.SWARM_COORDINATION_RUNTIME.swarm_task_router import SwarmTaskRoute


_KNOWN_SAFE_TOOLS = {
    "weather_lookup",
    "calendar_lookup",
    "mail_lookup",
    "screen_observer_read",
    "repo_git_status",
    "repo_tree",
    "repo_files",
    "read_file_snippet",
    "repo_search",
    "read_file_outline",
    "pytest_report_read",
    "session_memory",
    "local_chat_memory",
    "pc_open_browser",
    "pc_open_app",
    "risk_gate",
    "operator_proposal",
}


@dataclass(frozen=True, slots=True)
class SwarmConflictReport:
    report_id: str
    conflict_detected: bool
    blocking_conflict_kinds: tuple[str, ...]
    heavy_gpu_lock_status: str
    direct_execution_disabled_for_swarm: bool
    safe_action_delegated_to_action_library: bool
    risk_gate_required: bool
    reason_codes: tuple[str, ...]
    conflicts: tuple[SwarmConflictContract, ...]

    def __post_init__(self) -> None:
        if not isinstance(self.report_id, str) or not self.report_id.strip():
            raise ValueError("report_id must be a non-empty string")
        if self.direct_execution_disabled_for_swarm is not True:
            raise ValueError("direct_execution_disabled_for_swarm must be True")
        if self.safe_action_delegated_to_action_library is not True:
            raise ValueError("safe_action_delegated_to_action_library must be True")
        if self.conflict_detected and not self.blocking_conflict_kinds:
            raise ValueError("blocking_conflict_kinds must not be empty when conflict_detected")

    def to_read_model(self) -> SwarmConflictReadModel:
        return SwarmConflictReadModel(
            read_model_id="swarm_conflict_read_model_v1",
            conflict_detected=self.conflict_detected,
            blocking_conflict_kinds=self.blocking_conflict_kinds,
            heavy_gpu_lock_status=self.heavy_gpu_lock_status,
            risk_gate_required=self.risk_gate_required,
            direct_execution_disabled_for_swarm=self.direct_execution_disabled_for_swarm,
            reason_codes=self.reason_codes,
        )

    def as_dict(self) -> dict[str, Any]:
        payload = self.to_read_model().to_read_model()
        payload["conflicts"] = tuple(conflict.to_read_model() for conflict in self.conflicts)
        payload["safe_action_delegated_to_action_library"] = self.safe_action_delegated_to_action_library
        return payload


def detect_swarm_conflicts(routes: tuple[SwarmTaskRoute, ...]) -> SwarmConflictReport:
    conflicts: list[SwarmConflictContract] = []
    reason_codes: list[str] = []
    heavy_routes = [route for route in routes if route.heavy_model_requested]

    if len(heavy_routes) > 1:
        conflicts.append(
            SwarmConflictContract(
                conflict_id="swarm_conflict_heavy_gpu_v1",
                conflict_kind="heavy_gpu_parallel_blocked",
                blocking=True,
                reason_codes=("heavy_gpu_lock_required", "parallel_heavy_agents_denied"),
                heavy_gpu_conflict=True,
                direct_execution_conflict=False,
                unknown_tool_side_effect_conflict=False,
                voice_unverified_action_conflict=False,
            )
        )
        reason_codes.append("heavy_gpu_parallel_blocked")

    for route in routes:
        if route.direct_execution_disabled is not True or route.delegated_execution_surface == "swarm":
            conflicts.append(
                SwarmConflictContract(
                    conflict_id="swarm_conflict_direct_execution_v1",
                    conflict_kind="direct_swarm_execution_blocked",
                    blocking=True,
                    reason_codes=("swarm_execution_forbidden",),
                    heavy_gpu_conflict=False,
                    direct_execution_conflict=True,
                    unknown_tool_side_effect_conflict=False,
                    voice_unverified_action_conflict=False,
                )
            )
            reason_codes.append("direct_swarm_execution_blocked")
            break

    for route in routes:
        unknown_tools = tuple(tool for tool in route.selected_tools if tool not in _KNOWN_SAFE_TOOLS)
        if unknown_tools:
            conflicts.append(
                SwarmConflictContract(
                    conflict_id="swarm_conflict_unknown_tool_v1",
                    conflict_kind="unknown_tool_with_side_effects_blocked",
                    blocking=True,
                    reason_codes=("unknown_tool_side_effects", *unknown_tools),
                    heavy_gpu_conflict=False,
                    direct_execution_conflict=False,
                    unknown_tool_side_effect_conflict=True,
                    voice_unverified_action_conflict=False,
                )
            )
            reason_codes.append("unknown_tool_with_side_effects_blocked")
            break

    for route in routes:
        if route.task_contract.owner_identity_source == "voice_unverified" and any(
            tool.startswith("pc_") for tool in route.selected_tools
        ):
            conflicts.append(
                SwarmConflictContract(
                    conflict_id="swarm_conflict_voice_unverified_v1",
                    conflict_kind="voice_unverified_direct_pc_action_blocked",
                    blocking=True,
                    reason_codes=("voice_unverified_cannot_execute_pc_action",),
                    heavy_gpu_conflict=False,
                    direct_execution_conflict=False,
                    unknown_tool_side_effect_conflict=False,
                    voice_unverified_action_conflict=True,
                )
            )
            reason_codes.append("voice_unverified_direct_pc_action_blocked")
            break

    if len(heavy_routes) > 1:
        heavy_gpu_lock_status = "parallel_heavy_agents_blocked"
    elif len(heavy_routes) == 1:
        heavy_gpu_lock_status = "locked_single_heavy_agent"
    else:
        heavy_gpu_lock_status = "unlocked"
    risk_gate_required = any(route.risk_gate_required for route in routes) or any(
        conflict.voice_unverified_action_conflict or conflict.unknown_tool_side_effect_conflict
        for conflict in conflicts
    )
    return SwarmConflictReport(
        report_id="swarm_conflict_report_v1",
        conflict_detected=bool(conflicts),
        blocking_conflict_kinds=tuple(conflict.conflict_kind for conflict in conflicts),
        heavy_gpu_lock_status=heavy_gpu_lock_status,
        direct_execution_disabled_for_swarm=True,
        safe_action_delegated_to_action_library=True,
        risk_gate_required=risk_gate_required,
        reason_codes=tuple(reason_codes) if reason_codes else ("no_conflict",),
        conflicts=tuple(conflicts),
    )
