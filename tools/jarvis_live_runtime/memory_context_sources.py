from __future__ import annotations

from pathlib import Path
from typing import Any

from MAKSIMAR_CORE_LIB.memory_engine.history_ingestion.jarvis_history_query_models import (
    JarvisHistoryQuery,
)
from MAKSIMAR_CORE_LIB.memory_engine.history_ingestion.jarvis_history_query_reader import (
    run_jarvis_history_query,
)
from MAKSIMAR_CORE_LIB.memory_engine.memory_accessor import list_memory_definitions
from MAKSIMAR_CORE_LIB.enterprise_memory_domains.enterprise_memory_preview_builder import (
    build_enterprise_memory_preview,
)
from MAKSIMAR_SERVER.REGULATORY_MEMORY_FOUNDATION.regulatory_routing_preview_builder import (
    build_regulatory_routing_preview,
)
from MAKSIMAR_SERVER.CONTROL_PLANE.memory_routing.adapters.mempalace_read_only_routing_integration import (
    build_mempalace_read_only_routing_integration_preview,
)
from tools.jarvis_live_runtime.project_workspace_tools import (
    MAX_PROJECT_FILE_SNIPPETS,
    PROJECT_ROOT,
    _project_tree_summary,
    _read_project_file_snippet,
    _select_project_files_for_context,
)
from tools.jarvis_live_runtime.session_memory_store import (
    SESSION_STATE_PATH,
    _read_recent_local_chat_records,
    _session_turn_log_path,
)


RUNTIME_HISTORY_STORE = PROJECT_ROOT / "runtime_history_store"
RUNTIME_VECTOR_INDEX_ROOT = Path.home() / "MAKSIMAR_RUNTIME" / "runtime_vector_indexes"
RUNTIME_EMBEDDINGS_ROOT = Path.home() / "MAKSIMAR_RUNTIME" / "runtime_embeddings"
RUNTIME_RETRIEVAL_ROOT = Path.home() / "MAKSIMAR_RUNTIME" / "runtime_retrieval"

MAX_LOCAL_CHAT_MEMORY_SNIPPETS = 4


def _query_tokens(text: str) -> tuple[str, ...]:
    return tuple(
        part
        for part in text.casefold().replace("?", " ").replace(",", " ").split()
        if len(part) >= 4
    )


def _compact_text(text: str, source: Path) -> str:
    single_line = " ".join(text.split())
    return f"{source}: {single_line[:700]}"


def _memory_query_terms(user_text: str) -> tuple[str, ...]:
    ignored = {
        "джарвис",
        "jarvis",
        "помнишь",
        "обсуждали",
        "переписке",
        "переписка",
        "говорил",
        "просил",
        "было",
        "были",
        "что",
        "про",
        "мой",
        "моя",
    }
    terms = [term for term in _query_tokens(user_text) if term not in ignored]
    if "голос" in terms and "voice" not in terms:
        terms.append("voice")
    if "gpt" in user_text.casefold() and "gpt" not in terms:
        terms.append("gpt")
    return tuple(dict.fromkeys(terms))


def _asks_style_memory_recall(lowered: str) -> bool:
    recall_markers = ("помнишь", "ты помнишь", "напомни", "как я хочу", "какой стиль")
    style_markers = ("общал", "общаться", "стиль", "говорил", "говорить", "отвечал", "отвечать")
    return any(marker in lowered for marker in recall_markers) and any(marker in lowered for marker in style_markers)


def _asks_memory_recall(lowered: str) -> bool:
    return any(marker in lowered for marker in ("помнишь", "ты помнишь", "что я говорил", "что я просил"))


def _has_stored_memory_for_recall(context: Any) -> bool:
    user_text = str(getattr(context, "user_text", "")).strip()

    previous_turns = []
    for turn in getattr(context, "recent_turns", ()):
        turn_text = str(turn.get("text", "")).strip() if isinstance(turn, dict) else ""
        if turn_text and turn_text != user_text:
            previous_turns.append(turn_text)

    stored_chunks: list[str] = []
    stored_chunks.extend(previous_turns)

    rolling_summary = str(getattr(context, "rolling_summary", "")).strip()
    if rolling_summary:
        stored_chunks.append(rolling_summary)

    stored_chunks.extend(str(item) for item in getattr(context, "local_chat_memory_snippets", ()))
    stored_chunks.extend(str(item) for item in getattr(context, "retrieved_snippets", ()))

    stored_text = " ".join(stored_chunks).casefold()
    if not stored_text.strip():
        return False

    query_terms = tuple(term for term in _memory_query_terms(user_text) if len(term) >= 4)
    if query_terms:
        return any(term in stored_text for term in query_terms)

    return True


def _retrieve_history_snippets(user_text: str, deep: bool) -> list[str]:
    snippets: list[str] = []
    try:
        query = JarvisHistoryQuery(
            query_text=user_text,
            query_scope="project_history",
            query_ready=True,
        )
        result = run_jarvis_history_query(query)
        titles = tuple(str(title) for title in result.get("matched_titles", ()))
        snippets.extend(f"history_query_match: {title}" for title in titles[:3])
    except (ValueError, KeyError, TypeError):
        pass
    if not RUNTIME_HISTORY_STORE.exists():
        return snippets
    tokens = _query_tokens(user_text)
    records = sorted(RUNTIME_HISTORY_STORE.glob("normalized_history/conversations/*/normalized_record.json"))
    for record_path in records[:120]:
        try:
            text = record_path.read_text(encoding="utf-8", errors="replace")
        except OSError:
            continue
        lowered = text.casefold()
        if tokens and not any(token in lowered for token in tokens):
            continue
        snippets.append(_compact_text(text, source=record_path))
        if len(snippets) >= (6 if deep else 3):
            break
    return snippets


def _retrieve_project_workspace_snippets(user_text: str, deep: bool) -> list[str]:
    if not _needs_project_visibility(user_text):
        return []
    snippets = [_project_tree_summary()]
    for path in _select_project_files_for_context(user_text, deep=deep):
        snippet = _read_project_file_snippet(path)
        if snippet:
            snippets.append(snippet)
        if len(snippets) >= MAX_PROJECT_FILE_SNIPPETS + 1:
            break
    return snippets


def _retrieve_memory_engine_snippets(user_text: str) -> list[str]:
    tokens = _query_tokens(user_text)
    try:
        definitions = list_memory_definitions()
    except Exception:
        return []
    snippets: list[str] = []
    for definition in definitions[:300]:
        entity_id = str(getattr(definition, "entity_id", ""))
        if tokens and not any(token in entity_id.casefold() for token in tokens):
            continue
        version = str(getattr(definition, "version", ""))
        snippets.append(f"memory_engine_registry: entity_id={entity_id}; version={version}")
        if len(snippets) >= 3:
            break
    return snippets


def _retrieve_enterprise_memory_snippets(user_text: str) -> list[str]:
    lowered = user_text.casefold()
    if not any(marker in lowered for marker in ("суверенн", "sovereign", "business", "sales", "продаж", "enterprise", "tenant")):
        return []
    try:
        preview = build_enterprise_memory_preview()
    except Exception:
        return []
    return [
        "enterprise_business_memory: "
        f"preview_ready={preview.get('preview_ready')}; "
        f"tenant_scopes={preview.get('tenant_scopes')}; "
        f"business_ids={preview.get('business_ids')}; "
        f"policy_record_ids={preview.get('policy_record_ids')}; "
        f"runtime_policy_binding_allowed={preview.get('runtime_policy_binding_allowed')}; "
        "read_only=true"
    ]


def _retrieve_regulatory_memory_snippets(user_text: str) -> list[str]:
    lowered = user_text.casefold()
    if not any(marker in lowered for marker in ("закон", "law", "regulatory", "compliance", "юрисдик", "jurisdiction", "tenant")):
        return []
    try:
        preview = build_regulatory_routing_preview()
    except Exception:
        return []
    return [
        "regulatory_memory_foundation: "
        f"preview_ready={preview.get('preview_ready')}; "
        f"route_count={preview.get('route_count')}; "
        f"tenant_scope_required={preview.get('tenant_scope_required')}; "
        f"jurisdiction_scope_required={preview.get('jurisdiction_scope_required')}; "
        f"read_only={preview.get('read_only')}; "
        f"runtime_mutation_allowed={preview.get('runtime_mutation_allowed')}; "
        f"direct_core_write_allowed={preview.get('direct_core_write_allowed')}"
    ]


def _retrieve_vector_memory_snippets(user_text: str) -> list[str]:
    lowered = user_text.casefold()
    if not any(marker in lowered for marker in ("vector", "embedding", "индекс", "retrieval", "rag")):
        return []
    existing_roots = tuple(
        str(path)
        for path in (RUNTIME_VECTOR_INDEX_ROOT, RUNTIME_EMBEDDINGS_ROOT, RUNTIME_RETRIEVAL_ROOT)
        if path.exists()
    )
    if not existing_roots:
        return []
    return [
        "vector_memory: runtime vector/embedding roots detected; "
        f"roots={existing_roots}; query_helper=not_connected; canonical_write_allowed=false"
    ]


def _retrieve_mempalace_status_snippets(user_text: str) -> list[str]:
    if "mempalace" not in user_text.casefold():
        return []
    status = _mempalace_status()
    try:
        preview = build_mempalace_read_only_routing_integration_preview()
    except Exception:
        preview = {}
    return [
        "mempalace_read_only_sandbox: "
        f"status={status}; "
        f"read_only_routing_enabled={preview.get('read_only_routing_enabled', False)}; "
        f"routing_integration_ready={preview.get('routing_integration_ready', False)}; "
        f"canonical_write_allowed={preview.get('canonical_write_allowed', False)}; "
        f"runtime_mutation_allowed={preview.get('runtime_mutation_allowed', False)}; "
        f"query_domains={preview.get('query_domains', ())}"
    ]


def _retrieve_local_chat_memory_snippets(user_text: str, state: dict[str, Any]) -> tuple[str, ...]:
    snippets: list[str] = []
    tokens = _query_tokens(user_text)
    rolling_summary = str(state.get("rolling_summary", "")).strip()
    if rolling_summary:
        snippets.append(f"session_summary: {rolling_summary[:500]}")
    for record in _read_recent_local_chat_records(limit=24):
        text = " ".join(
            str(record.get(key, ""))
            for key in ("user_message", "jarvis_answer", "turn_summary", "active_task")
        ).casefold()
        if tokens and not any(token in text for token in tokens):
            continue
        snippets.append(
            "local_chat_memory: "
            f"day={record.get('day_bucket', '')}; "
            f"user={str(record.get('user_message', ''))[:180]}; "
            f"jarvis={str(record.get('jarvis_answer', ''))[:180]}"
        )
        if len(snippets) >= MAX_LOCAL_CHAT_MEMORY_SNIPPETS:
            break
    return tuple(snippets[:MAX_LOCAL_CHAT_MEMORY_SNIPPETS])


def _build_memory_surface_inventory() -> tuple[dict[str, Any], ...]:
    return (
        _surface("session_memory", "session-runtime", str(SESSION_STATE_PATH), "usable_now", ()),
        _surface("local_chat_memory", "append-only local chat/session memory", str(_session_turn_log_path()), "usable_now" if _session_turn_log_path().exists() else "usable_now", ("tests/jarvis_live_runtime/test_jarvis_live_memory_federation_smoke.py",)),
        _surface("project_workspace_read_model", "read-only project tree and bounded file snippets", str(PROJECT_ROOT), "usable_now", ("tests/jarvis_live_runtime/test_jarvis_live_brain_loop_context_smoke.py",)),
        _surface("runtime_history_store", "read-only retrieval", str(RUNTIME_HISTORY_STORE), "usable_now" if RUNTIME_HISTORY_STORE.exists() else "not_connected", ("tests/memory_engine/test_jarvis_history_query_reader_smoke.py",)),
        _surface("memory_engine_registry", "canonical/read-only retrieval", "MAKSIMAR_CORE_LIB/memory_engine", "usable_now", ("tests/memory_engine/test_memory_loader_smoke.py",)),
        _surface("vector_runtime_indexes", "vector", str(RUNTIME_VECTOR_INDEX_ROOT), "usable_now" if RUNTIME_VECTOR_INDEX_ROOT.exists() else "not_connected", ("tests/storage_registry/test_retrieval_index_reference_models_smoke.py",)),
        _surface("enterprise_business_memory", "business-sales", "MAKSIMAR_CORE_LIB/enterprise_memory_domains", "usable_now", ("tests/governance_federation_gap/test_memory_federation_policy_models_smoke.py",)),
        _surface("regulatory_memory_foundation", "regulatory", "MAKSIMAR_SERVER/REGULATORY_MEMORY_FOUNDATION", "usable_now", ("tests/regulatory_memory_foundation/test_regulatory_routing_acceptance_smoke.py",)),
        _surface("mempalace_read_only_sandbox", "external-vendor", "MAKSIMAR_SERVER/CONTROL_PLANE/memory_routing/adapters/mempalace_read_only_routing_integration.py", "sandbox_only", ("tests/memory_routing_adapters/test_mempalace_read_only_routing_integration_smoke.py",)),
        _surface("dashboard_memory_read_models", "dashboard-read-model", "MAKSIMAR_SERVER/DASHBOARD_READ_ONLY_VIEWS", "read_only", ("tests/final_memory_map/test_final_memory_summary_builder_smoke.py",)),
    )


def _surface(
    surface_id: str,
    surface_type: str,
    path: str,
    status: str,
    existing_tests: tuple[str, ...],
) -> dict[str, Any]:
    return {
        "surface_id": surface_id,
        "path": path,
        "type": surface_type,
        "status": status,
        "existing_tests": existing_tests,
        "forbidden_direct_write": True,
        "canonical_memory_write_allowed": False,
        "pc_control_allowed": False,
    }


def _mempalace_status() -> str:
    try:
        preview = build_mempalace_read_only_routing_integration_preview()
    except Exception:
        return "not_connected"
    if preview.get("routing_integration_ready") is True and preview.get("read_only_routing_enabled") is True:
        return "sandbox_only_read_only"
    return "sandbox_only_manual_review_required"


def _needs_deep_memory(lowered: str) -> bool:
    deep_markers = (
        "проект",
        "структур",
        "дерево",
        "файл",
        "файлы",
        "содержим",
        "ядро",
        "repo",
        "repository",
        "workspace",
        "source",
        "исходник",
        "memory",
        "память",
        "history",
        "runtime_history_store",
        "код",
        "статус",
        "ошибка",
        "тест",
        "git",
        "architecture",
        "архитектур",
        "approval gate",
        "суверенн",
        "business",
        "sales",
        "продаж",
        "enterprise",
        "закон",
        "regulatory",
        "compliance",
        "mempalace",
        "vector",
        "embedding",
        "обсуждали",
        "переписк",
        "gpt",
        "голос",
        "voice",
        "n8n",
        "tool",
        "adapter",
        "адаптер",
        "автоматизац",
    )
    return any(marker in lowered for marker in deep_markers)


def _needs_project_visibility(text: str) -> bool:
    lowered = text.casefold()
    markers = (
        "проект",
        "структур",
        "дерево",
        "файл",
        "файлы",
        "содержим",
        "ядро",
        "repo",
        "repository",
        "workspace",
        "source",
        "исходник",
        "код",
        "control_plane",
        "brain_loop",
        "terminal_chat",
    )
    return any(marker in lowered for marker in markers)
