from __future__ import annotations

import json
import shutil
import subprocess
from typing import Any

from MAKSIMAR_CORE_LIB.action_library_adapters.external_tool_library_adapter import (
    build_jarvis_external_adapter_visibility_read_model,
)
from MAKSIMAR_CORE_LIB.enterprise_memory_domains.enterprise_memory_preview_builder import (
    build_enterprise_memory_preview,
)
from MAKSIMAR_CORE_LIB.memory_engine.memory_accessor import list_memory_definitions
from MAKSIMAR_CORE_LIB.retrieval_backend import (
    inspect_mgrep_readonly_availability,
    inspect_qdrant_readonly_availability,
    inspect_sqlite_vec_readonly_availability,
)
from MAKSIMAR_SERVER.REGULATORY_MEMORY_FOUNDATION.regulatory_routing_preview_builder import (
    build_regulatory_routing_preview,
)

from MAKSIMAR_SERVER.AI_ORCHESTRATION.memory_context_sources import (
    _build_memory_surface_inventory,
    _mempalace_status,
)
from MAKSIMAR_CORE_LIB.project_read.jarvis_runtime_library_store import (
    build_runtime_library_store_read_model,
)
from MAKSIMAR_SERVER.AI_ORCHESTRATION.ollama_transport import (
    PRIMARY_CONVERSATION_MODEL_ID,
    ollama_get_json as _ollama_get_json,
    ollama_post_json as _ollama_post_json,
)
from MAKSIMAR_SERVER.AI_ORCHESTRATION.project_workspace_tools import (
    PROJECT_FILES_PAGE_SIZE,
    PROJECT_ROOT,
    PROJECT_TREE_MAX_ENTRIES,
    PROJECT_VISIBILITY_KEY_FILES,
    _domain_groups_for_paths,
    _important_paths_detected,
    _run_read_only_command,
    _top_level_entries_from_tracked_files,
    _tracked_project_files,
    repo_files,
    repo_git_status,
    repo_tree,
)
from MAKSIMAR_SERVER.AI_ORCHESTRATION.session_memory_store import (
    SESSION_STATE_PATH,
    _load_session_state,
    _session_turn_log_path,
    _memory_truth_contract,
    _stable_style_profile_from_state,
    _read_recent_local_chat_records,
    DANGEROUS_MEMORY_FLAGS,
)



def _operator_capability_flags() -> dict[str, Any]:
    return {
        "read_project_allowed": True,
        "read_memory_allowed": True,
        "read_history_allowed": True,
        "read_mempalace_allowed": True,
        "read_n8n_allowed": True,
        "agent_selection_allowed": True,
        "skill_selection_allowed": True,
        "tool_selection_allowed": True,
        "external_adapter_selection_allowed": True,
        "runtime_library_visibility_allowed": True,
        "runtime_import_probe_allowed": True,
        "runtime_probe_allowed": True,
        "sandbox_probe_allowed": True,
        "sandbox_execution_allowed": True,
        "code_draft_allowed": True,
        "patch_proposal_allowed": True,
        "bounded_test_allowed": True,
        "n8n_workflow_read_allowed": True,
        "n8n_workflow_proposal_allowed": True,
        "mempalace_read_allowed": True,
        "mempalace_query_allowed": True,
        "core_write_allowed": False,
        "canonical_write_allowed": False,
        "direct_core_mutation_allowed": False,
        "auto_apply_allowed": False,
        "auto_git_add_allowed": False,
        "auto_git_commit_allowed": False,
        "auto_git_push_allowed": False,
        "auto_install_allowed": False,
        "auto_download_allowed": False,
        "pc_control_without_approval": False,
        "browser_control_without_approval": False,
        "mobile_control_without_approval": False,
    }


def build_jarvis_live_brain_health() -> dict[str, Any]:
    """Compatibility health projected from the existing current journal owner."""
    memory = build_jarvis_live_memory_federation_status()
    health = dict(memory["canonical_session_health"])
    recent = _read_recent_local_chat_records()
    return {
        "status": health["status"], "canonical_session_health": health,
        "session_memory_path": health["path"], "local_chat_memory_path": health["path"],
        "session_memory_exists": _session_turn_log_path().is_file(),
        "local_chat_memory_exists": _session_turn_log_path().is_file(),
        "compatibility_session_state_path": str(SESSION_STATE_PATH),
        "stable_style_profile": _stable_style_profile_from_state(_load_session_state()),
        "style_profile_scope": "DESCRIPTIVE_COMPATIBILITY_SETTINGS_ONLY",
        "memory_truth_contract": _memory_truth_contract(),
        "append_only_local_chat_write_enabled": True,
        "native_session_writer": "CONTROL_PLANE.api_server._capture_canonical_turn_memory -> CanonicalSessionContextStore.append",
        "dangerous_mutation_flags": dict(DANGEROUS_MEMORY_FLAGS),
        "canonical_turn_count": health["canonical_turn_count"],
        "recent_turn_count": len(recent), "recent_turn_count_scope": "BOUNDED_JOURNAL_READBACK",
        "last_append_at": health.get("last_append_at"), "memory_federation": memory,
        "read_only": True, "canonical_memory_write_allowed": False, "pc_control_allowed": False,
        "permission_scope": "THIS_READ_MODEL_ONLY; native journal writer remains canonical",
    }


def build_jarvis_live_session_status() -> dict[str, Any]:
    """One shared current health projection; no compatibility cache readiness."""
    return build_jarvis_live_brain_health()


def build_jarvis_live_project_status_read_model() -> dict[str, Any]:
    payload = {
        "project_status": _project_status_summary(),
        "read_only": True,
        "pc_control_allowed": False,
        "canonical_memory_write_allowed": False,
    }
    payload.update(_operator_capability_flags())
    return payload


def build_project_workspace_read_model() -> dict[str, Any]:
    git_status = repo_git_status()
    tracked = _tracked_project_files()
    payload = {
        "project_root": str(PROJECT_ROOT),
        "git_branch": git_status["branch"],
        "git_head": git_status["head"],
        "git_status_short": git_status["status_short"],
        "dirty_files": git_status["dirty_files"],
        "untracked_files": git_status["untracked_files"],
        "staged_files": git_status["staged_files"],
        "tracked_file_count": len(tracked),
        "tracked_files_by_page": repo_files(page=1, page_size=PROJECT_FILES_PAGE_SIZE),
        "top_level_tree": repo_tree(depth=2, max_entries=PROJECT_TREE_MAX_ENTRIES),
        "important_paths_detected_dynamically": _important_paths_detected(tracked),
        "domain_groups": _domain_groups_for_paths(tracked),
        "recent_test_status_if_available": "not_run_from_chat",
        "roadmap_status_if_available": status_tools().get("roadmap_post_step_drift_check", ""),
        "model_status_if_available": model_runtime_status(),
        "runtime_status_if_available": status_tools().get("jarvis_live_ci_status", ""),
        "read_only": True,
        "direct_execution_allowed": False,
        "canonical_write_allowed": False,
        "pc_control_allowed": False,
    }
    payload.update(_operator_capability_flags())
    return payload


def status_tools() -> dict[str, str]:
    return {
        "jarvis_live_ci_status": _run_read_only_command(("python", "tools/project_readiness_control/jarvis_live_ci_status.py")),
        "roadmap_post_step_drift_check": _run_read_only_command(("python", "tools/roadmap_post_step_drift_check.py")),
        "read_only": "true",
    }


def _compact_json(value: Any) -> str:
    try:
        return json.dumps(value, ensure_ascii=False, sort_keys=True)
    except TypeError:
        return str(value)


def model_runtime_status() -> dict[str, str]:
    version = _ollama_get_json("/api/version")
    tags = _ollama_get_json("/api/tags")
    ps = _ollama_get_json("/api/ps")
    show_primary = _ollama_post_json("/api/show", {"model": PRIMARY_CONVERSATION_MODEL_ID})
    return {
        "ollama_version": _compact_json(version) if version else "unavailable",
        "ollama_tags": _compact_json(tags) if tags else "unavailable",
        "ollama_ps": _compact_json(ps) if ps else "unavailable",
        "ollama_show_primary_model": _compact_json(show_primary) if show_primary else "unavailable",
        "nvidia_smi": _run_optional_read_only_command(("nvidia-smi",)),
        "free_h": _run_optional_read_only_command(("free", "-h")),
        "ollama_is_local_model_engine": "true",
        "pc_control_allowed": "false",
    }


def build_jarvis_live_memory_federation_status() -> dict[str, Any]:
    surfaces = _build_memory_surface_inventory()
    active = tuple(surface["surface_id"] for surface in surfaces if surface["status"] == "usable_now")
    disabled = tuple(surface["surface_id"] for surface in surfaces if surface["status"] in {"disabled", "not_connected", "unsafe"})
    sandbox_only = tuple(surface["surface_id"] for surface in surfaces if surface["status"] == "sandbox_only")
    stores: dict[str, dict[str, Any]] = {}
    for surface in surfaces:
        if surface["classification"] not in {"CANONICAL_STORE", "CHILD_BACKEND"}:
            continue
        storage_path = surface["path"]
        store = stores.setdefault(storage_path, {"path": storage_path, "owner": surface.get("owner"),
            "runtime_status": surface["runtime_status"], "logical_surfaces": [],
            "store_kind": "CHROMA_VECTOR_ARCHIVE" if surface["surface_id"] == "mempalace_search" else "APPEND_ONLY_JSONL",
            "vector_index": surface["surface_id"] == "mempalace_search"})
        store["logical_surfaces"].append(surface["surface_id"])
        if surface["surface_id"] in {"native_event_journal", "native_incident_history"}:
            store["native_journal_health"] = surface["health"]
    payload = {
        "memory_federation_available": True,
        "inventory_coverage": "REGISTERED_NATIVE_SURFACES_ONLY",
        "whole_organism_inventory_complete": False,
        "memory_surfaces_detected_count": len(surfaces),
        "physical_stores": tuple(stores.values()),
        "physical_store_count": len(stores),
        "live_physical_store_count": sum(store["runtime_status"] == "LIVE_READ_ONLY" for store in stores.values()),
        "surface_count_is_not_store_count": True,
        "canonical_session_health": next(surface["health"] for surface in surfaces if surface["surface_id"] == "local_chat_memory"),
        "active_retrieval_surfaces": active,
        "disabled_memory_surfaces": disabled,
        "sandbox_only_memory_surfaces": sandbox_only,
        "vector_memory_available": any(surface["surface_id"] == "mempalace_search"
            and surface.get("health", {}).get("status") == "LIVE_READ_ONLY"
            and surface.get("health", {}).get("embedding_count", 0) > 0 for surface in surfaces),
        "regulatory_memory_available": any(surface["surface_id"] == "regulatory_memory_foundation" and surface.get("persisted_dataset_available") is True for surface in surfaces),
        "business_memory_available": any(surface["surface_id"] == "enterprise_business_memory" and surface.get("persisted_dataset_available") is True for surface in surfaces),
        "enterprise_regulatory_contract_read_models_available": True,
        "mempalace_status": _mempalace_status(),
        "runtime_history_store_exists": any(surface["surface_id"] == "runtime_history_store" and surface["status"] == "usable_now" for surface in surfaces),
        "session_memory_exists": _session_turn_log_path().is_file(),
        "recent_turn_count": len(_read_recent_local_chat_records()),
        "recent_turn_count_scope": "BOUNDED_ELIGIBLE_CANONICAL_JOURNAL_READBACK",
        "surfaces": surfaces,
        "canonical_memory_write_allowed": False,
        "pc_control_allowed": False,
    }
    payload.update(_operator_capability_flags())
    return payload


def build_jarvis_live_tool_catalog_read_model() -> dict[str, Any]:
    memory = build_jarvis_live_memory_federation_status()
    external_adapters = build_jarvis_external_adapter_visibility_read_model()
    runtime_libraries = build_runtime_library_store_read_model()
    mgrep = inspect_mgrep_readonly_availability(PROJECT_ROOT).to_read_model()
    sqlite_vec = inspect_sqlite_vec_readonly_availability(PROJECT_ROOT).to_read_model()
    qdrant = inspect_qdrant_readonly_availability(PROJECT_ROOT).to_read_model()
    memory_definitions = list_memory_definitions()
    enterprise_preview = build_enterprise_memory_preview()
    regulatory_preview = build_regulatory_routing_preview()
    mempalace_surface = next(
        (surface for surface in memory["surfaces"] if surface["surface_id"] == "mempalace_search"),
        None,
    )
    read_tools = (
        "repo_git_status",
        "build_project_workspace_read_model",
        "repo_tree",
        "repo_files",
        "repo_search",
        "read_file_snippet",
        "read_file_outline",
        "repo_import_graph",
        "status_tools",
        "model_runtime_status",
        "stable_style_profile",
        "session_memory",
        "local_chat_memory",
        "runtime_history_store",
        "history_query",
        "memory_engine_registry",
        "enterprise_business_memory",
        "regulatory_memory_foundation",
        "vector_runtime_indexes",
        "mempalace_search",
        "mgrep_readonly",
        "sqlite_vec_readonly",
        "qdrant_readonly_status",
        "retrieval_backend_status_read_model",
        "retrieval_vendor_gate_contract",
        "retrieval_tool_registry_contract",
        "semantic_intent_classifier",
    )
    proposal_tools = (
        "operator_proposal",
        "approval_boundary_read",
        "capability_registry_read",
        "pytest_run_proposal",
        "git_commit_proposal",
        "download_install_proposal",
        "n8n_adapter_proposal",
        "pc_action_proposal",
        "tool_call_proposal",
    )
    # Historical views remain visible as metadata, but cannot reintroduce a
    # superseded execution owner through the compatibility read-tools catalog.
    superseded_surfaces = frozenset(
        surface["surface_id"] for surface in memory["surfaces"]
        if surface.get("runtime_status") == "SUPERSEDED_BY_CANONICAL_OWNER"
    )
    read_tools = tuple(tool for tool in read_tools if tool not in superseded_surfaces)
    payload = {
        "catalog_id": "jarvis_live_existing_tool_catalog_v1",
        "superseded_read_model_tools": tuple(sorted(superseded_surfaces)),
        "read_only": True,
        "all_existing_read_tools_connected": True,
        "all_existing_memory_surfaces_connected": not memory["disabled_memory_surfaces"],
        "read_tools": read_tools,
        "proposal_tools": proposal_tools,
        "memory_surfaces": tuple(surface["surface_id"] for surface in memory["surfaces"]),
        "active_retrieval_surfaces": memory["active_retrieval_surfaces"],
        "sandbox_only_memory_surfaces": memory["sandbox_only_memory_surfaces"],
        "disabled_memory_surfaces": memory["disabled_memory_surfaces"],
        "execution_allowed": False,
        "approval_required_for_actions": True,
        "pc_control_allowed": False,
        "shell_execution_enabled": False,
        "direct_execution_allowed": False,
        "canonical_write_allowed": False,
        "runtime_mutation_allowed": False,
        "deployment_allowed_now": False,
        "retrieval_tool_contracts_visible": True,
        "retrieval_tool_runtime_enabled": True,
        "retrieval_auto_routing_contract_enabled": True,
        "retrieval_auto_routing_runtime_enabled": True,
        "project_repo_read_only_tools": (
            "repo_git_status",
            "build_project_workspace_read_model",
            "repo_tree",
            "repo_files",
            "repo_search",
            "read_file_snippet",
            "read_file_outline",
        ),
        "retrieval_read_only_tools": (
            "mgrep_readonly",
            "sqlite_vec_readonly",
            "qdrant_readonly_status",
            "retrieval_backend_status_read_model",
            "retrieval_tool_registry_contract",
        ),
        "memory_history_read_only_tools": (
            "session_memory",
            "local_chat_memory",
            "runtime_history_store",
            "history_query",
            "memory_engine_registry",
            "enterprise_business_memory",
            "regulatory_memory_foundation",
            "mempalace_search",
        ),
        "model_status_read_only_tools": (
            "model_runtime_status",
            "build_jarvis_live_session_status",
            "build_jarvis_live_brain_health",
            "model_registry_status",
        ),
        "roadmap_safety_read_only_tools": (
            "status_tools",
            "roadmap_post_step_drift_check",
            "jarvis_live_ci_status",
            "project_safety_formatter",
        ),
        "action_proposal_only_tools": proposal_tools,
        "mgrep_status": mgrep,
        "sqlite_vec_status": sqlite_vec,
        "qdrant_status": qdrant,
        "memory_definition_count": len(memory_definitions),
        "memory_definition_ids": tuple(definition.entity_id for definition in memory_definitions[:24]),
        "enterprise_memory_preview_ready": bool(enterprise_preview.get("preview_ready", False)),
        "regulatory_routing_preview_ready": bool(regulatory_preview.get("preview_ready", False)),
        "mempalace_routing_ready": bool(
            mempalace_surface
            and mempalace_surface.get("runtime_status") == "LIVE_READ_ONLY"
            and mempalace_surface.get("health", {}).get("status") == "LIVE_READ_ONLY"
        ),
        "mempalace_routing_readiness_scope": memory["inventory_coverage"],
        "external_adapter_tools": tuple(external_adapters["active_adapter_ids"]),
        "external_adapter_registry_tools": tuple(tool["tool_id"] for tool in external_adapters["registry"]["tools"]),
        "external_adapter_runtime_status": tuple(external_adapters["adapters"]),
        "external_adapter_unavailable_tools": tuple(external_adapters["unavailable_adapter_ids"]),
        "external_adapter_legacy_tools": tuple(external_adapters["legacy_adapter_ids"]),
        "external_adapter_runtime_python": str(external_adapters["runtime_python"]),
        "external_adapter_probe": external_adapters["probe"],
        "runtime_library_store_connected": True,
        "runtime_library_packages": tuple(runtime_libraries["packages"]),
        "runtime_library_available_packages": tuple(runtime_libraries["available_packages"]),
        "runtime_library_package_names": tuple(runtime_libraries["package_names"]),
        "runtime_library_available_package_names": tuple(runtime_libraries["available_package_names"]),
        "runtime_library_module_names": tuple(runtime_libraries["module_names"]),
        "runtime_library_agents": tuple(runtime_libraries["agents"]),
        "runtime_library_skills_rag": tuple(runtime_libraries["skills_rag"]),
        "runtime_library_tools_browser": tuple(runtime_libraries["tools_browser"]),
        "runtime_library_categories": tuple(runtime_libraries["categories"]),
        "runtime_library_probe_reports_read": tuple(runtime_libraries["probe_reports_read"]),
        "runtime_library_probe_reports_loaded": tuple(runtime_libraries.get("probe_reports_loaded", ())),
        "runtime_library_source_observations": tuple(runtime_libraries.get("source_observations", ())),
        "runtime_library_source_errors": tuple(runtime_libraries.get("source_errors", ())),
        "runtime_library_current_execution_verified": runtime_libraries.get("current_execution_verified", False),
        "runtime_library_probe_freshness": runtime_libraries.get("probe_freshness", "UNASSESSED"),
        "runtime_library_execution_allowed": True,
        "runtime_library_install_allowed": False,
        "runtime_library_download_allowed": False,
        "qdrant_server_runtime_enabled": False,
        "direct_execution_allowed": False,
        "canonical_write_allowed": False,
        "pc_control_allowed": False,
    }
    payload["_external_visibility"] = external_adapters
    payload.update(_operator_capability_flags())
    return payload


def _project_status_summary() -> str:
    branch = _run_read_only_command(("git", "branch", "--show-current"))
    status = _run_read_only_command(("git", "status", "--short"))
    tracked = _tracked_project_files()
    top_entries = _top_level_entries_from_tracked_files(tracked) if tracked else ()
    key_files = tuple(path for path in PROJECT_VISIBILITY_KEY_FILES if (PROJECT_ROOT / path).exists())
    history_path = _session_turn_log_path()
    history_exists = history_path.is_file()
    return (
        f"project_root={PROJECT_ROOT}; branch={branch or 'unknown'}; "
        f"git_status_short={status[:500] if status else 'clean_or_unavailable'}; "
        f"tracked_file_count={len(tracked) if tracked else 'unknown'}; "
        f"top_level={', '.join(top_entries[:40])}; "
        f"canonical_chat_path_files={', '.join(key_files)}; "
        f"runtime_history_store={history_path}; "
        f"runtime_history_store_exists={str(history_exists).lower()}; "
        "project_workspace_read_enabled=true; project_file_read_enabled=true; "
        "pc_control_allowed=false; canonical_write_allowed=false; direct_execution_allowed=false"
    )


def _run_read_only_command(command: tuple[str, ...]) -> str:
    try:
        result = subprocess.run(
            list(command),
            cwd=str(PROJECT_ROOT),
            check=False,
            stdout=subprocess.PIPE,
            stderr=subprocess.DEVNULL,
            text=True,
            timeout=5,
        )
    except (OSError, subprocess.TimeoutExpired):
        return ""
    if result.returncode != 0:
        return ""
    return result.stdout.strip()


def _run_optional_read_only_command(command: tuple[str, ...]) -> str:
    if shutil.which(command[0]) is None:
        return ""
    return _run_read_only_command(command)
