from __future__ import annotations

import json
import hashlib
import os
import time
from collections import deque
from pathlib import Path
from threading import RLock
from typing import Any
from datetime import datetime, timezone

from MAKSIMAR_CORE_LIB.ai_orchestration.semantic_intent_contract import IdentityContext


PROJECT_ROOT = Path(__file__).resolve().parents[2]
RUNTIME_ROOT = Path.home() / "MAKSIMAR_RUNTIME" / "jarvis_live"
SESSION_MEMORY_ROOT = RUNTIME_ROOT / "session_memory"
SESSION_STATE_PATH = SESSION_MEMORY_ROOT / "jarvis_live_session_state.json"
SESSION_TURN_LOG_NAME = "jarvis_live_terminal_turns.jsonl"

MAX_RECENT_TURNS = 4

# Derived cache only: classification truth stays in the same append-only journal.
_EXCLUSION_CACHE: tuple[tuple[str, int, int, int], frozenset[str]] | None = None
_EXCLUSION_LOCK = RLock()
_EXCLUSION_SOURCE = "canonical_session_record_exclusion"


def session_record_sha256(record: dict[str, Any]) -> str:
    """Exact immutable record identity; never classify from prose or session names."""
    return hashlib.sha256(json.dumps(record, ensure_ascii=False, sort_keys=True,
                                     separators=(",", ":")).encode("utf-8")).hexdigest()


def _session_excluded_record_hashes() -> frozenset[str]:
    global _EXCLUSION_CACHE
    path = _session_turn_log_path()
    try:
        stat = path.stat()
    except FileNotFoundError:
        return frozenset()
    signature = (str(path.resolve()), stat.st_ino, stat.st_size, stat.st_mtime_ns)
    with _EXCLUSION_LOCK:
        if _EXCLUSION_CACHE is not None and _EXCLUSION_CACHE[0] == signature:
            return _EXCLUSION_CACHE[1]
        excluded: set[str] = set()
        known: set[str] = set()
        # An unreadable row could contain classification evidence. Never infer
        # semantic eligibility by skipping unknown/corrupt journal contents.
        with path.open("rb") as handle:
            for line in handle:
                try:
                    record = json.loads(line)
                except (ValueError, TypeError) as exc:
                    raise ValueError("canonical_session_classification_unreadable_journal") from exc
                if not isinstance(record, dict):
                    raise ValueError("canonical_session_classification_unreadable_journal")
                if (record.get("source") != _EXCLUSION_SOURCE
                    and record.get("schema_version") != "canonical_session_record_exclusion.v1"):
                    if record.get("source") != "jarvis_terminal_chat":
                        raise ValueError("canonical_session_classification_unknown_record_type")
                    known.add(session_record_sha256(record))
                    continue
                hashes = record.get("record_sha256s")
                refs = record.get("evidence_refs")
                if (not line.endswith(b"\n")
                    or record.get("source") != _EXCLUSION_SOURCE
                    or record.get("schema_version") != "canonical_session_record_exclusion.v1"
                    or record.get("persistence_status") != "PERSISTED"
                    or not _canonical_timestamp(record.get("persisted_at"))
                    or record.get("classification") not in {"TEST_FIXTURE", "NON_USER_DIAGNOSTIC"}
                    or not isinstance(hashes, list) or not hashes
                    or any(not isinstance(h, str) or len(h) != 64
                           or any(c not in "0123456789abcdef" for c in h) for h in hashes)
                    or not isinstance(refs, list) or not refs
                    or any(not isinstance(ref, str) or not ref.strip() for ref in refs)
                    or any(h not in known for h in hashes)):
                    raise ValueError("invalid_canonical_session_exclusion_evidence")
                excluded.update(hashes)
        result = frozenset(excluded)
        _EXCLUSION_CACHE = signature, result
        return result


def session_record_semantically_eligible(record: dict[str, Any]) -> bool:
    """Shared exclusion for history, context, grounding and experience qualification."""
    return (record.get("source") != _EXCLUSION_SOURCE
            and session_record_sha256(record) not in _session_excluded_record_hashes())


def _canonical_timestamp(value: Any) -> str:
    """Accept real timezone-aware source dates, never placeholders or file times."""
    if not isinstance(value, str) or not value:
        return ""
    try:
        parsed = datetime.fromisoformat(value.replace("Z", "+00:00"))
    except ValueError:
        return ""
    if parsed.tzinfo is None:
        return ""
    return parsed.astimezone(timezone.utc).isoformat().replace("+00:00", "Z")


def canonical_experience_projection(record: dict[str, Any]) -> dict[str, Any] | None:
    """One read-compatible experience shape over the existing append-only store."""
    if not session_record_semantically_eligible(record):
        return None
    artifact = record.get("artifact") if isinstance(record.get("artifact"), dict) else {}
    raw = artifact.get("learning_experience") or record.get("learning_experience")
    if not isinstance(raw, dict) or not raw.get("experience_id"):
        return None
    durable = record.get("experience") if isinstance(record.get("experience"), dict) else {}
    bundle = artifact.get("learning_bundle") if isinstance(artifact.get("learning_bundle"), dict) else {}
    observed = _canonical_timestamp(durable.get("observed_at") or artifact.get("observed_at"))
    created = _canonical_timestamp(durable.get("created_at") or bundle.get("created_at"))
    persisted = _canonical_timestamp(durable.get("persisted_at") or record.get("persisted_at"))
    refs = tuple(raw.get("verification_refs", ()))
    provenance = tuple(dict.fromkeys(filter(None, (
        raw.get("provenance_ref", ""), "trace://" + str(record["trace_id"]) if record.get("trace_id") else "",
        *bundle.get("provenance", ()),
    ))))
    return {
        "schema_version": "canonical_experience.v1", "experience_id": str(raw["experience_id"]),
        "experience_kind": raw.get("experience_kind", ""), "actor": raw.get("actor", ""),
        "task_ref": raw.get("task_ref", ""), "session_id": record.get("session_id", ""),
        "trace_id": record.get("trace_id", ""), "created_at": created, "observed_at": observed,
        "persisted_at": persisted, "timestamp_status": "KNOWN" if observed or created else "UNKNOWN_LEGACY",
        "verification_status": raw.get("verification_status", "PENDING"),
        "qualification_status": raw.get("verification_status", "PENDING"),
        "review_status": artifact.get("audit_verdict", "UNKNOWN"), "audit_verdict": artifact.get("audit_verdict", "UNKNOWN"),
        "review_ref": refs[0] if refs else "", "verification_refs": refs,
        "evidence_refs": tuple(raw.get("evidence_refs", ())), "provenance_refs": provenance,
        "learning_bundle_id": bundle.get("bundle_id", ""),
        "learning_bundle_hash": artifact.get("learning_bundle_hash", ""),
        "learning_bundle_version": bundle.get("schema_version", ""),
        "execution_receipt_refs": tuple(receipt.get("receipt_id", "") for receipt in artifact.get("execution_receipts", ()) if isinstance(receipt, dict)),
        "execution_receipts": tuple(artifact.get("execution_receipts", ())),
        "source_node": bundle.get("source_node", ""), "source_body": bundle.get("source_body", ""),
        "capability_id": bundle.get("capability_id", ""), "artifact_kind": artifact.get("kind", ""),
        "training_eligible": raw.get("training_eligible", False),
        "training_export_allowed": raw.get("training_export_allowed", False),
        "training_candidate_creation_allowed": raw.get("training_candidate_creation_allowed", False),
        "active_model_runtime_mutation_allowed": False, "active_model_auto_promotion_allowed": False,
        "persistence_status": record.get("persistence_status", "UNKNOWN"), "non_canonical": True,
    }


class CanonicalSessionContextStore:
    """Server-owned identity-isolated bounded context inside the existing session store."""

    def __init__(
        self,
        *,
        max_turns: int = 6,
        max_text_chars: int = 1200,
        max_context_chars: int = 900,
        max_turn_context_chars: int = 420,
    ) -> None:
        self.max_turns = max_turns
        self.max_text_chars = max_text_chars
        self.max_context_chars = max_context_chars
        self.max_turn_context_chars = max_turn_context_chars
        self._events: dict[tuple[str, str], deque[dict[str, Any]]] = {}
        self._lock = RLock()

    @staticmethod
    def _key(session_id: str, identity: IdentityContext) -> tuple[str, str]:
        return identity.identity_id, session_id

    def _restore_persisted_context(self, session_id: str, identity: IdentityContext) -> None:
        """Lazy restart recovery from the same append log, with exact isolation.

        Historical rows lacking identity/session binding cannot enter a session.
        Stream the file into a bounded deque; never create another session store.
        """
        # Validate even a corrupt-only journal or an already-cached empty context.
        # Eligibility cannot depend on encountering a parsable chat row first.
        _session_excluded_record_hashes()
        key = self._key(session_id, identity)
        with self._lock:
            if key in self._events:
                return
            restored: deque[dict[str, Any]] = deque(maxlen=self.max_turns * 4)
            try:
                with _session_turn_log_path().open("r", encoding="utf-8") as handle:
                    for line in handle:
                        try:
                            item = json.loads(line)
                        except (ValueError, TypeError):
                            continue
                        if (isinstance(item, dict) and item.get("source") == "jarvis_terminal_chat"
                            and item.get("identity_id") == identity.identity_id
                            and item.get("session_id") == session_id
                            and item.get("persistence_status") == "PERSISTED"):
                            if session_record_semantically_eligible(item):
                                restored.append(item)
            except FileNotFoundError:
                pass
            except (OSError, UnicodeError) as exc:
                raise ValueError("canonical_session_context_unreadable_journal") from exc
            self._events[key] = restored

    def read(self, session_id: str, identity: IdentityContext) -> dict[str, Any]:
        self._restore_persisted_context(session_id, identity)
        key = self._key(session_id, identity)
        with self._lock:
            all_events = tuple(item for item in self._events.get(key, ())
                               if session_record_semantically_eligible(item))
        selected = all_events[-self.max_turns:]
        remaining_chars = self.max_context_chars
        bounded_reversed: list[dict[str, Any]] = []
        text_was_truncated = False
        for item in reversed(selected):
            if remaining_chars <= 0:
                break
            turn_budget = min(self.max_turn_context_chars, remaining_chars)
            user_text = str(item.get("user_text", ""))[:min(self.max_text_chars, 160, turn_budget)]
            turn_budget -= len(user_text)
            assistant_text = str(item.get("assistant_text", ""))[
                :min(self.max_text_chars, 220, max(0, turn_budget))
            ]
            turn_budget -= len(assistant_text)
            topic = str(item.get("topic", ""))[:min(40, max(0, turn_budget))]
            used_chars = len(user_text) + len(assistant_text) + len(topic)
            remaining_chars -= used_chars
            text_was_truncated = text_was_truncated or any((
                len(user_text) < len(str(item.get("user_text", ""))),
                len(assistant_text) < len(str(item.get("assistant_text", ""))),
            ))
            bounded_reversed.append({
                "user_text": user_text,
                "assistant_text": assistant_text,
                "topic": topic,
                "trace_id": str(item.get("trace_id", "")),
            })
        turns = tuple(reversed(bounded_reversed))
        omitted_turn_count = max(0, len(all_events) - len(turns))
        unresolved = next((str(item.get("unresolved_reference", "")) for item in reversed(selected)
                           if item.get("unresolved_reference")), "")
        return {
            "schema_version": "bounded_session_context.v2",
            "session_id": session_id,
            "identity_facts": {
                "identity_id": identity.identity_id,
                "display_name": identity.display_name,
                "profile_type": identity.profile_type,
                "assistant_identity": identity.assistant_identity,
            },
            "bounded_chronological_turns": turns,
            "recent_artifacts": tuple(
                dict(item["artifact"]) for item in reversed(all_events)
                if isinstance(item.get("artifact"), dict)
            )[:4],
            "recent_relevant_turns": (),
            "current_topic": "",
            "unresolved_reference": {
                "present": bool(unresolved),
                "description": unresolved[:300],
                "resolution_scope": "bounded_same_identity_session",
            },
            "selection_basis": "model_semantic_selection_pending",
            "truncated": text_was_truncated or omitted_turn_count > 0,
            "omitted_turn_count": omitted_turn_count,
            "context_text_char_budget": self.max_context_chars,
            "browser_page_context": next((dict(item.get("browser_page_context", {})) for item in reversed(all_events) if isinstance(item.get("browser_page_context"), dict)), {}),
        }

    def append(self, session_id: str, identity: IdentityContext, *, user_text: str, assistant_text: str,
               topic: str, unresolved_reference: str, trace_id: str,
               artifact: dict[str, Any] | None = None) -> dict[str, Any]:
        self._restore_persisted_context(session_id, identity)
        event = {
            "schema_version": "canonical_session_event.v4", "session_id": session_id,
            "identity_id": identity.identity_id,
            "source": "jarvis_terminal_chat",
            "user_text": user_text[:self.max_text_chars], "assistant_text": assistant_text[:self.max_text_chars],
            "topic": topic[:160], "unresolved_reference": unresolved_reference[:300], "trace_id": trace_id,
            "persistence_status": "PENDING",
            "persisted_at": _timestamp(),
        }
        if artifact:
            event["artifact"] = {
                "kind": str(artifact.get("kind", "")),
                "provider": str(artifact.get("provider", "")),
                "provider_id": str(artifact.get("provider_id", "")),
            "trace_id": trace_id,
            }
            if isinstance(artifact.get("learning_experience"), dict):
                event["artifact"]["learning_experience"] = dict(artifact["learning_experience"])
            if "audit_verdict" in artifact:
                event["artifact"]["audit_verdict"] = str(artifact["audit_verdict"])
            if isinstance(artifact.get("retrieval_trace"), dict):
                event["artifact"]["retrieval_trace"] = dict(artifact["retrieval_trace"])
            if isinstance(artifact.get("execution_receipts"), (list, tuple)):
                event["artifact"]["execution_receipts"] = [
                    {key: receipt[key] for key in (
                        "schema_version", "receipt_id", "request_id", "trace_id", "step_id",
                        "capability_id", "operation_id", "provider_id", "status", "result",
                    ) if key in receipt}
                    for receipt in artifact["execution_receipts"][:16] if isinstance(receipt, dict)
                    and receipt.get("trace_id") == trace_id and receipt.get("schema_version") == "execution_receipt.v1"
                ]
            event["artifact"]["observed_at"] = _canonical_timestamp(artifact.get("observed_at"))
            if isinstance(artifact.get("learning_bundle"), dict):
                event["artifact"]["learning_bundle"] = {
                    key: artifact["learning_bundle"][key] for key in (
                        "schema_version", "bundle_id", "source_node", "source_body", "source_actor",
                        "created_at", "capability_id", "artifact_ref", "evidence_refs", "evaluation_refs", "provenance",
                    ) if key in artifact["learning_bundle"]
                }
                event["artifact"]["learning_bundle_hash"] = str(artifact.get("learning_bundle_hash", ""))
        if isinstance(artifact, dict) and isinstance(artifact.get("browser_page_context"), dict):
            event["browser_page_context"] = dict(artifact["browser_page_context"])
        if isinstance(artifact, dict) and isinstance(artifact.get("learning_experience"), dict):
            # Keep only the bounded, model-independent qualification projection;
            # proposal bodies remain referenced by evidence, never copied here.
            experience = artifact["learning_experience"]
            event["learning_experience"] = {
                key: experience[key] for key in (
                    "experience_id", "actor", "experience_kind", "verification_status",
                    "training_eligible", "evidence_refs", "verification_refs",
                ) if key in experience
            }
        experience_projection = canonical_experience_projection(event)
        if experience_projection is not None:
            event["experience"] = experience_projection
        with self._lock:
            events = self._events.setdefault(self._key(session_id, identity), deque(maxlen=self.max_turns * 4))
            events.append(event)
        # Reuse the existing append-only local chat history surface so a later
        # retrieval turn (or a process restart) can discover bounded artifacts.
        try:
            SESSION_MEMORY_ROOT.mkdir(parents=True, exist_ok=True)
            persisted_event = dict(event)
            persisted_event["persistence_status"] = "PERSISTED"
            if "experience" in persisted_event:
                persisted_event["experience"] = dict(persisted_event["experience"], persistence_status="PERSISTED")
            with _session_turn_log_path().open("a", encoding="utf-8") as handle:
                handle.write(json.dumps(persisted_event, ensure_ascii=False, sort_keys=True) + "\n")
                handle.flush()
                os.fsync(handle.fileno())
            event["persistence_status"] = "PERSISTED"
        except OSError:
            event["persistence_status"] = "NOT_PERSISTED"
        if "experience" in event:
            event["experience"]["persistence_status"] = event["persistence_status"]
        return dict(event)

    def exclude_persisted_records(self, *, record_sha256s: tuple[str, ...],
                                  classification: str, evidence_refs: tuple[str, ...]) -> dict[str, Any]:
        """Owner maintenance only; append evidence, never rewrite or erase raw turns.

        This is deliberately not a model capability or a public request parameter.
        Callers must supply exact already-persisted identities and retained evidence.
        Exclusion is monotonic; this method cannot promote data back to user memory.
        """
        hashes = tuple(dict.fromkeys(record_sha256s))
        if (classification not in {"TEST_FIXTURE", "NON_USER_DIAGNOSTIC"} or not hashes
            or not evidence_refs or any(not isinstance(ref, str) or not ref.strip() for ref in evidence_refs)):
            raise ValueError("session_exclusion_requires_classification_and_evidence")
        with self._lock, _EXCLUSION_LOCK:
            path = _session_turn_log_path()
            known: set[str] = set()
            with path.open(encoding="utf-8") as handle:
                for line in handle:
                    try:
                        record = json.loads(line)
                    except (ValueError, TypeError):
                        continue
                    if isinstance(record, dict) and record.get("source") == "jarvis_terminal_chat":
                        known.add(session_record_sha256(record))
            if any(h not in known for h in hashes):
                raise ValueError("session_exclusion_record_not_persisted")
            with path.open("rb") as raw:
                raw.seek(-1, os.SEEK_END)
                if raw.read(1) != b"\n":
                    raise ValueError("session_exclusion_incomplete_journal_tail")
            fresh = tuple(h for h in hashes if h not in _session_excluded_record_hashes())
            if not fresh:
                return {"status": "ALREADY_EXCLUDED", "record_sha256s": hashes, "written": False}
            event = {"schema_version": "canonical_session_record_exclusion.v1",
                     "source": _EXCLUSION_SOURCE, "record_sha256s": list(fresh),
                     "classification": classification, "evidence_refs": list(evidence_refs),
                     "persisted_at": _timestamp(), "persistence_status": "PERSISTED"}
            with path.open("a", encoding="utf-8") as handle:
                handle.write(json.dumps(event, ensure_ascii=False, sort_keys=True) + "\n")
                handle.flush()
                os.fsync(handle.fileno())
            return {"status": "EXCLUDED", "record_sha256s": fresh, "written": True,
                    "source": str(path), "raw_records_retained": True}

    def recent_artifact(self, session_id: str, identity: IdentityContext, *, kind: str) -> dict[str, Any] | None:
        self._restore_persisted_context(session_id, identity)
        key = self._key(session_id, identity)
        with self._lock:
            all_events = tuple(item for item in self._events.get(key, ())
                               if session_record_semantically_eligible(item))
        for item in reversed(all_events):
            artifact = item.get("artifact")
            if isinstance(artifact, dict) and artifact.get("kind") == kind:
                return dict(artifact)
        return None

STABLE_STYLE_PROFILE = {
    "user_name": "Александр",
    "assistant_identity": "JARVIS",
    "relation_style": "брат / напарник по гаражу",
    "communication_style": "natural, direct, practical, not overly short, not template-like",
    "avoid": "не повторять 'Нужна помощь?' после каждого ответа; не начинать отношения заново в новой сессии",
    "concise_rule": "быть коротким только когда владелец просит коротко; иначе отвечать достаточно полно для задачи",
}

DANGEROUS_MEMORY_FLAGS = {
    "direct_core_write_allowed": False,
    "runtime_mutation_allowed": False,
    "canonical_truth_update_allowed": False,
    "auto_apply_allowed": False,
    "deployment_allowed_now": False,
    "external_release_allowed_now": False,
    "memory_foundation_reopen_allowed": False,
    "regulatory_truth_update_allowed": False,
    "regulatory_auto_apply_allowed": False,
    "approval_bypass_allowed": False,
    "self_expansion_allowed_now": False,
    "pc_control_enabled": False,
    "phone_control_enabled": False,
    "direct_global_memory_write": False,
    "auto_project_truth_write": False,
}


def _query_tokens(text: str) -> tuple[str, ...]:
    return tuple(
        part
        for part in text.casefold().replace("?", " ").replace(",", " ").split()
        if len(part) >= 4
    )


def _append_assistant_and_summarize(
    state: dict[str, Any],
    response_text: str,
    context: JarvisBrainContext,
) -> None:
    _append_turn(state, "assistant", response_text)
    state["rolling_summary"] = _build_rolling_summary(state)
    state["active_topics"] = _extract_active_topics(context.user_text)
    _save_session_state(state)
    _append_local_chat_memory_record(state, response_text, context)


def _append_turn(state: dict[str, Any], role: str, text: str) -> None:
    if not text.strip():
        return
    turns = list(state.get("recent_turns", []))
    turns.append({"role": role, "text": text.strip(), "updated_at": str(time.time())})
    state["recent_turns"] = turns[-MAX_RECENT_TURNS:]
    # Descriptive restored session flags are not per-step HOST permissions.
    # Appending dialogue must not reset owner state; defaults apply only once.
    state.setdefault("local_session_persistence", True)
    state.setdefault("canonical_memory_write_allowed", False)
    state.setdefault("pc_control_allowed", False)


def _append_local_chat_memory_record(
    state: dict[str, Any],
    response_text: str,
    context: JarvisBrainContext,
) -> None:
    if not context.user_text.strip() and not response_text.strip():
        return
    record = {
        "timestamp": _timestamp(),
        "session_id": context.session_id,
        "day_bucket": _day_bucket(),
        "user_message": context.user_text.strip(),
        "jarvis_answer": response_text.strip(),
        "route": context.request_route,
        "mode": context.route_mode,
        "model_id": context.selected_model_role["model_id"],
        "selected_model_role": context.selected_model_role["selected_model_role"],
        "retrieval_mode": context.retrieval_mode,
        "retrieval_surfaces_used": context.retrieval_surfaces_used,
        "retrieved_snippet_count": len(context.retrieved_snippets),
        "local_chat_memory_snippet_count": len(context.local_chat_memory_snippets),
        "source": "jarvis_terminal_chat",
        "turn_summary": _brief_turn_summary(context.user_text, response_text),
        "active_task": _detect_active_task(context.user_text),
        "style_preference": _extract_style_preference(context.user_text),
        "thinking_stored": False,
        "canonical_memory_write_allowed": False,
        "direct_global_memory_write": False,
        "pc_control_allowed": False,
    }
    try:
        SESSION_MEMORY_ROOT.mkdir(parents=True, exist_ok=True)
        with _session_turn_log_path().open("a", encoding="utf-8") as handle:
            handle.write(json.dumps(record, ensure_ascii=False, sort_keys=True) + "\n")
    except OSError:
        return


def _session_turn_log_path() -> Path:
    return SESSION_MEMORY_ROOT / SESSION_TURN_LOG_NAME


def inspect_canonical_session_memory_health() -> dict[str, Any]:
    """Inspect the existing durable store without exporting conversation text."""
    path = _session_turn_log_path()
    health: dict[str, Any] = {"owner": "CanonicalSessionContextStore", "path": str(path),
        "observed_at": datetime.now(timezone.utc).isoformat(), "read_only": True,
        "status": "NOT_CONFIGURED", "record_count": 0, "canonical_turn_count": 0,
        "experience_count": 0, "receipt_record_count": 0, "retrieval_trace_count": 0,
        "semantic_excluded_turn_count": 0, "classification_record_count": 0,
        "invalid_record_count": 0, "incomplete_tail": False, "last_append_at": None,
        "separate_store": False,
        "count_semantics": {
            "record_count": "RAW_RETAINED_COMPLETE_VALID_JSON_OBJECTS_INCLUDING_EXCLUDED_TURNS_AND_CLASSIFICATION_RECORDS",
            "canonical_turn_count": "SEMANTICALLY_ELIGIBLE_CHAT_TURNS_NOT_VERIFIED_MEMORY_FACTS",
            "semantic_excluded_turn_count": "RETAINED_CHAT_TURNS_EXCLUDED_BY_CANONICAL_EVIDENCE",
            "classification_record_count": "APPEND_ONLY_CLASSIFICATION_EVIDENCE_NOT_USER_TURNS",
            "invalid_record_count": "MALFORMED_COMPLETE_LINES_NOT_INCLUDED_IN_RECORD_COUNT",
            "experience_count": "ELIGIBLE_EXPERIENCE_METADATA_NOT_AUTOMATIC_TRAINING_APPROVAL",
        }}
    try:
        if not path.is_file():
            return health
        size = path.stat().st_size
        health["snapshot_bytes"] = size
        if size > 64_000_000:
            return {**health, "status": "ENVIRONMENT_BLOCKED", "error": "health_scan_budget_exceeded"}
        with path.open("rb") as handle:
            snapshot = handle.read(size)
        classification_error = None
        try:
            excluded = _session_excluded_record_hashes()
        except (ValueError, UnicodeError) as exc:
            # Physical health remains inspectable even when no semantic read is
            # safe. Raw metadata counts must not become qualified memories.
            excluded = frozenset()
            classification_error = str(exc)
        for line in snapshot.splitlines(keepends=True):
            if not line.endswith(b"\n"):
                health["incomplete_tail"] = True
                continue
            try:
                record = json.loads(line)
                if not isinstance(record, dict):
                    raise ValueError("invalid record shape")
            except (ValueError, UnicodeDecodeError):
                health["invalid_record_count"] += 1
                continue
            health["record_count"] += 1  # Physical retention includes excluded raw records.
            if record.get("source") == _EXCLUSION_SOURCE:
                health["classification_record_count"] += 1
                continue
            if classification_error is None and session_record_sha256(record) in excluded:
                health["semantic_excluded_turn_count"] += record.get("source") == "jarvis_terminal_chat"
                continue
            if record.get("source") == "jarvis_terminal_chat":
                health["canonical_turn_count"] += 1
                stamp = _canonical_timestamp(record.get("persisted_at"))
                if stamp:
                    health["last_append_at"] = stamp
            artifact = record.get("artifact") or {}
            if not isinstance(artifact, dict):
                continue
            health["experience_count"] += isinstance(artifact.get("learning_experience"), dict)
            health["receipt_record_count"] += bool(artifact.get("execution_receipts"))
            health["retrieval_trace_count"] += isinstance(artifact.get("retrieval_trace"), dict)
        health["status"] = ("PARTIAL" if health["invalid_record_count"] or health["incomplete_tail"]
                            else "LIVE_READ_ONLY" if health["record_count"] else "NOT_CONFIGURED")
        if classification_error is not None:
            health.update(status="PARTIAL", semantic_eligibility_status="BLOCKED",
                          classification_error=classification_error,
                          canonical_turn_count=None, semantic_excluded_turn_count=None,
                          diagnostic_record_scope="RAW_VALID_OBJECT_METADATA_NOT_SEMANTICALLY_QUALIFIED",
                          last_append_scope="RAW_VALID_CHAT_RECORDS_NOT_ELIGIBLE_HISTORY")
            health["count_semantics"]["canonical_turn_count"] = "UNKNOWN_CLASSIFICATION_INTEGRITY_FAILED"
            health["count_semantics"]["semantic_excluded_turn_count"] = "UNKNOWN_CLASSIFICATION_INTEGRITY_FAILED"
            health["count_semantics"]["experience_count"] = "RAW_OBSERVED_EXPERIENCE_METADATA_NOT_ELIGIBLE_OR_TRAINING_APPROVED"
    except OSError as exc:
        health.update(status="ENVIRONMENT_BLOCKED", error=type(exc).__name__)
    return health


def _read_recent_local_chat_records(limit: int = 8, *, experience_only: bool = False) -> tuple[dict[str, Any], ...]:
    path = _session_turn_log_path()
    if not path.exists():
        return ()
    _session_excluded_record_hashes()
    try:
        lines = path.read_text(encoding="utf-8", errors="replace").splitlines()
    except FileNotFoundError:
        return ()
    except OSError as exc:
        raise ValueError("canonical_session_reader_unreadable_journal") from exc
    records: list[dict[str, Any]] = []
    scan_limit = 4096 if experience_only else max(limit * 3, limit)
    scanned_eligible = 0
    for line in reversed(lines):
        try:
            payload = json.loads(line)
        except json.JSONDecodeError:
            continue
        if isinstance(payload, dict) and payload.get("source") == "jarvis_terminal_chat":
            if not session_record_semantically_eligible(payload):
                continue
            scanned_eligible += 1
            if scanned_eligible > scan_limit:
                break
            if experience_only and canonical_experience_projection(payload) is None:
                continue
            records.insert(0, payload)
        if len(records) >= limit:
            break
    return tuple(records[-limit:])


def _load_session_state() -> dict[str, Any]:
    if not SESSION_STATE_PATH.exists():
        return _empty_session_state()
    try:
        payload = json.loads(SESSION_STATE_PATH.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError):
        return _empty_session_state()
    if not isinstance(payload, dict):
        return _empty_session_state()
    return _normalize_session_state(payload)


def _save_session_state(state: dict[str, Any]) -> None:
    # This compatibility cache is not a policy owner. Loading/saving it must
    # not reset persisted owner settings or promote them into host permissions.
    payload = _normalize_session_state(state)
    payload["session_memory_path"] = str(SESSION_STATE_PATH)
    payload["local_chat_memory_path"] = str(_session_turn_log_path())
    from MAKSIMAR_CORE_LIB.shared_services.atomic_io import atomic_write_json, AtomicIOError
    try:
        SESSION_MEMORY_ROOT.mkdir(parents=True, exist_ok=True)
        atomic_write_json(SESSION_STATE_PATH, payload)
    except (OSError, AtomicIOError):
        return


def _empty_session_state() -> dict[str, Any]:
    return _normalize_session_state({
        "recent_turns": [],
        "rolling_summary": "",
        "active_topics": [],
        "pending_memory_write_proposal": False,
        "pending_memory_write_payload": {},
        "memory_write_completed": False,
        "local_session_persistence": True,
        "canonical_memory_write_allowed": False,
        "pc_control_allowed": False,
    })


def _normalize_session_state(state: dict[str, Any]) -> dict[str, Any]:
    normalized = dict(state)
    normalized.setdefault("recent_turns", [])
    normalized.setdefault("rolling_summary", "")
    normalized.setdefault("active_topics", [])
    normalized.setdefault("style_preferences", {})
    normalized.setdefault("pending_memory_write_proposal", False)
    normalized.setdefault("pending_memory_write_payload", {})
    normalized.setdefault("memory_write_completed", False)
    normalized["stable_style_profile"] = _stable_style_profile_from_state(normalized)
    normalized.setdefault("local_session_persistence", True)
    normalized.setdefault("canonical_memory_write_allowed", False)
    normalized.setdefault("pc_control_allowed", False)
    normalized.setdefault("dangerous_mutation_flags", dict(DANGEROUS_MEMORY_FLAGS))
    normalized.setdefault("memory_truth_contract", _memory_truth_contract())
    for key, default in _memory_enablement_flags().items():
        normalized.setdefault(key, default)
    normalized["settings_authority"] = "descriptive_session_cache; authorization belongs to host policy"
    return normalized


def _stable_style_profile_from_state(state: dict[str, Any]) -> dict[str, str]:
    profile = dict(STABLE_STYLE_PROFILE)
    preferences = state.get("style_preferences")
    if isinstance(preferences, dict):
        for key, value in preferences.items():
            if isinstance(key, str) and isinstance(value, str) and value.strip():
                profile[key] = value.strip()[:300]
    return profile


def _update_style_preferences(state: dict[str, Any], user_text: str) -> None:
    preference = _extract_style_preference(user_text)
    if not preference:
        return
    preferences = state.get("style_preferences")
    if not isinstance(preferences, dict):
        preferences = {}
    preferences["explicit_owner_style_preference"] = preference
    state["style_preferences"] = preferences


def _extract_style_preference(text: str) -> str:
    del text
    return ""


def _memory_enablement_flags() -> dict[str, bool]:
    return {
        "memory_enabled": True,
        "project_memory_enabled": True,
        "project_memory_read_enabled": True,
        "conversation_memory_enabled": True,
        "chat_memory_enabled": True,
        "session_memory_enabled": True,
        "runtime_history_enabled": True,
        "runtime_history_read_enabled": True,
        "rag_enabled": True,
        "retrieval_enabled": True,
        "memory_retrieval_enabled": True,
        "project_history_retrieval_enabled": True,
        "history_retrieval_enabled": True,
        "runtime_history_store_enabled": True,
        "jarvis_history_read_enabled": True,
        "jarvis_history_query_enabled": True,
        "roadmap_context_enabled": True,
        "roadmap_next_step_enabled": True,
        "memory_skill_context_enabled": True,
        "memory_summary_context_enabled": True,
        "project_workspace_read_enabled": True,
        "project_tree_read_enabled": True,
        "project_file_read_enabled": True,
        "project_source_snippet_read_enabled": True,
        "project_structure_context_enabled": True,
        "regulatory_memory_read_enabled": True,
        "regulatory_summary_enabled": True,
        "audit_read_model_enabled": True,
        "approval_context_read_enabled": True,
        "source_trace_context_enabled": True,
        "evidence_pack_context_enabled": True,
        "recent_turn_context_enabled": True,
        "rolling_summary_enabled": True,
        "local_session_persistence_enabled": True,
        "context_assembly_enabled": True,
        "retrieval_before_project_answer": True,
        "hallucination_guard_enabled": True,
        "memory_truth_contract_enabled": True,
        "session_memory_write_enabled": True,
        "runtime_history_append_enabled": False,
        "conversation_history_append_enabled": True,
        "chat_transcript_append_enabled": True,
        "chat_memory_write_enabled": True,
    }


def _memory_truth_contract() -> dict[str, str]:
    return {
        "canonical_truth": "read_only_not_written_by_live_chat",
        "project_history": "read_only_imported_history_context",
        "project_workspace": "read_only_tree_and_bounded_file_snippets",
        "local_chat_memory": "append_only_terminal_chat_memory",
        "session_summary": "local_session_context",
        "user_preference": "local_style_preference",
        "uncertain_memory": "must_be_reported_as_uncertain",
    }


def _timestamp() -> str:
    return time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime())


def _day_bucket() -> str:
    return time.strftime("%Y-%m-%d", time.localtime())


def _brief_turn_summary(user_text: str, response_text: str) -> str:
    return f"user={user_text.strip()[:160]} | jarvis={response_text.strip()[:160]}"


def _detect_active_task(text: str) -> str:
    del text
    return ""


def _build_rolling_summary(state: dict[str, Any]) -> str:
    turns = list(state.get("recent_turns", []))[-4:]
    joined = " | ".join(f"{turn.get('role')}: {turn.get('text')}" for turn in turns)
    return joined[:900]


def _extract_active_topics(text: str) -> list[str]:
    del text
    return []


def _format_turns(turns: tuple[dict[str, str], ...]) -> str:
    if not turns:
        return ""
    lines = [f"- {turn.get('role')}: {turn.get('text')}" for turn in turns]
    return "RECENT_SESSION_TURNS:\n" + "\n".join(lines)


def _format_style_profile(profile: dict[str, str]) -> str:
    if not profile:
        return ""
    lines = [f"- {key}: {value}" for key, value in profile.items()]
    return "STABLE_STYLE_PROFILE:\n" + "\n".join(lines)
