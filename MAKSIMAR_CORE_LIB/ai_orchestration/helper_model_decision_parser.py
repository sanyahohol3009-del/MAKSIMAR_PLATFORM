from __future__ import annotations

import json
import re
import unicodedata
from dataclasses import dataclass
from typing import Any

from MAKSIMAR_CORE_LIB.ai_orchestration.semantic_intent_contract import (
    CapabilityRequirement,
    Goal,
    OperationRequirement,
    RequestUnderstanding,
    ResponseRequirement,
)


def normalize_input_text(raw_text: str) -> str:
    """Apply platform-neutral, meaning-preserving normalization before model correction."""
    normalized = unicodedata.normalize("NFC", str(raw_text or ""))
    return re.sub(r"[\t\r\f\v ]+", " ", normalized).strip()


def _require_non_empty_string(value: Any, field_name: str) -> str:
    if not isinstance(value, str) or not value.strip():
        raise ValueError(f"{field_name} must be a non-empty string")
    return value.strip()


def _normalize_operation_parameter(value: Any, parameter: str) -> str:
    """Normalize one operation parameter to a string. A structured `logical_spec`
    (object) is serialized to JSON so it stays a single string parameter."""
    if parameter in {"logical_spec", "memory_filter"} and isinstance(value, dict):
        return json.dumps(value, ensure_ascii=False)
    return _require_non_empty_string(value, parameter)


def _require_string_list(value: Any, field_name: str) -> tuple[str, ...]:
    if not isinstance(value, list):
        raise ValueError(f"{field_name} must be a list")
    normalized_items: list[str] = []
    for item in value:
        if isinstance(item, dict) and field_name == "workflow_steps":
            step_name = item.get("step_name") or item.get("action") or item.get("name")
            normalized_items.append(_require_non_empty_string(step_name, field_name))
            continue
        normalized_items.append(_require_non_empty_string(item, field_name))
    normalized = tuple(normalized_items)
    if not normalized:
        raise ValueError(f"{field_name} must not be empty")
    return normalized


def _normalize_confidence(value: Any) -> float:
    try:
        confidence = float(value)
    except (TypeError, ValueError) as exc:
        raise ValueError("confidence must be numeric") from exc

    if confidence >= 2.0 and confidence <= 100.0:
        confidence = confidence / 100.0
    if confidence < 0.0:
        return 0.0
    if confidence > 1.0:
        return 1.0
    return confidence


def _strict_json_object(payload: str, *, contract_name: str) -> dict[str, Any]:
    """Parse one complete JSON object and reject duplicate fields."""
    def object_pairs(pairs: list[tuple[str, Any]]) -> dict[str, Any]:
        result: dict[str, Any] = {}
        for key, value in pairs:
            if key in result:
                raise ValueError(f"{contract_name} contains duplicate field: {key}")
            result[key] = value
        return result

    try:
        raw = json.loads(payload, object_pairs_hook=object_pairs)
    except json.JSONDecodeError as exc:
        raise ValueError(f"{contract_name} must be valid JSON") from exc
    if not isinstance(raw, dict):
        raise ValueError(f"{contract_name} must be a JSON object")
    return raw


@dataclass(frozen=True, slots=True)
class HelperInputCorrection:
    corrected_text: str
    ambiguity_candidates: tuple[str, ...]
    confidence: float
    reason_codes: tuple[str, ...]
    preserve_original: bool
    no_change_needed: bool
    schema_version: str = "helper_input_correction.v2"

    def to_read_model(self) -> dict[str, Any]:
        return {name: getattr(self, name) for name in self.__dataclass_fields__}


class RepairableHelperCorrectionContradiction(ValueError):
    """Strict helper truth failure eligible for one same-model quality review."""

    def __init__(self, message: str, *, sanitized_payload: dict[str, Any]) -> None:
        super().__init__(message)
        self.sanitized_payload = dict(sanitized_payload)


def parse_helper_input_correction_payload(
    payload: dict[str, Any] | str,
    *,
    expected_safe_normalized_text: str,
) -> HelperInputCorrection:
    """Parse correction-only helper output; capability and operation fields are forbidden."""
    if isinstance(payload, str):
        raw = _strict_json_object(payload, contract_name="helper input correction")
    elif isinstance(payload, dict):
        raw = dict(payload)
    else:
        raise TypeError("payload must be dict or JSON string")
    required = {
        "schema_version", "corrected_text", "ambiguity_candidates", "confidence",
        "reason_codes", "preserve_original", "no_change_needed",
    }
    if set(raw) != required:
        raise ValueError("helper input correction fields must exactly match correction schema")
    if raw["schema_version"] != "helper_input_correction.v2":
        raise ValueError("unknown helper input correction schema")
    corrected_text = _require_non_empty_string(raw["corrected_text"], "corrected_text")
    ambiguities = _require_string_list_allow_empty(raw["ambiguity_candidates"], "ambiguity_candidates")
    reasons = _require_string_list(raw["reason_codes"], "reason_codes")
    forbidden = {"capability_id", "operation_id", "provider_id", "selected_tools", "policy_decision"}
    if forbidden.intersection(raw):
        raise ValueError("helper input correction cannot select semantic execution fields")
    if raw["preserve_original"] is not True:
        raise ValueError("helper input correction must preserve original input")
    if not isinstance(raw["no_change_needed"], bool):
        raise ValueError("no_change_needed must be boolean")
    changed = corrected_text != expected_safe_normalized_text
    if raw["no_change_needed"] is changed:
        raise RepairableHelperCorrectionContradiction(
            "no_change_needed must exactly reflect whether corrected_text changed",
            sanitized_payload=raw,
        )
    return HelperInputCorrection(
        corrected_text=corrected_text,
        ambiguity_candidates=ambiguities,
        confidence=_normalize_confidence(raw["confidence"]),
        reason_codes=reasons,
        preserve_original=True,
        no_change_needed=raw["no_change_needed"],
    )


def _require_string_list_allow_empty(value: Any, field_name: str) -> tuple[str, ...]:
    if not isinstance(value, list):
        raise ValueError(f"{field_name} must be a list")
    return tuple(_require_non_empty_string(item, field_name) for item in value)


def parse_request_understanding_payload(
    payload: dict[str, Any] | str,
    *,
    host_request_id: str,
    host_original_text: str,
    host_relevant_context_trace_ids: tuple[str, ...] = (),
    authoritative_operation_catalog: tuple[dict[str, Any], ...] | None = None,
) -> RequestUnderstanding:
    """Strictly parse the versioned model output used before capability discovery."""
    if isinstance(payload, str):
        raw = _strict_json_object(payload, contract_name="request understanding")
    elif isinstance(payload, dict):
        raw = dict(payload)
    else:
        raise TypeError("payload must be dict or JSON string")
    required = {
        "schema_version", "language", "goals",
        "required_capabilities", "effect_type", "target_scope", "reversibility",
        "external_side_effect", "unresolved_capabilities", "operation_requirements",
        "current_topic", "unresolved_reference", "risk_class", "confidence", "reason_codes",
    }
    optional_fields = {"response_requirements", "execution_restriction", "execution_restriction_source"}
    if not (required <= set(raw) <= required | optional_fields):
        raise ValueError(f"request understanding fields must exactly match schema: {tuple(sorted(required))!r}")
    if raw["schema_version"] != "request_understanding.v2":
        raise ValueError("unknown request understanding schema")
    if not isinstance(raw["goals"], list) or not raw["goals"]:
        raise ValueError("goals must be a non-empty list")
    goals = tuple(Goal(goal_id=item["goal_id"], description=item["description"]) for item in raw["goals"] if isinstance(item, dict))
    if len(goals) != len(raw["goals"]):
        raise ValueError("every goal must be an object")
    raw_response_requirements = raw.get("response_requirements", [])
    if not isinstance(raw_response_requirements, list):
        raise ValueError("response_requirements must be a list")
    if any(not isinstance(item, dict) for item in raw_response_requirements):
        raise ValueError("every response requirement must be an object")
    response_requirements = tuple(
        ResponseRequirement(
            response_requirement_id=item["response_requirement_id"],
            applies_to_goal_ids=tuple(item["applies_to_goal_ids"]),
            description=str(item.get("description", "")),
            memory_query_kind=item.get("memory_query_kind"),
            subject_binding=item.get("subject_binding"),
            requirement_kind=item.get("requirement_kind"),
        )
        for item in raw_response_requirements if isinstance(item, dict)
    )
    if not isinstance(raw["required_capabilities"], list):
        raise ValueError("required_capabilities must be a list")
    authoritative_capability_ids = {
        str(item["capability_id"]) for item in (authoritative_operation_catalog or ())
    }
    required_capability_fields = {"capability_id", "purpose", "required"}
    optional_legacy_capability_fields = {
        "operation_contract_required", "unresolved_operation_reason",
    }
    for item in raw["required_capabilities"]:
        fields = set(item) if isinstance(item, dict) else set()
        valid_fields = (
            fields == required_capability_fields
            if authoritative_operation_catalog is not None
            else (
                required_capability_fields <= fields
                and fields <= required_capability_fields | optional_legacy_capability_fields
            )
        )
        if not isinstance(item, dict) or not valid_fields:
            raise ValueError(
                "required capability fields must exactly match canonical model contract"
            )
    requirements = tuple(
        CapabilityRequirement(
            capability_id=item["capability_id"], purpose=item["purpose"], required=item["required"],
            operation_contract_required=True,
            unresolved_operation_reason=(
                ""
                if authoritative_operation_catalog is not None
                and item["capability_id"] in authoritative_capability_ids
                else "authoritative_operation_not_selected"
                if authoritative_operation_catalog is not None
                else str(item.get("unresolved_operation_reason", ""))
            ),
        )
        for item in raw["required_capabilities"]
    )
    if not isinstance(raw["unresolved_capabilities"], list):
        raise ValueError("unresolved_capabilities must be a list")
    unresolved_capabilities = tuple(_require_non_empty_string(item, "unresolved_capabilities") for item in raw["unresolved_capabilities"])
    if authoritative_operation_catalog is None and not isinstance(raw["operation_requirements"], list):
        raise ValueError("operation_requirements must be a list")
    if authoritative_operation_catalog is not None and not isinstance(raw["operation_requirements"], dict):
        raise ValueError("model operation_requirements must be an operation-parameter object")
    contract_by_operation = {
        str(item["operation_id"]): item for item in (authoritative_operation_catalog or ())
    }
    operation_requirements_list = []
    if authoritative_operation_catalog is not None:
        selected_operations = raw["operation_requirements"]
        if set(selected_operations) != set(contract_by_operation):
            raise ValueError("model operation parameter IDs must exactly match authoritative operations")
        for operation_id, parameters in selected_operations.items():
            contract = contract_by_operation.get(str(operation_id))
            if contract is None:
                raise ValueError(f"operation contract not found: {operation_id}")
            if not isinstance(parameters, dict):
                raise ValueError(f"operation parameters must be an object: {operation_id}")
            required_parameters = tuple(str(item) for item in contract.get("required_parameters", ()))
            optional_parameters = tuple(str(item) for item in contract.get("optional_parameters", ()))
            if not set(required_parameters) <= set(parameters) <= set(required_parameters + optional_parameters):
                raise ValueError(f"operation parameters must exactly match contract: {operation_id}")
            normalized_parameters = tuple(
                (parameter, _normalize_operation_parameter(parameters[parameter], parameter))
                for parameter in dict.fromkeys(required_parameters + optional_parameters)
                if parameter in parameters
            )
            operation_requirements_list.append(OperationRequirement(
                capability_id=str(contract["capability_id"]),
                operation_id=str(operation_id),
                purpose=str(contract["operation_description"]),
                required_evidence=tuple(contract["evidence_kinds"]),
                effect_type=contract["effect_type"],
                target_scope=contract["target_scope"],
                reversibility=contract["reversibility"],
                external_side_effect=contract["external_side_effect"],
                risk_class=contract["risk_class"],
                required=True,
                parameters=normalized_parameters,
                declared_prerequisite_for_operation_ids=tuple(contract.get("declared_prerequisite_for_operation_ids", ())),
            ))
    for item in raw["operation_requirements"]:
        if authoritative_operation_catalog is not None:
            break
        if not isinstance(item, dict):
            continue
        operation_requirements_list.append(OperationRequirement(
            capability_id=item["capability_id"], operation_id=item["operation_id"], purpose=item["purpose"],
            required_evidence=tuple(item["required_evidence"]), effect_type=item["effect_type"],
            target_scope=item["target_scope"], reversibility=item["reversibility"],
            external_side_effect=item["external_side_effect"], risk_class=item["risk_class"],
            required=item["required"],
            declared_prerequisite_for_operation_ids=tuple(item.get("declared_prerequisite_for_operation_ids", ())),
            parameters=tuple(
                (str(key), str(value)) for key, value in item.get("parameters", {}).items()
            ),
        ))
    operation_requirements = tuple(operation_requirements_list)
    if (
        authoritative_operation_catalog is None
        and len(operation_requirements) != len(raw["operation_requirements"])
    ):
        raise ValueError("every operation requirement must be an object")
    if authoritative_operation_catalog is not None:
        selected_operation_capabilities = {
            item.capability_id for item in operation_requirements if item.required
        }
        requirement_by_capability = {
            item.capability_id: item for item in requirements if item.required
        }
        for capability_id in selected_operation_capabilities:
            requirement = requirement_by_capability.get(capability_id)
            if requirement is None:
                raise ValueError(
                    f"selected_authoritative_operation_capability_not_required:{capability_id}"
                )
            if requirement.operation_contract_required is not True:
                raise ValueError(
                    f"selected_authoritative_operation_requires_operation_contract:{capability_id}"
                )
            if requirement.unresolved_operation_reason:
                raise ValueError(
                    f"selected_authoritative_operation_cannot_be_unresolved:{capability_id}"
                )
    if not isinstance(raw["reason_codes"], list):
        raise ValueError("reason_codes must be a list")
    top_level_effect = raw["effect_type"]
    top_level_reversibility = raw["reversibility"]
    top_level_external_side_effect = raw["external_side_effect"]
    top_level_risk = raw["risk_class"]
    reason_codes = tuple(raw["reason_codes"])
    if authoritative_operation_catalog is not None and operation_requirements:
        effect_rank = {"OBSERVE": 0, "MUTATE": 1, "EXECUTE": 2, "EXPORT": 3, "PERSIST": 4, "UNKNOWN": 5}
        risk_rank = {"READ_ONLY": 0, "MUTATION": 1, "DANGEROUS": 2, "UNKNOWN": 3}
        reversibility_rank = {
            "REVERSIBLE": 0, "PARTIALLY_REVERSIBLE": 1, "IRREVERSIBLE": 2, "UNKNOWN": 3,
        }
        top_level_effect = max(
            (item.effect_type for item in operation_requirements), key=effect_rank.__getitem__,
        )
        top_level_risk = max(
            (item.risk_class for item in operation_requirements), key=risk_rank.__getitem__,
        )
        top_level_reversibility = max(
            (item.reversibility for item in operation_requirements), key=reversibility_rank.__getitem__,
        )
        top_level_external_side_effect = any(
            item.external_side_effect is True for item in operation_requirements
        )
        reason_codes = reason_codes + ("host_hydrated_top_level_contract_aggregate",)
    return RequestUnderstanding(
        request_id=host_request_id, original_text=host_original_text, language=raw["language"],
        goals=goals, required_capabilities=requirements, response_requirements=response_requirements,
        effect_type=top_level_effect,
        target_scope=raw["target_scope"], reversibility=top_level_reversibility,
        external_side_effect=top_level_external_side_effect, unresolved_capabilities=unresolved_capabilities,
        operation_requirements=operation_requirements,
        current_topic=str(raw["current_topic"]), unresolved_reference=str(raw["unresolved_reference"]),
        relevant_context_trace_ids=host_relevant_context_trace_ids,
        risk_class=top_level_risk,
        confidence=raw["confidence"],
        reason_codes=reason_codes,
        execution_restriction=str(raw.get("execution_restriction", "NONE")),
        execution_restriction_source=str(raw.get("execution_restriction_source", "")),
    )


@dataclass(frozen=True, slots=True)
class DiscoverySelection:
    selected_values: tuple[str, ...]
    discovery_complete: bool
    continuation_required: bool
    continuation_reason: str
    ambiguity_present: bool
    confidence: float
    reason_codes: tuple[str, ...]
    selection_justifications: tuple[dict[str, str], ...] = ()


def parse_discovery_selection_payload(
    payload: dict[str, Any] | str,
    *,
    value_key: str,
    allowed_values: tuple[str, ...],
    max_values_per_pass: int | None = None,
    allow_empty_complete: bool = False,
) -> DiscoverySelection:
    """Strict parser shared by typed kind and capability discovery."""
    if isinstance(payload, str):
        raw = _strict_json_object(payload, contract_name="discovery selection")
    elif isinstance(payload, dict):
        raw = dict(payload)
    else:
        raise TypeError("payload must be dict or JSON string")
    required = {
        value_key, "continuation_required", "continuation_reason",
        "ambiguity_present", "confidence", "reason_codes",
    }
    if value_key == "candidate_operation_ids":
        required.add("selection_justifications")
    if set(raw) != required:
        raise ValueError("discovery selection fields must exactly match schema")
    for field_name in ("continuation_required", "ambiguity_present"):
        if not isinstance(raw[field_name], bool):
            raise ValueError(f"{field_name} must be boolean")
    if not isinstance(raw["continuation_reason"], str):
        raise ValueError("continuation_reason must be a string")
    if raw["continuation_required"] and not raw["continuation_reason"].strip():
        raise ValueError("continuation_reason required when continuation is requested")
    selection = raw[value_key]
    if isinstance(selection, list):
        values = tuple(str(value) for value in selection)
    elif isinstance(selection, dict):
        slot_keys = tuple(f"selection_{index}" for index in range(1, 5))
        slot_encoded = value_key == "candidate_operation_ids" and set(selection) == set(slot_keys)
        if slot_encoded:
            values = tuple(
                str(selection[key]) for key in slot_keys if selection[key] is not None
            )
        else:
            if any(value is not True for value in selection.values()):
                raise ValueError(f"{value_key} values must all be true")
            values = tuple(str(value) for value in selection)
    else:
        raise ValueError(f"{value_key} must be an object or array")
    if not values:
        if raw["continuation_required"]:
            raise ValueError("discovery continuation requires at least one new ID")
        if not allow_empty_complete:
            raise ValueError(f"{value_key} must be a non-empty object")
    if max_values_per_pass is not None and len(values) > max_values_per_pass:
        raise ValueError("discovery selection exceeds per-pass maximum")
    # Continuation is bounded transport for further model discovery, never a demand to
    # fill the current pass to its maximum capacity. Monotonic progress is enforced by:
    #   - a non-empty selection whenever continuation_required (above);
    #   - the caller's remaining-scope loop removing already-selected IDs;
    #   - the caller's strictly bounded pass count.
    if len(values) != len(set(values)):
        raise ValueError("discovery selection contains duplicate IDs")
    allowed = set(allowed_values)
    if any(value not in allowed for value in values):
        raise ValueError("discovery returned unregistered value")
    reasons = _require_string_list(raw["reason_codes"], "reason_codes")
    justifications: tuple[dict[str, str], ...] = ()
    if value_key == "candidate_operation_ids":
        raw_justifications = raw["selection_justifications"]
        if not isinstance(raw_justifications, dict):
            raise ValueError("selection_justifications must be an object")
        if set(raw_justifications) != set(values):
            raise ValueError("operation selection justification coverage mismatch")
        normalized: list[dict[str, str]] = []
        for operation_id in values:
            item = raw_justifications[operation_id]
            if not isinstance(item, dict) or set(item) != {
                "justification_kind", "source_grounding", "goal_id",
            }:
                raise ValueError("operation selection justification fields invalid")
            kind = _require_non_empty_string(item["justification_kind"], "justification_kind")
            if kind not in {"DIRECT_GOAL_EFFECT", "DECLARED_OPERATION_DEPENDENCY"}:
                raise ValueError("unknown operation selection justification kind")
            normalized.append({
                "operation_id": operation_id,
                "goal_id": _require_non_empty_string(item["goal_id"], "goal_id"),
                "justification_kind": kind,
                "source_grounding": _require_non_empty_string(item["source_grounding"], "source_grounding"),
            })
        justifications = tuple(normalized)
    return DiscoverySelection(
        selected_values=values,
        discovery_complete=not raw["continuation_required"],
        continuation_required=raw["continuation_required"],
        continuation_reason=raw["continuation_reason"],
        ambiguity_present=raw["ambiguity_present"],
        confidence=_normalize_confidence(raw["confidence"]),
        reason_codes=reasons,
        selection_justifications=justifications,
    )
