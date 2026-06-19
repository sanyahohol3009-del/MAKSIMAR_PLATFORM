from __future__ import annotations

from dataclasses import dataclass
from typing import Any

from MAKSIMAR_CORE_LIB.swarm_coordination import SwarmTaskContract
from tools.jarvis_live_runtime.autonomous_tool_model_router import build_autonomous_tool_model_decision
from tools.jarvis_live_runtime.owner_identity_claim import OwnerIdentityClaim


def _read_only_discovery_only(selected_tools: tuple[str, ...]) -> bool:
    return all(
        tool in {
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
        }
        for tool in selected_tools
    )


def _select_agent_role(normalized_intent: str) -> tuple[str, tuple[str, ...]]:
    if normalized_intent == "weather_lookup":
        return "tool_selector_agent", ("tool_selector_agent",)
    if normalized_intent in {"calendar_lookup", "mail_lookup", "screen_observer"}:
        return "tool_selector_agent", ("tool_selector_agent",)
    if normalized_intent in {"code_debug", "project_workspace"}:
        return "project_coder_agent", ("project_coder_agent",)
    if normalized_intent == "complex_code_analysis":
        return "architect_agent", ("architect_agent",)
    if normalized_intent in {"safe_pc_open_browser", "safe_pc_open_app"}:
        return "action_worker_agent", ("action_worker_agent",)
    if normalized_intent == "risk_action_request":
        return "safety_guard_agent", ("safety_guard_agent",)
    return "conversation_agent", ("conversation_agent",)


@dataclass(frozen=True, slots=True)
class SwarmTaskRoute:
    route_id: str
    task_contract: SwarmTaskContract
    selected_agent_role: str
    selected_agent_roles: tuple[str, ...]
    selected_model_role_id: str
    selected_model_id: str
    selected_tools: tuple[str, ...]
    heavy_model_requested: bool
    delegated_execution_surface: str
    action_library_delegation_required: bool
    risk_gate_required: bool
    direct_execution_disabled: bool
    reason_codes: tuple[str, ...]

    def __post_init__(self) -> None:
        if not isinstance(self.route_id, str) or not self.route_id.strip():
            raise ValueError("route_id must be a non-empty string")
        if self.selected_agent_role not in self.selected_agent_roles:
            raise ValueError("selected_agent_role must be contained in selected_agent_roles")
        if self.direct_execution_disabled is not True:
            raise ValueError("direct_execution_disabled must be True")
        if not self.reason_codes:
            raise ValueError("reason_codes must not be empty")

    def to_read_model(self) -> dict[str, Any]:
        return {
            "route_id": self.route_id,
            "task_contract": self.task_contract.to_read_model(),
            "selected_agent_role": self.selected_agent_role,
            "selected_agent_roles": self.selected_agent_roles,
            "selected_model_role_id": self.selected_model_role_id,
            "selected_model_id": self.selected_model_id,
            "selected_tools": self.selected_tools,
            "heavy_model_requested": self.heavy_model_requested,
            "delegated_execution_surface": self.delegated_execution_surface,
            "action_library_delegation_required": self.action_library_delegation_required,
            "risk_gate_required": self.risk_gate_required,
            "direct_execution_disabled": self.direct_execution_disabled,
            "reason_codes": self.reason_codes,
        }


def route_swarm_task(
    user_text: str,
    *,
    input_channel: str,
    owner_identity_claim: OwnerIdentityClaim,
) -> SwarmTaskRoute:
    decision = build_autonomous_tool_model_decision(
        user_text,
        input_channel=input_channel,
        owner_identity_claim=owner_identity_claim,
    )
    selected_tools = tuple(str(tool) for tool in decision["selected_tools"])
    selected_agent_role, candidate_roles = _select_agent_role(str(decision["normalized_intent"]))
    direct_execution_requested = any(tool.startswith("pc_") for tool in selected_tools)
    read_only_only = _read_only_discovery_only(selected_tools)
    task_contract = SwarmTaskContract(
        task_id="swarm_task_contract_v1",
        user_text=str(user_text),
        input_channel=str(decision["input_channel"]),
        normalized_intent=str(decision["normalized_intent"]),
        selected_model_role_id=str(decision["selected_model_role_id"]),
        selected_model_id=str(decision["selected_model_id"]),
        selected_tools=selected_tools,
        candidate_agent_roles=candidate_roles,
        task_complexity=str(decision["task_complexity"]),
        heavy_model_requested=bool(decision["heavy_model_selected"]),
        risk_gate_required=bool(decision["risk_gate_required"]),
        safe_direct_action_candidate=bool(decision["safe_direct_action_allowed"]),
        read_only_discovery_only=read_only_only,
        owner_identity_source=str(owner_identity_claim.source),
        direct_execution_requested=direct_execution_requested,
    )
    delegated_surface = "none"
    action_library_required = False
    if direct_execution_requested:
        delegated_surface = "action_library"
        action_library_required = True
    elif bool(decision["risk_gate_required"]):
        delegated_surface = "risk_gate"
    return SwarmTaskRoute(
        route_id="swarm_task_route_v1",
        task_contract=task_contract,
        selected_agent_role=selected_agent_role,
        selected_agent_roles=candidate_roles,
        selected_model_role_id=str(decision["selected_model_role_id"]),
        selected_model_id=str(decision["selected_model_id"]),
        selected_tools=selected_tools,
        heavy_model_requested=bool(decision["heavy_model_selected"]),
        delegated_execution_surface=delegated_surface,
        action_library_delegation_required=action_library_required,
        risk_gate_required=bool(decision["risk_gate_required"]),
        direct_execution_disabled=True,
        reason_codes=(
            f"intent:{decision['normalized_intent']}",
            f"agent:{selected_agent_role}",
            f"model:{decision['selected_model_role_id']}",
        ),
    )
