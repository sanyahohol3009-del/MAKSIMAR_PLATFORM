from __future__ import annotations

from pathlib import Path
import hashlib
import json
import os
import sqlite3
from datetime import datetime, timezone
from typing import Any

from MAKSIMAR_CORE_LIB.memory_engine.history_ingestion.jarvis_history_query_models import (
    JarvisHistoryQuery,
)
from MAKSIMAR_CORE_LIB.memory_engine.history_ingestion.jarvis_history_query_reader import (
    run_jarvis_history_query,
)
from MAKSIMAR_CORE_LIB.memory_engine.memory_accessor import list_memory_definitions
from MAKSIMAR_CORE_LIB.retrieval_backend import build_retrieval_runtime_readonly_availability
from MAKSIMAR_CORE_LIB.enterprise_memory_domains.enterprise_memory_preview_builder import (
    build_enterprise_memory_preview,
)
from MAKSIMAR_SERVER.REGULATORY_MEMORY_FOUNDATION.regulatory_routing_preview_builder import (
    build_regulatory_routing_preview,
)
from MAKSIMAR_SERVER.CONTROL_PLANE.memory_routing.adapters.mempalace_read_only_routing_integration import (
    build_mempalace_read_only_routing_integration_preview,
)
from MAKSIMAR_SERVER.AI_ORCHESTRATION.project_workspace_tools import (
    MAX_PROJECT_FILE_SNIPPETS,
    PROJECT_ROOT,
    _project_tree_summary,
    _read_project_file_snippet,
    _select_project_files_for_context,
)
from MAKSIMAR_SERVER.AI_ORCHESTRATION.session_memory_store import (
    SESSION_STATE_PATH,
    _read_recent_local_chat_records,
    _session_turn_log_path,
    inspect_canonical_session_memory_health,
)


RUNTIME_VECTOR_INDEX_ROOT = Path.home() / "MAKSIMAR_RUNTIME" / "runtime_vector_indexes"
RUNTIME_EMBEDDINGS_ROOT = Path.home() / "MAKSIMAR_RUNTIME" / "runtime_embeddings"
RUNTIME_RETRIEVAL_ROOT = Path.home() / "MAKSIMAR_RUNTIME" / "runtime_retrieval"

MAX_LOCAL_CHAT_MEMORY_SNIPPETS = 4






























def _build_memory_surface_inventory() -> tuple[dict[str, Any], ...]:
    optional_vectors = build_retrieval_runtime_readonly_availability(PROJECT_ROOT)
    surfaces = (
        _surface("session_memory", "session-runtime", str(SESSION_STATE_PATH), "usable_now", ()),
        _surface("local_chat_memory", "append-only local chat/session memory", str(_session_turn_log_path()), "usable_now" if _session_turn_log_path().exists() else "usable_now", ("tests/jarvis_live_runtime/test_jarvis_live_memory_federation_smoke.py",)),
        _surface("project_workspace_read_model", "read-only project tree and bounded file snippets", str(PROJECT_ROOT), "usable_now", ("tests/jarvis_live_runtime/test_jarvis_live_brain_loop_context_smoke.py",)),
        _surface("runtime_history_store", "canonical append-only session/experience retrieval", str(_session_turn_log_path()), "usable_now" if _session_turn_log_path().is_file() else "not_connected", ("tests/memory_engine/test_jarvis_history_query_reader_smoke.py",)),
        _surface("memory_engine_registry", "canonical/read-only retrieval", "MAKSIMAR_CORE_LIB/memory_engine", "usable_now", ("tests/memory_engine/test_memory_loader_smoke.py",)),
        _surface("vector_runtime_indexes", "optional vector backend availability projection", str(RUNTIME_VECTOR_INDEX_ROOT), "usable_now" if any(item.available for item in optional_vectors) else "not_connected", ("tests/storage_registry/test_retrieval_index_reference_models_smoke.py",)),
        _surface("enterprise_business_memory", "business-sales", "MAKSIMAR_CORE_LIB/enterprise_memory_domains", "usable_now", ("tests/governance_federation_gap/test_memory_federation_policy_models_smoke.py",)),
        _surface("regulatory_memory_foundation", "regulatory", "MAKSIMAR_SERVER/REGULATORY_MEMORY_FOUNDATION", "usable_now", ("tests/regulatory_memory_foundation/test_regulatory_routing_acceptance_smoke.py",)),
        _surface("mempalace_read_only_sandbox", "external-vendor", "MAKSIMAR_SERVER/CONTROL_PLANE/memory_routing/adapters/mempalace_read_only_routing_integration.py", "sandbox_only", ("tests/memory_routing_adapters/test_mempalace_read_only_routing_integration_smoke.py",)),
        _surface("dashboard_memory_read_models", "dashboard-read-model", "MAKSIMAR_SERVER/DASHBOARD_READ_ONLY_VIEWS", "read_only", ("tests/final_memory_map/test_final_memory_summary_builder_smoke.py",)),
    )
    mempalace = _mempalace_live_read_model()
    session_health = inspect_canonical_session_memory_health()
    surfaces += (_surface("mempalace_search", "auxiliary project document/reference retrieval", mempalace.get("storage_path") or "configured Mempalace palace", "usable_now" if mempalace["status"] == "LIVE_READ_ONLY" else "not_connected", ("tests/jarvis_live_runtime/test_memory_retrieval_capabilities_visible.py",)),)
    for surface in surfaces:
        surface["classification"] = "READ_MODEL"
        surface["runtime_status"] = "READ_MODEL_ONLY"
        if surface["surface_id"] in {"runtime_history_store", "local_chat_memory"}:
            surface.update(classification="CANONICAL_STORE", owner="CanonicalSessionContextStore",
                           writer="CONTROL_PLANE.api_server._capture_canonical_turn_memory (ordinary/streaming) → CanonicalSessionContextStore.append",
                           persistence="append-only JSONL; flush/fsync", runtime_status=session_health["status"],
                           health=session_health)
        if surface["surface_id"] == "runtime_history_store":
            surface.update(classification="READ_MODEL", canonical_store_surface="local_chat_memory",
                           owner="run_jarvis_history_query over CanonicalSessionContextStore",
                           logical_roles=("history retrieval", "experience retrieval", "provenance retrieval"))
        if surface["surface_id"] == "local_chat_memory":
            surface["logical_roles"] = ("conversation", "episodic history", "developer experience", "LearningBundle references", "execution receipt memory", "retrieval trace")
        if surface["surface_id"] == "session_memory":
            surface.update(classification="READ_MODEL", owner="session_memory_store", settings_authority="descriptive cache, not host authorization")
        if surface["surface_id"] in {"enterprise_business_memory", "regulatory_memory_foundation"}:
            surface.update(runtime_status="CONTRACT_PREVIEW", persisted_dataset_available=False,
                           contract_examples_only=True, data_status="NOT_CONFIGURED",
                           owner="existing enterprise/regulatory contract preview builders")
        if surface["surface_id"] == "memory_engine_registry":
            surface.update(classification="CANONICAL_OWNER", owner="MemoryRegistry/load_memory_definition",
                           logical_roles=("versioned YAML memory definitions",),
                           path=str(PROJECT_ROOT / "MAKSIMAR_CORE/contracts/memory"))
        if surface["surface_id"] == "vector_runtime_indexes":
            surface.update(classification="OPTIONAL_PROVIDER", runtime_status="NOT_CONFIGURED"
                if not any(item.available for item in optional_vectors) else "LIVE_READ_ONLY",
                backends=tuple(item.to_read_model() for item in optional_vectors),
                directory_presence_is_not_runtime_availability=True)
        if surface["surface_id"] == "mempalace_search":
            surface.update(classification="CHILD_BACKEND", owner="ExistingMemoryRetrievalAdapter", health=mempalace,
                           runtime_status=mempalace["status"], persistence="existing native Chroma palace",
                           logical_roles=(mempalace["logical_role"],),
                           native_memory_authority=mempalace["native_memory_authority"],
                           writer="native mempalace.miner.process_file via typed refresh_mempalace_source",
                           write_scope="already indexed canonical project documentation; derived index only")
        if surface["surface_id"] == "mempalace_read_only_sandbox":
            surface.update(classification="LEGACY", runtime_status="SUPERSEDED_BY_CANONICAL_OWNER", superseded_by="mempalace_search")
    return surfaces + _native_runtime_journal_surfaces()


def _native_runtime_journal_surfaces() -> tuple[dict[str, Any], ...]:
    """Observe existing native journals without calling layout-creating readers.

    These are lifecycle/incident stores, never conversation or verified-work
    stores. The existing writers retain ownership; this projection cannot write.
    """
    from MAKSIMAR_CORE_LIB.event_bus.event_paths import get_event_journal_path
    from CORE_ROOT.runtime_paths import INCIDENT_HISTORY_FILE
    specifications = (
        ("native_event_journal", get_event_journal_path(),
         "MAKSIMAR_CORE_LIB.event_bus.event_writer.append_event_record",
         "EventRecord", ("runtime lifecycle events",), "event"),
        ("native_incident_history", INCIDENT_HISTORY_FILE,
         "CORE_ROOT.incident_history.write_incident_record",
         "native incident record", ("runtime recovery incidents",), "incident"),
    )
    surfaces = []
    for identity, path, owner, schema, roles, record_kind in specifications:
        health = _native_runtime_journal_health(path, record_kind)
        surface = _surface(identity, schema, str(path),
            "usable_now" if health["status"] == "LIVE_READ_ONLY" else "not_connected",
            ("tests/runtime/test_native_journal_append_durability.py",))
        surface.update(classification="CANONICAL_STORE", runtime_status=health["status"],
            owner=owner, writer=owner, persistence="append-only JSONL; flush/fsync",
            write_scope="existing native lifecycle/recovery writer only",
            logical_roles=roles, health=health,
            native_memory_authority={"conversation": False, "verified_experience": False})
        surfaces.append(surface)
    return tuple(surfaces)


def _native_runtime_journal_health(path: Path, record_kind: str) -> dict[str, Any]:
    """Bounded metadata snapshot; never exposes payloads or changes the journal."""
    from MAKSIMAR_CORE_LIB.event_bus.event_reader import _parse_event_line
    health = {"status": "NOT_CONFIGURED", "read_only": True,
        "observed_at": datetime.now(timezone.utc).isoformat(), "storage_path": str(path),
        "record_count": None, "invalid_record_count": None, "latest_event_at": None,
        "snapshot_byte_limit": 2_000_000, "snapshot_record_limit": 10_000}
    try:
        if not path.is_file():
            return health
        with path.open("rb") as handle:
            raw = handle.read(health["snapshot_byte_limit"] + 1)
        health["snapshot_bytes"] = len(raw)
        if len(raw) > health["snapshot_byte_limit"]:
            health.update(status="ENVIRONMENT_BLOCKED", error="journal_byte_bound_exceeded")
            return health
        health["snapshot_sha256"] = hashlib.sha256(raw).hexdigest()
        lines = [line for line in raw.splitlines() if line.strip()]
        if len(lines) > health["snapshot_record_limit"]:
            health.update(status="ENVIRONMENT_BLOCKED", error="journal_record_bound_exceeded")
            return health
        dates = []
        health.update(record_count=0, invalid_record_count=0)
        for line in lines:
            try:
                if record_kind == "event":
                    record = _parse_event_line(line.decode("utf-8"))
                    if not record.event_id or not record.event_type or not record.source:
                        raise ValueError("missing_event_identity")
                    date = datetime.fromisoformat(record.created_at.replace("Z", "+00:00"))
                    if date.tzinfo is None:
                        raise ValueError("event_date_missing_timezone")
                else:
                    record = json.loads(line)
                    if not isinstance(record, dict) or not isinstance(record.get("reason"), str) or not isinstance(record.get("status"), str):
                        raise ValueError("invalid_incident_schema")
                    date = datetime.fromtimestamp(float(record["timestamp_wall"]), timezone.utc)
                    float(record["timestamp_monotonic"])
                dates.append(date.astimezone(timezone.utc))
                health["record_count"] += 1
            except (KeyError, TypeError, ValueError, OverflowError, OSError):
                health["invalid_record_count"] += 1
        health["latest_event_at"] = max(dates).isoformat() if dates else None
        health["status"] = "ENVIRONMENT_BLOCKED" if health["invalid_record_count"] else "LIVE_READ_ONLY"
        if health["invalid_record_count"]:
            health["error"] = "invalid_native_journal_records"
    except (OSError, ValueError) as exc:
        health.update(status="ENVIRONMENT_BLOCKED", error=type(exc).__name__)
    return health


def _mempalace_live_read_model() -> dict[str, Any]:
    """Bounded readback of the configured native store, shared by UI and JARVIS.

    Never creates a palace, loads embeddings, copies documents or writes metadata.
    Hashes establish source freshness; existence alone never establishes health.
    """
    payload: dict[str, Any] = {"owner": "ExistingMemoryRetrievalAdapter", "classification": "CHILD_BACKEND",
        "logical_role": "AUXILIARY_PROJECT_DOCUMENT_REFERENCE_RETRIEVAL", "runtime_authority": False,
        "native_memory_authority": {role: False for role in ("business", "regulatory", "session", "experience", "evidence", "learning", "skills", "user", "device")},
        "status": "NOT_CONFIGURED", "observed_at": datetime.now(timezone.utc).isoformat(),
        "read_only": True, "source_authority": "original source files"}
    try:
        config = Path.home() / ".mempalace/config.json"
        configured = os.environ.get("MEMPALACE_PALACE")
        if not configured and config.is_file():
            configured = json.loads(config.read_text(encoding="utf-8")).get("palace_path")
        if not configured:
            return payload
        db = Path(configured).expanduser().resolve() / "chroma.sqlite3"
        payload["storage_path"] = str(db)
        if not db.is_file():
            return payload
        with sqlite3.connect(db.as_uri() + "?mode=ro", uri=True, timeout=2) as connection:
            rows = connection.execute("SELECT id,key,string_value,int_value FROM embedding_metadata WHERE key IN ('source_file','source_sha256','chunk_index','wing','room','filed_at','normalize_version') LIMIT 10001").fetchall()
            payload["embedding_count"] = connection.execute("SELECT count(*) FROM embeddings").fetchone()[0]
            payload["collection_count"] = connection.execute("SELECT count(*) FROM collections").fetchone()[0]
        if len(rows) > 10000:
            payload.update(status="ENVIRONMENT_BLOCKED", error="metadata_scan_bound_exceeded")
            return payload
        metadata: dict[int, dict[str, Any]] = {}
        for identity, key, text, integer in rows:
            metadata.setdefault(identity, {})[key] = text if text is not None else integer
        sources = {}; chunk_keys = []; indexed_times = []
        for meta in metadata.values():
            if meta.get("filed_at"):
                indexed_times.append(meta["filed_at"])
            if "chunk_index" not in meta:
                continue  # Native closets are derived summaries, not duplicate drawers.
            key = (meta.get("source_file"), meta.get("wing"), meta.get("room"), meta["chunk_index"])
            chunk_keys.append(key)
            path = Path(meta.get("source_file", "")).resolve()
            indexed_hash = meta.get("source_sha256")
            if str(path) not in sources:
                current_hash = None
                if path.is_relative_to(PROJECT_ROOT) and path.is_file() and path.stat().st_size <= 2_000_000:
                    current_hash = hashlib.sha256(path.read_bytes()).hexdigest()
                sources[str(path)] = {"path": str(path), "indexed_sha256": indexed_hash,
                    "current_sha256": current_hash,
                    "freshness": "FRESH" if indexed_hash and indexed_hash == current_hash else "STALE" if indexed_hash else "UNVERIFIED"}
            elif sources[str(path)]["indexed_sha256"] != indexed_hash:
                sources[str(path)]["freshness"] = "STALE"
        payload.update(drawer_count=len(chunk_keys), source_count=len(sources),
            duplicate_chunk_count=len(chunk_keys)-len(set(chunk_keys)), sources=tuple(sources.values()),
            last_indexed_at=max(indexed_times, default=None),
            freshness="FRESH" if sources and all(s["freshness"] == "FRESH" for s in sources.values()) else "STALE_OR_UNVERIFIED")
        payload["status"] = "LIVE_READ_ONLY" if chunk_keys and payload["freshness"] == "FRESH" and payload["duplicate_chunk_count"] == 0 else "NOT_CONFIGURED" if not chunk_keys else "ENVIRONMENT_BLOCKED"
    except (OSError, ValueError, sqlite3.Error) as exc:
        payload.update(status="ENVIRONMENT_BLOCKED", error=type(exc).__name__)
    return payload


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
    live = _mempalace_live_read_model()
    if live["status"] == "LIVE_READ_ONLY":
        return "live_read_only_child_archive"
    try:
        preview = build_mempalace_read_only_routing_integration_preview()
    except Exception:
        return "not_connected"
    if preview.get("routing_integration_ready") is True and preview.get("read_only_routing_enabled") is True:
        return "sandbox_only_read_only"
    return "sandbox_only_manual_review_required"
