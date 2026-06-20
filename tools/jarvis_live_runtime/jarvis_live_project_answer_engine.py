from __future__ import annotations

import re
from typing import Any

from MAKSIMAR_CORE_LIB.retrieval_backend import (
    build_retrieval_backend_status_read_model,
    build_retrieval_readonly_tool_route,
    build_retrieval_runtime_readonly_availability,
    build_retrieval_tool_enablement_policy,
    build_retrieval_tool_registry_contract,
    inspect_mgrep_readonly_availability,
    inspect_qdrant_readonly_availability,
    inspect_sqlite_vec_readonly_availability,
)
from MAKSIMAR_CORE_LIB.runtime_activation import build_default_capability_activation_matrix

from tools.jarvis_live_runtime.jarvis_live_guarded_answer_engine import _asks_pc_action
from tools.jarvis_live_runtime.jarvis_live_read_models import (
    build_jarvis_live_tool_catalog_read_model,
    build_project_workspace_read_model,
    model_runtime_status,
    status_tools,
)
from tools.jarvis_live_runtime.memory_context_builder import JarvisBrainContext
from tools.jarvis_live_runtime.memory_context_sources import (
    _memory_query_terms,
    _retrieve_history_snippets,
)
from tools.jarvis_live_runtime.project_workspace_tools import (
    PROJECT_FILE_MAX_BYTES,
    PROJECT_FILE_PAGE_LINES,
    PROJECT_ROOT,
    PROJECT_TREE_MAX_ENTRIES,
    PROJECT_VISIBILITY_KEY_FILES,
    _domain_groups_for_paths,
    _top_level_entries_from_tracked_files,
    _tracked_project_files,
    read_file_outline,
    read_file_snippet,
    repo_files,
    repo_git_status,
    repo_import_graph,
    repo_search,
    repo_tree,
)
from tools.jarvis_live_runtime.read_only_tool_router import (
    _extract_filename_token,
    _extract_requested_file_path,
)
from tools.jarvis_live_runtime.jarvis_skill_visibility import (
    build_jarvis_agent_catalog_read_model,
    build_jarvis_skill_visibility_read_model,
)
from tools.jarvis_live_runtime.session_memory_store import _memory_truth_contract

def _answer_with_read_only_tools_if_grounded(
    user_text: str,
    context: JarvisBrainContext,
    plan: dict[str, Any],
) -> str:
    intent = str(plan.get("intent_family", "CONVERSATION"))
    if intent == "CONVERSATION":
        return ""
    if intent == "ACTIVATION_MATRIX":
        plan["evidence_count"] = 1
        return _format_activation_matrix_answer()
    if intent == "PROJECT_STATUS":
        plan["evidence_count"] = 1
        return _format_project_status_answer()
    if intent == "PROJECT_STRUCTURE":
        plan["evidence_count"] = 3
        return _format_project_structure_grounded_answer()
    if intent == "PROJECT_SEARCH":
        answer, evidence_count = _format_project_semantic_search_answer(user_text, _plan_tool_route(plan))
        plan["evidence_count"] = evidence_count
        return answer
    if intent == "SEMANTIC_SIMILARITY":
        answer, evidence_count = _format_semantic_similarity_answer(
            user_text,
            _plan_tool_route(plan),
            _extract_semantic_similarity_query(user_text),
        )
        plan["evidence_count"] = evidence_count
        return answer
    if intent == "RETRIEVAL_BACKEND_STATUS":
        plan["evidence_count"] = 3
        return _format_retrieval_backend_status_answer()
    if intent == "VENDOR_STATUS":
        plan["evidence_count"] = 2
        return _format_retrieval_vendor_status_answer()
    if intent == "CONTAINER_STATUS":
        plan["evidence_count"] = 3
        return _format_retrieval_container_status_answer()
    if intent == "TEST_STATUS":
        plan["evidence_count"] = 1
        return _format_roadmap_answer()
    if intent == "SOURCE_EVIDENCE":
        answer, evidence_count = _format_source_evidence_answer(user_text)
        plan["evidence_count"] = evidence_count
        return answer
    if intent == "DOCS_CONTRACTS":
        answer, evidence_count = _format_project_semantic_search_answer(user_text, _plan_tool_route(plan))
        plan["evidence_count"] = evidence_count
        return answer
    if intent == "AUTO_TOOL_USE":
        plan["evidence_count"] = 2
        return _format_auto_tool_use_status_answer()
    if intent == "PROJECT_FILE":
        path = _extract_requested_file_path(user_text)
        if not path:
            plan["evidence_count"] = 0
            return "Не нашёл подтверждение в текущих read-only источниках: путь файла не распознан."
        snippet = _format_file_answer(path, page=1, intent="PROJECT_FILE")
        outline = _format_outline_answer(path)
        plan["evidence_count"] = 2 if "denied" not in snippet.casefold() else 0
        return snippet + "\n\n" + outline
    if intent == "MEMORY_RECALL":
        answer, evidence_count = _format_memory_history_grounded_answer(user_text, context)
        plan["evidence_count"] = evidence_count
        return answer
    if intent == "MODEL_STATUS":
        plan["evidence_count"] = 1
        return _format_project_models_answer()
    if intent == "ROADMAP_STATUS":
        plan["evidence_count"] = 1
        return _format_roadmap_answer()
    if intent == "SAFETY_STATUS":
        plan["evidence_count"] = 1
        return _format_safety_answer()
    if intent == "ACTION_REQUEST":
        plan["evidence_count"] = 1
        return _format_action_request_proposal_answer(user_text)
    if intent == "TOOL_CATALOG":
        catalog = build_jarvis_live_tool_catalog_read_model()
        plan["evidence_count"] = len(catalog["read_tools"]) + len(catalog["proposal_tools"])
        return _format_tool_catalog_answer(catalog)
    if intent == "AGENT_CATALOG":
        catalog = build_jarvis_agent_catalog_read_model()
        plan["evidence_count"] = len(catalog["visible_agents"])
        return _format_agent_catalog_answer(catalog)
    if intent == "SKILL_VISIBILITY":
        visibility = build_jarvis_skill_visibility_read_model()
        plan["evidence_count"] = len(visibility["visible_tools"]) + len(visibility["visible_agents"])
        return _format_skill_visibility_answer(visibility)
    return ""


def _plan_tool_route(plan: dict[str, Any]) -> dict[str, Any]:
    route = plan.get("tool_route")
    return route if isinstance(route, dict) else {}


def _answer_project_read_tool_request(user_text: str) -> str:
    text = user_text.strip()
    lowered = text.casefold()
    if text.startswith("/project"):
        return _answer_project_command(text)
    if any(marker in lowered for marker in ("что изменено", "что поменялось", "какие изменения", "dirty", "untracked")):
        return _format_project_status_answer()
    if any(marker in lowered for marker in ("покажи полностью весь проект", "весь проект", "полный проект")):
        return _format_project_atlas_answer()
    if "terminal chat" in lowered and any(marker in lowered for marker in ("где", "найди", "что у нас")):
        return _format_search_answer("terminal_chat jarvis_live_terminal_chat")
    if any(marker in lowered for marker in ("core guard", "watchdog", "safety", "security", "approval", "execution control")):
        return _format_safety_answer()
    if any(marker in lowered for marker in ("ollama", "qwen", "модел", "model")) and any(marker in lowered for marker in ("что сделано", "статус", "runtime", "оптимизац")):
        return _format_project_models_answer()
    return ""


def _answer_project_command(text: str) -> str:
    parts = text.split()
    if len(parts) == 1:
        return _format_project_snapshot_answer()
    command = parts[1]
    if command == "status":
        return _format_project_status_answer()
    if command == "tree":
        return _format_tree_answer()
    if command == "files":
        page = _parse_int(parts[2], default=1) if len(parts) > 2 else 1
        return _format_files_answer(page)
    if command == "dirty":
        return _format_dirty_answer()
    if command == "search" and len(parts) > 2:
        return _format_search_answer(" ".join(parts[2:]))
    if command == "file" and len(parts) > 2:
        page = _parse_int(parts[3], default=1) if len(parts) > 3 else 1
        return _format_file_answer(parts[2], page, intent="PROJECT_FILE")
    if command == "outline" and len(parts) > 2:
        return _format_outline_answer(parts[2])
    if command == "imports":
        return _format_imports_answer(parts[2] if len(parts) > 2 else None)
    if command == "tests":
        return _format_tests_answer()
    if command == "roadmap":
        return _format_roadmap_answer()
    if command == "models":
        return _format_project_models_answer()
    if command == "safety":
        return _format_safety_answer()
    return _format_project_help()


def _format_project_snapshot_answer() -> str:
    model = build_project_workspace_read_model()
    tree_entries = model["top_level_tree"]["entries"][:25]
    return (
        "Project workspace read-only snapshot:\n"
        f"project_root={model['project_root']}\n"
        f"branch={model['git_branch']} head={str(model['git_head'])[:12]}\n"
        f"tracked_file_count={model['tracked_file_count']}\n"
        f"top_level={', '.join(tree_entries)}\n"
        f"dirty={len(model['dirty_files'])} untracked={len(model['untracked_files'])} staged={len(model['staged_files'])}\n"
        "read_only=true direct_execution_allowed=false canonical_write_allowed=false pc_control_allowed=false"
    )


def _format_project_status_answer() -> str:
    status = repo_git_status()
    return (
        "Project git status read-only:\n"
        f"branch={status['branch']} head={str(status['head'])[:12]}\n"
        f"dirty_files={_csv(status['dirty_files']) or 'none'}\n"
        f"untracked_files={_csv(status['untracked_files']) or 'none'}\n"
        f"staged_files={_csv(status['staged_files']) or 'none'}\n"
        f"diff_name_only={_csv(status['diff_name_only']) or 'none'}\n"
        f"diff_stat={status['diff_stat'] or 'none'}\n"
        "read_only=true direct_execution_allowed=false"
    )


def _format_project_structure_grounded_answer() -> str:
    model = build_project_workspace_read_model()
    tree_entries = model["top_level_tree"]["entries"][:35]
    canonical_chain = (
        "tools/jarvis_live_runtime/jarvis_live_chat_launcher.py -> "
        "CONTROL_PLANE/api_server.py -> "
        "MAKSIMAR_SERVER/AI_ORCHESTRATION/jarvis_live_brain_loop_server_adapter.py -> "
        "tools/jarvis_live_runtime/jarvis_live_brain_loop.py -> Ollama"
    )
    return (
        "Да, брат, проверил workspace read-only.\n"
        f"project_root={model['project_root']}\n"
        f"branch={model['git_branch']} head={str(model['git_head'])[:12]}\n"
        f"tracked_file_count={model['tracked_file_count']}\n"
        f"dirty={len(model['dirty_files'])} untracked={len(model['untracked_files'])} staged={len(model['staged_files'])}\n"
        f"top_level={', '.join(tree_entries)}\n"
        f"terminal chat canonical chain={canonical_chain}\n"
        "next_inspect=/project files 1 | /project search <term> | /project file <path> 1\n"
        "read_only=true direct_execution_allowed=false canonical_write_allowed=false pc_control_allowed=false"
    )


def _format_tree_answer() -> str:
    tree = repo_tree()
    return "Project tree page read-only:\n" + "\n".join(f"- {entry}" for entry in tree["entries"][:PROJECT_TREE_MAX_ENTRIES])


def _format_files_answer(page: int) -> str:
    payload = repo_files(page=page)
    lines = [f"Project files page {payload['page']}/{payload['total_pages']} read-only:"]
    lines.extend(f"- {path}" for path in payload["files"])
    return "\n".join(lines)


def _format_dirty_answer() -> str:
    status = repo_git_status()
    return (
        "Project dirty files read-only:\n"
        f"staged={_csv(status['staged_files']) or 'none'}\n"
        f"dirty={_csv(status['dirty_files']) or 'none'}\n"
        f"untracked={_csv(status['untracked_files']) or 'none'}"
    )


def _format_search_answer(query: str) -> str:
    payload = repo_search(query)
    if not payload["results"]:
        return f"Search read-only: query={query}; results=none."
    lines = [f"Search read-only: query={query}; results={payload['result_count']}"]
    for result in payload["results"]:
        lines.append(f"- {result['path']}:{result['line_number']}: {result['line']}")
    return "\n".join(lines)


def _format_project_semantic_search_answer(
    user_text: str,
    tool_route: dict[str, Any] | None = None,
    semantic_query: str | None = None,
    intent_label: str = "PROJECT_SEARCH",
) -> tuple[str, int]:
    route = tool_route or build_retrieval_readonly_tool_route("PROJECT_SEARCH", ("mgrep_readonly", "repo_search"), PROJECT_ROOT).to_read_model()
    mgrep = inspect_mgrep_readonly_availability(PROJECT_ROOT).to_read_model()
    query = semantic_query.strip() if semantic_query and semantic_query.strip() else _semantic_search_query(user_text)
    payload = repo_search(query)
    if not payload["results"] and query != user_text.strip():
        payload = repo_search(user_text.strip())
    path_hits = _project_path_matches(query)
    if not payload["results"]:
        if path_hits:
            lines = [
                f"[work] intent={intent_label}",
                f"primary_tool={route['primary_tool']}",
                f"effective_tool={route['effective_tool']}",
                f"selected_tool_chain={_csv(route['selected_tool_chain'])}",
                f"fallback_tool={route['fallback_tool']}",
                f"fallback_reason={route['fallback_reason']}",
                f"mgrep_source_present={str(mgrep['source_present']).lower()}",
                f"mgrep_usable_now={str(mgrep['usable_now']).lower()}",
                f"Нашёл по именам файлов read-only: query={query}; path_results={len(path_hits)}",
            ]
            lines.extend(f"- {path}" for path in path_hits[:20])
            for path in path_hits[:2]:
                outline = read_file_outline(path)
                if outline.get("allowed"):
                    lines.append(
                        f"outline {path}: imports={_csv(outline['imports']) or 'none'}; "
                        f"classes={_csv(outline['classes']) or 'none'}; "
                        f"functions={_csv(outline['functions'][:12]) or 'none'}"
                    )
            lines.append("read_only=true execution_allowed=false direct_execution_allowed=false")
            return "\n".join(lines), len(path_hits)
        return (
            f"[work] intent={intent_label}\n"
            "Не нашёл подтверждение в текущих read-only источниках.\n"
            f"primary_tool={route['primary_tool']}\n"
            f"effective_tool={route['effective_tool']}\n"
            f"selected_tool_chain={_csv(route['selected_tool_chain'])}\n"
            f"fallback_tool={route['fallback_tool']}\n"
            f"fallback_reason={route['fallback_reason']}\n"
            f"mgrep_source_present={str(mgrep['source_present']).lower()}\n"
            f"mgrep_usable_now={str(mgrep['usable_now']).lower()}\n"
            "checked_tools=mgrep_readonly, repo_search, read_file_snippet, read_file_outline\n"
            f"query={query}",
            0,
        )
    lines = [
        f"[work] intent={intent_label}",
        f"primary_tool={route['primary_tool']}",
        f"effective_tool={route['effective_tool']}",
        f"selected_tool_chain={_csv(route['selected_tool_chain'])}",
        f"fallback_tool={route['fallback_tool']}",
        f"fallback_reason={route['fallback_reason']}",
        f"mgrep_source_present={str(mgrep['source_present']).lower()}",
        f"mgrep_usable_now={str(mgrep['usable_now']).lower()}",
        f"Нашёл по проекту read-only: query={query}; results={payload['result_count']}",
    ]
    paths: list[str] = []
    for result in payload["results"][:12]:
        path = str(result["path"])
        if path not in paths:
            paths.append(path)
        lines.append(f"- {path}:{result['line_number']}: {result['line']}")
    for path in path_hits[:8]:
        if path not in paths:
            paths.append(path)
            lines.append(f"- {path}: path_match")
    for path in paths[:2]:
        outline = read_file_outline(path)
        if outline.get("allowed"):
            lines.append(
                f"outline {path}: imports={_csv(outline['imports']) or 'none'}; "
                f"classes={_csv(outline['classes']) or 'none'}; "
                f"functions={_csv(outline['functions'][:12]) or 'none'}"
            )
    lines.append("read_only=true execution_allowed=false direct_execution_allowed=false")
    return "\n".join(lines), int(payload["result_count"]) + len(path_hits)


def _format_semantic_similarity_answer(
    user_text: str,
    tool_route: dict[str, Any] | None = None,
    semantic_query: str | None = None,
) -> tuple[str, int]:
    route = tool_route or build_retrieval_readonly_tool_route(
        "SEMANTIC_SIMILARITY",
        ("sqlite_vec_readonly", "repo_search", "qdrant_readonly"),
        PROJECT_ROOT,
    ).to_read_model()
    sqlite_vec = inspect_sqlite_vec_readonly_availability(PROJECT_ROOT).to_read_model()
    query = semantic_query.strip() if semantic_query and semantic_query.strip() else _extract_semantic_similarity_query(user_text)
    answer, evidence_count = _format_project_semantic_search_answer(user_text, route, query, "SEMANTIC_SIMILARITY")
    recommendation = (
        "EXTEND existing surface when evidence paths match the requested domain; "
        "otherwise create only a contract/adapter after source review."
    )
    return (
        f"primary_tool={route['primary_tool']}\n"
        f"effective_tool={route['effective_tool']}\n"
        f"selected_tool_chain={_csv(route['selected_tool_chain'])}\n"
        f"fallback_tool={route['fallback_tool']}\n"
        f"fallback_reason={route['fallback_reason']}\n"
        f"sqlite_vec_source_present={str(sqlite_vec['source_present']).lower()}\n"
        f"sqlite_vec_usable_now={str(sqlite_vec['usable_now']).lower()}\n"
        + answer
        + "\nsemantic_duplicate_policy=read_only_repo_search_before_vector_runtime\n"
        + "sqlite_vec_readonly_runtime_enabled=false qdrant_readonly_runtime_enabled=false\n"
        + f"CREATE_EXTEND_ADAPTER_RECOMMENDATION={recommendation}"
    ), evidence_count


def _format_retrieval_backend_status_answer() -> str:
    status = build_retrieval_backend_status_read_model().to_read_model()
    registry = build_retrieval_tool_registry_contract().to_read_model()
    policy = build_retrieval_tool_enablement_policy().to_read_model()
    availability = {
        item.backend_kind: item.to_read_model()
        for item in build_retrieval_runtime_readonly_availability(PROJECT_ROOT)
    }
    lines = [
        "[work] intent=RETRIEVAL_BACKEND_STATUS",
        "primary_tool=qdrant_readonly_status",
        "effective_tool=qdrant_readonly_status",
        "selected_tool_chain=qdrant_readonly_status,retrieval_backend_status_read_model,retrieval_tool_registry_contract",
        "fallback_reason=qdrant source is present but server/container runtime is intentionally disabled",
        "Retrieval backend status read-only:",
        "contract_ready=true",
        "vendor_acquired=true",
        "scan_passed=false",
        f"runtime_enabled={str(status['execution_allowed_now']).lower()}",
        f"read_only_tool_routing_enabled={str(policy['read_only_tool_routing_enabled']).lower()}",
        f"auto_routing_readonly_enabled={str(policy['auto_routing_readonly_enabled']).lower()}",
        f"tool_registered={str(registry['runtime_registration_enabled']).lower()}",
        f"readonly_router_registered={str(registry['readonly_router_registration_enabled']).lower()}",
        f"backend_runtime_enabled={str(policy['backend_runtime_enabled']).lower()}",
        f"auto_routing_runtime_enabled={str(policy['auto_routing_runtime_enabled']).lower()}",
    ]
    for adapter in status["adapter_statuses"]:
        lines.append(
            f"- {adapter['backend_kind']}: contract_mode={adapter['contract_mode']} "
            f"source_of_truth={str(adapter['source_of_truth']).lower()} "
            f"source_ref_required={str(adapter['source_ref_required']).lower()} "
            f"evidence_binding_required={str(adapter['evidence_binding_required']).lower()} "
            f"output_requires_normalization={str(adapter['output_requires_normalization']).lower()} "
            f"execution_allowed_now={str(adapter['execution_allowed_now']).lower()} "
            f"network_allowed_by_default={str(adapter['network_allowed_by_default']).lower()}"
        )
    for backend_kind in ("mgrep", "sqlite_vec", "qdrant"):
        backend = availability[backend_kind]
        lines.append(
            f"- {backend_kind}_runtime_readonly: source_present={str(backend['source_present']).lower()} "
            f"usable_now={str(backend['usable_now']).lower()} selected_tool={backend['selected_tool']} "
            f"fallback_tool={backend['fallback_tool']} unavailable_reason={backend['unavailable_reason']}"
        )
    lines.append("qdrant_network_service_adapter_candidate=true qdrant_server_required_now=false qdrant_container_enabled=false")
    lines.append("read_only=true execution_allowed=false direct_execution_allowed=false canonical_write_allowed=false")
    lines.append("source_ref=MAKSIMAR_CORE_LIB/retrieval_backend/retrieval_backend_status_read_model.py")
    return "\n".join(lines)


def _format_retrieval_vendor_status_answer() -> str:
    policy = build_retrieval_tool_enablement_policy().to_read_model()
    vendor_gate = policy["vendor_gate"]
    lines = [
        "Retrieval vendor/quarantine status read-only:",
        f"vendor_gate_required={str(vendor_gate['vendor_gate_required']).lower()}",
        f"source_verified_required={str(vendor_gate['source_verified_required']).lower()}",
        f"license_review_required={str(vendor_gate['license_review_required']).lower()}",
        f"scanner_required={str(vendor_gate['scanner_required']).lower()}",
        f"runtime_enabled={str(vendor_gate['runtime_enabled']).lower()}",
        "manifest=EXTERNAL_BACKENDS/vendor_quarantine/retrieval_backend_manifest.yaml",
    ]
    for source in vendor_gate["vendor_sources"]:
        lines.append(
            f"- {source['backend_kind']}: source_url={source['source_url']} "
            f"source_status={source['source_status']} scan_status={source['scan_status']} "
            f"vendor_gate_completed={str(source['vendor_gate_completed']).lower()} "
            f"fail_closed_until_source_verified={str(source['fail_closed_until_source_verified']).lower()}"
        )
    lines.append("safe_next_step=run vendor quarantine source/license/scanner gate before any runtime/download/install.")
    return "\n".join(lines)


def _format_retrieval_container_status_answer() -> str:
    contract = read_file_snippet("CONTAINER_DEPLOYMENT/cubes/retrieval_backend/container_contract.yaml", start_line=1, end_line=80)
    profile = read_file_snippet("CONTAINER_DEPLOYMENT/cubes/retrieval_backend/runtime_profile.yaml", start_line=1, end_line=80)
    return (
        "Retrieval container/runtime boundary read-only:\n"
        "container_ready=true runtime_enabled=false docker_required_now=false "
        "qdrant_container_enabled=false network_allowed_by_default=false\n"
        "source_ref=CONTAINER_DEPLOYMENT/cubes/retrieval_backend/container_contract.yaml;"
        "CONTAINER_DEPLOYMENT/cubes/retrieval_backend/runtime_profile.yaml\n"
        f"container_contract_allowed={str(contract.get('allowed', False)).lower()} "
        f"runtime_profile_allowed={str(profile.get('allowed', False)).lower()}\n"
        "safe_next_step=keep runtime disabled until a later explicit runtime batch approves service/network/container execution."
    )


def _format_source_evidence_answer(user_text: str) -> tuple[str, int]:
    query = _semantic_search_query(user_text)
    if query == "jarvis":
        query = "source_ref evidence_binding evidence_id trace_id"
    answer, evidence_count = _format_project_semantic_search_answer(query)
    if evidence_count == 0:
        return (
            "Evidence missing: no source/evidence hit was found in read-only repo search. "
            "needed_tool=repo_search/read_file_snippet safe_next_step=ask for a narrower file, contract, or trace id.",
            0,
        )
    return answer + "\nsource_bound=true hallucination_allowed=false", evidence_count


def _format_auto_tool_use_status_answer() -> str:
    policy = build_retrieval_tool_enablement_policy().to_read_model()
    return (
        "Automatic read-only tool routing status:\n"
        "semantic_classifier=enabled_in_existing_router\n"
        f"intent_groups={_csv(policy['semantic_intent_groups'])}\n"
        "read_only_first=true free_generation_after_tool_check=true\n"
        f"runtime_tool_execution_enabled={str(policy['runtime_tool_execution_enabled']).lower()} "
        f"auto_routing_runtime_enabled={str(policy['auto_routing_runtime_enabled']).lower()} "
        "direct_execution_allowed=false pc_control_allowed=false canonical_write_allowed=false"
    )


def _format_file_answer(path: str, page: int, intent: str = "PROJECT_FILE") -> str:
    payload = read_file_snippet(path, page=page)
    if not payload.get("allowed"):
        return (
            f"[work] intent={intent}\n"
            "primary_tool=read_file_snippet\n"
            "effective_tool=read_file_snippet\n"
            "selected_tool_chain=read_file_snippet,read_file_outline,repo_files\n"
            f"fallback_reason={payload.get('error', 'unknown')}\n"
            f"File snippet denied: path={path}; error={payload.get('error', 'unknown')}; "
            "read_only=true execution_allowed=false"
        )
    lines = [
        f"[work] intent={intent}",
        "primary_tool=read_file_snippet",
        "effective_tool=read_file_snippet",
        "selected_tool_chain=read_file_snippet,read_file_outline,repo_files",
        "fallback_reason=exact filename resolved before Ollama fallback",
        f"File snippet read-only: {path} page={payload['page']} lines={payload['start_line']}-{payload['end_line']}",
    ]
    lines.extend(payload["snippet"])
    lines.append("read_only=true execution_allowed=false")
    return "\n".join(lines)


def _format_outline_answer(path: str) -> str:
    payload = read_file_outline(path)
    if not payload.get("allowed"):
        return f"File outline denied: path={path}; error={payload.get('error', 'unknown')}; read_only=true."
    return (
        f"File outline read-only: {path}; line_count={payload['line_count']}\n"
        f"imports={_csv(payload['imports']) or 'none'}\n"
        f"classes={_csv(payload['classes']) or 'none'}\n"
        f"functions={_csv(payload['functions']) or 'none'}\n"
        f"constants={_csv(payload['constants']) or 'none'}"
    )


def _format_imports_answer(path: str | None) -> str:
    payload = repo_import_graph(path=path)
    lines = [f"Import graph read-only: edges={payload['edge_count']}"]
    lines.extend(f"- {edge['from']} -> {edge['to']}" for edge in payload["edges"])
    return "\n".join(lines)


def _format_tests_answer() -> str:
    tests = [path for path in _tracked_project_files() if path.startswith("tests/") and path.endswith(".py")]
    groups = _domain_groups_for_paths(tuple(tests))
    lines = [f"Project tests read-only: test_file_count={len(tests)}"]
    for group, paths in groups.items():
        if paths:
            lines.append(f"- {group}: {len(paths)} files; sample={', '.join(paths[:6])}")
    return "\n".join(lines)


def _format_roadmap_answer() -> str:
    status = status_tools()
    return (
        "Roadmap/status read-only:\n"
        f"jarvis_live_ci_status:\n{status.get('jarvis_live_ci_status', '')}\n"
        f"roadmap_post_step_drift_check:\n{status.get('roadmap_post_step_drift_check', '')}"
    )


def _format_project_models_answer() -> str:
    status = model_runtime_status()
    return (
        "Ollama/model runtime read-only:\n"
        "canonical_chain=chat launcher -> CONTROL_PLANE/api_server.py -> "
        "jarvis_live_brain_loop_server_adapter.py -> jarvis_live_brain_loop.py -> Ollama\n"
        "Ollama is local model engine on localhost:11434, not a second JARVIS server.\n"
        "tool_calls are proposals/requests only; actual execution must go through CONTROL_PLANE capability/approval/action adapter/audit.\n"
        "future_adapter_scope=/api/chat, think control, tool_calls, structured JSON, /api/ps, /api/tags, /api/show, keep_alive, embeddings later\n"
        f"ollama_version={status.get('ollama_version') or 'unavailable'}\n"
        f"ollama_tags={status.get('ollama_tags') or 'unavailable'}\n"
        f"ollama_ps={status.get('ollama_ps') or 'unavailable'}\n"
        f"ollama_show_primary_model={status.get('ollama_show_primary_model') or 'unavailable'}\n"
        f"nvidia_smi={status.get('nvidia_smi') or 'unavailable'}\n"
        f"free_h={status.get('free_h') or 'unavailable'}\n"
        "pc_control_allowed=false direct_execution_allowed=false model_download_allowed=false_from_chat"
    )


def _format_memory_history_grounded_answer(user_text: str, context: JarvisBrainContext) -> tuple[str, int]:
    checked = [
        "stable_style_profile",
        "session_memory",
        "local_chat_memory",
        "memory_engine_registry",
        "runtime_history_store",
        "history_query",
        "mempalace_read_only_sandbox",
    ]
    evidence: list[str] = []
    query_terms = _memory_query_terms(user_text)
    if context.rolling_summary.strip():
        evidence.append(f"session_summary: {context.rolling_summary.strip()}")
    for turn in context.recent_turns[-6:]:
        text = str(turn.get("text", "")).strip()
        if text and text != context.user_text.strip():
            evidence.append(f"session_turn/{turn.get('role', '')}: {text[:260]}")
    evidence.extend(context.local_chat_memory_snippets[:4])
    evidence.extend(context.retrieved_snippets[:6])
    if not evidence:
        history_snippets = _retrieve_history_snippets(user_text, deep=True)
        evidence.extend(history_snippets[:6])
    if query_terms:
        evidence = [item for item in evidence if any(term in item.casefold() for term in query_terms)]
    if not evidence:
        return (
            "Не нашёл подтверждение в текущих read-only источниках.\n"
            f"checked_sources={', '.join(checked)}\n"
            "imported_gpt_history=unavailable_or_no_match\n"
            "canonical_memory_write_allowed=false",
            0,
        )
    lines = [
        "Проверил память/историю read-only.",
        f"checked_sources={', '.join(checked)}",
        f"evidence_count={len(evidence)}",
    ]
    lines.extend(f"- {item}" for item in evidence[:8])
    lines.append("canonical_memory_write_allowed=false direct_global_memory_write=false")
    return "\n".join(lines), len(evidence)


def _format_safety_answer() -> str:
    terms = ("runtime_mutation_allowed", "direct_execution_allowed", "approval", "pc_control_allowed", "watchdog", "core guard", "OOB", "safety", "security")
    results: list[dict[str, Any]] = []
    seen: set[tuple[str, int]] = set()
    for term in terms:
        for result in repo_search(term, max_results=8)["results"]:
            key = (str(result["path"]), int(result["line_number"]))
            if key in seen:
                continue
            seen.add(key)
            results.append(result)
            if len(results) >= 30:
                break
        if len(results) >= 30:
            break
    lines = ["Safety/security surfaces read-only:"]
    if results:
        lines.extend(f"- {result['path']}:{result['line_number']}: {result['line']}" for result in results)
    else:
        lines.append("- no direct matches found in bounded search")
    lines.append("direct_execution_allowed=false canonical_write_allowed=false pc_control_allowed=false")
    return "\n".join(lines)


def _format_action_request_proposal_answer(user_text: str) -> str:
    lowered = user_text.casefold()
    action_family = "generic_action"
    if any(marker in lowered for marker in ("коммит", "commit", "git commit")):
        action_family = "git_commit"
    elif any(marker in lowered for marker in ("тест", "pytest", "провер")):
        action_family = "test_run"
    elif any(marker in lowered for marker in ("скачай", "установ", "install", "download", "n8n", "модель")):
        action_family = "download_or_install"
    elif _asks_pc_action(lowered):
        action_family = "pc_control"
    return (
        "Operator proposal only. Я не буду утверждать, что действие выполнено, пока нет tool_result.\n"
        f"requested_action={user_text.strip()[:240]}\n"
        f"action_family={action_family}\n"
        "execution_allowed=false approval_required=true proposal_only=true\n"
        "allowed_next_step=подготовить patch/plan через существующий capability/approval/action adapter\n"
        "pc_control_allowed=false shell_execution_enabled=false direct_execution_allowed=false "
        "canonical_write_allowed=false deployment_allowed_now=false"
    )


def _format_tool_catalog_answer(catalog: dict[str, Any]) -> str:
    read_only = str(bool(catalog.get("read_only", True))).lower()
    execution_allowed = str(bool(catalog.get("execution_allowed", False))).lower()
    mgrep = catalog.get("mgrep_status", {})
    sqlite_vec = catalog.get("sqlite_vec_status", {})
    qdrant = catalog.get("qdrant_status", {})
    lines = [
        "[work] intent=TOOL_CATALOG "
        "tools=build_jarvis_live_tool_catalog_read_model,inspect_mgrep_readonly_availability,"
        "inspect_sqlite_vec_readonly_availability,inspect_qdrant_readonly_availability "
        f"read_only={read_only} execution_allowed={execution_allowed}",
        "Project / repo read-only:",
    ]
    for tool in catalog.get("project_repo_read_only_tools", ()):
        lines.append(f"- {tool} status=available read_only")
    lines.extend(
        (
            "Retrieval read-only:",
            f"- mgrep_readonly status=read_only usable_now={str(bool(mgrep.get('usable_now', False))).lower()} "
            f"source_present={str(bool(mgrep.get('source_present', False))).lower()} "
            f"effective_status={mgrep.get('selected_tool', 'repo_search')}",
            f"- sqlite_vec_readonly status=read_only usable_now={str(bool(sqlite_vec.get('usable_now', False))).lower()} "
            f"source_present={str(bool(sqlite_vec.get('source_present', False))).lower()} "
            f"effective_status={sqlite_vec.get('selected_tool', 'repo_search')}",
            f"- qdrant_readonly_status status=read_only usable_now={str(bool(qdrant.get('usable_now', False))).lower()} "
            f"source_present={str(bool(qdrant.get('source_present', False))).lower()} "
            f"effective_status={qdrant.get('selected_tool', 'qdrant_readonly_status')}",
            "- retrieval_backend_status_read_model status=available read_only",
            "- retrieval_tool_registry_contract status=available read_only",
            "Memory / history read-only:",
        )
    )
    for tool in catalog.get("memory_history_read_only_tools", ()):
        lines.append(f"- {tool} status=available read_only")
    lines.extend(
        (
            f"- memory_engine_registry status=available read_only definitions={catalog.get('memory_definition_count', 0)}",
            "Model/status read-only:",
        )
    )
    for tool in catalog.get("model_status_read_only_tools", ()):
        lines.append(f"- {tool} status=available read_only")
    lines.extend(
        (
            "Roadmap / safety read-only:",
        )
    )
    for tool in catalog.get("roadmap_safety_read_only_tools", ()):
        lines.append(f"- {tool} status=available read_only")
    lines.extend(
        (
            f"- roadmap_status status=available read_only drift_check_wired={str(bool(catalog.get('all_existing_read_tools_connected', True))).lower()}",
            "External adapters (runtime-grounded):",
        )
    )
    for adapter in catalog.get("external_adapter_runtime_status", ()):
        if not isinstance(adapter, dict):
            continue
        lines.append(
            f"- {adapter.get('tool_id', '')} status={adapter.get('availability_status', 'unknown')} "
            f"selection_enabled={str(bool(adapter.get('selection_enabled', False))).lower()} "
            f"import_probe_passed={str(bool(adapter.get('import_probe_worked', False))).lower()} "
            f"package={adapter.get('runtime_package_name', '') or adapter.get('package_name', '')} "
            f"import={adapter.get('runtime_import_name', '') or adapter.get('import_name', '')} "
            f"blocked_reason={adapter.get('activation_blocked_reason', '') or 'none'}"
        )
    lines.extend(
        (
            f"external_adapter_tools={_csv(catalog.get('external_adapter_tools', ())) or 'none'}",
            f"external_adapter_unavailable={_csv(catalog.get('external_adapter_unavailable_tools', ())) or 'none'}",
            f"external_adapter_legacy={_csv(catalog.get('external_adapter_legacy_tools', ())) or 'none'}",
            "Action tools:",
        )
    )
    for tool in catalog.get("action_proposal_only_tools", ()):
        lines.append(f"- {tool} status=proposal_only disabled")
    lines.extend(
        (
            f"mgrep_usable_now={str(bool(mgrep.get('usable_now', False))).lower()}",
            f"sqlite_vec_usable_now={str(bool(sqlite_vec.get('usable_now', False))).lower()}",
            f"qdrant_server_runtime_enabled={str(bool(catalog.get('qdrant_server_runtime_enabled', False))).lower()}",
            f"active_retrieval_surfaces={_csv(catalog.get('active_retrieval_surfaces', ())) or 'none'}",
            f"sandbox_only_memory_surfaces={_csv(catalog.get('sandbox_only_memory_surfaces', ())) or 'none'}",
            f"disabled_memory_surfaces={_csv(catalog.get('disabled_memory_surfaces', ())) or 'none'}",
            f"enterprise_memory_preview_ready={str(bool(catalog.get('enterprise_memory_preview_ready', False))).lower()}",
            f"regulatory_routing_preview_ready={str(bool(catalog.get('regulatory_routing_preview_ready', False))).lower()}",
            f"mempalace_routing_ready={str(bool(catalog.get('mempalace_routing_ready', False))).lower()}",
            "direct_execution_allowed=false",
            "canonical_write_allowed=false",
            "pc_control_allowed=false",
            "shell_execution_enabled=false",
            "direct_execution_allowed=false",
            "execution_allowed=false",
        )
    )
    return "\n".join(lines)


def _format_agent_catalog_answer(catalog: dict[str, Any]) -> str:
    lines = [
        "[work] intent=AGENT_CATALOG tools=build_jarvis_agent_catalog_read_model read_only=true execution_allowed=false",
        "Grounded agent catalog:",
    ]
    for agent in catalog.get("agents", ()):
        if not isinstance(agent, dict):
            continue
        lines.append(
            f"- {agent.get('role_id', '')} capabilities={_csv(agent.get('allowed_capabilities', ())) or 'none'} "
            f"may_route={str(bool(agent.get('may_route', False))).lower()} "
            f"may_propose={str(bool(agent.get('may_propose', False))).lower()}"
        )
    lines.extend(
        (
            f"required_grounded_agents={_csv(catalog.get('required_grounded_agents', ())) or 'none'}",
            "external_adapter_selector_agent=not_present_in_canonical_swarm_roles",
            "direct_execution_allowed=false",
            "canonical_write_allowed=false",
            "pc_control_allowed=false",
        )
    )
    return "\n".join(lines)


def _format_skill_visibility_answer(visibility: dict[str, Any]) -> str:
    lines = [
        "[work] intent=SKILL_VISIBILITY tools=build_jarvis_skill_visibility_read_model,build_jarvis_live_tool_catalog_read_model "
        "read_only=true execution_allowed=false",
        "Project workspace tools:",
    ]
    for tool in visibility.get("project_workspace_tools", ()):
        lines.append(f"- {tool} status=available read_only")
    lines.append("Repo read/search/outline/import graph:")
    for tool in visibility.get("repo_introspection_tools", ()):
        lines.append(f"- {tool} status=available read_only")
    lines.append("Memory/history/retrieval:")
    for tool in visibility.get("memory_retrieval_tools", ()):
        lines.append(f"- {tool} status=available read_only")
    lines.append("Tests/roadmap/drift:")
    for tool in visibility.get("tests_roadmap_drift_tools", ()):
        lines.append(f"- {tool} status=available read_only")
    lines.append("Model/runtime status:")
    for tool in visibility.get("model_runtime_tools", ()):
        lines.append(f"- {tool} status=available read_only")
    lines.append("External adapters:")
    for adapter in visibility.get("external_adapter_statuses", ()):
        if not isinstance(adapter, dict):
            continue
        lines.append(
            f"- {adapter.get('tool_id', '')} status={adapter.get('availability_status', 'unknown')} "
            f"selection_enabled={str(bool(adapter.get('selection_enabled', False))).lower()} "
            f"import_probe_passed={str(bool(adapter.get('import_probe_worked', False))).lower()}"
        )
    lines.append("Action proposals:")
    for tool in visibility.get("action_proposal_tools", ()):
        lines.append(f"- {tool} status=proposal_only disabled")
    lines.extend(
        (
            f"visible_agents={_csv(visibility.get('visible_agents', ())) or 'none'}",
            f"external_adapter_tools={_csv(visibility.get('external_adapter_tools', ())) or 'none'}",
            f"external_adapter_unavailable={_csv(visibility.get('external_adapter_unavailable_tools', ())) or 'none'}",
            "PC-control status:",
            f"- windows_gui_bridge_enabled={str(bool(visibility.get('windows_gui_bridge_enabled', False))).lower()}",
            f"- pc_control_allowed={str(bool(visibility.get('pc_control_allowed', False))).lower()}",
            "direct_execution_allowed=false",
            "canonical_write_allowed=false",
        )
    )
    return "\n".join(lines)


def _format_project_atlas_answer() -> str:
    model = build_project_workspace_read_model()
    groups = model["domain_groups"]
    lines = [
        "Не буду dump'ить весь репозиторий в один ответ. Даю read-only atlas и команды пагинации.",
        f"project_root={model['project_root']}",
        f"tracked_file_count={model['tracked_file_count']}",
    ]
    for group, paths in groups.items():
        if paths:
            lines.append(f"- {group}: {len(paths)} files; sample={', '.join(paths[:5])}")
    lines.extend((
        "Дальше смотри страницами:",
        "/project files 1",
        "/project files 2",
        "/project search <term>",
        "/project file <path> <page>",
    ))
    return "\n".join(lines)


def _format_project_help() -> str:
    return (
        "Project commands: /project, /project status, /project tree, /project files <page>, "
        "/project dirty, /project search <query>, /project file <path> <page>, "
        "/project outline <path>, /project imports <path>, /project tests, /project roadmap, "
        "/project models, /project safety"
    )


def _answer_project_workspace_summary_if_grounded(context: JarvisBrainContext) -> str:
    if not _asks_project_workspace_summary(context.user_text.casefold()):
        return ""
    tracked = _tracked_project_files()
    top_entries = _top_level_entries_from_tracked_files(tracked) if tracked else ()
    visible_top = tuple(
        entry.rstrip("/")
        for entry in top_entries
        if entry.rstrip("/") in {"CONTROL_PLANE", "MAKSIMAR_SERVER", "MAKSIMAR_CORE_LIB", "tools", "tests", "runtime_history_store"}
    )
    if not visible_top:
        visible_top = ("CONTROL_PLANE", "MAKSIMAR_SERVER", "MAKSIMAR_CORE_LIB", "tools", "tests")
    canonical_files = tuple(path for path in PROJECT_VISIBILITY_KEY_FILES if (PROJECT_ROOT / path).exists())
    if not canonical_files:
        return ""
    chain = (
        "tools/jarvis_live_runtime/jarvis_live_chat_launcher.py -> "
        "CONTROL_PLANE/api_server.py -> "
        "MAKSIMAR_SERVER/AI_ORCHESTRATION/jarvis_live_brain_loop_server_adapter.py -> "
        "tools/jarvis_live_runtime/jarvis_live_brain_loop.py -> Ollama"
    )
    support_files = (
        "tools/jarvis_live_runtime/jarvis_live_terminal_chat.py, "
        "tools/jarvis_live_runtime/jarvis_personality_policy.py, "
        "tools/jarvis_live_runtime/jarvis_live_response_mode.py"
    )
    tracked_text = f"; tracked_file_count={len(tracked)}" if tracked else ""
    return (
        "Да, брат, вижу проект в read-only режиме. "
        f"Корень: {PROJECT_ROOT}{tracked_text}. "
        f"По верхнему уровню вижу: {', '.join(visible_top)}. "
        f"Ядро terminal chat сейчас идет так: {chain}. "
        f"За интерфейс, стиль и режимы ответа отвечают: {support_files}. "
        "Я могу читать дерево проекта и bounded snippets файлов, но не пишу в ядро, "
        "не выполняю команды и не управляю ПК: "
        "project_workspace_read_enabled=true, project_tree_read_enabled=true, "
        "project_file_read_enabled=true, direct_execution_allowed=false, "
        "canonical_write_allowed=false, pc_control_allowed=false."
    )


def _asks_project_workspace_summary(lowered: str) -> bool:
    project_markers = (
        "структур",
        "дерево",
        "что ты видишь по проекту",
        "ядро terminal chat",
        "terminal chat chain",
        "project workspace",
        "файлы проекта",
        "структура ядра",
    )
    return any(marker in lowered for marker in project_markers)


def _extract_semantic_similarity_query(user_text: str) -> str:
    text = user_text.strip()
    lowered = text.casefold()
    patterns = (
        r"^(?:найди\s+)?похож[еаы]?[йя]?\s+на\s+",
        r"^семантически\s+",
        r"^по\s+смыслу\s+",
        r"^semantic\s+similarity\s+",
        r"^semantic\s+",
        r"^similar\s+to\s+",
        r"^related\s+to\s+",
        r"^similar\s+",
    )
    for pattern in patterns:
        candidate = re.sub(pattern, "", text, flags=re.IGNORECASE).strip(" ,.;:!?-")
        if candidate != text and candidate:
            return candidate
    for trigger in ("найди похожее на", "похожее на", "похожие на"):
        if trigger in lowered:
            index = lowered.index(trigger) + len(trigger)
            candidate = text[index:].strip(" ,.;:!?-")
            if candidate:
                return candidate
    return _semantic_search_query(user_text)


def _semantic_search_query(user_text: str) -> str:
    lowered = user_text.casefold()
    filename = _extract_filename_token(user_text)
    if filename:
        return filename
    direct_queries = (
        ("source_ref", "source_ref"),
        ("source-ref", "source_ref"),
        ("source ref", "source_ref"),
        ("evidence_binding", "evidence_binding"),
        ("evidence-binding", "evidence_binding"),
        ("evidence binding", "evidence_binding"),
        ("source_of_truth", "source_of_truth"),
        ("network_allowed_by_default", "network_allowed_by_default"),
        ("runtime_mutation_allowed", "runtime_mutation_allowed"),
        ("direct_execution_allowed", "direct_execution_allowed"),
        ("vendor_gate_required", "vendor_gate_required"),
    )
    for marker, query in direct_queries:
        if marker in lowered:
            return query
    known_queries = (
        ("terminal chat", "terminal_chat jarvis_live_terminal_chat"),
        ("brain_loop", "jarvis_live_brain_loop"),
        ("n8n", "n8n adapter vendor gate sandbox"),
        ("голос", "voice jarvis live voice"),
        ("voice", "voice jarvis live voice"),
        ("памят", "memory local_chat runtime_history_store"),
        ("memory", "memory local_chat runtime_history_store"),
        ("core guard", "core guard watchdog safety"),
        ("watchdog", "watchdog core guard safety"),
        ("ollama", "ollama qwen model runtime"),
        ("qwen", "ollama qwen model runtime"),
        ("tool", "tool adapter capability approval"),
        ("adapter", "adapter capability approval"),
        ("адаптер", "adapter capability approval"),
        ("автоматизац", "workflow automation n8n adapter"),
        ("retrieval", "retrieval_backend retrieval tool contract status read model"),
        ("qdrant", "qdrant_adapter_contract qdrant_server_required_now qdrant_container_enabled"),
        ("sqlite", "sqlite_vec_adapter_contract sqlite_vec_readonly"),
        ("mgrep", "mgrep_adapter_contract mgrep_readonly"),
        ("source_ref", "source_ref evidence_binding evidence_id trace_id"),
        ("evidence", "source_ref evidence_binding evidence_id trace_id"),
        ("container", "container_contract runtime_profile runtime_enabled docker_required_now"),
        ("docker", "container_contract runtime_profile docker_required_now"),
        ("vendor", "vendor_gate retrieval_backend_manifest vendor_quarantine"),
    )
    for marker, query in known_queries:
        if marker in lowered:
            return query
    cleaned = user_text.strip()
    return cleaned[:120] if cleaned else "jarvis"


def _project_path_matches(query: str, max_results: int = 20) -> tuple[str, ...]:
    terms = tuple(term for term in _query_tokens(query) if term not in {"где", "найди", "поиск"})
    if not terms:
        return ()
    matches: list[str] = []
    for path in _tracked_project_files():
        lowered = path.casefold()
        if any(term in lowered for term in terms):
            matches.append(path)
        if len(matches) >= max_results:
            break
    return tuple(matches)


def _query_tokens(text: str) -> tuple[str, ...]:
    return tuple(part for part in text.casefold().replace("?", " ").replace(",", " ").split() if len(part) >= 4)


def _format_section(title: str, value: str) -> str:
    return f"{title}:\n{value}" if value else ""


def _format_list(title: str, values: tuple[str, ...]) -> str:
    if not values:
        return ""
    return title + ":\n" + "\n".join(f"- {value}" for value in values)


def _parse_int(value: Any, default: int) -> int:
    try:
        return int(str(value))
    except (TypeError, ValueError):
        return default


def _csv(value: Any) -> str:
    if isinstance(value, (list, tuple)):
        return ", ".join(str(item) for item in value)
    return str(value)
