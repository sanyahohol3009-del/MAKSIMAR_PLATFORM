"""Governed developer-experience learning input.

This is a typed qualification boundary over existing evidence.  It is not a
second history store and it never mutates model weights or canonical memory.
"""
from __future__ import annotations

import hashlib
import json
import re
from dataclasses import dataclass
from typing import Any, Literal


Actor = Literal["CODEX", "DEEPSEEK", "JARVIS", "HUMAN"]
ExperienceKind = Literal[
    "DEVELOPMENT", "DEBUGGING", "REPAIR", "ARCHITECTURE_DESIGN",
    "OPTIMIZATION", "MIGRATION", "INTEGRATION", "SECURITY_REVIEW",
    "PERFORMANCE_TUNING", "TEST_DESIGN", "FAILED_EXPERIMENT",
]
VerificationStatus = Literal["VERIFIED", "PARTIAL", "REJECTED", "PENDING"]

_SECRET = re.compile(
    r"(?i)(?:api[_-]?key|token|password|passwd|cookie|authorization|secret)\s*[:=]\s*[^\s,;]+"
)


def redact_text(value: str) -> str:
    if not isinstance(value, str):
        raise TypeError("value must be a string")
    return _SECRET.sub(lambda m: m.group(0).split(":")[0].split("=")[0] + "=<redacted>", value)


@dataclass(frozen=True, slots=True)
class DeveloperExperienceRecord:
    experience_id: str
    actor: Actor
    task_ref: str
    evidence_refs: tuple[str, ...]
    failure_class: str | None
    repair_verified: bool
    outcome: Literal["verified", "rejected", "pending"]
    provenance_ref: str
    pii_redacted: bool = True
    experience_kind: ExperienceKind = "DEVELOPMENT"
    verification_status: VerificationStatus = "PENDING"
    verification_refs: tuple[str, ...] = ()
    training_export_allowed: bool = False
    training_candidate_creation_allowed: bool = False
    active_model_runtime_mutation_allowed: bool = False
    active_model_auto_promotion_allowed: bool = False

    def __post_init__(self) -> None:
        for name in ("experience_id", "task_ref", "provenance_ref"):
            value = getattr(self, name)
            if not isinstance(value, str) or not value.strip():
                raise ValueError(f"{name} must be non-empty")
        if self.actor not in {"CODEX", "DEEPSEEK", "JARVIS", "HUMAN"}:
            raise ValueError("unsupported actor")
        if not self.evidence_refs:
            raise ValueError("evidence_refs must be non-empty")
        if any(not isinstance(ref, str) or not ref.strip() for ref in self.evidence_refs):
            raise ValueError("evidence_refs must contain non-empty strings")
        if self.experience_kind not in {
            "DEVELOPMENT", "DEBUGGING", "REPAIR", "ARCHITECTURE_DESIGN",
            "OPTIMIZATION", "MIGRATION", "INTEGRATION", "SECURITY_REVIEW",
            "PERFORMANCE_TUNING", "TEST_DESIGN", "FAILED_EXPERIMENT",
        }:
            raise ValueError("unsupported experience_kind")
        if self.verification_status not in {"VERIFIED", "PARTIAL", "REJECTED", "PENDING"}:
            raise ValueError("unsupported verification_status")
        if self.experience_kind == "REPAIR" and self.verification_status == "VERIFIED" and not self.repair_verified:
            raise ValueError("verified repairs require repair_verified=True")
        if self.verification_status == "VERIFIED" and not self.verification_refs:
            raise ValueError("verified experience requires verification_refs")
        if self.pii_redacted is not True:
            raise ValueError("pii_redacted must be True")
        if self.active_model_runtime_mutation_allowed or self.active_model_auto_promotion_allowed:
            raise ValueError("active model mutation and auto-promotion are forbidden")

    @property
    def training_eligible(self) -> bool:
        return self.verification_status == "VERIFIED" and bool(self.evidence_refs) and bool(self.verification_refs)

    def to_read_model(self) -> dict[str, Any]:
        return {
            "experience_id": self.experience_id,
            "actor": self.actor,
            "task_ref": self.task_ref,
            "evidence_refs": self.evidence_refs,
            "failure_class": self.failure_class,
            "repair_verified": self.repair_verified,
            "outcome": self.outcome,
            "provenance_ref": self.provenance_ref,
            "pii_redacted": self.pii_redacted,
            "training_eligible": self.training_eligible,
            "experience_kind": self.experience_kind,
            "verification_status": self.verification_status,
            "verification_refs": self.verification_refs,
            "training_export_allowed": self.training_export_allowed and self.training_eligible,
            "training_candidate_creation_allowed": self.training_candidate_creation_allowed and self.training_eligible,
            "active_model_runtime_mutation_allowed": False,
            "active_model_auto_promotion_allowed": False,
        }


def build_developer_experience_record(
    *,
    actor: Actor,
    task_ref: str,
    evidence_refs: tuple[str, ...],
    failure_class: str | None,
    repair_verified: bool,
    outcome: Literal["verified", "rejected", "pending"],
    provenance_ref: str,
    experience_kind: ExperienceKind = "DEVELOPMENT",
    verification_status: VerificationStatus | None = None,
    verification_refs: tuple[str, ...] = (),
    training_export_allowed: bool = False,
    training_candidate_creation_allowed: bool = False,
) -> DeveloperExperienceRecord:
    """Build a bounded record referencing existing evidence only."""
    if any(_SECRET.search(ref) for ref in evidence_refs):
        raise ValueError("evidence references must not contain secret material")
    canonical = json.dumps(
        {"actor": actor, "task_ref": redact_text(task_ref), "evidence_refs": evidence_refs,
         "failure_class": failure_class, "repair_verified": repair_verified,
         "outcome": outcome, "provenance_ref": provenance_ref},
        sort_keys=True, separators=(",", ":"), ensure_ascii=False,
    ).encode("utf-8")
    experience_id = "devexp_" + hashlib.sha256(canonical).hexdigest()[:24]
    resolved_status: VerificationStatus = verification_status or {
        "verified": "VERIFIED", "rejected": "REJECTED", "pending": "PENDING",
    }[outcome]
    return DeveloperExperienceRecord(
        experience_id=experience_id, actor=actor, task_ref=redact_text(task_ref),
        evidence_refs=evidence_refs, failure_class=failure_class,
        repair_verified=repair_verified, outcome=outcome,
        provenance_ref=provenance_ref,
        experience_kind=experience_kind,
        verification_status=resolved_status,
        verification_refs=verification_refs,
        training_export_allowed=training_export_allowed,
        training_candidate_creation_allowed=training_candidate_creation_allowed,
    )


def qualify_provider_execution_experience(*, task_ref: str, trace_id: str,
        operation_status: str, evidence: dict[str, Any]) -> DeveloperExperienceRecord | None:
    """Capture host receipt/readback verification, without asserting peer review or training."""
    if operation_status != "COMPLETE" or evidence.get("status") != "COMPLETE" or not trace_id:
        return None
    kinds = {"browser_page_opened", "browser_navigation", "n8n_execution", "n8n_workflow",
             "project_workbench_opened", "file_snippet", "file_outline", "git_worktree_status",
             "windows_screen_capture", "media_probe", "mempalace_search", "mempalace_index_refresh"}
    items = [item for item in evidence.get("items", ()) if isinstance(item, dict) and item.get("kind") in kinds]
    if not items:
        return None
    refs = []
    verification_refs = []
    keys = ("request_id", "trace_id", "step_id", "capability_id", "operation_id", "provider_id")
    for item in items:
        digest = "sha256:" + hashlib.sha256(str(item.get("observation", "")).encode()).hexdigest()
        if (item.get("content_hash") != digest or item.get("trace_id") != trace_id
                or not item.get("observed_at") or not all(item.get(key) for key in keys)):
            return None
        receipt = next((r for r in evidence.get("receipts", ()) if isinstance(r, dict)
                        and r.get("status") == "COMPLETE" and r.get("receipt_id")
                        and all(r.get(key) == item.get(key) for key in keys)), None)
        if receipt is None:
            return None
        refs.append("evidence://" + trace_id + "/" + str(item["step_id"]) + "/" + digest)
        verification_refs.append("receipt://" + str(receipt["receipt_id"]))
    return build_developer_experience_record(actor="JARVIS", task_ref=task_ref,
        evidence_refs=tuple(refs), failure_class=None, repair_verified=False,
        outcome="verified", provenance_ref="trace://" + trace_id,
        experience_kind="INTEGRATION", verification_status="VERIFIED",
        verification_refs=tuple(dict.fromkeys(verification_refs)),
        training_export_allowed=False, training_candidate_creation_allowed=False)


def capture_proposal_experience(
    *, actor: Actor, task_ref: str, proposal_ref: str,
    audit_ref: str, verification_ref: str, experience_kind: ExperienceKind,
    verified: bool, audit_verdict: str | None = None,
) -> DeveloperExperienceRecord:
    """Qualify one proposal using references to existing evidence only."""
    revision_required = not verified and audit_verdict == "REVISE"
    execution_pending = not verified and audit_verdict == "ACCEPTED_FOR_EXPERIMENT"
    status: VerificationStatus = ("VERIFIED" if verified else "PENDING" if execution_pending
        else "PARTIAL" if revision_required else "REJECTED")
    outcome: Literal["verified", "rejected", "pending"] = ("verified" if verified
        else "pending" if revision_required or execution_pending else "rejected")
    return build_developer_experience_record(
        actor=actor,
        task_ref=task_ref,
        evidence_refs=(proposal_ref, audit_ref),
        failure_class=None if verified or execution_pending else "proposal_audit_revision_required" if revision_required else "proposal_audit_rejected",
        repair_verified=False,
        outcome=outcome,
        provenance_ref=verification_ref,
        experience_kind=experience_kind,
        verification_status=status,
        verification_refs=(verification_ref,) if verified else (),
        training_export_allowed=verified,
    )


def qualify_verified_sandbox_experience(
    *, actor: Actor, task_ref: str, evidence_refs: tuple[str, ...],
    provenance_ref: str, review_ref: str, execution_status: str,
    review_status: str,
) -> DeveloperExperienceRecord | None:
    """Qualify one reviewed sandbox execution using existing experience policy.

    This keeps execution/review eligibility semantics in the DeveloperExperience
    owner; callers only adapt already-produced typed evidence into this contract.
    """
    if execution_status != "COMPLETE" or review_status != "REVIEWED":
        return None
    return build_developer_experience_record(
        actor=actor, task_ref=task_ref, evidence_refs=evidence_refs,
        failure_class=None, repair_verified=False, outcome="verified",
        provenance_ref=provenance_ref, experience_kind="TEST_DESIGN",
        verification_status="VERIFIED", verification_refs=(review_ref,),
        training_export_allowed=False,
    )
