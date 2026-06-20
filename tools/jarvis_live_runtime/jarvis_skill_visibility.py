from __future__ import annotations

from collections import Counter
from pathlib import Path
from typing import Any

from MAKSIMAR_CORE_LIB.action_library_adapters.action_capability_inventory_read_model import (
    build_action_capability_inventory_read_model,
)
from MAKSIMAR_CORE_LIB.action_library_adapters.external_tool_library_adapter import (
    build_jarvis_external_adapter_visibility_read_model,
)
from MAKSIMAR_CORE_LIB.runtime_activation import build_default_capability_activation_matrix
from MAKSIMAR_CORE_LIB.swarm_coordination.swarm_agent_role_contract import (
    build_default_swarm_agent_role_contracts,
)
from tools.jarvis_live_runtime.jarvis_live_read_models import build_jarvis_live_tool_catalog_read_model
from tools.jarvis_live_runtime.memory_context_builder import build_jarvis_live_memory_federation_status


PROJECT_ROOT = Path(__file__).resolve().parents[2]
_SKILL_SCAN_KEYWORDS = ("skill", "skills", "tool", "tools", "capability", "registry", "activation", "memory")
_SKILL_SCAN_ROOTS = (
    PROJECT_ROOT / "tools",
    PROJECT_ROOT / "MAKSIMAR_CORE_LIB",
    PROJECT_ROOT / "MAKSIMAR_SERVER",
)
_ROUTER_VISIBLE_TOOLS = (
    "weather_lookup",
    "calendar_lookup",
    "mail_lookup",
    "screen_observer_read",
    "repo_git_status",
    "repo_tree",
    "repo_files",
    "repo_search",
    "read_file_snippet",
    "read_file_outline",
    "pytest_report_read",
    "session_memory",
    "local_chat_memory",
    "pc_open_browser",
    "pc_open_app",
    "risk_gate",
    "operator_proposal",
)


def _normalize_tool_name(name: str) -> str:
    return "".join(ch for ch in str(name).casefold() if ch.isalnum() or ch == "_")


def _scan_visible_skills() -> tuple[str, ...]:
    found: set[str] = set()
    for root in _SKILL_SCAN_ROOTS:
        if not root.exists():
            continue
        for path in root.rglob("*"):
            if not path.is_file():
                continue
            relative = path.relative_to(PROJECT_ROOT).as_posix()
            lowered = relative.casefold()
            if any(keyword in lowered for keyword in _SKILL_SCAN_KEYWORDS):
                found.add(relative)
    return tuple(sorted(found))


def build_jarvis_skill_visibility_read_model() -> dict[str, Any]:
    tool_catalog = build_jarvis_live_tool_catalog_read_model()
    memory_status = build_jarvis_live_memory_federation_status()
    action_inventory = build_action_capability_inventory_read_model().to_read_model()
    external_visibility = build_jarvis_external_adapter_visibility_read_model()
    activation = build_default_capability_activation_matrix().to_read_model()
    swarm_agents = tuple(contract.to_read_model() for contract in build_default_swarm_agent_role_contracts())

    read_only_tools = tuple(tool_catalog["read_tools"])
    proposal_tools = tuple(tool_catalog["proposal_tools"])
    action_tools = tuple(capability["capability_id"] for capability in action_inventory["capabilities"])
    external_adapter_tools = tuple(tool["tool_id"] for tool in external_visibility["registry"]["tools"])
    memory_tools = tuple(tool_catalog["memory_surfaces"])
    activation_tools = tuple(entry["capability_id"] for entry in activation["entries"])

    all_tools = (
        read_only_tools
        + proposal_tools
        + action_tools
        + external_adapter_tools
        + memory_tools
        + activation_tools
        + _ROUTER_VISIBLE_TOOLS
    )
    duplicate_tools = tuple(
        sorted(
            tool_name
            for tool_name, count in Counter(_normalize_tool_name(tool) for tool in all_tools).items()
            if count > 1
        )
    )
    visible_tools = tuple(sorted(dict.fromkeys(all_tools)))
    visible_agents = tuple(agent["role_id"] for agent in swarm_agents)
    visible_skills = _scan_visible_skills()

    return {
        "visible_tools": visible_tools,
        "visible_agents": visible_agents,
        "visible_skills": visible_skills,
        "external_adapter_tools": external_adapter_tools,
        "read_only_tools": read_only_tools,
        "safe_direct_tools": tuple(action_inventory["safe_direct_capabilities"])
        + tuple(external_visibility["registry"]["safe_direct_tool_ids"]),
        "risk_gated_tools": tuple(action_inventory["risk_gated_capabilities"])
        + tuple(external_visibility["registry"]["risk_gated_tool_ids"]),
        "duplicate_tools": duplicate_tools,
        "unknown_tools_blocked": True,
        "semantic_dedupe_enabled": True,
        "memory_tools": memory_tools,
        "activation_capabilities": activation_tools,
        "universal_registry_tools": tuple(tool["tool_id"] for tool in external_visibility["registry"]["tools"]),
    }


def select_skills_for_tools(selected_tools: tuple[str, ...], selected_agent_roles: tuple[str, ...]) -> tuple[str, ...]:
    visibility = build_jarvis_skill_visibility_read_model()
    selected: list[str] = []
    tool_set = set(selected_tools)
    if tool_set & set(visibility["external_adapter_tools"]):
        selected.append("external_agent_tooling")
    if tool_set & set(visibility["read_only_tools"]):
        selected.append("read_only_discovery")
    if tool_set & set(visibility["safe_direct_tools"]):
        selected.append("action_library_safe_direct")
    if tool_set & set(visibility["risk_gated_tools"]):
        selected.append("risk_gate_or_action_library")
    if tool_set & set(visibility["memory_tools"]):
        selected.append("memory_federation")
    if "project_coder_agent" in selected_agent_roles or "architect_agent" in selected_agent_roles:
        selected.append("project_workspace_analysis")
    if "tool_selector_agent" in selected_agent_roles:
        selected.append("tool_selection")
    if "action_worker_agent" in selected_agent_roles:
        selected.append("action_library")
    if "safety_guard_agent" in selected_agent_roles:
        selected.append("safety_guard")
    if not selected:
        selected.append("conversation")
    return tuple(dict.fromkeys(selected))
