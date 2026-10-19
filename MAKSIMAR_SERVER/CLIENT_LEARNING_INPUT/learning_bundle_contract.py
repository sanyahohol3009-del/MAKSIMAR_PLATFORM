"""Portable learning envelope owned by CLIENT_LEARNING_INPUT."""
from __future__ import annotations

import hashlib
import json
from dataclasses import dataclass
from typing import Any, Literal
from MAKSIMAR_CORE_LIB.ai_orchestration.semantic_intent_contract import utc_observed_at


ArtifactType = Literal[
    "developer_experience", "semantic_curriculum", "semantic_head",
    "skill_procedure", "demonstration", "control_policy", "model_adapter",
]


@dataclass(frozen=True, slots=True)
class LearningBundle:
    schema_version: str
    bundle_id: str
    source_node: str
    source_body: str
    source_actor: str
    created_at: str
    capability_id: str
    organ_id: str
    artifact_type: ArtifactType
    artifact_ref: str
    model_fingerprint: str | None = None
    embedding_fingerprint: str | None = None
    body_fingerprint: str | None = None
    metrics: tuple[tuple[str, str], ...] = ()
    constraints: tuple[str, ...] = ()
    evidence_refs: tuple[str, ...] = ()
    evaluation_refs: tuple[str, ...] = ()
    provenance: tuple[str, ...] = ()
    compatibility: str = "REQUIRES_ADAPTATION"

    def __post_init__(self) -> None:
        for name in ("schema_version", "bundle_id", "source_node", "source_body", "source_actor", "created_at", "artifact_ref"):
            if not isinstance(getattr(self, name), str) or not getattr(self, name).strip():
                raise ValueError(f"{name} must be non-empty")
        if self.schema_version != "learning_bundle.v1":
            raise ValueError("unsupported learning bundle schema")
        if self.artifact_type not in {"developer_experience", "semantic_curriculum", "semantic_head", "skill_procedure", "demonstration", "control_policy", "model_adapter"}:
            raise ValueError("unsupported artifact_type")
        if any(token in self.artifact_ref.casefold() for token in ("secret", "token", "password", "credential")):
            raise ValueError("artifact_ref must not expose credentials")
        if not self.evidence_refs:
            raise ValueError("evidence_refs must be non-empty")
        if self.compatibility not in {"SEMANTIC_TRANSFER_ALLOWED", "DIRECT_WEIGHT_TRANSFER_ALLOWED", "DIRECT_POLICY_TRANSFER_ALLOWED", "REQUIRES_ADAPTATION", "REJECTED"}:
            raise ValueError("unsupported compatibility decision")

    def to_dict(self) -> dict[str, Any]:
        return {"schema_version": self.schema_version, "bundle_id": self.bundle_id,
                "source_node": self.source_node, "source_body": self.source_body,
                "source_actor": self.source_actor, "created_at": self.created_at,
                "capability_id": self.capability_id, "organ_id": self.organ_id,
                "artifact_type": self.artifact_type, "artifact_ref": self.artifact_ref,
                "model_fingerprint": self.model_fingerprint, "embedding_fingerprint": self.embedding_fingerprint,
                "body_fingerprint": self.body_fingerprint, "metrics": dict(self.metrics),
                "constraints": self.constraints, "evidence_refs": self.evidence_refs,
                "evaluation_refs": self.evaluation_refs, "provenance": self.provenance,
                "compatibility": self.compatibility}

    def serialize(self) -> str:
        return json.dumps(self.to_dict(), ensure_ascii=False, sort_keys=True, separators=(",", ":"))

    @property
    def content_hash(self) -> str:
        return "sha256:" + hashlib.sha256(self.serialize().encode("utf-8")).hexdigest()


def build_experience_learning_bundle(*, experience_id: str, actor: str, audit_verdict: str,
                                     evidence_refs: tuple[str, ...], verification_refs: tuple[str, ...],
                                     created_at: str | None = None,
                                     capability_id: str = "code.proposal.generate",
                                     organ_id: str = "self_evolution",
                                     artifact_type: ArtifactType = "developer_experience") -> LearningBundle:
    return LearningBundle(
        schema_version="learning_bundle.v1", bundle_id="bundle_" + experience_id,
        source_node="jarvis_main", source_body="software_runtime", source_actor=actor,
        created_at=created_at or utc_observed_at(), capability_id=capability_id,
        organ_id=organ_id, artifact_type=artifact_type,
        artifact_ref="experience://" + experience_id, evidence_refs=evidence_refs,
        evaluation_refs=verification_refs, provenance=("audit_verdict=" + audit_verdict,),
        constraints=("non_canonical_experience", "no_model_mutation", "no_hardware_execution"),
        compatibility="SEMANTIC_TRANSFER_ALLOWED",
    )


def build_sandbox_learning_bundle(*, artifact_ref: str, sandbox_id: str,
                                  source_actor: str, evidence_refs: tuple[str, ...],
                                  evaluation_refs: tuple[str, ...],
                                  metrics: tuple[tuple[str, str], ...] = (),
                                  failed: bool = False, created_at: str | None = None) -> LearningBundle:
    """Create a portable sandbox result envelope; qualification remains upstream."""
    if sandbox_id != "simulation":
        raise ValueError("simulation LearningBundle builder requires sandbox_id=simulation")
    return LearningBundle(
        schema_version="learning_bundle.v1", bundle_id="bundle_sandbox_" + hashlib.sha256(artifact_ref.encode()).hexdigest()[:16],
        source_node="jarvis_main", source_body="software_runtime", source_actor=source_actor,
        created_at=created_at or utc_observed_at(), capability_id="simulation.run", organ_id="evolution_debug",
        artifact_type="demonstration", artifact_ref=artifact_ref, metrics=metrics,
        constraints=("sandbox_only", "artifact_only", "failed_experiment" if failed else "executed_experiment"),
        evidence_refs=evidence_refs, evaluation_refs=evaluation_refs,
        provenance=("sandbox_id=" + sandbox_id, "result_status=" + ("FAILED" if failed else "COMPLETED")),
        compatibility="SEMANTIC_TRANSFER_ALLOWED",
    )


def decide_compatibility(*, artifact_type: ArtifactType, source_fingerprint: str | None,
                         target_fingerprint: str | None, source_body: str | None = None,
                         target_body: str | None = None) -> dict[str, str]:
    if artifact_type == "model_adapter":
        direct = source_fingerprint is not None and source_fingerprint == target_fingerprint
        return {"semantic_transfer": "SEMANTIC_TRANSFER_ALLOWED", "direct_weight_transfer": "DIRECT_WEIGHT_TRANSFER_ALLOWED" if direct else "REJECTED"}
    if artifact_type == "control_policy":
        direct = source_body is not None and source_body == target_body and source_fingerprint == target_fingerprint
        return {"semantic_transfer": "SEMANTIC_TRANSFER_ALLOWED", "direct_policy_transfer": "DIRECT_POLICY_TRANSFER_ALLOWED" if direct else "REJECTED"}
    return {"semantic_transfer": "SEMANTIC_TRANSFER_ALLOWED", "direct_weight_transfer": "REQUIRES_ADAPTATION"}


def validate_learning_bundle_intake(bundle: LearningBundle, experience: Any) -> dict[str, Any]:
    """Validate local intake against the canonical experience record.

    This is a qualification/projection boundary only; it does not persist,
    promote, mutate weights, or grant execution authority.
    """
    experience_id = str(getattr(experience, "experience_id", ""))
    actor = str(getattr(experience, "actor", ""))
    evidence_refs = tuple(getattr(experience, "evidence_refs", ()))
    if bundle.artifact_ref != "experience://" + experience_id:
        raise ValueError("bundle artifact_ref does not resolve to experience")
    if bundle.source_actor != actor or bundle.source_actor != str(bundle.source_actor).strip():
        raise ValueError("bundle actor mismatch")
    if not set(evidence_refs).issubset(set(bundle.evidence_refs)):
        raise ValueError("bundle evidence refs incomplete")
    return {
        "accepted": True,
        "experience_id": experience_id,
        "actor": actor,
        "verification_status": str(getattr(experience, "verification_status", "PENDING")),
        "audit_verdict": next((item.split("=", 1)[1] for item in bundle.provenance if item.startswith("audit_verdict=")), "UNKNOWN"),
        "training_eligible": bool(getattr(experience, "training_eligible", False)),
        "bundle_id": bundle.bundle_id,
        "bundle_hash": bundle.content_hash,
        "authority": "qualification_only",
    }
