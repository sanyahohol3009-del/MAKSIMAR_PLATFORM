from __future__ import annotations

from dataclasses import dataclass
from abc import ABC, abstractmethod
from datetime import UTC, datetime
from contextlib import contextmanager
from contextvars import ContextVar
import threading
import math
import time
from typing import Any


_ALLOWED_PROFILE_TYPES = {"owner", "trusted_family", "child", "unknown"}
_ALLOWED_RISK_CLASSES = {"read_only", "safe_direct", "risk_gate"}
_ALLOWED_EFFECT_TYPES = {"OBSERVE", "MUTATE", "EXECUTE", "EXPORT", "PERSIST", "UNKNOWN"}
_ALLOWED_REVERSIBILITY = {"REVERSIBLE", "PARTIALLY_REVERSIBLE", "IRREVERSIBLE", "UNKNOWN"}
_ALLOWED_EXECUTION_RESTRICTIONS = {"NONE", "NO_EXECUTE", "PREPARE_ONLY"}



# Public semantic verdict fields belong to the existing intent contract. This is
# a bounded model judgment, never an execution permission or evidence receipt.
SOURCE_CANDIDATE_VERDICT_SCHEMA: dict[str, Any] = {
    "type": "object", "additionalProperties": False,
    "required": ["status", "supported", "missing", "contradictions", "unsupported_claims", "reason"],
    "properties": {
        "status": {"type": "string", "enum": ["COMPLETE", "INCOMPLETE", "INVALID", "UNPROVEN"]},
        **{key: {"type": "array", "uniqueItems": True,
                 "items": {"type": "string", "minLength": 1}}
           for key in ("supported", "missing", "contradictions", "unsupported_claims")},
        "reason": {"type": "string", "minLength": 1},
    },
}


def validate_source_candidate_verdict(verdict: Any, candidate_ids: tuple[str, ...]) -> str:
    """Check verdict consistency; the verifier, not these IDs, judges source coverage.

    Candidate IDs are references ONLY. They cannot define the source's requested
    semantic set. Missing source facets must be assessed independently by the model.
    Malformed/inconsistent judgments are UNPROVEN, never permissive UNKNOWN.
    """
    if not isinstance(verdict, dict) or set(verdict) != set(SOURCE_CANDIDATE_VERDICT_SCHEMA["required"]):
        return "UNPROVEN"
    if not isinstance(verdict["reason"], str) or not verdict["reason"].strip():
        return "UNPROVEN"
    for key in ("supported", "missing", "contradictions", "unsupported_claims"):
        rows = verdict[key]
        if (not isinstance(rows, list) or any(not isinstance(v, str) or not v.strip() for v in rows)
                or len(set(rows)) != len(rows)):
            return "UNPROVEN"
    if len(set(candidate_ids)) != len(candidate_ids) or not set(verdict["supported"]) <= set(candidate_ids):
        return "UNPROVEN"
    status = verdict["status"]
    if status == "COMPLETE":
        if (verdict["missing"] or verdict["contradictions"] or verdict["unsupported_claims"]
                or set(verdict["supported"]) != set(candidate_ids) or not candidate_ids):
            return "UNPROVEN"
    elif status == "INCOMPLETE":
        if not verdict["missing"] or verdict["contradictions"] or verdict["unsupported_claims"]:
            return "UNPROVEN"
    elif status == "INVALID":
        if not (verdict["contradictions"] or verdict["unsupported_claims"]):
            return "UNPROVEN"
    elif status != "UNPROVEN":
        return "UNPROVEN"
    return status


def _require_non_empty(value: str, field_name: str) -> str:
    if not isinstance(value, str) or not value.strip():
        raise ValueError(f"{field_name} must be a non-empty string")
    return value.strip()


def _require_choice(value: str, field_name: str, allowed: set[str]) -> str:
    normalized = _require_non_empty(value, field_name)
    if normalized not in allowed:
        raise ValueError(f"{field_name} must be one of {tuple(sorted(allowed))!r}")
    return normalized


def _normalize_string_tuple(values: tuple[str, ...], field_name: str) -> tuple[str, ...]:
    if not isinstance(values, tuple):
        raise ValueError(f"{field_name} must be a tuple")
    normalized: list[str] = []
    for value in values:
        normalized.append(_require_non_empty(value, field_name))
    return tuple(normalized)


def _validate_operation_reference_order(items: tuple[Any, ...], operation_field: str) -> None:
    """Validate existing linear operation order; do not plan/reorder or invent edges."""
    for index, item in enumerate(items):
        for target in item.declared_prerequisite_for_operation_ids:
            positions = tuple(i for i, candidate in enumerate(items) if getattr(candidate, operation_field) == target)
            if len(positions) > 1 or any(position <= index for position in positions):
                raise ValueError("operation_dependency_order_or_identity_invalid")


def _normalize_confidence(value: float) -> float:
    try:
        confidence = float(value)
    except (TypeError, ValueError) as exc:
        raise ValueError("confidence must be numeric") from exc
    if confidence < 0.0 or confidence > 1.0:
        raise ValueError("confidence must be between 0.0 and 1.0")
    return confidence


@dataclass(frozen=True, slots=True)
class JarvisSemanticIntent:
    speaker_profile_id: str
    speaker_profile_type: str
    semantic_intent: str
    scope: str
    risk_class: str
    evidence_required: bool
    selected_tools: tuple[str, ...]
    selected_skills: tuple[str, ...]
    selected_agents: tuple[str, ...]
    selected_model_role: str
    final_brain_required: bool
    approval_required: bool
    confidence: float
    reason_codes: tuple[str, ...]

    def __post_init__(self) -> None:
        object.__setattr__(self, "speaker_profile_id", _require_non_empty(self.speaker_profile_id, "speaker_profile_id"))
        object.__setattr__(
            self,
            "speaker_profile_type",
            _require_choice(self.speaker_profile_type, "speaker_profile_type", _ALLOWED_PROFILE_TYPES),
        )
        object.__setattr__(self, "semantic_intent", _require_non_empty(self.semantic_intent, "semantic_intent"))
        object.__setattr__(self, "scope", _require_non_empty(self.scope, "scope"))
        object.__setattr__(self, "risk_class", _require_choice(self.risk_class, "risk_class", _ALLOWED_RISK_CLASSES))
        object.__setattr__(self, "selected_tools", _normalize_string_tuple(self.selected_tools, "selected_tools"))
        object.__setattr__(self, "selected_skills", _normalize_string_tuple(self.selected_skills, "selected_skills"))
        object.__setattr__(self, "selected_agents", _normalize_string_tuple(self.selected_agents, "selected_agents"))
        object.__setattr__(self, "selected_model_role", _require_non_empty(self.selected_model_role, "selected_model_role"))
        object.__setattr__(self, "confidence", _normalize_confidence(self.confidence))
        object.__setattr__(self, "reason_codes", _normalize_string_tuple(self.reason_codes, "reason_codes"))
        if not self.reason_codes:
            raise ValueError("reason_codes must not be empty")
        if self.risk_class == "risk_gate" and self.approval_required is not True:
            raise ValueError("risk_gate semantic intents must require approval")
        if self.final_brain_required is not True and self.semantic_intent not in {
            "safe_pc_open_browser",
            "safe_pc_open_app",
            "weather_lookup",
            "calendar_lookup",
            "mail_lookup",
        }:
            raise ValueError("final_brain_required may be false only for deterministic/safe direct intents")

    def to_read_model(self) -> dict[str, Any]:
        return {
            "speaker_profile_id": self.speaker_profile_id,
            "speaker_profile_type": self.speaker_profile_type,
            "semantic_intent": self.semantic_intent,
            "scope": self.scope,
            "risk_class": self.risk_class,
            "evidence_required": self.evidence_required,
            "selected_tools": self.selected_tools,
            "selected_skills": self.selected_skills,
            "selected_agents": self.selected_agents,
            "selected_model_role": self.selected_model_role,
            "final_brain_required": self.final_brain_required,
            "approval_required": self.approval_required,
            "confidence": self.confidence,
            "reason_codes": self.reason_codes,
        }


@dataclass(frozen=True, slots=True)
class Goal:
    goal_id: str
    description: str
    schema_version: str = "goal.v1"

    def __post_init__(self) -> None:
        if self.schema_version != "goal.v1":
            raise ValueError("schema_version must be goal.v1")
        object.__setattr__(self, "goal_id", _require_non_empty(self.goal_id, "goal_id"))
        object.__setattr__(self, "description", _require_non_empty(self.description, "description"))

    def to_read_model(self) -> dict[str, Any]:
        return {"schema_version": self.schema_version, "goal_id": self.goal_id, "description": self.description}


@dataclass(frozen=True, slots=True)
class CapabilityRequirement:
    capability_id: str
    purpose: str
    required: bool
    operation_contract_required: bool = True
    unresolved_operation_reason: str = ""
    schema_version: str = "capability_requirement.v1"

    def __post_init__(self) -> None:
        if self.schema_version != "capability_requirement.v1":
            raise ValueError("schema_version must be capability_requirement.v1")
        object.__setattr__(self, "capability_id", _require_non_empty(self.capability_id, "capability_id"))
        object.__setattr__(self, "purpose", _require_non_empty(self.purpose, "purpose"))
        if not isinstance(self.required, bool):
            raise ValueError("required must be bool")
        if not isinstance(self.operation_contract_required, bool):
            raise ValueError("operation_contract_required must be bool")
        if not isinstance(self.unresolved_operation_reason, str):
            raise ValueError("unresolved_operation_reason must be a string")

    def to_read_model(self) -> dict[str, Any]:
        return {
            "schema_version": self.schema_version,
            "capability_id": self.capability_id,
            "purpose": self.purpose,
            "required": self.required,
            "operation_contract_required": self.operation_contract_required,
            "unresolved_operation_reason": self.unresolved_operation_reason,
        }


def validate_response_requirement_goal_references(
    response_requirements: tuple[ResponseRequirement, ...], goal_ids: set[str],
) -> None:
    """Shared existing response/goal association validation, before or after binding."""
    for response_requirement in response_requirements:
        unknown = set(response_requirement.applies_to_goal_ids) - goal_ids
        if response_requirement.subject_binding is not None:
            unknown |= {dict(response_requirement.subject_binding)["subject_goal_id"]} - goal_ids
        if unknown:
            raise ValueError(
                "response_requirement references unknown goal_id: " + ",".join(sorted(unknown))
            )


RESPONSE_SUBJECT_RELATIONS = (
    "SOURCE_OF_SUBJECT", "ACTOR_OF_SUBJECT", "OPERATION_OF_SUBJECT",
    "EFFECT_OF_OPERATION", "RECEIPT_OF_EFFECT", "REVIEW_OF_SUBJECT_OR_EXPERIENCE",
    "LEARNING_QUALIFICATION_OF_EXPERIENCE",
)
_RESPONSE_SUBJECT_IDENTITIES = (
    "experience_id", "trace_id", "request_id", "task_ref", "actor",
    "operation_id", "step_id", "receipt_id", "source_ref", "learning_bundle_id", "effect_type",
)


def response_subject_binding_schema() -> dict[str, Any]:
    """Request-local identity constraints; no evidence copies or subject registry."""
    return {"type": "object", "additionalProperties": False,
        "required": ["scope", "relation", "subject_goal_id"], "properties": {
            "scope": {"type": "string", "enum": ["SUBJECT", "EXISTENTIAL"]},
            "relation": {"type": "string", "enum": list(RESPONSE_SUBJECT_RELATIONS)},
            "subject_goal_id": {"type": "string", "minLength": 1},
            **{key: {"type": "string", "minLength": 1} for key in _RESPONSE_SUBJECT_IDENTITIES}}}


def validate_response_subject_binding(value: Any) -> dict[str, str]:
    if not isinstance(value, (dict, tuple)):
        raise ValueError("response_subject_binding_not_object")
    data = dict(value)
    required = {"scope", "relation", "subject_goal_id"}
    if not required <= set(data) or set(data) - required - set(_RESPONSE_SUBJECT_IDENTITIES):
        raise ValueError("response_subject_binding_invalid_fields")
    if any(not isinstance(v, str) or not v.strip() for v in data.values()):
        raise ValueError("response_subject_binding_invalid_identity")
    if data["scope"] not in {"SUBJECT", "EXISTENTIAL"} or data["relation"] not in RESPONSE_SUBJECT_RELATIONS:
        raise ValueError("response_subject_binding_invalid_relation")
    if "effect_type" in data and data["effect_type"] not in _ALLOWED_EFFECT_TYPES:
        raise ValueError("response_subject_binding_invalid_effect")
    return data


# Answer-fact semantics under the existing response contract, not retrieval routing.
_RESPONSE_REQUIREMENT_RELATIONS = {
    "PROVENANCE": {"allowed": ("SOURCE_OF_SUBJECT", "ACTOR_OF_SUBJECT"), "primary": "ACTOR_OF_SUBJECT"},
    "RATIONALE": {"allowed": ("SOURCE_OF_SUBJECT",), "primary": "SOURCE_OF_SUBJECT"},
    "EXECUTION": {"allowed": ("OPERATION_OF_SUBJECT", "EFFECT_OF_OPERATION", "RECEIPT_OF_EFFECT"), "primary": "RECEIPT_OF_EFFECT"},
    "EVIDENCE": {"allowed": ("SOURCE_OF_SUBJECT", "RECEIPT_OF_EFFECT"), "primary": "SOURCE_OF_SUBJECT"},
    "REVIEW_STATUS": {"allowed": ("REVIEW_OF_SUBJECT_OR_EXPERIENCE",), "primary": "REVIEW_OF_SUBJECT_OR_EXPERIENCE"},
    "LEARNING_QUALIFICATION": {"allowed": ("LEARNING_QUALIFICATION_OF_EXPERIENCE",), "primary": "LEARNING_QUALIFICATION_OF_EXPERIENCE"},
}


def response_subject_constraints_schema() -> dict[str, Any]:
    """Semantic identities on the existing GoalFrame, without host IDs/relation."""
    properties = response_subject_binding_schema()["properties"]
    return {"type": "object", "additionalProperties": False, "required": ["scope"],
            "properties": {k: v for k, v in properties.items() if k not in ("relation", "subject_goal_id")}}


def hydrate_response_requirements(goals: tuple[dict[str, Any], ...],
        obligations: tuple[dict[str, Any], ...]) -> tuple[dict[str, Any], ...]:
    """Project declared facets; identities remain untrusted constraints, not truth.

    This cannot prove the first model captured every natural-language facet.
    Canonical evidence joins and publication validation remain mandatory.
    """
    by_id = {g["goal_id"]: g for g in goals}
    if len(by_id) != len(goals):
        raise ValueError("response_subject_goal_duplicate")
    result = []
    for index, item in enumerate(obligations):
        data = dict(item)
        data.pop("schema_version", None)
        data["response_requirement_id"] = f"goalframe_response_{index}"
        kind = data.get("requirement_kind")
        if kind is not None and data.get("subject_binding") is None:
            if kind not in _RESPONSE_REQUIREMENT_RELATIONS:
                raise ValueError("response_requirement_kind_unknown")
            references = tuple(data["applies_to_goal_ids"])
            subject_id = data.pop("subject_goal_id", None)
            if subject_id is None:
                if len(references) != 1:
                    raise ValueError("response_subject_goal_ambiguous")
                subject_id = references[0]
            if subject_id not in by_id or subject_id not in references:
                raise ValueError("response_subject_goal_unknown")
            anchor = by_id[subject_id].get("subject_constraints")
            if not isinstance(anchor, dict):
                raise ValueError("response_subject_constraints_unavailable")
            data["subject_binding"] = {**anchor, "subject_goal_id": subject_id,
                                      "relation": _RESPONSE_REQUIREMENT_RELATIONS[kind]["primary"]}
        data.pop("subject_goal_id", None)
        typed = ResponseRequirement(**{**data, "applies_to_goal_ids": tuple(data["applies_to_goal_ids"])})
        validate_response_requirement_goal_references((typed,), set(by_id))
        result.append(typed.to_read_model())
    return tuple(result)


def validate_response_obligation_coverage(expected: tuple[dict[str, Any], ...],
        produced: tuple[dict[str, Any], ...]) -> None:
    """Bijection against declared facets; not a natural-language completeness claim."""
    def keyed(items):
        out = {}
        for item in items:
            key = item.get("response_requirement_id")
            if not isinstance(key, str) or not key or key in out:
                raise ValueError("response_obligation_duplicate_or_unbound")
            out[key] = item
        return out
    source, actual = keyed(expected), keyed(produced)
    if set(source) != set(actual):
        raise ValueError("response_obligation_missing_or_extra")
    if source != actual:
        raise ValueError("response_obligation_kind_subject_or_value_mismatch")
    import json
    facets = [json.dumps({k: v for k, v in q.items() if k not in ("response_requirement_id", "schema_version")},
                         sort_keys=True, ensure_ascii=False) for q in produced]
    if len(set(facets)) != len(facets):
        raise ValueError("response_obligation_duplicate")


def response_requirement_semantics_schema(*, native: bool = False,
        base_schema: dict[str, Any] | None = None) -> dict[str, Any]:
    """One compatibility constraint shared by generation and typed validation.

    Legacy direct callers may omit the new field. Native GoalFrame generation
    requires an explicit fact kind; a retrieval obligation cannot use null.
    """
    if native and base_schema is not None:
        # Model-facing semantic projection: one discriminated kind, no internal
        # IDs/bindings/relations. Complete internal validation follows hydration.
        common = {k: v for k, v in base_schema.items() if k not in ("anyOf", "oneOf")}
        properties = {k: v for k, v in common["properties"].items() if k != "subject_binding"}
        properties["subject_goal_id"] = {"type": "string", "minLength": 1}
        common = {**common, "properties": properties}
        alternatives = []
        for kind in (None, *_RESPONSE_REQUIREMENT_RELATIONS):
            values = {**properties, "requirement_kind": {"const": kind}}
            values["memory_query_kind"] = ({"type": "null"} if kind is None else {"type": "string"})
            alternatives.append({**common, "properties": values})
        return {**common, "oneOf": alternatives}
    legacy = {"properties": {"requirement_kind": {"type": "null"}}}
    if native:
        legacy["properties"]["memory_query_kind"] = {"type": "null"}
    constraint = {"properties": {"requirement_kind": {"anyOf": [
        {"type": "null"}, {"type": "string", "enum": list(_RESPONSE_REQUIREMENT_RELATIONS)}]}},
        "anyOf": [legacy, *({"required": ["requirement_kind", "subject_binding"],
            "properties": {"requirement_kind": {"const": kind}, "memory_query_kind": {"type": "string"},
                "subject_binding": {"properties": {"relation": {"enum": list(relations["allowed"])}}}}}
            for kind, relations in _RESPONSE_REQUIREMENT_RELATIONS.items())]}


    if base_schema is None:
        return constraint
    # Native grammar compilers may visit anyOf alternatives independently.
    # Make every alternative a complete original response object, including
    # all identity fields and required keys, rather than a partial property mask.
    common = {k: v for k, v in base_schema.items() if k != "anyOf"}
    alternatives = []
    for case in constraint["anyOf"]:
        properties = dict(common["properties"])
        for name, restriction in case["properties"].items():
            original = properties.get(name, {})
            properties[name] = {**original, **restriction}
            if name == "subject_binding":
                properties[name]["properties"] = {
                    **original.get("properties", {}), **restriction.get("properties", {})}
        alternatives.append({**common, "properties": properties,
            "required": list(dict.fromkeys([*common.get("required", ()), *case.get("required", ())]))})
    return {**common, "anyOf": alternatives}


def validate_response_requirement_relation(kind: Any, binding: Any) -> None:
    """Reject incompatible typed facts without interpreting or rewriting prose."""
    if kind is None:
        return  # Existing direct contract compatibility; native generation is strict.
    if not isinstance(kind, str) or kind not in _RESPONSE_REQUIREMENT_RELATIONS:
        raise ValueError("response_requirement_kind_unknown")
    typed = validate_response_subject_binding(binding)
    if typed["relation"] not in _RESPONSE_REQUIREMENT_RELATIONS[kind]["allowed"]:
        raise ValueError("response_requirement_relation_incompatible:" + kind)
    if typed["relation"] == "ACTOR_OF_SUBJECT" and not typed.get("actor"):
        raise ValueError("response_requirement_actor_identity_required")


@dataclass(frozen=True, slots=True)
class ResponseRequirement:
    response_requirement_id: str
    applies_to_goal_ids: tuple[str, ...]
    description: str = ""
    schema_version: str = "response_requirement.v1"
    memory_query_kind: str | None = None
    subject_binding: tuple[tuple[str, str], ...] | None = None
    requirement_kind: str | None = None

    def __post_init__(self) -> None:
        if self.schema_version != "response_requirement.v1":
            raise ValueError("schema_version must be response_requirement.v1")
        object.__setattr__(self, "response_requirement_id", _require_non_empty(
            self.response_requirement_id, "response_requirement_id"
        ))
        object.__setattr__(self, "applies_to_goal_ids", _normalize_string_tuple(
            self.applies_to_goal_ids, "applies_to_goal_ids"
        ))
        if not self.applies_to_goal_ids:
            raise ValueError("applies_to_goal_ids must reference at least one goal")
        if not isinstance(self.description, str):
            raise ValueError("description must be a string")
        if self.subject_binding is not None:
            object.__setattr__(self, "subject_binding", tuple(validate_response_subject_binding(self.subject_binding).items()))
        validate_response_requirement_relation(self.requirement_kind, self.subject_binding)
        if self.requirement_kind is not None and self.memory_query_kind is None:
            raise ValueError("typed_response_fact_requires_memory_query_kind")
        if self.memory_query_kind is not None:
            _require_non_empty(self.memory_query_kind, "memory_query_kind")

    def to_read_model(self) -> dict[str, Any]:
        return {
            "schema_version": self.schema_version,
            "response_requirement_id": self.response_requirement_id,
            "applies_to_goal_ids": list(self.applies_to_goal_ids),
            "description": self.description,
            **({"memory_query_kind": self.memory_query_kind} if self.memory_query_kind is not None else {}),
            **({"subject_binding": dict(self.subject_binding)} if self.subject_binding is not None else {}),
            **({"requirement_kind": self.requirement_kind} if self.requirement_kind is not None else {}),
        }


@dataclass(frozen=True, slots=True)
class OperationRequirement:
    capability_id: str
    operation_id: str
    purpose: str
    required_evidence: tuple[str, ...]
    effect_type: str
    target_scope: str
    reversibility: str
    external_side_effect: bool | None
    risk_class: str
    required: bool
    parameters: tuple[tuple[str, str], ...] = ()
    schema_version: str = "operation_requirement.v1"
    declared_prerequisite_for_operation_ids: tuple[str, ...] = ()

    def __post_init__(self) -> None:
        references = _normalize_string_tuple(self.declared_prerequisite_for_operation_ids, "declared_prerequisite_for_operation_ids")
        if references != self.declared_prerequisite_for_operation_ids or len(set(references)) != len(references):
            raise ValueError("operation_dependency_references_invalid_or_duplicate")
        if self.operation_id in references:
            raise ValueError("operation_dependency_self_reference")
        if self.schema_version != "operation_requirement.v1":
            raise ValueError("schema_version must be operation_requirement.v1")
        object.__setattr__(self, "capability_id", _require_non_empty(self.capability_id, "capability_id"))
        object.__setattr__(self, "operation_id", _require_non_empty(self.operation_id, "operation_id"))
        object.__setattr__(self, "purpose", _require_non_empty(self.purpose, "purpose"))
        object.__setattr__(self, "required_evidence", _normalize_string_tuple(self.required_evidence, "required_evidence"))
        object.__setattr__(self, "effect_type", _require_choice(self.effect_type, "effect_type", _ALLOWED_EFFECT_TYPES))
        object.__setattr__(self, "target_scope", _require_non_empty(self.target_scope, "target_scope"))
        object.__setattr__(self, "reversibility", _require_choice(self.reversibility, "reversibility", _ALLOWED_REVERSIBILITY))
        if self.external_side_effect not in (True, False, None):
            raise ValueError("external_side_effect must be bool or null")
        if self.risk_class not in {"READ_ONLY", "MUTATION", "DANGEROUS", "UNKNOWN"}:
            raise ValueError("unknown operation risk_class")
        if not self.required_evidence:
            raise ValueError("required_evidence must not be empty")
        if not isinstance(self.required, bool):
            raise ValueError("required must be bool")
        if not isinstance(self.parameters, tuple):
            raise ValueError("operation parameters must be a tuple")
        normalized_parameters: list[tuple[str, str]] = []
        for item in self.parameters:
            if not isinstance(item, tuple) or len(item) != 2:
                raise ValueError("operation parameters must contain key/value tuples")
            normalized_parameters.append((
                _require_non_empty(item[0], "operation parameter name"),
                _require_non_empty(item[1], "operation parameter value"),
            ))
        if len({key for key, _ in normalized_parameters}) != len(normalized_parameters):
            raise ValueError("operation parameter names must be unique")
        object.__setattr__(self, "parameters", tuple(normalized_parameters))

    def to_read_model(self) -> dict[str, Any]:
        return {
            "schema_version": self.schema_version,
            "capability_id": self.capability_id,
            "operation_id": self.operation_id,
            "purpose": self.purpose,
            "required_evidence": self.required_evidence,
            "effect_type": self.effect_type,
            "target_scope": self.target_scope,
            "reversibility": self.reversibility,
            "external_side_effect": self.external_side_effect,
            "risk_class": self.risk_class,
            "required": self.required,
            "parameters": dict(self.parameters),
            **({"declared_prerequisite_for_operation_ids": self.declared_prerequisite_for_operation_ids}
               if self.declared_prerequisite_for_operation_ids else {}),
        }


@dataclass(frozen=True, slots=True)
class RequestUnderstanding:
    request_id: str
    original_text: str
    language: str
    goals: tuple[Goal, ...]
    required_capabilities: tuple[CapabilityRequirement, ...]
    effect_type: str
    target_scope: str
    reversibility: str
    external_side_effect: bool | None
    unresolved_capabilities: tuple[str, ...]
    operation_requirements: tuple[OperationRequirement, ...]
    current_topic: str
    unresolved_reference: str
    relevant_context_trace_ids: tuple[str, ...]
    risk_class: str
    confidence: float
    reason_codes: tuple[str, ...]
    response_requirements: tuple[ResponseRequirement, ...] = ()
    execution_restriction: str = "NONE"
    execution_restriction_source: str = ""
    schema_version: str = "request_understanding.v2"

    def __post_init__(self) -> None:
        if self.schema_version != "request_understanding.v2":
            raise ValueError("schema_version must be request_understanding.v2")
        object.__setattr__(self, "request_id", _require_non_empty(self.request_id, "request_id"))
        object.__setattr__(self, "original_text", _require_non_empty(self.original_text, "original_text"))
        object.__setattr__(self, "language", _require_non_empty(self.language, "language"))
        object.__setattr__(
            self,
            "execution_restriction",
            _require_choice(self.execution_restriction, "execution_restriction", _ALLOWED_EXECUTION_RESTRICTIONS),
        )
        if self.execution_restriction != "NONE" and not self.execution_restriction_source.strip():
            raise ValueError("non-NONE execution_restriction must be source-grounded to the utterance")
        object.__setattr__(self, "execution_restriction_source", self.execution_restriction_source.strip())
        if not self.goals or not all(isinstance(item, Goal) for item in self.goals):
            raise ValueError("goals must contain Goal values")
        if not all(isinstance(item, CapabilityRequirement) for item in self.required_capabilities):
            raise ValueError("required_capabilities must contain CapabilityRequirement values")
        if not all(isinstance(item, ResponseRequirement) for item in self.response_requirements):
            raise ValueError("response_requirements must contain ResponseRequirement values")
        validate_response_requirement_goal_references(
            self.response_requirements, {item.goal_id for item in self.goals},
        )
        object.__setattr__(self, "effect_type", _require_choice(self.effect_type, "effect_type", _ALLOWED_EFFECT_TYPES))
        object.__setattr__(self, "target_scope", _require_non_empty(self.target_scope, "target_scope"))
        object.__setattr__(self, "reversibility", _require_choice(self.reversibility, "reversibility", _ALLOWED_REVERSIBILITY))
        if self.external_side_effect not in (True, False, None):
            raise ValueError("external_side_effect must be bool or null")
        if not isinstance(self.unresolved_capabilities, tuple):
            raise ValueError("unresolved_capabilities must be a tuple")
        for capability_id in self.unresolved_capabilities:
            _require_non_empty(capability_id, "unresolved_capabilities")
        if not all(isinstance(item, OperationRequirement) for item in self.operation_requirements):
            raise ValueError("operation_requirements must contain OperationRequirement values")
        _validate_operation_reference_order(self.operation_requirements, "operation_id")
        if not isinstance(self.current_topic, str) or not isinstance(self.unresolved_reference, str):
            raise ValueError("topic and unresolved reference must be strings")
        if self.risk_class not in {"READ_ONLY", "MUTATION", "DANGEROUS", "UNKNOWN"}:
            raise ValueError("unknown risk_class")
        object.__setattr__(self, "relevant_context_trace_ids", _normalize_string_tuple(
            self.relevant_context_trace_ids, "relevant_context_trace_ids"
        ))
        object.__setattr__(self, "confidence", _normalize_confidence(self.confidence))

    def to_read_model(self) -> dict[str, Any]:
        return {
            "schema_version": self.schema_version,
            "request_id": self.request_id,
            "original_text": self.original_text,
            "language": self.language,
            "goals": tuple(item.to_read_model() for item in self.goals),
            "required_capabilities": tuple(item.to_read_model() for item in self.required_capabilities),
            "response_requirements": tuple(item.to_read_model() for item in self.response_requirements),
            "effect_type": self.effect_type,
            "target_scope": self.target_scope,
            "reversibility": self.reversibility,
            "external_side_effect": self.external_side_effect,
            "unresolved_capabilities": self.unresolved_capabilities,
            "operation_requirements": tuple(item.to_read_model() for item in self.operation_requirements),
            "current_topic": self.current_topic,
            "unresolved_reference": self.unresolved_reference,
            "relevant_context_trace_ids": self.relevant_context_trace_ids,
            "risk_class": self.risk_class,
            "confidence": self.confidence,
            "reason_codes": self.reason_codes,
            "execution_restriction": self.execution_restriction,
            "execution_restriction_source": self.execution_restriction_source,
        }


@dataclass(frozen=True, slots=True)
class CapabilityCandidate:
    capability_id: str
    provider_id: str
    status: str
    permissions_granted: bool
    healthy: bool
    schema_version: str = "capability_candidate.v1"

    def __post_init__(self) -> None:
        if self.schema_version != "capability_candidate.v1":
            raise ValueError("schema_version must be capability_candidate.v1")
        object.__setattr__(self, "capability_id", _require_non_empty(self.capability_id, "capability_id"))
        object.__setattr__(self, "provider_id", _require_non_empty(self.provider_id, "provider_id"))
        if self.status not in {"AVAILABLE", "UNAVAILABLE"}:
            raise ValueError("candidate status must be AVAILABLE or UNAVAILABLE")

    def to_read_model(self) -> dict[str, Any]:
        return {
            "schema_version": self.schema_version,
            "capability_id": self.capability_id,
            "provider_id": self.provider_id,
            "status": self.status,
            "permissions_granted": self.permissions_granted,
            "healthy": self.healthy,
        }


@dataclass(frozen=True, slots=True)
class PlanStep:
    step_id: str
    goal_id: str
    capability_id: str
    operation: str
    required_evidence: tuple[str, ...]
    effect_type: str
    target_scope: str
    reversibility: str
    external_side_effect: bool
    risk_class: str
    parameters: tuple[tuple[str, str], ...] = ()
    schema_version: str = "plan_step.v1"
    declared_prerequisite_for_operation_ids: tuple[str, ...] = ()

    def __post_init__(self) -> None:
        references = _normalize_string_tuple(self.declared_prerequisite_for_operation_ids, "declared_prerequisite_for_operation_ids")
        if references != self.declared_prerequisite_for_operation_ids or len(set(references)) != len(references):
            raise ValueError("operation_dependency_references_invalid_or_duplicate")
        if self.operation in references:
            raise ValueError("operation_dependency_self_reference")
        if self.schema_version != "plan_step.v1":
            raise ValueError("invalid plan step schema")
        for field_name in ("step_id", "goal_id", "capability_id", "operation"):
            object.__setattr__(self, field_name, _require_non_empty(getattr(self, field_name), field_name))
        object.__setattr__(self, "required_evidence", _normalize_string_tuple(self.required_evidence, "required_evidence"))
        if not self.required_evidence:
            raise ValueError("plan step required_evidence must not be empty")
        object.__setattr__(self, "effect_type", _require_choice(self.effect_type, "effect_type", _ALLOWED_EFFECT_TYPES))
        object.__setattr__(self, "target_scope", _require_non_empty(self.target_scope, "target_scope"))
        object.__setattr__(self, "reversibility", _require_choice(self.reversibility, "reversibility", _ALLOWED_REVERSIBILITY))
        if not isinstance(self.external_side_effect, bool):
            raise ValueError("external_side_effect must be bool")
        if self.risk_class not in {"READ_ONLY", "MUTATION", "DANGEROUS", "UNKNOWN"}:
            raise ValueError("unknown plan step risk_class")
        if not isinstance(self.parameters, tuple):
            raise ValueError("plan step parameters must be a tuple")
        normalized_parameters: list[tuple[str, str]] = []
        for item in self.parameters:
            if not isinstance(item, tuple) or len(item) != 2:
                raise ValueError("plan step parameters must contain key/value tuples")
            normalized_parameters.append((
                _require_non_empty(item[0], "plan step parameter name"),
                _require_non_empty(item[1], "plan step parameter value"),
            ))
        if len({key for key, _ in normalized_parameters}) != len(normalized_parameters):
            raise ValueError("plan step parameter names must be unique")
        object.__setattr__(self, "parameters", tuple(normalized_parameters))

    def to_read_model(self) -> dict[str, Any]:
        return self.__dict__ if hasattr(self, "__dict__") else {
            "schema_version": self.schema_version, "step_id": self.step_id,
            "goal_id": self.goal_id, "capability_id": self.capability_id, "operation": self.operation,
            "required_evidence": self.required_evidence,
            "effect_type": self.effect_type, "target_scope": self.target_scope,
            "reversibility": self.reversibility, "external_side_effect": self.external_side_effect,
            "risk_class": self.risk_class, "parameters": dict(self.parameters),
            **({"declared_prerequisite_for_operation_ids": self.declared_prerequisite_for_operation_ids}
               if self.declared_prerequisite_for_operation_ids else {}),
        }


@dataclass(frozen=True, slots=True)
class ExecutionPlan:
    request_id: str
    steps: tuple[PlanStep, ...]
    schema_version: str = "execution_plan.v1"

    def __post_init__(self) -> None:
        if self.schema_version != "execution_plan.v1" or not self.steps:
            raise ValueError("execution plan must contain versioned steps")
        _validate_operation_reference_order(self.steps, "operation")

    def to_read_model(self) -> dict[str, Any]:
        return {"schema_version": self.schema_version, "request_id": self.request_id, "steps": tuple(x.to_read_model() for x in self.steps)}


@dataclass(frozen=True, slots=True)
class EvidenceItem:
    kind: str
    source: str
    observation: str
    scope: str
    confidence: float
    trace_id: str
    observed_at: str
    content_hash: str = ""
    source_reference: str = ""
    truncated: bool = False
    omitted_count: int = 0
    request_id: str = ""
    step_id: str = ""
    capability_id: str = ""
    operation_id: str = ""
    provider_id: str = ""
    schema_version: str = "evidence_item.v1"

    def __post_init__(self) -> None:
        if self.schema_version != "evidence_item.v1":
            raise ValueError("schema_version must be evidence_item.v1")
        for field_name in ("kind", "source", "observation", "scope", "trace_id", "observed_at"):
            object.__setattr__(self, field_name, _require_non_empty(getattr(self, field_name), field_name))
        object.__setattr__(self, "confidence", _normalize_confidence(self.confidence))
        if self.omitted_count < 0:
            raise ValueError("omitted_count must be non-negative")

    def to_read_model(self) -> dict[str, Any]:
        return {name: getattr(self, name) for name in self.__dataclass_fields__}


@dataclass(frozen=True, slots=True)
class ExecutionReceipt:
    receipt_id: str
    request_id: str
    trace_id: str
    step_id: str
    capability_id: str
    operation_id: str
    provider_id: str
    status: str
    result: str
    schema_version: str = "execution_receipt.v1"

    def __post_init__(self) -> None:
        if self.schema_version != "execution_receipt.v1":
            raise ValueError("invalid execution receipt schema")
        for name in ("receipt_id", "request_id", "trace_id", "step_id", "capability_id", "operation_id", "provider_id", "result"):
            object.__setattr__(self, name, _require_non_empty(getattr(self, name), name))
        if self.status not in {"COMPLETE", "FAILED", "TIMEOUT"}:
            raise ValueError("invalid execution receipt status")

    def to_read_model(self) -> dict[str, Any]:
        return {name: getattr(self, name) for name in self.__dataclass_fields__}


@dataclass(frozen=True, slots=True)
class EvidenceBundle:
    request_id: str
    capability_id: str
    trace_id: str
    status: str
    items: tuple[EvidenceItem, ...]
    limitations: tuple[str, ...]
    receipts: tuple[ExecutionReceipt, ...]
    errors: tuple[str, ...]
    schema_version: str = "evidence_bundle.v1"
    capability_ids: tuple[str, ...] = ()

    def __post_init__(self) -> None:
        if self.schema_version != "evidence_bundle.v1":
            raise ValueError("schema_version must be evidence_bundle.v1")
        if self.status not in {"COMPLETE", "PARTIAL", "UNAVAILABLE"}:
            raise ValueError("invalid evidence status")
        if any(item.trace_id != self.trace_id for item in self.items):
            raise ValueError("all evidence items must share bundle trace_id")
        for item in self.items:
            if not all((item.request_id, item.step_id, item.capability_id, item.operation_id, item.provider_id)):
                raise ValueError("evidence items must be attributed to request/step/capability/operation/provider")
            if item.request_id != self.request_id:
                raise ValueError("all evidence items must share bundle request_id")
        if not all(isinstance(item, ExecutionReceipt) for item in self.receipts):
            raise ValueError("receipts must contain ExecutionReceipt values")
        if any(item.trace_id != self.trace_id or item.request_id != self.request_id for item in self.receipts):
            raise ValueError("all receipts must share bundle request_id and trace_id")
        if not self.capability_ids:
            object.__setattr__(self, "capability_ids", (self.capability_id,))
        object.__setattr__(self, "capability_ids", _normalize_string_tuple(self.capability_ids, "capability_ids"))

    def to_read_model(self) -> dict[str, Any]:
        return {
            "schema_version": self.schema_version, "request_id": self.request_id,
            "capability_id": self.capability_id, "trace_id": self.trace_id, "status": self.status,
            "capability_ids": self.capability_ids,
            "items": tuple(x.to_read_model() for x in self.items), "limitations": self.limitations,
            "receipts": tuple(item.to_read_model() for item in self.receipts), "errors": self.errors,
        }


@dataclass(frozen=True, slots=True)
class OrchestrationTrace:
    trace_id: str
    request_id: str
    route: str
    stages: tuple[str, ...]
    selected_capabilities: tuple[str, ...]
    selected_providers: tuple[str, ...]
    policy_result: str
    evidence_status: str
    final_brain_status: str
    rollback_reason: str = ""
    schema_version: str = "orchestration_trace.v1"

    def to_read_model(self) -> dict[str, Any]:
        return {name: getattr(self, name) for name in self.__dataclass_fields__}


class ProjectUnderstandingPort(ABC):
    @abstractmethod
    def health(self) -> dict[str, Any]: ...

    @abstractmethod
    def collect_evidence(self, understanding: RequestUnderstanding, plan: ExecutionPlan, trace_id: str,
                         deadline: "RequestDeadline | None" = None) -> EvidenceBundle: ...


class ConversationPort(ABC):
    @abstractmethod
    def health(self) -> dict[str, Any]: ...

    @abstractmethod
    def collect_evidence(self, understanding: RequestUnderstanding, plan: ExecutionPlan, trace_id: str,
                         identity: "IdentityContext", session_context: dict[str, Any],
                         deadline: "RequestDeadline | None" = None) -> EvidenceBundle: ...


@dataclass(frozen=True, slots=True)
class IdentityContext:
    identity_id: str
    identity_source: str
    profile_type: str
    owner_verified: bool
    trusted: bool
    display_name: str = ""
    assistant_identity: str = "JARVIS"
    schema_version: str = "identity_context.v1"

    def __post_init__(self) -> None:
        if self.schema_version != "identity_context.v1":
            raise ValueError("invalid identity schema")
        for name in ("identity_id", "identity_source", "profile_type"):
            object.__setattr__(self, name, _require_non_empty(getattr(self, name), name))

    def to_read_model(self) -> dict[str, Any]:
        return {name: getattr(self, name) for name in self.__dataclass_fields__}

    @property
    def owner_authorized(self) -> bool:
        return self.owner_verified and self.trusted and self.profile_type == "owner"


@dataclass(frozen=True, slots=True)
class PermissionDecision:
    granted: bool
    capability_id: str
    identity_source: str
    policy_version: str
    denial_reason: str
    trace_id: str
    operation_id: str = ""
    approval_required: bool = False
    schema_version: str = "permission_decision.v1"
    # Canonical execution scope.  Mutation authorization must bind to the
    # concrete PlanStep; an empty value is never a wildcard for mutations.
    step_id: str = ""

    def to_read_model(self) -> dict[str, Any]:
        return {name: getattr(self, name) for name in self.__dataclass_fields__}


class PermissionEvaluationPort(ABC):
    @abstractmethod
    def evaluate(self, *, capability_id: str, operation_id: str = "", risk_class: str,
                 effect_type: str = "OBSERVE", target_scope: str = "unknown",
                 reversibility: str = "UNKNOWN", external_side_effect: bool = False,
                 identity: IdentityContext, trace_id: str, step_id: str = "") -> PermissionDecision: ...


class ModelUnderstandingPort(ABC):
    @abstractmethod
    def understand(self, *, system_prompt: str, user_prompt: str,
                   deadline: "RequestDeadline") -> dict[str, Any]: ...


@dataclass(frozen=True, slots=True)
class GroundedResponseSection:
    """Model-authored presentation referencing the supplied evidence assertions.

    Reference claims are not truth: the existing FinalBrain publication gate
    must still prove exact values, associations and the entire explanation.
    """
    prose: str
    covered_fact_ids: tuple[int, ...]

    def __post_init__(self) -> None:
        if not isinstance(self.prose, str) or not self.prose.strip():
            raise ValueError("grounded_response_empty_prose")
        if (not isinstance(self.covered_fact_ids, tuple)
                or any(type(value) is not int or value < 0 for value in self.covered_fact_ids)):
            raise ValueError("grounded_response_invalid_fact_ids")
        if len(set(self.covered_fact_ids)) != len(self.covered_fact_ids):
            raise ValueError("grounded_response_duplicate_fact_ids")

    @classmethod
    def generation_schema(cls, fact_ids: tuple[int, ...], *, exact_coverage: bool = True) -> dict[str, Any]:
        """Constrain references to source facts; prose remains model-authored.

        Grammar constraints do not prove that prose covers or preserves a fact.
        Publication still requires the complete factual/semantic validator.
        """
        if (not isinstance(fact_ids, tuple)
                or any(type(value) is not int or value < 0 for value in fact_ids)
                or len(set(fact_ids)) != len(fact_ids)):
            raise ValueError("grounded_response_invalid_schema_fact_ids")
        return {
            "type": "object", "additionalProperties": False,
            "required": ["prose", "covered_fact_ids"],
            "properties": {
                "prose": {"type": "string", "minLength": 1},
                "covered_fact_ids": {
                    "type": "array", "uniqueItems": True,
                    **({"minItems": len(fact_ids), "maxItems": len(fact_ids)} if exact_coverage else {}),
                    "items": {"type": "integer", "minimum": min(fact_ids, default=0),
                              "maximum": max(fact_ids, default=-1)},
                },
            },
        }

    def evidence_presentation(self, catalog: dict[int, tuple[str, Any]], *, source_digest: str) -> dict[str, Any]:
        """Resolve validated request-local references; never generate model prose."""
        from copy import deepcopy
        if any(fact_id not in catalog for fact_id in self.covered_fact_ids):
            raise ValueError("grounded_response_unknown_fact_id")
        return {"prose": self.prose, "facts": [
            {"fact_id": fact_id, "assertion_path": catalog[fact_id][0],
             "value": deepcopy(catalog[fact_id][1]), "assertion_source_sha256": source_digest}
            for fact_id in self.covered_fact_ids]}

    @classmethod
    def from_read_model(cls, value: Any) -> "GroundedResponseSection":
        if (not isinstance(value, dict) or set(value) != {"prose", "covered_fact_ids"}
                or not isinstance(value.get("covered_fact_ids"), list)):
            raise ValueError("grounded_response_invalid_section")
        return cls(prose=value["prose"], covered_fact_ids=tuple(value["covered_fact_ids"]))


class FinalBrainPort(ABC):
    @abstractmethod
    def answer(self, *, deadline: "RequestDeadline", **payload: Any) -> dict[str, Any]: ...


@dataclass(frozen=True, slots=True)
class UnderstandingAttemptPolicy:
    """Existing adapter retry policy and optional request-wide model-call ceiling."""
    max_model_attempts: int | None = None
    schema_max_attempts: int = 2

    def __post_init__(self) -> None:
        if type(self.schema_max_attempts) is not int or self.schema_max_attempts not in (1, 2):
            raise ValueError("understanding_schema_attempt_budget_invalid")
        if self.max_model_attempts is not None and (
                type(self.max_model_attempts) is not int or self.max_model_attempts < 1):
            raise ValueError("understanding_model_attempt_budget_invalid")


_CURRENT_REQUEST_DEADLINE: ContextVar[RequestDeadline | None] = ContextVar("canonical_request_deadline", default=None)


class RequestDeadline:
    """Shared monotonic deadline and cooperative cancellation token."""

    def __init__(self, timeout_seconds: float, *, started_at: float | None = None,
                 understanding_attempt_policy: UnderstandingAttemptPolicy | None = None) -> None:
        if not isinstance(timeout_seconds, (int, float)) or isinstance(timeout_seconds, bool) or not math.isfinite(timeout_seconds) or timeout_seconds <= 0:
            raise ValueError("timeout_seconds must be positive")
        self.started_at = time.monotonic() if started_at is None else started_at
        if not isinstance(self.started_at, (int, float)) or not math.isfinite(self.started_at):
            raise ValueError("started_at must be finite monotonic time")
        self.expires_at = self.started_at + float(timeout_seconds)
        self._cancelled = threading.Event()
        self.understanding_attempt_policy = UnderstandingAttemptPolicy() if understanding_attempt_policy is None else understanding_attempt_policy
        if not isinstance(self.understanding_attempt_policy, UnderstandingAttemptPolicy):
            raise ValueError("understanding_attempt_policy_invalid")
        self._understanding_attempt_lock = threading.Lock()
        self._attempt_policy_bound = understanding_attempt_policy is not None
        self.understanding_model_attempt_count = 0
        self.understanding_model_attempts: list[dict[str, Any]] = []

    @staticmethod
    def current() -> RequestDeadline | None:
        return _CURRENT_REQUEST_DEADLINE.get()

    @contextmanager
    def bind(self):
        """Carry this same authority through native request/threadpool context."""
        current = self.current()
        if current is not None and current is not self:
            raise ValueError("request_deadline_authority_conflict")
        binding = _CURRENT_REQUEST_DEADLINE.set(self)
        try:
            yield self
        finally:
            _CURRENT_REQUEST_DEADLINE.reset(binding)

    def bind_attempt_policy(self, policy: UnderstandingAttemptPolicy) -> None:
        if not isinstance(policy, UnderstandingAttemptPolicy):
            raise ValueError("understanding_attempt_policy_invalid")
        with self._understanding_attempt_lock:
            if self._attempt_policy_bound or self.understanding_model_attempt_count:
                if policy != self.understanding_attempt_policy:
                    raise ValueError("understanding_attempt_policy_conflict")
            else:
                self.understanding_attempt_policy = policy
                self._attempt_policy_bound = True

    def check(self) -> None:
        if self.cancelled:
            raise TimeoutError("canonical_request_cancelled_or_expired")

    def reserve_understanding_model_attempt(self) -> int:
        with self._understanding_attempt_lock:
            limit = self.understanding_attempt_policy.max_model_attempts
            if limit is not None and self.understanding_model_attempt_count >= limit:
                raise ValueError("understanding_model_attempt_budget_exhausted")
            self.understanding_model_attempt_count += 1
            return self.understanding_model_attempt_count

    def understanding_attempt_available(self) -> bool:
        with self._understanding_attempt_lock:
            limit = self.understanding_attempt_policy.max_model_attempts
            return limit is None or self.understanding_model_attempt_count < limit

    def remaining(self, component_limit: float | None = None) -> float:
        remaining = max(0.0, self.expires_at - time.monotonic())
        return min(remaining, component_limit) if component_limit is not None else remaining

    def cancel(self) -> None:
        self._cancelled.set()

    @property
    def cancelled(self) -> bool:
        return self._cancelled.is_set() or self.remaining() <= 0


def utc_observed_at() -> str:
    return datetime.now(tz=UTC).isoformat(timespec="seconds")


def _logical_step_item_schema(nesting_depth: int = 2) -> dict[str, Any]:
    """Provider-neutral DAG step variants; topology is flat, so grammar is non-recursive."""
    common = {
        "step_id": {"type": "string", "minLength": 1, "maxLength": 48},
        "next_step_ids": {"type": "array", "maxItems": 8, "uniqueItems": True, "items": {"type": "string"}},
    }
    def variant(action: str, required: tuple[str, ...], properties: dict[str, Any]) -> dict[str, Any]:
        return {"type": "object", "additionalProperties": False,
                "required": ["action", "step_id", "next_step_ids", *required],
                "properties": {**common, "action": {"type": "string", "const": action}, **properties}}
    return {"oneOf": [
        variant("set_field", ("field", "value"), {
            "field": {"type": "string"},
            "value": {"type": "string", "description": "Assignment only; never calculate, transform, generate, fetch, store, or publish."},
        }),
        variant("transform", ("code",), {
            "code": {"type": "string", "description": "Executable n8n JavaScript that performs the requested local data transformation."},
        }),
        variant("http_request", ("url",), {"url": {"type": "string"},
            "method": {"type": "string", "enum": ["GET", "POST", "PUT", "PATCH", "DELETE"]}}),
        variant("jarvis_capability", ("capability_id", "request"), {
            "capability_id": {"type": "string", "minLength": 1, "maxLength": 120},
            "request": {"type": "string", "minLength": 1, "maxLength": 1000}}),
        variant("catalog_query", (
            "catalog_query", "semantic_operation", "provider_name", "provider_provenance",
            "provider_inference_justification", "arguments",
        ), {
            "catalog_query": {"type": "string"},
            "semantic_operation": {
                "type": "string", "minLength": 1, "maxLength": 40,
                "description": "Concise base-form intended action, never the broad operation class or source sentence.",
            },
            "provider_name": {"type": "string"},
            "provider_provenance": {"type": "string", "enum": ["SOURCE_EXPLICIT", "SEMANTIC_INFERENCE"]},
            "provider_inference_justification": {"type": "string"},
            "arguments": {
                "type": "object",
                "description": "Source values keyed by semantic display names, not guessed installed names.",
            }}),
        variant("condition", ("field", "operator", "true_step_id", "false_step_id"), {
            "field": {"type": "string"}, "value": {"type": "string"},
            "operator": {"type": "string", "enum": [
                "equals", "equal", "not_equals", "contains", "greater", "less", "exists", "not_exists"]},
            "true_step_id": {"type": "string"}, "false_step_id": {"type": "string"}}),
        variant("route", ("field", "branches"), {"field": {"type": "string"},
            "branches": {"type": "array", "minItems": 1, "maxItems": 8, "items": {
                "type": "object", "additionalProperties": False, "required": ["target_step_id"],
                "properties": {"label": {"type": "string"}, "value": {"type": "string"},
                               "default": {"type": "boolean"}, "target_step_id": {"type": "string"}}}}}),
        variant("merge", (), {"merge_mode": {"type": "string", "enum": ["append", "combine_by_position"]}}),
    ]}


_LOGICAL_SPEC_PARAMETER_SCHEMA: dict[str, Any] = {
    "type": "object",
    "additionalProperties": False,
    "required": ["trigger", "steps"],
    "description": (
        "Provider-neutral logical automation spec. Trigger and steps describe the semantic "
        "requirement (catalog_query) only; never installed node types or versions."
    ),
    "properties": {
        "trigger": {
            "oneOf": [
                {
                    "type": "string",
                    "enum": ["manual", "schedule", "webhook"],
                    "description": "Intrinsic trigger kind: manual (button/run), schedule (time), or webhook.",
                },
                {
                    "type": "object",
                    "additionalProperties": False,
                    "required": ["catalog_query", "provider_name"],
                    "properties": {
                        "catalog_query": {
                            "type": "string", "minLength": 4, "maxLength": 200,
                            "description": "Trigger discovery requirement; never an executable provider selection.",
                        },
                        "provider_name": {
                            "type": "string", "minLength": 1, "maxLength": 200,
                            "description": "Exact installed provider identity selected by the existing author model.",
                        },
                    },
                },
            ],
        },
        "steps": {
            "type": "array",
            "minItems": 1,
            "maxItems": 8,
            "items": _logical_step_item_schema(),
        },
        "semantic_requirements": {
            "type": "array", "maxItems": 8, "items": {
                "type": "object", "additionalProperties": False,
                "required": ["requirement_id", "operation_class", "source_grounding", "step_id"],
                "properties": {
                    "requirement_id": {"type": "string", "minLength": 1, "maxLength": 48},
                    "operation_class": {"type": "string", "enum": [
                        "ASSIGN", "TRANSFORM", "FETCH", "GENERATE", "PUBLISH", "SEND", "RECORD",
                        "STORE", "TRANSCRIBE", "SYNTHESIZE", "RENDER", "SEARCH", "DELEGATE",
                        "OBSERVE", "ACT",
                    ]},
                    "source_grounding": {"type": "string", "minLength": 1, "maxLength": 160},
                    "step_id": {"type": "string", "minLength": 1, "maxLength": 48},
                },
            },
        },
        "constraints": {
            "type": "array",
            "items": {"type": "string", "enum": ["local_only", "no_credentials"]},
            "uniqueItems": True,
        },
    },
}
