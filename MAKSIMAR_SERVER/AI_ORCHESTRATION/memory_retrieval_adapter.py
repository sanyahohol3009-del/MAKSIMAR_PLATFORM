from __future__ import annotations

"""Canonical evidence adapter over existing memory readers and native index writer."""

import hashlib
import json
import os
import subprocess
from pathlib import Path
from typing import Any, Callable

_MEMPALACE_VENV_PYTHON = Path("EXTERNAL_BACKENDS/mempalace/venv/bin/python")


def _mempalace_refresh_source(source_path: str) -> Path:
    """Bound derived-index writes to already reviewed project documentation."""
    path = Path(source_path).expanduser().resolve()
    docs = (PROJECT_ROOT / "docs").resolve()
    if not path.is_relative_to(docs) or path.suffix.lower() not in {".md", ".txt"}:
        raise ValueError("refresh requires a canonical project documentation source")
    if not path.is_file() or path.stat().st_size > 2_000_000:
        raise ValueError("refresh source missing or exceeds bounded document size")
    return path


def _run_mempalace_refresh(source_path: str) -> dict[str, Any]:
    """Reuse the native miner for one existing source; never enroll a new corpus."""
    source = _mempalace_refresh_source(source_path)
    script = """import sys,json,hashlib,contextlib
from pathlib import Path
from mempalace.config import MempalaceConfig
from mempalace.palace import get_collection,get_closets_collection
from mempalace.miner import process_file
source=Path(sys.argv[1]); root=Path(sys.argv[2])
palace=sys.argv[3] or MempalaceConfig().palace_path
collection=get_collection(palace,create=False)
before=collection.get(where={'source_file':str(source)},include=['metadatas'])
if not before.ids: raise ValueError('source_not_already_indexed')
wings={m.get('wing') for m in before.metadatas}; rooms={m.get('room') for m in before.metadatas}
if len(wings)!=1 or rooms!={'general'}: raise ValueError('ambiguous_native_source_ownership')
before_hashes=sorted({m.get('source_sha256','') for m in before.metadatas})
with contextlib.redirect_stdout(sys.stderr):
    count,room=process_file(source,root,collection,next(iter(wings)),[],'JARVIS',False,
        closets_col=get_closets_collection(palace,create=False))
after=collection.get(where={'source_file':str(source)},include=['metadatas'])
digest=hashlib.sha256(source.read_bytes()).hexdigest()
keys=[(m.get('wing'),m.get('room'),m.get('chunk_index')) for m in after.metadatas]
verified=bool(after.ids) and all(m.get('source_sha256')==digest for m in after.metadatas) and len(keys)==len(set(keys))
print(json.dumps({'source_path':str(source),'palace':palace,'previous_indexed_sha256':before_hashes,
    'current_source_sha256':digest,'indexed_sha256':sorted({m.get('source_sha256','') for m in after.metadatas}),
    'drawers_written':count,'source_drawer_count':len(after.ids),'duplicate_chunks':len(keys)-len(set(keys)),
    'freshness':'FRESH' if verified else 'STALE','effect_readback_verified':verified,
    'derived_index_only':True,'runtime_authority':False}))
sys.exit(0 if verified else 1)
"""
    completed = subprocess.run([str(_MEMPALACE_VENV_PYTHON), "-B", "-c", script,
        str(source), str(PROJECT_ROOT), os.environ.get("MEMPALACE_PALACE", "")],
        capture_output=True, text=True, encoding="utf-8", errors="replace", timeout=45, check=False)
    try:
        payload = json.loads(completed.stdout)
    except (ValueError, TypeError):
        return {"returncode": completed.returncode, "error": "native_index_refresh_failed"}
    return {**payload, "returncode": completed.returncode}


def _run_mempalace_search(query: str, palace_path: str | None = None) -> dict[str, Any]:
    """Run a real Mempalace search via the frozen 3.3.5 runtime (read-only).

    Returns the real search output/returncode; never fabricates a result when the
    store is unavailable or un-mined.
    """
    import subprocess as _sp

    # The installed vendor configuration owns the index location. Do not
    # silently redirect searches to a second default palace.
    script = """import sys,json,hashlib
from pathlib import Path
from mempalace.config import MempalaceConfig
from mempalace.searcher import search_memories
from mempalace.palace import get_collection
palace=sys.argv[2] or MempalaceConfig().palace_path
root=Path(sys.argv[3]).resolve()
result=search_memories(sys.argv[1],palace,n_results=6,candidate_strategy='union')
if not result.get('error'):
    indexed=get_collection(palace,create=False).get(include=['metadatas'])
    metas=list(zip(indexed.ids,indexed.metadatas))
    unique=[]; seen=set()
    for hit in result.get('results',[]):
        key=(hit.get('source_path'),hit.get('matched_chunk_index'),hit.get('text'))
        if key in seen: continue
        seen.add(key); sources=[]
        for drawer_id,meta in metas:
            path=Path(meta.get('source_file','')).resolve()
            if (str(path) != hit.get('source_path') or meta.get('wing') != hit.get('wing')
                or not path.is_relative_to(root) or not path.is_file()): continue
            if meta.get('chunk_index') != hit.get('matched_chunk_index'): continue
            current_hash=hashlib.sha256(path.read_bytes()).hexdigest()
            indexed_hash=meta.get('source_sha256')
            sources.append({'path':str(path),'sha256':current_hash,'indexed_sha256':indexed_hash,
                'freshness':'FRESH' if indexed_hash==current_hash else 'STALE' if indexed_hash else 'UNVERIFIED',
                'drawer_id':drawer_id,'chunk_index':meta.get('chunk_index'),
                'indexed_at':meta.get('filed_at'),'index_version':meta.get('normalize_version'),
                'provenance_version':meta.get('provenance_version'),
                'indexed_source_mtime':meta.get('source_mtime'),'current_source_mtime':path.stat().st_mtime})
        hit['source_readback']=sources; unique.append(hit)
    result['results']=unique[:3]
print(json.dumps({'palace':palace,'retrieval':result},ensure_ascii=False))
sys.exit(1 if result.get('error') else 0)
"""
    palace = palace_path or os.environ.get("MEMPALACE_PALACE", "")
    command = [str(_MEMPALACE_VENV_PYTHON), "-B", "-c", script, query, palace, str(PROJECT_ROOT)]
    try:
        completed = _sp.run(
            command, text=True, encoding="utf-8", errors="replace",
            capture_output=True, timeout=30.0, check=False,
        )
    except (_sp.SubprocessError, TimeoutError, OSError) as exc:
        return {"query": query, "palace": palace, "error": type(exc).__name__, "returncode": None}
    try:
        readback = json.loads(completed.stdout)
    except (ValueError, TypeError):
        return {"query": query, "palace": palace, "returncode": None,
                "error": "invalid_mempalace_structured_readback"}
    return {
        "query": query,
        "palace": readback.get("palace"),
        "retrieval": readback.get("retrieval"),
        "returncode": completed.returncode,
        "stderr": completed.stderr.strip()[-400:],
        "derived_index_only": True,
        "runtime_authority": False,
    }

from MAKSIMAR_CORE_LIB.ai_orchestration.semantic_intent_contract import (
    EvidenceBundle,
    EvidenceItem,
    ExecutionPlan,
    ExecutionReceipt,
    RequestDeadline,
    RequestUnderstanding,
    utc_observed_at,
)
from MAKSIMAR_CORE_LIB.enterprise_memory_domains.enterprise_memory_preview_builder import (
    build_enterprise_memory_preview,
)
from MAKSIMAR_CORE_LIB.memory_engine.history_ingestion.jarvis_history_query_models import (
    JarvisHistoryQuery,
)
from MAKSIMAR_CORE_LIB.memory_engine.history_ingestion.jarvis_history_query_reader import (
    run_jarvis_history_query,
)
from MAKSIMAR_CORE_LIB.memory_engine.memory_accessor import list_memory_definitions
from MAKSIMAR_CORE_LIB.retrieval_backend import (
    build_retrieval_runtime_readonly_availability,
)
from MAKSIMAR_SERVER.AI_ORCHESTRATION.project_workspace_tools import PROJECT_ROOT
from MAKSIMAR_SERVER.AI_ORCHESTRATION.memory_context_sources import _mempalace_live_read_model
from MAKSIMAR_SERVER.AI_ORCHESTRATION.session_memory_store import (
    _read_recent_local_chat_records,
    _session_turn_log_path,
)
from MAKSIMAR_SERVER.DASHBOARD_READ_ONLY_VIEWS.dashboard_read_only_views_readiness_gate import (
    build_dashboard_read_only_views_phase_preview,
)
from MAKSIMAR_SERVER.DASHBOARD_READ_ONLY_VIEWS.final_memory_map.final_memory_preview_builder import build_final_memory_preview
from MAKSIMAR_SERVER.CONTROL_PLANE.memory_routing.adapters.mempalace_read_only_routing_integration import (
    build_mempalace_read_only_routing_integration_preview,
)
from MAKSIMAR_SERVER.REGULATORY_MEMORY_FOUNDATION.regulatory_routing_preview_builder import (
    build_regulatory_routing_preview,
)
from MAKSIMAR_SERVER.AI_ORCHESTRATION.jarvis_live_read_models import (
    build_jarvis_live_memory_federation_status,
)


PROVIDER_ID = "existing_memory_retrieval_tools"


def _contract_memory_preview(builder: Callable[[], Any]) -> dict[str, Any]:
    """Qualify existing static contract examples separately from populated data."""
    return {"classification": "READ_MODEL", "data_status": "NOT_CONFIGURED",
            "persisted_dataset_available": False, "contract_examples_only": True,
            "runtime_authority": False, "owner": builder.__module__ + "." + builder.__name__,
            "contract_preview": builder()}


def _bounded_memory_payload(value: Any) -> tuple[str, int]:
    """Reuse structured field bounding, then trim collections before encoding."""
    from MAKSIMAR_SERVER.AI_ORCHESTRATION.project_understanding_adapter import ExistingProjectUnderstandingAdapter
    bounded, omitted = ExistingProjectUnderstandingAdapter._bounded_payload(value, max_items=40, max_text=900)
    def collections(node):
        if isinstance(node, dict):
            return [child for value in node.values() for child in collections(value)]
        if isinstance(node, list):
            return ([node] if node else []) + [child for value in node for child in collections(value)]
        return []
    while len(json.dumps(bounded, ensure_ascii=False, default=str, sort_keys=True)) > 12000:
        candidates = collections(bounded)
        if not candidates:
            bounded, extra = ExistingProjectUnderstandingAdapter._bounded_payload(bounded, max_items=40, max_text=100)
            omitted += extra
            if not extra:
                raise ValueError("memory structured payload exceeds budget")
        else:
            largest = max(candidates, key=lambda item: len(json.dumps(item, default=str)))
            largest.pop()
            omitted += 1
    return json.dumps(bounded, ensure_ascii=False, default=str, sort_keys=True), omitted
from MAKSIMAR_CORE_LIB.memory_engine.history_ingestion.jarvis_history_query_models import (
    MEMORY_FILTER_SCHEMA, HISTORY_MEMORY_FILTER_SCHEMA, SOURCE_DOCUMENT_MEMORY_FILTER_SCHEMA,
)


def _learning_experience_projection(records: tuple[dict[str, Any], ...], query: str) -> tuple[dict[str, Any], ...]:
    """Project bounded learning metadata into the existing history result.

    Session history is the source of persistence; this is deliberately a
    read-time projection, not a second index or store.  Matching uses the
    same observable textual/metadata fields available in the event schema.
    """
    result: dict[str, dict[str, Any]] = {}
    for record in records:
        from MAKSIMAR_SERVER.AI_ORCHESTRATION.session_memory_store import canonical_experience_projection
        canonical = canonical_experience_projection(record)
        if canonical is not None:
            result[canonical["experience_id"]] = canonical
    return tuple(result.values())

MEMORY_RETRIEVAL_OPERATION_CONTRACTS: tuple[dict[str, Any], ...] = (
    {
        "operation_id": "search_history",
        "description": (
            "Retrieve real persisted conversation history or verified experiences, including simulation results, "
            "experience IDs, trace/session provenance, evidence and review refs, verification/review status, "
            "canonical timestamps and LearningBundle links. Supports typed semantic purpose and time bounds. "
            "Legacy experiences with unknown dates remain readable but are excluded from dated queries."
        ),
        "required_parameters": ("query", "memory_filter"),
        "parameter_schemas": {"memory_filter": HISTORY_MEMORY_FILTER_SCHEMA},
        "evidence_kinds": ("history_search",),
        "effect_type": "OBSERVE",
        "target_scope": "local_project_history",
        "semantic_owner_id": "memory.retrieve",
        "reversibility": "REVERSIBLE",
        "external_side_effect": False,
        "risk_class": "READ_ONLY",
    },
    {
        "operation_id": "inspect_recent_session_memory",
        "description": "Read actual bounded recent records from existing local chat history.",
        "required_parameters": (),
        "evidence_kinds": ("session_memory",),
        "effect_type": "OBSERVE",
        "target_scope": "local_session_history",
        "semantic_owner_id": "memory.retrieve",
        "reversibility": "REVERSIBLE",
        "external_side_effect": False,
        "risk_class": "READ_ONLY",
    },
    {
        "operation_id": "inspect_memory_registry",
        "description": "Read YAML memory-definition schemas only; not current layers, physical stores, index availability or live health.",
        "required_parameters": (),
        "evidence_kinds": ("memory_registry",),
        "effect_type": "OBSERVE",
        "target_scope": "local_memory_registry",
        "semantic_owner_id": "memory.retrieve",
        "reversibility": "REVERSIBLE",
        "external_side_effect": False,
        "risk_class": "READ_ONLY",
    },
    {
        "operation_id": "inspect_memory_domains",
        "description": "Read enterprise and regulatory memory projection metadata, not project-history content.",
        "required_parameters": (),
        "evidence_kinds": ("memory_domains",),
        "effect_type": "OBSERVE",
        "target_scope": "local_memory_domains",
        "semantic_owner_id": "memory.retrieve",
        "reversibility": "REVERSIBLE",
        "external_side_effect": False,
        "risk_class": "READ_ONLY",
    },
    {
        "operation_id": "inspect_retrieval_backends",
        "description": "Read retrieval-backend availability only, not stored history content.",
        "required_parameters": (),
        "evidence_kinds": ("retrieval_backends",),
        "effect_type": "OBSERVE",
        "target_scope": "local_retrieval_runtime",
        "semantic_owner_id": "memory.retrieve",
        "reversibility": "REVERSIBLE",
        "external_side_effect": False,
        "risk_class": "READ_ONLY",
    },
    {
        "operation_id": "inspect_memory_federation",
        "description": "Observe live memory owners/layers, physical paths/counts, domain state, session health and Mempalace auxiliary role/authority/index health. Shared JARVIS/UI projection.",
        "required_parameters": (),
        "evidence_kinds": ("memory_federation",),
        "effect_type": "OBSERVE",
        "target_scope": "local_memory_runtime",
        "semantic_owner_id": "memory.retrieve",
        "reversibility": "REVERSIBLE",
        "external_side_effect": False,
        "risk_class": "READ_ONLY",
    },
)

MEMORY_CAPABILITY_OPERATION_CONTRACTS: dict[str, tuple[dict[str, Any], ...]] = {
    "runtime_history_store": MEMORY_RETRIEVAL_OPERATION_CONTRACTS,
    "dashboard_memory_read_models": ({
        "operation_id": "read_dashboard_memory_models",
        "description": "Read the existing dashboard memory view readiness and contract preview.",
        "required_parameters": (), "evidence_kinds": ("dashboard_memory_models",),
        "effect_type": "OBSERVE", "target_scope": "local_memory_runtime",
        "semantic_owner_id": "memory.retrieve",
        "reversibility": "REVERSIBLE", "external_side_effect": False, "risk_class": "READ_ONLY",
    },),
    "enterprise_business_memory": ({
        "operation_id": "read_enterprise_business_memory",
        "description": "Read the existing enterprise business-memory projection without mutation.",
        "required_parameters": (), "evidence_kinds": ("enterprise_business_memory",),
        "effect_type": "OBSERVE", "target_scope": "local_memory_domains",
        "semantic_owner_id": "memory.retrieve",
        "reversibility": "REVERSIBLE", "external_side_effect": False, "risk_class": "READ_ONLY",
    },),
    "local_chat_memory": ({
        "operation_id": "read_local_chat_memory",
        "description": "Read bounded recent records from the existing append-only local chat memory.",
        "required_parameters": (), "evidence_kinds": ("local_chat_memory",),
        "effect_type": "OBSERVE", "target_scope": "local_session_history",
        "semantic_owner_id": "memory.retrieve",
        "reversibility": "REVERSIBLE", "external_side_effect": False, "risk_class": "READ_ONLY",
    },),
    "memory_engine_registry": ({
        "operation_id": "read_memory_engine_registry",
        "description": "Read YAML memory-definition schemas only; not current layers, physical stores, index availability or live health.",
        "required_parameters": (), "evidence_kinds": ("memory_engine_registry",),
        "effect_type": "OBSERVE", "target_scope": "local_memory_registry",
        "semantic_owner_id": "memory.retrieve",
        "reversibility": "REVERSIBLE", "external_side_effect": False, "risk_class": "READ_ONLY",
    },),
    "regulatory_memory_foundation": ({
        "operation_id": "read_regulatory_memory_foundation",
        "description": "Read the existing regulatory-memory routing projection without mutation.",
        "required_parameters": (), "evidence_kinds": ("regulatory_memory_foundation",),
        "effect_type": "OBSERVE", "target_scope": "local_memory_domains",
        "semantic_owner_id": "memory.retrieve",
        "reversibility": "REVERSIBLE", "external_side_effect": False, "risk_class": "READ_ONLY",
    },),
    "session_memory": ({
        "operation_id": "read_session_memory",
        "description": "Read the bounded canonical local session-memory state.",
        "required_parameters": (), "evidence_kinds": ("session_memory",),
        "effect_type": "OBSERVE", "target_scope": "local_session_history",
        "semantic_owner_id": "memory.retrieve",
        "reversibility": "REVERSIBLE", "external_side_effect": False, "risk_class": "READ_ONLY",
    },),
    "mempalace_read_only_sandbox": ({
        "operation_id": "read_mempalace_sandbox",
        "description": "Read the existing Mempalace sandbox integration status without writes or synchronization.",
        "required_parameters": (), "evidence_kinds": ("mempalace_sandbox",),
        "effect_type": "OBSERVE", "target_scope": "local_memory_runtime",
        "semantic_owner_id": "memory.retrieve",
        "reversibility": "REVERSIBLE", "external_side_effect": False, "risk_class": "READ_ONLY",
    },),
    "mempalace_search": ({
        "operation_id": "search_mempalace", "supported_goal_effect_intents": ("retrieve",),
        "description": "Retrieve indexed source-document excerpts from the native Mempalace child archive, with source path, drawer identity and hash freshness. Archive search does not inspect current platform health, connected stores, configured domain datasets or inventory counts; use inspect_memory_federation for those.",
        "required_parameters": ("query",), "optional_parameters": ("memory_filter",),
        "parameter_schemas": {"memory_filter": SOURCE_DOCUMENT_MEMORY_FILTER_SCHEMA},
        "evidence_kinds": ("mempalace_search",),
        "effect_type": "OBSERVE", "target_scope": "local_memory_runtime",
        "semantic_owner_id": "memory.retrieve",
        "reversibility": "REVERSIBLE", "external_side_effect": False, "risk_class": "READ_ONLY",
    }, {
        "operation_id": "refresh_mempalace_source",
        "description": "Refresh the derived native archive index of one already indexed canonical project document after its source changed. Reuse its native wing/store; do not edit the source, enroll new files, or change runtime authority. Return actual source/index SHA and freshness after the native writer.",
        "required_parameters": ("source_path",), "evidence_kinds": ("mempalace_index_refresh",),
        "effect_type": "MUTATE", "target_scope": "local_memory_runtime",
        "semantic_owner_id": "memory.retrieve", "reversibility": "REVERSIBLE",
        "external_side_effect": False, "risk_class": "MUTATION",
    }),
    "vector_runtime_indexes": ({
        "operation_id": "read_vector_runtime_indexes",
        "description": "Read current local vector and retrieval backend availability without executing retrieval.",
        "required_parameters": (), "evidence_kinds": ("vector_runtime_indexes",),
        "effect_type": "OBSERVE", "target_scope": "local_retrieval_runtime",
        "semantic_owner_id": "memory.retrieve",
        "reversibility": "REVERSIBLE", "external_side_effect": False, "risk_class": "READ_ONLY",
    },),
}

ALL_MEMORY_RETRIEVAL_OPERATION_CONTRACTS = tuple(
    contract
    for contracts in MEMORY_CAPABILITY_OPERATION_CONTRACTS.values()
    for contract in contracts
)


class ExistingMemoryRetrievalAdapter:
    """One owner-level adapter over existing read/query implementations."""

    provider_id = PROVIDER_ID

    def health(self) -> dict[str, Any]:
        return {
            "provider_id": self.provider_id,
            "status": "AVAILABLE",
            "read_only": False,
            "writes": "bounded native derived-index refresh only; per-operation typed policy",
            "history_store_present": _session_turn_log_path().exists(),
            "session_log_present": _session_turn_log_path().exists(),
        }

    def collect_evidence(
        self,
        understanding: RequestUnderstanding,
        plan: ExecutionPlan,
        trace_id: str,
        deadline: RequestDeadline | None = None,
    ) -> EvidenceBundle:
        operations: dict[str, Callable[[], Any]] = {
            "inspect_recent_session_memory": lambda: {
                "records": _read_recent_local_chat_records(limit=8),
                "source": str(_session_turn_log_path()),
            },
            "inspect_memory_registry": lambda: {
                "definitions": tuple(
                    {
                        "entity_id": item.entity_id,
                        "version": item.version,
                        "file_path": str(item.file_path),
                        "description": str(item.payload.get("description", "")),
                    }
                    for item in list_memory_definitions()
                )
            },
            "inspect_memory_domains": lambda: {
                "enterprise": _contract_memory_preview(build_enterprise_memory_preview),
                "regulatory": _contract_memory_preview(build_regulatory_routing_preview),
            },
            "inspect_retrieval_backends": lambda: {
                "mempalace_vector_archive": _mempalace_live_read_model(),
                "backends": tuple(
                    item.to_read_model()
                    for item in build_retrieval_runtime_readonly_availability(PROJECT_ROOT)
                )
            },
            "inspect_memory_federation": lambda: {
                "federation": build_jarvis_live_memory_federation_status(),
                "mempalace": _mempalace_live_read_model(),
            },
            "read_dashboard_memory_models": build_final_memory_preview,
            "read_enterprise_business_memory": lambda: _contract_memory_preview(build_enterprise_memory_preview),
            "read_local_chat_memory": lambda: {
                "records": _read_recent_local_chat_records(limit=8),
                "source": str(_session_turn_log_path()),
            },
            "read_memory_engine_registry": lambda: {
                "definitions": tuple(
                    {
                        "entity_id": item.entity_id,
                        "version": item.version,
                        "file_path": str(item.file_path),
                        "description": str(item.payload.get("description", "")),
                    }
                    for item in list_memory_definitions()
                )
            },
            "read_regulatory_memory_foundation": lambda: _contract_memory_preview(build_regulatory_routing_preview),
            "read_mempalace_sandbox": build_mempalace_read_only_routing_integration_preview,
            "search_mempalace": lambda: _run_mempalace_search(str(understanding.original_text)),
            "read_vector_runtime_indexes": lambda: {
                "mempalace_vector_archive": _mempalace_live_read_model(),
                "backends": tuple(
                    item.to_read_model()
                    for item in build_retrieval_runtime_readonly_availability(PROJECT_ROOT)
                )
            },
        }
        # Logical session roles share the same eligible canonical journal reader.
        # The style compatibility cache is never a fallback memory authority.
        operations["read_session_memory"] = operations["inspect_recent_session_memory"]
        items: list[EvidenceItem] = []
        receipts: list[ExecutionReceipt] = []
        errors: list[str] = []
        for step in plan.steps:
            if deadline is not None and deadline.cancelled:
                errors.append(f"{step.operation}:total_deadline")
                break
            operation = operations.get(step.operation)
            if operation is None and step.operation not in {"search_history", "refresh_mempalace_source"}:
                errors.append(f"{step.operation}:unsupported_operation")
                continue
            try:
                if step.operation == "refresh_mempalace_source":
                    source_path = dict(step.parameters).get("source_path")
                    if not source_path:
                        errors.append(f"{step.operation}:missing_source_path")
                        continue
                    operation = lambda: _run_mempalace_refresh(str(source_path))
                if step.operation in {"search_history", "search_mempalace"}:
                    query = dict(step.parameters).get("query")
                    if not query:
                        errors.append(f"{step.operation}:missing_query")
                        continue
                    if step.operation == "search_history":
                        def _search_history(query=query):
                            filter_value = dict(step.parameters).get("memory_filter", "{}")
                            filters = json.loads(filter_value) if isinstance(filter_value, str) else filter_value
                            if not isinstance(filters, dict) or set(filters) - {"query_kind", "time_basis", "time_start", "time_end"}:
                                raise ValueError("invalid typed memory filter")
                            history_query = JarvisHistoryQuery(query_text=query, query_scope="project_history",
                                query_ready=True, **filters)
                            records = _read_recent_local_chat_records(limit=64,
                                experience_only=history_query.query_kind != "HISTORY")
                            experiences = _learning_experience_projection(records, query)
                            inputs = experiences if history_query.query_kind != "HISTORY" else tuple(
                                {k: r[k] for k in ("trace_id", "session_id", "topic", "user_text", "assistant_text", "timestamp", "persisted_at") if k in r}
                                for r in records
                            )
                            readback = run_jarvis_history_query(history_query, inputs)
                            return {
                                "history_query": readback,
                                "source": str(_session_turn_log_path()),
                            }
                        operation = _search_history
                    else:
                        operation = lambda query=query: _run_mempalace_search(str(query))
                payload = operation()
            except Exception as exc:
                errors.append(f"{step.operation}:{type(exc).__name__}")
                continue
            if step.operation in {"search_mempalace", "refresh_mempalace_source"} and (
                not isinstance(payload, dict) or payload.get("returncode") != 0
                or (step.operation == "refresh_mempalace_source" and payload.get("effect_readback_verified") is not True)
            ):
                error = str(payload.get("error") or payload.get("stdout") or "mempalace_search_failed") if isinstance(payload, dict) else "invalid_result"
                errors.append(f"{step.operation}:{error[:160]}")
                continue
            bounded, omitted = _bounded_memory_payload(payload)
            digest = hashlib.sha256(bounded.encode("utf-8")).hexdigest()
            evidence_kind = next(
                contract["evidence_kinds"][0]
                for contract in ALL_MEMORY_RETRIEVAL_OPERATION_CONTRACTS
                if contract["operation_id"] == step.operation
            )
            items.append(EvidenceItem(
                kind=str(evidence_kind),
                source=f"{self.provider_id}:{step.operation}",
                observation=bounded,
                scope=str(PROJECT_ROOT),
                confidence=1.0,
                trace_id=trace_id,
                observed_at=utc_observed_at(),
                content_hash=f"sha256:{digest}",
                source_reference=f"memory://{step.operation}",
                truncated=bool(omitted),
                omitted_count=omitted,
                request_id=understanding.request_id,
                step_id=step.step_id,
                capability_id=step.capability_id,
                operation_id=step.operation,
                provider_id=self.provider_id,
            ))
            receipts.append(ExecutionReceipt(
                receipt_id=f"{trace_id}:{step.step_id}",
                request_id=understanding.request_id,
                trace_id=trace_id,
                step_id=step.step_id,
                capability_id=step.capability_id,
                operation_id=step.operation,
                provider_id=self.provider_id,
                status="COMPLETE",
                result=("native derived index refresh verified against source bytes"
                        if step.operation == "refresh_mempalace_source" else "required read-only memory/retrieval evidence collected"),
            ))
        status = "COMPLETE" if items and not errors else "PARTIAL" if items else "UNAVAILABLE"
        return EvidenceBundle(
            request_id=understanding.request_id,
            capability_id=(plan.steps[0].capability_id if plan.steps else "runtime_history_store"),
            trace_id=trace_id,
            status=status,
            items=tuple(items),
            limitations=(
                () if status == "COMPLETE" else
                ("memory or retrieval evidence incomplete; returned evidence remains bounded and read-only",)
            ),
            receipts=tuple(receipts),
            errors=tuple(errors),
            capability_ids=tuple(dict.fromkeys(step.capability_id for step in plan.steps)),
        )


__all__ = [
    "ExistingMemoryRetrievalAdapter",
    "MEMORY_CAPABILITY_OPERATION_CONTRACTS",
    "MEMORY_RETRIEVAL_OPERATION_CONTRACTS",
    "PROVIDER_ID",
]
