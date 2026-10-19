"""Authenticated downstream projections; no new event/approval/config authority."""
from __future__ import annotations

import base64
import hashlib
import json
import os
import time
from datetime import UTC, datetime
from pathlib import Path
from typing import Any

from fastapi import HTTPException
from MAKSIMAR_CORE_LIB.event_bus.event_paths import get_event_journal_path
from MAKSIMAR_CORE_LIB.event_bus.event_reader import _parse_event_line
from MAKSIMAR_CORE_LIB.security_layer.host_principal import identity_from_host_token
from MAKSIMAR_CORE_LIB.security_layer.semantic_policy import SemanticPolicyEvaluator


def require_operator_read(token: str, session_id: str):
    verified = identity_from_host_token(token)
    if verified is None:
        raise HTTPException(401, "verified_host_principal_required")
    principal, identity = verified
    if not session_id or principal.session_id != session_id:
        raise HTTPException(403, "host_session_mismatch")
    decision = SemanticPolicyEvaluator().evaluate(
        capability_id="project.read", operation_id="read_operator_projection",
        risk_class="READ_ONLY", effect_type="OBSERVE", target_scope="operator_read_projection",
        identity=identity, trace_id="operator_read", reversibility="REVERSIBLE",
    )
    if not identity.owner_authorized or not decision.granted:
        raise HTTPException(403, "operator_read_denied")
    return principal, identity, decision


def envelope(value: Any, *, source: str, produced_at: str | None = None,
             unit: str | None = None, max_age_seconds: float | None = None,
             status: str = "NO_DATA") -> dict[str, Any]:
    now = datetime.now(UTC)
    age = None
    if produced_at:
        try:
            produced = datetime.fromisoformat(produced_at.replace("Z", "+00:00"))
            if produced.tzinfo is None:
                raise ValueError("producer timezone missing")
            age = (now - produced).total_seconds()
            if age < -5:
                status = "DEGRADED"
            elif max_age_seconds is not None and age > max_age_seconds:
                status = "STALE"
        except (ValueError, TypeError):
            status = "DEGRADED"
    elif status == "LIVE":
        status = "NO_DATA"
    return {"value": value, "unit": unit, "source": source,
            "observed_at": now.isoformat(), "produced_at": produced_at,
            "freshness": {"age_seconds": age, "max_age_seconds": max_age_seconds},
            "status": status, "provenance": source, "schema_version": "operator_value.v1"}


def _identifier(value: str) -> str:
    allowed = "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789_.:-/"
    return value[:128] if value and len(value) <= 128 and all(c in allowed for c in value) else "REDACTED"


def event_projection(*, cursor: str = "", limit: int = 100,
                     journal: Path | None = None) -> dict[str, Any]:
    """Bounded cursor over the existing journal; payloads are never exposed."""
    if not 1 <= limit <= 200:
        raise HTTPException(422, "event_limit_out_of_range")
    path = journal or get_event_journal_path()
    if not path.is_file():
        return {"events": [], "cursor": "", "reset": bool(cursor),
                "state": envelope(None, source=str(path), status="NO_DATA")}
    events = []; errors = 0; reset = False
    with path.open("rb") as handle:
        stat = os.fstat(handle.fileno())
        prefix = handle.readline(65537); handle.seek(0)
        generation = f"{stat.st_dev}:{stat.st_ino}:" + hashlib.sha256(prefix).hexdigest()
        offset = 0
        if cursor:
            try:
                if len(cursor) > 1024: raise ValueError("cursor too large")
                saved = json.loads(base64.urlsafe_b64decode(cursor + "=" * (-len(cursor) % 4)))
                if saved["generation"] != generation or not isinstance(saved["offset"], int) or not 0 <= saved["offset"] <= stat.st_size:
                    reset = True
                else:
                    offset = saved["offset"]
                    # Only a line boundary can be resumed. Never read fragments.
                    if offset:
                        handle.seek(offset - 1)
                        if handle.read(1) != b"\n": raise ValueError("cursor not at boundary")
            except (ValueError, KeyError, TypeError, json.JSONDecodeError):
                raise HTTPException(422, "invalid_event_cursor") from None
        handle.seek(offset)
        scanned = 0
        while len(events) < limit and scanned < 400:
            start = handle.tell(); raw = handle.readline(65537)
            if not raw: break
            if not raw.endswith(b"\n"):
                if len(raw) > 65536:
                    raise HTTPException(503, "oversized_event_record")
                handle.seek(start); break  # producer has not completed this line
            offset = handle.tell(); scanned += 1
            try:
                record = _parse_event_line(raw.decode("utf-8"))
                event = {"event_id": _identifier(record.event_id), "event_type": _identifier(record.event_type),
                         "source": _identifier(record.source), "created_at": record.created_at,
                         "payload_redacted": True}
                state = envelope(None, source=event["source"], produced_at=record.created_at,
                                 max_age_seconds=60, status="LIVE")
                # 60s is explicit presentation freshness, never event-bus health.
                event["freshness"] = state["freshness"]; event["status"] = state["status"]
                if state["status"] == "DEGRADED": errors += 1; continue
                events.append(event)
            except (ValueError, KeyError, TypeError, UnicodeError): errors += 1
    next_cursor = base64.urlsafe_b64encode(json.dumps({"generation": generation, "offset": offset}).encode()).decode().rstrip("=")
    return {"events": events, "cursor": next_cursor, "reset": reset, "parse_errors": errors,
            "state": envelope(len(events), source=str(path), produced_at=datetime.fromtimestamp(stat.st_mtime, UTC).isoformat(),
                              unit="events_in_page", max_age_seconds=60, status="DEGRADED" if errors else "LIVE"),
            "read_only": True, "scope": "verified_owner_only; payload omitted; no bus availability inference"}


def foundation_projection(root: Path) -> dict[str, Any]:
    expected = {"runtime": ("heartbeat_state.json", "process_supervisor"),
                "guard": ("guard_heartbeat_state.json", "stop_gate_watcher"),
                "core_guard": ("core_guard_heartbeat_state.json", "core_guard"),
                "kernel_guard": ("kernel_heartbeat_state.json", "kernel_watchdog")}
    result = {}
    for scope, (name, owner) in expected.items():
        path = root / "RUNTIME/state" / name
        try:
            payload = json.loads(path.read_text())
            produced = datetime.fromtimestamp(float(payload["ts"]), UTC).isoformat()
            state = "LIVE" if payload.get("status") == "alive" and payload.get("source") == owner else "SERVICE_OFFLINE"
            result[scope] = envelope(payload.get("status"), source=str(path), produced_at=produced,
                                     max_age_seconds=10, status=state)
        except (OSError, ValueError, KeyError, TypeError):
            result[scope] = envelope(None, source=str(path), status="NO_DATA")
    return result


def supervisor_settings_projection() -> list[dict[str, Any]]:
    """Read only the existing child environment; defaults belong to supervisor."""
    from SUPERVISOR.process_supervisor import build_environment
    configured = build_environment()
    names = ("JARVIS_HELPER_INPUT_CORRECTION_ENABLED", "JARVIS_HELPER_MODEL",
             "OLLAMA_NUM_PARALLEL", "OLLAMA_MAX_LOADED_MODELS")
    return [{"setting_id": "SUPERVISOR.environment." + name,
             "owner": "SUPERVISOR/process_supervisor.py:build_environment",
             "value": configured[name], "value_source": "actual child environment" if name in os.environ else "supervisor default",
             "read_only": True, "writer": None, "validation": "existing owner environment contract",
             "restart_requirement": "supervisor child restart for environment change", "ui_control": "readonly_value",
             "secret": False} for name in names]


def model_runtime_projection() -> dict[str, Any]:
    """Observe the existing Ollama transport; declarations are not liveness."""
    from MAKSIMAR_SERVER.AI_ORCHESTRATION.ollama_transport import ollama_get_json, OLLAMA_BASE_URL
    from MAKSIMAR_CORE_LIB.ai_orchestration.model_profile_registry_contract import build_jarvis_live_runtime_model_role_profiles
    tags = ollama_get_json('/api/tags', timeout_seconds=2)
    observed = datetime.now(UTC).isoformat()
    if not isinstance(tags.get('models'), list):
        return {'state': envelope(None, source=OLLAMA_BASE_URL + '/api/tags', status='SERVICE_OFFLINE'), 'roles': []}
    models = tags['models']
    by_name = {str(m.get('name', '')): m for m in models if isinstance(m, dict)}
    roles = []
    for profile in build_jarvis_live_runtime_model_role_profiles():
        installed = by_name.get(profile.model_id)
        target = by_name.get(profile.target_model_id)
        family = str((installed or {}).get('details', {}).get('family', 'UNKNOWN'))
        target_family = str((target or {}).get('details', {}).get('family', 'UNKNOWN'))
        parent = str((installed or {}).get('details', {}).get('parent_model', 'UNKNOWN'))
        status = 'NOT_CONNECTED' if installed is None else 'LIVE'
        if installed and (target is None or family != target_family or parent != profile.target_model_id): status = 'DEGRADED'
        roles.append({'role_id': profile.role_id, 'model_id': profile.model_id,
                      'declared_target': profile.target_model_id, 'observed_family': family,
                      'observed_parent_model': parent,
                      'target_installed': target is not None,
                      'runtime': envelope(installed is not None, source=OLLAMA_BASE_URL + '/api/tags',
                                          produced_at=observed, max_age_seconds=15, status=status),
                      'acceptance': 'DRIFTED_OR_TARGET_UNPROVED' if status == 'DEGRADED' else status,
                      'proposal_only': profile.proposal_only})
    return {'state': envelope(len(models), source=OLLAMA_BASE_URL + '/api/tags', unit='installed_models',
                              produced_at=observed, max_age_seconds=15, status='LIVE'),
            'roles': roles, 'scope': 'actual tag/parent/family observation; no inference success claim'}


def local_host_projection(root: Path) -> dict[str, Any]:
    """Thin field envelopes over the existing WSL host snapshot owner."""
    from CONTROL_PLANE.health.monitor import take_snapshot
    source = 'CONTROL_PLANE/health/monitor.py:take_snapshot'
    try:
        snapshot = take_snapshot(str(root))
        produced = datetime.fromtimestamp(snapshot.ts, UTC).isoformat()
        fields = {
            'uptime_seconds': (snapshot.uptime_s, 'seconds'),
            'cpu_count': (snapshot.cpu_count, 'logical_cpus'),
            'load_average': (snapshot.loadavg, 'runnable_process_load_1m_5m_15m'),
            'memory_total_bytes': (snapshot.mem_total, 'bytes'),
            'memory_used_bytes': (snapshot.mem_used, 'bytes'),
            'root_filesystem_total_bytes': (snapshot.disk_total, 'bytes'),
            'root_filesystem_free_bytes': (snapshot.disk_free, 'bytes'),
        }
        return {'scope': 'local WSL Linux host and project root filesystem only; not Windows desktop or federated fleet',
                'fields': {name: envelope(value, source=source, produced_at=produced,
                                         unit=unit, max_age_seconds=10, status='LIVE')
                           for name, (value, unit) in fields.items()}}
    except (OSError, ValueError):
        return {'scope': 'local WSL host only', 'state': envelope(None, source=source, status='NO_DATA')}
