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
from tools.jarvis_live_runtime.jarvis_runtime_library_store import build_runtime_library_store_read_model
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


def build_jarvis_agent_catalog_read_model() -> dict[str, Any]:
    swarm_agents = tuple(contract.to_read_model() for contract in build_default_swarm_agent_role_contracts())
    runtime_libraries = build_runtime_library_store_read_model()
    visible_agents = tuple(agent["role_id"] for agent in swarm_agents)
    required_grounded_agents = tuple(
        agent_id
        for agent_id in (
            "tool_selector_agent",
            "project_coder_agent",
            "architect_agent",
            "safety_guard_agent",
            "action_worker_agent",
        )
        if agent_id in visible_agents
    )
    return {
        "agents": swarm_agents,
        "visible_agents": visible_agents,
        "required_grounded_agents": required_grounded_agents,
        "runtime_agent_libraries": tuple(runtime_libraries["agents"]),
        "runtime_agent_library_package_names": tuple(
            package["package_name"] for package in runtime_libraries["agents"] if isinstance(package, dict)
        ),
        "external_adapter_selector_agent_present": "external_adapter_selector_agent" in visible_agents,
        "external_adapter_selector_agent_status": "not_present_in_canonical_swarm_roles",
        "read_only": True,
        "execution_allowed": False,
        "pc_control_allowed": False,
        "canonical_write_allowed": False,
    }


def build_jarvis_skill_visibility_read_model() -> dict[str, Any]:
    tool_catalog = build_jarvis_live_tool_catalog_read_model()
    memory_status = build_jarvis_live_memory_federation_status()
    action_inventory = build_action_capability_inventory_read_model().to_read_model()
    external_visibility = build_jarvis_external_adapter_visibility_read_model()
    runtime_libraries = build_runtime_library_store_read_model()
    activation = build_default_capability_activation_matrix().to_read_model()
    agent_catalog = build_jarvis_agent_catalog_read_model()

    read_only_tools = tuple(tool_catalog["read_tools"])
    proposal_tools = tuple(tool_catalog["proposal_tools"])
    action_tools = tuple(capability["capability_id"] for capability in action_inventory["capabilities"])
    external_adapter_tools = tuple(external_visibility["active_adapter_ids"])
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
    visible_agents = tuple(agent_catalog["visible_agents"])
    visible_skills = _scan_visible_skills()

    return {
        "visible_tools": visible_tools,
        "visible_agents": visible_agents,
        "visible_skills": visible_skills,
        "agents": tuple(agent_catalog["agents"]),
        "external_adapter_tools": external_adapter_tools,
        "external_adapter_statuses": tuple(external_visibility["adapters"]),
        "external_adapter_legacy_tools": tuple(external_visibility["legacy_adapter_ids"]),
        "external_adapter_unavailable_tools": tuple(external_visibility["unavailable_adapter_ids"]),
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
        "project_workspace_tools": tuple(tool_catalog["project_repo_read_only_tools"]),
        "repo_introspection_tools": ("repo_search", "read_file_snippet", "read_file_outline", "repo_import_graph"),
        "memory_retrieval_tools": tuple(tool_catalog["memory_history_read_only_tools"])
        + tuple(tool_catalog["retrieval_read_only_tools"]),
        "tests_roadmap_drift_tools": ("status_tools", "roadmap_post_step_drift_check", "jarvis_live_ci_status"),
        "model_runtime_tools": tuple(tool_catalog["model_status_read_only_tools"]),
        "action_proposal_tools": proposal_tools,
        "runtime_library_packages": tuple(runtime_libraries["packages"]),
        "runtime_library_package_names": tuple(runtime_libraries["package_names"]),
        "runtime_library_available_package_names": tuple(runtime_libraries["available_package_names"]),
        "runtime_library_agents": tuple(runtime_libraries["agents"]),
        "runtime_library_skills_rag": tuple(runtime_libraries["skills_rag"]),
        "runtime_library_tools_browser": tuple(runtime_libraries["tools_browser"]),
        "runtime_library_categories": tuple(runtime_libraries["categories"]),
        "runtime_library_probe_reports_read": tuple(runtime_libraries["probe_reports_read"]),
        "runtime_library_execution_allowed": False,
        "runtime_library_install_allowed": False,
        "runtime_library_download_allowed": False,
        "windows_gui_bridge_enabled": False,
        "pc_control_allowed": False,
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
