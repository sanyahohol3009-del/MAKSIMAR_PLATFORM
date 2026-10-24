from __future__ import annotations

import json
import shutil
import subprocess
from typing import Any

from MAKSIMAR_CORE_LIB.action_library_adapters.external_tool_library_adapter import (
    build_jarvis_external_adapter_visibility_read_model as _build_external_visibility,
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



def build_provider_observation_context() -> dict[str, Any]:
    """Read canonical process launch context before any provider observation.

    This read model is not an HTTP-controlled permission or an admission decision.
    Invalid canonical context propagates before any observer can start I/O.
    """
    from CORE_ROOT.run_context import model_free_startup
    disabled = model_free_startup()
    return {"model_free_startup": disabled,
            "provider_observation_status": "NOT_ATTEMPTED" if disabled else "ELIGIBLE_FOR_OBSERVATION"}


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


# Process import observation is composed here; Core Lib only validates truth.
from pathlib import Path
import sys
from MAKSIMAR_CORE_LIB.action_library_adapters.agent_tooling_runtime_probe import (
    AgentToolingRuntimeProbeResult, EXTERNAL_RUNTIME_PYTHON,
    EXTERNAL_IMPORT_PROBE_TIMEOUT_SECONDS, _probe_path_only_manifest, parse_import_probe_response,
)
from MAKSIMAR_CORE_LIB.action_library_adapters.external_tool_library_adapter import load_external_tool_manifests


def _probe_import_in_external_runtime(package_name: str, import_name: str) -> AgentToolingRuntimeProbeResult:
    return _probe_import_with_runtime_python(str(EXTERNAL_RUNTIME_PYTHON), package_name, import_name)


def _probe_import_with_runtime_python(runtime_python: str, package_name: str, import_name: str) -> AgentToolingRuntimeProbeResult:
    if build_provider_observation_context()["model_free_startup"]:
        # Existing bool DTO: False means not proven, with explicit skipped reason.
        # Registration remains in manifests; this result grants no availability.
        return AgentToolingRuntimeProbeResult(
            installed=False, import_probe_passed=False, package_name=package_name,
            import_name=import_name, version_if_available="", runtime_python=runtime_python,
            errors=("model_free_import_not_attempted",), import_attempted=False,
        )
    runtime_python_path = Path(runtime_python)
    if not runtime_python_path.is_file():
        return AgentToolingRuntimeProbeResult(
            installed=False,
            import_probe_passed=False,
            package_name=package_name,
            import_name=import_name,
            version_if_available="",
            runtime_python=runtime_python,
            errors=("runtime_python_missing",),
            import_attempted=False,
        )
    probe_script = """
import importlib
import importlib.metadata
import json
import sys

package_name = sys.argv[1]
import_name = sys.argv[2]
result = {
    "installed": False,
    "import_probe_passed": False,
    "import_attempted": False,
    "package_name": package_name,
    "import_name": import_name,
    "version_if_available": "",
    "runtime_python": sys.executable,
    "errors": [],
}
try:
    result["import_attempted"] = True
    importlib.import_module(import_name)
    result["installed"] = True
    result["import_probe_passed"] = True
    try:
        result["version_if_available"] = importlib.metadata.version(package_name)
    except Exception:
        try:
            result["version_if_available"] = importlib.metadata.version(import_name)
        except Exception:
            result["version_if_available"] = ""
except Exception as exc:
    result["errors"] = [f"{type(exc).__name__}:{exc}"]
print(json.dumps(result, ensure_ascii=False))
"""
    try:
        completed = subprocess.run(
            [runtime_python, "-c", probe_script, package_name, import_name],
            check=False,
            capture_output=True,
            text=True,
            timeout=EXTERNAL_IMPORT_PROBE_TIMEOUT_SECONDS,
        )
    except (OSError, subprocess.TimeoutExpired) as exc:
        return AgentToolingRuntimeProbeResult(
            installed=False, import_probe_passed=False, package_name=package_name,
            import_name=import_name, version_if_available="", runtime_python=runtime_python,
            errors=(type(exc).__name__,), import_attempted=None if isinstance(exc, subprocess.TimeoutExpired) else False,
        )

    return parse_import_probe_response(completed, runtime_python, package_name, import_name)


def probe_agent_tooling_runtime() -> tuple[AgentToolingRuntimeProbeResult, ...]:
    results: list[AgentToolingRuntimeProbeResult] = []
    for manifest in load_external_tool_manifests():
        metadata = manifest.metadata if isinstance(manifest.metadata, dict) else {}
        external_path = str(metadata.get("external_path", "")).strip()
        if external_path:
            results.append(_probe_path_only_manifest(external_path, manifest.tool_id))
            continue
        runtime_selector = str(metadata.get("probe_runtime", "")).strip()
        package_name = manifest.package_name or manifest.module_import_name or manifest.tool_id
        import_name = manifest.module_import_name or manifest.package_name or manifest.tool_id
        if runtime_selector == "current_python":
            results.append(_probe_import_with_runtime_python(sys.executable, package_name, import_name))
            continue
        results.append(_probe_import_in_external_runtime(package_name, import_name))
    return tuple(results)


def build_agent_tooling_runtime_probe_read_model() -> dict[str, Any]:
    results = probe_agent_tooling_runtime()
    return {
        "runtime_python": str(EXTERNAL_RUNTIME_PYTHON),
        "probe_results": tuple(result.to_read_model() for result in results),
        "installed": tuple(result.package_name for result in results if result.installed),
        "import_probe_passed": tuple(result.package_name for result in results if result.import_probe_passed),
        "errors": tuple(result.errors for result in results if result.errors),
    }


def main() -> int:
    parser = argparse.ArgumentParser(description="Probe external agent/tooling runtime packages in the isolated venv.")
    parser.parse_args()
    print(json.dumps(build_agent_tooling_runtime_probe_read_model(), indent=2, ensure_ascii=False, sort_keys=True))
    return 0


def build_jarvis_external_adapter_visibility_read_model(probe_read_model=None):
    try:
        observation = build_agent_tooling_runtime_probe_read_model() if probe_read_model is None else probe_read_model
    except Exception:
        # Preserve the existing visibility consumer's unavailable-on-probe-error contract.
        observation = {"runtime_python": "", "probe_results": (), "installed": (),
                       "import_probe_passed": (), "errors": ("runtime_probe_unavailable",)}
    return _build_external_visibility(probe_read_model=observation)


def build_agent_tooling_runtime_adapter_read_model():
    from MAKSIMAR_CORE_LIB.action_library_adapters.agent_tooling_runtime_adapter import build_agent_tooling_runtime_adapter_read_model as build_adapter
    return build_adapter(probe_read_model=build_agent_tooling_runtime_probe_read_model())


def observe_foundation_consistency() -> dict:
    """Project a single canonical preflight snapshot, without rereading runtime files."""
    from MAKSIMAR_SERVER.OBSERVABILITY.jarvis_live.jarvis_live_observability_read_model import (
        observe_runtime_preflight, classify_observed_runtime,
    )
    from CORE_ROOT import runtime_paths as paths

    try:
        snapshot = observe_runtime_preflight()
        decision = classify_observed_runtime(snapshot)
    except (OSError, ValueError, TypeError, KeyError, AttributeError):
        return {"observation_error": "canonical_preflight_unavailable"}
    if not isinstance(snapshot, dict):
        return {"observation_error": "canonical_preflight_malformed"}
    def mapping(value):
        return value if isinstance(value, dict) else {}
    heartbeats = mapping(snapshot.get("heartbeats"))
    tmux = mapping(snapshot.get("tmux"))
    raw_sessions = tmux.get("sessions")
    sessions_known = (tmux.get("available") is True and not tmux.get("error")
                      and isinstance(raw_sessions, list) and all(isinstance(v, str) for v in raw_sessions))
    session_names = {
        "runtime": paths.RUNTIME_SESSION_NAME, "guard": paths.GUARD_SESSION_NAME,
        "core_guard": paths.CORE_GUARD_SESSION_NAME, "kernel_guard": paths.KERNEL_GUARD_SESSION_NAME,
    }
    processes = {}
    for scope in session_names:
        verified = mapping(heartbeats.get(scope)).get("process_verified")
        processes[scope] = verified if type(verified) is bool else None
    health, port = mapping(snapshot.get("health")), mapping(snapshot.get("port"))
    api = None
    if type(health.get("ok")) is bool and type(port.get("owned_by_project")) is bool:
        api = health["ok"] is True and port["owned_by_project"] is True and decision.get("healthy") is True
    return {
        "heartbeats": heartbeats, "processes": processes,
        "sessions": {scope: name in raw_sessions if sessions_known else None for scope, name in session_names.items()},
        "logs": {scope: None for scope in session_names},
        "runtime_api": api,
        "run_metadata": snapshot.get("run_metadata"),
        "observed_wall_time": snapshot.get("observed_wall_time"),
        "observed_monotonic_time": snapshot.get("observed_monotonic_time"),
        "canonical_decision": decision,
        "historical_only": mapping(snapshot.get("run_metadata")).get("status") in ("shutdown", "crashed"),
        "epoch_verified": decision.get("heartbeat_chain_valid") is True,
    }
