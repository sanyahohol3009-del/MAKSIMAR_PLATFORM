from __future__ import annotations

import json
import shutil
import subprocess
from typing import Any

from MAKSIMAR_CORE_LIB.enterprise_memory_domains.enterprise_memory_preview_builder import (
    build_enterprise_memory_preview,
)
from MAKSIMAR_CORE_LIB.memory_engine.memory_accessor import list_memory_definitions
from MAKSIMAR_CORE_LIB.retrieval_backend import (
    inspect_mgrep_readonly_availability,
    inspect_qdrant_readonly_availability,
    inspect_sqlite_vec_readonly_availability,
)
from MAKSIMAR_SERVER.CONTROL_PLANE.memory_routing.adapters.mempalace_read_only_routing_integration import (
    build_mempalace_read_only_routing_integration_preview,
)
from MAKSIMAR_SERVER.REGULATORY_MEMORY_FOUNDATION.regulatory_routing_preview_builder import (
    build_regulatory_routing_preview,
)

from tools.jarvis_live_runtime.memory_context_sources import (
    _build_memory_surface_inventory,
    _mempalace_status,
)
from tools.jarvis_live_runtime.ollama_transport import (
    PRIMARY_CONVERSATION_MODEL_ID,
    ollama_get_json as _ollama_get_json,
    ollama_post_json as _ollama_post_json,
)
from tools.jarvis_live_runtime.project_workspace_tools import (
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
from tools.jarvis_live_runtime.session_memory_store import (
    SESSION_STATE_PATH,
    _load_session_state,
)

RUNTIME_HISTORY_STORE = PROJECT_ROOT / "runtime_history_store"

def build_jarvis_live_project_status_read_model() -> dict[str, Any]:
    return {
        "project_status": _project_status_summary(),
        "read_only": True,
        "pc_control_allowed": False,
        "canonical_memory_write_allowed": False,
    }


def build_project_workspace_read_model() -> dict[str, Any]:
    git_status = repo_git_status()
    tracked = _tracked_project_files()
    return {
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
    return {
        "memory_federation_available": True,
        "memory_surfaces_detected_count": len(surfaces),
        "active_retrieval_surfaces": active,
        "disabled_memory_surfaces": disabled,
        "sandbox_only_memory_surfaces": sandbox_only,
        "vector_memory_available": any(surface["surface_id"] == "vector_runtime_indexes" and surface["status"] == "usable_now" for surface in surfaces),
        "regulatory_memory_available": any(surface["surface_id"] == "regulatory_memory_foundation" and surface["status"] == "usable_now" for surface in surfaces),
        "business_memory_available": any(surface["surface_id"] == "enterprise_business_memory" and surface["status"] == "usable_now" for surface in surfaces),
        "mempalace_status": _mempalace_status(),
        "runtime_history_store_exists": RUNTIME_HISTORY_STORE.exists(),
        "session_memory_exists": SESSION_STATE_PATH.exists(),
        "recent_turn_count": len(_load_session_state().get("recent_turns", [])),
        "surfaces": surfaces,
        "canonical_memory_write_allowed": False,
        "pc_control_allowed": False,
    }


def build_jarvis_live_tool_catalog_read_model() -> dict[str, Any]:
    memory = build_jarvis_live_memory_federation_status()
    mgrep = inspect_mgrep_readonly_availability(PROJECT_ROOT).to_read_model()
    sqlite_vec = inspect_sqlite_vec_readonly_availability(PROJECT_ROOT).to_read_model()
    qdrant = inspect_qdrant_readonly_availability(PROJECT_ROOT).to_read_model()
    memory_definitions = list_memory_definitions()
    enterprise_preview = build_enterprise_memory_preview()
    regulatory_preview = build_regulatory_routing_preview()
    mempalace_preview = build_mempalace_read_only_routing_integration_preview()
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
        "mempalace_read_only_sandbox",
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
    return {
        "catalog_id": "jarvis_live_existing_tool_catalog_v1",
        "read_only": True,
        "all_existing_read_tools_connected": True,
        "all_existing_memory_surfaces_connected": True,
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
            "mempalace_read_only_sandbox",
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
        "mempalace_routing_ready": bool(mempalace_preview.get("routing_integration_ready", False)),
        "qdrant_server_runtime_enabled": False,
        "direct_execution_allowed": False,
        "canonical_write_allowed": False,
        "pc_control_allowed": False,
    }


def _project_status_summary() -> str:
    branch = _run_read_only_command(("git", "branch", "--show-current"))
    status = _run_read_only_command(("git", "status", "--short"))
    tracked = _tracked_project_files()
    top_entries = _top_level_entries_from_tracked_files(tracked) if tracked else ()
    key_files = tuple(path for path in PROJECT_VISIBILITY_KEY_FILES if (PROJECT_ROOT / path).exists())
    history_exists = RUNTIME_HISTORY_STORE.exists()
    return (
        f"project_root={PROJECT_ROOT}; branch={branch or 'unknown'}; "
        f"git_status_short={status[:500] if status else 'clean_or_unavailable'}; "
        f"tracked_file_count={len(tracked) if tracked else 'unknown'}; "
        f"top_level={', '.join(top_entries[:40])}; "
        f"canonical_chat_path_files={', '.join(key_files)}; "
        f"runtime_history_store={RUNTIME_HISTORY_STORE}; "
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
