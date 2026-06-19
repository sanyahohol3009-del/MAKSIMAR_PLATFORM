from __future__ import annotations

from dataclasses import dataclass
from typing import Any


SWARM_AGENT_ROLES = (
    "conversation_agent",
    "project_coder_agent",
    "architect_agent",
    "tool_selector_agent",
    "safety_guard_agent",
    "action_worker_agent",
)


def _require_non_empty(value: str, field_name: str) -> None:
    if not isinstance(value, str) or not value.strip():
        raise ValueError(f"{field_name} must be a non-empty string")


@dataclass(frozen=True, slots=True)
class SwarmAgentRoleContract:
    role_id: str
    display_name: str
    allowed_capabilities: tuple[str, ...]
    may_propose: bool
    may_analyze: bool
    may_route: bool
    may_explain: bool
    may_execute_pc_action: bool
    may_execute_shell_action: bool
    may_write_runtime_state: bool
    may_deploy: bool
    may_write_canonical_memory: bool

    def __post_init__(self) -> None:
        _require_non_empty(self.role_id, "role_id")
        _require_non_empty(self.display_name, "display_name")
        if self.role_id not in SWARM_AGENT_ROLES:
            raise ValueError(f"unknown swarm role: {self.role_id!r}")
        if not self.allowed_capabilities:
            raise ValueError("allowed_capabilities must not be empty")
        for field_name in ("may_propose", "may_analyze", "may_route", "may_explain"):
            if getattr(self, field_name) is not True:
                raise ValueError(f"{field_name} must be True")
        for field_name in (
            "may_execute_pc_action",
            "may_execute_shell_action",
            "may_write_runtime_state",
            "may_deploy",
            "may_write_canonical_memory",
        ):
            if getattr(self, field_name) is not False:
                raise ValueError(f"{field_name} must be False")

    def to_read_model(self) -> dict[str, Any]:
        return {
            "role_id": self.role_id,
            "display_name": self.display_name,
            "allowed_capabilities": self.allowed_capabilities,
            "may_propose": self.may_propose,
            "may_analyze": self.may_analyze,
            "may_route": self.may_route,
            "may_explain": self.may_explain,
            "may_execute_pc_action": self.may_execute_pc_action,
            "may_execute_shell_action": self.may_execute_shell_action,
            "may_write_runtime_state": self.may_write_runtime_state,
            "may_deploy": self.may_deploy,
            "may_write_canonical_memory": self.may_write_canonical_memory,
        }


def build_default_swarm_agent_role_contracts() -> tuple[SwarmAgentRoleContract, ...]:
    return (
        SwarmAgentRoleContract(
            role_id="conversation_agent",
            display_name="Conversation Agent",
            allowed_capabilities=("propose", "analyze", "route", "explain"),
            may_propose=True,
            may_analyze=True,
            may_route=True,
            may_explain=True,
            may_execute_pc_action=False,
            may_execute_shell_action=False,
            may_write_runtime_state=False,
            may_deploy=False,
            may_write_canonical_memory=False,
        ),
        SwarmAgentRoleContract(
            role_id="project_coder_agent",
            display_name="Project Coder Agent",
            allowed_capabilities=("propose", "analyze", "route", "explain", "read_repo"),
            may_propose=True,
            may_analyze=True,
            may_route=True,
            may_explain=True,
            may_execute_pc_action=False,
            may_execute_shell_action=False,
            may_write_runtime_state=False,
            may_deploy=False,
            may_write_canonical_memory=False,
        ),
        SwarmAgentRoleContract(
            role_id="architect_agent",
            display_name="Architect Agent",
            allowed_capabilities=("propose", "analyze", "route", "explain", "architecture_review"),
            may_propose=True,
            may_analyze=True,
            may_route=True,
            may_explain=True,
            may_execute_pc_action=False,
            may_execute_shell_action=False,
            may_write_runtime_state=False,
            may_deploy=False,
            may_write_canonical_memory=False,
        ),
        SwarmAgentRoleContract(
            role_id="tool_selector_agent",
            display_name="Tool Selector Agent",
            allowed_capabilities=("propose", "analyze", "route", "explain", "select_tools"),
            may_propose=True,
            may_analyze=True,
            may_route=True,
            may_explain=True,
            may_execute_pc_action=False,
            may_execute_shell_action=False,
            may_write_runtime_state=False,
            may_deploy=False,
            may_write_canonical_memory=False,
        ),
        SwarmAgentRoleContract(
            role_id="safety_guard_agent",
            display_name="Safety Guard Agent",
            allowed_capabilities=("propose", "analyze", "route", "explain", "risk_gate"),
            may_propose=True,
            may_analyze=True,
            may_route=True,
            may_explain=True,
            may_execute_pc_action=False,
            may_execute_shell_action=False,
            may_write_runtime_state=False,
            may_deploy=False,
            may_write_canonical_memory=False,
        ),
        SwarmAgentRoleContract(
            role_id="action_worker_agent",
            display_name="Action Worker Agent",
            allowed_capabilities=("propose", "analyze", "route", "explain", "delegate_action"),
            may_propose=True,
            may_analyze=True,
            may_route=True,
            may_explain=True,
            may_execute_pc_action=False,
            may_execute_shell_action=False,
            may_write_runtime_state=False,
            may_deploy=False,
            may_write_canonical_memory=False,
        ),
    )


def get_swarm_agent_role_contract(role_id: str) -> SwarmAgentRoleContract:
    contracts = {contract.role_id: contract for contract in build_default_swarm_agent_role_contracts()}
    if role_id not in contracts:
        raise ValueError(f"unknown swarm role: {role_id!r}")
    return contracts[role_id]
