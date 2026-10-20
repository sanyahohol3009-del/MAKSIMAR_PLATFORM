from __future__ import annotations

from CORE_ROOT.run_context import model_free_startup

"""Server-owned read-only inventory of existing JARVIS capabilities."""

import importlib.util
import json
import sys
from dataclasses import asdict, dataclass
from functools import lru_cache
from pathlib import Path
from typing import Any

from MAKSIMAR_CORE_LIB.action_library_adapters.external_tool_library_adapter import (
    build_jarvis_external_adapter_visibility_read_model,
)
from MAKSIMAR_CORE_LIB.memory_engine.memory_accessor import list_memory_definitions
from MAKSIMAR_CORE_LIB.retrieval_backend import (
    build_retrieval_tool_registry_contract,
    inspect_mgrep_readonly_availability,
    inspect_qdrant_readonly_availability,
    inspect_sqlite_vec_readonly_availability,
)
from MAKSIMAR_CORE_LIB.swarm_coordination import build_default_swarm_agent_role_contracts
from MAKSIMAR_CORE_LIB.workers_registry.worker_registry_contract import (
    build_worker_registry_contract,
)
from MAKSIMAR_SERVER.SKILL_ADAPTER_REGISTRY.skill_adapter_registry_contract import (
    build_skill_adapter_registry_contract,
)
from MAKSIMAR_SERVER.WORKFLOW_AUTOMATION_RUNTIME.n8n_adapter_contract import (
    build_n8n_adapter_contract,
)
from MAKSIMAR_SERVER.WORKFLOW_AUTOMATION_RUNTIME.jarvis_pc_action_adapter_contract import (
    DIRECT_PC_ACTION_MAP, PC_ACTION_OPERATION_CONTRACTS, WINDOWS_EDGE_PROVIDER_ID,
)
from MAKSIMAR_CORE_LIB.project_read.codegraph_readonly_adapter import (
    inspect_codegraph_readonly_capability,
)
from MAKSIMAR_SERVER.AI_ORCHESTRATION.jarvis_live_read_models import (
    build_jarvis_live_memory_federation_status,
    build_jarvis_live_tool_catalog_read_model,
)
from MAKSIMAR_CORE_LIB.project_read.jarvis_runtime_library_store import (
    RUNTIME_LIBRARY_STORE_ROOT,
    build_runtime_library_store_read_model,
)
from MAKSIMAR_SERVER.AI_ORCHESTRATION.session_memory_store import SESSION_STATE_PATH, _session_turn_log_path
from MAKSIMAR_SERVER.AI_ORCHESTRATION.memory_retrieval_adapter import (
    MEMORY_CAPABILITY_OPERATION_CONTRACTS,
    PROVIDER_ID as MEMORY_RETRIEVAL_PROVIDER_ID,
)
from MAKSIMAR_SERVER.AI_ORCHESTRATION.project_understanding_adapter import (
    PROJECT_READONLY_INVENTORY_CONTRACTS,
)
from MAKSIMAR_SERVER.AI_ORCHESTRATION.simulation_worker_adapter import (
    PROVIDER_ID as SIMULATION_WORKER_PROVIDER_ID,
    SIMULATION_CAPABILITY_OPERATION_CONTRACTS,
)
from MAKSIMAR_SERVER.AI_ORCHESTRATION.n8n_adapter import (
    N8N_CAPABILITY_OPERATION_CONTRACTS,
    PROVIDER_ID as N8N_PROVIDER_ID,
)
from MAKSIMAR_SERVER.AI_ORCHESTRATION.model_role_adapter import (
    MODEL_ROLE_OPERATION_CONTRACTS,
    PROVIDER_ID as MODEL_ROLE_PROVIDER_ID,
)
from MAKSIMAR_SERVER.AI_ORCHESTRATION.media_provider_adapter import (
    MEDIA_CAPABILITY_OPERATION_CONTRACTS,
    PROVIDER_ID as MEDIA_PROVIDER_ID,
)
from MAKSIMAR_SERVER.AI_ORCHESTRATION.browser_provider_adapter import (
    BROWSER_CAPABILITY, BROWSER_CAPABILITY_OPERATION_CONTRACTS,
    PROVIDER_ID as BROWSER_PROVIDER_ID,
)
from MAKSIMAR_CORE_LIB.ai_orchestration.model_profile_registry_contract import (
    build_jarvis_live_runtime_model_role_profiles,
)
from MAKSIMAR_CORE_LIB.capability_registry.capability_registry_loader import (
    load_capability_manifests,
)


PROJECT_ROOT = Path(__file__).resolve().parents[2]
RUNTIME_ROOT = Path.home() / "MAKSIMAR_RUNTIME"
RUNTIME_VENVS_ROOT = RUNTIME_ROOT / "venvs"
AGENT_TOOLING_MANIFEST_ROOT = PROJECT_ROOT / "EXTERNAL_BACKENDS/agent_tooling/manifests"
MEMPALACE_ROOT = PROJECT_ROOT / "EXTERNAL_BACKENDS/mempalace/source"
MEMPALACE_RUNTIME_PYTHON = PROJECT_ROOT / "EXTERNAL_BACKENDS/mempalace/venv/bin/python"
MEMPALACE_DEFAULT_PALACE = Path.home() / ".mempalace"


def _mempalace_ready() -> bool:
    """Mirror Mempalace's persisted-palace truth without invoking or mutating it."""
    if not MEMPALACE_RUNTIME_PYTHON.exists():
        return False
    config_path = MEMPALACE_DEFAULT_PALACE / "config.json"
    try:
        configured = Path(str(json.loads(config_path.read_text(encoding="utf-8")).get("palace_path") or ""))
    except (OSError, ValueError, TypeError):
        return False
    if not configured.is_dir() or not (configured / "chroma.sqlite3").is_file():
        return False
    import sqlite3
    try:
        with sqlite3.connect((configured / "chroma.sqlite3").as_uri() + "?mode=ro", uri=True, timeout=1) as connection:
            return connection.execute("SELECT COUNT(*) FROM embeddings").fetchone()[0] > 0
    except (sqlite3.Error, OSError):
        return False
# Source provenance follows the SAME existing execution owner.
from MAKSIMAR_SERVER.AI_ORCHESTRATION.n8n_adapter import _N8N_ROOT as N8N_ROOT
RETRIEVAL_ROOT = PROJECT_ROOT / "EXTERNAL_BACKENDS/vendor_quarantine/retrieval_backends"
WINDOWS_EDGE_VENV = Path("/mnt/c/MAKSIMAR_EDGE/.venv")
FLUTTER_ROOT = RUNTIME_ROOT / "tools/flutter"
RUNTIME_HISTORY_STORE_ROOT = _session_turn_log_path()
VOICE_RUNTIME_PATHS = {
    "runtime_voice:faster_whisper": RUNTIME_VENVS_ROOT / "faster_whisper_stt",
    "runtime_voice:kokoro_tts": RUNTIME_VENVS_ROOT / "kokoro_tts",
    "runtime_voice:silero_tts": RUNTIME_VENVS_ROOT / "silero_tts",
    "runtime_voice:piper_windows_edge": WINDOWS_EDGE_VENV,
}
JARVIS_LIBRARY_DIRS = {
    "jarvis_runtime_library:agents": RUNTIME_LIBRARY_STORE_ROOT / "agents",
    "jarvis_runtime_library:skills": RUNTIME_LIBRARY_STORE_ROOT / "skills",
    "jarvis_runtime_library:tools": RUNTIME_LIBRARY_STORE_ROOT / "tools",
    "jarvis_runtime_library:manifests": RUNTIME_LIBRARY_STORE_ROOT / "manifests",
}
SCAN_ROOTS: tuple[Path, ...] = (
    PROJECT_ROOT / "tools/jarvis_live_runtime",
    PROJECT_ROOT / "MAKSIMAR_CORE_LIB/action_library_adapters",
    PROJECT_ROOT / "MAKSIMAR_CORE_LIB/retrieval_backend",
    PROJECT_ROOT / "MAKSIMAR_CORE_LIB/memory_engine",
    PROJECT_ROOT / "MAKSIMAR_CORE_LIB/workers_registry",
    PROJECT_ROOT / "MAKSIMAR_SERVER/WORKFLOW_AUTOMATION_RUNTIME",
    PROJECT_ROOT / "CONTROL_PLANE",
    AGENT_TOOLING_MANIFEST_ROOT,
    MEMPALACE_ROOT,
    N8N_ROOT,
    RETRIEVAL_ROOT,
    RUNTIME_LIBRARY_STORE_ROOT,
)


@dataclass(frozen=True, slots=True)
class CapabilityRecord:
    capability_id: str
    capability_kind: str
    display_name: str
    source: str
    source_file_or_path: str
    import_path: str
    external_path: str
    runtime_python_or_executable: str
    direct_allowed: bool
    owner_gate_required: bool
    approval_required: bool
    read_only: bool
    protected: bool
    missing_dependency: bool
    status: str
    reason: str
    selection_enabled: bool
    execution_policy: str
    capability_exists: bool = True
    provider_id: str = ""
    provider_exists: bool = False
    provider_available: bool | None = None
    adapter_installed: bool = False
    identity_eligible: bool | None = None
    policy_execution_allowed: bool | None = None
    executed: bool = False
    execution_receipt_present: bool = False

    def to_read_model(self) -> dict[str, Any]:
        return asdict(self)


def build_existing_capability_inventory(*, readonly_catalog: dict[str, Any] | None = None,
                                        external_visibility: dict[str, Any] | None = None) -> tuple[dict[str, Any], ...]:
    records = _inventory_records() if readonly_catalog is None and external_visibility is None else _build_inventory_records(
        readonly_catalog=readonly_catalog, external_visibility=external_visibility,
    )
    return tuple(record.to_read_model() for record in records)


def build_existing_capability_inventory_summary(
    records: tuple[dict[str, Any], ...] | None = None,
) -> dict[str, Any]:
    records = records or build_existing_capability_inventory()
    by_kind: dict[str, int] = {}
    by_status: dict[str, int] = {}
    selection_enabled_count = 0
    direct_allowed_count = 0
    for record in records:
        by_kind[record["capability_kind"]] = by_kind.get(record["capability_kind"], 0) + 1
        by_status[record["status"]] = by_status.get(record["status"], 0) + 1
        if record["selection_enabled"]:
            selection_enabled_count += 1
        if record["direct_allowed"]:
            direct_allowed_count += 1
    return {
        "inventory_id": "existing_capability_inventory_v2",
        "total_capabilities": len(records),
        "counts_by_kind": by_kind,
        "counts_by_status": by_status,
        "selection_enabled_count": selection_enabled_count,
        "direct_allowed_count": direct_allowed_count,
        "scan_roots": tuple(str(path) for path in SCAN_ROOTS),
        "runtime_roots": (
            str(RUNTIME_ROOT),
            str(RUNTIME_VENVS_ROOT),
            str(RUNTIME_LIBRARY_STORE_ROOT),
            str(FLUTTER_ROOT),
            str(WINDOWS_EDGE_VENV),
        ),
    }


def build_semantic_capability_registry_projection(
    *, readiness: dict[str, Any] | None = None,
) -> dict[str, Any]:
    """Build the bounded model-facing projection of the one existing inventory.

    This function never inspects user text and never infers live availability from
    installation paths.  Turn-specific identity, policy, execution and receipt
    truth remains unresolved until the canonical spine evaluates a typed plan.
    """
    model_free = model_free_startup()  # HTTP/readiness payloads cannot override launch context.
    runtime = dict(readiness or {})
    manifests = {str(item["id"]): item for item in load_capability_manifests()}
    entries = [
        _semantic_projection_entry(record, manifests.get(str(record["capability_id"])), runtime)
        for record in build_existing_capability_inventory()
    ]
    # Semantic existence is stable even when the implementation provider is down.
    # Availability is resolved separately by the host at execution time.
    entries.append(_browser_projection_entry(runtime))
    projected_ids = {str(item["capability_id"]) for item in entries}
    entries.extend(
        _manifest_projection_entry(manifest)
        for capability_id, manifest in manifests.items()
        if capability_id not in projected_ids
    )
    entries.extend(_model_role_projection_entries(runtime))
    if model_free:
        for entry in entries:
            if entry["kind"] == "model_role" or MODEL_ROLE_PROVIDER_ID in entry.get("provider_ids", ()):
                # Preserve typed operation/installation metadata, but never infer
                # executable provider availability from it in this launch mode.
                entry["provider_available"] = False
                entry["availability_status"] = "UNAVAILABLE"
    return {
        "schema_version": "semantic_capability_registry_projection.v1",
        "registry_id": "existing_capability_inventory_v2",
        "model_free_startup": model_free,
        "source_owner": "MAKSIMAR_SERVER.SKILL_ADAPTER_REGISTRY.existing_capability_inventory",
        "capability_count": len(entries),
        "inventory_capability_count": len(build_existing_capability_inventory()),
        "manifest_only_capability_count": sum(1 for capability_id in manifests if capability_id not in projected_ids),
        "model_role_count": len(build_jarvis_live_runtime_model_role_profiles()),
        "entries": tuple(entries),
        "selection_basis": "model_semantics_over_typed_registry_projection",
        "user_text_inspected": False,
}


def _browser_projection_entry(runtime: dict[str, Any]) -> dict[str, Any]:
    contracts = BROWSER_CAPABILITY_OPERATION_CONTRACTS[BROWSER_CAPABILITY]
    available = runtime.get("browser_provider_available")
    return {
        "capability_id": BROWSER_CAPABILITY, "kind": "browser",
        "semantic_description": "Bounded web page read, navigation and authorized local interaction.",
        "capability_exists": True, "adapter_installed": True,
        "provider_ids": (BROWSER_PROVIDER_ID,), "provider_exists": True,
        "provider_available": available if isinstance(available, bool) else None,
        "availability_status": "AVAILABLE" if available is True else "UNAVAILABLE" if available is False else "UNKNOWN",
        "operation_contract_source": "EXISTING_TYPED_CONTRACT",
        "provider_binding_status": "BOUND", "execution_contract_available": True,
        "selection_mode": "EXECUTABLE",
        "supported_effects": tuple(dict.fromkeys(str(x["effect_type"]) for x in contracts)),
        "operation_contracts": contracts,
        "target_restrictions": ("localhost_browser_dom", "public_browser_dom"),
        "identity_eligibility_metadata": {"owner_gate_required": True, "turn_identity_eligible": None},
        "policy_metadata": {"execution_policy": "per_step_policy", "approval_may_be_required": True, "turn_policy_execution_allowed": None},
        "model_role_requirements": (), "executed": False, "execution_receipt_present": False,
        "source_status": "runtime_backed",
    }


def build_global_semantic_capability_projection(
    *, readiness: dict[str, Any] | None = None,
) -> dict[str, Any]:
    """Compact read-model for global intent understanding.

    Concrete provider/worker entries remain in the canonical projection and are
    intentionally excluded here.  Owners are derived from their typed operation
    contracts, so this is not a second capability registry.
    """
    full = build_semantic_capability_registry_projection(readiness=readiness)
    owners: dict[str, dict[str, Any]] = {}
    for entry in full.get("entries", ()):
        for operation in entry.get("operation_contracts", ()) or ():
            owner = str(operation.get("semantic_owner_id", "")).strip()
            if not owner:
                continue
            item = owners.setdefault(owner, {
                "semantic_owner_id": owner,
                "semantic_description": str(operation.get("description", ""))[:120],
                "supported_effects": set(),
                "availability": set(),
            })
            effect = str(operation.get("effect_type", "")).strip()
            if effect:
                item["supported_effects"].add(effect)
            item["availability"].add(str(entry.get("availability_status", "UNKNOWN")))
    entries = []
    for owner in sorted(owners):
        item = owners[owner]
        entries.append({
            "semantic_owner_id": owner,
            "semantic_description": item["semantic_description"],
            "supported_effects": tuple(sorted(item["supported_effects"])),
            "availability": tuple(sorted(item["availability"])),
        })
    return {
        "schema_version": "global_semantic_capability_projection.v1",
        "source_owner": "MAKSIMAR_SERVER.SKILL_ADAPTER_REGISTRY.existing_capability_inventory",
        "entries": tuple(entries),
        "owner_count": len(entries),
        "authority": "READ_MODEL",
        "user_text_inspected": False,
    }


def resolve_semantic_owner_operation_candidates(
    semantic_owner_id: str,
    *,
    projection: dict[str, Any] | None = None,
) -> tuple[dict[str, Any], ...]:
    """Resolve canonical operation candidates for one COMPACT human semantic owner.

    Groups canonical operation contracts by their ``semantic_owner_id`` (the compact
    human-level JARVIS organ, e.g. ``windows.volume``), distinct from the broader
    technical ``target_scope``. Returns 0/1/N candidates so the caller applies the same
    resolution truth table (0 -> typed unresolved; 1 -> deterministic; N -> bounded
    in-owner semantic selection). Effect/params/evidence_kind remain HOST truth.
    """
    proj = projection if projection is not None else build_semantic_capability_registry_projection()
    candidates: list[dict[str, Any]] = []
    seen: set[str] = set()
    for entry in proj.get("entries", ()):
        for op in entry.get("operation_contracts", ()) or ():
            if str(op.get("semantic_owner_id")) != semantic_owner_id:
                continue
            operation_id = str(op.get("operation_id"))
            if operation_id in seen:
                continue
            seen.add(operation_id)
            candidates.append(dict(op))
    return tuple(candidates)


def _semantic_projection_entry(
    record: dict[str, Any], manifest: dict[str, Any] | None, readiness: dict[str, Any],
) -> dict[str, Any]:
    if manifest is not None:
        return _manifest_projection_entry(manifest)
    capability_id = str(record["capability_id"])
    kind = str(record["capability_kind"])
    installed = _source_present(record)
    authoritative = _existing_authoritative_execution_contract(record)
    provider_ids = (
        (str(authoritative["provider_id"]),)
        if authoritative is not None
        else _existing_bound_provider_ids(record)
    )
    provider_exists = bool(provider_ids)
    provider_available = _provider_availability(record, readiness, provider_exists)
    contract_source = (
        "EXISTING_TYPED_CONTRACT"
        if authoritative is not None
        else _existing_contract_source(kind)
    )
    selection_mode = (
        "EXECUTABLE"
        if authoritative is not None
        else "PLAN_ONLY" if contract_source == "EXISTING_TYPED_CONTRACT" else "VISIBILITY_ONLY"
    )
    operation_contracts = (
        tuple(dict(item) for item in authoritative["operation_contracts"])
        if authoritative is not None
        else ()
    )
    approval_may_be_required = (
        any(
            str(item.get("risk_class")) == "DANGEROUS"
            or bool(item.get("external_side_effect"))
            or str(item.get("reversibility")) == "IRREVERSIBLE"
            for item in operation_contracts
        )
        if operation_contracts else bool(record["approval_required"])
    )
    semantic_description = f"{record['display_name']}. Registered {kind} capability. {record['reason']}"
    if operation_contracts:
        semantic_description = " ".join(
            str(item["description"]).strip() for item in operation_contracts
            if str(item.get("description", "")).strip()
        )
    return {
        "capability_id": capability_id,
        "kind": kind,
        "semantic_description": semantic_description,
        "capability_exists": True,
        "adapter_installed": installed,
        "provider_ids": provider_ids,
        "provider_exists": provider_exists,
        "provider_available": provider_available,
        "availability_status": (
            "AVAILABLE" if provider_available is True else
            "UNAVAILABLE" if provider_available is False else "UNKNOWN"
        ),
        "operation_contract_source": contract_source,
        "provider_binding_status": "BOUND" if provider_exists else "UNBOUND",
        "execution_contract_available": authoritative is not None,
        "selection_mode": selection_mode,
        "supported_effects": (
            tuple(dict.fromkeys(str(item["effect_type"]) for item in operation_contracts))
            if operation_contracts else ("UNKNOWN",)
        ),
        "operation_contracts": operation_contracts,
        "target_restrictions": (
            tuple(dict.fromkeys(str(item["target_scope"]) for item in operation_contracts))
            if operation_contracts else ("UNKNOWN",)
        ),
        "identity_eligibility_metadata": {
            "owner_gate_required": bool(record["owner_gate_required"]),
            "turn_identity_eligible": None,
        },
        "policy_metadata": {
            "execution_policy": "per_step_policy" if operation_contracts else str(record["execution_policy"]),
            "approval_may_be_required": approval_may_be_required,
            "turn_policy_execution_allowed": None,
        },
        "model_role_requirements": (),
        "executed": False,
        "execution_receipt_present": False,
        "source_status": str(record["status"]),
    }


def _manifest_projection_entry(manifest: dict[str, Any]) -> dict[str, Any]:
    return {
        "capability_id": str(manifest["id"]), "kind": "canonical_capability",
        "semantic_description": str(manifest["description"]), "capability_exists": True,
        "adapter_installed": True, "provider_ids": (str(manifest["provider"]),),
        "provider_exists": True, "provider_available": None, "availability_status": "UNKNOWN",
        "operation_contract_source": "MANIFEST", "provider_binding_status": "BOUND",
        "execution_contract_available": True, "selection_mode": "EXECUTABLE",
        "supported_effects": tuple(dict.fromkeys(str(item["effect_type"]) for item in manifest["operation_contracts"])),
        "operation_contracts": tuple({
            "operation_id": str(item["operation_id"]), "description": str(item["description"]),
            "required_parameters": tuple(item["required_parameters"]), "evidence_kinds": tuple(item["evidence_kinds"]),
            "effect_type": str(item["effect_type"]), "target_scope": str(item["target_scope"]),
            "semantic_owner_id": str(manifest["id"]),
            "reversibility": str(item["reversibility"]),
            "external_side_effect": bool(item["external_side_effect"]), "risk_class": str(item["risk_class"]),
        } for item in manifest["operation_contracts"]),
        "target_restrictions": tuple(dict.fromkeys(str(item["target_scope"]) for item in manifest["operation_contracts"])),
        "identity_eligibility_metadata": {"owner_gate_required": False, "turn_identity_eligible": None},
        "policy_metadata": {"execution_policy": "per_step_policy", "approval_may_be_required": False, "turn_policy_execution_allowed": None},
        "model_role_requirements": (), "executed": False, "execution_receipt_present": False,
        "source_status": "manifest_backed",
    }


def _existing_bound_provider_ids(record: dict[str, Any]) -> tuple[str, ...]:
    kind = str(record["capability_kind"])
    if kind in {"pc_action", "runtime_windows_edge"}:
        return ("windows_edge_adapter",)
    return ()


def _existing_authoritative_execution_contract(
    record: dict[str, Any],
) -> dict[str, Any] | None:
    """Expose only proven owner-level contracts; never synthesize by kind."""
    capability_id = str(record.get("capability_id", ""))
    pc_contracts = PC_ACTION_OPERATION_CONTRACTS.get(capability_id)
    if pc_contracts is not None:
        return {
            "provider_id": WINDOWS_EDGE_PROVIDER_ID,
            "operation_contracts": pc_contracts,
        }
    memory_contracts = MEMORY_CAPABILITY_OPERATION_CONTRACTS.get(capability_id)
    if memory_contracts is not None:
        return {
            "provider_id": MEMORY_RETRIEVAL_PROVIDER_ID,
            "operation_contracts": memory_contracts,
        }
    project_contracts = PROJECT_READONLY_INVENTORY_CONTRACTS.get(capability_id)
    if project_contracts is not None:
        return {
            "provider_id": "existing_project_workspace_tools",
            "operation_contracts": project_contracts,
        }
    simulation_contracts = SIMULATION_CAPABILITY_OPERATION_CONTRACTS.get(capability_id)
    if simulation_contracts is not None:
        return {
            "provider_id": SIMULATION_WORKER_PROVIDER_ID,
            "operation_contracts": simulation_contracts,
        }
    n8n_contracts = N8N_CAPABILITY_OPERATION_CONTRACTS.get(capability_id)
    if n8n_contracts is not None:
        return {
            "provider_id": N8N_PROVIDER_ID,
            "operation_contracts": n8n_contracts,
        }
    local_model_contracts = MODEL_ROLE_OPERATION_CONTRACTS.get(capability_id)
    if local_model_contracts is not None:
        return {
            "provider_id": MODEL_ROLE_PROVIDER_ID,
            "operation_contracts": local_model_contracts,
        }
    media_contracts = MEDIA_CAPABILITY_OPERATION_CONTRACTS.get(capability_id)
    if media_contracts is not None:
        return {"provider_id": MEDIA_PROVIDER_ID, "operation_contracts": media_contracts}
    return None


def _source_present(record: dict[str, Any]) -> bool:
    source = Path(str(record.get("source_file_or_path", "")))
    external = Path(str(record.get("external_path", ""))) if record.get("external_path") else None
    return source.exists() or bool(external and external.exists()) or bool(record.get("import_path"))


def _provider_availability(
    record: dict[str, Any], readiness: dict[str, Any], provider_bound: bool,
) -> bool | None:
    if str(record.get("capability_id", "")) in SIMULATION_CAPABILITY_OPERATION_CONTRACTS:
        return True
    if str(record.get("capability_id", "")) in {
        "content.metadata.generate", "content.shorts.generate", "code.proposal.generate", "media.probe",
    }:
        return True
    if str(record.get("capability_id", "")) == "mempalace_search":
        return _mempalace_ready()
    kind = str(record["capability_kind"])
    if kind in {"pc_action", "runtime_windows_edge"}:
        value = readiness.get("pc_executor_available")
        return value if isinstance(value, bool) else None
    if not provider_bound:
        return False
    return None


def _existing_contract_source(kind: str) -> str:
    typed_kinds = {
        "pc_action", "runtime_windows_edge", "skill", "agent", "worker", "memory_tool",
        "retrieval_tool", "retrieval_backend", "external_adapter", "workflow_automation",
        "runtime_voice", "runtime_tooling", "jarvis_runtime_library",
    }
    return "EXISTING_TYPED_CONTRACT" if kind in typed_kinds else "VISIBILITY_ONLY"


def _model_role_projection_entries(readiness: dict[str, Any]) -> tuple[dict[str, Any], ...]:
    residency = readiness.get("model_residency", {}) if isinstance(readiness.get("model_residency"), dict) else {}
    entries = []
    for profile in build_jarvis_live_runtime_model_role_profiles():
        state = residency.get(profile.model_id, {}) if isinstance(residency.get(profile.model_id), dict) else {}
        installed = state.get("installed") if isinstance(state.get("installed"), bool) else profile.installed
        capability_id = "model_role:" + profile.role_id
        operation_contracts = MODEL_ROLE_OPERATION_CONTRACTS.get(capability_id, ())
        provider_ids = (MODEL_ROLE_PROVIDER_ID,) if operation_contracts else ()
        role_description = f"Model execution role {profile.role}: " + ", ".join(profile.use_cases)
        if operation_contracts and installed:
            role_description = (
                "Installed and AVAILABLE local proposal-only model execution role "
                f"{profile.role}: " + ", ".join(profile.use_cases)
            )
        elif not operation_contracts:
            role_description = (
                f"Visibility-only installed model role {profile.role}; no independent capability operation or "
                "provider binding. Runtime assignment metadata only: " + ", ".join(profile.use_cases)
            )
        entries.append({
            "capability_id": capability_id,
            "kind": "model_role",
            "semantic_description": role_description,
            "capability_exists": True,
            "adapter_installed": installed,
            "provider_ids": provider_ids, "provider_exists": bool(provider_ids),
            "provider_available": (bool(installed) if provider_ids else False),
            "availability_status": ("AVAILABLE" if provider_ids and installed else "UNAVAILABLE"),
            "operation_contract_source": "EXISTING_TYPED_CONTRACT",
            "provider_binding_status": "BOUND" if provider_ids else "UNBOUND",
            "execution_contract_available": bool(operation_contracts),
            "selection_mode": "EXECUTABLE" if operation_contracts else "PLAN_ONLY",
            "supported_effects": tuple(dict.fromkeys(
                str(item["effect_type"]) for item in operation_contracts
            )) if operation_contracts else ("UNKNOWN",),
            "operation_contracts": tuple(dict(item) for item in operation_contracts),
            "target_restrictions": tuple(dict.fromkeys(
                str(item["target_scope"]) for item in operation_contracts
            )) if operation_contracts else ("UNKNOWN",),
            "identity_eligibility_metadata": {"owner_gate_required": False, "turn_identity_eligible": None},
            "policy_metadata": {"execution_policy": "typed_model_role_selection", "approval_may_be_required": False, "turn_policy_execution_allowed": None},
            "model_role_requirements": (profile.role_id,),
            "executed": False, "execution_receipt_present": False,
            "source_status": profile.status,
        })
    return tuple(entries)


def build_existing_capability_catalog(
    *, readonly_catalog: dict[str, Any] | None = None,
    external_visibility: dict[str, Any] | None = None,
) -> dict[str, Any]:
    """Group existing inventory records for compatibility read endpoints."""
    records = build_existing_capability_inventory(
        readonly_catalog=readonly_catalog, external_visibility=external_visibility,
    )
    summary = build_existing_capability_inventory_summary(records)
    grouped = {
        "direct_pc_actions": _filter_inventory(records, capability_kind="pc_action"),
        "readonly_project_tools": _filter_inventory(records, capability_kind="readonly_tool", read_only=True),
        "readonly_tools": _filter_inventory(records, capability_kind="readonly_tool", read_only=True),
        "memory_tools": _filter_inventory(records, capability_kind="memory_tool"),
        "retrieval_tools": _filter_inventory(records, capability_kind="retrieval_tool"),
        "retrieval_backends": _filter_inventory(records, capability_kind="retrieval_backend"),
        "skills": _filter_inventory(records, capability_kind="skill"),
        "agents": _filter_inventory(records, capability_kind="agent"),
        "workers": _filter_inventory(records, capability_kind="worker"),
        "external_adapters": _filter_inventory(records, capability_kind="external_adapter"),
        "workflow_automation": _filter_inventory(records, capability_kind="workflow_automation"),
        "runtime_tooling": _filter_inventory(records, capability_kind="runtime_tooling"),
        "runtime_voice": _filter_inventory(records, capability_kind="runtime_voice"),
        "runtime_windows_edge": _filter_inventory(records, capability_kind="runtime_windows_edge"),
        "jarvis_runtime_library": _filter_inventory(records, capability_kind="jarvis_runtime_library"),
        "protected_tools": _filter_inventory(records, capability_kind="protected_tool"),
    }
    unavailable = tuple(record for record in records if record["status"] in {
        "degraded", "external_not_found", "unavailable", "missing",
    })
    external_tools = tuple(record for record in records if record.get("external_path") and
                           record.get("source") in {"external_runtime", "vendor_quarantine"})
    return {
        "catalog_id": "existing_capability_inventory_v2", "source": "existing_capability_inventory",
        "counts_by_capability_kind": summary["counts_by_kind"],
        "counts_by_status": summary["counts_by_status"],
        "capability_visible_count": summary["selection_enabled_count"],
        "capability_direct_count": summary["direct_allowed_count"],
        "external_code_commit_policy": "external runtime only, do not commit vendor code",
        **grouped, "external_tools": external_tools, "unavailable_capabilities": unavailable,
    }


def resolve_existing_capability(capability_id: str) -> dict[str, Any]:
    """Resolve one explicit typed capability ID; no language is inspected."""
    normalized = str(capability_id or "").strip()
    record = _capability_record_by_id().get(normalized)
    if record is not None:
        return dict(record)
    return {
        "capability_id": normalized, "capability_kind": "", "display_name": "",
        "status": "blocked_unknown_capability", "reason": "capability_not_found_in_existing_inventory",
        "direct_allowed": False, "approval_required": True, "selection_enabled": False,
        "execution_policy": "unknown_capability",
    }


@lru_cache(maxsize=1)
def _capability_record_by_id() -> dict[str, dict[str, Any]]:
    return {record["capability_id"]: record for record in build_existing_capability_inventory()}


def _filter_inventory(records: tuple[dict[str, Any], ...], **conditions: Any) -> tuple[dict[str, Any], ...]:
    return tuple(record for record in records
                 if all(record.get(key) == expected for key, expected in conditions.items()))


@lru_cache(maxsize=1)
def _inventory_records() -> tuple[CapabilityRecord, ...]:
    return _build_inventory_records()


def _build_inventory_records(*, readonly_catalog: dict[str, Any] | None = None,
                             external_visibility: dict[str, Any] | None = None) -> tuple[CapabilityRecord, ...]:
    records: list[CapabilityRecord] = []
    records.extend(_scan_pc_actions())
    records.extend(_scan_readonly_tools(readonly_catalog))
    records.extend(_scan_memory_tools())
    records.extend(_scan_retrieval_backends())
    records.extend(_scan_skills())
    records.extend(_scan_agents())
    records.extend(_scan_workers())
    records.extend(_scan_external_adapters(external_visibility))
    records.extend(_scan_local_content_capabilities())
    records.extend(_scan_runtime_tooling())
    records.extend(_scan_runtime_voice())
    records.extend(_scan_windows_edge())
    records.extend(_scan_runtime_library_sources())
    canonical: dict[str, CapabilityRecord] = {}
    for record in records:
        canonical[record.capability_id] = record
    return tuple(sorted(canonical.values(), key=lambda item: (item.capability_kind, item.capability_id)))


def _safe_read_json(path: Path) -> dict[str, Any]:
    try:
        payload = json.loads(path.read_text(encoding="utf-8"))
    except (FileNotFoundError, OSError, json.JSONDecodeError):
        return {}
    return payload if isinstance(payload, dict) else {}


def _build_record(
    *,
    capability_id: str,
    capability_kind: str,
    display_name: str,
    source: str,
    source_file_or_path: Path | str,
    import_path: str = "",
    external_path: Path | str = "",
    runtime_python_or_executable: Path | str = "",
    direct_allowed: bool,
    owner_gate_required: bool,
    approval_required: bool,
    read_only: bool,
    protected: bool,
    status: str,
    reason: str,
    selection_enabled: bool | None = None,
    execution_policy: str = "",
) -> CapabilityRecord:
    normalized_status = status if status else "unknown"
    normalized_selection = normalized_status not in {"external_not_found", "missing"} if selection_enabled is None else selection_enabled
    missing_dependency = normalized_status not in {"available", "degraded"}
    source_path = Path(str(source_file_or_path))
    external = Path(str(external_path)) if str(external_path) else None
    adapter_installed = source_path.exists() or bool(external and external.exists()) or bool(import_path)
    provider_id = "windows_edge_adapter" if capability_kind in {"pc_action", "runtime_windows_edge"} else ""
    provider_exists = bool(provider_id)
    return CapabilityRecord(
        capability_id=capability_id,
        capability_kind=capability_kind,
        display_name=display_name,
        source=source,
        source_file_or_path=str(source_file_or_path),
        import_path=import_path,
        external_path=str(external_path),
        runtime_python_or_executable=str(runtime_python_or_executable),
        direct_allowed=direct_allowed,
        owner_gate_required=owner_gate_required,
        approval_required=approval_required,
        read_only=read_only,
        protected=protected,
        missing_dependency=missing_dependency,
        status=normalized_status,
        reason=reason,
        selection_enabled=normalized_selection,
        execution_policy=execution_policy or ("direct_read_only" if direct_allowed and read_only else "approval_required"),
        capability_exists=True,
        provider_id=provider_id,
        provider_exists=provider_exists,
        provider_available=None if provider_exists else False,
        adapter_installed=adapter_installed,
        identity_eligible=None,
        policy_execution_allowed=None,
        executed=False,
        execution_receipt_present=False,
    )


def _scan_pc_actions() -> list[CapabilityRecord]:
    source_path = PROJECT_ROOT / "MAKSIMAR_SERVER/WORKFLOW_AUTOMATION_RUNTIME/jarvis_pc_action_adapter_contract.py"
    records: list[CapabilityRecord] = []
    for action_id, meta in sorted(DIRECT_PC_ACTION_MAP.items()):
        protected = bool(meta.get("protected", False))
        records.append(
            _build_record(
                capability_id=action_id,
                capability_kind="pc_action",
                display_name=action_id.replace("_", " "),
                source="internal_project",
                source_file_or_path=source_path,
                import_path="MAKSIMAR_SERVER.WORKFLOW_AUTOMATION_RUNTIME.jarvis_pc_action_adapter_contract",
                direct_allowed=bool(meta.get("direct_owner_gate", False)),
                owner_gate_required=True,
                approval_required=protected,
                read_only=False,
                protected=protected,
                status="degraded",
                reason="typed_mapping_configured_runtime_health_required:" + str(
                    meta.get("executor_function", "mapped_direct_pc_action")
                ),
                selection_enabled=True,
                execution_policy="verified_owner_typed_allowlist_runtime_health_required",
            )
        )
    return records




def _scan_local_content_capabilities() -> list[CapabilityRecord]:
    """Project-supported semantic content outcomes backed by the existing model-role provider."""
    return [
        _build_record(
            capability_id="content.metadata.generate",
            capability_kind="content",
            display_name="content metadata generation",
            source="internal_project",
            source_file_or_path=PROJECT_ROOT / "MAKSIMAR_SERVER/AI_ORCHESTRATION/model_role_adapter.py",
            import_path="MAKSIMAR_SERVER.AI_ORCHESTRATION.model_role_adapter",
            direct_allowed=True,
            owner_gate_required=False,
            approval_required=False,
            read_only=True,
            protected=False,
            status="available",
            reason="typed semantic content capability resolved through an installed local model provider role",
            execution_policy="per_step_policy",
        ),
        _build_record(
            capability_id="content.shorts.generate",
            capability_kind="content",
            display_name="shorts content generation",
            source="internal_project",
            source_file_or_path=PROJECT_ROOT / "MAKSIMAR_SERVER/AI_ORCHESTRATION/model_role_adapter.py",
            import_path="MAKSIMAR_SERVER.AI_ORCHESTRATION.model_role_adapter",
            direct_allowed=True, owner_gate_required=False, approval_required=False,
            read_only=True, protected=False, status="available",
            reason="bounded shorts script generation through canonical local model role",
            execution_policy="per_step_policy",
        ),
        _build_record(
            capability_id="code.proposal.generate",
            capability_kind="code",
            display_name="code proposal generation",
            source="internal_project",
            source_file_or_path=PROJECT_ROOT / "MAKSIMAR_SERVER/AI_ORCHESTRATION/model_role_adapter.py",
            import_path="MAKSIMAR_SERVER.AI_ORCHESTRATION.model_role_adapter",
            direct_allowed=True,
            owner_gate_required=False,
            approval_required=False,
            read_only=True,
            protected=False,
            status="available",
            reason="typed semantic code capability resolved through an installed local model provider role",
            execution_policy="per_step_policy",
        ),
        _build_record(
            capability_id="media.probe", capability_kind="media", display_name="local media probe",
            source="external_runtime", source_file_or_path=Path("/usr/bin/ffprobe"),
            runtime_python_or_executable=Path("/usr/bin/ffprobe"), direct_allowed=True,
            owner_gate_required=False, approval_required=False, read_only=True, protected=False,
            status="available", reason="installed ffprobe read-only provider",
            execution_policy="per_step_policy",
        ),
    ]


def _scan_readonly_tools(catalog: dict[str, Any] | None = None) -> list[CapabilityRecord]:
    catalog = catalog or build_jarvis_live_tool_catalog_read_model()
    tool_ids = tuple(catalog.get("read_tools", ()))
    source_path = PROJECT_ROOT / "tools/jarvis_live_runtime/jarvis_live_read_models.py"
    records = [
        _build_record(
            capability_id=str(tool_id),
            capability_kind="readonly_tool",
            display_name=str(tool_id).replace("_", " "),
            source="internal_project",
            source_file_or_path=source_path,
            import_path="tools.jarvis_live_runtime.jarvis_live_read_models",
            direct_allowed=True,
            owner_gate_required=False,
            approval_required=False,
            read_only=True,
            protected=False,
            status="available",
            reason="existing_readonly_catalog",
            execution_policy="direct_read_only",
        )
        for tool_id in tool_ids
    ]
    records.extend(
        (
            _build_record(
                capability_id="build_jarvis_live_tool_catalog_read_model",
                capability_kind="readonly_tool",
                display_name="jarvis live tool catalog",
                source="internal_project",
                source_file_or_path=source_path,
                import_path="tools.jarvis_live_runtime.jarvis_live_read_models",
                direct_allowed=True,
                owner_gate_required=False,
                approval_required=False,
                read_only=True,
                protected=False,
                status="available",
                reason="dispatcher_catalog_view",
                execution_policy="direct_visibility_status_planning",
            ),
            _build_record(
                capability_id="build_jarvis_live_memory_federation_status",
                capability_kind="readonly_tool",
                display_name="jarvis live memory federation status",
                source="internal_project",
                source_file_or_path=source_path,
                import_path="tools.jarvis_live_runtime.jarvis_live_read_models",
                direct_allowed=True,
                owner_gate_required=False,
                approval_required=False,
                read_only=True,
                protected=False,
                status="available",
                reason="memory_federation_view",
                execution_policy="direct_read_only",
            ),
            _build_record(
                capability_id="project_codegraph_readonly",
                capability_kind="readonly_tool",
                display_name="project codegraph readonly",
                source="internal_project",
                source_file_or_path=PROJECT_ROOT / "tools/jarvis_live_runtime/codegraph_readonly_adapter.py",
                import_path="tools.jarvis_live_runtime.codegraph_readonly_adapter",
                external_path=PROJECT_ROOT / "codegraph-out",
                runtime_python_or_executable=PROJECT_ROOT / ".venv/bin/codegraph",
                direct_allowed=True,
                owner_gate_required=False,
                approval_required=False,
                read_only=True,
                protected=False,
                status=str(inspect_codegraph_readonly_capability().get("status", "degraded")),
                reason=str(inspect_codegraph_readonly_capability().get("reason", "codegraph_readonly_capability")),
                selection_enabled=True,
                execution_policy="direct_read_only_report_query",
            ),
        )
    )
    return records


def _scan_memory_tools() -> list[CapabilityRecord]:
    memory_status = build_jarvis_live_memory_federation_status()
    surfaces = tuple(memory_status.get("surfaces", ()))
    records: list[CapabilityRecord] = []
    for surface in surfaces:
        if not isinstance(surface, dict):
            continue
        surface_id = str(surface.get("surface_id", "")).strip()
        if not surface_id:
            continue
        if (surface.get("runtime_status") == "SUPERSEDED_BY_CANONICAL_OWNER"
            or surface_id in {"session_memory", "runtime_history_store", "memory_engine_registry", "mempalace_search"}
            or surface_id not in MEMORY_CAPABILITY_OPERATION_CONTRACTS):
            continue  # Dedicated records below own these capabilities; views are not extra execution owners.
        status = "available" if surface.get("status") == "usable_now" else "degraded"
        records.append(
            _build_record(
                capability_id=surface_id,
                capability_kind="memory_tool",
                display_name=surface_id.replace("_", " "),
                source="internal_project",
                source_file_or_path=PROJECT_ROOT / "MAKSIMAR_SERVER/AI_ORCHESTRATION/memory_context_sources.py",
                import_path="MAKSIMAR_SERVER.AI_ORCHESTRATION.memory_context_sources",
                direct_allowed=True,
                owner_gate_required=False,
                approval_required=False,
                read_only=True,
                protected=False,
                status=status,
                reason=str(surface.get("status", "")),
                execution_policy="direct_read_only",
            )
        )
    try:
        definitions = list_memory_definitions()
        registry_status = "available"
        registry_reason = f"memory_definitions={len(definitions)}"
    except Exception as exc:
        registry_status = "degraded"
        registry_reason = type(exc).__name__
    records.extend(
        (
            _build_record(
                capability_id="session_memory",
                capability_kind="memory_tool",
                display_name="session memory",
                source="internal_project",
                source_file_or_path=SESSION_STATE_PATH,
                import_path="MAKSIMAR_SERVER.AI_ORCHESTRATION.session_memory_store",
                direct_allowed=True,
                owner_gate_required=False,
                approval_required=False,
                read_only=True,
                protected=False,
                status="available" if SESSION_STATE_PATH.exists() else "degraded",
                reason="session_state_path_exists" if SESSION_STATE_PATH.exists() else "session_state_path_missing",
                execution_policy="direct_read_only",
            ),
            _build_record(
                capability_id="runtime_history_store",
                capability_kind="memory_tool",
                display_name="runtime history store",
                source="internal_project",
                source_file_or_path=RUNTIME_HISTORY_STORE_ROOT,
                import_path="MAKSIMAR_CORE_LIB.memory_engine.history_ingestion",
                direct_allowed=True,
                owner_gate_required=False,
                approval_required=False,
                read_only=True,
                protected=False,
                status="available" if RUNTIME_HISTORY_STORE_ROOT.exists() else "degraded",
                reason="history_store_exists" if RUNTIME_HISTORY_STORE_ROOT.exists() else "history_store_missing",
                execution_policy="direct_read_only",
            ),
            _build_record(
                capability_id="memory_engine_registry",
                capability_kind="memory_tool",
                display_name="memory engine registry",
                source="internal_project",
                source_file_or_path=PROJECT_ROOT / "MAKSIMAR_CORE_LIB/memory_engine/memory_accessor.py",
                import_path="MAKSIMAR_CORE_LIB.memory_engine.memory_accessor",
                direct_allowed=True,
                owner_gate_required=False,
                approval_required=False,
                read_only=True,
                protected=False,
                status=registry_status,
                reason=registry_reason,
                execution_policy="direct_read_only",
            ),
            _build_record(
                capability_id="mempalace_search",
                capability_kind="memory_tool",
                display_name="Mempalace source archive search and native index refresh",
                source="external_runtime",
                source_file_or_path=MEMPALACE_ROOT,
                import_path="mempalace",
                external_path=MEMPALACE_DEFAULT_PALACE,
                runtime_python_or_executable=MEMPALACE_RUNTIME_PYTHON,
                direct_allowed=_mempalace_ready(),
                owner_gate_required=False,
                approval_required=False,
                read_only=False,
                protected=False,
                status=("available" if _mempalace_ready() else "degraded"),
                reason=("persisted palace available" if _mempalace_ready()
                        else "runtime installed but no persisted palace has been initialized/mined"),
                execution_policy="typed_per_operation_policy",
            ),
        )
    )
    return records


def _scan_retrieval_backends() -> list[CapabilityRecord]:
    availability = (
        inspect_mgrep_readonly_availability(PROJECT_ROOT).to_read_model(),
        inspect_sqlite_vec_readonly_availability(PROJECT_ROOT).to_read_model(),
        inspect_qdrant_readonly_availability(PROJECT_ROOT).to_read_model(),
    )
    records: list[CapabilityRecord] = []
    for item in availability:
        backend_kind = str(item["backend_kind"])
        capability_id = f"retrieval_backend:{backend_kind}"
        status = "available" if bool(item["available"]) else "degraded"
        if backend_kind == "qdrant" and bool(item["source_present"]):
            status = "degraded"
        records.append(
            _build_record(
                capability_id=capability_id,
                capability_kind="retrieval_backend",
                display_name=backend_kind.replace("_", " "),
                source="vendor_quarantine",
                source_file_or_path=item["vendor_path"],
                import_path="MAKSIMAR_CORE_LIB.retrieval_backend.retrieval_runtime_readonly_tools",
                external_path=item["vendor_path"],
                direct_allowed=bool(item["available"]),
                owner_gate_required=False,
                approval_required=False,
                read_only=True,
                protected=False,
                status=status,
                reason=str(item["unavailable_reason"]),
                execution_policy="direct_read_search_status",
            )
        )
    registry = build_retrieval_tool_registry_contract()
    for contract in registry.tools:
        records.append(
            _build_record(
                capability_id=contract.tool_kind,
                capability_kind="retrieval_tool",
                display_name=contract.tool_kind.replace("_", " "),
                source="internal_project",
                source_file_or_path=PROJECT_ROOT / "MAKSIMAR_CORE_LIB/retrieval_backend",
                import_path="MAKSIMAR_CORE_LIB.retrieval_backend",
                direct_allowed=True,
                owner_gate_required=False,
                approval_required=False,
                read_only=True,
                protected=False,
                status="available",
                reason="retrieval_tool_registry_contract",
                execution_policy="direct_read_only",
            )
        )
    return records


def _scan_skills() -> list[CapabilityRecord]:
    registry = build_skill_adapter_registry_contract()
    return [
        _build_record(
            capability_id=entry.skill_id,
            capability_kind="skill",
            display_name=entry.module_slug.replace("_", " "),
            source="internal_project",
            source_file_or_path=PROJECT_ROOT / "MAKSIMAR_SERVER/SKILL_ADAPTER_REGISTRY",
            import_path="MAKSIMAR_SERVER.SKILL_ADAPTER_REGISTRY.skill_adapter_registry_contract",
            direct_allowed=entry.adapter_execution_mode == "read_only",
            owner_gate_required=False,
            approval_required=entry.adapter_execution_mode != "read_only",
            read_only=entry.adapter_execution_mode == "read_only",
            protected=entry.adapter_execution_mode != "read_only",
            status="available" if entry.active else "degraded",
            reason=entry.adapter_execution_mode,
            execution_policy="direct_read_only" if entry.adapter_execution_mode == "read_only" else "approval_required",
        )
        for entry in registry.entries
    ]


def _scan_agents() -> list[CapabilityRecord]:
    records: list[CapabilityRecord] = []
    for contract in build_default_swarm_agent_role_contracts():
        records.append(
            _build_record(
                capability_id=contract.role_id,
                capability_kind="agent",
                display_name=contract.role_id.replace("_", " "),
                source="internal_project",
                source_file_or_path=PROJECT_ROOT / "MAKSIMAR_CORE_LIB/swarm_coordination/swarm_agent_role_contract.py",
                import_path="MAKSIMAR_CORE_LIB.swarm_coordination.swarm_agent_role_contract",
                direct_allowed=True,
                owner_gate_required=False,
                approval_required=True,
                read_only=False,
                protected=True,
                status="available",
                reason="swarm_agent_role_contract",
                execution_policy="direct_planning_approval_for_execution",
            )
        )
    return records


def _scan_workers() -> list[CapabilityRecord]:
    contract = build_worker_registry_contract()
    return [
        _build_record(
            capability_id=worker.worker_id,
            capability_kind="worker",
            display_name=worker.worker_type.replace("_", " "),
            source="internal_project",
            source_file_or_path=PROJECT_ROOT / "MAKSIMAR_CORE_LIB/workers_registry/worker_registry_contract.py",
            import_path="MAKSIMAR_CORE_LIB.workers_registry.worker_registry_contract",
            direct_allowed=False,
            owner_gate_required=False,
            approval_required=True,
            read_only=False,
            protected=True,
            status="available" if worker.active else "degraded",
            reason=worker.target_node,
            execution_policy="approval_required",
        )
        for worker in contract.workers
    ]


def _scan_external_adapters(visibility: dict[str, Any] | None = None) -> list[CapabilityRecord]:
    visibility = visibility or build_jarvis_external_adapter_visibility_read_model()
    adapter_map = {
        str(item["tool_id"]): item
        for item in visibility.get("adapters", ())
        if isinstance(item, dict)
    }
    records: list[CapabilityRecord] = []
    for manifest_path in sorted(AGENT_TOOLING_MANIFEST_ROOT.glob("*_manifest.json")):
        payload = _safe_read_json(manifest_path)
        capability_id = str(payload.get("tool_id", "")).strip()
        if not capability_id.startswith("external_adapter:"):
            continue
        adapter = adapter_map.get(capability_id, {})
        metadata = payload.get("metadata", {}) if isinstance(payload.get("metadata", {}), dict) else {}
        external_path = str(metadata.get("external_path", "")).strip()
        status = str(adapter.get("availability_status", "")).strip() or ("available" if external_path and Path(external_path).expanduser().exists() else "degraded")
        reason = str(adapter.get("activation_blocked_reason", "")).strip() or str(payload.get("description", "")).strip()
        if capability_id == "external_adapter:n8n":
            reason = "status/templates/planning direct; create/run/activate/credentials require approval"
        elif capability_id == "external_adapter:mempalace":
            reason = "status/search/read_only query direct; mining/write/sync/repair gated"
        elif capability_id == "external_adapter:smolagents":
            reason = "status/list/planning direct; protected tool execution requires owner gate and approval"
        records.append(
            _build_record(
                capability_id=capability_id,
                capability_kind="external_adapter",
                display_name=str(payload.get("source_library", capability_id)).strip(),
                source="external_runtime" if capability_id == "external_adapter:smolagents" else "vendor_quarantine",
                source_file_or_path=manifest_path,
                import_path=str(payload.get("module_import_name", "")).strip(),
                external_path=external_path,
                runtime_python_or_executable=str(adapter.get("runtime_python", "")).strip(),
                direct_allowed=True,
                owner_gate_required=capability_id == "external_adapter:smolagents",
                approval_required=True,
                read_only=False,
                protected=True,
                status="available" if status == "available" else "degraded",
                reason=reason,
                selection_enabled=True,
                execution_policy=(
                    "direct_status_list_planning_read_only_tools_owner_gate_for_pc_browser_file_shell_write"
                    if capability_id == "external_adapter:smolagents"
                    else "direct_status_templates_planning_approval_for_execution"
                ),
            )
        )
    n8n_contract = build_n8n_adapter_contract()
    records.append(
        _build_record(
            capability_id="workflow_automation:n8n",
            capability_kind="workflow_automation",
            display_name="n8n workflow automation",
            source="vendor_quarantine",
            source_file_or_path=PROJECT_ROOT / "MAKSIMAR_SERVER/WORKFLOW_AUTOMATION_RUNTIME/n8n_adapter_contract.py",
            import_path="MAKSIMAR_SERVER.WORKFLOW_AUTOMATION_RUNTIME.n8n_adapter_contract",
            external_path=N8N_ROOT,
            direct_allowed=True,
            owner_gate_required=False,
            approval_required=True,
            read_only=False,
            protected=True,
            status="available" if N8N_ROOT.exists() else "external_not_found",
            reason="n8n-compatible graph inspection and planning are direct; runtime execution remains approval-gated",
            execution_policy="direct_status_templates_graph_planning_approval_for_create_run_activate_credentials",
        )
    )
    return records


def _scan_runtime_tooling() -> list[CapabilityRecord]:
    flutter_exists = FLUTTER_ROOT.exists()
    return [
        _build_record(
            capability_id="runtime_tooling:flutter",
            capability_kind="runtime_tooling",
            display_name="Flutter runtime",
            source="external_runtime",
            source_file_or_path=FLUTTER_ROOT,
            external_path=FLUTTER_ROOT,
            runtime_python_or_executable=FLUTTER_ROOT / "bin/flutter",
            direct_allowed=True,
            owner_gate_required=False,
            approval_required=True,
            read_only=False,
            protected=True,
            status="available" if flutter_exists else "external_not_found",
            reason="status/path/version/planning direct; build/deploy/device/network exposure require approval",
            execution_policy="direct_status_project_structure_planning_approval_for_build_deploy_device",
        )
    ]


def _scan_runtime_voice() -> list[CapabilityRecord]:
    records: list[CapabilityRecord] = []
    for capability_id, path in VOICE_RUNTIME_PATHS.items():
        exists = path.exists()
        records.append(
            _build_record(
                capability_id=capability_id,
                capability_kind="runtime_voice",
                display_name=capability_id.split(":", 1)[1].replace("_", " "),
                source="external_runtime",
                source_file_or_path=path,
                external_path=path,
                runtime_python_or_executable=path / "bin/python",
                direct_allowed=True,
                owner_gate_required=False,
                approval_required=capability_id != "runtime_voice:faster_whisper",
                read_only=capability_id == "runtime_voice:faster_whisper",
                protected=capability_id != "runtime_voice:faster_whisper",
                status="available" if exists else "external_not_found",
                reason="runtime voice component detected",
                execution_policy="direct_status_probe_read_only" if capability_id == "runtime_voice:faster_whisper" else "direct_status_probe_approval_for_mutation",
            )
        )
    return records


def _scan_windows_edge() -> list[CapabilityRecord]:
    exists = WINDOWS_EDGE_VENV.exists()
    return [
        _build_record(
            capability_id="runtime_windows_edge",
            capability_kind="runtime_windows_edge",
            display_name="Windows Voice Edge",
            source="external_runtime",
            source_file_or_path=WINDOWS_EDGE_VENV,
            external_path=WINDOWS_EDGE_VENV,
            runtime_python_or_executable=WINDOWS_EDGE_VENV / "Scripts/python.exe",
            direct_allowed=True,
            owner_gate_required=True,
            approval_required=True,
            read_only=False,
            protected=True,
            status="available" if exists else "external_not_found",
            reason="owner/family gated PC bridge with localhost-only boundary",
            execution_policy="direct_status_owner_gate_plus_approval_for_protected_execution",
        )
    ]


def _scan_runtime_library_sources() -> list[CapabilityRecord]:
    runtime_store = build_runtime_library_store_read_model()
    records: list[CapabilityRecord] = []
    for capability_id, path in JARVIS_LIBRARY_DIRS.items():
        exists = path.exists()
        reason = "runtime library directory present" if exists else "runtime library directory missing"
        records.append(
            _build_record(
                capability_id=capability_id,
                capability_kind="jarvis_runtime_library",
                display_name=capability_id.split(":", 1)[1].replace("_", " "),
                source="external_runtime",
                source_file_or_path=path,
                external_path=path,
                runtime_python_or_executable=runtime_store.get("probe_report_dir", ""),
                direct_allowed=True,
                owner_gate_required=False,
                approval_required=False,
                read_only=True,
                protected=False,
                status="available" if exists else "external_not_found",
                reason=reason,
                execution_policy="direct_visibility_status_planning",
            )
        )
    return records



def current_environment_has_module(import_name: str) -> bool:
    if not import_name:
        return False
    return importlib.util.find_spec(import_name) is not None


__all__ = [
    "CapabilityRecord",
    "build_existing_capability_inventory",
    "build_existing_capability_inventory_summary",
    "build_global_semantic_capability_projection",
    "current_environment_has_module",
]
