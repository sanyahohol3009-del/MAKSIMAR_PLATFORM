from __future__ import annotations

from MAKSIMAR_CORE_LIB.ai_orchestration.semantic_intent_contract import RequestDeadline, UnderstandingAttemptPolicy

import json
import anyio
from functools import wraps
from fastapi.routing import APIRoute
from starlette.requests import ClientDisconnect
from starlette.concurrency import run_in_threadpool
from contextlib import asynccontextmanager
from datetime import UTC, datetime
from importlib import import_module
from typing import Any, AsyncIterator, Iterable

from fastapi import FastAPI, Header, HTTPException
from fastapi.responses import StreamingResponse
from pathlib import Path
import time

from CONTROL_PLANE.health.monitor import take_snapshot
from CORE_ROOT.run_context import model_free_startup
from CONTROL_PLANE.canonical_semantic_spine import (
    CANONICAL_TURN_TIMEOUT_SECONDS,
    CANDIDATE_DISCOVERY_JSON_SCHEMA,
    KIND_DISCOVERY_JSON_SCHEMA,
    REQUEST_UNDERSTANDING_JSON_SCHEMA,
    run_canonical_semantic_turn,
    stream_canonical_semantic_turn,
)
from MAKSIMAR_SERVER.AI_ORCHESTRATION.project_understanding_adapter import ExistingProjectUnderstandingAdapter
from MAKSIMAR_SERVER.AI_ORCHESTRATION.memory_retrieval_adapter import ExistingMemoryRetrievalAdapter
from MAKSIMAR_SERVER.AI_ORCHESTRATION.simulation_worker_adapter import ExistingSimulationWorkerAdapter
from MAKSIMAR_SERVER.AI_ORCHESTRATION.n8n_adapter import ExistingN8nAdapter
from MAKSIMAR_SERVER.AI_ORCHESTRATION.model_role_adapter import ExistingOllamaModelRoleAdapter
from MAKSIMAR_SERVER.AI_ORCHESTRATION.media_provider_adapter import ExistingFfprobeMediaAdapter
from MAKSIMAR_SERVER.AI_ORCHESTRATION.browser_provider_adapter import ExistingPlaywrightBrowserAdapter
from MAKSIMAR_SERVER.AI_ORCHESTRATION.conversation_evidence_adapter import ExistingConversationEvidenceAdapter
from MAKSIMAR_SERVER.AI_ORCHESTRATION.model_understanding_adapter import ExistingOllamaModelUnderstandingAdapter
from MAKSIMAR_SERVER.AI_ORCHESTRATION.session_memory_store import CanonicalSessionContextStore
from MAKSIMAR_CORE_LIB.security_layer.semantic_policy import (
    SemanticPolicyEvaluator, identity_context_from_http_payload,
)
from MAKSIMAR_CORE_LIB.ai_orchestration.semantic_intent_contract import IdentityContext
from MAKSIMAR_CORE_LIB.security_layer.host_approval_handshake import CANONICAL_HOST_APPROVAL_STORE
from MAKSIMAR_CORE_LIB.security_layer.host_principal import identity_from_host_token
from MAKSIMAR_SERVER.AI_ORCHESTRATION.jarvis_live_brain_loop_server_adapter import ExistingFinalBrainAdapter
from MAKSIMAR_SERVER.OBSERVABILITY.jarvis_live.jarvis_live_observability_read_model import (
    build_runtime_readiness_payload, record_in_flight_trace_event, in_flight_trace_read_model, set_in_flight_trace,
)
from MAKSIMAR_SERVER.SKILL_ADAPTER_REGISTRY.existing_capability_inventory import (
    build_existing_capability_catalog,
    build_semantic_capability_registry_projection,
)
from MAKSIMAR_SERVER.WORKFLOW_AUTOMATION_RUNTIME.jarvis_pc_action_adapter_contract import (
    DIRECT_PC_ACTION_MAP, ExistingWindowsEdgeAdapter,
)
from MAKSIMAR_SERVER.CLIENT_LEARNING_INPUT import (
    build_experience_learning_bundle,
    build_sandbox_learning_bundle,
    capture_proposal_experience,
    qualify_verified_sandbox_experience,
    validate_learning_bundle_intake,
)
from MAKSIMAR_SERVER.PROPOSAL_AUDIT import audit_proposal_runtime
from MAKSIMAR_SERVER.CLIENT_LEARNING_INPUT.developer_experience_contract import qualify_provider_execution_experience
from MAKSIMAR_CORE_LIB.evolution_debug import requirement_from_semantic_understanding, select_sandbox

@asynccontextmanager
async def _control_plane_lifespan(_: FastAPI) -> AsyncIterator[None]:
    _prewarm_semantic_capability_inventory()
    import importlib

    importlib.import_module("MAKSIMAR_SERVER.WORKERS.simulation_worker")  # registers worker runtime factory in CORE
    yield


app = FastAPI(title="MAKSIMAR Control Plane", lifespan=_control_plane_lifespan)


def _operator_read_context(authorization: str | None, session_id: str | None):
    from MAKSIMAR_SERVER.OBSERVABILITY.operator_shell_read_model import require_operator_read
    if not authorization or not authorization.startswith("Bearer "):
        raise HTTPException(401, "verified_host_principal_required")
    return require_operator_read(authorization[7:], session_id or "")


@app.get("/operator-shell/read-model")
def operator_shell_read_model(authorization: str | None = Header(default=None),
                              x_jarvis_session: str | None = Header(default=None)):
    from MAKSIMAR_SERVER.OBSERVABILITY.operator_shell_read_model import foundation_projection, supervisor_settings_projection, model_runtime_projection, local_host_projection, envelope
    principal, identity, decision = _operator_read_context(authorization, x_jarvis_session)
    pending = CANONICAL_HOST_APPROVAL_STORE.pending_for_session(principal.session_id)
    session_context = CANONICAL_SESSION_CONTEXT.read(principal.session_id, identity)
    return {"schema_version": "operator_shell_read.v1", "read_only": True,
            "identity": {"identity_id": principal.identity_id, "session_id": principal.session_id,
                         "role": principal.profile_type, "verified": True},
            "exposure": {"read_permission": decision.to_read_model(),
                         "scope": "owner-only authenticated projection", "direct_execution_allowed": False,
                         "action_path": "/jarvis-live/hot; per-step policy; exact HOST approvals",
                         "unsupported_roles": "AUTH_DENIED; no inferred family/admin grants"},
            "foundation": foundation_projection(PROJECT_ROOT),
            "models": model_runtime_projection(),
            "local_host": local_host_projection(PROJECT_ROOT),
            "session_memory": envelope(len(session_context.get("bounded_chronological_turns", ())),
                source="MAKSIMAR_SERVER/AI_ORCHESTRATION/session_memory_store.py:CanonicalSessionContextStore.read",
                produced_at=datetime.now(UTC).isoformat(), unit="bounded_same_session_turns", max_age_seconds=15, status="LIVE"),
            "settings": supervisor_settings_projection(),
            "approvals": {"pending_count": len(pending), "pending": [p.to_read_model() for p in pending],
                          "scope": "this exact authenticated session only; no global cross-session count"},
            "observed": envelope(True, source="CONTROL_PLANE/api_server.py", produced_at=datetime.now(UTC).isoformat(), status="LIVE")}


@app.get("/operator-shell/approvals/{approval_id}")
def operator_shell_approval(approval_id: str, authorization: str | None = Header(default=None),
                            x_jarvis_session: str | None = Header(default=None)):
    principal, _, _ = _operator_read_context(authorization, x_jarvis_session)
    record = CANONICAL_HOST_APPROVAL_STORE.get(approval_id)
    if record is None or record.session_id != principal.session_id:
        raise HTTPException(404, "approval_not_found_in_session")
    return {"read_only": True, "approval": record.to_read_model()}


@app.get("/operator-shell/events")
def operator_shell_events(cursor: str = "", limit: int = 100,
                          authorization: str | None = Header(default=None),
                          x_jarvis_session: str | None = Header(default=None)):
    from MAKSIMAR_SERVER.OBSERVABILITY.operator_shell_read_model import event_projection
    _operator_read_context(authorization, x_jarvis_session)
    return event_projection(cursor=cursor, limit=limit)
PROJECT_ROOT = Path(__file__).resolve().parents[1]
API_LOG_FILE = PROJECT_ROOT / ".runtime" / "jarvis_live" / "api.log"
PROJECT_UNDERSTANDING_ADAPTER = ExistingProjectUnderstandingAdapter()
MEMORY_RETRIEVAL_ADAPTER = ExistingMemoryRetrievalAdapter()
SIMULATION_WORKER_ADAPTER = ExistingSimulationWorkerAdapter()
N8N_ADAPTER = ExistingN8nAdapter()
MODEL_ROLE_ADAPTER = ExistingOllamaModelRoleAdapter()
MEDIA_PROVIDER_ADAPTER = ExistingFfprobeMediaAdapter()
BROWSER_PROVIDER_ADAPTER = ExistingPlaywrightBrowserAdapter()
WINDOWS_EDGE_ADAPTER = ExistingWindowsEdgeAdapter()
CONVERSATION_EVIDENCE_ADAPTER = ExistingConversationEvidenceAdapter()
MODEL_UNDERSTANDING_ADAPTER = ExistingOllamaModelUnderstandingAdapter(
    json_schema=REQUEST_UNDERSTANDING_JSON_SCHEMA,
    candidate_json_schema=CANDIDATE_DISCOVERY_JSON_SCHEMA,
    kind_json_schema=KIND_DISCOVERY_JSON_SCHEMA,
)
PROJECT_READ_PERMISSION = SemanticPolicyEvaluator()
FINAL_BRAIN_ADAPTER = ExistingFinalBrainAdapter()
CANONICAL_SESSION_CONTEXT = CanonicalSessionContextStore()


def _legacy_runtime_readiness_payload() -> dict[str, Any]:
    """Health-only legacy boundary; it is not reachable from the canonical /hot turn."""
    payload = build_runtime_readiness_payload(control_plane_alive=True)
    payload["browser_provider_available"] = BROWSER_PROVIDER_ADAPTER.health().get("status") == "AVAILABLE"
    return payload


def _existing_capability_catalog(*, readonly_catalog: dict[str, Any] | None = None,
                                 external_visibility: dict[str, Any] | None = None) -> dict[str, Any]:
    """Inventory read boundary; it performs typed grouping only."""
    return build_existing_capability_catalog(
        readonly_catalog=readonly_catalog, external_visibility=external_visibility,
    )


def _semantic_capability_projection() -> dict[str, Any]:
    """Compose the existing inventory with the existing runtime readiness owner."""
    return build_semantic_capability_registry_projection(
        readiness=_legacy_runtime_readiness_payload(),
    )


def _prewarm_semantic_capability_inventory() -> None:
    """Pay the static inventory scan at runtime startup, never on the first owner turn."""
    projection = _semantic_capability_projection()
    if int(projection.get("capability_count", 0)) <= 0:
        raise RuntimeError("semantic_capability_inventory_prewarm_empty")


def _legacy_readonly_adapter() -> Any:
    module_name = (
        "MAKSIMAR_SERVER.AI_ORCHESTRATION."
        "jarvis_live_"
        "brain_loop_"
        "server_adapter"
    )
    return import_module(module_name)


def _identity_from_hot_payload(payload: dict[str, Any], session_id: str) -> Any:
    """Resolve HOST identity only from a verified principal, never JSON claims."""
    verified = identity_from_host_token(str(payload.get("host_auth_token", "")))
    if verified is None:
        return IdentityContext("anonymous", "http_unverified", "unknown", False, False, "", "JARVIS")
    principal, identity = verified
    if principal.session_id != session_id:
        return IdentityContext("anonymous", "http_unverified", "unknown", False, False, "", "JARVIS")
    return identity


@app.get("/")
def root():
    return {"status": "MAKSIMAR control plane online"}


@app.get("/health")
def health():
    root = str(Path(__file__).resolve().parents[1])
    snap = take_snapshot(root)

    return {"ok": True, "health": snap.as_dict()}


@app.get("/health/latency")
def health_latency():
    t0 = time.perf_counter()
    dt_ms = (time.perf_counter() - t0) * 1000.0

    return {"ok": True, "latency_ms": dt_ms}


@app.get("/jarvis-live/health")
def jarvis_live_health() -> dict[str, Any]:
    health_payload = _legacy_readonly_adapter().build_jarvis_live_brain_health()
    memory = dict(health_payload.get("memory_federation", {}))
    readiness = _legacy_runtime_readiness_payload()
    return {
        "ok": True,
        "surface": "CONTROL_PLANE/api_server.py",
        "hotpath_runtime": "CONTROL_PLANE/canonical_semantic_spine.py",
        "brain_loop": "tools/jarvis_live_runtime/jarvis_live_brain_loop.py",
        "default_model": health_payload.get("default_model", "jarvis:chat8b"),
        "primary_conversation_model": health_payload.get("primary_conversation_model", "jarvis:chat8b"),
        "fallback_model": health_payload.get("fallback_model", "jarvis-live:qwen14b"),
        "heavy_coder_model": health_payload.get("heavy_coder_model", "jarvis:coder14b"),
        "memory_federation_available": memory.get("memory_federation_available", False),
        "memory_surfaces_detected_count": memory.get("memory_surfaces_detected_count", 0),
        "active_retrieval_surfaces": memory.get("active_retrieval_surfaces", ()),
        "disabled_memory_surfaces": memory.get("disabled_memory_surfaces", ()),
        "sandbox_only_memory_surfaces": memory.get("sandbox_only_memory_surfaces", ()),
        "vector_memory_available": memory.get("vector_memory_available", False),
        "regulatory_memory_available": memory.get("regulatory_memory_available", False),
        "business_memory_available": memory.get("business_memory_available", False),
        "mempalace_status": memory.get("mempalace_status", "not_detected"),
        "runtime_history_store_exists": memory.get("runtime_history_store_exists", False),
        "session_memory_exists": memory.get("session_memory_exists", False),
        "canonical_memory_write_allowed": False,
        **readiness,
        "health": health_payload,
    }

@app.get("/jarvis-live/status")
def jarvis_live_status() -> dict[str, Any]:
    from dataclasses import asdict
    from MAKSIMAR_SERVER.MEMORY_REGISTRY.global_registry_projection_builder import build_memory_component_inventory_projection
    from MAKSIMAR_SERVER.MEMORY_REGISTRY.global_registry_projection_models import MEMORY_COMPONENT_INVENTORY_SCOPE
    components = tuple(asdict(item) for item in build_memory_component_inventory_projection())
    session_payload = _legacy_readonly_adapter().build_jarvis_live_session_status()
    memory = dict(session_payload.get("memory_federation", {}))
    readiness = _legacy_runtime_readiness_payload()
    return {
        "ok": True,
        "surface": "CONTROL_PLANE/api_server.py",
        "default_model": session_payload.get("default_model", "jarvis:chat8b"),
        "primary_conversation_model": session_payload.get("primary_conversation_model", "jarvis:chat8b"),
        "fallback_model": session_payload.get("fallback_model", "jarvis-live:qwen14b"),
        "heavy_coder_model": session_payload.get("heavy_coder_model", "jarvis:coder14b"),
        "memory_federation_available": memory.get("memory_federation_available", False),
        "memory_surfaces_detected_count": memory.get("memory_surfaces_detected_count", 0),
        "active_retrieval_surfaces": memory.get("active_retrieval_surfaces", ()),
        "disabled_memory_surfaces": memory.get("disabled_memory_surfaces", ()),
        "sandbox_only_memory_surfaces": memory.get("sandbox_only_memory_surfaces", ()),
        "vector_memory_available": memory.get("vector_memory_available", False),
        "regulatory_memory_available": memory.get("regulatory_memory_available", False),
        "business_memory_available": memory.get("business_memory_available", False),
        "mempalace_status": memory.get("mempalace_status", "not_detected"),
        "runtime_history_store_exists": memory.get("runtime_history_store_exists", False),
        "session_memory_exists": memory.get("session_memory_exists", False),
        "recent_turn_count": session_payload.get("recent_turn_count", 0),
        "logical_components": components,
        "logical_component_count": len(components),
        "component_inventory_scope": MEMORY_COMPONENT_INVENTORY_SCOPE,
        "canonical_memory_write_allowed": False,
        **readiness,
        "session": session_payload,
    }


@app.get("/jarvis-live/readiness")
def jarvis_live_readiness() -> dict[str, Any]:
    return {
        "ok": True,
        "surface": "CONTROL_PLANE/api_server.py",
        "readiness": _legacy_runtime_readiness_payload(),
    }


@app.get("/jarvis-live/project")
def jarvis_live_project() -> dict[str, Any]:
    return {
        "ok": True,
        "surface": "CONTROL_PLANE/api_server.py",
        "project": _legacy_readonly_adapter().build_project_workspace_read_model(),
        "read_only": True,
    }


@app.get("/jarvis-live/project/status")
def jarvis_live_project_status() -> dict[str, Any]:
    return {
        "ok": True,
        "surface": "CONTROL_PLANE/api_server.py",
        "project_status": _legacy_readonly_adapter().build_jarvis_live_project_status_read_model(),
        "read_only": True,
    }


@app.get("/jarvis-live/project/tree")
def jarvis_live_project_tree(depth: int = 2, max_entries: int = 300) -> dict[str, Any]:
    return {
        "ok": True,
        "surface": "CONTROL_PLANE/api_server.py",
        "tree": _legacy_readonly_adapter().repo_tree(depth=depth, max_entries=max_entries),
        "read_only": True,
    }


@app.get("/jarvis-live/project/files")
def jarvis_live_project_files(page: int = 1, page_size: int = 80) -> dict[str, Any]:
    return {
        "ok": True,
        "surface": "CONTROL_PLANE/api_server.py",
        "files": _legacy_readonly_adapter().repo_files(page=page, page_size=page_size),
        "read_only": True,
    }


@app.get("/jarvis-live/project/dirty")
def jarvis_live_project_dirty() -> dict[str, Any]:
    status = _legacy_readonly_adapter().repo_git_status()
    return {
        "ok": True,
        "surface": "CONTROL_PLANE/api_server.py",
        "dirty_files": status.get("dirty_files", ()),
        "untracked_files": status.get("untracked_files", ()),
        "staged_files": status.get("staged_files", ()),
        "diff_name_only": status.get("diff_name_only", ()),
        "diff_stat": status.get("diff_stat", ""),
        "read_only": True,
    }


@app.get("/jarvis-live/project/search")
def jarvis_live_project_search(q: str = "", path: str = "", max_results: int = 40) -> dict[str, Any]:
    paths = tuple(part for part in path.split(",") if part.strip()) if path else None
    return {
        "ok": True,
        "surface": "CONTROL_PLANE/api_server.py",
        "search": _legacy_readonly_adapter().repo_search(q, paths=paths, max_results=max_results),
        "read_only": True,
    }


@app.get("/jarvis-live/project/file")
def jarvis_live_project_file(path: str, start_line: int = 1, end_line: int | None = None, page: int = 1) -> dict[str, Any]:
    return {
        "ok": True,
        "surface": "CONTROL_PLANE/api_server.py",
        "file": _legacy_readonly_adapter().read_file_snippet(path, start_line=start_line, end_line=end_line, page=page),
        "read_only": True,
    }


@app.get("/jarvis-live/project/outline")
def jarvis_live_project_outline(path: str) -> dict[str, Any]:
    return {
        "ok": True,
        "surface": "CONTROL_PLANE/api_server.py",
        "outline": _legacy_readonly_adapter().read_file_outline(path),
        "read_only": True,
    }


@app.get("/jarvis-live/project/imports")
def jarvis_live_project_imports(path: str | None = None, max_edges: int = 80) -> dict[str, Any]:
    return {
        "ok": True,
        "surface": "CONTROL_PLANE/api_server.py",
        "imports": _legacy_readonly_adapter().repo_import_graph(path=path, max_edges=max_edges),
        "read_only": True,
    }


@app.get("/jarvis-live/project/tests")
def jarvis_live_project_tests() -> dict[str, Any]:
    model = _legacy_readonly_adapter().build_project_workspace_read_model()
    test_files = model.get("domain_groups", {}).get("tests", ())
    return {
        "ok": True,
        "surface": "CONTROL_PLANE/api_server.py",
        "test_file_count": len(test_files),
        "test_files": test_files,
        "project": model,
        "read_only": True,
    }


@app.get("/jarvis-live/project/roadmap")
def jarvis_live_project_roadmap() -> dict[str, Any]:
    return {
        "ok": True,
        "surface": "CONTROL_PLANE/api_server.py",
        "status": _legacy_readonly_adapter().status_tools(),
        "read_only": True,
    }


@app.get("/jarvis-live/project/models")
def jarvis_live_project_models() -> dict[str, Any]:
    return jarvis_live_models()


@app.get("/jarvis-live/project/safety")
def jarvis_live_project_safety() -> dict[str, Any]:
    terms = ("runtime_mutation_allowed", "direct_execution_allowed", "approval", "pc_control_allowed", "watchdog", "core guard", "OOB", "safety", "security")
    results: list[dict[str, Any]] = []
    seen: set[tuple[str, int]] = set()
    for term in terms:
        for result in _legacy_readonly_adapter().repo_search(term, max_results=8)["results"]:
            key = (str(result["path"]), int(result["line_number"]))
            if key in seen:
                continue
            seen.add(key)
            results.append(result)
            if len(results) >= 30:
                break
        if len(results) >= 30:
            break
    return {
        "ok": True,
        "surface": "CONTROL_PLANE/api_server.py",
        "safety_matches": tuple(results),
        "canonical_memory_write_allowed": False,
        "pc_control_allowed": False,
        "api_log_file": str(API_LOG_FILE),
        "read_only": True,
    }


@app.get("/jarvis-live/memory")
def jarvis_live_memory() -> dict[str, Any]:
    adapter = _legacy_readonly_adapter()
    session_payload = adapter.build_jarvis_live_session_status()
    return {
        "ok": True,
        "surface": "CONTROL_PLANE/api_server.py",
        "session": session_payload,
        "brain_health": adapter.build_jarvis_live_brain_health(),
        "read_only": True,
    }


@app.get("/jarvis-live/models")
def jarvis_live_models() -> dict[str, Any]:
    if model_free_startup():
        raise HTTPException(status_code=503, detail={
            "status": "UNAVAILABLE", "reason": "model_free_startup",
        })
    return {
        "ok": True,
        "surface": "CONTROL_PLANE/api_server.py",
        "models": _legacy_readonly_adapter().model_runtime_status(),
        "read_only": True,
    }


@app.get("/jarvis-live/tools")
def jarvis_live_tools() -> dict[str, Any]:
    raw_legacy_catalog = _legacy_readonly_adapter().build_jarvis_live_tool_catalog_read_model()
    legacy_catalog = dict(raw_legacy_catalog)
    external_visibility = legacy_catalog.pop("_external_visibility", None)
    dispatcher_catalog = _existing_capability_catalog(
        readonly_catalog=legacy_catalog, external_visibility=external_visibility,
    )
    merged_tools = {
        **legacy_catalog,
        "catalog_id": dispatcher_catalog["catalog_id"],
        "source": dispatcher_catalog["source"],
        "capability_visible_count": dispatcher_catalog["capability_visible_count"],
        "capability_direct_count": dispatcher_catalog["capability_direct_count"],
        "counts_by_capability_kind": dispatcher_catalog["counts_by_capability_kind"],
        "counts_by_status": dispatcher_catalog["counts_by_status"],
    }
    return {
        "ok": True,
        "surface": "CONTROL_PLANE/api_server.py",
        "source": "existing_capability_inventory",
        "counts_by_capability_kind": dispatcher_catalog["counts_by_capability_kind"],
        "counts_by_status": dispatcher_catalog["counts_by_status"],
        "direct_pc_actions": dispatcher_catalog["direct_pc_actions"],
        "readonly_tools": dispatcher_catalog["readonly_tools"],
        "memory_tools": dispatcher_catalog["memory_tools"],
        "retrieval_backends": dispatcher_catalog["retrieval_backends"],
        "skills": dispatcher_catalog["skills"],
        "agents": dispatcher_catalog["agents"],
        "workers": dispatcher_catalog["workers"],
        "external_adapters": dispatcher_catalog["external_adapters"],
        "workflow_automation": dispatcher_catalog["workflow_automation"],
        "runtime_tooling": dispatcher_catalog["runtime_tooling"],
        "runtime_voice": dispatcher_catalog["runtime_voice"],
        "runtime_windows_edge": dispatcher_catalog["runtime_windows_edge"],
        "jarvis_runtime_library": dispatcher_catalog["jarvis_runtime_library"],
        "external_tools": dispatcher_catalog["external_tools"],
        "protected_tools": dispatcher_catalog["protected_tools"],
        "unavailable_capabilities": dispatcher_catalog["unavailable_capabilities"],
        "capability_visible_count": dispatcher_catalog["capability_visible_count"],
        "capability_direct_count": dispatcher_catalog["capability_direct_count"],
        "external_code_commit_policy": dispatcher_catalog["external_code_commit_policy"],
        "tools": merged_tools,
        "legacy_tools": legacy_catalog,
        "read_only": True,
    }


@app.get("/jarvis-live/logs")
def jarvis_live_logs() -> dict[str, Any]:
    return {
        "ok": True,
        "surface": "CONTROL_PLANE/api_server.py",
        "api_log_file": str(API_LOG_FILE),
        "read_only": True,
    }


@app.get("/jarvis-live/inflight-traces")
def jarvis_live_inflight_traces(trace_id: str | None = None) -> dict[str, Any]:
    return in_flight_trace_read_model(trace_id)


def _capture_canonical_turn_memory(
    canonical: dict[str, Any], payload: dict[str, Any], session_id: str,
    identity: Any, text: str, response_text: str,
) -> dict[str, Any]:
    """One existing durable capture path for ordinary and streaming canonical turns."""
    understanding = canonical.get("understanding") if isinstance(canonical.get("understanding"), dict) else {}
    created_artifact = _extract_created_workflow_artifact(canonical)
    evidence = canonical.get("evidence_bundle") if isinstance(canonical.get("evidence_bundle"), dict) else {}
    browser_items = evidence.get("items", ()) if isinstance(evidence, dict) else ()
    proposal_audit = None
    proposal_learning = None
    learning_bundle = None
    learning_bundle_intake = None
    simulation_learning = None
    simulation_learning_bundle = None
    simulation_learning_intake = None
    proposal_items = [item for item in evidence.get("items", ())
                      if isinstance(item, dict) and item.get("kind") == "code_proposal"]
    if proposal_items:
        proposal_item = proposal_items[0]
        proposal_audit = audit_proposal_runtime({
            "proposal_id": str(canonical.get("trace_id", "proposal")),
            "proposal": str(proposal_item.get("observation", "")),
            "observed_problem_refs": (str(proposal_item.get("content_hash", "")),),
            "affected_components": (str(proposal_item.get("source_reference", "")),),
        })
        audit_ref = "audit://proposal/" + str(canonical.get("trace_id", ""))
        try:
            proposal_observation = json.loads(str(proposal_item.get("observation", "{}")))
        except (ValueError, TypeError):
            proposal_observation = {}
        proposal_learning = capture_proposal_experience(
            actor="CODEX" if isinstance(proposal_observation, dict) and proposal_observation.get("compute_provider") == "codex_cli" else "JARVIS", task_ref=text,
            proposal_ref=str(proposal_item.get("content_hash", "proposal")),
            audit_ref=audit_ref,
            verification_ref="evidence://" + str(canonical.get("trace_id", "")),
            experience_kind="ARCHITECTURE_DESIGN",
            # A proposal receipt proves delivery, never independent execution.
            # Real execution/readback qualification has its existing separate owner.
            verified=False,
            audit_verdict=proposal_audit.verdict,
        )
        learning_bundle = build_experience_learning_bundle(
            experience_id=proposal_learning.experience_id,
            actor=proposal_learning.actor,
            audit_verdict=proposal_audit.verdict,
            evidence_refs=tuple(proposal_learning.evidence_refs),
            verification_refs=tuple(proposal_learning.verification_refs),
            created_at=str(proposal_item.get("observed_at", "")) or None,
        )
        learning_bundle_intake = validate_learning_bundle_intake(learning_bundle, proposal_learning)
    # A reviewed simulation is an experience candidate, not canonical truth.
    # Build it only from the execution/review evidence already produced by the
    # canonical turn, then pass it through the existing intake validator.
    simulation_items = [item for item in evidence.get("items", ())
                        if isinstance(item, dict) and item.get("kind") == "simulation_result"]
    review_items = [item for item in evidence.get("items", ())
                    if isinstance(item, dict) and item.get("kind") == "sandbox_review"]
    simulation_receipts = [item for item in evidence.get("receipts", ())
                           if isinstance(item, dict) and item.get("operation_id") == "analyze_simulation"]
    if simulation_items and review_items and simulation_receipts:
        try:
            review_observation = json.loads(str(review_items[0].get("observation", "{}")))
        except (TypeError, ValueError, json.JSONDecodeError):
            review_observation = {}
        if review_observation.get("review_status") == "REVIEWED":
            source_trace = str(canonical.get("trace_id", ""))
            artifact_ref = str(simulation_items[0].get("source_reference", ""))
            review_ref = str(review_items[0].get("source_reference", ""))
            receipt_id = str(simulation_receipts[0].get("receipt_id", ""))
            receipt_ref = "receipt://" + source_trace + "/" + receipt_id
            learning_refs = (artifact_ref, receipt_ref, "trace://" + source_trace)
            simulation_learning = qualify_verified_sandbox_experience(
                actor="JARVIS",
                task_ref="simulation.run/analyze_simulation:" + source_trace,
                evidence_refs=learning_refs,
                provenance_ref="trace://" + source_trace,
                review_ref=review_ref,
                execution_status=str(simulation_receipts[0].get("status", "")),
                review_status=str(review_observation.get("review_status", "")),
            )
            simulation_learning_bundle = build_sandbox_learning_bundle(
                artifact_ref="experience://" + simulation_learning.experience_id,
                sandbox_id="simulation",
                source_actor=simulation_learning.actor,
                evidence_refs=learning_refs,
                evaluation_refs=(review_ref,),
                created_at=str(simulation_items[0].get("observed_at", "")) or None,
                metrics=(("execution_receipt_ref", receipt_ref), ("source_operation", "analyze_simulation"),
                         ("execution_target", "worker_sim_001")),
            )
            simulation_learning_intake = validate_learning_bundle_intake(
                simulation_learning_bundle, simulation_learning,
            )
    def _page_context(item: dict[str, Any]) -> dict[str, Any] | None:
        try:
            observation = json.loads(str(item.get("observation", "{}")))
        except (TypeError, ValueError, json.JSONDecodeError):
            return None
        if not isinstance(observation, dict):
            return None
        url = str(observation.get("url", ""))
        if not url.startswith(("http://", "https://")):
            return None
        return {
        "session_id": session_id, "current_url": url,
        "title": str(observation.get("title", ""))[:200],
        "trace_id": str(canonical.get("trace_id", "")),
        "operation": str(item.get("operation_id", "")),
        "source_reference": str(item.get("source_reference", "")),
        }
    page_context = next((_page_context(item) for item in browser_items if isinstance(item, dict)), None)
    if page_context:
        created_artifact = {**(created_artifact or {}), "browser_page_context": page_context}
    if proposal_learning is not None:
        created_artifact = {
            **(created_artifact or {}),
            "kind": "proposal_experience",
            "learning_experience": proposal_learning.to_read_model(),
            "audit_verdict": proposal_audit.verdict if proposal_audit else "",
            "learning_bundle": learning_bundle.to_dict() if learning_bundle else None,
            "learning_bundle_hash": learning_bundle.content_hash if learning_bundle else "",
            "observed_at": str(proposal_item.get("observed_at", "")),
        }
    if simulation_learning is not None:
        created_artifact = {
            **(created_artifact or {}),
            "kind": "simulation_experience",
            "learning_experience": simulation_learning.to_read_model(),
            "learning_bundle": simulation_learning_bundle.to_dict() if simulation_learning_bundle else None,
            "learning_bundle_hash": simulation_learning_bundle.content_hash if simulation_learning_bundle else "",
            "observed_at": str(simulation_items[0].get("observed_at", "")),
            "audit_verdict": "REVIEWED",
        }
    if proposal_learning is None and simulation_learning is None:
        provider_learning = qualify_provider_execution_experience(
            task_ref=("voice-origin: " if _payload_input_channel(payload) == "voice" else "") + text,
            trace_id=str(canonical.get("trace_id", "")),
            operation_status=str(canonical.get("operation_status", "")), evidence=evidence,
        )
        if provider_learning is not None:
            observed_at = next(str(item["observed_at"]) for item in evidence["items"]
                               if isinstance(item, dict) and item.get("observed_at"))
            provider_bundle = build_experience_learning_bundle(
                experience_id=provider_learning.experience_id, actor=provider_learning.actor,
                audit_verdict="EXECUTION_RECEIPTS_VERIFIED",
                evidence_refs=provider_learning.evidence_refs, verification_refs=provider_learning.verification_refs,
                created_at=observed_at, capability_id=str(evidence.get("capability_id", "")),
                organ_id="canonical_provider_execution",
            )
            learning_bundle_intake = validate_learning_bundle_intake(provider_bundle, provider_learning)
            created_artifact = {**(created_artifact or {}), "kind": "provider_execution_experience",
                "learning_experience": provider_learning.to_read_model(),
                "learning_bundle": provider_bundle.to_dict(), "learning_bundle_hash": provider_bundle.content_hash,
                "observed_at": observed_at, "audit_verdict": "EXECUTION_RECEIPTS_VERIFIED"}
    evidence_step_ids = {item.get("step_id") for item in evidence.get("items", ()) if isinstance(item, dict)}
    durable_receipts = [receipt for receipt in evidence.get("receipts", ()) if isinstance(receipt, dict)
                        and receipt.get("step_id") in evidence_step_ids][:16]
    if durable_receipts:
        created_artifact = {**(created_artifact or {"kind": "execution_receipt_memory"}),
                            "execution_receipts": durable_receipts}
    retrieval_items = [item for item in evidence.get("items", ()) if isinstance(item, dict)
                       and item.get("kind") in {"mempalace_search", "history_search", "session_memory", "local_chat_memory", "memory_federation", "dashboard_memory_models", "memory_domains", "regulatory_memory_foundation", "enterprise_business_memory", "retrieval_backends"}]
    if retrieval_items:
        # Persist only trace/provenance metadata in the existing session log.
        # Document text and provider payloads remain owned by their sources.
        retrieval_sources = []
        for item in retrieval_items[:8]:
            try:
                observation = json.loads(str(item.get("observation", "{}")))
            except (ValueError, TypeError):
                observation = {}
            if item.get("kind") == "mempalace_search" and isinstance(observation, dict):
                for hit in (observation.get("retrieval") or {}).get("results", ())[:3]:
                    retrieval_sources.extend(hit.get("source_readback", ())[:1])
        created_artifact = {**(created_artifact or {"kind": "memory_retrieval_trace"}),
            "retrieval_trace": {"trace_id": str(canonical.get("trace_id", "")),
                "operation_status": str(canonical.get("operation_status", "")),
                "observed_at": retrieval_items[0].get("observed_at"),
                "kinds": [item["kind"] for item in retrieval_items[:8]],
                "evidence_refs": [item.get("source_reference") or item.get("content_hash") for item in retrieval_items[:8]],
                "content_hashes": [item.get("content_hash") for item in retrieval_items[:8]],
                "source_refs": [item.get("source_reference") for item in retrieval_items[:8]],
                "sources": retrieval_sources[:3],
                "receipt_count": len(evidence.get("receipts", ())), "payload_copied": False}}
    session_event = CANONICAL_SESSION_CONTEXT.append(
        session_id, identity, user_text=text, assistant_text=response_text,
        topic=str(understanding.get("current_topic", "")),
        unresolved_reference=str(understanding.get("unresolved_reference", "")),
        trace_id=str(canonical.get("trace_id", "")),
        artifact=created_artifact,
    )
    capture = {"session_event": session_event,
               "learning_bundle": learning_bundle_intake or simulation_learning_intake}
    if proposal_audit is not None:
        capture["proposal_audit"] = proposal_audit.to_read_model()
        capture["proposal_learning"] = proposal_learning.to_read_model() if proposal_learning else None
    if simulation_learning is not None:
        capture["simulation_learning"] = simulation_learning.to_read_model()
        capture["simulation_learning_bundle"] = simulation_learning_bundle.to_dict() if simulation_learning_bundle else None
        capture["simulation_learning_bundle_hash"] = simulation_learning_bundle.content_hash if simulation_learning_bundle else ""
        capture["simulation_learning_intake"] = simulation_learning_intake
    return capture


def _payload_understanding_attempt_policy(payload: dict[str, Any]) -> UnderstandingAttemptPolicy:
    value = payload.get("understanding_attempt_policy")
    if value is None:
        return UnderstandingAttemptPolicy()
    if not isinstance(value, dict) or set(value) - {"max_model_attempts", "schema_max_attempts"}:
        raise ValueError("understanding_attempt_policy_invalid")
    return UnderstandingAttemptPolicy(**value)



class _HotRequestRoute(APIRoute):
    """Native lifetime of the existing /hot route; sole upstream receive owner."""

    async def handle(self, scope, receive, send):
        deadline = RequestDeadline(CANONICAL_TURN_TIMEOUT_SECONDS)
        tx, rx = anyio.create_memory_object_stream(1)
        disconnected = False

        async def receive_messages():
            nonlocal disconnected
            async with tx:
                while True:
                    message = await receive()
                    if message["type"] == "http.disconnect":
                        disconnected = True
                        deadline.cancel()
                    await tx.send(message)
                    if message["type"] == "http.disconnect":
                        return

        async def guarded_send(message):
            nonlocal disconnected
            # Empty framing closes a completed stream, it publishes no answer.
            terminal_frame = (message["type"] == "http.response.body"
                              and not message.get("body") and not message.get("more_body", False))
            if disconnected or not terminal_frame:
                deadline.check()
            try:
                await send(message)
            except OSError:
                disconnected = True
                deadline.cancel()
                raise

        with deadline.bind():
            try:
                async with rx, anyio.create_task_group() as tasks:
                    tasks.start_soon(receive_messages)
                    try:
                        await super().handle(scope, rx.receive, guarded_send)
                    except (OSError, TimeoutError, ClientDisconnect):
                        if not deadline.cancelled:
                            raise
                    finally:
                        tasks.cancel_scope.cancel()
            finally:
                # Local caller cancellation is not provider abort or VRAM release.
                deadline.cancel()


class _HotStreamingResponse(StreamingResponse):
    """Finalize this response's sync iterator even if ASGI send fails."""

    def __init__(self, lines: Iterable[str], deadline: RequestDeadline):
        super().__init__(lines, media_type="application/x-ndjson")
        self._owned_lines = lines
        self._request_deadline = deadline

    async def __call__(self, scope, receive, send):
        try:
            await super().__call__(scope, receive, send)
        finally:
            self._request_deadline.cancel()
            # Native threadpool calls are joined; do not rely on GC to close
            # a retained sync generator, or claim that this aborts a backend.
            with anyio.CancelScope(shield=True), self._request_deadline.bind():
                try:
                    close = getattr(self._owned_lines, "close", None)
                    if callable(close):
                        await run_in_threadpool(close)
                finally:
                    await self.body_iterator.aclose()


def _hot_request_deadline(payload: dict[str, Any]) -> RequestDeadline:
    if set(payload) & {"request_deadline", "deadline", "total_timeout_seconds"}:
        raise ValueError("client_request_deadline_authority_forbidden")
    policy = _payload_understanding_attempt_policy(payload)
    deadline = RequestDeadline.current()
    if deadline is None:
        deadline = RequestDeadline(CANONICAL_TURN_TIMEOUT_SECONDS, understanding_attempt_policy=policy)
    deadline.bind_attempt_policy(policy)
    deadline.check()
    return deadline


def _hot_request_scope(function):
    @wraps(function)
    def scoped(payload):
        payload = {**payload, "trace_id": str(payload.get("trace_id") or f"trace_{time.time_ns()}")}
        deadline = _hot_request_deadline(payload)
        with deadline.bind():
            try:
                result = function(payload)
                deadline.check()
                return result
            except TimeoutError:
                if not deadline.cancelled:
                    raise
                record_in_flight_trace_event(payload["trace_id"], "HTTP_REQUEST_CANCELLED", "CANCELLED",
                    caller_cancelled=True, provider_operation_terminated="UNKNOWN",
                    residency_released="UNKNOWN", resource_available="UNKNOWN")
                return {"ok": False, "operation_status": "CANCELLED",
                        "error_kind": "canonical_request_cancelled_or_expired"}
    return scoped


@_hot_request_scope
def jarvis_live_hot(payload: dict[str, Any]) -> Any:
    if _payload_stream_requested(payload):
        return _HotStreamingResponse(_hot_stream_lines(payload, RequestDeadline.current()), RequestDeadline.current())
    text = _payload_text(payload)
    session_id = _payload_session_id(payload)
    trace_id = str(payload.get("trace_id") or f"trace_{time.time_ns()}")
    set_in_flight_trace(trace_id)
    record_in_flight_trace_event(trace_id, "HTTP_REQUEST_ACCEPTED")
    record_in_flight_trace_event(trace_id, "CANONICAL_TURN_STARTED")
    identity = _identity_from_hot_payload(payload, session_id)
    session_context = CANONICAL_SESSION_CONTEXT.read(session_id, identity)
    RequestDeadline.current().check()
    registry_projection = _semantic_capability_projection()
    RequestDeadline.current().check()
    canonical = run_canonical_semantic_turn(
        text=text,
        project_port=PROJECT_UNDERSTANDING_ADAPTER,
        conversation_port=CONVERSATION_EVIDENCE_ADAPTER,
        model_port=MODEL_UNDERSTANDING_ADAPTER,
        final_brain_port=FINAL_BRAIN_ADAPTER,
        permission_port=PROJECT_READ_PERMISSION,
        identity=identity,
        session_context=session_context,
        input_channel=_payload_input_channel(payload),
        input_quality_metadata=_payload_input_quality_metadata(payload),
        understanding_attempt_policy=_payload_understanding_attempt_policy(payload),
        request_deadline=RequestDeadline.current(),
        registry_projection=registry_projection,
        trace_id=trace_id,
        provider_ports={
            PROJECT_UNDERSTANDING_ADAPTER.provider_id: PROJECT_UNDERSTANDING_ADAPTER,
            MEMORY_RETRIEVAL_ADAPTER.provider_id: MEMORY_RETRIEVAL_ADAPTER,
            SIMULATION_WORKER_ADAPTER.provider_id: SIMULATION_WORKER_ADAPTER,
            MODEL_ROLE_ADAPTER.provider_id: MODEL_ROLE_ADAPTER,
            MEDIA_PROVIDER_ADAPTER.provider_id: MEDIA_PROVIDER_ADAPTER,
            WINDOWS_EDGE_ADAPTER.provider_id: WINDOWS_EDGE_ADAPTER,
            CONVERSATION_EVIDENCE_ADAPTER.provider_id: CONVERSATION_EVIDENCE_ADAPTER,
            N8N_ADAPTER.provider_id: N8N_ADAPTER,
            BROWSER_PROVIDER_ADAPTER.provider_id: BROWSER_PROVIDER_ADAPTER,
        },
        session_id=session_id,
    )
    RequestDeadline.current().check()
    record_in_flight_trace_event(trace_id, "CANONICAL_TURN_COMPLETED", status=str(canonical.get("capability_status", "UNKNOWN")))
    expected_capability_id = str(payload.get("expected_capability_id") or "").strip()
    if expected_capability_id:
        selected = tuple(str(item) for item in canonical.get("selected_capabilities", ()))
        projected_ids = {str(item.get("capability_id")) for item in registry_projection.get("entries", ())}
        if expected_capability_id not in projected_ids or expected_capability_id not in selected:
            canonical = dict(canonical)
            canonical["operation_status"] = "SAFETY_VALIDATION_FAILED"
            canonical["capability_status"] = "SAFETY_VALIDATION_FAILED"
            canonical["response_text"] = (
                "Canonical capability invocation failed closed: selected capability did not match "
                "the workflow's expected capability contract."
            )
            canonical["expected_capability_validation"] = {
                "status": "MISMATCH", "expected_capability_id": expected_capability_id,
                "selected_capability_ids": selected,
            }
    response_text = str(canonical.get("response_text", "")).strip()
    pc_truth = _pc_turn_truth(canonical, identity)
    understanding = canonical.get("understanding") if isinstance(canonical.get("understanding"), dict) else {}
    sandbox_selection = None
    sandbox_requirement = requirement_from_semantic_understanding(understanding)
    if sandbox_requirement is not None:
        sandbox_selection = select_sandbox(sandbox_requirement)
    RequestDeadline.current().check()
    capture = _capture_canonical_turn_memory(canonical, payload, session_id, identity, text, response_text)
    result = {
        "ok": bool(response_text), "route": "CANONICAL_SEMANTIC_TURN",
        "intent_family": "GENERAL_SEMANTIC_TURN", "llm_response": response_text,
        "response_text": response_text,
        "read_only": str(understanding.get("effect_type", "UNKNOWN")) == "OBSERVE",
        "direct_allowed": canonical.get("operation_status") == "COMPLETE",
        "approval_required": canonical.get("operation_status") in {"APPROVAL_REQUIRED", "PARTIAL_APPROVAL_REQUIRED"},
        "canonical_memory_write_allowed": False,
        "error_kind": "" if canonical.get("operation_status") == "COMPLETE" else canonical.get("operation_status", ""),
        "learning_bundle": capture.get("learning_bundle"),
        "sandbox_selection": sandbox_selection,
        "session_event": capture["session_event"], **canonical, **pc_truth,
    }
    result.update(capture)
    result.update(_selected_registry_projection(canonical, registry_projection))
    return {
        "ok": True,
        "surface": "CONTROL_PLANE/api_server.py",
        "streaming": False,
        "legacy_command_path_used": False,
        "result": result,
        "route": result.get("route", "DIRECT_DIALOG"),
        "intent_family": result.get("intent_family", "CONVERSATION"),
        "llm_response": result.get("llm_response", ""),
        "response_text": result.get("response_text", result.get("llm_response", "")),
        "pc_control_allowed": bool(result.get("pc_operation_authorized_for_this_turn", False))
        and bool(result.get("pc_executor_available", False)),
        "live_hotpath_enabled": bool(result.get("live_hotpath_enabled", True)),
        "direct_dialog_allowed": bool(result.get("direct_dialog_allowed", True)),
        "direct_ollama_allowed": bool(result.get("direct_ollama_allowed", True)),
        "owner_pc_action_eligible": result["owner_pc_action_eligible"],
        "policy_execution_allowed": result["policy_execution_allowed"],
        "pc_executor_available": result["pc_executor_available"],
        "pc_operation_authorized_for_this_turn": result["pc_operation_authorized_for_this_turn"],
        "executed": result["executed"],
        "execution_receipt": result["execution_receipt"],
        "project_readonly_allowed": bool(result.get("project_readonly_allowed", True)),
        "protected_mutation_required": bool(result.get("protected_mutation_required", False)),
        "selected_capability_id": result.get("selected_capability_id", ""),
        "selected_capability_kind": result.get("selected_capability_kind", ""),
        "selected_tool_id": result.get("selected_tool_id", ""),
        "selected_skill_id": result.get("selected_skill_id", ""),
        "selected_agent_id": result.get("selected_agent_id", ""),
        "selected_memory_tool_id": result.get("selected_memory_tool_id", ""),
        "selected_retrieval_tool_id": result.get("selected_retrieval_tool_id", ""),
        "selection_source": result.get("selection_source", ""),
        "capability_status": result.get("capability_status", ""),
        "approval_required": bool(result.get("approval_required", False)),
        "direct_allowed": bool(result.get("direct_allowed", False)),
        "execution_policy": result.get("execution_policy", ""),
        "capability_visible_count": int(result.get("capability_visible_count", 0)),
        "canonical_write_allowed": False,
        "canonical_memory_write_allowed": bool(result.get("canonical_memory_write_allowed", False)),
        "pending_memory_write_proposal": bool(result.get("pending_memory_write_proposal", False)),
        "memory_write_completed": bool(result.get("memory_write_completed", False)),
        "error_kind": result.get("error_kind", ""),
        "orchestration_path": result.get("orchestration_path", "legacy_rollback"),
        "trace_id": result.get("trace_id", ""),
        "understanding_schema_version": result.get("understanding_schema_version", ""),
        "selected_capabilities": tuple(result.get("selected_capabilities", ())),
        "fallback_used": bool(result.get("fallback_used", False)),
        "fallback_reason": result.get("fallback_reason", ""),
        "orchestration_trace": result.get("trace", result.get("orchestration_trace", {})),
        "evidence_bundle": result.get("evidence_bundle"),
        "execution_plan": result.get("execution_plan"),
        "selected_provider_operation": result.get("selected_provider_operation", ()),
        "operation_status": result.get("operation_status", ""),
        "project_tools_used": bool(result.get("project_tools_used", False)),
        "session_event": result.get("session_event"),
        "pending_approvals": result.get("pending_approvals", ()),
    }


app.router.add_api_route("/jarvis-live/hot", jarvis_live_hot, methods=["POST"],
                         route_class_override=_HotRequestRoute)


@app.get("/jarvis-live/approvals/{approval_id}")
def get_pending_approval(approval_id: str) -> dict[str, Any]:
    """Read one bounded HOST approval challenge (never grants authority)."""
    record = CANONICAL_HOST_APPROVAL_STORE.get(approval_id)
    if record is None:
        return {"ok": False, "status": "NOT_FOUND"}
    return {"ok": True, "approval": record.to_read_model()}


@app.post("/jarvis-live/approvals/{approval_id}")
def decide_pending_approval(approval_id: str, payload: dict[str, Any]) -> dict[str, Any]:
    """HOST approval action; approval is bound to the stored exact PlanStep."""
    approved = payload.get("decision") == "approve"
    if payload.get("decision") not in {"approve", "deny"}:
        return {"ok": False, "status": "INVALID_DECISION"}
    # Authority comes from the existing HOST identity contract, never from a
    # caller-supplied approver_id.  HTTP/UI approval requires an authenticated
    # trusted owner session and must match the pending session binding.
    verified = identity_from_host_token(str(payload.get("host_auth_token", "")))
    if verified is None:
        return {"ok": False, "status": "UNAUTHORIZED", "reason": "verified_host_principal_required"}
    principal, approval_identity = verified
    session_id = _payload_session_id(payload)
    if session_id != principal.session_id:
        return {"ok": False, "status": "DENIED", "reason": "approval_session_mismatch"}
    approver_id = principal.identity_id
    try:
        record, decision, resumed = CANONICAL_HOST_APPROVAL_STORE.decide(
            approval_id, approved=approved, approver_id=approver_id, session_id=session_id,
        )
    except (KeyError, ValueError) as exc:
        return {"ok": False, "status": "DENIED", "reason": str(exc)}
    memory_capture = None
    if (record.status == "CONSUMED" and isinstance(resumed, dict)
            and isinstance(resumed.get("evidence_bundle"), dict)
            and isinstance(resumed.get("execution_plan"), dict)):
        # Reuse the ordinary/stream capture owner for this exact HOST continuation.
        # Identity, session and trace come from the authenticated stored approval;
        # task text comes from its canonical callback, never the approval payload.
        canonical = {
            **resumed, "trace_id": record.trace_id, "request_id": record.request_id,
            "operation_status": str(resumed.get("status", "")),
        }
        memory_capture = _capture_canonical_turn_memory(
            canonical, {}, record.session_id, approval_identity,
            str(resumed.get("input_text", record.description)), "",
        )
    return {
        "ok": True, "status": record.status, "approval": record.to_read_model(),
        "permission_decision": decision.to_read_model() if decision else None,
        "resumed": resumed, "memory_capture": memory_capture,
    }


def _payload_stream_requested(payload: dict[str, Any]) -> bool:
    return payload.get("stream") is True or payload.get("response_mode") == "stream"


def _selected_registry_projection(
    canonical: dict[str, Any], registry_projection: dict[str, Any],
) -> dict[str, Any]:
    selected = tuple(str(value) for value in canonical.get("selected_capabilities", ()))
    by_id = {str(item["capability_id"]): item for item in registry_projection.get("entries", ())}
    selected_entries = tuple(by_id[value] for value in selected if value in by_id)
    ids_by_kind: dict[str, list[str]] = {}
    for entry in selected_entries:
        ids_by_kind.setdefault(str(entry.get("kind", "")), []).append(str(entry["capability_id"]))
    tool_kinds = {"readonly_tool", "memory_tool", "retrieval_tool", "retrieval_backend", "runtime_tooling"}
    tool_ids = tuple(str(entry["capability_id"]) for entry in selected_entries if entry.get("kind") in tool_kinds)
    return {
        "selected_capability_id": selected[0] if selected else "",
        "selected_capability_kind": str(selected_entries[0].get("kind", "")) if selected_entries else "",
        "selected_tool_id": tool_ids[0] if tool_ids else "", "selected_tool_ids": tool_ids,
        "selected_skill_id": next(iter(ids_by_kind.get("skill", ())), ""),
        "selected_agent_id": next(iter(ids_by_kind.get("agent", ())), ""),
        "selected_model_role": next(iter(ids_by_kind.get("model_role", ())), ""),
        "selected_memory_tool_id": next(iter(ids_by_kind.get("memory_tool", ())), ""),
        "selected_retrieval_tool_id": next(iter(ids_by_kind.get("retrieval_tool", ())), ""),
        "capability_visible_count": int(registry_projection.get("capability_count", 0)),
    }


def _hot_stream_lines(payload: dict[str, Any], request_deadline: RequestDeadline | None = None) -> Iterable[str]:
    payload = {**payload, "trace_id": str(payload.get("trace_id") or f"trace_{time.time_ns()}")}
    if request_deadline is not None:
        with request_deadline.bind():
            deadline = _hot_request_deadline(payload)
    else:
        deadline = _hot_request_deadline(payload)
    events = _hot_stream_events(payload)
    try:
        while True:
            # A sync generator can be advanced on different framework threads.
            # Bind/reset per advance, never across a yield to another context.
            with deadline.bind():
                deadline.check()
                try:
                    line = next(events)
                except StopIteration:
                    return
                deadline.check()
            yield line
    except TimeoutError:
        if not deadline.cancelled:
            raise
        record_in_flight_trace_event(payload["trace_id"], "HTTP_REQUEST_CANCELLED", "CANCELLED",
            caller_cancelled=True, provider_operation_terminated="UNKNOWN",
            residency_released="UNKNOWN", resource_available="UNKNOWN")
    finally:
        deadline.cancel()
        with deadline.bind():
            events.close()


def _hot_stream_events(payload: dict[str, Any]) -> Iterable[str]:
    text = _payload_text(payload)
    session_id = _payload_session_id(payload)
    identity = _identity_from_hot_payload(payload, session_id)
    session_context = CANONICAL_SESSION_CONTEXT.read(session_id, identity)
    RequestDeadline.current().check()
    registry_projection = _semantic_capability_projection()
    RequestDeadline.current().check()
    events = stream_canonical_semantic_turn(
        trace_id=str(payload.get("trace_id") or f"trace_{time.time_ns()}"),
        session_id=session_id,
        text=text, project_port=PROJECT_UNDERSTANDING_ADAPTER,
        conversation_port=CONVERSATION_EVIDENCE_ADAPTER,
        model_port=MODEL_UNDERSTANDING_ADAPTER, final_brain_port=FINAL_BRAIN_ADAPTER,
        permission_port=PROJECT_READ_PERMISSION, identity=identity,
        session_context=session_context, input_channel=_payload_input_channel(payload),
        input_quality_metadata=_payload_input_quality_metadata(payload),
        understanding_attempt_policy=_payload_understanding_attempt_policy(payload),
        request_deadline=RequestDeadline.current(),
        registry_projection=registry_projection,
        provider_ports={
            PROJECT_UNDERSTANDING_ADAPTER.provider_id: PROJECT_UNDERSTANDING_ADAPTER,
            MEMORY_RETRIEVAL_ADAPTER.provider_id: MEMORY_RETRIEVAL_ADAPTER,
            SIMULATION_WORKER_ADAPTER.provider_id: SIMULATION_WORKER_ADAPTER,
            MODEL_ROLE_ADAPTER.provider_id: MODEL_ROLE_ADAPTER,
            MEDIA_PROVIDER_ADAPTER.provider_id: MEDIA_PROVIDER_ADAPTER,
            WINDOWS_EDGE_ADAPTER.provider_id: WINDOWS_EDGE_ADAPTER,
            CONVERSATION_EVIDENCE_ADAPTER.provider_id: CONVERSATION_EVIDENCE_ADAPTER,
            N8N_ADAPTER.provider_id: N8N_ADAPTER,
            BROWSER_PROVIDER_ADAPTER.provider_id: BROWSER_PROVIDER_ADAPTER,
        },
    )
    try:
        for event in events:
            RequestDeadline.current().check()
            public_event = dict(event)
            if public_event.get("event") in {"done", "error"}:
                result = dict(public_event.get("result", {}))
                response_text = str(public_event.get("response_text", result.get("response_text", ""))).strip()
                result.setdefault("trace_id", str(public_event.get("trace_id", "")))
                capture = _capture_canonical_turn_memory(result, payload, session_id, identity, text, response_text)
                result.update(capture)
                session_event = capture["session_event"]
                for private_key in ("final_brain_input", "helper_raw_result", "final_brain_result", "main_model_attempts"):
                    result.pop(private_key, None)
                result.update(_selected_registry_projection(result, registry_projection))
                result["session_event"] = session_event
                public_event["result"] = result
                public_event["session_event"] = session_event
            RequestDeadline.current().check()
            yield json.dumps(public_event, ensure_ascii=False, default=str) + "\n"
    except (BrokenPipeError, ConnectionResetError, ConnectionAbortedError, GeneratorExit):
        return
    finally:
        close = getattr(events, "close", None)
        if callable(close):
            close()


def write_hot_stream_to_callable(write_callable: Any, payload: dict[str, Any]) -> bool:
    """Compatibility writer over the canonical /hot stream; disconnect is not fatal."""
    lines = _hot_stream_lines({**payload, "stream": True})
    try:
        for line in lines:
            write_callable(line)
    except (BrokenPipeError, ConnectionResetError, ConnectionAbortedError):
        return False
    finally:
        close = getattr(lines, "close", None)
        if callable(close):
            close()
    return True


@app.post("/jarvis-live/command")
def jarvis_live_command(payload: dict[str, Any]) -> dict[str, Any]:
    del payload
    return {
        "ok": False,
        "surface": "CONTROL_PLANE/api_server.py",
        "streaming": False,
        "route": "LEGACY_DISABLED",
        "llm_response": "Старый путь /jarvis-live/command отключен. Используй /jarvis-live/hot.",
        "legacy_command_path_used": False,
        "legacy_route_disabled": True,
        "live_hotpath_enabled": True,
        "direct_dialog_allowed": True,
        "direct_ollama_allowed": True,
        "project_readonly_allowed": True,
        "protected_mutation_required": False,
        "canonical_memory_write_allowed": False,
    }


@app.post("/jarvis-live/chat/stream")
def jarvis_live_streaming_chat(payload: dict[str, Any]) -> StreamingResponse:
    del payload
    return StreamingResponse(
        _legacy_disabled_stream(),
        media_type="application/x-ndjson",
    )


def write_jarvis_live_stream_to_callable(
    write_callable: Any,
    text: str,
    session_id: str = "windows_voice_edge",
) -> bool:
    response_text = "Старый поток /jarvis-live/chat/stream отключен. Используй /jarvis-live/hot."
    event = {
        "event": "done",
        "route": "LEGACY_DISABLED",
        "response_text": response_text,
        "llm_response": response_text,
        "chunk": response_text,
        "text": response_text,
        "legacy_command_path_used": False,
    }
    try:
        write_callable(json.dumps(event, ensure_ascii=False) + "\n")
    except BrokenPipeError:
        return False
    return True


def _legacy_disabled_stream() -> Iterable[str]:
    response_text = "Старый поток /jarvis-live/chat/stream отключен. Используй /jarvis-live/hot."
    event = {
        "event": "done",
        "route": "LEGACY_DISABLED",
        "response_text": response_text,
        "llm_response": response_text,
        "chunk": response_text,
        "text": response_text,
        "legacy_command_path_used": False,
        "live_hotpath_enabled": True,
    }
    yield json.dumps(event, ensure_ascii=False) + "\n"


def _payload_text(payload: dict[str, Any]) -> str:
    for key in ("text", "command", "message", "input"):
        value = payload.get(key)
        if isinstance(value, str) and value.strip():
            return value
    return ""


def _payload_session_id(payload: dict[str, Any]) -> str:
    value = payload.get("session_id")
    if isinstance(value, str) and value.strip():
        return value.strip()
    return "windows_voice_edge"


def _payload_input_channel(payload: dict[str, Any]) -> str:
    value = payload.get("input_channel")
    return value.strip() if isinstance(value, str) and value.strip() else "unknown"


def _payload_input_quality_metadata(payload: dict[str, Any]) -> dict[str, Any]:
    value = payload.get("input_quality_metadata")
    return dict(value) if isinstance(value, dict) else {}


def _extract_created_workflow_artifact(canonical: dict[str, Any]) -> dict[str, Any] | None:
    """Extract the created n8n workflow identity from the evidence bundle (host truth)."""
    evidence = canonical.get("evidence_bundle")
    if not isinstance(evidence, dict):
        return None
    for item in evidence.get("items", ()) or ():
        if not isinstance(item, dict):
            continue
        if str(item.get("source", "")).endswith(":create_workflow"):
            wid = str(item.get("source_reference", "")).strip()
            if wid:
                return {"kind": "automation/workflow", "provider": "n8n", "provider_id": wid}
    return None


def _pc_turn_truth(canonical: dict[str, Any], identity: Any) -> dict[str, Any]:
    plan = canonical.get("execution_plan")
    steps = tuple(plan.get("steps", ())) if isinstance(plan, dict) else ()
    pc_steps = tuple(
        step for step in steps
        if isinstance(step, dict) and (
            step.get("capability_id") == "pc.control"
            or step.get("capability_id") in DIRECT_PC_ACTION_MAP
        )
    )
    raw_permissions = canonical.get("permission_decision")
    if isinstance(raw_permissions, dict):
        permissions = (raw_permissions,)
    elif isinstance(raw_permissions, (tuple, list)):
        permissions = tuple(item for item in raw_permissions if isinstance(item, dict))
    else:
        permissions = ()
    pc_capability_ids = {str(step.get("capability_id")) for step in pc_steps}
    pc_permissions = tuple(item for item in permissions if item.get("capability_id") in pc_capability_ids)
    policy_execution_allowed = bool(
        pc_steps
        and pc_permissions
        and all(item.get("granted") is True and item.get("approval_required") is not True for item in pc_permissions)
    )
    owner_pc_action_eligible = bool(identity.owner_authorized)
    pc_operation_authorized = bool(owner_pc_action_eligible and policy_execution_allowed and pc_steps)
    readiness = _legacy_runtime_readiness_payload() if pc_steps else {}
    pc_executor_available = readiness.get("pc_executor_available") if pc_steps else None
    evidence = canonical.get("evidence_bundle")
    receipts = tuple(evidence.get("receipts", ())) if isinstance(evidence, dict) else ()
    pc_operation_ids = {step.get("operation") for step in pc_steps}
    pc_receipts = tuple(
        receipt for receipt in receipts
        if isinstance(receipt, dict) and receipt.get("operation_id") in pc_operation_ids
    )
    receipt = pc_receipts[0] if pc_receipts else None
    receipt_valid = bool(
        isinstance(receipt, dict)
        and receipt.get("trace_id") == canonical.get("trace_id")
        and receipt.get("status") in {"COMPLETE", "EXECUTED"}
        and receipt.get("operation_id") in pc_operation_ids
    )
    return {
        "owner_pc_action_eligible": owner_pc_action_eligible,
        "policy_execution_allowed": policy_execution_allowed,
        "pc_executor_available": pc_executor_available,
        "pc_operation_authorized_for_this_turn": pc_operation_authorized,
        "executed": receipt_valid,
        "execution_receipt": receipt if receipt_valid else None,
    }
