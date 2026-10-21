from __future__ import annotations

from MAKSIMAR_CORE_LIB.ai_orchestration.semantic_intent_contract import (response_subject_binding_schema, response_requirement_semantics_schema, response_subject_constraints_schema, hydrate_response_requirements, validate_response_obligation_coverage, UnderstandingAttemptPolicy, validate_source_candidate_verdict)

from MAKSIMAR_CORE_LIB.memory_engine.history_ingestion.jarvis_history_query_models import MEMORY_FILTER_SCHEMA, validate_memory_filter

"""Canonical general semantic spine for conversation and project turns."""

import json
import hashlib
from math import ceil
from functools import lru_cache
from dataclasses import replace
from typing import Any, Iterator
from uuid import uuid4

from MAKSIMAR_CORE_LIB.ai_orchestration.helper_model_decision_parser import (
    RepairableHelperCorrectionContradiction,
    normalize_input_text,
    parse_discovery_selection_payload,
    parse_helper_input_correction_payload,
    parse_request_understanding_payload,
)
from MAKSIMAR_CORE_LIB.ai_orchestration.model_profile_registry_contract import (
    context_tokens_for_jarvis_model,
    resident_context_tokens_for_jarvis_model,
)
from MAKSIMAR_SERVER.AI_ORCHESTRATION.ollama_transport import (
    HELPER_INPUT_CORRECTION_MODEL_ID,
    MODEL_CONTEXT_AUTHORITY_SOURCE,
    PRIMARY_CONVERSATION_MODEL_ID,
    REQUEST_UNDERSTANDING_NUM_CTX,
    REQUEST_UNDERSTANDING_NUM_PREDICT,
    OPERATION_DISCOVERY_NUM_PREDICT,
)
from MAKSIMAR_CORE_LIB.ai_orchestration.semantic_intent_contract import (
    CapabilityCandidate,
    ConversationPort,
    EvidenceBundle,
    EvidenceItem,
    ExecutionReceipt,
    ExecutionPlan,
    FinalBrainPort,
    IdentityContext,
    ModelUnderstandingPort,
    OrchestrationTrace,
    PermissionEvaluationPort,
    PlanStep,
    ProjectUnderstandingPort,
    RequestDeadline,
    RequestUnderstanding,
    utc_observed_at,
)
from MAKSIMAR_CORE_LIB.capability_registry.capability_registry_loader import (
    discover_capability_providers,
    discover_projected_capability_providers,
    load_capability_manifests,
    project_semantic_capability_index,
    project_semantic_operation_catalog,
    select_semantic_projection_details,
    validate_semantic_capability_projection,
    validate_operation_dependency_references,
)
from MAKSIMAR_CORE_LIB.security_layer.semantic_policy import validate_structured_safety
from MAKSIMAR_CORE_LIB.security_layer.host_approval_handshake import (
    CANONICAL_HOST_APPROVAL_STORE,
)
from MAKSIMAR_SERVER.OBSERVABILITY.jarvis_live.jarvis_live_observability_read_model import trace_stage


MINIMUM_UNDERSTANDING_CONFIDENCE = 0.70
REQUEST_UNDERSTANDING_RESERVED_OUTPUT_TOKENS = REQUEST_UNDERSTANDING_NUM_PREDICT
CANDIDATE_DISCOVERY_RESERVED_OUTPUT_TOKENS = 256
OPERATION_DISCOVERY_RESERVED_OUTPUT_TOKENS = OPERATION_DISCOVERY_NUM_PREDICT
# Candidate/operation discovery is served by the compact CHAT-role call in
# ``ExistingOllamaModelUnderstandingAdapter.discover_candidates``.  Keep its
# prompt-budget authority aligned with that transport request; the larger
# structured understanding context remains reserved for ``_understand``.
SEMANTIC_SELECTION_NUM_CTX = resident_context_tokens_for_jarvis_model(PRIMARY_CONVERSATION_MODEL_ID)
PROMPT_SAFETY_MARGIN_TOKENS = 96
UNKNOWN_SCHEMA_CONTEXT_RESERVE_TOKENS = 64
DISCOVERY_VALUES_PER_PASS = 4
CANONICAL_TURN_TIMEOUT_SECONDS = 420.0


@lru_cache(maxsize=1)
def _load_manifest_operation_catalog() -> tuple[dict[str, Any], ...]:
    """Build the runtime operation cache solely from versioned capability manifests."""
    catalog: list[dict[str, Any]] = []
    for manifest in load_capability_manifests():
        for contract in manifest["operation_contracts"]:
            catalog.append({
                "capability_id": manifest["id"],
                "provider_id": manifest["provider"],
                "operation_id": contract["operation_id"],
                "description": contract["description"],
                "required_parameters": tuple(contract["required_parameters"]),
                "evidence_kinds": tuple(contract["evidence_kinds"]),
                "effect_type": contract["effect_type"], "target_scope": contract["target_scope"],
                "reversibility": contract["reversibility"],
                "external_side_effect": contract["external_side_effect"], "risk_class": contract["risk_class"],
                "manifest_version": manifest["version"],
            })
    return tuple(catalog)


def load_operation_catalog(
    registry_projection: dict[str, Any] | None = None,
) -> tuple[dict[str, Any], ...]:
    if registry_projection is None:
        return _load_manifest_operation_catalog()
    return tuple(dict(item) for item in project_semantic_operation_catalog(registry_projection))


def operation_contract(
    operation_id: str, registry_projection: dict[str, Any] | None = None,
) -> dict[str, Any] | None:
    return next((item for item in load_operation_catalog(registry_projection) if item["operation_id"] == operation_id), None)


def _operation_schema() -> dict[str, Any]:
    return {
        "type": "object", "additionalProperties": False,
        "required": [
            "capability_id", "operation_id", "purpose", "required_evidence",
            "effect_type", "target_scope", "reversibility", "external_side_effect",
            "risk_class", "required",
        ],
        "properties": {
            "capability_id": {"type": "string"}, "operation_id": {"type": "string"}, "purpose": {"type": "string"},
            "required_evidence": {"type": "array", "minItems": 1, "items": {"type": "string"}},
            "effect_type": {"type": "string", "enum": ["OBSERVE", "MUTATE", "EXECUTE", "EXPORT", "PERSIST", "UNKNOWN"]},
            "target_scope": {"type": "string"},
            "reversibility": {"type": "string", "enum": ["REVERSIBLE", "PARTIALLY_REVERSIBLE", "IRREVERSIBLE", "UNKNOWN"]},
            "external_side_effect": {"enum": [True, False, None]},
            "risk_class": {"type": "string", "enum": ["READ_ONLY", "MUTATION", "DANGEROUS", "UNKNOWN"]},
            "required": {"type": "boolean"},
        },
    }


REQUEST_UNDERSTANDING_JSON_SCHEMA: dict[str, Any] = {
    "type": "object", "additionalProperties": False,
    "required": [
        "schema_version", "language", "goals", "required_capabilities",
        "effect_type", "target_scope", "reversibility", "external_side_effect", "unresolved_capabilities",
        "operation_requirements", "current_topic", "unresolved_reference", "risk_class", "confidence", "reason_codes",
    ],
    "properties": {
        "schema_version": {"type": "string", "const": "request_understanding.v2"},
        "language": {"type": "string"},
        "goals": {"type": "array", "minItems": 1, "items": {"type": "object", "additionalProperties": False,
            "required": ["goal_id", "description"], "properties": {"goal_id": {"type": "string"}, "description": {"type": "string"}}}},
        "required_capabilities": {"type": "array", "minItems": 1, "items": {"type": "object", "additionalProperties": False,
            "required": ["capability_id", "purpose", "required", "operation_contract_required", "unresolved_operation_reason"],
            "properties": {"capability_id": {"type": "string"}, "purpose": {"type": "string"},
                "required": {"type": "boolean"}, "operation_contract_required": {"type": "boolean"},
                "unresolved_operation_reason": {"type": "string"}}}},
        "response_requirements": {"type": "array", "items": {"type": "object", "additionalProperties": False,
            "required": ["response_requirement_id", "applies_to_goal_ids"],
            "properties": {"response_requirement_id": {"type": "string"},
                "applies_to_goal_ids": {"type": "array", "minItems": 1, "items": {"type": "string"}},
                "description": {"type": "string"},
                "memory_query_kind": {"anyOf": [{"type": "null"}, json.loads(json.dumps(MEMORY_FILTER_SCHEMA["properties"]["query_kind"]))]}, "subject_binding": response_subject_binding_schema(), "requirement_kind": response_requirement_semantics_schema()["properties"]["requirement_kind"]}, "anyOf": response_requirement_semantics_schema()["anyOf"]}},
        "effect_type": {"type": "string", "enum": ["OBSERVE", "MUTATE", "EXECUTE", "EXPORT", "PERSIST", "UNKNOWN"]},
        "target_scope": {"type": "string"}, "reversibility": {"type": "string", "enum": ["REVERSIBLE", "PARTIALLY_REVERSIBLE", "IRREVERSIBLE", "UNKNOWN"]},
        "external_side_effect": {"enum": [True, False, None]}, "unresolved_capabilities": {"type": "array", "items": {"type": "string"}},
        "operation_requirements": {"type": "array", "items": _operation_schema()},
        "current_topic": {"type": "string"}, "unresolved_reference": {"type": "string"},
        "risk_class": {"type": "string", "enum": ["READ_ONLY", "MUTATION", "DANGEROUS", "UNKNOWN"]},
        "confidence": {"type": "number", "minimum": 0, "maximum": 1},
        "reason_codes": {"type": "array", "items": {"type": "string"}},
        "execution_restriction": {"type": "string", "enum": ["NONE", "NO_EXECUTE", "PREPARE_ONLY"]},
        "execution_restriction_source": {"type": "string"},
    },
}


REQUEST_UNDERSTANDING_JSON_SCHEMA["properties"]["response_requirements"]["items"] = response_requirement_semantics_schema(
    base_schema=REQUEST_UNDERSTANDING_JSON_SCHEMA["properties"]["response_requirements"]["items"])


# Provider-neutral logical automation spec parameter (model-side). The trigger and each
# step carry a semantic catalog_query; the model must NOT emit installed node types,
# versions, resource enums, or credential IDs.


# Shared typed response/operation contracts own the provider-neutral DAG grammar.
from MAKSIMAR_CORE_LIB.ai_orchestration.semantic_intent_contract import (
    _logical_step_item_schema, _LOGICAL_SPEC_PARAMETER_SCHEMA,
)


def request_understanding_schema_for_projection(
    registry_projection: dict[str, Any] | None, *, source_text: str = "",
) -> dict[str, Any]:
    """Bind model output IDs to the exact authoritative projection for this call."""
    schema = json.loads(json.dumps(REQUEST_UNDERSTANDING_JSON_SCHEMA))
    if registry_projection is None:
        return schema
    capability_ids = tuple(
        str(item["capability_id"]) for item in registry_projection.get("entries", ())
    )
    projected_entries = tuple(registry_projection.get("entries", ()))
    operation_catalog = load_operation_catalog(registry_projection)
    operation_ids = tuple(dict.fromkeys(str(item["operation_id"]) for item in operation_catalog))
    if operation_catalog:
        effect_rank = {"OBSERVE": 0, "MUTATE": 1, "EXECUTE": 2, "EXPORT": 3, "PERSIST": 4, "UNKNOWN": 5}
        risk_rank = {"READ_ONLY": 0, "MUTATION": 1, "DANGEROUS": 2, "UNKNOWN": 3}
        reversibility_rank = {
            "REVERSIBLE": 0, "PARTIALLY_REVERSIBLE": 1, "IRREVERSIBLE": 2, "UNKNOWN": 3,
        }
        schema["properties"]["effect_type"] = {"type": "string", "const": max(
            (str(item["effect_type"]) for item in operation_catalog), key=effect_rank.__getitem__,
        )}
        schema["properties"]["risk_class"] = {"type": "string", "const": max(
            (str(item["risk_class"]) for item in operation_catalog), key=risk_rank.__getitem__,
        )}
        schema["properties"]["reversibility"] = {"type": "string", "const": max(
            (str(item["reversibility"]) for item in operation_catalog), key=reversibility_rank.__getitem__,
        )}
        schema["properties"]["external_side_effect"] = {
            "const": any(item.get("external_side_effect") is True for item in operation_catalog),
        }
        target_scopes = {str(item["target_scope"]) for item in operation_catalog}
        if len(target_scopes) == 1:
            schema["properties"]["target_scope"] = {"type": "string", "const": next(iter(target_scopes))}
    capabilities = schema["properties"]["required_capabilities"]
    capabilities["minItems"] = len(capability_ids)
    capabilities["maxItems"] = len(capability_ids)
    capabilities["uniqueItems"] = True
    capabilities["description"] = (
        "Smallest sufficient required set from the selected authoritative projection."
    )
    capability_properties = capabilities["items"]["properties"]
    capabilities["items"]["required"] = ["capability_id", "purpose", "required"]
    capability_properties.pop("operation_contract_required", None)
    capability_properties.pop("unresolved_operation_reason", None)
    capability_properties["capability_id"]["enum"] = list(capability_ids)
    # Every capability in the authoritative operation projection is host-selected and
    # required; the model must list each exactly once with required=true so its
    # operation_requirements stay consistent with the authoritative operation catalog.
    capability_properties["required"] = {"type": "boolean", "const": True}
    capability_properties["purpose"]["maxLength"] = 96
    unresolved = schema["properties"]["unresolved_capabilities"]
    unresolved["maxItems"] = len(capability_ids)
    unresolved["uniqueItems"] = True
    unresolved["items"]["enum"] = list(capability_ids)
    if projected_entries and all(
        item.get("execution_contract_available") is True for item in projected_entries
    ):
        unresolved["maxItems"] = 0
    operation_parameter_properties: dict[str, Any] = {}
    for operation in operation_catalog:
        required_parameters = tuple(str(item) for item in operation.get("required_parameters", ()))
        if "memory_filter" in operation.get("parameter_schemas", {}) and _canonical_memory_filter(registry_projection) is not None:
            required_parameters = tuple(dict.fromkeys((*required_parameters, "memory_filter")))
        properties: dict[str, Any] = {}
        optional_parameters = tuple(str(item) for item in operation.get("optional_parameters", ()))
        for parameter in dict.fromkeys(required_parameters + optional_parameters):
            if parameter in operation.get("parameter_schemas", {}):
                properties[parameter] = json.loads(json.dumps(operation["parameter_schemas"][parameter]))
                if parameter == "memory_filter":
                    canonical_filter = _canonical_memory_filter(registry_projection)
                    if canonical_filter is not None:
                        properties[parameter]["const"] = canonical_filter
            elif parameter == "logical_spec":
                logical_schema = json.loads(json.dumps(_LOGICAL_SPEC_PARAMETER_SCHEMA))
                artifact_requirements = tuple(
                    item for item in registry_projection.get(
                        "selection_artifact_operation_requirements", ()
                    ) if isinstance(item, dict) and item.get("requirement_id")
                )
                artifact_requirement_ids = tuple(
                    str(item["requirement_id"]) for item in artifact_requirements
                )
                semantic_schema = logical_schema["properties"]["semantic_requirements"]
                semantic_schema["items"] = {
                    "type": "object", "additionalProperties": False,
                    "required": ["requirement_id", "step_id"],
                    "properties": {
                        "requirement_id": {"type": "string", "enum": list(artifact_requirement_ids)},
                        "step_id": {"type": "string", "minLength": 1, "maxLength": 48},
                    },
                }
                semantic_schema["minItems"] = len(artifact_requirement_ids)
                semantic_schema["maxItems"] = len(artifact_requirement_ids)
                if artifact_requirement_ids:
                    logical_schema["required"] = list(dict.fromkeys([
                        *logical_schema["required"], "semantic_requirements",
                    ]))
                bridge_capability_ids = tuple(
                    capability_id for capability_id in capability_ids
                    if capability_id not in {"workflow_automation:n8n", "conversation.respond"}
                )
                step_variants = logical_schema["properties"]["steps"]["items"]["oneOf"]
                artifact_operation_classes = {
                    str(item.get("operation_class", "")) for item in artifact_requirements
                }
                installed_operation_ids: list[str] = []
                installed_catalog_requirement_count = 0
                if artifact_requirements:
                    from MAKSIMAR_SERVER.AI_ORCHESTRATION.n8n_logical_compiler import (
                        installed_provider_operation_ids,
                    )
                    for item in artifact_requirements:
                        provider_name = str(item.get("provider_name", "")).strip()
                        if provider_name:
                            provider_operation_ids = installed_provider_operation_ids(provider_name)
                            installed_operation_ids.extend(provider_operation_ids)
                            if provider_operation_ids:
                                installed_catalog_requirement_count += 1
                if installed_operation_ids:
                    catalog_variant = next(
                        item for item in step_variants
                        if item.get("properties", {}).get("action", {}).get("const") == "catalog_query"
                    )
                    catalog_variant["properties"]["semantic_operation"] = {
                        "type": "string", "enum": list(dict.fromkeys(installed_operation_ids)),
                        "description": "Exact operation ID from bounded installed provider contracts.",
                    }
                    canonical_provider_names = tuple(dict.fromkeys(
                        str(item.get("provider_name", "")).strip()
                        for item in artifact_requirements if str(item.get("provider_name", "")).strip()
                    ))
                    if canonical_provider_names:
                        catalog_variant["properties"]["provider_name"] = {
                            "type": "string", "enum": list(canonical_provider_names),
                            "description": "Canonical provider constraint from the source operation requirement.",
                        }
                    if installed_catalog_requirement_count == len(artifact_requirements):
                        logical_schema["properties"]["steps"].update({
                            "contains": {
                                "type": "object", "required": ["action"],
                                "properties": {"action": {"const": "catalog_query"}},
                            },
                            "minContains": installed_catalog_requirement_count,
                            "maxContains": installed_catalog_requirement_count,
                        })
                if artifact_requirements:
                    permitted_intrinsic_actions: set[str] = set()
                    if "ASSIGN" in artifact_operation_classes:
                        permitted_intrinsic_actions.add("set_field")
                    if "TRANSFORM" in artifact_operation_classes:
                        permitted_intrinsic_actions.add("transform")
                    step_variants[:] = [
                        item for item in step_variants
                        if item.get("properties", {}).get("action", {}).get("const")
                        not in {"set_field", "transform"} - permitted_intrinsic_actions
                    ]
                source_has_http_endpoint = any(
                    token.strip("()[]{}<>,.;'\"").casefold().startswith(("http://", "https://"))
                    for token in source_text.split()
                )
                if not source_has_http_endpoint:
                    step_variants[:] = [
                        item for item in step_variants
                        if item.get("properties", {}).get("action", {}).get("const") != "http_request"
                    ]
                jarvis_variant = next(
                    (item for item in step_variants
                     if item.get("properties", {}).get("action", {}).get("const") == "jarvis_capability"),
                    None,
                )
                if not bridge_capability_ids:
                    logical_schema["properties"]["steps"]["items"]["oneOf"] = [
                        item for item in step_variants if item is not jarvis_variant
                    ]
                elif jarvis_variant is not None:
                    jarvis_variant["properties"]["capability_id"]["enum"] = list(bridge_capability_ids)
                # Ollama's JSON grammar does not enforce array uniqueness while its
                # post-generation validator does. Repeated enum members are transport
                # noise, not additional semantic constraints; admit them here and
                # canonicalize to a set before strict host parsing below.
                logical_schema["properties"]["constraints"].pop("uniqueItems", None)
                properties[parameter] = logical_schema
            else:
                properties[parameter] = {
                    "type": "string", "minLength": 1, "maxLength": 512,
                    "description": (
                        "The exact literal parameter value extracted from the request: a number, a "
                        "scenario name, a path, or the requested text. Never a placeholder, sentence, "
                        "prefix, or commentary."
                    ),
                }
        parameter_schema: dict[str, Any] = {
            "type": "object",
            "additionalProperties": False,
            "properties": properties,
            "required": list(required_parameters),
        }
        if not properties:
            parameter_schema["maxProperties"] = 0
        operation_parameter_properties[str(operation["operation_id"])] = parameter_schema
    schema["properties"]["operation_requirements"] = {
        "type": "object",
        "additionalProperties": False,
        "minProperties": len(operation_ids),
        "maxProperties": len(operation_ids),
        "required": list(operation_ids),
        "description": (
            "Exact literal parameter values extracted from the request for every operation already "
            "selected by the same model discovery stage; never a placeholder, prose, prefix, or "
            "commentary. The host owns operation IDs and hydrates all authoritative contract metadata."
        ),
        "properties": operation_parameter_properties,
    }
    goals = schema["properties"]["goals"]["items"]["properties"]
    goals["goal_id"]["maxLength"] = 64
    goals["description"]["maxLength"] = 160
    schema["properties"]["language"]["maxLength"] = 16
    schema["properties"]["target_scope"]["maxLength"] = 96
    schema["properties"]["current_topic"]["maxLength"] = 80
    schema["properties"]["unresolved_reference"]["maxLength"] = 96
    schema["properties"]["reason_codes"]["maxItems"] = 3
    schema["properties"]["reason_codes"]["items"]["maxLength"] = 64
    schema["properties"]["confidence"]["description"] = (
        "Confidence in the final semantic interpretation, not STT, channel or helper confidence."
    )
    # Registry IDs and contract aggregates are already selected and justified by prior
    # typed stages. They are host-hydrated after this call; asking the model to echo them
    # creates a second selection surface and wastes the semantic/topology budget.
    host_hydrated = {
        "required_capabilities", "effect_type", "target_scope", "reversibility",
        "external_side_effect", "unresolved_capabilities", "risk_class", "goals",
        "execution_restriction", "execution_restriction_source",
    }
    for field in host_hydrated:
        schema["properties"].pop(field, None)
    schema["required"] = [
        field for field in schema["required"] if field not in host_hydrated
    ]
    if "selection_response_requirements" in registry_projection:
        schema["properties"].pop("response_requirements", None)
        schema["required"] = [field for field in schema["required"] if field != "response_requirements"]
    elif "response_requirements" not in schema["required"]:
        schema["required"].append("response_requirements")
    return schema


KIND_DISCOVERY_JSON_SCHEMA: dict[str, Any] = {
    "type": "object", "additionalProperties": False,
    "required": ["candidate_kinds", "continuation_required", "continuation_reason",
                 "ambiguity_present", "confidence", "reason_codes"],
    "properties": {
        "candidate_kinds": {
            "type": "object", "minProperties": 0, "maxProperties": DISCOVERY_VALUES_PER_PASS,
            "additionalProperties": {"type": "boolean", "const": True},
            "description": (
                "Smallest sufficient set of new registered semantic kinds encoded as unique JSON keys whose values "
                "are true. No key may come from host-owned already_selected_ids. When no kind in this exact scope is "
                "relevant, return an empty object with continuation_required=false."
            ),
        },
        "continuation_required": {
            "type": "boolean",
            "description": (
                "True only when a distinct explicit user goal remains unsatisfied after these kinds; false when the "
                "selected kinds suffice. Never continue to exhaust the domains."
            ),
        },
        "continuation_reason": {
            "type": "string", "maxLength": 160,
            "description": "Exact distinct explicit unsatisfied goal when continuing, otherwise empty.",
        },
        "ambiguity_present": {"type": "boolean"},
        "confidence": {"type": "number", "minimum": 0, "maximum": 1},
        "reason_codes": {
            "type": "array", "minItems": 1, "maxItems": 4,
            "items": {"type": "string", "maxLength": 64},
        },
    },
}


CANDIDATE_DISCOVERY_JSON_SCHEMA: dict[str, Any] = {
    "type": "object", "additionalProperties": False,
    "required": ["candidate_capability_ids", "continuation_required", "continuation_reason",
                 "ambiguity_present", "confidence", "reason_codes"],
    "properties": {
        "candidate_capability_ids": {
            "type": "object", "minProperties": 0, "maxProperties": DISCOVERY_VALUES_PER_PASS,
            "additionalProperties": {"type": "boolean", "const": True},
            "description": (
                "Smallest sufficient set of new registered capability IDs encoded as unique JSON keys whose values "
                "are true. No key may come from host-owned already_selected_ids. When no capability in this exact "
                "scope is relevant, return an empty object with continuation_required=false."
            ),
        },
        "continuation_required": {
            "type": "boolean",
            "description": (
                "True only when a distinct explicit user goal remains unsatisfied after these IDs; false when the "
                "selected authoritative contracts suffice. Never continue to exhaust the catalog."
            ),
        },
        "continuation_reason": {
            "type": "string", "maxLength": 160,
            "description": "Exact distinct explicit unsatisfied goal when continuing, otherwise empty.",
        },
        "ambiguity_present": {"type": "boolean"},
        "confidence": {"type": "number", "minimum": 0, "maximum": 1},
        "reason_codes": {
            "type": "array", "minItems": 1, "maxItems": 4,
            "items": {"type": "string", "maxLength": 64},
        },
    },
}


OPERATION_DISCOVERY_JSON_SCHEMA: dict[str, Any] = {
    "type": "object", "additionalProperties": False,
    "required": ["candidate_operation_ids", "selection_justifications", "continuation_required",
                 "continuation_reason", "ambiguity_present", "confidence", "reason_codes"],
    "properties": {
        "candidate_operation_ids": {
            "type": "object", "minProperties": 0, "maxProperties": DISCOVERY_VALUES_PER_PASS,
            "additionalProperties": {"type": "boolean", "const": True},
            "description": (
                "Smallest sufficient new authoritative operation set. If prior selections already satisfy every "
                "explicit goal, return an empty object with continuation_required=false."
            ),
        },
        "selection_justifications": {
            "type": "object", "minProperties": 0,
            "maxProperties": DISCOVERY_VALUES_PER_PASS, "additionalProperties": False,
            "description": "Exactly one typed, source-grounded justification per selected operation.",
        },
        "continuation_required": {"type": "boolean"},
        "continuation_reason": {"type": "string", "maxLength": 160},
        "ambiguity_present": {"type": "boolean"},
        "confidence": {"type": "number", "minimum": 0, "maximum": 1},
        "reason_codes": {
            "type": "array", "minItems": 1, "maxItems": 4,
            "items": {"type": "string", "maxLength": 64},
        },
    },
}


# --- GoalFrame v3: intent (understanding) is separated from technical binding. ---
# The semantic domain and effect intent are DERIVED from the SAME registry metadata
# (operation target_scope / effect_type); they are not a second registry or router.

EFFECT_DANGER_ORDER: dict[str, int] = {"OBSERVE": 0, "MUTATE": 1, "EXECUTE": 2}


def _effect_danger(effect_type: str) -> int:
    return EFFECT_DANGER_ORDER.get(effect_type, 2)  # unknown => most dangerous (fail-safe)


def semantic_domain_of_scope(target_scope: str) -> str:
    """Derive the semantic domain from the registry target_scope naming (one source of truth)."""
    if target_scope == "bounded_same_identity_session":
        return "conversation"
    if target_scope in ("local_project_worktree", "local_project_runtime"):
        return "project"
    if target_scope.startswith("local_memory") or target_scope in ("local_session_history", "local_project_history"):
        return "memory"
    if target_scope == "local_retrieval_runtime":
        return "retrieval"
    if target_scope == "local_simulation_runtime":
        return "simulation"
    if target_scope == "local_workflow_automation":
        return "automation"
    if target_scope in ("owner_windows_desktop", "owner_windows_screen"):
        return "windows"
    if target_scope == "provided_task_context":
        return "code"
    if target_scope == "provided_content_context":
        return "content"
    if target_scope == "local_media_file":
        return "media"
    if target_scope in ("localhost_browser_dom", "public_browser_dom"):
        return "browser"
    if target_scope.startswith("local_runtime") or target_scope == "localhost_windows_edge":
        return "runtime"
    return "runtime"


_SEMANTIC_DOMAIN_SCOPES: dict[str, frozenset[str]] = {
    "conversation": frozenset({"bounded_same_identity_session"}),
    "project": frozenset({"local_project_worktree", "local_project_runtime"}),
    "memory": frozenset({"local_memory_domains", "local_memory_registry", "local_memory_runtime",
                         "local_session_history", "local_project_history"}),
    "retrieval": frozenset({"local_retrieval_runtime", "local_memory_runtime"}),
    "simulation": frozenset({"local_simulation_runtime"}),
    "automation": frozenset({"local_workflow_automation"}),
    "windows": frozenset({"owner_windows_desktop", "owner_windows_screen"}),
    "code": frozenset({"provided_task_context"}),
    "content": frozenset({"provided_content_context"}),
    "media": frozenset({"local_media_file"}),
    "browser": frozenset({"localhost_browser_dom", "public_browser_dom"}),
    "runtime": frozenset({"local_runtime", "local_runtime_library", "local_runtime_tooling",
                          "localhost_windows_edge"}),
}

SEMANTIC_EFFECT_INTENTS: dict[str, frozenset[str]] = {
    "observe": frozenset({"OBSERVE"}),
    "change_state": frozenset({"MUTATE"}),
    "retrieve": frozenset({"OBSERVE"}),
    "reason_propose": frozenset({"OBSERVE"}),
    "compute_run": frozenset({"EXECUTE"}),
}

SEMANTIC_DOMAIN_MEANINGS: dict[str, str] = {
    "conversation": "talking using supplied facts (respond only); searching persisted past conversation records belongs to memory retrieve",
    "project": "the local project files/worktree",
    "memory": "persisted conversation/history, qualified experiences and indexed source-document knowledge; derived archive/index state includes original source path, source/index SHA and freshness readback; direct file contents/worktree operations remain in project",
    "retrieval": "retrieve knowledge or inspect retrieval/vector backend availability; changing an index is memory change_state",
    "simulation": "run simulations / workers",
    "automation": "create/modify/run/inspect a local workflow automation (n8n)",
    "windows": "control or observe the Windows desktop, including the browser application/window itself; not web-page content",
    "code": "analyze software code or generate a bounded code/patch proposal",
    "content": "create or transform user-facing content such as short videos, scripts, titles, descriptions, or hashtags",
    "media": "inspect or transform an already-existing local image, video, or audio file",
    "browser": "read and interact with bounded web-page content (DOM), identified by a page, URL, link, title, form, or page text; never launch/focus the desktop browser application/window",
    "runtime": "local runtime/library/tooling state",
}

SEMANTIC_EFFECT_MEANINGS: dict[str, str] = {
    "observe": "read/see without changing anything",
    "change_state": "change something (volume, text, browser, desktop)",
    "retrieve": "find prior recorded knowledge",
    "reason_propose": "reason or produce a proposal (no change)",
    "compute_run": "execute a computation/simulation",
}

GOAL_ROLES = ("PRIMARY_OUTCOME", "SUBGOAL")
SUBGOAL_JUSTIFICATION_KINDS = ("NONE", "EXPLICIT_INTERMEDIATE", "OPERATION_DEPENDENCY")
ARTIFACT_OPERATION_CLASSES = (
    "ASSIGN", "TRANSFORM", "FETCH", "GENERATE", "PUBLISH", "SEND", "RECORD", "STORE",
    "TRANSCRIBE", "SYNTHESIZE", "RENDER", "SEARCH", "DELEGATE", "OBSERVE", "ACT",
)


def _artifact_operation_requirement_schema() -> dict[str, Any]:
    return {
        "type": "object", "additionalProperties": False,
        "required": [
            "requirement_id", "operation_class", "source_grounding", "provider_name",
            "provider_provenance", "provider_inference_justification",
        ],
        "properties": {
            "requirement_id": {"type": "string", "minLength": 1, "maxLength": 48},
            "operation_class": {"type": "string", "enum": list(ARTIFACT_OPERATION_CLASSES)},
            "source_grounding": {"type": "string", "minLength": 1, "maxLength": 160},
            "provider_name": {
                "type": "string", "maxLength": 120,
                "description": "Actual provider/service name, never a provenance enum or placeholder.",
            },
            "provider_provenance": {
                "type": "string", "enum": ["NONE", "SOURCE_EXPLICIT", "SEMANTIC_INFERENCE"],
            },
            "provider_inference_justification": {"type": "string", "maxLength": 200},
        },
    }


def _goalframe_item_schema(role: str) -> dict[str, Any]:
    properties: dict[str, Any] = {
        "goal_id": {"type": "string", "enum": ["g1", "g2", "g3", "g4"]},
        "semantic_domain": {"type": "string", "enum": list(_SEMANTIC_DOMAIN_SCOPES)},
        "effect_intent": {"type": "string", "enum": list(SEMANTIC_EFFECT_INTENTS)},
        "memory_filter": {"anyOf": [{"type": "null"}, json.loads(json.dumps(MEMORY_FILTER_SCHEMA))]},
        "subject_constraints": response_subject_constraints_schema(),
        "requested_outcome": {"type": "string"}, "grounding": {"type": "string"},
        "ambiguity": {"type": "string"}, "goal_role": {"type": "string", "const": role},
        "parent_goal_id": ({"type": "null"} if role == "PRIMARY_OUTCOME" else
                           {"type": "string", "enum": ["g1", "g2", "g3", "g4"]}),
        "subgoal_justification_kind": ({"type": "string", "const": "NONE"} if role == "PRIMARY_OUTCOME" else
            {"type": "string", "enum": ["EXPLICIT_INTERMEDIATE", "OPERATION_DEPENDENCY"]}),
    }
    schema = {"type": "object", "additionalProperties": False,
              "required": [key for key in properties if key not in ("memory_filter", "subject_constraints")], "properties": properties}
    # Encode the same relation already enforced by typed provenance validation.
    # Invalid observe + historical filter pairs must not be generated as valid JSON.
    nonhistorical = json.loads(json.dumps(schema))
    nonhistorical["properties"]["memory_filter"] = {"type": "null"}
    historical = json.loads(json.dumps(schema))
    historical["properties"]["semantic_domain"] = {"type": "string", "const": "memory"}
    historical["properties"]["effect_intent"] = {"type": "string", "const": "retrieve"}
    historical["properties"]["memory_filter"] = json.loads(json.dumps(MEMORY_FILTER_SCHEMA))
    historical["required"].append("memory_filter")
    schema["anyOf"] = [nonhistorical, historical]
    return schema


GOALFRAME_UNDERSTANDING_JSON_SCHEMA: dict[str, Any] = {
    "type": "object", "additionalProperties": False,
    "required": ["goals", "execution_restriction", "execution_restriction_source", "response_requirements"],
    "properties": {
        "response_requirements": {"type": "array", "items": {
            "type": "object", "additionalProperties": False, "required": ["applies_to_goal_ids", "description", "memory_query_kind", "requirement_kind"],
            "properties": {"applies_to_goal_ids": {"type": "array", "minItems": 1,
                "items": json.loads(json.dumps(_goalframe_item_schema("PRIMARY_OUTCOME")["properties"]["goal_id"]))},
                           "description": {"type": "string"},
                           "memory_query_kind": {"anyOf": [{"type": "null"}, json.loads(json.dumps(MEMORY_FILTER_SCHEMA["properties"]["query_kind"]))]}, "subject_binding": response_subject_binding_schema(), "requirement_kind": response_requirement_semantics_schema()["properties"]["requirement_kind"]}, "anyOf": response_requirement_semantics_schema(native=True)["anyOf"],
        }},
        "execution_restriction": {
            "type": "string", "enum": ["NONE", "NO_EXECUTE", "PREPARE_ONLY"],
        },
        "execution_restriction_source": {"type": "string"},
        "goals": {
            "type": "array", "minItems": 1, "maxItems": 4,
            "items": {"oneOf": [
                _goalframe_item_schema("PRIMARY_OUTCOME"), _goalframe_item_schema("SUBGOAL"),
            ]},
        },
    },
}

ARTIFACT_OPERATION_EXTRACTION_JSON_SCHEMA: dict[str, Any] = {
    "type": "object", "additionalProperties": False,
    "required": ["artifact_operation_requirements"],
    "properties": {
        "artifact_operation_requirements": {
            "type": "array", "maxItems": 12,
            "items": {
                "type": "object", "additionalProperties": False,
                "required": ["goal_id", *_artifact_operation_requirement_schema()["required"]],
                "properties": {
                    "goal_id": {"type": "string", "minLength": 1, "maxLength": 48},
                    **_artifact_operation_requirement_schema()["properties"],
                },
            },
        },
    },
}


def _compact_global_projection(registry_projection: dict[str, Any] | None) -> dict[str, Any]:
    owners: dict[str, dict[str, Any]] = {}
    for entry in (registry_projection or {}).get("entries", ()):
        for op in entry.get("operation_contracts", ()) or ():
            owner = str(op.get("semantic_owner_id", "")).strip()
            if not owner:
                continue
            item = owners.setdefault(owner, {"semantic_owner_id": owner, "supported_effects": set()})
            effect = str(op.get("effect_type", "")).strip()
            if effect:
                item["supported_effects"].add(effect)
    entries = tuple({**item, "supported_effects": tuple(sorted(item["supported_effects"]))} for _, item in sorted(owners.items()))
    domains = tuple(sorted({str(item["semantic_owner_id"]).split(".", 1)[0] for item in entries}))
    return {"schema_version": "global_semantic_capability_projection.v1", "authority": "READ_MODEL", "owner_count": len(entries), "semantic_domains": domains}


GOALFRAME_UNDERSTANDING_JSON_SCHEMA["properties"]["response_requirements"]["items"] = response_requirement_semantics_schema(
    native=True, base_schema=GOALFRAME_UNDERSTANDING_JSON_SCHEMA["properties"]["response_requirements"]["items"])


def build_goalframe_understanding_prompt(*, original_text: str, global_projection: dict[str, Any] | None = None) -> tuple[str, str]:
    """Human-intent goal understanding: semantic_domain + effect_intent, no technical target_scope."""
    system_prompt = (
        "Understand the user's explicit goals ONCE in human terms. Return one goal frame per genuine operational goal. "
        "Assign distinct opaque goal labels g1..g4. They are provenance IDs, never paths, names or requested values. "
        "semantic_domain is WHAT the user means, effect_intent is WHAT they want to happen. "
        "For memory retrieval choose the requested object ONCE in memory_filter: SOURCE_DOCUMENT for actual indexed "
        "source-document knowledge (including source/index SHA/freshness); use ANY_TIME with empty bounds for that role. "
        "For persisted conversation or experience retrieval, include memory_filter with the requested object and time "
        "ONCE: HISTORY for utterances; VERIFIED_EXPERIENCE for evidence-qualified completed work; "
        "VERIFIED_SIMULATION for qualified simulation; PROVENANCE/REVIEW_STATUS for origin/review including pending. "
        "Use ANY_TIME for no date restriction or all-time requests, TODAY_UTC only for explicit today, "
        "EXPLICIT_RANGE for supplied timezone-aware bounds. Other goals use null/omit memory_filter. "
        "Retrieving document/source contents and checking current file/index freshness concerns the source corpus, "
        "not a past conversation or completed task that mentioned the document. Indexed source knowledge uses "
        "SOURCE_DOCUMENT; direct project-file reads and live health use null memory_filter. "
        "Live availability/status/health or configured-data-versus-contract-example inspection is observe, "
        "not historical record retrieval: memory_filter MUST be null even when the semantic domain is memory. "
        "Report fields of one inspection are one goal's response requirements, not duplicate retrieval and observe goals. "
        "Determine effect from the action requested NOW, not actions described by a historical record. "
        "Inspecting existing health, counts or freshness is observe; retrieving a prior update's experience is retrieve. "
        "Only an explicit request to update derived memory/index state NOW is memory change_state, even if the original "
        "must stay unchanged. Provenance/count/hash fields to report are response requirements of that goal. "
        "DOMAIN meanings: " + json.dumps(SEMANTIC_DOMAIN_MEANINGS, ensure_ascii=False) + ". "
        "EFFECT meanings: " + json.dumps(SEMANTIC_EFFECT_MEANINGS, ensure_ascii=False) + ". "
        "goal_role is PRIMARY_OUTCOME (the user's requested effect) or SUBGOAL (a source-grounded distinct intermediate "
        "outcome the user explicitly asked for, with parent_goal_id). A PRIMARY_OUTCOME must use parent_goal_id=null. "
        "Set subgoal_justification_kind=NONE for a primary; "
        "use EXPLICIT_INTERMEDIATE for a distinct intermediate outcome explicitly requested in a different source fragment. "
        "OPERATION_DEPENDENCY is reserved for a prerequisite declared by the host operation contract, never internal reasoning. "
        "Behavior, stages, services or integrations required inside an artifact the user asks to create are the artifact's "
        "specification, not separately executable host SUBGOALs. An explicit intermediate is independently deliverable "
        "outside the parent artifact, not merely a node or behavior within it. "
        "A conditional prerequisite, restriction, or a "
        "'report/show what is needed' answer requirement is NOT a goal: do NOT emit it as a goal frame. "
        "Details to present from the SAME retrieved result (record identity, provenance, evidence, review, date) "
        "are response requirements of that retrieval goal, never a second observe goal. Separate goals require "
        "an independently requested operation or different target, not additional fields in one answer. "
        "Represent an explicit prohibition on performing an effect as execution_restriction=NO_EXECUTE, even when "
        "the prohibited effect is behavior inside the requested artifact. Copy the exact prohibiting source fragment "
        "into execution_restriction_source. A request to prepare/create an artifact while withholding permission for "
        "one of its effects is NO_EXECUTE, not NONE. Use NONE with an empty source only when no prohibition exists. "
        "A production-file restriction still permits bounded read-only simulation. "
        "Do not classify a comparison/evaluation goal as project change_state merely because its restriction mentions "
        "working files; the restriction constrains effects, while the requested comparison remains (simulation, compute_run) "
        "when it is bounded and isolated. "
        "grounding MUST be an exact fragment copied from the user's message, never 'implicit'/'none'. "
        "A pure conversation/meta request is one goal (conversation, observe). "
        "A request to control the Windows desktop or browser application/window (for example launch, show, focus, or close the application) is (windows, change_state); this is distinct from web-page content. "
        "A request to observe the Windows screen is (windows, observe). "
        "A request naming a URL or asking to read a page title/content, follow a page link, or fill a web form is (browser, observe) or (browser, change_state) according to the requested page effect; never use (windows) for DOM/page-content work. "
        "When the request only asks to open, show, focus, or close the browser application and contains no page-content or URL outcome, classify it as (windows, change_state), because the target is the desktop application/window. "
        "A request for software code analysis or a patch proposal (no file change) is (code, reason_propose). "
        "A request to create user-facing content such as a short video or script, or to produce titles, descriptions, hashtags, or other content metadata, is (content, compute_run) when generation is requested and (content, reason_propose) when only a proposal is requested. A request to inspect or transform an already-existing local media file is (media, observe) or (media, compute_run) according to the requested effect. "
        "A request to search prior memory/history is (memory, retrieve). "
        "A request to run a simulation/worker, or to compare bounded candidate approaches on the same test inputs without changing project state, is (simulation, compute_run). "
        "Creating or modifying an automation is change_state; running an existing automation is compute_run. "
        "Never invent goals the user did not state. "
        "Preserve explicitly named instruments, providers, applications and source entities in requested_outcome; "
        "they constrain how the requested outcome is produced. An input file for a coding analysis does not "
        "replace that analysis with a file-reading outcome. Launching an IDE workspace changes the desktop "
        "application state even when its input is a project. "
        "Put requested answer fields and presentation in response_requirements linked to the retrieval/operation goal; do not split reading one result into "
        "retrieval plus display goals. Use an empty response_requirements array when none are requested. "
        "Type each answer fact with requirement_kind independently of memory_query_kind (retrieval object). "
        "Use the schema-constrained relation family; provenance, rationale, execution, evidence, review and qualification are different obligations. "
        "For each subject-specific goal provide semantic subject_constraints with scope SUBJECT and known actor/source/experience identities. "
        "Use EXISTENTIAL only for actual across-subject existence questions. Never invent absent identities. "
        "Response requirements reference their goal anchors; the host derives internal bindings, relation and response IDs. "
        "Do not emit subject_binding or relation. Preserve each separately requested answer facet and its semantic kind. "
        "GLOBAL semantic-owner view (read-only, for meaning only; concrete execution IDs are resolved later): "
        + json.dumps(global_projection or {"schema_version": "global_semantic_capability_projection.v1", "authority": "READ_MODEL", "entries": ()}, ensure_ascii=False, separators=(",", ":"))
    )
    user_prompt = json.dumps({"original_text": original_text}, ensure_ascii=False)
    return system_prompt, user_prompt


def _goalframe_input_fingerprints(
    *, source_text: str, system_prompt: str, user_prompt: str,
    global_projection: dict[str, Any],
) -> dict[str, Any]:
    """Bounded identity hashes for the exact GoalFrame model input; never stores raw text."""
    projection_text = json.dumps(
        global_projection, ensure_ascii=False, sort_keys=True, separators=(",", ":"),
    )
    digest = lambda value: hashlib.sha256(str(value).encode("utf-8")).hexdigest()
    return {
        "source_text_sha256": digest(source_text),
        "system_prompt_sha256": digest(system_prompt),
        "user_prompt_sha256": digest(user_prompt),
        "goalframe_projection_sha256": digest(projection_text),
        "combined_model_input_sha256": digest(system_prompt + user_prompt),
        "source_text_length": len(source_text),
        "system_prompt_length": len(system_prompt),
        "user_prompt_length": len(user_prompt),
        "projection_entry_count": len(global_projection.get("entries", ())),
        "model_id": PRIMARY_CONVERSATION_MODEL_ID,
        "model_role": "jarvis_chat_model",
        "num_ctx": REQUEST_UNDERSTANDING_NUM_CTX,
        "num_predict": REQUEST_UNDERSTANDING_NUM_PREDICT,
        "temperature": 0,
        "think": False,
        "stream": False,
        "keep_alive": "1800s",
        "seed_present": False,
    }


def build_artifact_operation_extraction_prompt(
    *, original_text: str, goals: list[dict[str, Any]], execution_restriction_source: str,
) -> tuple[str, str]:
    """Focused semantic pass that owns artifact behavior before any topology exists."""
    goal_projection = tuple({
        "goal_id": str(goal["goal_id"]),
        "semantic_domain": str(goal["semantic_domain"]),
        "requested_outcome": str(goal.get("requested_outcome", "")),
        "grounding": str(goal.get("grounding", "")),
    } for goal in goals if _requires_artifact_operations(goal))
    system_prompt = (
        "Independently extract EVERY operation that each requested automation artifact must perform after its trigger. "
        "This pass occurs before graph generation and is the one canonical artifact-operation fact; topology may only "
        "reference its requirement IDs. Do not extract the host act of creating/configuring the workflow, workflow "
        "metadata, its runtime/platform, control flow, or execution prohibitions. A prohibition changes authorization, "
        "not the artifact's requested behavior. A provider-preservation/substitution constraint is an attribute of the "
        "real operation, never a separate ASSIGN or STORE operation. Use ASSIGN only for literal/value assignment; TRANSFORM for intrinsic "
        "computation deriving new content; otherwise use the exact real class among FETCH, GENERATE, PUBLISH, SEND, "
        "RECORD, STORE, TRANSCRIBE, SYNTHESIZE, RENDER, SEARCH, DELEGATE, OBSERVE, ACT. Copy a narrow exact supporting "
        "fragment from original_text into source_grounding, including a late fragment beyond character 160. For an "
        "explicit provider copy its exact source surface and use SOURCE_EXPLICIT with an empty inference justification. "
        "ASSIGN and TRANSFORM are intrinsic artifact operations: their provider fields must be empty/NONE even when "
        "the source names the workflow platform. The platform hosts the artifact; it is not the provider of an "
        "intrinsic assignment or computation. "
        "For every non-intrinsic operation, a service/provider explicitly named in its supporting source fragment "
        "remains SOURCE_EXPLICIT even when execution or credentials are prohibited. Authorization never erases that "
        "provider constraint. Never write the placeholder text 'NONE' as a provider name. "
        "Use SEMANTIC_INFERENCE only with a nonempty separate justification; use NONE with empty provider fields when "
        "there is no provider. Emit one requirement per genuine source effect; never invent retrieval, delegation, "
        "storage, or other prerequisites merely because an operation could need them. Each supplied automation goal "
        "requires at least one genuine artifact operation. GOALS="
        + json.dumps(goal_projection, ensure_ascii=False, separators=(",", ":"))
        + " EXECUTION_RESTRICTION_SOURCE="
        + json.dumps(execution_restriction_source, ensure_ascii=False)
    )
    return system_prompt, json.dumps({"original_text": original_text}, ensure_ascii=False)


def _goalframe_projection(registry_projection: dict[str, Any], *, semantic_domain: str,
                          effect_intent: str, memory_filter: dict[str, str] | None = None) -> tuple[str, ...]:
    """Deterministic, safety-monotonic projection by (semantic_domain, effect_intent).

    A capability is a candidate only if its target_scope belongs to the domain AND its
    operation effect_type is NOT more dangerous than the effect_intent's intent. This makes
    the bounded-repair (broadening from an empty exact match to the domain) safety-monotonic:
    it may recover a binding but never recovers a MORE dangerous effect than the intent."""
    scopes = _SEMANTIC_DOMAIN_SCOPES.get(semantic_domain, frozenset())
    intent_types = SEMANTIC_EFFECT_INTENTS.get(effect_intent, frozenset({"OBSERVE"}))
    intent_danger = max((_effect_danger(t) for t in intent_types), default=0)
    matched: list[str] = []
    for entry in registry_projection.get("entries", ()):
        entry_scopes: set[str] = set()
        entry_effects: set[str] = set()
        for op in entry.get("operation_contracts") or ():
            supported_intents = tuple(op.get("supported_goal_effect_intents", ()))
            if supported_intents and effect_intent not in supported_intents:
                continue
            if memory_filter is not None:
                filter_schema = op.get("parameter_schemas", {}).get("memory_filter")
                if filter_schema is None:
                    continue
                from MAKSIMAR_SERVER.AI_ORCHESTRATION.model_understanding_adapter import validate_structured_payload
                _, compatible, _ = validate_structured_payload(json.dumps(memory_filter), filter_schema)
                if not compatible:
                    continue
            if op.get("target_scope"):
                entry_scopes.add(str(op["target_scope"]))
            if op.get("effect_type"):
                entry_effects.add(str(op["effect_type"]))
        if not (entry_scopes & scopes):
            continue
        # Safety-monotonic: skip capabilities whose EVERY effect is more dangerous than intent.
        if entry_effects and all(_effect_danger(e) > intent_danger for e in entry_effects):
            continue
        matched.append(str(entry["capability_id"]))
    return tuple(dict.fromkeys(matched))


GOAL_BINDING_JSON_SCHEMA: dict[str, Any] = {
    "type": "object", "additionalProperties": False,
    "required": ["status", "capability_id", "reason"],
    "properties": {
        "status": {"type": "string", "enum": ["BOUND", "UNAVAILABLE", "NOT_IMPLEMENTED", "UNRESOLVED"]},
        "capability_id": {"type": ["string", "null"]},
        "reason": {"type": "string", "maxLength": 160},
    },
}


def build_goalframe_binding_prompt(*, goal: dict[str, str], registry_projection: dict[str, Any]) -> tuple[str, str]:
    """GoalBinding: bind ONE authoritative goal to a compatible registered capability.

    Unlike legacy candidate discovery (which is centered on executable effects), this
    binding treats observable, executable, retrieval, model-role (reasoning), simulation,
    and unavailable/not-implemented capabilities alike."""
    index = _compact_index_payload(registry_projection)
    operation_support = tuple((str(entry["capability_id"]), str(op["operation_id"]),
        str(op.get("description", ""))[:400], str(op.get("semantic_owner_id", "")))
        for entry in registry_projection.get("entries", ()) for op in entry.get("operation_contracts", ()))
    input_contracts = tuple({"capability_id": str(entry["capability_id"]),
        "operation_id": str(op["operation_id"]), "parameter_schemas": op.get("parameter_schemas", {})}
        for entry in registry_projection.get("entries", ()) for op in entry.get("operation_contracts", ())
        if goal.get("memory_filter") and "memory_filter" in (op.get("parameter_schemas") or {}))
    system_prompt = (
        "Bind this ONE goal to the single best registered capability that satisfies it, considering "
        "observable (read), executable (run), retrieval, semantic generation, simulation, and "
        "unavailable/not-implemented capabilities alike. "
        "The goal's source grounding constrains the instrument and corpus even when its outcome omits them. "
        "Its linked response_requirements constrain the required evidence fields; do not bind a contract that "
        "cannot supply those facts merely because its subject label matches the requested outcome. "
        "Distinguish a named component that is the subject of inspection from an instrument requested for execution. "
        "A live health/inventory goal needs an actual live status/read-model contract, not archived documents about the component. "
        "Current source contents, file SHA and indexed-source freshness need an actual source/index read contract. "
        "Past task records and receipt/evidence hashes do not satisfy those source facts. "
        "When the goal requests execution with a retrieval engine or coding provider, bind its actual executable "
        "contract; a generic history reader, status viewer or alternative generator cannot satisfy that execution constraint. "
        "Do not substitute another provider when the named one is unavailable; report its availability honestly. "
        "GOAL=" + json.dumps(goal, ensure_ascii=False) + " "
        "INDEX=" + index + " "
        "OPERATION_SUPPORT=" + json.dumps(operation_support, ensure_ascii=False, separators=(",", ":")) + " "
        + ("TYPED_INPUT_CONTRACTS=" + json.dumps(input_contracts, ensure_ascii=False, separators=(",", ":"))
           + " The authoritative goal already chooses the memory object and time scope. Bind by declared input support; "
             "a retrieval request about completed past work does not require executing that work now. "
           if input_contracts else "")
        + "status=BOUND with capability_id when a listed candidate satisfies the goal. "
        "status=UNAVAILABLE with capability_id when the right candidate is registered but its provider is unavailable. "
        "status=NOT_IMPLEMENTED when the right capability is not implemented. "
        "status=UNRESOLVED with capability_id=null when no candidate fits. "
        "Always return exactly one status for this goal; never omit it."
    )
    user_prompt = json.dumps({"goal_id": goal["goal_id"]}, ensure_ascii=False)
    return system_prompt, user_prompt


def _bind_goalframe_goal(*, call: Any, goal: dict[str, str], registry_projection: dict[str, Any],
                         deadline: RequestDeadline, binding_attempt: int = 1,
                         binding_audit: dict[str, Any] | None = None) -> tuple[str | None, str]:
    """Bind one goal to its technical owner. Returns (capability_id_or_None, status)."""
    projection_summary = {
        "direct_capability_ids": tuple(
            str(item.get("capability_id", "")) for item in registry_projection.get("entries", ())
        )[:32],
        "operation_ids": tuple(
            str(operation.get("operation_id", ""))
            for item in registry_projection.get("entries", ())
            for operation in item.get("operation_contracts", ()) or ()
        )[:32],
        "semantic_owner_ids": tuple(
            str(operation.get("semantic_owner_id", ""))
            for item in registry_projection.get("entries", ())
            for operation in item.get("operation_contracts", ()) or ()
            if str(operation.get("semantic_owner_id", ""))
        )[:32],
    }
    projection_id = hashlib.sha256(
        json.dumps(projection_summary, ensure_ascii=False, sort_keys=True, separators=(",", ":")).encode()
    ).hexdigest()[:16]
    goal_summary = {
        key: goal.get(key, "") for key in (
            "goal_id", "semantic_domain", "effect_intent", "goal_role", "ambiguity",
        )
    }

    def record_binding(status: str, capability_id: Any, reason_class: str) -> None:
        trace_stage(
            "GOALFRAME_BINDING", "COMPLETED" if status == "BOUND" else "FAILED",
            binding_attempt=int(binding_attempt), binding_goal=goal_summary,
            binding_projection_id=projection_id,
            binding_direct_capability_ids=projection_summary["direct_capability_ids"],
            binding_operation_ids=projection_summary["operation_ids"],
            binding_semantic_owner_ids=projection_summary["semantic_owner_ids"],
            binding_status=status, binding_capability_id=(str(capability_id) if capability_id else None),
            binding_reason_present=bool(reason_class), binding_reason_class=reason_class,
        )

    system_prompt, user_prompt = build_goalframe_binding_prompt(goal=goal, registry_projection=registry_projection)
    result = call(system_prompt=system_prompt, user_prompt=user_prompt, deadline=deadline,
                  output_schema=GOAL_BINDING_JSON_SCHEMA)
    verification_error = (
        _model_call_verification_error(result) if isinstance(result, dict)
        else "semantic_result_envelope_not_object"
    )
    if binding_audit is not None:
        binding_audit.update(raw_model_content=result.get("content") if isinstance(result, dict) else result,
            final_valid=result.get("final_valid") if isinstance(result, dict) else None,
            semantic_verification_error=verification_error)
    if verification_error:
        record_binding("UNRESOLVED", None, "SEMANTIC_RESULT_INVALID")
        return None, "UNRESOLVED"
    content = result.get("content") if isinstance(result, dict) else result
    raw = content
    if isinstance(content, str):
        try:
            raw = json.loads(content)
        except (TypeError, ValueError, json.JSONDecodeError) as exc:
            record_binding("UNRESOLVED", None, "INVALID_JSON")
            trace_stage(
                "CANDIDATE_DISCOVERY_FAILURE", "FAILED", candidate_stage="PARSE",
                failure_type=type(exc).__name__, failure_code="goal_binding_invalid_json",
                repair_attempt=0, safe_structure={
                    "top_level_type": "unknown", "schema_parse_status": "FAILED",
                },
            )
            return None, "UNRESOLVED"
    if not isinstance(raw, dict):
        record_binding("UNRESOLVED", None, "TOP_LEVEL_NOT_OBJECT")
        trace_stage(
            "CANDIDATE_DISCOVERY_FAILURE", "FAILED", candidate_stage="VALIDATE",
            failure_type="ValueError", failure_code="goal_binding_top_level_not_object",
            repair_attempt=0, safe_structure={
                "top_level_type": type(raw).__name__, "schema_parse_status": "PASS",
            },
        )
        return None, "UNRESOLVED"
    status = str(raw.get("status", "UNRESOLVED"))
    cap = raw.get("capability_id")
    if binding_audit is not None:
        binding_audit.update(binding_status=status,
                             model_proposed_capability_id=cap,
                             binding_reason=str(raw.get("reason", ""))[:160])
    trace_stage("GOALFRAME_BINDING_REASON", "COMPLETED", binding_attempt=int(binding_attempt),
        binding_goal_id=goal["goal_id"], binding_status=status, binding_reason=str(raw.get("reason", ""))[:160])
    if status == "BOUND" and cap:
        resolved = str(cap)
        # Models may name the canonical semantic operation owner (for example
        # ``simulation.run``) rather than the concrete registered capability.
        # Resolve that typed owner through the supplied registry projection;
        # never accept an ID absent from the projection.
        if resolved not in {
            str(item.get("capability_id")) for item in registry_projection.get("entries", ())
        }:
            matches = tuple(
                str(item.get("capability_id"))
                for item in registry_projection.get("entries", ())
                if any(str(op.get("semantic_owner_id", "")) == resolved
                       for op in item.get("operation_contracts") or ())
            )
            if len(matches) == 1:
                resolved = matches[0]
        if resolved in {str(item.get("capability_id")) for item in registry_projection.get("entries", ())}:
            record_binding("BOUND", resolved, "BOUND")
            return resolved, "BOUND"
        record_binding("UNRESOLVED", resolved, "CAPABILITY_NOT_IN_PROJECTION")
        trace_stage(
            "CANDIDATE_DISCOVERY_FAILURE", "FAILED", candidate_stage="VALIDATE",
            failure_type="ValueError", failure_code="goal_binding_capability_not_in_projection",
            repair_attempt=0, safe_structure={
                "top_level_type": "dict", "top_level_keys": tuple(sorted(str(key) for key in raw))[:24],
                "candidate_count": 1, "candidate_ids": (resolved,),
                "schema_parse_status": "PASS",
            },
        )
        return None, "UNRESOLVED"
    if status in ("UNAVAILABLE", "NOT_IMPLEMENTED") and cap:
        record_binding(status, cap, status)
        return str(cap), status
    record_binding(status if status in {"UNRESOLVED", "BOUND"} else "UNRESOLVED", cap, "STATUS_UNRESOLVED")
    trace_stage(
        "CANDIDATE_DISCOVERY_FAILURE", "FAILED", candidate_stage="VALIDATE",
        failure_type="ValueError", failure_code="goal_binding_status_unresolved",
        repair_attempt=0, safe_structure={
            "top_level_type": "dict", "top_level_keys": tuple(sorted(str(key) for key in raw))[:24],
            "candidate_count": 1 if cap else 0,
            "candidate_ids": (str(cap),) if cap else (), "schema_parse_status": "PASS",
        },
    )
    return None, "UNRESOLVED"


def measure_prompt_budget(system_prompt: str, user_prompt: str, *, reserved_output_tokens: int,
                          output_schema: dict[str, Any] | None = None,
                          components: dict[str, str] | None = None,
                          num_ctx: int | None = None) -> dict[str, Any]:
    budget_num_ctx = (
        context_tokens_for_jarvis_model(PRIMARY_CONVERSATION_MODEL_ID)
        if num_ctx is None else int(num_ctx)
    )
    combined = system_prompt + user_prompt
    utf8_bytes = len(combined.encode("utf-8"))
    characters = len(combined)
    estimated_tokens = max(ceil(utf8_bytes / 3), ceil(characters / 2))
    input_budget = (budget_num_ctx - reserved_output_tokens - PROMPT_SAFETY_MARGIN_TOKENS
                    - UNKNOWN_SCHEMA_CONTEXT_RESERVE_TOKENS)
    schema_text = json.dumps(output_schema or {}, ensure_ascii=False, separators=(",", ":"))
    measured_components = {
        name: {"utf8_bytes": len(value.encode("utf-8")), "characters": len(value),
               "estimated_tokens": max(ceil(len(value.encode("utf-8")) / 3), ceil(len(value) / 2))}
        for name, value in (components or {"system_prompt": system_prompt, "user_prompt": user_prompt}).items()
    }
    measured_components["request_schema_format_material"] = {
        "utf8_bytes": len(schema_text.encode("utf-8")), "characters": len(schema_text),
        "estimated_tokens": max(ceil(len(schema_text.encode("utf-8")) / 3), ceil(len(schema_text) / 2)),
        "included_in_model_context": "UNKNOWN",
    }
    return {
        "utf8_bytes": utf8_bytes, "characters": characters,
        "estimated_prompt_tokens": estimated_tokens,
        "estimator_kind": "MAX_UTF8_BYTES_DIV_3_CHARACTERS_DIV_2",
        "estimator_is_conservative": True,
        "actual_prompt_tokens": None, "actual_prompt_tokens_source": None,
        "tokenizer_tokens": None, "tokenizer_status": "NOT_EXECUTED",
        "budget_decision_source": "CONSERVATIVE_STATIC_ESTIMATE",
        "output_schema_utf8_bytes": len(schema_text.encode("utf-8")),
        "output_schema_characters": len(schema_text),
        "schema_context_cost": "UNKNOWN",
        "schema_context_inclusion": "UNKNOWN_FOR_CURRENT_OLLAMA_VERSION",
        "total_request_material_utf8_bytes": utf8_bytes + len(schema_text.encode("utf-8")),
        "num_ctx": budget_num_ctx, "configured_num_ctx": budget_num_ctx,
        "budget_num_ctx": budget_num_ctx,
        "context_authority_source": MODEL_CONTEXT_AUTHORITY_SOURCE,
        "reserved_output_tokens": reserved_output_tokens,
        "safety_margin_tokens": PROMPT_SAFETY_MARGIN_TOKENS,
        "unknown_schema_context_reserve_tokens": UNKNOWN_SCHEMA_CONTEXT_RESERVE_TOKENS,
        "available_input_tokens": input_budget, "components": measured_components,
        "within_budget": estimated_tokens <= input_budget,
    }


def require_prompt_budget(system_prompt: str, user_prompt: str, *, reserved_output_tokens: int,
                          output_schema: dict[str, Any] | None = None,
                          components: dict[str, str] | None = None,
                          num_ctx: int | None = None) -> dict[str, Any]:
    measurement = measure_prompt_budget(
        system_prompt, user_prompt, reserved_output_tokens=reserved_output_tokens, output_schema=output_schema,
        components=components, num_ctx=num_ctx,
    )
    if not measurement["within_budget"]:
        raise ValueError("request_understanding_prompt_budget_exceeded")
    return measurement


def discovery_schema_for_registered_values(
    base_schema: dict[str, Any], *, value_key: str, allowed_values: tuple[str, ...],
    max_selected_values: int | None = None,
    operation_contracts: tuple[dict[str, Any], ...] | None = None,
) -> dict[str, Any]:
    """Bind structured discovery output to the exact registry scope for this model pass."""
    schema = json.loads(json.dumps(base_schema))
    selection_schema = schema["properties"][value_key]
    if value_key == "candidate_operation_ids":
        registered_operation_ids = tuple(str(contract["operation_id"]) for contract in (operation_contracts or ()))
        declared_prerequisites = {
            str(contract["operation_id"]) for contract in (operation_contracts or ())
            if validate_operation_dependency_references(contract, registered_operation_ids)
        }
        selection_limit = min(
            DISCOVERY_VALUES_PER_PASS,
            len(allowed_values),
            max_selected_values if max_selected_values is not None else DISCOVERY_VALUES_PER_PASS,
        )
        # Reuse the existing capability-discovery sparse selection contract.
        # IDs are exact registry keys, so duplicate operation values cannot be
        # represented; the strict parser still rejects malformed/legacy repeats.
        selection_schema.update(type="object", properties={
            value: {"type": "boolean", "const": True} for value in allowed_values},
            required=[], additionalProperties=False, minProperties=0,
            maxProperties=selection_limit,
            description="Select unique registered operation IDs as keys with true values; omit unselected IDs.")
        schema["properties"]["selection_justifications"] = {
            "type": "object",
            "additionalProperties": False,
            "properties": {
                value: {
                    "type": "object", "additionalProperties": False,
                    "required": ["goal_id", "justification_kind", "source_grounding"],
                    "properties": {
                        "goal_id": {"type": "string", "minLength": 1, "maxLength": 64},
                        "justification_kind": {
                            "type": "string",
                            "enum": ["DIRECT_GOAL_EFFECT"] + (
                                ["DECLARED_OPERATION_DEPENDENCY"]
                                if value in declared_prerequisites
                                else []
                            ),
                        },
                        "source_grounding": {"type": "string", "minLength": 1, "maxLength": 160},
                    },
                }
                for value in allowed_values
            },
            "minProperties": 0,
            "maxProperties": selection_limit,
        }
        if selection_limit <= 1:
            # With one remaining justified slot, a nonempty selection consumes
            # the complete capacity. Further selection cannot make progress.
            schema["properties"]["continuation_required"] = {"type": "boolean", "const": False}
            schema["properties"]["continuation_reason"] = {"type": "string", "const": ""}
        return schema
    else:
        # Explicitly-enumerated sparse object: the allowed capability IDs are PROPERTY
        # NAMES with const true and additionalProperties=false. JSON object keys are
        # inherently unique, so a duplicate capability ID is structurally unrepresentable
        # (a fixed-slot array, by contrast, can repeat the same VALUE in two slots).
        selection_schema["properties"] = {
            value: {"type": "boolean", "const": True} for value in allowed_values
        }
        selection_schema["additionalProperties"] = False
        selection_schema["maxProperties"] = min(DISCOVERY_VALUES_PER_PASS, len(allowed_values))
    if len(allowed_values) <= DISCOVERY_VALUES_PER_PASS:
        schema["properties"]["continuation_required"] = {"type": "boolean", "const": False}
        schema["properties"]["continuation_reason"] = {"type": "string", "const": ""}
    return schema


def _compact_index_payload(registry_projection: dict[str, Any]) -> str:
    index = project_semantic_capability_index(registry_projection)
    rows = tuple((
        item["capability_id"], item["kind"], item["description"][:96],
        item["availability"], bool(item["execution_contract"]),
    ) for item in index)
    return json.dumps({
        "legend": ("id", "kind", "description", "availability", "execution_contract"),
        "rows": rows,
    }, ensure_ascii=False, separators=(",", ":"))


def _semantic_context_for_model(
    session_context: dict[str, Any], *, user_text_limit: int = 120,
    assistant_text_limit: int = 160, topic_history_limit: int = 6,
    topic_text_limit: int = 40, unresolved_text_limit: int = 80,
) -> dict[str, Any]:
    """Project host session state into bounded semantic context without IDs."""
    turns = tuple(
        item for item in session_context.get("bounded_chronological_turns", ())
        if isinstance(item, dict)
    )
    recent_turns = tuple({
        "user_text": str(item.get("user_text", ""))[:user_text_limit],
        "assistant_text": str(item.get("assistant_text", ""))[:assistant_text_limit],
        "topic": str(item.get("topic", ""))[:40],
    } for item in turns[-2:])
    unresolved = session_context.get("unresolved_reference")
    unresolved_present = bool(
        unresolved.get("present") if isinstance(unresolved, dict) else unresolved
    )
    if (
        not turns
        and not unresolved_present
        and not str(session_context.get("current_topic", "")).strip()
        and not session_context.get("truncated")
        and not session_context.get("omitted_turn_count")
    ):
        return {}
    return {
        "bounded_turn_count": len(turns),
        "recent_turns": recent_turns,
        "topic_history": tuple(
            str(item.get("topic", ""))[:topic_text_limit]
            for item in turns[-topic_history_limit:]
            if str(item.get("topic", "")).strip()
        ),
        "unresolved_reference": {
            "present": unresolved.get("present"),
            "description": str(unresolved.get("description", ""))[:unresolved_text_limit],
        } if isinstance(unresolved, dict) else str(unresolved or "")[:unresolved_text_limit],
        "context_truncated": bool(session_context.get("truncated", False)),
        "omitted_turn_count": int(session_context.get("omitted_turn_count", 0)),
    }


def _semantic_discovery_context_for_model(session_context: dict[str, Any]) -> dict[str, Any]:
    """Project only referential topic labels for typed discovery stages.

    Kind, candidate and operation discovery decide the active semantic domain and the
    capabilities for the current explicit request. Historical turn text must never create
    a new goal or override the current domain — it causes semantic drift under a long
    shared session — so the current original_text owns the domain. A short topic-history
    label and an explicit unresolved reference are the only host-projected historical
    signals these stages may consult (referents and session facts, not domain content).
    The RequestUnderstanding stage keeps the full referential context separately, so
    conversation continuity is preserved.
    """
    turns = tuple(
        item for item in session_context.get("bounded_chronological_turns", ())
        if isinstance(item, dict)
    )
    topic_history = tuple(
        str(item.get("topic", ""))[:24]
        for item in turns[-2:]
        if str(item.get("topic", "")).strip()
    )
    unresolved = session_context.get("unresolved_reference")
    unresolved_present = bool(
        unresolved.get("present") if isinstance(unresolved, dict) else unresolved
    )
    artifacts = tuple(
        {"kind": str(a.get("kind", "")), "provider": str(a.get("provider", "")), "provider_id": str(a.get("provider_id", ""))}
        for a in session_context.get("recent_artifacts", ())
        if isinstance(a, dict) and a.get("kind")
    )
    if not topic_history and not unresolved_present and not artifacts:
        return {}
    result: dict[str, Any] = {}
    if artifacts:
        result["recent_artifacts"] = artifacts
    if topic_history:
        result["topic_history"] = topic_history
    if unresolved_present:
        result["unresolved_reference"] = (
            {
                "present": True,
                "description": str(unresolved.get("description", ""))[:48],
            }
            if isinstance(unresolved, dict)
            else str(unresolved or "")[:48]
        )
    return result


def build_kind_discovery_prompt(*, original_text: str, session_context: dict[str, Any],
                                registry_projection: dict[str, Any],
                                already_selected_ids: tuple[str, ...] = ()) -> tuple[str, str]:
    index = project_semantic_capability_index(registry_projection)
    projection_entries = {
        str(item["capability_id"]): item for item in registry_projection.get("entries", ())
    }
    by_kind: dict[str, list[dict[str, object]]] = {}
    for item in index:
        by_kind.setdefault(str(item["kind"]), []).append(item)
    domains = tuple((
        kind,
        len(items),
        sum(1 for item in items if item["execution_contract"]),
        sum(1 for item in items if item["availability"] == "AVAILABLE"),
        tuple(str(item["description"])[:64] for item in items if item["execution_contract"]),
    ) for kind, items in sorted(by_kind.items()))
    system_prompt = (
        "Select the smallest sufficient semantic kind set for explicit request goals using meaning and bounded context "
        "only, never text-pattern routing. The current original_text owns explicit goals; prior context may resolve a "
        "reference but must never add, replace or override a current explicit goal. A recent_artifacts automation/workflow "
        "is a prior workflow; a follow-up modify/run must select its owning kind, not conversation. A request to create, "
        "build or automate a workflow is an operational goal owned by the workflow_automation kind, never a conversation; "
        "select workflow_automation for it even when accounts/access are not yet connected. A pure conversation or meta request "
        "(a greeting, a capability or help inquiry) has no named action, observation, retrieval, computation or mutation "
        "goal and must select only the canonical conversation kind. Do not infer ancillary goals or select operations, "
        "providers or policy. "
        "DOMAINS tuples are (kind, visible_count, executable_count, available_count, descriptions). Prefer a directly "
        "sufficient executable kind for a requested action; use non-executable kinds only for an explicit consideration "
        "or limitation, never as duplicate layers for a goal already satisfied by an executable kind. Reading is an "
        "OBSERVE execution effect even when mutation is forbidden. Prior selections are host-owned and removed from "
        "this pass's domain enum. Encode each new kind as one unique candidate_kinds JSON key with value true. with one, "
        "two or three candidate_kinds keys, continuation_required MUST be false. Continue only for a distinct "
        "explicit user goal still unsatisfied; continuation_reason must identify that goal, not merely claim more "
        "relevance, context or ambiguity. Return at most " + str(DISCOVERY_VALUES_PER_PASS)
        + " new kinds this pass; this is not a semantic result limit. DOMAINS="
        + json.dumps(domains, ensure_ascii=False, separators=(",", ":"))
    )
    user_prompt = json.dumps({
        "original_text": original_text,
        "bounded_session_context": _semantic_discovery_context_for_model(session_context),
        "host_owned_already_selected_ids": already_selected_ids,
        "prior_selection_count": len(already_selected_ids),
    }, ensure_ascii=False, separators=(",", ":"))
    return system_prompt, user_prompt


def build_model_selected_kind_candidate_discovery_prompt(
    *, original_text: str, session_context: dict[str, Any],
    registry_projection: dict[str, Any], already_selected_ids: tuple[str, ...] = (),
) -> tuple[str, str]:
    """Give a bounded kind pass its typed cross-stage role without choosing an ID."""
    system_prompt, user_prompt = build_candidate_discovery_prompt(
        original_text=original_text,
        session_context=session_context,
        registry_projection=registry_projection,
        already_selected_ids=already_selected_ids,
    )
    return (
        system_prompt
        + " This bounded INDEX belongs to a semantic kind selected by the same main model in the immediately "
        "preceding typed stage. Select the smallest matching IDs when this kind has a distinct role in the current "
        "explicit goal. Return empty only when that prior kind selection was a false positive or another host pass "
        "fully covers the role. Do not describe an indexed execution_contract=true entry as non-executable.",
        user_prompt,
    )


def build_cross_kind_executable_reconciliation_prompt(
    *, original_text: str, session_context: dict[str, Any],
    registry_projection: dict[str, Any], selected_kinds: tuple[str, ...],
    already_selected_ids: tuple[str, ...] = (),
) -> tuple[str, str]:
    """Let the main model reconcile a selected semantic kind with canonical owners."""
    system_prompt, user_prompt = build_candidate_discovery_prompt(
        original_text=original_text,
        session_context=session_context,
        registry_projection=registry_projection,
        already_selected_ids=already_selected_ids,
    )
    envelope = json.loads(user_prompt)
    envelope["model_selected_kind_context"] = selected_kinds
    system_prompt = (
        system_prompt
        + " Reconcile this bounded cross-kind scope with the canonical executable owners: keep a selected kind's "
        "ID only when it covers an explicit goal not already satisfied by a canonical owner. Drop a kind that merely "
        "duplicates an already-selected canonical owner. Do not select a non-canonical ID that lacks an execution "
        "contract."
    )
    return system_prompt, json.dumps(envelope, ensure_ascii=False, separators=(",", ":"))


def build_cross_kind_executable_reconciliation_repair_prompt(
    *, original_text: str, session_context: dict[str, Any],
    registry_projection: dict[str, Any], selected_kinds: tuple[str, ...],
    already_selected_ids: tuple[str, ...] = (),
) -> tuple[str, str]:
    system_prompt, user_prompt = build_cross_kind_executable_reconciliation_prompt(
        original_text=original_text,
        session_context=session_context,
        registry_projection=registry_projection,
        selected_kinds=selected_kinds,
        already_selected_ids=already_selected_ids,
    )
    return (
        system_prompt
        + " The first reconciliation still returned only the response capability. Re-evaluate this typed "
        "inconsistency once: response cannot satisfy an observation, retrieval or execution role. Select a canonical "
        "owner whose authoritative operations cover the explicit role. Return response-only only if the prior kind "
        "was genuinely a false positive, with reason code kind_false_positive.",
        user_prompt,
    )


def build_candidate_discovery_prompt(*, original_text: str, session_context: dict[str, Any],
                                     registry_projection: dict[str, Any],
                                     already_selected_ids: tuple[str, ...] = ()) -> tuple[str, str]:
    response_capability_in_index = any(
        str(item.get("capability_id", "")) == "conversation.respond"
        for item in registry_projection.get("entries", ())
        if isinstance(item, dict)
    )
    empty_selection_rule = (
        "This INDEX contains the canonical response capability, so candidate_capability_ids MUST include conversation.respond. "
        if response_capability_in_index else
        "Return an empty object only when the request needs no executable effect from this INDEX. "
    )
    system_prompt = (
        "Select the smallest sufficient capability IDs for explicit goals by meaning and bounded context; never "
        "route by keyword, phrase, regex, marker, token root or exact text. Each ID needs a distinct execution or "
        "limitation role. The current original_text owns explicit goals; prior context may resolve a "
        "reference but must never add, replace or override a current explicit goal. "
        "INDEX's last boolean is execution_contract truth. AVAILABLE plus "
        "execution_contract=true is executable; UNKNOWN availability defers to per-step runtime truth. Do not call an "
        "AVAILABLE bound contract unavailable. Reading/checking is OBSERVE; no-change forbids MUTATE, not OBSERVE. "
        "A stored-history search needs its indexed executable memory capability; bounded session context is not a "
        "prerequisite for retrieval. "
        "Cover every explicit goal. Never discard a broad executable candidate when retained narrow contracts leave "
        "a goal uncovered. Required targets must be concrete from original_text or context; never invent placeholders. "
        "Selection records need only; host policy authorizes later. Delegated work or "
        "computation needs its indexed executable capability; RESPOND cannot substitute. A request to create or build an "
        "automation/workflow is owned by the workflow_automation capability, never RESPOND. RESPOND (conversation.respond) "
        "is mandatory when present in this INDEX: always select it for the visible answer. RESPOND cannot supply "
        "OBSERVE/RETRIEVE evidence; an evidence request with an answer needs both roles. Do not select operations, providers, policy, "
        "risk or an answer. A confirmation or no-execution constraint never removes the requested capability: select "
        "it for the typed plan and let per-step policy block execution. Return at most "
        + str(DISCOVERY_VALUES_PER_PASS) +
        " unique candidate_capability_ids=true; prior IDs are host-owned and absent. Do not mention a necessary ID "
        "only in reasons, and avoid redundant broad+narrow entries. With 1-3 selected keys continuation_required=false. "
        "Goals absent from this INDEX belong to another host pass; do not continue or substitute unrelated IDs. "
        + empty_selection_rule +
        "Continue only if another explicit goal needs an ID and all slots are used; never for relevance or breadth. INDEX="
        + _compact_index_payload(registry_projection)
    )
    user_prompt = json.dumps({"original_text": original_text,
                              "bounded_session_context": _semantic_discovery_context_for_model(session_context),
                              "host_owned_already_selected_ids": already_selected_ids,
                              "prior_selection_count": len(already_selected_ids)},
                             ensure_ascii=False, separators=(",", ":"))
    return system_prompt, user_prompt




def build_operation_discovery_prompt(
    *, original_text: str, session_context: dict[str, Any],
    registry_projection: dict[str, Any], already_selected_ids: tuple[str, ...] = (),
) -> tuple[str, str]:
    catalog = load_operation_catalog(registry_projection)
    candidate_stage_status = dict(registry_projection.get("candidate_stage_status", {}))
    dependency_contracts = dict(registry_projection.get("selection_operation_dependency_contracts", {})) or {
        str(item["operation_id"]): tuple(item["declared_prerequisite_for_operation_ids"])
        for item in catalog if item.get("declared_prerequisite_for_operation_ids")
    }
    rows = tuple((
        item["operation_id"], item["capability_id"], item["operation_description"][:180],
        item["effect_type"], item["target_scope"], item["risk_class"],
        tuple(str(parameter) for parameter in item.get("required_parameters", ())),
        candidate_stage_status.get(str(item["capability_id"]), "PRIMARY"),
    ) for item in catalog)
    goalframes = tuple({
        "goal_id": str(item.get("goal_id", "")),
        "effect_intent": str(item.get("effect_intent", "")),
        "requested_outcome": str(item.get("requested_outcome", ""))[:120],
        **({"memory_filter": item["memory_filter"]} if item.get("memory_filter") is not None else {}),
        "grounding": str(item.get("grounding", ""))[:160],
    } for item in registry_projection.get("selection_goalframes", ()))
    system_prompt = (
        "Select the smallest sufficient authoritative operation set by the user's actual goals. "
        "Compare declared output coverage, not names. Prefer a sufficient aggregate over redundant constituent "
        "reads. Cover all explicit goals and response facts. "
        "Return at most 4 new IDs per pass, not optional operations or the whole catalog. "
        "Artifact behavior belongs in create parameters/topology, not separate host run/inspect/modify operations. "
        "Creating includes complete initial configuration. Select modify only for a separately requested change "
        "to an existing artifact identified by source or bounded referent. A restriction against an effect "
        "forbids that effect as a direct current goal. "
        "Every required_params input must be given or directly resolvable from the request or explicit bounded "
        "referent; never invent a concrete target. A locate/find goal needs a query/no-target contract, "
        "not a target-required read. "
        "Continue only for a distinct explicit unmet goal, never overflow or broadness. A short summary needs "
        "direct state evidence. For content retrieval, do not add registry, domain, federation, catalog or availability "
        "operations unless that metadata or status is explicitly requested. "
        "PRIMARY is the consolidated semantic candidate set. ALTERNATIVE was selected by the same main model "
        "in an earlier bounded pass but omitted in consolidation; use it only if PRIMARY cannot cover a distinct "
        "explicit goal. Neither status routes user text. "
        "Include respond with necessary evidence operations when a visible answer is required and respond is "
        "in this catalog; it is not implicit. Do not choose providers, policy, evidence truth or the answer. "
        "candidate_operation_ids uses the existing sparse selection object: selected registered IDs are keys with true values; omit unselected IDs. "
        "selection_justifications keys must exactly equal selected IDs. "
        "Each justification cites a source GOAL goal_id and the shortest sufficient exact source_grounding "
        "fragment (at most 160 characters). Omit unselected IDs and invented dependencies. "
        "DIRECT_GOAL_EFFECT must match that goal's effect; DECLARED_OPERATION_DEPENDENCY requires an actual "
        "catalog prerequisite. Availability/relevance/complexity are not justifications. "
        "continuation_required means MORE SELECTION PASSES, never subsequent provider execution. "
        "Set it false when these operations cover the explicit request. Prior selections are host-owned "
        "and removed from this pass. CATALOG="
        + json.dumps({
            **({"declared_operation_dependencies": dependency_contracts} if dependency_contracts else {}),
            "legend": (
                "operation_id", "capability_id", "description", "effect", "target", "risk",
                "required_params", "candidate_status",
            ),
            "rows": rows,
            "goals": goalframes,
        }, ensure_ascii=False, separators=(",", ":"))
    )
    user_prompt = json.dumps({
        "original_text": original_text,
        "bounded_session_context": _semantic_discovery_context_for_model(session_context),
        "host_owned_already_selected_ids": already_selected_ids,
        "prior_selection_count": len(already_selected_ids),
    }, ensure_ascii=False, separators=(",", ":"))
    return system_prompt, user_prompt

def projection_for_kinds(registry_projection: dict[str, Any], kinds: tuple[str, ...]) -> dict[str, Any]:
    allowed = set(kinds)
    result = dict(registry_projection)
    result["entries"] = tuple(item for item in registry_projection.get("entries", ()) if str(item.get("kind")) in allowed)
    result["capability_count"] = len(result["entries"])
    return result


def _candidate_budget_groups(
    *,
    original_text: str,
    session_context: dict[str, Any],
    registry_projection: dict[str, Any],
    prompt_builder: Any = build_candidate_discovery_prompt,
) -> tuple[tuple[dict[str, Any], dict[str, Any]], ...]:
    """Partition a typed kind by context budget, never by request meaning."""
    capability_ids = tuple(
        str(item["capability_id"]) for item in registry_projection.get("entries", ())
    )
    groups: list[tuple[dict[str, Any], dict[str, Any]]] = []
    offset = 0
    while offset < len(capability_ids):
        size = min(DISCOVERY_VALUES_PER_PASS, len(capability_ids) - offset)
        while size > 0:
            group_ids = capability_ids[offset:offset + size]
            group_projection = select_semantic_projection_details(
                registry_projection, group_ids,
            )
            prompt = prompt_builder(
                original_text=original_text,
                session_context=session_context,
                registry_projection=group_projection,
            )
            budget = measure_prompt_budget(
                *prompt,
                reserved_output_tokens=CANDIDATE_DISCOVERY_RESERVED_OUTPUT_TOKENS,
                output_schema=discovery_schema_for_registered_values(
                    CANDIDATE_DISCOVERY_JSON_SCHEMA,
                    value_key="candidate_capability_ids",
                    allowed_values=group_ids,
                ),
                components=_prompt_material_components(*prompt),
                num_ctx=SEMANTIC_SELECTION_NUM_CTX,
            )
            if budget["within_budget"]:
                groups.append((group_projection, budget))
                offset += size
                break
            size -= 1
        if size == 0:
            raise ValueError(
                f"single_capability_prompt_budget_exceeded:{capability_ids[offset]}"
            )
    return tuple(groups)


def _prompt_material_components(system_prompt: str, user_prompt: str) -> dict[str, str]:
    marker = "CATALOG=" if "CATALOG=" in system_prompt else "INDEX=" if "INDEX=" in system_prompt else "DOMAINS="
    instruction, separator, registry = system_prompt.partition(marker)
    try:
        user = json.loads(user_prompt)
    except (TypeError, json.JSONDecodeError):
        user = {}
    return {
        "system_prompt": instruction + separator,
        "registry_index_or_details": registry,
        "user_request": json.dumps(user.get("original_text", ""), ensure_ascii=False),
        "bounded_session_context": json.dumps(user.get("bounded_session_context", {}), ensure_ascii=False,
                                              separators=(",", ":")),
        "input_preparation_helper_evidence": json.dumps(user.get("input_preparation", {}), ensure_ascii=False,
                                                         separators=(",", ":")),
        "identity_and_request_envelope": json.dumps({
            "request_id": user.get("request_id", ""), "identity_facts": user.get("identity_facts", {}),
            "host_owned_already_selected_ids": user.get("host_owned_already_selected_ids", ()),
            "prior_selection_count": user.get("prior_selection_count", 0),
        }, ensure_ascii=False, separators=(",", ":")),
    }


def _authoritative_prompt_details(registry_projection: dict[str, Any] | None) -> dict[str, Any]:
    if registry_projection is None:
        entries = tuple({
            "capability_id": manifest["id"], "kind": "canonical_capability",
            "description": manifest["description"], "availability": "UNKNOWN",
            "operation_contract_source": "MANIFEST", "provider_binding_status": "BOUND",
            "execution_contract_available": True, "selection_mode": "EXECUTABLE",
            "provider_ids": (manifest["provider"],),
            "operation_contracts": tuple(dict(item) for item in manifest["operation_contracts"]),
        } for manifest in load_capability_manifests())
    else:
        entries = tuple({
        "capability_id": item["capability_id"], "kind": item.get("kind"),
        # Truncate the capability-level semantic summary: full operation semantics are
        # already carried by operation_contracts rows below, so the summary is a compact
        # anchor, not a duplicate of the operation descriptions (budget compaction).
        "description": str(item.get("semantic_description") or "")[:120],
        "availability": item.get("availability_status"),
        "operation_contract_source": item.get("operation_contract_source"),
        "provider_binding_status": item.get("provider_binding_status"),
        "execution_contract_available": item.get("execution_contract_available"),
        "selection_mode": item.get("selection_mode"),
        "provider_ids": item.get("provider_ids", ()),
            "operation_contracts": tuple(
                dict(op, description=str(op.get("description") or "")[:60])
                for op in item.get("operation_contracts", ())
            ),
        } for item in registry_projection.get("entries", ()))
    capability_fields = (
        ("kind", "kind"), ("availability", "availability"),
        ("contract_source", "operation_contract_source"),
        ("binding_status", "provider_binding_status"),
        ("execution_contract", "execution_contract_available"),
        ("selection_mode", "selection_mode"), ("provider_ids", "provider_ids"),
    )
    operation_fields = (
        "operation_id", "description", "required_parameters", "optional_parameters", "effect_type",
        "target_scope", "risk_class",
    )
    operations = tuple(
        operation for item in entries for operation in item["operation_contracts"]
    )

    # Hoist only values proven identical in this exact model-selected scope.
    # This is a compact projection of the canonical registry/manifests, never
    # another source of truth, and retains every non-uniform field in rows.
    capability_defaults: dict[str, Any] = {}
    dynamic_capability_fields: list[tuple[str, str]] = []
    for serialized_name, source_name in capability_fields:
        first = entries[0].get(source_name) if entries else None
        if entries and all(item.get(source_name) == first for item in entries):
            capability_defaults[serialized_name] = first
        else:
            dynamic_capability_fields.append((serialized_name, source_name))
    operation_defaults: dict[str, Any] = {}
    dynamic_operation_fields: list[str] = []
    for field in operation_fields:
        first = operations[0].get(field) if operations else None
        if operations and all(operation.get(field) == first for operation in operations):
            operation_defaults[field] = first
        else:
            dynamic_operation_fields.append(field)
    return {
        "capability_defaults": capability_defaults,
        "operation_defaults": operation_defaults,
        "capability_legend": (
            "id", "description",
            *(name for name, _ in dynamic_capability_fields),
            "operations",
        ),
        "operation_legend": tuple(dynamic_operation_fields),
        "rows": tuple((
            item["capability_id"], item["description"],
            *(item.get(source_name) for _, source_name in dynamic_capability_fields),
            tuple(tuple(operation.get(field) for field in dynamic_operation_fields)
                  for operation in item["operation_contracts"]),
        ) for item in entries),
    }


def _compact_goalframe_prompt_records(records: tuple[dict[str, Any], ...]) -> Any:
    """Lossless uniform-field hoisting, matching the existing catalog row projection.

    Scope is model-visible goal facts only; full canonical GoalFrames remain host
    authority. Do not collapse distinct filters or choose facts from request text.
    """
    if len(records) < 2:
        return records
    common = {
        key: value for key, value in records[0].items()
        if all(key in item and item[key] == value for item in records)
    }
    if not common:
        return records
    fields = tuple(dict.fromkeys(key for item in records for key in item if key not in common))
    if any(set(item) != set(common) | set(fields) for item in records):
        return records
    compact = {"defaults": common, "legend": fields,
               "rows": tuple(tuple(item[key] for key in fields) for item in records)}
    # Never make a smaller input larger merely to force a uniform shape.
    encode = lambda value: json.dumps(value, ensure_ascii=False, separators=(",", ":"))
    return compact if len(encode(compact).encode()) < len(encode(records).encode()) else records


def build_request_understanding_prompt(*, request_id: str, original_text: str,
                                       identity: IdentityContext, session_context: dict[str, Any],
                                       input_preparation: dict[str, Any] | None = None,
                                       registry_projection: dict[str, Any] | None = None) -> tuple[str, str]:
    details = _authoritative_prompt_details(registry_projection)
    preparation = dict(input_preparation or {})
    preparation.pop("original_text", None)
    quality_metadata = preparation.get("input_quality_metadata")
    if isinstance(quality_metadata, dict):
        semantic_quality_metadata = dict(quality_metadata)
        semantic_quality_metadata.pop("stt_confidence", None)
        semantic_quality_metadata.pop("input_confidence", None)
        preparation["input_quality_metadata"] = semantic_quality_metadata
    if preparation.get("safe_normalized_text") == original_text:
        preparation.pop("safe_normalized_text", None)
    preparation = {key: value for key, value in preparation.items() if value not in ("", (), {}, None, 0.0, False)}
    if preparation.get("input_channel") == "unknown":
        preparation.pop("input_channel", None)
    context_for_prompt = _semantic_context_for_model(session_context)
    # Instructions follow the already model-selected typed contracts. Unrelated
    # workflow syntax used to consume the referential context's input budget,
    # even for a single memory read that has no logical_spec parameter.
    selected_parameters = {
        name
        for operation in load_operation_catalog(registry_projection)
        for name in (*operation.get("required_parameters", ()), *operation.get("optional_parameters", ()))
    }
    scoped_operation_owner_law = (
        "Operations and required executable capabilities must match exactly. Top-level fields use maximum step severity. "
        if registry_projection is not None else ""
    )
    model_output_shape_law = (
        "Exact keys: schema_version, language, response_requirements, operation_requirements, current_topic, "
        "unresolved_reference, confidence, reason_codes. "
        "Host hydrates canonical goals, capability IDs and contract effect/risk fields; never emit them. "
        if registry_projection is not None else
        "Use exactly the supplied request_understanding schema keys. "
    )
    logical_spec_law = (
        "logical_spec is a provider-neutral DAG using the schema's actions. condition/route/merge are control flow. "
        "semantic_requirements contains only {requirement_id,step_id}, covering every "
        "CANONICAL_ARTIFACT_OPERATIONS item exactly once without recreating its facts. ASSIGN=set_field; "
        "TRANSFORM=transform. Every other operation uses one real catalog_query, selected jarvis_capability, or "
        "source-grounded http_request; never set_field or control flow. Every real operation step has a canonical "
        "requirement reference; artifact creation itself is not a step. catalog_query.semantic_operation states the "
        "intended action, not its broad class. Preserve canonical provider/provenance; SOURCE_EXPLICIT has empty "
        "inference, SEMANTIC_INFERENCE has justification. arguments uses semantic display names, never guessed "
        "installed names. jarvis_capability requires another selected capability and never substitutes a named "
        "provider. trigger is the manual|schedule|webhook literal when intrinsic. "
        if registry_projection is not None and "logical_spec" in selected_parameters else ""
    )
    canonical_goals = tuple({
        "goal_id": str(item.get("goal_id", "")),
        "requested_outcome": str(item.get("requested_outcome", ""))[:120],
        **({"memory_filter": item["memory_filter"]} if item.get("memory_filter") is not None else {}),
    } for item in (registry_projection or {}).get("selection_goalframes", ()))
    prompt_goals = _compact_goalframe_prompt_records(canonical_goals)
    canonical_artifact_operations = tuple({
        "requirement_id": str(item.get("requirement_id", "")),
        "goal_id": str(item.get("goal_id", "")),
        "operation_class": str(item.get("operation_class", "")),
        "source_grounding": str(item.get("source_grounding", "")),
        "provider_name": str(item.get("provider_name", "")),
        "provider_provenance": str(item.get("provider_provenance", "NONE")),
    } for item in (registry_projection or {}).get("selection_artifact_operation_requirements", ()))
    system_prompt = (
        "Create request_understanding.v2 from meaning, context and typed CATALOG. Return only its JSON object. "
        + model_output_shape_law +
        "response_requirements is an array of {response_requirement_id,applies_to_goal_ids,description?}; applies "
        "only to CANONICAL_GOALS IDs. operation_requirements is an "
        "object keyed by every selected operation ID; each value contains ONLY its required and supplied optional "
        "parameters from the operation schema. "
        + logical_spec_law +
        "Only original_text creates goals; context resolves references. Named instruments/actions stay operational. "
        "NO_EXECUTE removes execute only, never create/modify; GoalFrame owns the restriction. "
        "Host owns identity/registry/provider/policy/evidence/receipts; use listed IDs. "
        + scoped_operation_owner_law
        + ("A CANONICAL_GOAL memory_filter is already authoritative meaning: copy it exactly into the selected "
        "history operation, never reinterpret its object/time scope. "
        if "memory_filter" in selected_parameters else "") +
        "Parameters are concrete original_text/context values, never placeholders. Goal IDs are opaque provenance "
        "identifiers, never filesystem paths, URLs or argument values. Extract the actual requested path or entity "
        "from original_text/context; do not substitute the goal identifier. "
        + ("memory_filter: HISTORY retrieves user/assistant conversations without verification filtering; asking "
        "for their real date does not mean verified learning. VERIFIED_EXPERIENCE retrieves completed work "
        "supported by execution evidence/review, never dialogue turns merely mentioning such work. "
        "VERIFIED_SIMULATION retrieves qualified simulation. PROVENANCE/REVIEW_STATUS include pending/rejected experiences for provenance/review "
        "questions. Choose by the requested memory object. Preserve source language/identifiers in query; avoid "
        "translation that loses lexical search terms. Use TODAY_UTC only for explicit today, ANY_TIME otherwise; "
        "EXPLICIT_RANGE requires timezone-aware bounds. Leave bounds empty for ANY_TIME/TODAY_UTC. "
        if "memory_filter" in selected_parameters else "") +
        "Evidence/provenance/review fields requested in the "
        "answer belong to response_requirements, not extra executable operations. "
        "Return compact JSON. "
        + ("CANONICAL_GOALS defaults apply to every row; legend names row fields. "
           if isinstance(prompt_goals, dict) else "")
        + "CANONICAL_GOALS="
        + json.dumps(prompt_goals, ensure_ascii=False, separators=(",", ":"))
        + " CANONICAL_ARTIFACT_OPERATIONS="
        + json.dumps(canonical_artifact_operations, ensure_ascii=False, separators=(",", ":"))
        + " CATALOG=" + json.dumps(details, ensure_ascii=False, separators=(",", ":"))
    )
    user_prompt = json.dumps({
        "request_id": request_id, "original_text": original_text,
        "input_preparation": preparation,
        "identity_facts": identity.to_read_model(), "bounded_session_context": context_for_prompt,
    }, ensure_ascii=False, separators=(",", ":"))
    return system_prompt, user_prompt


def _prepare_input(*, model_port: ModelUnderstandingPort, deadline: RequestDeadline,
                   original_text: str, input_channel: str,
                   input_quality_metadata: dict[str, Any]) -> tuple[dict[str, Any], dict[str, Any]]:
    safe_normalized = normalize_input_text(original_text)
    should_call = _helper_required(input_channel, input_quality_metadata)
    trace = {
        "helper_call_used": False,
        "helper_call_attempted": False,
        "helper_call_succeeded": False,
        "helper_raw_output_present": False,
        "helper_schema_valid": False,
        "helper_correction_valid": False,
        "semantic_correction_accepted": (
            False if input_quality_metadata.get("correction_requested") is True else None
        ),
        "helper_model_id": "",
        "original_text": original_text,
        "normalized_text": safe_normalized,
        "correction_applied": False,
        "helper_confidence": 0.0,
        "helper_failure_mode": "not_requested",
        "helper_model_call_attempted": False,
        "helper_model_call_succeeded": False,
        "helper_raw_result": None,
        "helper_parsed_result": None,
        "helper_transport_error": "",
        "helper_quality_review_attempted": False,
        "helper_quality_review_succeeded": False,
        "helper_quality_review_schema_valid": False,
        "helper_quality_review_error": "",
        "helper_quality_review_result_used": False,
        "helper_quality_review_raw_output_present": False,
        "helper_quality_review_raw_result": None,
        "helper_first_call_attempted": False,
        "helper_first_call_succeeded": False,
        "helper_first_raw_output_present": False,
        "helper_first_schema_valid": False,
        "helper_first_validation_error": "",
        "helper_first_result_used": False,
        "helper_first_raw_result": None,
        "input_channel": input_channel,
        "input_quality_metadata": dict(input_quality_metadata),
    }
    preparation = {
        "original_text": original_text,
        "safe_normalized_text": safe_normalized,
        "helper_correction_proposal": "",
        "helper_confidence": 0.0,
        "ambiguity_candidates": (),
        "input_channel": input_channel,
        "input_quality_metadata": input_quality_metadata,
    }
    correct_input = getattr(model_port, "correct_input", None)
    if not should_call:
        return preparation, trace
    trace.update({
        "helper_model_id": HELPER_INPUT_CORRECTION_MODEL_ID,
        "helper_failure_mode": "",
    })
    if not callable(correct_input):
        trace["helper_failure_mode"] = "adapter_method_unavailable"
        return preparation, trace
    try:
        result = correct_input(
            original_text=original_text, safe_normalized_text=safe_normalized,
            input_channel=input_channel, input_quality_metadata=input_quality_metadata,
            deadline=deadline,
        )
        raw_content = result.get("content", "")
        raw_output_present = isinstance(raw_content, str) and bool(raw_content.strip())
        trace.update({
            "helper_call_attempted": result.get("model_call_attempted") is True,
            "helper_call_succeeded": result.get("model_call_succeeded") is True,
            "helper_raw_output_present": raw_output_present,
            "helper_model_call_attempted": result.get("model_call_attempted") is True,
            "helper_model_call_succeeded": result.get("model_call_succeeded") is True,
            "helper_raw_result": result.get("raw_model_result"),
            "helper_first_call_attempted": result.get("model_call_attempted") is True,
            "helper_first_call_succeeded": result.get("model_call_succeeded") is True,
            "helper_first_raw_output_present": raw_output_present,
            "helper_first_raw_result": result.get("raw_model_result"),
        })
        if not result.get("ok"):
            trace["helper_failure_mode"] = "model_unavailable"
            trace["helper_transport_error"] = str(result.get("transport_error") or result.get("error") or "")
            return preparation, trace
        if not (
            trace["helper_call_attempted"]
            and trace["helper_call_succeeded"]
            and trace["helper_raw_output_present"]
        ):
            trace["helper_failure_mode"] = "unverified_model_result"
            return preparation, trace
        verification_error = _model_call_verification_error(result)
        if verification_error:
            trace["helper_failure_mode"] = "invalid_correction"
            trace["helper_first_validation_error"] = verification_error
            return preparation, trace
        correction = None
        review_prior: dict[str, Any] | None = None
        review_validation_error = ""
        try:
            correction = parse_helper_input_correction_payload(
                raw_content, expected_safe_normalized_text=safe_normalized,
            )
            trace["helper_schema_valid"] = True
            trace["helper_correction_valid"] = True
            trace["helper_first_schema_valid"] = True
            trace["helper_parsed_result"] = correction.to_read_model()
        except RepairableHelperCorrectionContradiction as exc:
            trace["helper_first_validation_error"] = str(exc)
            trace["helper_failure_mode"] = "invalid_correction"
            if input_quality_metadata.get("correction_requested") is not True:
                return preparation, trace
            review_prior = dict(exc.sanitized_payload)
            review_validation_error = str(exc)
        if (
            correction is not None
            and input_quality_metadata.get("correction_requested") is True
            and correction.no_change_needed
        ):
            review_prior = correction.to_read_model()
            review_validation_error = "correction_requested_no_change_review"
        if review_prior is not None:
            review_input = getattr(model_port, "review_input_correction", None)
            if not callable(review_input):
                trace["helper_quality_review_error"] = "adapter_method_unavailable"
                return preparation, trace
            trace["helper_quality_review_attempted"] = True
            try:
                review_result = review_input(
                    original_text=original_text, safe_normalized_text=safe_normalized,
                    input_channel=input_channel, input_quality_metadata=input_quality_metadata,
                    prior_correction=review_prior, validation_error=review_validation_error,
                    deadline=deadline,
                )
            except TimeoutError as exc:
                trace["helper_quality_review_error"] = f"TimeoutError:{exc}"
                return preparation, trace
            trace["helper_quality_review_succeeded"] = (
                review_result.get("model_call_succeeded") is True
            )
            review_raw = str(review_result.get("content", ""))
            trace["helper_quality_review_raw_output_present"] = bool(review_raw.strip())
            trace["helper_quality_review_raw_result"] = review_result.get("raw_model_result")
            if not (
                review_result.get("ok") is True
                and review_result.get("model_call_attempted") is True
                and review_result.get("model_call_succeeded") is True
                and review_result.get("raw_output_present") is True
                and review_raw.strip()
            ):
                trace["helper_quality_review_error"] = str(
                    review_result.get("transport_error")
                    or review_result.get("error")
                    or "unverified_model_result"
                )
                return preparation, trace
            try:
                verification_error = _model_call_verification_error(review_result)
                if verification_error:
                    raise ValueError(verification_error)
                correction = parse_helper_input_correction_payload(
                    review_raw, expected_safe_normalized_text=safe_normalized,
                )
            except (ValueError, TypeError, KeyError) as exc:
                trace["helper_quality_review_error"] = f"{type(exc).__name__}:{exc}"
                return preparation, trace
            trace["helper_quality_review_schema_valid"] = True
            trace["helper_correction_valid"] = True
            trace["helper_parsed_result"] = correction.to_read_model()
            trace["helper_raw_result"] = review_result.get("raw_model_result")
            trace["helper_raw_output_present"] = True
            trace["helper_call_succeeded"] = True
            trace["helper_quality_review_result_used"] = True
        else:
            trace["helper_first_result_used"] = True
    except TimeoutError:
        trace["helper_failure_mode"] = "timeout"
        return preparation, trace
    except (ValueError, TypeError, KeyError) as exc:
        trace["helper_failure_mode"] = "invalid_correction"
        if not trace["helper_first_validation_error"]:
            trace["helper_first_validation_error"] = f"{type(exc).__name__}:{exc}"
        return preparation, trace
    applied = bool(
        correction.confidence >= 0.75
        and not correction.no_change_needed
        and correction.corrected_text.strip() != safe_normalized
    )
    normalized_text = correction.corrected_text.strip() if applied else safe_normalized
    preparation.update({
        "helper_correction_proposal": correction.corrected_text,
        "helper_confidence": correction.confidence,
        "ambiguity_candidates": correction.ambiguity_candidates,
        "helper_reason_codes": correction.reason_codes,
        "normalized_text": normalized_text,
    })
    trace.update({
        "helper_call_used": True,
        "normalized_text": normalized_text,
        "correction_applied": applied,
        "semantic_correction_accepted": (
            True if applied else
            False if input_quality_metadata.get("correction_requested") is True else None
        ),
        "helper_confidence": correction.confidence,
        "helper_failure_mode": "",
    })
    return preparation, trace


def _helper_required(input_channel: str, metadata: dict[str, Any]) -> bool:
    """Use typed channel/quality facts only; user-language content is never inspected."""
    channel = str(input_channel or "unknown").strip().casefold()
    if channel in {"voice", "windows_voice_edge", "stt"}:
        return True
    if metadata.get("correction_requested") is True or metadata.get("input_incomplete") is True:
        return True
    confidence = metadata.get("stt_confidence", metadata.get("input_confidence"))
    return isinstance(confidence, (int, float)) and not isinstance(confidence, bool) and float(confidence) < 0.9


def _inject_workflow_identity(
    steps: tuple[PlanStep, ...], session_context: dict[str, Any] | None,
) -> tuple[PlanStep, ...]:
    """Inject the host-owned n8n workflow id from canonical session artifacts into
    workflow operations whose target is a previously-created workflow (modify/inspect/
    execute). The model never memorizes or regenerates the workflow id."""
    workflow_id = ""
    for artifact in (session_context or {}).get("recent_artifacts", ()) or ():
        if isinstance(artifact, dict) and artifact.get("kind") == "automation/workflow":
            workflow_id = str(artifact.get("provider_id", "")).strip()
            if workflow_id:
                break
    if not workflow_id:
        return steps
    injected: list[PlanStep] = []
    for step in steps:
        if step.operation in {"execute_workflow", "modify_workflow", "inspect_workflow"}:
            params = dict(step.parameters)
            if "workflow_id" not in params:
                params["workflow_id"] = workflow_id
            step = replace(step, parameters=tuple(params.items()))
        injected.append(step)
    return tuple(injected)


def _apply_execution_restriction(steps: tuple[PlanStep, ...], restriction: str) -> tuple[PlanStep, ...]:
    """Typed execution restriction: NO_EXECUTE / PREPARE_ONLY never erase create/modify —
    they only forbid the run/execute step. Enforced host-side even if the model emitted an
    execute operation, so the restriction is not merely a prompt hint."""
    if restriction not in {"NO_EXECUTE", "PREPARE_ONLY"}:
        return steps
    return tuple(
        step for step in steps
        if step.effect_type != "EXECUTE"
        or (step.target_scope == "local_simulation_runtime" and not step.external_side_effect)
    )


def _logical_spec_coverage_reasons(understanding: RequestUnderstanding) -> tuple[str, ...]:
    """Generic semantic-coverage guard: a logical_spec that is a homogeneous chain of
    set_field primitives (>= 2 steps, and NO catalog_query / condition / transform /
    http_request step) cannot satisfy a non-intrinsic operational goal and is flagged as
    semantic degeneration. Typed only — no user-text keyword matching."""
    reasons: list[str] = []
    for requirement in understanding.operation_requirements:
        if requirement.operation_id != "create_workflow":
            continue
        spec: Any = None
        for name, value in requirement.parameters:
            if name == "logical_spec":
                spec = value
                break
        if isinstance(spec, str):
            try:
                spec = json.loads(spec)
            except (ValueError, TypeError):
                continue
        steps = spec.get("steps") if isinstance(spec, dict) else None
        if not isinstance(steps, list):
            continue
        selected_capability_ids = {
            item.capability_id for item in understanding.required_capabilities if item.required
        }
        trigger = spec.get("trigger")
        if isinstance(trigger, dict):
            trigger_query = normalize_input_text(
                str(trigger.get("catalog_query") or "")
            ).casefold()
            if trigger_query in {"manual", "schedule", "webhook"}:
                reasons.append("logical_spec_intrinsic_trigger_not_canonical")
            if trigger_query == normalize_input_text(requirement.operation_id).casefold():
                reasons.append("logical_spec_host_operation_used_as_artifact_trigger")
            if trigger_query in {
                normalize_input_text(item).casefold() for item in selected_capability_ids
            }:
                reasons.append("logical_spec_host_capability_used_as_artifact_trigger")
        has_non_set = any(
            isinstance(s, dict) and (
                bool(s.get("catalog_query"))
                or str(s.get("action", "")) not in ("", "set_field")
            )
            for s in steps
        )
        all_intrinsic_set = len(steps) >= 2 and not has_non_set
        recursive_bridge_present = False
        for step in steps:
            if not isinstance(step, dict) or str(step.get("action") or "") != "jarvis_capability":
                continue
            capability_id = str(step.get("capability_id") or "").strip()
            if capability_id not in selected_capability_ids:
                reasons.append("logical_spec_jarvis_capability_not_selected")
            if capability_id in {"workflow_automation:n8n", "conversation.respond"}:
                reasons.append("logical_spec_jarvis_capability_recursive_or_non_executable")
                recursive_bridge_present = True
        by_id = {
            str(step.get("step_id") or ""): step for step in steps
            if isinstance(step, dict) and step.get("step_id")
        }
        canonical_requirements_bound = "_canonical_requirement_ids" in spec
        expected_requirement_ids = tuple(
            str(item) for item in spec.get("_canonical_requirement_ids") or () if str(item)
        )
        semantic_requirements = tuple(spec.get("semantic_requirements") or ())
        covered_requirement_ids = tuple(
            str(item.get("requirement_id") or "") for item in semantic_requirements
            if isinstance(item, dict)
        )
        if canonical_requirements_bound and set(expected_requirement_ids) - set(covered_requirement_ids):
            reasons.append("logical_spec_canonical_requirement_missing")
        if canonical_requirements_bound and set(covered_requirement_ids) - set(expected_requirement_ids):
            reasons.append("logical_spec_unknown_requirement_reference")
        if len(covered_requirement_ids) != len(set(covered_requirement_ids)):
            reasons.append("logical_spec_duplicate_requirement_coverage")
        covered_step_ids = {
            str(item.get("step_id") or "") for item in semantic_requirements
            if isinstance(item, dict)
        }
        if any(
            str(step.get("action") or "") in {"catalog_query", "jarvis_capability", "http_request"}
            and str(step.get("step_id") or "") not in covered_step_ids
            and not (recursive_bridge_present and str(step.get("action") or "") == "jarvis_capability")
            for step in steps if isinstance(step, dict)
        ):
            reasons.append("logical_spec_unreferenced_real_operation_step")
        for semantic in semantic_requirements:
            if not isinstance(semantic, dict):
                reasons.append("logical_spec_invalid_semantic_requirement")
                continue
            grounding = str(semantic.get("source_grounding") or "")
            step = by_id.get(str(semantic.get("step_id") or ""))
            if step is None:
                reasons.append("logical_spec_semantic_requirement_step_missing")
                continue
            operation_class = str(semantic.get("operation_class") or "")
            action = str(step.get("action") or "")
            if operation_class == "ASSIGN" and action != "set_field":
                reasons.append("logical_spec_assignment_not_set_field")
            elif operation_class == "TRANSFORM" and action != "transform":
                reasons.append("logical_spec_transform_not_transform")
            elif operation_class not in {"ASSIGN", "TRANSFORM"}:
                if action == "set_field":
                    reasons.append("logical_spec_real_operation_misrepresented_as_set_field")
                elif action not in {"catalog_query", "jarvis_capability", "http_request"}:
                    reasons.append("logical_spec_real_operation_not_operational_step")
            if action == "catalog_query" and normalize_input_text(
                str(step.get("semantic_operation") or "")
            ).casefold() == normalize_input_text(operation_class).casefold():
                reasons.append("logical_spec_catalog_operation_repeats_semantic_class")
            provider_name = str(semantic.get("provider_name") or "").strip()
            provider_provenance = str(semantic.get("provider_provenance") or "NONE")
            if provider_name:
                step_provider = str(step.get("provider_name") or "").strip()
                normalized_required = normalize_input_text(provider_name.replace("_", " ").replace("-", " ")).casefold()
                normalized_step = normalize_input_text(step_provider.replace("_", " ").replace("-", " ")).casefold()
                if action != "catalog_query" or normalized_step != normalized_required:
                    reasons.append("logical_spec_explicit_provider_constraint_not_covered")
                if str(step.get("provider_provenance") or "") != provider_provenance:
                    reasons.append("logical_spec_provider_provenance_mismatch")
                if provider_provenance == "SOURCE_EXPLICIT" and str(
                    step.get("provider_inference_justification") or ""
                ).strip():
                    reasons.append("logical_spec_explicit_provider_has_inference")
            if not _source_contains_grounding(understanding.original_text, grounding):
                reasons.append("logical_spec_semantic_requirement_not_source_grounded")
        if all_intrinsic_set:
            reasons.append("logical_spec_all_intrinsic_set_no_capability_coverage")
    return tuple(reasons)


def _validate_understanding_semantics(understanding: RequestUnderstanding) -> dict[str, object]:
    """Combine typed safety with exact current-source provenance verification."""
    result = dict(validate_structured_safety(understanding))
    reasons = list(result.get("reason_codes", ())) if not result.get("valid") else []
    if (
        understanding.execution_restriction != "NONE"
        and not _source_contains_grounding(
            understanding.original_text, understanding.execution_restriction_source,
        )
    ):
        reasons.append("execution_restriction_not_source_grounded")
    result["source_provenance_valid"] = not reasons
    if reasons:
        result["valid"] = False
        result["reason_codes"] = tuple(dict.fromkeys(str(item) for item in reasons))
    return result


_EFFECT_EVIDENCE_REQUIRED = {"MUTATE", "EXECUTE", "EXPORT", "PERSIST"}


def _unproven_effects(plan: ExecutionPlan, evidence: EvidenceBundle) -> tuple[str, ...]:
    """NO_EFFECT_WITHOUT_RECEIPT: every external effect (mutate/execute/export/persist) must
    have a COMPLETE execution receipt before it may be reported as completed. Returns the
    operation ids whose effect is not yet proven by a receipt."""
    complete_steps = {receipt.step_id for receipt in evidence.receipts if receipt.status == "COMPLETE"}
    return tuple(
        step.operation for step in plan.steps
        if step.effect_type in _EFFECT_EVIDENCE_REQUIRED and step.step_id not in complete_steps
    )


def run_canonical_semantic_turn(
    *, text: str, project_port: ProjectUnderstandingPort, conversation_port: ConversationPort,
    model_port: ModelUnderstandingPort, final_brain_port: FinalBrainPort,
    permission_port: PermissionEvaluationPort, identity: IdentityContext,
    session_context: dict[str, Any] | None = None, safety_blocked: bool = False,
    provider_ports: dict[str, Any] | None = None, input_channel: str = "unknown",
    input_quality_metadata: dict[str, Any] | None = None,
    registry_projection: dict[str, Any] | None = None,
    request_id: str | None = None, trace_id: str | None = None,
    defer_final_brain: bool = False,
    session_id: str = "",
    total_timeout_seconds: float = CANONICAL_TURN_TIMEOUT_SECONDS,
    understanding_attempt_policy: UnderstandingAttemptPolicy | None = None,
    request_deadline: RequestDeadline | None = None,
) -> dict[str, Any]:
    if registry_projection is not None:
        registry_projection = validate_semantic_capability_projection(registry_projection)
    deadline = request_deadline
    if deadline is None:
        deadline = RequestDeadline(total_timeout_seconds, understanding_attempt_policy=understanding_attempt_policy)
    elif not isinstance(deadline, RequestDeadline):
        raise ValueError("canonical_request_deadline_invalid")
    elif deadline.expires_at > deadline.started_at + float(total_timeout_seconds):
        raise ValueError("canonical_request_deadline_exceeds_turn_budget")
    elif understanding_attempt_policy is not None and deadline.understanding_attempt_policy != understanding_attempt_policy:
        raise ValueError("canonical_request_deadline_attempt_policy_mismatch")
    if deadline.cancelled:
        raise TimeoutError("canonical_turn_deadline_exceeded")
    input_preparation, helper_trace = _prepare_input(
        model_port=model_port, deadline=deadline, original_text=text,
        input_channel=input_channel, input_quality_metadata=dict(input_quality_metadata or {}),
    )
    result = _run_canonical_semantic_turn_after_input(
        text=text, project_port=project_port, conversation_port=conversation_port,
        model_port=model_port, final_brain_port=final_brain_port,
        permission_port=permission_port, identity=identity, session_context=session_context,
        safety_blocked=safety_blocked, provider_ports=provider_ports,
        total_timeout_seconds=max(0.001, deadline.remaining()),
        input_preparation=input_preparation, helper_trace=helper_trace,
        registry_projection=registry_projection, request_id=request_id, trace_id=trace_id,
        defer_final_brain=defer_final_brain, session_id=session_id, request_deadline=deadline,
    )
    helper_trace["understanding_model_attempts"] = list(deadline.understanding_model_attempts)
    helper_trace["understanding_model_attempt_count"] = deadline.understanding_model_attempt_count
    result.update(helper_trace)
    trace = result.get("trace")
    if isinstance(trace, dict):
        result["trace"] = {**trace, **helper_trace}
    return result


def stream_canonical_semantic_turn(**kwargs: Any) -> Iterator[dict[str, Any]]:
    """Run the same canonical turn and stream its one deferred Final Brain call."""
    trace_id = str(kwargs.pop("trace_id", "") or f"trace_{uuid4().hex}")
    request_id = str(kwargs.pop("request_id", "") or f"request_{uuid4().hex}")
    final_brain_port = kwargs["final_brain_port"]
    deadline = kwargs.pop("request_deadline", None)
    if deadline is None:
        deadline = RequestDeadline(
            kwargs.get("total_timeout_seconds", CANONICAL_TURN_TIMEOUT_SECONDS),
            understanding_attempt_policy=kwargs.get("understanding_attempt_policy"),
        )
    elif not isinstance(deadline, RequestDeadline):
        raise ValueError("canonical_request_deadline_invalid")
    try:
        yield {"event": "accepted", "status": "accepted", "trace_id": trace_id,
               "request_id": request_id, "orchestration_path": "canonical_semantic_turn_v2"}
        try:
            result = run_canonical_semantic_turn(
                **kwargs, trace_id=trace_id, request_id=request_id, defer_final_brain=True,
                request_deadline=deadline,
            )
        except Exception as exc:
            yield {
                "event": "error", "trace_id": trace_id, "request_id": request_id,
                "error_kind": "canonical_semantic_turn_exception",
                "error_message": type(exc).__name__, "response_text": "",
            }
            return
        yield {
            "event": "status", "status": "final_brain_pending" if result.get("operation_status") == "FINAL_BRAIN_PENDING" else "blocked",
            "trace_id": trace_id, "request_id": request_id,
            "stages": tuple(result.get("trace", {}).get("stages", ())) if isinstance(result.get("trace"), dict) else (),
            "helper_evidence": {
                key: result.get(key) for key in (
                    "helper_call_attempted", "helper_call_succeeded", "helper_raw_output_present",
                    "helper_schema_valid", "helper_correction_valid", "helper_call_used",
                )
            },
            "selected_capabilities": tuple(result.get("selected_capabilities", ())),
            "selected_provider_operation": tuple(result.get("selected_provider_operation", ())),
        }
        if result.get("operation_status") != "FINAL_BRAIN_PENDING":
            yield {"event": "error", "trace_id": trace_id, "request_id": request_id,
                   "error_kind": str(result.get("operation_status", "CANONICAL_TURN_BLOCKED")),
                   "error_message": str(result.get("degradation", "canonical turn did not reach Final Brain")),
                   "response_text": str(result.get("response_text", "")), "result": result}
            return
        stream_answer = getattr(final_brain_port, "stream_answer", None)
        if not callable(stream_answer):
            yield {"event": "error", "trace_id": trace_id, "request_id": request_id,
                   "error_kind": "final_brain_stream_unavailable",
                   "error_message": "Final Brain port has no streaming transport", "response_text": "", "result": result}
            return
        if deadline.cancelled:
            yield {"event": "error", "trace_id": trace_id, "request_id": request_id,
                   "error_kind": "final_brain_deadline_exceeded",
                   "error_message": "Final Brain deadline exceeded", "response_text": "", "result": result}
            return
        emitted_chunk = False
        for event in stream_answer(deadline=deadline, **dict(result["final_brain_input"])):
            if deadline.cancelled:
                yield {"event": "error", "trace_id": trace_id, "request_id": request_id,
                       "error_kind": "final_brain_deadline_exceeded",
                       "error_message": "Final Brain deadline exceeded", "response_text": "", "result": result}
                return
            event_type = str(event.get("event", ""))
            if event_type == "chunk":
                chunk = str(event.get("chunk", event.get("text", "")))
                if not chunk:
                    continue
                emitted_chunk = True
                yield {"event": "chunk", "trace_id": trace_id, "request_id": request_id,
                       "chunk": chunk, "text": chunk}
                continue
            if event_type == "done":
                response_text = str(event.get("response_text", "")).strip()
                generation_ok = bool(
                    emitted_chunk and response_text
                    and event.get("model_call_attempted") is True
                    and event.get("model_call_succeeded") is True
                    and event.get("raw_output_present") is True
                    and event.get("done") is True
                    and event.get("done_reason") != "length"
                    and event.get("truncation") is False
                )
                if not generation_ok:
                    yield {"event": "error", "trace_id": trace_id, "request_id": request_id,
                           "error_kind": "final_brain_empty_result",
                           "error_message": "Final Brain returned no visible answer", "response_text": "", "result": result}
                    return
                result["response_text"] = response_text
                _record_stream_completed_conversation_response(result)
                result["generation_completed"] = True
                result["delivery_completed"] = None
                result["response_execution_status"] = "GENERATION_COMPLETE_DELIVERY_UNKNOWN"
                result["operation_status"] = (
                    "PARTIAL_APPROVAL_REQUIRED" if result.get("approval_required_steps")
                    else "PARTIAL_POLICY_DENIED" if result.get("policy_denied_steps")
                    else "PARTIAL_UNAVAILABLE" if result.get("provider_unavailable_steps") else "COMPLETE"
                )
                trace = dict(result.get("trace", {}))
                trace["final_brain_status"] = "COMPLETE"
                trace["stages"] = tuple(trace.get("stages", ())) + ("final_brain_stream",)
                result["trace"] = trace
                telemetry_keys = (
                    "model", "model_id", "done", "done_reason", "prompt_eval_count", "eval_count",
                    "prompt_eval_duration", "eval_duration", "load_duration", "total_duration",
                    "configured_num_ctx", "requested_num_ctx", "observed_context_length",
                    "truncation", "context_authority_source", "prompt_budget",
                )
                telemetry = {key: event.get(key) for key in telemetry_keys}
                result["final_brain_telemetry"] = telemetry
                yield {
                    "event": "done", "trace_id": trace_id, "request_id": request_id,
                    "response_text": response_text, "result": result, **telemetry,
                }
                return
            if event_type == "error":
                yield {**event, "event": "error", "trace_id": trace_id, "request_id": request_id,
                       "result": result}
                return
        yield {"event": "error", "trace_id": trace_id, "request_id": request_id,
               "error_kind": "final_brain_stream_incomplete",
               "error_message": "Final Brain stream ended without terminal event", "response_text": "", "result": result}
    finally:
        deadline.cancel()


def _record_stream_completed_conversation_response(result: dict[str, Any]) -> None:
    plan = result.get("execution_plan") if isinstance(result.get("execution_plan"), dict) else {}
    evidence = result.get("evidence_bundle") if isinstance(result.get("evidence_bundle"), dict) else {}
    steps = tuple(step for step in plan.get("steps", ()) if (
        isinstance(step, dict) and step.get("capability_id") == "conversation.respond"
        and step.get("operation") == "respond"
    ))
    if not steps or not evidence:
        return
    receipts = list(evidence.get("receipts", ()))
    for step in steps:
        receipts.append(ExecutionReceipt(
            receipt_id=f"{result['trace_id']}:{step['step_id']}:final_brain",
            request_id=str(plan["request_id"]), trace_id=str(result["trace_id"]),
            step_id=str(step["step_id"]), capability_id="conversation.respond", operation_id="respond",
            provider_id="existing_jarvis_final_brain", status="COMPLETE",
            result="visible Final Brain stream completed and canonically validated",
        ).to_read_model())
    evidence["receipts"] = tuple(receipts)
    result["evidence_bundle"] = evidence
    truths = [dict(item) for item in result.get("capability_truth", ())]
    for truth in truths:
        if truth.get("capability_id") != "conversation.respond":
            continue
        matching = tuple(receipt for receipt in receipts if (
            receipt.get("request_id") == plan.get("request_id")
            and receipt.get("trace_id") == result.get("trace_id")
            and receipt.get("capability_id") == "conversation.respond"
            and receipt.get("operation_id") == "respond"
            and receipt.get("provider_id") == "existing_jarvis_final_brain"
            and receipt.get("status") == "COMPLETE"
        ))
        truth["executed"] = bool(matching)
        truth["execution_receipt_present"] = bool(matching)
        truth["step_execution_truth"] = tuple({
            "request_id": plan.get("request_id"), "trace_id": result.get("trace_id"),
            "step_id": step["step_id"], "capability_id": "conversation.respond",
            "operation_id": "respond", "provider_id": "existing_jarvis_final_brain",
            "executed": True, "execution_receipt_present": True,
            "receipt_ids": tuple(receipt["receipt_id"] for receipt in matching
                                 if receipt.get("step_id") == step["step_id"]),
            "execution_status": "COMPLETE", "evidence_items": (),
        } for step in steps)
    result["capability_truth"] = tuple(truths)


def _inject_artifact_capabilities(
    projection: dict[str, Any] | None,
    full_projection: dict[str, Any] | None,
    session_context: dict[str, Any] | None,
) -> dict[str, Any] | None:
    """Deterministically include the owning semantic capability of recent session artifacts.

    A recent typed artifact (e.g. kind=automation/workflow, provider=n8n) contributes its
    owning capability to the candidate set so a follow-up reference can be planned. This is
    host truth (artifact provider -> registered capability), never raw-text routing.
    """
    if not isinstance(projection, dict) or not isinstance(full_projection, dict):
        return projection
    providers = {
        str(a.get("provider", ""))
        for a in (session_context or {}).get("recent_artifacts", ())
        if isinstance(a, dict)
    }
    if not providers:
        return projection
    full_by_id = {str(e["capability_id"]): e for e in full_projection.get("entries", ())}
    current_ids = {str(e["capability_id"]) for e in projection.get("entries", ())}
    added: list[dict[str, Any]] = []
    for cap_id, entry in full_by_id.items():
        # Only executable owners (execution_contract_available) — excludes stale
        # external_adapter:* shadow entries that share the provider suffix.
        if entry.get("execution_contract_available") is not True:
            continue
        for provider in providers:
            if provider and cap_id.endswith(":" + provider) and cap_id not in current_ids:
                added.append(dict(entry))
    if not added:
        return projection
    result = dict(projection)
    result["entries"] = tuple(projection.get("entries", ())) + tuple(added)
    result["capability_count"] = len(result["entries"])
    return result


def _run_canonical_semantic_turn_after_input(
    *, text: str, project_port: ProjectUnderstandingPort, conversation_port: ConversationPort,
    model_port: ModelUnderstandingPort, final_brain_port: FinalBrainPort,
    permission_port: PermissionEvaluationPort, identity: IdentityContext,
    session_context: dict[str, Any] | None = None, safety_blocked: bool = False,
    provider_ports: dict[str, Any] | None = None,
    total_timeout_seconds: float = CANONICAL_TURN_TIMEOUT_SECONDS,
    input_preparation: dict[str, Any] | None = None,
    helper_trace: dict[str, Any] | None = None,
    registry_projection: dict[str, Any] | None = None,
    request_id: str | None = None, trace_id: str | None = None,
    defer_final_brain: bool = False,
    session_id: str = "",
    request_deadline: RequestDeadline | None = None,
) -> dict[str, Any]:
    del safety_blocked  # Policy is applied after semantic understanding, never by phrase pre-routing.
    request_id = request_id or f"request_{uuid4().hex}"
    trace_id = trace_id or f"trace_{uuid4().hex}"
    helper_trace = helper_trace if isinstance(helper_trace, dict) else {}
    stages = ["api", "identity_context", "input_normalization"]
    if helper_trace.get("helper_call_used"):
        stages.append("helper_input_correction")
    stages.append("bounded_session_context")
    deadline = request_deadline or RequestDeadline(total_timeout_seconds)
    bounded_context = dict(session_context or {})
    understanding_projection = registry_projection
    if registry_projection is not None:
        stages.append("model_capability_discovery")
        trace_stage("CANDIDATE_DISCOVERY_STARTED", deadline_remaining=deadline.remaining())
        understanding_projection = _model_selected_registry_details(
            model_port=model_port, deadline=deadline, original_text=text,
            session_context=bounded_context, registry_projection=registry_projection,
            audit_trace=helper_trace, request_id=request_id, identity=identity,
            input_preparation=dict(input_preparation or {}),
        )
        if understanding_projection is None:
            trace_stage("CANDIDATE_DISCOVERY_COMPLETED", "FAILED", error_class="candidate_discovery_invalid")
            return _failure(trace_id, request_id, stages, "UNDERSTANDING_UNAVAILABLE", "model_candidate_discovery_invalid")
        trace_stage("CANDIDATE_DISCOVERY_COMPLETED", "COMPLETED", deadline_remaining=deadline.remaining())
        understanding_projection = _inject_artifact_capabilities(
            understanding_projection, registry_projection, bounded_context,
        )
        stages.append("model_operation_discovery")
        trace_stage("OPERATION_SELECTION_STARTED", deadline_remaining=deadline.remaining())
        understanding_projection = _model_selected_operation_details(
            model_port=model_port, deadline=deadline, original_text=text,
            session_context=bounded_context, registry_projection=understanding_projection,
            audit_trace=helper_trace,
        )
        if understanding_projection is None:
            trace_stage("OPERATION_SELECTION_COMPLETED", "FAILED", error_class="operation_discovery_invalid")
            return _failure(
                trace_id, request_id, stages, "UNDERSTANDING_UNAVAILABLE",
                "model_operation_discovery_invalid",
            )
        trace_stage("OPERATION_SELECTION_COMPLETED", "COMPLETED", deadline_remaining=deadline.remaining())
        scoped_understanding = (
            getattr(model_port, "supports_call_scoped_understanding_schema", False) is True
        )
        stages.append("request_understanding_prompt_admission")
        candidate_ids = tuple(
            str(item["capability_id"])
            for item in understanding_projection.get("entries", ())
        )
        candidate_trace = helper_trace.get("candidate_discovery")
        continuation_passes = list(
            candidate_trace.get("continuation_passes", ())
            if isinstance(candidate_trace, dict) else ()
        )
        try:
            if not scoped_understanding:
                # Compatibility-only ports own their historical full understanding
                # payload and cannot consume the lazy call-scoped schema. Their model
                # output remains strictly parsed below, without host schema hydration.
                admitted_ids = candidate_ids
            else:
                admitted_ids = _consolidate_for_understanding_budget(
                    call=model_port.discover_candidates,
                    candidate_ids=candidate_ids,
                    request_id=request_id,
                    original_text=text,
                    identity=identity,
                    session_context=bounded_context,
                    input_preparation=dict(input_preparation or {}),
                    registry_projection=understanding_projection,
                    deadline=deadline,
                    trace=continuation_passes,
                    audit_trace=helper_trace.setdefault("model_discovery_attempts", []),
                    repair_state=helper_trace,
                    preserve_model_selected_scope=True,
                )
            prior_projection = understanding_projection
            understanding_projection = select_semantic_projection_details(
                prior_projection, admitted_ids,
            )
            for provenance_key in (
                "selection_goalframes", "selection_artifact_operation_requirements",
                "selection_capability_justifications", "selection_response_requirements",
                "selection_execution_restriction",
                "selection_execution_restriction_source", "candidate_stage_status",
            ):
                if provenance_key in prior_projection:
                    understanding_projection[provenance_key] = prior_projection[provenance_key]
            if isinstance(candidate_trace, dict):
                candidate_trace["candidate_capability_ids"] = admitted_ids
                candidate_trace["continuation_passes"] = tuple(continuation_passes)
                candidate_trace["understanding_budget_admission_after_operation_discovery"] = True
        except (TimeoutError, ValueError, TypeError, KeyError, json.JSONDecodeError) as exc:
            helper_trace["understanding_prompt_admission_error"] = f"{type(exc).__name__}:{exc}"
            return _failure(
                trace_id, request_id, stages, "UNDERSTANDING_UNAVAILABLE",
                "request_understanding_prompt_admission_invalid",
            )
    stages.append("model_understanding")
    trace_stage("REQUEST_UNDERSTANDING_STARTED", deadline_remaining=deadline.remaining())
    understanding = _understand(
        model_port, deadline, request_id, text, identity, bounded_context,
        input_preparation=dict(input_preparation or {}), audit_trace=helper_trace,
        registry_projection=(
            understanding_projection
            if getattr(model_port, "supports_call_scoped_understanding_schema", False) is True
            else None
        ),
    )
    if understanding is None:
        trace_stage("REQUEST_UNDERSTANDING_COMPLETED", "FAILED", error_class="model_understanding_invalid")
        return _failure(trace_id, request_id, stages, "UNDERSTANDING_UNAVAILABLE", "model_understanding_invalid")
    trace_stage("REQUEST_UNDERSTANDING_COMPLETED", "COMPLETED", deadline_remaining=deadline.remaining())
    stages.append("schema_validation")
    if understanding.confidence < MINIMUM_UNDERSTANDING_CONFIDENCE:
        return _failure(trace_id, request_id, stages, "UNDERSTANDING_UNRESOLVED", "model_understanding_low_confidence", understanding)
    stages.append("structured_safety_validation")
    safety = _validate_understanding_semantics(understanding)
    coverage_reasons = _logical_spec_coverage_reasons(understanding)
    if coverage_reasons:
        safety = dict(safety)
        prior_safety_reasons = () if safety.get("valid") else tuple(safety.get("reason_codes", ()))
        safety["valid"] = False
        safety["reason_codes"] = prior_safety_reasons + coverage_reasons
        safety["logical_spec_coverage_reasons"] = coverage_reasons
    if not safety["valid"]:
        helper_trace["initial_understanding_validation_reasons"] = tuple(
            str(item) for item in safety.get("reason_codes", ())
        )
        stages.append("bounded_structured_semantics_repair")
        repaired = _understand(
            model_port, deadline, request_id, text, identity, bounded_context,
            replan_reason="contract_violations:" + ",".join(str(item) for item in safety["reason_codes"]),
            input_preparation=dict(input_preparation or {}), audit_trace=helper_trace,
            registry_projection=understanding_projection,
        )
        repaired_safety = _validate_understanding_semantics(repaired) if repaired is not None else safety
        repaired_coverage = _logical_spec_coverage_reasons(repaired) if repaired is not None else coverage_reasons
        helper_trace["understanding_repair_succeeded"] = bool(
            repaired is not None and repaired_safety["valid"] and not repaired_coverage
        )
        if repaired is None or not repaired_safety["valid"] or repaired_coverage:
            return _failure(trace_id, request_id, stages, "SAFETY_VALIDATION_FAILED", "structured_semantics_inconsistent",
                            repaired or understanding, safety_validation=repaired_safety)
        understanding, safety = repaired, repaired_safety

    required_capabilities = tuple(dict.fromkeys(
        item.capability_id for item in understanding.required_capabilities if item.required
    ))
    if not required_capabilities:
        return _failure(trace_id, request_id, stages, "UNRESOLVED_CAPABILITY", "required_capability_missing", understanding,
                        safety_validation=safety)
    stages.append("registry_discovery")
    providers = _discover_providers(required_capabilities, understanding_projection)
    operation_error = _operation_resolution_error(understanding, required_capabilities, providers, understanding_projection)
    if operation_error:
        stages.append("bounded_semantic_replan")
        replanned = _understand(model_port, deadline, request_id, text, identity, bounded_context,
                                replan_reason=operation_error, input_preparation=dict(input_preparation or {}),
                                audit_trace=helper_trace, registry_projection=understanding_projection)
        if replanned is not None:
            understanding = replanned
            safety = _validate_understanding_semantics(understanding)
            required_capabilities = tuple(dict.fromkeys(
                item.capability_id for item in understanding.required_capabilities if item.required
            ))
            providers = _discover_providers(required_capabilities, understanding_projection)
            operation_error = _operation_resolution_error(understanding, required_capabilities, providers, understanding_projection)
    if operation_error:
        result = _failure(trace_id, request_id, stages, "UNRESOLVED_OPERATION", operation_error, understanding,
                          selected_capabilities=required_capabilities, safety_validation=safety)
        result["capability_truth"] = _projection_capability_truth(
            required_capabilities, understanding_projection, identity=identity,
        )
        return result

    stages.append("semantic_plan")
    steps = tuple(PlanStep(
        step_id=f"step_{index}", goal_id=understanding.goals[min(index - 1, len(understanding.goals) - 1)].goal_id,
        capability_id=requirement.capability_id, operation=requirement.operation_id,
        required_evidence=requirement.required_evidence, effect_type=requirement.effect_type,
        target_scope=requirement.target_scope, reversibility=requirement.reversibility,
        external_side_effect=requirement.external_side_effect, risk_class=requirement.risk_class,
        parameters=requirement.parameters,
        declared_prerequisite_for_operation_ids=requirement.declared_prerequisite_for_operation_ids,
    ) for index, requirement in enumerate(understanding.operation_requirements, start=1) if requirement.required)
    page_context = session_context.get("browser_page_context", {}) if isinstance(session_context, dict) else {}
    current_url = str(page_context.get("current_url", "")) if isinstance(page_context, dict) else ""
    if current_url:
        enriched_steps = []
        for step in steps:
            params = dict(step.parameters)
            if step.operation == "browser.fill_submit" and "url" not in params:
                params["url"] = current_url
            enriched_steps.append(replace(step, parameters=tuple(params.items())))
        steps = tuple(enriched_steps)
    steps = _inject_workflow_identity(steps, session_context)
    dependency_context = ExecutionPlan(request_id=request_id, steps=steps) if steps else None
    steps = _apply_execution_restriction(steps, understanding.execution_restriction)
    if not steps:
        result = _failure(trace_id, request_id, stages, "PLAN_ONLY", "no_executable_operation_requested", understanding,
                          selected_capabilities=required_capabilities, safety_validation=safety)
        result["capability_truth"] = _projection_capability_truth(
            required_capabilities, understanding_projection, identity=identity,
        )
        return result
    # The canonical /hot contract always completes a valid semantic turn through the
    # existing Final Brain. Whether the endpoint responds is host-owned orchestration
    # state, not a natural-language capability choice. Attach only the authoritative
    # manifest-backed response operation; never fabricate an operation or provider.
    if not any(
        step.capability_id == "conversation.respond" and step.operation == "respond"
        for step in steps
    ):
        response_contract = operation_contract("respond", registry_projection)
        response_provider_ids = tuple(response_contract.get("provider_ids", ())) if response_contract else ()
        if response_contract and response_contract.get("provider_id"):
            response_provider_ids += (str(response_contract["provider_id"]),)
        if (
            response_contract is None
            or response_contract.get("capability_id") != "conversation.respond"
            or "existing_jarvis_final_brain" not in response_provider_ids
        ):
            return _failure(
                trace_id, request_id, stages, "UNRESOLVED_OPERATION",
                "canonical_response_contract_unavailable", understanding,
                selected_capabilities=required_capabilities, safety_validation=safety,
            )
        steps += (PlanStep(
            step_id=f"step_{len(steps) + 1}",
            goal_id=understanding.goals[-1].goal_id,
            capability_id="conversation.respond",
            operation="respond",
            required_evidence=tuple(response_contract["evidence_kinds"]),
            effect_type=str(response_contract["effect_type"]),
            target_scope=str(response_contract["target_scope"]),
            reversibility=str(response_contract["reversibility"]),
            external_side_effect=bool(response_contract["external_side_effect"]),
            risk_class=str(response_contract["risk_class"]),
        ),)
        response_providers = _discover_providers(("conversation.respond",), registry_projection)
        if not response_providers.get("conversation.respond"):
            return _failure(
                trace_id, request_id, stages, "UNRESOLVED_OPERATION",
                "canonical_response_provider_unresolved", understanding,
                selected_capabilities=required_capabilities, safety_validation=safety,
            )
        providers = dict(providers)
        providers["conversation.respond"] = response_providers["conversation.respond"]
        stages.append("canonical_response_orchestration")
    # Existing providers can observe concrete target effects before the single
    # policy owner evaluates them. They cannot change selected operations/data.
    policy_ports = provider_ports or {
        "existing_project_workspace_tools": project_port,
        "existing_jarvis_final_brain": conversation_port,
    }
    for capability_id in tuple(dict.fromkeys(step.capability_id for step in steps)):
        provider_entry = providers.get(capability_id, ({},))[0]
        port = policy_ports.get(str(provider_entry.get("provider_id", "")))
        prepare = getattr(port, "prepare_plan_for_policy", None)
        if not callable(prepare):
            continue
        original = tuple(step for step in steps if step.capability_id == capability_id)
        try:
            prepared = prepare(plan=ExecutionPlan(request_id=request_id, steps=original), trace_id=trace_id)
            if not isinstance(prepared, ExecutionPlan) or prepared.request_id != request_id or len(prepared.steps) != len(original):
                raise ValueError("provider_effect_projection_plan_mismatch")
            immutable = ("step_id", "goal_id", "capability_id", "operation", "required_evidence", "parameters", "target_scope")
            if any(any(getattr(before, key) != getattr(after, key) for key in immutable)
                   for before, after in zip(original, prepared.steps)):
                raise ValueError("provider_effect_projection_changed_selected_operation")
        except (OSError, ValueError, TypeError) as exc:
            return _failure(trace_id, request_id, stages, "UNAVAILABLE", str(exc), understanding,
                            selected_capabilities=required_capabilities, safety_validation=safety)
        replacements = {step.step_id: step for step in prepared.steps}
        steps = tuple(replacements.get(step.step_id, step) for step in steps)
    plan = ExecutionPlan(request_id=request_id, steps=steps)

    stages.append("policy")
    permissions = tuple(permission_port.evaluate(
        capability_id=step.capability_id, operation_id=step.operation, effect_type=step.effect_type,
        target_scope=step.target_scope, reversibility=step.reversibility,
        external_side_effect=step.external_side_effect, risk_class=step.risk_class,
        identity=identity, trace_id=trace_id, step_id=step.step_id,
    ) for step in steps)
    denied = next((item for item in permissions if not item.granted and not item.approval_required), None)
    approval = next((item for item in permissions if item.approval_required), None)
    # Each evaluation belongs to this concrete invocation/PlanStep. Operation
    # identity is not an authorization key: two steps may share an operation
    # while having different parameters, effects, risks or approval decisions.
    step_permissions = tuple(zip(steps, permissions))
    executable_steps = tuple(step for step, decision in step_permissions
                             if decision.granted and not decision.approval_required)
    blocked_steps = tuple(step for step, decision in step_permissions
                          if not decision.granted or decision.approval_required)
    approval_steps = tuple(step for step, decision in step_permissions if decision.approval_required)
    denied_steps = tuple(step for step, decision in step_permissions
                         if not decision.granted and not decision.approval_required)

    def _register_pending_approvals() -> tuple[dict[str, Any], ...]:
        continuation_ports = provider_ports or {
            "existing_project_workspace_tools": project_port,
            "existing_jarvis_final_brain": conversation_port,
        }
        pending_records: list[dict[str, Any]] = []
        for pending_step in approval_steps:
            pending_permission = next((item for item in permissions if item.step_id == pending_step.step_id), None)
            if pending_permission is None:
                continue
            provider_entry = providers.get(pending_step.capability_id, ({},))[0]
            continuation_port = continuation_ports.get(str(provider_entry.get("provider_id", "")))

            def _resume(approved_decision: Any, *, _step: PlanStep = pending_step, _port: Any = continuation_port) -> dict[str, Any]:
                if _port is None:
                    return {"status": "UNAVAILABLE", "reason": "provider_port_unavailable"}
                resumed_plan = ExecutionPlan(request_id=request_id, steps=(_step,))
                resumed_bundle = _execute_evidence(
                    understanding, resumed_plan, trace_id, identity,
                    _select_relevant_session_context(bounded_context, understanding),
                    RequestDeadline(120.0), (_step.capability_id,),
                    {_step.capability_id: _port}, (approved_decision,), dependency_plan=dependency_context,
                )
                return {"status": resumed_bundle.status, "evidence_bundle": resumed_bundle.to_read_model(),
                        "execution_plan": resumed_plan.to_read_model(),
                        "input_text": text, "understanding": understanding.to_read_model()}

            pending_records.append(CANONICAL_HOST_APPROVAL_STORE.create(
                request_id=request_id, session_id=session_id, decision=pending_permission,
                plan_step=pending_step.to_read_model(),
                description=f"Approve {pending_step.capability_id}.{pending_step.operation}", resume=_resume,
            ).to_read_model())
        return tuple(pending_records)

    if (denied is not None or approval is not None) and not executable_steps:
        blocked_truth = tuple({
            "capability_id": capability_id, "capability_exists": True,
            "provider_id": str(providers[capability_id][0].get("provider_id", "")),
            "provider_exists": bool(providers[capability_id][0].get("provider_exists", True)),
            "provider_available": providers[capability_id][0].get("provider_available"),
            "identity_eligible": bool(identity.trusted), "policy_execution_allowed": False,
            "permissions_granted": False, "executed": False, "execution_receipt_present": False,
        } for capability_id in required_capabilities)
        provider_unavailable = any(item["provider_available"] is False for item in blocked_truth)
        status = "UNAVAILABLE" if provider_unavailable else "DENIED" if denied is not None else "APPROVAL_REQUIRED"
        decision = denied or approval
        result = _failure(trace_id, request_id, stages, status,
                          ("provider_unavailable" if provider_unavailable else decision.denial_reason or "policy_requires_approval"),
                          understanding, selected_capabilities=required_capabilities,
                          permission=tuple(item.to_read_model() for item in permissions), safety_validation=safety)
        result["execution_plan"] = plan.to_read_model()
        result["selected_provider_operation"] = tuple(step.operation for step in steps)
        result["capability_truth"] = blocked_truth
        result["approval_required_steps"] = tuple(step.to_read_model() for step in approval_steps)
        result["policy_denied_steps"] = tuple(step.to_read_model() for step in denied_steps)
        result["pending_approvals"] = _register_pending_approvals()
        return result

    execution_plan = ExecutionPlan(request_id=request_id, steps=executable_steps)
    execution_capabilities = tuple(dict.fromkeys(step.capability_id for step in executable_steps))

    ports = provider_ports or {
        "existing_project_workspace_tools": project_port,
        "existing_jarvis_final_brain": conversation_port,
    }
    candidates: list[CapabilityCandidate] = []
    resolved_ports: dict[str, Any] = {}
    provider_unavailable_steps: tuple[PlanStep, ...] = ()
    capability_truth: list[dict[str, Any]] = []
    for capability_id in execution_capabilities:
        capability_permissions = tuple(item for item in permissions if item.capability_id == capability_id)
        provider = providers[capability_id][0]
        provider_id = str(provider["provider_id"])
        evidence_port = ports.get(provider_id)
        declared_available = provider.get("provider_available")
        if evidence_port is not None:
            health = evidence_port.health()
        else:
            health = {"status": "AVAILABLE" if declared_available is True else "UNAVAILABLE"}
        provider_available = health.get("status") == "AVAILABLE" and evidence_port is not None
        candidate = CapabilityCandidate(
            capability_id=capability_id, provider_id=provider_id,
            status="AVAILABLE" if provider_available else "UNAVAILABLE",
            permissions_granted=bool(capability_permissions) and all(item.granted for item in capability_permissions),
            healthy=provider_available,
        )
        candidates.append(candidate)
        capability_truth.append({
            "capability_id": capability_id, "capability_exists": True,
            "provider_id": provider_id, "provider_exists": bool(provider.get("provider_exists", evidence_port is not None)),
            "execution_provider_id": provider_id,
            "evidence_collector_id": (
                str(getattr(evidence_port, "evidence_collector_id", "")) if evidence_port is not None else ""
            ),
            "provider_available": provider_available,
            "identity_eligible": bool(capability_permissions),
            "policy_execution_allowed": bool(capability_permissions) and all(item.granted for item in capability_permissions),
            "permissions_granted": bool(capability_permissions) and all(item.granted for item in capability_permissions),
            "executed": False, "execution_receipt_present": False,
            "step_execution_truth": (),
        })
        if not candidate.healthy:
            provider_unavailable_steps += tuple(step for step in executable_steps if step.capability_id == capability_id)
            continue
        resolved_ports[capability_id] = evidence_port

    provider_executable_steps = tuple(
        step for step in executable_steps if step.capability_id in resolved_ports
    )
    pending_approvals = _register_pending_approvals()
    if not provider_executable_steps:
        result = _failure(trace_id, request_id, stages, "UNAVAILABLE", "all_selected_providers_unavailable", understanding,
                          selected_capabilities=required_capabilities,
                          permission=tuple(item.to_read_model() for item in permissions), safety_validation=safety)
        result["capability_truth"] = tuple(capability_truth)
        result["execution_plan"] = plan.to_read_model()
        return result
    execution_plan = ExecutionPlan(request_id=request_id, steps=provider_executable_steps)
    execution_capabilities = tuple(dict.fromkeys(step.capability_id for step in provider_executable_steps))

    stages.extend(("execution", "evidence_bundle"))
    selected_context = _select_relevant_session_context(bounded_context, understanding)
    evidence = _execute_evidence(understanding, execution_plan, trace_id, identity, selected_context, deadline,
                                 execution_capabilities, resolved_ports, permissions, dependency_plan=dependency_context)
    nonexecuted_steps = blocked_steps + provider_unavailable_steps
    if nonexecuted_steps:
        evidence = EvidenceBundle(
            request_id=evidence.request_id, capability_id=evidence.capability_id, trace_id=evidence.trace_id,
            status=evidence.status, items=evidence.items,
            limitations=evidence.limitations + tuple(
                f"step_not_executed:{step.step_id}:{step.operation}" for step in nonexecuted_steps
            ), receipts=evidence.receipts, errors=evidence.errors, capability_ids=evidence.capability_ids,
        )
        for capability_id in dict.fromkeys(step.capability_id for step in blocked_steps):
            provider = providers.get(capability_id, ({},))[0]
            capability_permissions = tuple(item for item in permissions if item.capability_id == capability_id)
            capability_item = next(
                (item for item in capability_truth if item["capability_id"] == capability_id), None,
            )
            if capability_item is None:
                capability_item = {
                    "capability_id": capability_id, "capability_exists": True,
                    "provider_id": str(provider.get("provider_id", "")),
                    "provider_exists": bool(provider.get("provider_exists")),
                    "provider_available": provider.get("provider_available"),
                    "identity_eligible": bool(identity.trusted),
                    "executed": False, "execution_receipt_present": False,
                }
                capability_truth.append(capability_item)
            capability_item.update({
                "policy_execution_allowed": False, "permissions_granted": False,
                "approval_required": any(item.approval_required for item in capability_permissions),
            })
    for item in capability_truth:
        capability_steps = tuple(step for step in steps if step.capability_id == item["capability_id"])
        if capability_steps:
            step_truth = _step_execution_truth(
                capability_steps, evidence, expected_provider_id=str(item["provider_id"]),
            )
            item["step_execution_truth"] = step_truth
            item["executed"] = bool(step_truth) and all(step["executed"] for step in step_truth)
            item["execution_receipt_present"] = bool(step_truth) and all(
                step["execution_receipt_present"] for step in step_truth
            )
    required_evidence = {kind for step in provider_executable_steps for kind in step.required_evidence}
    observed_evidence = {item.kind for item in evidence.items}
    missing_evidence = sorted(required_evidence - observed_evidence)
    unproven_effects = _unproven_effects(execution_plan, evidence)
    if (missing_evidence or evidence.status != "COMPLETE") and not nonexecuted_steps:
        stages.append("bounded_missing_evidence_replan")
        replanned = _understand(model_port, deadline, request_id, text, identity, bounded_context,
                                replan_reason="missing_required_evidence:" + ",".join(missing_evidence or evidence.errors),
                                input_preparation=dict(input_preparation or {}), audit_trace=helper_trace,
                                registry_projection=understanding_projection)
        if replanned is not None and _validate_understanding_semantics(replanned)["valid"] \
                and not _logical_spec_coverage_reasons(replanned) \
                and not _operation_resolution_error(replanned, required_capabilities, providers, understanding_projection):
            understanding = replanned
            steps = tuple(PlanStep(
                step_id=f"replan_step_{index}",
                goal_id=understanding.goals[min(index - 1, len(understanding.goals) - 1)].goal_id,
                capability_id=requirement.capability_id, operation=requirement.operation_id,
                required_evidence=requirement.required_evidence, effect_type=requirement.effect_type,
                target_scope=requirement.target_scope, reversibility=requirement.reversibility,
                external_side_effect=requirement.external_side_effect, risk_class=requirement.risk_class,
                parameters=requirement.parameters,
                declared_prerequisite_for_operation_ids=requirement.declared_prerequisite_for_operation_ids,
            ) for index, requirement in enumerate(understanding.operation_requirements, start=1) if requirement.required)
            plan = ExecutionPlan(request_id=request_id, steps=steps)
            permissions = tuple(permission_port.evaluate(
                capability_id=step.capability_id, operation_id=step.operation, effect_type=step.effect_type,
                target_scope=step.target_scope, reversibility=step.reversibility,
                external_side_effect=step.external_side_effect, risk_class=step.risk_class,
                identity=identity, trace_id=trace_id,
            ) for step in steps)
            denied = next((item for item in permissions if not item.granted and not item.approval_required), None)
            approval = next((item for item in permissions if item.approval_required), None)
            if denied is not None or approval is not None:
                status = "DENIED" if denied is not None else "APPROVAL_REQUIRED"
                decision = denied or approval
                return _failure(
                    trace_id, request_id, stages, status,
                    decision.denial_reason or "replanned_step_policy_requires_approval", understanding,
                    selected_capabilities=required_capabilities,
                    permission=tuple(item.to_read_model() for item in permissions),
                    safety_validation=_validate_understanding_semantics(understanding),
                )
            selected_context = _select_relevant_session_context(bounded_context, understanding)
            evidence = _execute_evidence(understanding, plan, trace_id, identity, selected_context, deadline,
                                         required_capabilities, resolved_ports, permissions)
            required_evidence = {kind for step in steps for kind in step.required_evidence}
            observed_evidence = {item.kind for item in evidence.items}
            missing_evidence = sorted(required_evidence - observed_evidence)
            unproven_effects = _unproven_effects(plan, evidence)
            # The Final Brain must see the replacement plan's actual receipts,
            # not the initial failed plan's execution flags.
            for item in capability_truth:
                capability_steps = tuple(step for step in steps if step.capability_id == item["capability_id"] and step.capability_id != "conversation.respond")
                if not capability_steps:
                    continue
                step_truth = _step_execution_truth(capability_steps, evidence, expected_provider_id=str(item["provider_id"]))
                item["step_execution_truth"] = step_truth
                item["executed"] = bool(step_truth) and all(value["executed"] for value in step_truth)
                item["execution_receipt_present"] = bool(step_truth) and all(value["execution_receipt_present"] for value in step_truth)
                decisions = tuple(value for value in permissions if value.capability_id == item["capability_id"])
                item["permissions_granted"] = bool(decisions) and all(value.granted for value in decisions)
                item["policy_execution_allowed"] = item["permissions_granted"]
    if missing_evidence or unproven_effects or evidence.status != "COMPLETE":
        trace = _trace(trace_id, request_id, stages, required_capabilities,
                       tuple(item.provider_id for item in candidates), "ALLOWED", evidence.status, "NOT_CALLED",
                       "missing_required_evidence")
        return {
            "handled": True, "orchestration_path": "canonical_semantic_turn_v2", "trace_id": trace_id,
            "understanding": understanding.to_read_model(), "understanding_schema_version": understanding.schema_version,
            "selected_capabilities": required_capabilities,
            "selected_provider_operation": tuple(step.operation for step in steps),
            "selection_source": "model_semantic_registry", "fallback_used": False, "fallback_reason": "",
            "capability_status": "PARTIAL", "operation_status": "PARTIAL_EVIDENCE",
            "missing_evidence": tuple(missing_evidence), "unproven_effects": tuple(unproven_effects),
            "degradation": "required_evidence_incomplete",
            "response_text": _degraded_response("required_evidence_incomplete"),
            "permission_decision": tuple(item.to_read_model() for item in permissions),
            "safety_validation": safety, "identity": identity.to_read_model(),
            "evidence_bundle": evidence.to_read_model(), "execution_plan": plan.to_read_model(),
            "trace": trace.to_read_model(), "project_tools_used": "project.read" in required_capabilities,
        }
    grounded_understanding, subject_grounding = _ground_requested_memory_subjects(
        understanding=understanding,
        goalframes=tuple((understanding_projection or {}).get("selection_goalframes", ())),
        evidence=evidence, source_text=text, session_context=selected_context,
    )
    helper_trace["subject_grounding"] = subject_grounding
    trace_stage("REQUESTED_SUBJECT_GROUNDING", "COMPLETED" if grounded_understanding is not None else "FAILED",
                safe_structure={"valid": subject_grounding["valid"], "error_count": len(subject_grounding["errors"])})
    if grounded_understanding is None:
        failed = _failure(trace_id, request_id, stages, "SUBJECT_GROUNDING_UNAVAILABLE", "requested_subject_not_grounded")
        failed.update(understanding=understanding.to_read_model(), evidence_bundle=evidence.to_read_model(), execution_plan=plan.to_read_model(),
                      subject_grounding=subject_grounding)
        return failed
    understanding = grounded_understanding
    final_payload = {
        "original_text": text, "understanding": understanding.to_read_model(),
        "execution_plan": plan.to_read_model(), "evidence_bundle": evidence.to_read_model(),
        "capability_state": tuple(capability_truth), "session_context": selected_context,
        "identity_facts": identity.to_read_model(),
    }
    if defer_final_brain:
        stages.append("final_brain_pending")
        trace = _trace(trace_id, request_id, stages, required_capabilities,
                       tuple(item.provider_id for item in candidates), "ALLOWED", evidence.status, "PENDING", "")
        return {
            "handled": True, "orchestration_path": "canonical_semantic_turn_v2", "trace_id": trace_id,
            "understanding": understanding.to_read_model(), "understanding_schema_version": understanding.schema_version,
            "selected_capabilities": required_capabilities,
            "selected_provider_operation": tuple(step.operation for step in steps),
            "selection_source": "model_semantic_registry", "fallback_used": False, "fallback_reason": "",
            "capability_status": "AVAILABLE", "operation_status": "FINAL_BRAIN_PENDING",
            "response_text": "", "permission_decision": tuple(item.to_read_model() for item in permissions),
            "safety_validation": safety, "identity": identity.to_read_model(),
            "evidence_bundle": evidence.to_read_model(), "execution_plan": plan.to_read_model(),
            "trace": trace.to_read_model(), "project_tools_used": "project.read" in required_capabilities,
            "capability_truth": tuple(capability_truth), "final_brain_input": final_payload,
            "pending_approvals": pending_approvals,
            "approval_required_steps": tuple(step.to_read_model() for step in approval_steps),
            "policy_denied_steps": tuple(step.to_read_model() for step in denied_steps),
            "provider_unavailable_steps": tuple(step.to_read_model() for step in provider_unavailable_steps),
        }

    stages.append("final_brain")
    try:
        final = final_brain_port.answer(deadline=deadline, **final_payload)
    except TimeoutError:
        final = {
            "ok": False, "response_text": "", "error": "final_brain_timeout",
            "model_call_attempted": False, "model_call_succeeded": False,
            "model_call_used": False, "raw_output_present": False,
        }
    response_text = str(final.get("response_text", "")).strip()
    final_ok = bool(
        final.get("ok") and response_text
        and final.get("model_call_attempted") is True
        and final.get("model_call_succeeded") is True
        and final.get("raw_output_present") is True
        and final.get("done") is True
        and final.get("done_reason") != "length"
        and final.get("truncation") is False
    )
    if final_ok:
        final = dict(final)
        final["model_call_used"] = True
        evidence, capability_truth = _record_completed_conversation_response(
            evidence=evidence, plan=plan, capability_truth=capability_truth,
        )
    helper_trace["final_brain_result"] = final
    trace = _trace(trace_id, request_id, stages, required_capabilities, tuple(item.provider_id for item in candidates),
                   "ALLOWED", evidence.status, "COMPLETE" if final_ok else "UNAVAILABLE", "")
    return {
        "handled": True, "orchestration_path": "canonical_semantic_turn_v2", "trace_id": trace_id,
        "understanding": understanding.to_read_model(), "understanding_schema_version": understanding.schema_version,
        "selected_capabilities": required_capabilities, "selected_provider_operation": tuple(step.operation for step in steps),
        "selection_source": "model_semantic_registry", "fallback_used": False, "fallback_reason": "",
        "capability_status": "AVAILABLE" if final_ok else "UNAVAILABLE", "operation_status": (
            "FINAL_BRAIN_UNAVAILABLE" if not final_ok else "PARTIAL_APPROVAL_REQUIRED" if approval_steps
            else "PARTIAL_POLICY_DENIED" if denied_steps
            else "PARTIAL_UNAVAILABLE" if provider_unavailable_steps else "COMPLETE"
        ),
        "missing_evidence": tuple(missing_evidence), "degradation": "" if final_ok else "final_brain_unavailable",
        "response_text": response_text or _degraded_response("final_brain"),
        "permission_decision": tuple(item.to_read_model() for item in permissions), "safety_validation": safety,
        "identity": identity.to_read_model(),
        "evidence_bundle": evidence.to_read_model(), "execution_plan": plan.to_read_model(),
        "trace": trace.to_read_model(), "project_tools_used": "project.read" in required_capabilities,
        "capability_truth": tuple(capability_truth),
        "generation_completed": final_ok, "delivery_completed": True if final_ok else False,
        "response_execution_status": "COMPLETE" if final_ok else "NOT_EXECUTED",
        "pending_approvals": pending_approvals,
        "approval_required_steps": tuple(step.to_read_model() for step in approval_steps),
        "policy_denied_steps": tuple(step.to_read_model() for step in denied_steps),
        "provider_unavailable_steps": tuple(step.to_read_model() for step in provider_unavailable_steps),
    }


def _parse_goalframe_goals(content: Any) -> list[dict[str, Any]]:
    """Parse the GoalFrame understanding output into typed goal frames."""
    raw = content
    if isinstance(content, str):
        try:
            raw = json.loads(content)
        except Exception:
            return []
    if not isinstance(raw, dict):
        return []
    goals = raw.get("goals")
    if not isinstance(goals, list):
        return []
    parsed: list[dict[str, Any]] = []
    for g in goals:
        if not isinstance(g, dict):
            continue
        gid = str(g.get("goal_id", "")).strip()
        dom = str(g.get("semantic_domain", "")).strip()
        eff = str(g.get("effect_intent", "")).strip()
        role = str(g.get("goal_role", "")).strip()
        parent_raw = g.get("parent_goal_id")
        parent = "" if parent_raw is None else str(parent_raw).strip()
        if gid and dom in _SEMANTIC_DOMAIN_SCOPES and eff in SEMANTIC_EFFECT_INTENTS:
            artifact_requirements = []
            for requirement in g.get("artifact_operation_requirements") or ():
                if not isinstance(requirement, dict):
                    continue
                artifact_requirements.append({
                    "requirement_id": str(requirement.get("requirement_id", "")).strip(),
                    "goal_id": gid,
                    "operation_class": str(requirement.get("operation_class", "")).strip(),
                    "source_grounding": str(requirement.get("source_grounding", "")).strip(),
                    "provider_name": str(requirement.get("provider_name", "")).strip(),
                    "provider_provenance": str(requirement.get("provider_provenance", "NONE")).strip(),
                    "provider_inference_justification": str(
                        requirement.get("provider_inference_justification", "")
                    ).strip(),
                })
            parsed.append({
                "goal_id": gid, "semantic_domain": dom, "effect_intent": eff,
                "requested_outcome": str(g.get("requested_outcome", "")).strip(),
                "grounding": str(g.get("grounding", "")).strip(),
                "goal_role": role, "parent_goal_id": parent,
                "subgoal_justification_kind": str(
                    g.get("subgoal_justification_kind", "NONE")
                ).strip(),
                "artifact_operation_requirements": tuple(artifact_requirements),
                **({"subject_constraints": dict(g["subject_constraints"])} if g.get("subject_constraints") is not None else {}),
                **({"memory_filter": g["memory_filter"]} if g.get("memory_filter") is not None else {}),
                **({"response_requirements": tuple(
                    dict(requirement) for requirement in raw.get("response_requirements", ())
                    if isinstance(requirement, dict) and gid in requirement.get("applies_to_goal_ids", ())
                )} if any(isinstance(requirement, dict) and gid in requirement.get("applies_to_goal_ids", ())
                    for requirement in raw.get("response_requirements", ())) else {}),
            })
    return parsed


def _parse_goalframe_semantics(content: Any) -> tuple[list[dict[str, str]], str, str]:
    raw = content
    if isinstance(content, str):
        try:
            raw = json.loads(content)
        except Exception:
            raw = {}
    if not isinstance(raw, dict):
        raw = {}
    restriction = str(raw.get("execution_restriction", "NONE")).strip()
    source = str(raw.get("execution_restriction_source", "")).strip()
    return _parse_goalframe_goals(raw), restriction, source


def _parse_artifact_operation_requirements(content: Any) -> list[dict[str, str]]:
    raw = content
    if isinstance(content, str):
        try:
            raw = json.loads(content)
        except Exception:
            return []
    if not isinstance(raw, dict) or not isinstance(raw.get("artifact_operation_requirements"), list):
        return []
    parsed = []
    for item in raw["artifact_operation_requirements"]:
        if not isinstance(item, dict):
            continue
        parsed.append({key: str(item.get(key, "")).strip() for key in (
            "requirement_id", "goal_id", "operation_class", "source_grounding", "provider_name",
            "provider_provenance", "provider_inference_justification",
        )})
    return parsed


def _attach_artifact_operation_requirements(
    goals: list[dict[str, Any]], requirements: list[dict[str, str]],
) -> list[dict[str, Any]]:
    attached = []
    for goal in goals:
        item = dict(goal)
        item["artifact_operation_requirements"] = tuple(
            requirement for requirement in requirements
            if requirement.get("goal_id") == goal.get("goal_id")
        )
        attached.append(item)
    return attached


def _requires_artifact_operations(goal: dict[str, Any]) -> bool:
    """Only artifact creation/modification needs an artifact DAG decomposition."""
    return goal.get("semantic_domain") == "automation" and goal.get("effect_intent") == "change_state"


def _extract_artifact_operation_requirements(
    *, understand: Any, deadline: RequestDeadline, original_text: str,
    goals: list[dict[str, Any]], execution_restriction_source: str,
    audit_trace: dict[str, Any] | None = None,
) -> list[dict[str, Any]] | None:
    automation_goal_ids = tuple(
        str(goal["goal_id"]) for goal in goals if _requires_artifact_operations(goal)
    )
    if not automation_goal_ids:
        return _attach_artifact_operation_requirements(goals, [])
    system_prompt, user_prompt = build_artifact_operation_extraction_prompt(
        original_text=original_text, goals=goals,
        execution_restriction_source=execution_restriction_source,
    )
    schema = json.loads(json.dumps(ARTIFACT_OPERATION_EXTRACTION_JSON_SCHEMA))
    schema["properties"]["artifact_operation_requirements"]["items"]["properties"]["goal_id"] = {
        "type": "string", "enum": list(automation_goal_ids),
    }

    repair_allowed = True
    def call(prompt: str) -> tuple[list[dict[str, Any]], tuple[tuple[str, str], ...]]:
        nonlocal repair_allowed
        result = understand(
            system_prompt=prompt, user_prompt=user_prompt, deadline=deadline, output_schema=schema,
        )
        content = result.get("content") if isinstance(result, dict) else result
        verification_error = _model_call_verification_error(result)
        if verification_error:
            violations = (("", "artifact_semantic_result_invalid:" + verification_error),)
            repair_allowed = bool(isinstance(result, dict) and result.get("model_call_succeeded") is True
                and result.get("raw_output_present") is True and result.get("truncation") is not True
                and str(result.get("done_reason", "")).lower() != "length")
            if audit_trace is not None:
                audit_trace.setdefault("artifact_operation_extraction_attempts", []).append({
                    "content": content, "violations": violations,
                    "final_valid": result.get("final_valid") if isinstance(result, dict) else None,
                    "semantic_verification_error": verification_error,
                })
            return [], violations
        requirements = _parse_artifact_operation_requirements(content)
        for requirement in requirements:
            if requirement.get("operation_class") in {"ASSIGN", "TRANSFORM"}:
                # The model owns the semantic class. Once it chose an intrinsic
                # class, the typed contract owns the absence of an external provider.
                requirement["provider_name"] = ""
                requirement["provider_provenance"] = "NONE"
                requirement["provider_inference_justification"] = ""
            elif normalize_input_text(str(requirement.get("provider_name", ""))).casefold() in {
                "none", "null", "n/a",
            }:
                # Preserve the claimed provenance so validation sees the
                # contradiction and the same semantic brain must repair it.
                requirement["provider_name"] = ""
            provider_name = requirement.get("provider_name", "")
            if provider_name and _source_mentions_provider_surface(original_text, provider_name):
                # Explicitness is source identity, therefore HOST-verifiable machine truth.
                requirement["provider_provenance"] = "SOURCE_EXPLICIT"
                requirement["provider_inference_justification"] = ""
        attached = _attach_artifact_operation_requirements(goals, requirements)
        violations = (
            _goalframe_validation_violations(attached, source_text=original_text)
            + _artifact_restriction_overlap_violations(attached, execution_restriction_source)
        )
        if audit_trace is not None:
            audit_trace.setdefault("artifact_operation_extraction_attempts", []).append({
                "content": content,
                "violations": tuple(violations),
            })
        return attached, violations

    attached, violations = call(system_prompt)
    if not violations:
        return attached
    if not repair_allowed:
        return None
    repair_prompt = system_prompt + (
        " Repair these typed extraction violations without deleting a genuine requested behavior: "
        + ";".join(f"{item}:{reason}" for item, reason in violations)
        + ". Return one complete replacement. Exact source fragments only; restrictions are never operations."
    )
    repaired, repaired_violations = call(repair_prompt)
    return None if repaired_violations else repaired


def _goalframe_restriction_violations(
    restriction: str, restriction_source: str, *, source_text: str,
) -> tuple[tuple[str, str], ...]:
    if restriction not in {"NONE", "NO_EXECUTE", "PREPARE_ONLY"}:
        return (("execution_restriction", "invalid_execution_restriction"),)
    if restriction == "NONE":
        return (() if not restriction_source else (
            ("execution_restriction", "none_restriction_has_source"),
        ))
    if not _source_contains_grounding(source_text, restriction_source):
        return (("execution_restriction", "restriction_not_source_grounded"),)
    return ()


def _artifact_restriction_overlap_violations(
    goals: list[dict[str, Any]], restriction_source: str,
) -> tuple[tuple[str, str], ...]:
    """A prohibition is authorization evidence, never an artifact operation."""
    normalized_restriction = normalize_input_text(restriction_source).casefold()
    if not normalized_restriction:
        return ()
    violations = []
    for goal in goals:
        for requirement in goal.get("artifact_operation_requirements", ()):
            grounding = normalize_input_text(str(requirement.get("source_grounding", ""))).casefold()
            restriction_prefix = normalized_restriction[:32]
            if grounding and (
                grounding in normalized_restriction
                or normalized_restriction in grounding
                or (restriction_prefix and restriction_prefix in grounding)
            ):
                violations.append((
                    str(requirement.get("requirement_id") or goal.get("goal_id") or ""),
                    "artifact_operation_is_execution_restriction",
                ))
    return tuple(violations)


def _ground_requested_memory_subjects(*, understanding: RequestUnderstanding,
        goalframes: tuple[dict[str, Any], ...], evidence: EvidenceBundle,
        source_text: str, session_context: dict[str, Any] | None = None,
        ) -> tuple[RequestUnderstanding | None, dict[str, Any]]:
    """Resolve source-backed references before the existing answer/evidence gate.

    Reuse the original GoalFrame source span and policy-controlled canonical
    readback. Explicit canonical identities retain their original path. A typed
    task descriptor copied from the source may instead join the host's existing
    same-session chronology and a canonical experience. Actor/rank/recency alone
    never selects a subject. General deictic references remain unresolved.
    """
    by_goal = {g["goal_id"]: g for g in goalframes}
    errors, resolved, requirements = [], {}, []
    for requirement in understanding.response_requirements:
        if requirement.memory_query_kind is None:
            requirements.append(requirement)
            continue
        binding = dict(requirement.subject_binding or ())
        goal = by_goal.get(binding.get("subject_goal_id"), {})
        scope = (goal.get("subject_constraints") or {}).get("scope")
        reference = goal.get("grounding", "")
        def fail(code):
            errors.append({"requirement_id": requirement.response_requirement_id, "code": code})
        if (not binding or scope != binding.get("scope") or not reference
                or not _source_contains_grounding(source_text, reference)):
            fail("requested_subject_source_anchor_unavailable")
            continue
        if scope == "EXISTENTIAL":
            # No singular subject is selected. Existing relation/evidence checks
            # still govern every positive existential claim.
            if any(binding.get(key) for key in ("experience_id", "trace_id", "request_id")):
                fail("existential_scope_has_singular_identity")
                continue
            requirements.append(requirement)
            resolved[requirement.response_requirement_id] = {"scope": "EXISTENTIAL", "subject_selected": False}
            continue
        # Source provenance validation is separate from identity comparison.
        # Opaque canonical IDs/paths must be copied exactly, not normalized into
        # existence, and actor/source/receipt existence cannot select a change.
        if not isinstance(reference, str) or reference not in source_text:
            fail("requested_subject_reference_not_exact_source")
            continue
        documents = requirement.memory_query_kind == "SOURCE_DOCUMENT"
        constraints = goal.get("subject_constraints") or {}
        # Reuse the existing task_ref semantic field, never parse request words
        # or reinterpret a failed opaque-ID lookup as a descriptive fallback.
        descriptor = (not documents and constraints.get("task_ref") == reference
                      and binding.get("task_ref") == reference
                      and not any(binding.get(key) for key in ("experience_id", "trace_id", "request_id")))
        context = session_context or {}
        contextual_traces = {
            turn["trace_id"] for turn in context.get("bounded_chronological_turns", ())
            if isinstance(turn, dict) and isinstance(turn.get("trace_id"), str) and turn["trace_id"]
        } if context.get("schema_version") == "bounded_session_context.v2" else set()
        session_id = context.get("session_id")
        candidates = {}
        for item in evidence.items:
            if item.truncated or item.kind != ("mempalace_search" if documents else "history_search"):
                continue
            try:
                observation = json.loads(item.observation)
            except (ValueError, TypeError):
                continue
            if not isinstance(observation, dict):
                fail("canonical_subject_readback_malformed")
                continue
            container = observation.get("retrieval" if documents else "history_query")
            rows = container.get("results" if documents else "matches", ()) if isinstance(container, dict) else None
            if not isinstance(rows, (list, tuple)) or any(not isinstance(row, dict) for row in rows):
                fail("canonical_subject_readback_malformed")
                continue
            if documents:
                for row in rows:
                    readbacks = row.get("source_readback") or ()
                    if not isinstance(readbacks, (list, tuple)) or any(not isinstance(value, dict) for value in readbacks):
                        fail("canonical_subject_readback_malformed")
                        continue
                    for readback in readbacks:
                        # This is the existing provider's independent file
                        # readback, never merely an indexed source label.
                        if readback.get("path") == reference and isinstance(readback.get("sha256"), str) and readback["sha256"]:
                            key = (reference, readback["sha256"])
                            candidates[key] = {"source_ref": reference}
            else:
                for row in rows:
                    if any(value is not None and not isinstance(value, str) for value in (
                            row.get(key) for key in ("experience_id", "trace_id", "request_id", "task_ref", "actor"))):
                        fail("canonical_subject_readback_malformed")
                        continue
                    # Neither actor, task similarity, source label nor a valid
                    # receipt is an independently unique requested-change ID.
                    if descriptor:
                        # Task text is a semantic constraint, not unique identity.
                        # Only independent canonical lineage into the host-owned
                        # context can establish relevance; inspect ALL candidates.
                        if (not session_id or not row.get("experience_id")
                                or row.get("task_ref") != reference
                                or row.get("trace_id") not in contextual_traces
                                or row.get("session_id") != session_id
                                or (constraints.get("actor") and row.get("actor") != constraints["actor"])):
                            continue
                    elif not any(row.get(key) == reference for key in ("experience_id", "trace_id", "request_id")):
                        continue
                    identity = {key: row[key] for key in ("experience_id", "trace_id", "request_id") if row.get(key)}
                    if not identity:
                        continue
                    key = tuple((key, row.get(key)) for key in ("experience_id", "trace_id", "request_id", "task_ref", "actor"))
                    candidates[key] = identity
        if len(candidates) != 1:
            fail("requested_subject_ambiguous" if candidates else "requested_subject_not_established")
            continue
        identity = next(iter(candidates.values()))
        if any(key in binding and binding[key] != value for key, value in identity.items()):
            fail("model_subject_proposal_conflicts_with_requested_record")
            continue
        # Add only independently grounded canonical identity. Actor, operation,
        # receipt, review and qualification constraints remain subject to the
        # SAME downstream joins; this is not another evidence relation engine.
        grounded = replace(requirement, subject_binding=tuple({**binding, **identity}.items()))
        requirements.append(grounded)
        resolved[requirement.response_requirement_id] = {
            "scope": "SUBJECT", "canonical_identity": identity,
            "resolution_basis": "SOURCE_TASK_DESCRIPTOR_AND_CANONICAL_SESSION_LINEAGE" if descriptor else "EXPLICIT_CANONICAL_REFERENCE",
        }
    proof = {"valid": not errors, "errors": errors, "requirements": resolved,
             "owner": "CONTROL_PLANE.canonical_semantic_spine", "model_proposal_is_authority": False,
             "resolution_scope": "EXPLICIT_REFERENCES_OR_TYPED_SOURCE_TASK_DESCRIPTOR_WITH_SESSION_LINEAGE",
             "descriptive_references_inferred": False, "ambiguous_subject_autoselect_count": 0}
    if errors:
        return None, proof
    return replace(understanding, response_requirements=tuple(requirements)), proof


def _source_contains_grounding(source_text: str, grounding: str) -> bool:
    """Verify copied evidence by normalization and containment, never semantic parsing."""
    normalized_source = " ".join(normalize_input_text(source_text).casefold().split())
    normalized_grounding = " ".join(normalize_input_text(grounding).casefold().split())
    return bool(normalized_grounding and normalized_grounding in normalized_source)


def _source_mentions_provider_surface(source_text: str, provider_name: str) -> bool:
    """Mechanical provider identity check tolerant only of identifier separators."""
    normalized_source = normalize_input_text(
        source_text.replace("_", " ").replace("-", " ")
    ).casefold()
    normalized_provider = normalize_input_text(
        provider_name.replace("_", " ").replace("-", " ")
    ).casefold()
    return bool(normalized_provider and normalized_provider in normalized_source)


def _goalframe_validation_violations(
    goals: list[dict[str, Any]], *, source_text: str, require_artifact_operations: bool = True,
) -> tuple[tuple[str, str], ...]:
    """Typed provenance validation for GoalFrames against the current utterance.

    This verifies evidence identity only: normalized grounding must occur in the current
    source. It does not infer meaning from words. PRIMARY_OUTCOME has no parent;
    SUBGOAL has a valid non-self parent and typed independent-binding justification;
    IDs are unique and the parent graph is acyclic."""
    violations: list[tuple[str, str]] = []
    counts: dict[str, int] = {}
    for goal in goals:
        counts[goal["goal_id"]] = counts.get(goal["goal_id"], 0) + 1
    goal_ids = set(counts)
    by_id = {g["goal_id"]: g for g in goals if counts[g["goal_id"]] == 1}
    requirement_counts: dict[str, int] = {}
    grounding_classes: dict[str, set[str]] = {}
    for goal in goals:
        for requirement in goal.get("artifact_operation_requirements", ()):
            requirement_id = str(requirement.get("requirement_id", ""))
            requirement_counts[requirement_id] = requirement_counts.get(requirement_id, 0) + 1
            normalized_requirement_grounding = normalize_input_text(
                str(requirement.get("source_grounding", ""))
            ).casefold()
            grounding_classes.setdefault(normalized_requirement_grounding, set()).add(
                str(requirement.get("operation_class", ""))
            )
    for g in goals:
        gid = g["goal_id"]
        role = g.get("goal_role", "")
        parent = g.get("parent_goal_id", "").strip()
        grounding = g.get("grounding", "").strip()
        normalized_goal_grounding = normalize_input_text(grounding).casefold()
        basis = g.get("subgoal_justification_kind", "NONE")
        artifact_requirements = tuple(g.get("artifact_operation_requirements", ()))
        if g.get("memory_filter") is not None:
            try:
                validate_memory_filter(g["memory_filter"])
            except (ValueError, TypeError, AttributeError):
                violations.append((gid, "goal_memory_filter_invalid"))
            if g.get("semantic_domain") != "memory" or g.get("effect_intent") != "retrieve":
                violations.append((gid, "goal_memory_filter_domain_effect_invalid"))
        if counts[gid] > 1:
            violations.append((gid, "duplicate_goal_id"))
        if role not in GOAL_ROLES:
            violations.append((gid, "invalid_goal_role"))
        if not _source_contains_grounding(source_text, grounding):
            violations.append((gid, "goal_not_source_grounded"))
        if require_artifact_operations and _requires_artifact_operations(g) and not artifact_requirements:
            violations.append((gid, "automation_artifact_operations_missing"))
        for requirement in artifact_requirements:
            requirement_id = str(requirement.get("requirement_id", "")).strip()
            operation_class = str(requirement.get("operation_class", "")).strip()
            operation_grounding = str(requirement.get("source_grounding", "")).strip()
            provider_name = str(requirement.get("provider_name", "")).strip()
            provider_provenance = str(requirement.get("provider_provenance", "NONE")).strip()
            inference = str(requirement.get("provider_inference_justification", "")).strip()
            violation_id = requirement_id or gid
            if not requirement_id:
                violations.append((gid, "artifact_operation_requirement_id_missing"))
            elif requirement_counts.get(requirement_id, 0) != 1:
                violations.append((requirement_id, "artifact_operation_requirement_id_not_unique"))
            if operation_class not in ARTIFACT_OPERATION_CLASSES:
                violations.append((violation_id, "artifact_operation_class_invalid"))
            if normalize_input_text(provider_name).casefold() in {
                "none", "null", "n/a", "source explicit", "source_explicit",
                "semantic inference", "semantic_inference",
            }:
                violations.append((violation_id, "artifact_provider_name_is_placeholder"))
            if not _source_contains_grounding(source_text, operation_grounding):
                violations.append((violation_id, "artifact_operation_not_source_grounded"))
            elif normalize_input_text(operation_grounding).casefold() == normalized_goal_grounding:
                violations.append((violation_id, "artifact_operation_duplicates_goal_fact"))
            elif len(operation_grounding) >= 160:
                violations.append((violation_id, "artifact_operation_grounding_not_precise"))
            elif len(grounding_classes.get(normalize_input_text(operation_grounding).casefold(), set())) > 1:
                violations.append((violation_id, "artifact_operation_grounding_reused_incompatibly"))
            if operation_class in {"ASSIGN", "TRANSFORM"} and (
                provider_name or provider_provenance != "NONE" or inference
            ):
                violations.append((violation_id, "intrinsic_artifact_operation_has_provider"))
            if operation_class in ARTIFACT_OPERATION_CLASSES \
                    and operation_class not in {"ASSIGN", "TRANSFORM"} \
                    and provider_provenance == "NONE":
                violations.append((violation_id, "real_artifact_operation_provider_missing"))
            if provider_provenance == "SOURCE_EXPLICIT":
                if not provider_name or not _source_mentions_provider_surface(source_text, provider_name):
                    violations.append((violation_id, "explicit_artifact_provider_not_source_grounded"))
                if inference:
                    violations.append((violation_id, "explicit_artifact_provider_has_inference"))
            elif provider_provenance == "SEMANTIC_INFERENCE":
                if not provider_name or not inference:
                    violations.append((violation_id, "inferred_artifact_provider_incomplete"))
                elif _source_mentions_provider_surface(source_text, provider_name):
                    violations.append((violation_id, "inferred_artifact_provider_was_source_explicit"))
            elif provider_provenance == "NONE":
                if provider_name or inference:
                    violations.append((violation_id, "provider_none_has_provider_facts"))
            else:
                violations.append((violation_id, "artifact_provider_provenance_invalid"))
        if role == "PRIMARY_OUTCOME":
            if parent:
                violations.append((gid, "primary_outcome_has_parent"))
            if basis != "NONE":
                violations.append((gid, "primary_outcome_has_subgoal_justification"))
        elif role == "SUBGOAL":
            if not parent:
                violations.append((gid, "subgoal_missing_parent"))
            elif parent not in goal_ids:
                violations.append((gid, "subgoal_parent_not_found"))
            elif parent == gid:
                violations.append((gid, "subgoal_parent_is_self"))
            if basis not in {"EXPLICIT_INTERMEDIATE", "OPERATION_DEPENDENCY"}:
                violations.append((gid, "subgoal_justification_missing"))
            if basis == "EXPLICIT_INTERMEDIATE" and parent in by_id:
                parent_grounding = by_id[parent].get("grounding", "")
                if normalize_input_text(grounding).casefold() == normalize_input_text(parent_grounding).casefold():
                    violations.append((gid, "subgoal_not_distinct_source_fragment"))
    parent_map = {g["goal_id"]: g.get("parent_goal_id", "").strip() for g in goals}
    for gid in goal_ids:
        seen: set[str] = set()
        cur = gid
        while cur and cur in parent_map:
            if cur in seen:
                violations.append((gid, "goal_parent_cycle"))
                break
            seen.add(cur)
            cur = parent_map[cur]
    return tuple(violations)


def _goalframe_response_requirement_violations(
    goals: list[dict[str, Any]], presentation: tuple[dict[str, Any], ...],
) -> tuple[tuple[str, str], ...]:
    """Reuse the canonical response contract before capability binding."""
    from MAKSIMAR_CORE_LIB.ai_orchestration.semantic_intent_contract import (
        ResponseRequirement, validate_response_requirement_goal_references,
    )
    try:
        requirements = tuple(ResponseRequirement(
            response_requirement_id=f"goalframe_response_{index}",
            applies_to_goal_ids=tuple(requirement["applies_to_goal_ids"]),
            description=requirement.get("description", ""),
            memory_query_kind=requirement.get("memory_query_kind"),
            subject_binding=requirement.get("subject_binding"),
            requirement_kind=requirement.get("requirement_kind"),
        ) for index, requirement in enumerate(presentation))
        validate_response_requirement_goal_references(
            requirements, {str(goal["goal_id"]) for goal in goals},
        )
        if any(q.subject_binding is not None and q.requirement_kind is None for q in requirements):
            raise ValueError("response_requirement_kind_required_for_bound_fact")
        by_id = {str(goal["goal_id"]): goal for goal in goals}
        for original, requirement in zip(presentation, requirements):
            # Older direct contract callers may omit this optional metadata.
            # The canonical model generation schema requires an explicit value.
            if "memory_query_kind" not in original:
                continue
            kind = requirement.memory_query_kind
            if kind is not None and kind not in MEMORY_FILTER_SCHEMA["properties"]["query_kind"]["enum"]:
                raise ValueError("response_memory_query_kind_unknown")
            for goal_id in requirement.applies_to_goal_ids:
                goal_filter = by_id[goal_id].get("memory_filter")
                if goal_filter is None:
                    if kind is not None:
                        raise ValueError("response_memory_kind_requires_memory_retrieval:" + goal_id)
                    continue
                if kind is None:
                    raise ValueError("response_memory_kind_required_for_retrieval:" + goal_id)
                requested_filter = validate_memory_filter({**goal_filter, "query_kind": kind})
                from MAKSIMAR_SERVER.AI_ORCHESTRATION.model_understanding_adapter import validate_structured_payload
                # Reuse the existing disjoint source/history contracts. This
                # validates model-selected kinds; it never selects or rewrites one.
                if not any(
                    validate_structured_payload(json.dumps(goal_filter), variant)[1]
                    and validate_structured_payload(json.dumps(requested_filter), variant)[1]
                    for variant in MEMORY_FILTER_SCHEMA["anyOf"]
                ):
                    raise ValueError("response_memory_object_incompatible_with_goal:" + goal_id)
    except (ValueError, TypeError, KeyError, AttributeError) as exc:
        return (("", str(exc)),)
    return ()


def _model_selected_registry_details_goalframe(
    *, model_port: ModelUnderstandingPort, deadline: RequestDeadline, original_text: str,
    session_context: dict[str, Any], registry_projection: dict[str, Any], audit_trace: dict[str, Any],
) -> dict[str, Any] | None:
    """GoalFrame v3 canonical discovery: one intent-understanding call -> deterministic
    safety-monotonic projection -> per-goal bounded candidate binding."""
    def presentation_from_model(content: Any) -> tuple[dict[str, Any], ...]:
        payload = json.loads(content) if isinstance(content, str) else content
        if not isinstance(payload, dict):
            return ()
        obligations = tuple(payload.get("response_requirements", ()))
        try:
            return hydrate_response_requirements(tuple(_parse_goalframe_goals(payload)), obligations)
        except (ValueError, TypeError, KeyError):
            # Retain malformed obligations for the existing typed violation/repair
            # gate. Never drop, coerce, or silently synthesize a missing facet.
            return obligations

    understand = getattr(model_port, "understand", None)
    discover_candidates = getattr(model_port, "discover_candidates", None)
    if not callable(understand) or not callable(discover_candidates):
        return None
    audit_trace["model_discovery_attempts"] = []
    def goalframe_schema_failed(result, attempt):
        if isinstance(result, dict):
            attempt["model_attempts"] = result.get("model_attempts", [])
        verification_error = (
            _model_call_verification_error(result) if isinstance(result, dict)
            else "semantic_result_envelope_not_object"
        )
        if not verification_error:
            return False
        if audit_trace.get("goalframe_repair_state") == "ATTEMPTED":
            audit_trace["goalframe_repair_state"] = "FAILED"
        attempt["semantic_verification_error"] = verification_error
        violations = (("", "goalframe_semantic_result_invalid:" + verification_error),)
        attempt["validation_violations"] = violations
        attempt["native_ok"] = result.get("ok") if isinstance(result, dict) else None
        attempt["native_schema_valid"] = result.get("schema_valid") if isinstance(result, dict) else None
        attempt["native_final_valid"] = result.get("final_valid") if isinstance(result, dict) else None
        audit_trace["candidate_discovery_error"] = "goalframe_provenance_invalid"
        audit_trace["candidate_discovery_violations"] = violations
        return True

    def source_coverage(content, *, repair_available=True):
        # This subordinate gate has no transport, deadline or authority of its own.
        verification = {"status": "UNPROVEN", "valid": False,
                        "reason": "source_candidate_verifier_unavailable", "verdict": None}
        verify = getattr(model_port, "verify_source_candidate", None)
        attempts_before = len(deadline.understanding_model_attempts)
        try:
            if not deadline.understanding_attempt_available() or deadline.cancelled or deadline.remaining() <= 0:
                verification["reason"] = "source_candidate_shared_budget_unavailable"
            elif callable(verify):
                candidate = json.loads(content) if isinstance(content, str) else content
                result = verify(source_text=original_text, candidate=candidate, deadline=deadline)
                ids = tuple(["goal:" + str(g.get("goal_id", "")) for g in candidate.get("goals", ())]
                            + ["requirement:" + str(i) for i, _ in enumerate(candidate.get("response_requirements", ()))])
                if isinstance(result, dict):
                    verification = dict(result)
                    status = validate_source_candidate_verdict(result.get("verdict"), ids)
                    call = result.get("model_call")
                    if not isinstance(call, dict) or _model_call_verification_error(call):
                        status = "UNPROVEN"
                    verification.update(status=status, valid=status == "COMPLETE")
        except Exception as exc:
            verification.update(status="UNPROVEN", valid=False,
                                reason=f"source_candidate_verification_failed:{type(exc).__name__}:{exc}")
        status = verification["status"]
        verification["repair_decision"] = (
            "ELIGIBLE" if repair_available and deadline.understanding_attempt_available()
            and not deadline.cancelled and deadline.remaining() > 0 else "UNAVAILABLE"
        ) if status == "INCOMPLETE" else "NONE"
        verification["model_attempts"] = list(deadline.understanding_model_attempts[attempts_before:])
        for raw_attempt in verification["model_attempts"]:
            if raw_attempt.get("semantic_verdict") is None:
                raw_attempt.update(semantic_verdict="UNPROVEN", semantic_reason=verification.get("reason"))
            raw_attempt["repair_decision"] = verification["repair_decision"]
        audit_trace.setdefault("goalframe_source_verifications", []).append(verification)
        if status == "COMPLETE":
            return ()
        if status == "INCOMPLETE":
            return (("", "source_candidate_incomplete:" + json.dumps(verification.get("verdict"), ensure_ascii=False)),)
        audit_trace["candidate_discovery_error"] = "goalframe_provenance_invalid"
        audit_trace["candidate_discovery_violations"] = (("", "source_candidate_" + status.lower()),)
        return None

    goalframe_repair_attempted = False
    goalframe_validation_started = False
    audit_trace["goalframe_repair_state"] = "NOT_ATTEMPTED"
    try:
        trace_stage("GOALFRAME_STARTED")
        sys_prompt, user_prompt = build_goalframe_understanding_prompt(
            original_text=original_text,
            global_projection=_compact_global_projection(registry_projection),
        )
        trace_stage(
            "GOALFRAME_INPUT_FINGERPRINT", "STARTED",
            **_goalframe_input_fingerprints(
                source_text=original_text, system_prompt=sys_prompt, user_prompt=user_prompt,
                global_projection=_compact_global_projection(registry_projection),
            ),
        )
        result = understand(system_prompt=sys_prompt, user_prompt=user_prompt, deadline=deadline,
                            output_schema=GOALFRAME_UNDERSTANDING_JSON_SCHEMA)
        goalframe_validation_started = True
        content = result.get("content") if isinstance(result, dict) else result
        first_goalframe_attempt = {"attempt": 0, "raw_model_content": content,
                                   "validation_violations": None}
        audit_trace.setdefault("goalframe_understanding_attempts", []).append(first_goalframe_attempt)
        if goalframe_schema_failed(result, first_goalframe_attempt):
            return None
        goals, execution_restriction, execution_restriction_source = _parse_goalframe_semantics(content)
        presentation = presentation_from_model(content)
        trace_stage("GOALFRAME_TYPED_GOALS", "COMPLETED", safe_structure={
            "goals": tuple({
                "goal_id": goal.get("goal_id", ""),
                "semantic_domain": goal.get("semantic_domain", ""),
                "effect_intent": goal.get("effect_intent", ""),
                "goal_role": goal.get("goal_role", ""),
                "parent_goal_id": goal.get("parent_goal_id", ""),
                "subgoal_relation": goal.get("subgoal_justification_kind", ""),
                "requested_outcome_class": "PRESENT" if goal.get("requested_outcome") else "EMPTY",
                "ambiguity": (
                    "PRESENT" if goal.get("ambiguity") else "ABSENT"
                ) if "ambiguity" in goal else "NOT_RETAINED",
            } for goal in goals),
            "execution_restriction": execution_restriction,
        })
        if not goals:
            trace_stage("GOALFRAME_COMPLETED", "FAILED", error_class="goalframe_empty")
            audit_trace["candidate_discovery_error"] = "goalframe_provenance_invalid"
            return None
        trace_stage("GOALFRAME_COMPLETED", "COMPLETED")
        # ONE bounded same-brain repair for typed provenance violations (not silent drop).
        repair_used = False
        violations = (
            _goalframe_validation_violations(
                goals, source_text=original_text, require_artifact_operations=False,
            )
            + _goalframe_restriction_violations(
                execution_restriction, execution_restriction_source, source_text=original_text,
            )
            + _artifact_restriction_overlap_violations(goals, execution_restriction_source)
            + _goalframe_response_requirement_violations(goals, presentation)
        )
        if not violations:
            semantic_violations = source_coverage(content)
            if semantic_violations is None:
                return None
            violations += semantic_violations
        first_goalframe_attempt["validation_violations"] = tuple(violations)
        if violations:
            if not deadline.understanding_attempt_available() or deadline.cancelled or deadline.remaining() <= 0:
                audit_trace["goalframe_repair_state"] = "UNAVAILABLE"
                audit_trace["candidate_discovery_error"] = "goalframe_provenance_invalid"
                return None
            repair_prompt = sys_prompt + (
                " Repair typed provenance only: " + ";".join(f"{gid}:{r}" for gid, r in violations)
                + ". Preserve the user's requested meaning. For an execution-restriction violation, re-evaluate the "
                "restriction type against the source prohibition. NONE means no prohibition and requires an empty "
                "execution_restriction_source; do not quote the whole request as a prohibition. When there is an "
                "actual prohibition, preserve its source span and choose the matching restriction type."
            )
            goalframe_repair_attempted = True
            audit_trace["goalframe_repair_state"] = "ATTEMPTED"
            repair_prompt += " Rejected candidate JSON: " + str(content)
            repaired_result = understand(system_prompt=repair_prompt, user_prompt=user_prompt, deadline=deadline,
                                         output_schema=GOALFRAME_UNDERSTANDING_JSON_SCHEMA)
            repaired_content = repaired_result.get("content") if isinstance(repaired_result, dict) else repaired_result
            corrected_goalframe_attempt = {"attempt": 1, "raw_model_content": repaired_content,
                                           "validation_violations": None}
            audit_trace["goalframe_understanding_attempts"].append(corrected_goalframe_attempt)
            if goalframe_schema_failed(repaired_result, corrected_goalframe_attempt):
                return None
            repaired_goals, repaired_restriction, repaired_restriction_source = _parse_goalframe_semantics(
                repaired_content,
            )
            repaired_presentation = presentation_from_model(repaired_content)
            repaired_violations = (
                _goalframe_validation_violations(
                    repaired_goals, source_text=original_text, require_artifact_operations=False,
                )
                + _goalframe_restriction_violations(
                    repaired_restriction, repaired_restriction_source, source_text=original_text,
                )
                + _artifact_restriction_overlap_violations(
                    repaired_goals, repaired_restriction_source,
                )
                + _goalframe_response_requirement_violations(repaired_goals, repaired_presentation)
            ) if repaired_goals else (("", "goalframe_empty"),)
            if not repaired_violations:
                semantic_violations = source_coverage(repaired_content, repair_available=False)
                if semantic_violations is None:
                    audit_trace["goalframe_repair_state"] = "FAILED"
                    return None
                repaired_violations += semantic_violations
            corrected_goalframe_attempt["validation_violations"] = tuple(repaired_violations)
            if repaired_violations:
                audit_trace["goalframe_repair_state"] = "FAILED"
                audit_trace["candidate_discovery_error"] = "goalframe_provenance_invalid"
                audit_trace["candidate_discovery_violations"] = tuple(repaired_violations)
                audit_trace["candidate_discovery_rejected_goals"] = tuple(repaired_goals)
                return None
            goals = repaired_goals
            presentation = repaired_presentation
            execution_restriction = repaired_restriction
            execution_restriction_source = repaired_restriction_source
            repair_used = True
            audit_trace["goalframe_repair_state"] = "SUCCEEDED"

        extracted_goals = _extract_artifact_operation_requirements(
            understand=understand, deadline=deadline, original_text=original_text,
            goals=goals, execution_restriction_source=execution_restriction_source,
            audit_trace=audit_trace,
        )
        if extracted_goals is None:
            audit_trace["candidate_discovery_error"] = "artifact_operation_extraction_invalid"
            return None
        goals = extracted_goals
        audit_trace["source_artifact_operation_requirements"] = tuple(
            requirement for goal in goals
            for requirement in goal.get("artifact_operation_requirements", ())
        )

        def bind_goal_set(current_goals: list[dict[str, str]], *, binding_attempt: int = 1) -> tuple[
            list[str], list[dict[str, str]], list[tuple[str, str]],
        ]:
            selected_ids: list[str] = ["conversation.respond"]
            typed_justifications: list[dict[str, str]] = [{
                "goal_id": "host_final_response", "goal_role": "HOST_ORCHESTRATION",
                "parent_goal_id": "", "capability_id": "conversation.respond",
                "justification_kind": "FINAL_BRAIN_RESPONSE_REQUIRED",
                "source_grounding": "",
            }]
            binding_violations: list[tuple[str, str]] = []
            capability_by_goal: dict[str, str] = {}
            # Parents first makes an operation-dependency claim verifiable even when the
            # model serialized a child before its parent.
            ordered = sorted(current_goals, key=lambda item: item.get("goal_role") == "SUBGOAL")
            for goal in ordered:
                ids = _goalframe_projection(
                    registry_projection, semantic_domain=goal["semantic_domain"],
                    effect_intent=goal["effect_intent"], memory_filter=goal.get("memory_filter"),
                )
                audit_trace.setdefault("goal_binding_candidates", []).append({
                    "binding_attempt": binding_attempt, "goal": dict(goal), "candidate_ids": ids,
                })
                if not ids:
                    trace_stage("GOALFRAME_BINDING", "FAILED", binding_attempt=int(binding_attempt),
                        binding_goal={key: goal.get(key, "") for key in (
                            "goal_id", "semantic_domain", "effect_intent", "goal_role", "parent_goal_id",
                            "subgoal_justification_kind")},
                        binding_direct_capability_ids=(), binding_operation_ids=(),
                        binding_semantic_owner_ids=(), binding_status="NO_COMPATIBLE_CAPABILITY",
                        binding_capability_id=None, binding_reason_class="EMPTY_COMPATIBLE_PROJECTION")
                    binding_violations.append((goal["goal_id"], "goal_has_no_compatible_capability"))
                    continue
                cap, _status = _bind_goalframe_goal(
                    call=discover_candidates, goal=goal,
                    registry_projection=select_semantic_projection_details(registry_projection, ids),
                    deadline=deadline, binding_attempt=binding_attempt,
                    binding_audit=audit_trace["goal_binding_candidates"][-1],
                )
                if not cap or cap not in set(ids):
                    binding_violations.append((goal["goal_id"], "capability_selection_unjustified"))
                    continue
                if goal.get("subgoal_justification_kind") == "OPERATION_DEPENDENCY":
                    parent_capability = capability_by_goal.get(goal.get("parent_goal_id", ""), "")
                    parent_entry = next((
                        item for item in registry_projection.get("entries", ())
                        if str(item.get("capability_id")) == parent_capability
                    ), None)
                    declared = bool(parent_entry and any(
                        cap in tuple(str(value) for value in contract.get("prerequisite_capability_ids", ()))
                        for contract in parent_entry.get("operation_contracts", ())
                    ))
                    if not declared:
                        binding_violations.append((goal["goal_id"], "subgoal_dependency_not_registry_declared"))
                        continue
                capability_by_goal[goal["goal_id"]] = cap
                selected_ids.append(cap)
                typed_justifications.append({
                    "goal_id": goal["goal_id"], "goal_role": goal["goal_role"],
                    "parent_goal_id": goal.get("parent_goal_id", ""), "capability_id": cap,
                    "justification_kind": (
                        "PRIMARY_OUTCOME" if goal["goal_role"] == "PRIMARY_OUTCOME"
                        else goal["subgoal_justification_kind"]
                    ),
                    "source_grounding": goal["grounding"],
                })
            return selected_ids, typed_justifications, binding_violations

        selected, justifications, binding_violations = bind_goal_set(goals, binding_attempt=1)
        if binding_violations and not repair_used:
            if not deadline.understanding_attempt_available() or deadline.cancelled or deadline.remaining() <= 0:
                audit_trace["goalframe_repair_state"] = "UNAVAILABLE"
                audit_trace["candidate_discovery_error"] = "goalframe_selection_justification_invalid"
                return None
            goalframe_repair_attempted = True
            audit_trace["goalframe_repair_state"] = "ATTEMPTED"
            repair_prompt = sys_prompt + (
                " Repair typed selection provenance only: "
                + ";".join(f"{gid}:{reason}" for gid, reason in binding_violations)
                + ". Preserve the user's requested meaning; do not silently delete a genuine explicit goal."
            )
            repair_prompt += " Rejected candidate JSON: " + str(content)
            repaired_result = understand(
                system_prompt=repair_prompt, user_prompt=user_prompt, deadline=deadline,
                output_schema=GOALFRAME_UNDERSTANDING_JSON_SCHEMA,
            )
            repaired_content = repaired_result.get("content") if isinstance(repaired_result, dict) else repaired_result
            binding_repair_attempt = {"attempt": len(audit_trace["goalframe_understanding_attempts"]),
                                      "raw_model_content": repaired_content,
                                      "validation_violations": None}
            audit_trace["goalframe_understanding_attempts"].append(binding_repair_attempt)
            if goalframe_schema_failed(repaired_result, binding_repair_attempt):
                return None
            repaired_goals, repaired_restriction, repaired_restriction_source = _parse_goalframe_semantics(repaired_content)
            repaired_presentation = presentation_from_model(repaired_content)
            provenance = (
                _goalframe_validation_violations(repaired_goals, source_text=original_text)
                + _goalframe_restriction_violations(repaired_restriction, repaired_restriction_source, source_text=original_text)
                + _artifact_restriction_overlap_violations(repaired_goals, repaired_restriction_source)
                + _goalframe_response_requirement_violations(repaired_goals, repaired_presentation)
            ) if repaired_goals else (("", "goalframe_empty"),)
            if not provenance:
                semantic_violations = source_coverage(repaired_content, repair_available=False)
                if semantic_violations is None:
                    audit_trace["goalframe_repair_state"] = "FAILED"
                    return None
                provenance += semantic_violations
            if not provenance:
                goals = repaired_goals
                execution_restriction = repaired_restriction
                execution_restriction_source = repaired_restriction_source
                presentation = repaired_presentation
                selected, justifications, binding_violations = bind_goal_set(goals, binding_attempt=2)
                audit_trace["goalframe_repair_state"] = "FAILED" if binding_violations else "SUCCEEDED"
            else:
                audit_trace["goalframe_repair_state"] = "FAILED"
                audit_trace["candidate_discovery_error"] = "goalframe_provenance_invalid"
                audit_trace["candidate_discovery_violations"] = tuple(provenance)
                return None
        if binding_violations:
            audit_trace["candidate_discovery_error"] = "goalframe_selection_justification_invalid"
            audit_trace["candidate_discovery_violations"] = tuple(binding_violations)
            return None
        final_selected = tuple(dict.fromkeys(selected))
        justified_capabilities = {item["capability_id"] for item in justifications}
        unjustified_capabilities = tuple(
            capability_id for capability_id in final_selected
            if capability_id not in justified_capabilities
        )
        if unjustified_capabilities:
            audit_trace["candidate_discovery_error"] = "goalframe_selection_justification_invalid"
            audit_trace["candidate_discovery_violations"] = tuple(
                (capability_id, "capability_without_typed_justification")
                for capability_id in unjustified_capabilities
            )
            return None
        projection = select_semantic_projection_details(registry_projection, final_selected)
        projection["selection_goalframes"] = tuple(goals)
        # Preserve presentation authored by the SAME original semantic model.
        # Parameter extraction must not become a second interpretation of it.
        projection["selection_response_requirements"] = json.loads(json.dumps(presentation))
        projection["selection_artifact_operation_requirements"] = tuple(
            requirement for goal in goals
            for requirement in goal.get("artifact_operation_requirements", ())
        )
        projection["selection_capability_justifications"] = tuple(justifications)
        projection["selection_execution_restriction"] = execution_restriction
        projection["selection_execution_restriction_source"] = execution_restriction_source
        audit_trace["candidate_discovery"] = {
            "strategy": "GOALFRAME_V3_INTENT_TO_BINDING", "goals": goals,
            "response_requirements": presentation,
            "selection_justifications": justifications,
            "unjustified_capabilities": unjustified_capabilities,
        }
        return projection
    except Exception as exc:
        trace_stage("GOALFRAME_FAILURE", "FAILED", error_class=type(exc).__name__,
                    detail=str(exc)[:240])
        detail = f"{type(exc).__name__}:{exc}"
        if goalframe_validation_started:
            if goalframe_repair_attempted:
                audit_trace["goalframe_repair_state"] = "FAILED"
            # A malformed/failed SAME-brain correction cannot authorize another
            # semantic attempt through the legacy discovery compatibility path.
            audit_trace["candidate_discovery_error"] = "goalframe_provenance_invalid"
            audit_trace["candidate_discovery_correction_error"] = detail
            attempts = audit_trace.setdefault("goalframe_understanding_attempts", [])
            if not goalframe_repair_attempted:
                if attempts:
                    attempts[-1]["post_validation_error"] = detail
            elif attempts and attempts[-1].get("attempt") == 1:
                if attempts[-1]["validation_violations"] is None:
                    attempts[-1]["validation_violations"] = (("", "correction_response_invalid:" + detail),)
                else:
                    attempts[-1]["post_validation_error"] = detail
            else:
                attempts.append({"attempt": 1, "raw_model_content": None,
                                 "validation_violations": (("", "correction_call_failed:" + detail),)})
        else:
            audit_trace["candidate_discovery_error"] = detail
        return None


def _model_selected_registry_details(
    *, model_port: ModelUnderstandingPort, deadline: RequestDeadline, original_text: str,
    session_context: dict[str, Any], registry_projection: dict[str, Any], audit_trace: dict[str, Any],
    request_id: str, identity: IdentityContext, input_preparation: dict[str, Any],
) -> dict[str, Any] | None:
    discover_candidates = getattr(model_port, "discover_candidates", None)
    if not callable(discover_candidates):
        audit_trace["candidate_discovery_error"] = "main_model_candidate_method_unavailable"
        return None
    try:
        # GoalFrame v3 is the canonical active path; legacy full-index/kind remains as
        # fallback (NOT deleted until production fresh-15 + reachability prove it dead).
        goalframe_result = _model_selected_registry_details_goalframe(
            model_port=model_port, deadline=deadline, original_text=original_text,
            session_context=session_context, registry_projection=registry_projection,
            audit_trace=audit_trace,
        )
        if goalframe_result is not None:
            return goalframe_result
        # Invalid GoalFrame semantics exhausted their one same-brain repair and must
        # fail closed. The legacy discovery path is reachable only when GoalFrame is
        # unsupported/unavailable, never as a bypass for rejected semantic provenance.
        if audit_trace.get("candidate_discovery_error") in {
            "goalframe_provenance_invalid", "goalframe_selection_justification_invalid",
        }:
            return None
        full_system, full_user = build_candidate_discovery_prompt(
            original_text=original_text, session_context=session_context, registry_projection=registry_projection,
        )
        full_budget = measure_prompt_budget(
            full_system, full_user, reserved_output_tokens=CANDIDATE_DISCOVERY_RESERVED_OUTPUT_TOKENS,
            output_schema=CANDIDATE_DISCOVERY_JSON_SCHEMA,
            components=_prompt_material_components(full_system, full_user),
            num_ctx=SEMANTIC_SELECTION_NUM_CTX,
        )
        hierarchy_trace: dict[str, Any] = {
            "full_index_capability_count": registry_projection["capability_count"],
            "full_index_prompt_budget": full_budget,
        }
        audit_trace["hierarchical_discovery"] = hierarchy_trace
        audit_trace["model_discovery_attempts"] = []
        passes: list[dict[str, Any]] = []
        if full_budget["within_budget"]:
            candidate_ids = _run_discovery_continuation(
                call=discover_candidates, prompt_builder=build_candidate_discovery_prompt,
                value_key="candidate_capability_ids", allowed_values=tuple(
                    str(item["capability_id"]) for item in registry_projection["entries"]
                ), original_text=original_text, session_context=session_context,
                registry_projection=registry_projection, deadline=deadline,
                output_schema=CANDIDATE_DISCOVERY_JSON_SCHEMA, trace=passes,
                audit_trace=audit_trace["model_discovery_attempts"],
                repair_state=audit_trace,
                call_role="full_index_candidate_discovery",
            )
            hierarchy_trace["used"] = False
        else:
            discover_kinds = getattr(model_port, "discover_kinds", None)
            if not callable(discover_kinds):
                raise ValueError("main_model_kind_method_unavailable")
            registered_kinds = tuple(sorted({str(item["kind"]) for item in registry_projection["entries"]}))
            kind_passes: list[dict[str, Any]] = []
            kinds = _run_discovery_continuation(
                call=discover_kinds, prompt_builder=build_kind_discovery_prompt,
                value_key="candidate_kinds", allowed_values=registered_kinds,
                original_text=original_text, session_context=session_context,
                registry_projection=registry_projection, deadline=deadline,
                output_schema=KIND_DISCOVERY_JSON_SCHEMA, trace=kind_passes,
                audit_trace=audit_trace["model_discovery_attempts"], repair_state=audit_trace,
                call_role="kind_discovery",
            )
            executable_projection = dict(registry_projection)
            executable_projection["entries"] = tuple(sorted(
                (
                    item for item in registry_projection["entries"]
                    if item.get("execution_contract_available") is True
                    and item.get("kind") == "canonical_capability"
                ),
                key=lambda item: str(item.get("capability_id", "")),
            ))
            executable_projection["capability_count"] = len(executable_projection["entries"])
            executable_ids = tuple(
                str(item["capability_id"]) for item in executable_projection["entries"]
            )
            executable_candidate_ids: tuple[str, ...] = ()
            if executable_ids:
                executable_candidate_ids = _run_discovery_continuation(
                    call=discover_candidates, prompt_builder=build_candidate_discovery_prompt,
                    value_key="candidate_capability_ids", allowed_values=executable_ids,
                    original_text=original_text, session_context=session_context,
                    registry_projection=executable_projection, deadline=deadline,
                    output_schema=CANDIDATE_DISCOVERY_JSON_SCHEMA, trace=passes,
                    audit_trace=audit_trace["model_discovery_attempts"], repair_state=audit_trace,
                    call_role="authoritative_executable_candidate_discovery",
                )
            selected_noncanonical_kinds = {str(k) for k in kinds if str(k) != "canonical_capability"}
            collected = list(executable_candidate_ids)
            for kind in sorted(selected_noncanonical_kinds):
                kind_projection = projection_for_kinds(registry_projection, (kind,))
                groups = _candidate_budget_groups(
                    original_text=original_text, session_context=session_context,
                    registry_projection=kind_projection,
                )
                for group_number, (group_projection, _) in enumerate(groups, 1):
                    suffix = "" if len(groups) == 1 else f":chunk:{group_number}"
                    collected.extend(_run_discovery_continuation(
                        call=discover_candidates, prompt_builder=build_candidate_discovery_prompt,
                        value_key="candidate_capability_ids",
                        allowed_values=tuple(
                            str(item["capability_id"]) for item in group_projection["entries"]
                        ),
                        original_text=original_text, session_context=session_context,
                        registry_projection=group_projection, deadline=deadline,
                        output_schema=CANDIDATE_DISCOVERY_JSON_SCHEMA, trace=passes,
                        audit_trace=audit_trace["model_discovery_attempts"], repair_state=audit_trace,
                        call_role=f"candidate_discovery_kind:{kind}{suffix}",
                    ))
            unconsolidated_candidate_ids = tuple(dict.fromkeys(collected))
            candidate_ids, _consolidation_audit = _consolidate_candidate_ids_if_needed(
                call=discover_candidates, candidate_ids=unconsolidated_candidate_ids,
                original_text=original_text, session_context=session_context,
                registry_projection=registry_projection, deadline=deadline,
                trace=passes, audit_trace=audit_trace["model_discovery_attempts"],
                repair_state=audit_trace,
                prior_authoritative_model_selected_ids=executable_candidate_ids,
            )
            hierarchy_trace["candidate_consolidation"] = _consolidation_audit
            hierarchy_trace.update({
                "used": True, "kind_passes": tuple(kind_passes), "model_selected_kinds": kinds,
                "authoritative_executable_selected_ids": executable_candidate_ids,
                "strategy": "AUTHORITATIVE_CANONICAL_AND_MODEL_SELECTED_KINDS",
            })
        alternative_ids: tuple[str, ...] = ()
        augmentation = hierarchy_trace.get(
            "authoritative_canonical_model_selected_kind_augmentation"
        )
        if isinstance(augmentation, dict):
            unconsolidated = tuple(augmentation.get("unconsolidated_candidate_ids", ()))
            alternative_ids = tuple(
                capability_id for capability_id in unconsolidated
                if capability_id not in set(candidate_ids)
            )
        operation_scope_ids = tuple(dict.fromkeys(candidate_ids + alternative_ids))
        details = select_semantic_projection_details(
            registry_projection, operation_scope_ids,
        )
        details["candidate_stage_status"] = {
            capability_id: (
                "PRIMARY" if capability_id in set(candidate_ids) else "ALTERNATIVE"
            )
            for capability_id in operation_scope_ids
        }
        hierarchy_trace["operation_discovery_alternative_ids"] = alternative_ids
        audit_trace["candidate_discovery"] = {
            "model_role": "jarvis:chat8b", "same_main_model_as_understanding": True,
            "helper_used_for_discovery": False, "prompt_budget": full_budget,
            "hierarchical_discovery": hierarchy_trace, "candidate_capability_ids": candidate_ids,
            "continuation_passes": tuple(passes), "schema_valid": True,
        }
        return details
    except (TimeoutError, ValueError, TypeError, KeyError, json.JSONDecodeError) as exc:
        audit_trace["candidate_discovery_error"] = f"{type(exc).__name__}:{exc}"
        trace_stage(
            "CANDIDATE_DISCOVERY_FAILURE", "FAILED", candidate_stage="VALIDATE",
            failure_type=type(exc).__name__, failure_code=str(exc)[:160],
            repair_attempt=int(audit_trace.get("model_backed_repair_count", 0)),
            safe_structure={"top_level_type": "unavailable", "schema_parse_status": "UNKNOWN"},
        )
        return None


def _goal_effect_operation_projection(registry_projection: dict[str, Any]) -> dict[str, Any]:
    """Narrow existing operation contracts by their bound typed goal effects.

    This is the same compatibility rule enforced after model selection, applied
    before publishing the candidate enum. No request text or semantic selection.
    """
    goals = {
        str(goal.get("goal_id")): goal
        for goal in registry_projection.get("selection_goalframes", ())
        if isinstance(goal, dict) and goal.get("goal_id")
    }
    if not goals:
        return registry_projection
    bindings: dict[str, set[str]] = {}
    for item in registry_projection.get("selection_capability_justifications", ()):
        if isinstance(item, dict) and str(item.get("goal_id")) in goals:
            bindings.setdefault(str(item.get("capability_id")), set()).add(str(item["goal_id"]))
    projected = json.loads(json.dumps(registry_projection))
    entries = []
    for entry in projected.get("entries", ()):
        goal_ids = bindings.get(str(entry.get("capability_id")), set()) if bindings else set(goals)
        entry["operation_contracts"] = [
            contract for contract in entry.get("operation_contracts", ())
            if any(
                str(contract.get("effect_type")) in SEMANTIC_EFFECT_INTENTS.get(
                    str(goals[goal_id].get("effect_intent", "")), frozenset())
                and (
                    not contract.get("supported_goal_effect_intents")
                    or goals[goal_id].get("effect_intent") in contract["supported_goal_effect_intents"]
                )
                for goal_id in goal_ids
            )
        ]
        if entry["operation_contracts"] or entry.get("execution_contract_available") is not True:
            entries.append(entry)
    projected["entries"] = entries
    projected["capability_count"] = len(entries)
    return projected


def _model_selected_operation_details(
    *, model_port: ModelUnderstandingPort, deadline: RequestDeadline, original_text: str,
    session_context: dict[str, Any], registry_projection: dict[str, Any],
    audit_trace: dict[str, Any],
) -> dict[str, Any] | None:
    if not isinstance(registry_projection, dict) or not registry_projection.get("entries"):
        audit_trace["operation_discovery_error"] = "empty_candidate_projection"
        return None
    if getattr(model_port, "supports_call_scoped_understanding_schema", False) is not True:
        audit_trace["operation_discovery"] = {
            "status": "LEGACY_TYPED_MODEL_PORT", "candidate_operation_ids": (),
        }
        return registry_projection
    operation_projection = registry_projection
    candidate_stage_status = dict(registry_projection.get("candidate_stage_status", {}))
    non_response_executable = tuple(
        item for item in registry_projection.get("entries", ())
        if item.get("execution_contract_available") is True
        and item.get("capability_id") != "conversation.respond"
    )
    if non_response_executable:
        operation_projection = dict(registry_projection)
        # The consolidated PRIMARY set is the model-selected smallest-sufficient scope.
        # ALTERNATIVE entries are redundant candidates dropped by the bounded reduction;
        # they must not bloat the operation-discovery prompt past its configured budget.
        operation_projection["entries"] = tuple(
            item for item in registry_projection["entries"]
            if item.get("capability_id") != "conversation.respond"
            and candidate_stage_status.get(str(item.get("capability_id"))) != "ALTERNATIVE"
        )
        operation_projection["capability_count"] = len(operation_projection["entries"])
        audit_trace["response_operation_orchestration"] = (
            "HOST_ATTACHED_AFTER_EVIDENCE_PLAN"
        )
    operation_projection = _goal_effect_operation_projection(operation_projection)
    catalog = load_operation_catalog(operation_projection) if operation_projection.get("entries") else ()
    restriction = str(operation_projection.get("selection_execution_restriction", "NONE"))
    if restriction in {"NO_EXECUTE", "PREPARE_ONLY"}:
        # A typed effect restriction narrows the authoritative executable scope.  This
        # is contract validation, not operation-name routing: create/modify contracts
        # remain available while every registry operation whose effect is EXECUTE is
        # structurally unavailable to semantic selection for this turn.
        catalog = tuple(
            item for item in catalog
            if str(item.get("effect_type")) != "EXECUTE"
            or (
                str(item.get("target_scope")) == "local_simulation_runtime"
                and not bool(item.get("external_side_effect"))
            )
        )
        allowed_operation_ids = {str(item["operation_id"]) for item in catalog}
        restricted_projection = json.loads(json.dumps(operation_projection))
        restricted_entries = []
        for entry in restricted_projection.get("entries", ()):
            entry["operation_contracts"] = [
                contract for contract in entry.get("operation_contracts", ())
                if str(contract.get("operation_id")) in allowed_operation_ids
            ]
            if entry["operation_contracts"] or entry.get("execution_contract_available") is not True:
                restricted_entries.append(entry)
        restricted_projection["entries"] = restricted_entries
        restricted_projection["capability_count"] = len(restricted_entries)
        operation_projection = restricted_projection
    if not catalog:
        if non_response_executable and registry_projection.get("selection_goalframes"):
            audit_trace["operation_discovery_error"] = "goal_effect_has_no_compatible_operation"
            return None
        audit_trace["operation_discovery"] = {
            "status": "NOT_REQUIRED", "candidate_operation_ids": (),
        }
        return operation_projection
    if len(catalog) == 1:
        # Candidate selection is still semantic/model-driven.  Once that
        # bounded projection exposes exactly one authoritative operation,
        # another model call cannot make a meaningful choice; it can only
        # echo the registry.  Preserve the sole typed contract for the
        # RequestUnderstanding model to parameterize and validate.
        operation_id = str(catalog[0]["operation_id"])
        audit_trace["operation_discovery"] = {
            "status": "NOT_REQUIRED_SINGLE_AUTHORITATIVE_OPERATION",
            "candidate_operation_ids": (operation_id,),
            "strategy": "AUTHORITATIVE_REGISTRY_SINGLETON",
            "selection_justifications": ({
                "capability_id": str(catalog[0]["capability_id"]),
                "operation_id": operation_id,
                "justification_kind": "ONLY_OPERATION_FOR_JUSTIFIED_CAPABILITY",
            },),
            "unjustified_operations": (),
            "schema_valid": True,
        }
        return operation_projection
    call = getattr(model_port, "discover_candidates", None)
    if not callable(call):
        audit_trace["operation_discovery_error"] = "main_model_operation_discovery_method_unavailable"
        return None
    passes: list[dict[str, Any]] = []
    attempts = audit_trace.setdefault("model_discovery_attempts", [])
    # Each typed capability-to-goal binding permits one direct operation.  Extra
    # operations are legal only when their registry contract declares an operational
    # dependency.  This prevents artifact-internal steps from becoming additional
    # host operations while remaining independent of capability/provider names.
    operation_scope_capability_ids = {
        str(item.get("capability_id")) for item in operation_projection.get("entries", ())
    }
    capability_justifications = tuple(
        item for item in operation_projection.get("selection_capability_justifications", ())
        if (
            isinstance(item, dict)
            and str(item.get("capability_id")) in operation_scope_capability_ids
        )
    )
    direct_operation_slots = len(capability_justifications)
    if not direct_operation_slots:
        direct_operation_slots = max(1, len(tuple(operation_projection.get("selection_goalframes", ()))))
    dependency_slots = sum(
        1 for item in catalog if item.get("declared_prerequisite_for_operation_ids")
    )
    max_selected_operations = min(
        len(catalog), direct_operation_slots + dependency_slots,
    )
    try:
        operation_ids = _run_discovery_continuation(
            call=call, prompt_builder=build_operation_discovery_prompt,
            value_key="candidate_operation_ids",
            allowed_values=tuple(str(item["operation_id"]) for item in catalog),
            original_text=original_text, session_context=session_context,
            registry_projection=operation_projection, deadline=deadline,
            output_schema=OPERATION_DISCOVERY_JSON_SCHEMA, trace=passes,
            audit_trace=attempts, repair_state=audit_trace,
            call_role="operation_discovery",
            max_selected_values=max_selected_operations,
        )
        selected = set(operation_ids)
        details = json.loads(json.dumps(operation_projection))
        selected_entries = []
        for entry in details.get("entries", ()):
            entry["operation_contracts"] = [
                contract for contract in entry.get("operation_contracts", ())
                if str(contract.get("operation_id")) in selected
            ]
            # Candidate discovery is a broad semantic consideration stage.
            # Operation discovery is the same model's exact executable choice.
            # An executable candidate with no selected operation is not part of
            # this turn's plan; do not retain an invalid empty executable entry
            # and do not rewrite it as PLAN_ONLY.
            if (
                entry.get("execution_contract_available") is True
                and not entry["operation_contracts"]
            ):
                continue
            selected_entries.append(entry)
        details["entries"] = selected_entries
        validate_semantic_capability_projection(details)
        selected_contracts = tuple(
            (str(entry["capability_id"]), contract) for entry in selected_entries
            for contract in entry.get("operation_contracts", ())
        )
        semantic_justifications = {
            str(item["operation_id"]): item
            for pass_item in passes
            for item in pass_item.get("selection_justifications", ())
        }
        operation_justifications = tuple({
            "capability_id": capability_id,
            "operation_id": str(contract["operation_id"]),
            "goal_id": semantic_justifications.get(
                str(contract["operation_id"]), {},
            ).get("goal_id", ""),
            "justification_kind": semantic_justifications.get(
                str(contract["operation_id"]), {},
            ).get("justification_kind", ""),
            "source_grounding": semantic_justifications.get(
                str(contract["operation_id"]), {},
            ).get("source_grounding", ""),
        } for capability_id, contract in selected_contracts)
        selected_catalog = {str(contract["operation_id"]): contract for _, contract in selected_contracts}
        for contract in catalog:
            targets = validate_operation_dependency_references(contract)
            if set(targets).intersection(selected) and str(contract["operation_id"]) not in selected:
                raise ValueError("operation_prerequisite_not_selected")
        for justification in operation_justifications:
            if justification["justification_kind"] == "DECLARED_OPERATION_DEPENDENCY":
                contract = selected_catalog[justification["operation_id"]]
                targets = validate_operation_dependency_references(contract)
                if not set(targets).intersection(selected):
                    raise ValueError("operation_dependency_target_not_selected")
        justified_operation_ids = {
            str(item["operation_id"]) for item in operation_justifications
            if item["justification_kind"] and item["source_grounding"]
        }
        unjustified = tuple(sorted(selected - justified_operation_ids))
        if unjustified:
            raise ValueError("unjustified_operation_selection:" + ",".join(unjustified))
        audit_trace["operation_discovery"] = {
            "model_role": "jarvis:chat8b",
            "candidate_operation_ids": operation_ids,
            "continuation_passes": tuple(passes),
            "strategy": "UNIQUE_TYPED_KEYS_WITH_HOST_CONTINUATION",
            "selection_justifications": operation_justifications,
            "unjustified_operations": unjustified,
            "schema_valid": True,
        }
        return details
    except (TimeoutError, ValueError, TypeError, KeyError, json.JSONDecodeError) as exc:
        audit_trace["operation_discovery_error"] = f"{type(exc).__name__}:{exc}"
        return None


def _measure_operation_discovery_budget(
    *, candidate_ids: tuple[str, ...], registry_projection: dict[str, Any],
    original_text: str, session_context: dict[str, Any],
) -> dict[str, Any]:
    """Measure the downstream operation-discovery prompt budget for a model-selected set.

    Consolidation is a technical budget-reduction step, never a second semantic selection
    authority. This measurement decides whether a reduction pass is even required; it uses
    the same prompt builder and schema as `_model_selected_operation_details` and never a
    request-text or capability-name heuristic.
    """
    projection = select_semantic_projection_details(registry_projection, candidate_ids)
    projection["candidate_stage_status"] = {
        str(capability_id): "PRIMARY" for capability_id in candidate_ids
    }
    non_response_executable = tuple(
        item for item in projection.get("entries", ())
        if item.get("execution_contract_available") is True
        and str(item.get("capability_id")) != "conversation.respond"
    )
    operation_projection = projection
    if non_response_executable:
        operation_projection = dict(projection)
        operation_projection["entries"] = tuple(
            item for item in projection["entries"]
            if str(item.get("capability_id")) != "conversation.respond"
        )
        operation_projection["capability_count"] = len(operation_projection["entries"])
    operation_projection = _goal_effect_operation_projection(operation_projection)
    catalog = load_operation_catalog(operation_projection) if operation_projection.get("entries") else ()
    if not catalog:
        return {
            "within_budget": True, "operation_count": 0,
            "candidate_count": len(candidate_ids),
        }
    operation_ids = tuple(str(item["operation_id"]) for item in catalog)
    system_prompt, user_prompt = build_operation_discovery_prompt(
        original_text=original_text, session_context=session_context,
        registry_projection=operation_projection,
    )
    schema = discovery_schema_for_registered_values(
        OPERATION_DISCOVERY_JSON_SCHEMA, value_key="candidate_operation_ids",
        allowed_values=operation_ids, operation_contracts=tuple(catalog),
    )
    measurement = measure_prompt_budget(
        system_prompt, user_prompt,
        reserved_output_tokens=OPERATION_DISCOVERY_RESERVED_OUTPUT_TOKENS,
        output_schema=schema,
        components=_prompt_material_components(system_prompt, user_prompt),
        num_ctx=SEMANTIC_SELECTION_NUM_CTX,
    )
    measurement["operation_count"] = len(operation_ids)
    measurement["candidate_count"] = len(candidate_ids)
    return measurement


def _consolidate_candidate_ids_if_needed(
    *, call: Any, candidate_ids: tuple[str, ...], original_text: str,
    session_context: dict[str, Any], registry_projection: dict[str, Any],
    deadline: RequestDeadline, trace: list[dict[str, Any]],
    audit_trace: list[dict[str, Any]], repair_state: dict[str, Any],
    prior_authoritative_model_selected_ids: tuple[str, ...] = (),
) -> tuple[tuple[str, ...], dict[str, Any]]:
    """Reduce a model-selected candidate set only when downstream operation discovery
    cannot already accept it. Never re-select an already-bounded model-selected set."""
    budget = _measure_operation_discovery_budget(
        candidate_ids=candidate_ids, registry_projection=registry_projection,
        original_text=original_text, session_context=session_context,
    )
    # This set has already been selected by the authoritative model with typed goal
    # justification. A technical prompt budget may partition later operation material,
    # but it must never trigger a second semantic capability selection that can erase a
    # justified goal. Preserve the canonical set and let the operation stage fail closed
    # if its own bounded contract cannot be admitted.
    del call, deadline, trace, audit_trace, repair_state, prior_authoritative_model_selected_ids
    return candidate_ids, {
        "status": "NOT_REQUIRED_ALREADY_BOUNDED",
        "reason": (
            "DOWNSTREAM_BUDGET_FITS_MODEL_SELECTED_SET"
            if budget["within_budget"] else
            "CAPABILITY_SET_PRESERVED_DESPITE_DOWNSTREAM_BUDGET"
        ),
        "candidate_count": len(candidate_ids),
        "operation_discovery_prompt_budget": budget,
    }


def _consolidate_candidate_ids(
    *, call: Any, candidate_ids: tuple[str, ...], original_text: str,
    session_context: dict[str, Any], registry_projection: dict[str, Any],
    deadline: RequestDeadline, trace: list[dict[str, Any]], audit_trace: list[dict[str, Any]],
    repair_state: dict[str, Any],
    prior_authoritative_model_selected_ids: tuple[str, ...] = (),
) -> tuple[str, ...]:
    """Bound same-model consolidation by context size, never by request-text routing."""
    current = tuple(dict.fromkeys(candidate_ids))
    if not current:
        raise ValueError("candidate_consolidation_empty")
    for round_number in range(1, len(current) + 2):
        projection = select_semantic_projection_details(registry_projection, current)
        prompt = build_candidate_discovery_prompt(
            original_text=original_text, session_context=session_context,
            registry_projection=projection,
        )
        budget = measure_prompt_budget(
            *prompt, reserved_output_tokens=CANDIDATE_DISCOVERY_RESERVED_OUTPUT_TOKENS,
            output_schema=CANDIDATE_DISCOVERY_JSON_SCHEMA,
            components=_prompt_material_components(*prompt),
            num_ctx=SEMANTIC_SELECTION_NUM_CTX,
        )
        if budget["within_budget"]:
            consolidated = _run_discovery_continuation(
                call=call, prompt_builder=build_candidate_discovery_prompt,
                value_key="candidate_capability_ids", allowed_values=current,
                original_text=original_text, session_context=session_context,
                registry_projection=projection, deadline=deadline,
                output_schema=CANDIDATE_DISCOVERY_JSON_SCHEMA, trace=trace,
                audit_trace=audit_trace, repair_state=repair_state,
                call_role=f"candidate_consolidation_round:{round_number}",
                prior_model_selected_ids=prior_authoritative_model_selected_ids,
            )
            return tuple(dict.fromkeys(consolidated))
        grouped: list[str] = []
        for group_number, start in enumerate(range(0, len(current), DISCOVERY_VALUES_PER_PASS), 1):
            group = current[start:start + DISCOVERY_VALUES_PER_PASS]
            group_projection = select_semantic_projection_details(registry_projection, group)
            grouped.extend(_run_discovery_continuation(
                call=call, prompt_builder=build_candidate_discovery_prompt,
                value_key="candidate_capability_ids", allowed_values=group,
                original_text=original_text, session_context=session_context,
                registry_projection=group_projection, deadline=deadline,
                output_schema=CANDIDATE_DISCOVERY_JSON_SCHEMA, trace=trace,
                audit_trace=audit_trace, repair_state=repair_state,
                call_role=f"candidate_consolidation_round:{round_number}:group:{group_number}",
                prior_model_selected_ids=prior_authoritative_model_selected_ids,
            ))
        next_ids = tuple(dict.fromkeys(grouped))
        if not next_ids or len(next_ids) >= len(current):
            raise ValueError("candidate_consolidation_no_progress")
        current = next_ids
    raise ValueError("candidate_consolidation_progress_guard_exceeded")


def _consolidate_for_understanding_budget(
    *, call: Any, candidate_ids: tuple[str, ...], request_id: str, original_text: str,
    identity: IdentityContext, session_context: dict[str, Any], input_preparation: dict[str, Any],
    registry_projection: dict[str, Any], deadline: RequestDeadline, trace: list[dict[str, Any]],
    audit_trace: list[dict[str, Any]], repair_state: dict[str, Any],
    preserve_model_selected_scope: bool = False,
) -> tuple[str, ...]:
    """Admit the exact selected scope; never re-select production operations for budget.

    Unbound compatibility callers retain the existing bounded consolidation path.
    The canonical turn has already selected operations with GoalFrame provenance;
    a technical admission failure must retain those choices and fail closed.
    """
    current = tuple(dict.fromkeys(candidate_ids))
    for round_number in range(1, len(current) + 2):
        details = select_semantic_projection_details(registry_projection, current)
        for provenance_key in (
            "selection_goalframes", "selection_artifact_operation_requirements",
            "selection_capability_justifications", "selection_response_requirements",
            "selection_execution_restriction",
            "selection_execution_restriction_source", "candidate_stage_status",
        ):
            if provenance_key in registry_projection:
                details[provenance_key] = registry_projection[provenance_key]
        understanding_prompt = build_request_understanding_prompt(
            request_id=request_id, original_text=original_text, identity=identity,
            session_context=session_context, input_preparation=input_preparation,
            registry_projection=details,
        )
        understanding_schema = request_understanding_schema_for_projection(details, source_text=original_text)
        budget = measure_prompt_budget(
            *understanding_prompt,
            reserved_output_tokens=REQUEST_UNDERSTANDING_RESERVED_OUTPUT_TOKENS,
            output_schema=understanding_schema,
            components=_prompt_material_components(*understanding_prompt),
            num_ctx=REQUEST_UNDERSTANDING_NUM_CTX,
        )
        if preserve_model_selected_scope:
            repair_state["understanding_prompt_admission"] = {
                "status": "ADMITTED" if budget["within_budget"] else "BUDGET_EXCEEDED",
                "selected_capability_ids": current,
                "selected_operation_ids": tuple(
                    str(contract["operation_id"])
                    for entry in details.get("entries", ())
                    for contract in entry.get("operation_contracts", ())
                ),
                "semantic_reselection_attempted": False,
                "prompt_budget": budget,
            }
            if not budget["within_budget"]:
                raise ValueError("understanding_prompt_budget_exceeded_for_model_selected_operations")
        if budget["within_budget"]:
            return current
        grouped: list[str] = []
        for group_number, start in enumerate(range(0, len(current), DISCOVERY_VALUES_PER_PASS), 1):
            group = current[start:start + DISCOVERY_VALUES_PER_PASS]
            group_projection = select_semantic_projection_details(registry_projection, group)
            grouped.extend(_run_discovery_continuation(
                call=call, prompt_builder=build_candidate_discovery_prompt,
                value_key="candidate_capability_ids", allowed_values=group,
                original_text=original_text, session_context=session_context,
                registry_projection=group_projection, deadline=deadline,
                output_schema=CANDIDATE_DISCOVERY_JSON_SCHEMA, trace=trace,
                audit_trace=audit_trace, repair_state=repair_state,
                call_role=f"understanding_budget_consolidation_round:{round_number}:group:{group_number}",
            ))
        next_ids = tuple(dict.fromkeys(grouped))
        if not next_ids or len(next_ids) >= len(current):
            raise ValueError("understanding_budget_consolidation_no_progress")
        current = next_ids
    raise ValueError("understanding_budget_consolidation_progress_guard_exceeded")


def _run_discovery_continuation(
    *, call: Any, prompt_builder: Any, value_key: str, allowed_values: tuple[str, ...],
    original_text: str, session_context: dict[str, Any], registry_projection: dict[str, Any],
    deadline: RequestDeadline, output_schema: dict[str, Any], trace: list[dict[str, Any]],
    audit_trace: list[dict[str, Any]] | None = None, call_role: str = "candidate_discovery",
    repair_state: dict[str, Any] | None = None,
    prior_model_selected_ids: tuple[str, ...] = (),
    max_selected_values: int | None = None,
) -> tuple[str, ...]:
    def record_candidate_failure(raw: str, *, stage: str, exc: BaseException, repair_attempt: int,
                                 value_key: str) -> None:
        """Persist bounded parser/validator diagnostics without model output."""
        structure: dict[str, Any] = {"top_level_type": "unknown", "schema_parse_status": "FAILED"}
        try:
            payload = json.loads(raw)
            structure = {
                "top_level_type": type(payload).__name__,
                "top_level_keys": tuple(sorted(str(key) for key in payload))[:24] if isinstance(payload, dict) else (),
                "candidate_count": len(payload.get(value_key, ())) if isinstance(payload, dict) and isinstance(payload.get(value_key), (list, dict)) else 0,
                "candidate_ids": (
                    tuple(str(value) for value in payload.get(value_key, ()))[:16]
                    if isinstance(payload, dict) and isinstance(payload.get(value_key), list)
                    else tuple(str(key) for key in payload.get(value_key, {}))[:16]
                    if isinstance(payload, dict) and isinstance(payload.get(value_key), dict)
                    else ()
                ),
                "justification_field_present": isinstance(payload, dict) and "selection_justifications" in payload,
                "justification_count": len(payload.get("selection_justifications", ())) if isinstance(payload, dict) and isinstance(payload.get("selection_justifications"), list) else 0,
                "schema_parse_status": "PASS",
            }
        except (TypeError, ValueError, json.JSONDecodeError):
            pass
        safe_code = str(exc)[:160]
        trace_stage(
            "CANDIDATE_DISCOVERY_FAILURE", "FAILED", candidate_stage=stage,
            failure_type=type(exc).__name__, failure_code=safe_code,
            repair_attempt=repair_attempt, safe_structure=structure,
        )

    def validate_operation_justifications(parsed: Any, projection: dict[str, Any]) -> None:
        if value_key != "candidate_operation_ids":
            return
        goals = {
            str(item.get("goal_id")): item
            for item in projection.get("selection_goalframes", ())
            if isinstance(item, dict) and str(item.get("goal_id", ""))
        }
        contracts = {
            str(item["operation_id"]): item for item in load_operation_catalog(registry_projection)
        }
        for justification in parsed.selection_justifications:
            if not _source_contains_grounding(original_text, justification["source_grounding"]):
                raise ValueError("operation_justification_not_source_grounded")
            if goals:
                goal = goals.get(justification["goal_id"])
                if goal is None:
                    raise ValueError("operation_justification_goal_not_found")
                contract = contracts.get(justification["operation_id"])
                allowed_effects = SEMANTIC_EFFECT_INTENTS.get(
                    str(goal.get("effect_intent", "")), frozenset(),
                )
                if contract is None or str(contract.get("effect_type")) not in allowed_effects:
                    raise ValueError("operation_effect_not_justified_by_goal")
                supported_intents = tuple(contract.get("supported_goal_effect_intents", ()))
                if supported_intents and goal.get("effect_intent") not in supported_intents:
                    raise ValueError("operation_intent_not_supported_by_contract")
            if justification["justification_kind"] == "DECLARED_OPERATION_DEPENDENCY":
                contract = contracts.get(justification["operation_id"])
                if not contract or not validate_operation_dependency_references(contract, tuple(contracts)):
                    raise ValueError("operation_dependency_not_registry_declared")

    def parse_and_validate(raw: str, *, projection: dict[str, Any], response_required: bool,
                           repair_attempt: int) -> Any:
        try:
            parsed = parse_discovery_selection_payload(
                raw, value_key=value_key, allowed_values=allowed_values,
                max_values_per_pass=(
                    DISCOVERY_VALUES_PER_PASS if max_selected_values is None
                    else min(DISCOVERY_VALUES_PER_PASS, max_selected_values - len(selected))
                ),
                allow_empty_complete=not response_required,
            )
        except (ValueError, TypeError, KeyError) as exc:
            record_candidate_failure(raw, stage="REPAIR_PARSE" if repair_attempt else "PARSE",
                                     exc=exc, repair_attempt=repair_attempt, value_key=value_key)
            raise
        try:
            validate_operation_justifications(parsed, projection)
            if max_selected_values is not None and any(value in selected for value in parsed.selected_values):
                raise ValueError("discovery selection repeats canonical state")
            new_values = tuple(value for value in parsed.selected_values if value not in selected)
            prospective_count = len(set(selected + new_values))
            if max_selected_values is not None and parsed.continuation_required and not new_values:
                raise ValueError("discovery_continuation_no_progress")
            if max_selected_values is not None:
                if prospective_count > max_selected_values:
                    raise ValueError("operation_selection_exceeds_typed_justification_capacity")
                if parsed.continuation_required and prospective_count >= max_selected_values:
                    raise ValueError("operation_continuation_exceeds_typed_justification_capacity")
            if (
                response_required
                and "conversation.respond" not in prior_model_selected_ids
                and "conversation.respond" not in parsed.selected_values
            ):
                raise ValueError("accepted turn omitted canonical response capability")
        except (ValueError, TypeError, KeyError) as exc:
            record_candidate_failure(raw, stage="REPAIR_VALIDATE" if repair_attempt else "VALIDATE",
                                     exc=exc, repair_attempt=repair_attempt, value_key=value_key)
            raise
        return parsed

    selected: tuple[str, ...] = ()
    allowed = set(allowed_values)
    call_attempts = audit_trace if audit_trace is not None else trace
    # The registry cardinality is a progress guard, not a semantic result ceiling.
    for pass_number in range(1, len(allowed_values) + 2):
        if deadline.cancelled or deadline.remaining() <= 0:
            raise TimeoutError("discovery_continuation_deadline_exceeded")
        remaining_allowed_values = tuple(value for value in allowed_values if value not in selected)
        if not remaining_allowed_values:
            raise ValueError("discovery_continuation_exhausted_without_completion")
        pass_projection = _discovery_projection_for_remaining_scope(
            registry_projection=registry_projection,
            value_key=value_key,
            remaining_allowed_values=remaining_allowed_values,
        )
        if value_key == "candidate_operation_ids":
            pass_projection["selection_operation_dependency_contracts"] = {
                str(item["operation_id"]): validate_operation_dependency_references(item)
                for item in load_operation_catalog(registry_projection)
                if item.get("declared_prerequisite_for_operation_ids")
            }
        system_prompt, user_prompt = prompt_builder(
            original_text=original_text, session_context=session_context,
            registry_projection=pass_projection, already_selected_ids=selected,
        )
        if value_key == "candidate_operation_ids" and max_selected_values is not None:
            remaining_capacity = max_selected_values - len(selected)
            system_prompt += (
                f" This pass has capacity={remaining_capacity} additional justified operation IDs. "
                "Exhausting capacity requires continuation_required=false. Choose sufficient outputs, not optional reads."
            )
        call_schema = discovery_schema_for_registered_values(
            output_schema, value_key=value_key, allowed_values=remaining_allowed_values,
            max_selected_values=(
                None if max_selected_values is None else max_selected_values - len(selected)
            ),
            operation_contracts=(
                tuple(load_operation_catalog(registry_projection))
                if value_key == "candidate_operation_ids" else None
            ),
        )
        response_required = (
            value_key == "candidate_capability_ids"
            and "conversation.respond" in remaining_allowed_values
        )
        budget = require_prompt_budget(
            system_prompt, user_prompt, reserved_output_tokens=(
                OPERATION_DISCOVERY_RESERVED_OUTPUT_TOKENS
                if value_key == "candidate_operation_ids"
                else CANDIDATE_DISCOVERY_RESERVED_OUTPUT_TOKENS
            ),
            output_schema=call_schema, components=_prompt_material_components(system_prompt, user_prompt),
            num_ctx=SEMANTIC_SELECTION_NUM_CTX,
        )
        result = call(
            system_prompt=system_prompt, user_prompt=user_prompt, deadline=deadline,
            output_schema=call_schema,
        )
        raw = str(result.get("content", ""))
        attempt = _model_call_trace_item(
            result=result, call_role=call_role, pass_number=pass_number,
            requested_scope=remaining_allowed_values, already_selected_ids=selected, prompt_budget=budget,
        )
        call_attempts.append(attempt)
        verification_error = _model_call_verification_error(result)
        schema_repairable = (
            verification_error.startswith("model_structured_schema_invalid:")
            and result.get("raw_output_present") is True
            and result.get("truncation") is not True
            and str(result.get("done_reason", "")).lower() != "length"
            and bool(raw.strip())
        )
        if verification_error and not schema_repairable:
            attempt["validation_error"] = verification_error
            record_candidate_failure(raw, stage="VALIDATE", exc=ValueError(verification_error), repair_attempt=0, value_key=value_key)
            raise ValueError(verification_error)
        if int(budget["budget_num_ctx"]) != int(result.get("requested_num_ctx", -1)):
            attempt["validation_error"] = "budget_transport_num_ctx_mismatch"
            record_candidate_failure(raw, stage="VALIDATE", exc=ValueError("budget_transport_num_ctx_mismatch"), repair_attempt=0, value_key=value_key)
            raise ValueError("budget_transport_num_ctx_mismatch")
        try:
            if verification_error:
                # A completed response rejected by the transport schema still
                # uses the existing one-repair gate. Never accept it directly.
                raise ValueError(verification_error)
            parsed = parse_and_validate(raw, projection=pass_projection,
                                         response_required=response_required, repair_attempt=0)
        except (ValueError, TypeError, KeyError) as exc:
            record_candidate_failure(raw, stage="VALIDATE", exc=exc, repair_attempt=0, value_key=value_key)
            attempt["schema_valid"] = False
            attempt["validation_error"] = f"{type(exc).__name__}:{exc}"
            if repair_state is None or int(repair_state.get("model_backed_repair_count", 0)) >= 1:
                if repair_state is not None:
                    repair_state["model_backed_repair_blocked"] = "single_repair_limit_reached"
                raise
            repair_state["model_backed_repair_count"] = (
                int(repair_state.get("model_backed_repair_count", 0)) + 1
            )
            repair_system_prompt = (
                system_prompt
                + " Prior JSON invalid: "
                + str(attempt["validation_error"])[:160]
                + ". Return one complete replacement with the same meaning and current enum only; no duplicate or "
                "prior IDs. "
                + (
                    "You omitted the canonical response capability: candidate_capability_ids MUST include "
                    "conversation.respond. "
                    if value_key == "candidate_capability_ids"
                    and "canonical response capability" in str(attempt["validation_error"])
                    else ""
                )
                + "continuation_required=true requires at least one new ID and another distinct explicit "
                "unmet goal."
            )
            if value_key == "candidate_operation_ids":
                repair_system_prompt += (
                    " Cardinality overflow is not evidence that continuation is required. Choose the smallest "
                    "sufficient current subset. Keep continuation false when that subset satisfies the user's goal; "
                    "do not move optional overflow IDs into later passes."
                )
                discovery_error = str(attempt["validation_error"])
                if "operation selection justification coverage mismatch" in discovery_error:
                    repair_system_prompt += (
                        " selection_justifications must contain exactly one entry keyed by each selected non-null "
                        "operation ID, and no entries for unselected IDs. Every entry requires a valid goal_id, "
                        "justification_kind and original source_grounding. Remove any selected operation you cannot "
                        "justify; do not invent a goal or a dependency to fill a missing entry."
                    )
                if "operation_effect_not_justified_by_goal" in discovery_error:
                    repair_system_prompt += (
                        " Remove any operation whose catalog effect is outside the cited goal's typed effect intent; "
                        "creating an artifact does not itself require inspecting or executing it."
                    )
                if "operation_intent_not_supported_by_contract" in discovery_error:
                    repair_system_prompt += (
                        " Select only an operation declaring support for the cited goal's effect intent; "
                        "retrieving archive content cannot establish live availability of a configured dataset."
                    )
                if "operation_justification_not_source_grounded" in discovery_error:
                    repair_system_prompt += (
                        " source_grounding must copy an exact contiguous original request span, without paraphrase, "
                        "translation, inserted words or omitted interior words. Discard the rejected fragment and copy a "
                        "shorter verbatim fragment from original_text; do not copy a cut-off or corrected quotation. "
                        "Preserve the same requested operation."
                    )
                if "operation_dependency_not_registry_declared" in discovery_error:
                    repair_system_prompt += (
                        " DECLARED_OPERATION_DEPENDENCY is valid only when the catalog declares that prerequisite; "
                        "otherwise remove it unless it is independently a direct requested goal effect."
                    )
            repair_budget = require_prompt_budget(
                repair_system_prompt, user_prompt,
                reserved_output_tokens=(
                    OPERATION_DISCOVERY_RESERVED_OUTPUT_TOKENS
                    if value_key == "candidate_operation_ids"
                    else CANDIDATE_DISCOVERY_RESERVED_OUTPUT_TOKENS
                ),
                output_schema=call_schema,
                components=_prompt_material_components(repair_system_prompt, user_prompt),
                num_ctx=SEMANTIC_SELECTION_NUM_CTX,
            )
            repair_result = call(
                system_prompt=repair_system_prompt, user_prompt=user_prompt, deadline=deadline,
                output_schema=call_schema,
            )
            repair_attempt = _model_call_trace_item(
                result=repair_result, call_role=f"{call_role}_repair", pass_number=pass_number,
                requested_scope=remaining_allowed_values, already_selected_ids=selected,
                prompt_budget=repair_budget,
            )
            call_attempts.append(repair_attempt)
            repair_raw = str(repair_result.get("content", ""))
            repair_verification_error = _model_call_verification_error(repair_result)
            if repair_verification_error:
                repair_attempt["validation_error"] = repair_verification_error
                record_candidate_failure(repair_raw, stage="REPAIR_VALIDATE", exc=ValueError(repair_verification_error), repair_attempt=1, value_key=value_key)
                raise ValueError(repair_verification_error)
            if int(repair_budget["budget_num_ctx"]) != int(repair_result.get("requested_num_ctx", -1)):
                repair_attempt["validation_error"] = "budget_transport_num_ctx_mismatch"
                record_candidate_failure(str(repair_result.get("content", "")), stage="REPAIR_VALIDATE", exc=ValueError("budget_transport_num_ctx_mismatch"), repair_attempt=1, value_key=value_key)
                raise ValueError("budget_transport_num_ctx_mismatch")
            try:
                parsed = parse_and_validate(repair_raw, projection=pass_projection,
                                             response_required=response_required, repair_attempt=1)
            except (ValueError, TypeError, KeyError) as repair_exc:
                repair_attempt["schema_valid"] = False
                repair_attempt["validation_error"] = f"{type(repair_exc).__name__}:{repair_exc}"
                raise
            repair_attempt["schema_valid"] = True
            attempt = repair_attempt
        attempt["schema_valid"] = True
        values = parsed.selected_values
        if response_required and "conversation.respond" not in values:
            if "conversation.respond" in prior_model_selected_ids:
                # The model already selected the canonical response capability in the prior
                # authoritative pass of this turn; preserving it here when the model's
                # consolidation re-selection omits it is preservation, not host semantic injection.
                values = values + ("conversation.respond",)
                attempt["response_preserved"] = True
                attempt["response_preservation_provenance"] = tuple(prior_model_selected_ids)
            else:
                raise ValueError("accepted turn omitted canonical response capability")
        if any(value in selected for value in values):
            attempt["validation_error"] = "discovery selection repeats canonical state"
            raise ValueError("discovery selection repeats canonical state")
        new_values = values
        continuation = parsed.continuation_required
        summary = {
            "pass": pass_number, "already_selected_ids": selected,
            "new_ids": new_values, "continuation_required": continuation,
            "prompt_budget": budget,
            "selection_justifications": parsed.selection_justifications,
        }
        if call_attempts is trace:
            attempt.update(summary)
        else:
            trace.append(summary)
        if continuation and not new_values:
            attempt["validation_error"] = "discovery_continuation_no_progress"
            raise ValueError("discovery_continuation_no_progress")
        selected = tuple(dict.fromkeys(selected + new_values))
        if max_selected_values is not None and len(selected) > max_selected_values:
            attempt["validation_error"] = "operation_selection_exceeds_typed_justification_capacity"
            raise ValueError("operation_selection_exceeds_typed_justification_capacity")
        attempt["model_call_used"] = True
        if not continuation:
            return selected
        if max_selected_values is not None and len(selected) >= max_selected_values:
            attempt["validation_error"] = "operation_continuation_exceeds_typed_justification_capacity"
            raise ValueError("operation_continuation_exceeds_typed_justification_capacity")
    raise ValueError("discovery_continuation_progress_guard_exceeded")


def _discovery_projection_for_remaining_scope(
    *,
    registry_projection: dict[str, Any],
    value_key: str,
    remaining_allowed_values: tuple[str, ...],
) -> dict[str, Any]:
    """Remove host-owned prior selections from the next typed model scope."""
    if value_key == "candidate_capability_ids":
        return select_semantic_projection_details(
            registry_projection, remaining_allowed_values,
        )
    if value_key == "candidate_kinds":
        return projection_for_kinds(
            registry_projection, remaining_allowed_values,
        )
    if value_key == "candidate_operation_ids":
        remaining = set(remaining_allowed_values)
        result = json.loads(json.dumps(registry_projection))
        entries = []
        for entry in result.get("entries", ()):
            operations = [
                operation for operation in entry.get("operation_contracts", ())
                if str(operation.get("operation_id", "")) in remaining
            ]
            if not operations:
                continue
            entry["operation_contracts"] = operations
            entries.append(entry)
        result["entries"] = entries
        result["capability_count"] = len(entries)
        return result
    raise ValueError(f"unsupported discovery value key: {value_key}")


def _model_call_verification_error(result: dict[str, Any]) -> str:
    """Return the exact failed envelope predicate instead of collapsing failures."""
    if not isinstance(result, dict):
        return "semantic_result_envelope_not_object"
    if result.get("model_call_attempted") is not True:
        return "model_call_attempted_not_true"
    if result.get("model_call_succeeded") is not True:
        detail = str(result.get("transport_error") or result.get("error") or "UNKNOWN")
        return f"model_call_succeeded_not_true:{detail}"
    if result.get("final_valid") is not True or result.get("schema_valid") is False:
        detail = str(result.get("validation_error") or (
            "final_valid_not_true" if result.get("final_valid") is not True else "schema_valid_false"
        ))
        return f"model_structured_schema_invalid:{detail}"
    if result.get("raw_output_present") is not True:
        return "raw_output_present_not_true"
    if result.get("truncation") is True or str(result.get("done_reason", "")).lower() == "length":
        return "model_output_truncated"
    if not str(result.get("content", "")).strip():
        return "visible_structured_content_empty"
    if result.get("ok") is not True:
        detail = str(result.get("error") or "UNKNOWN")
        return f"model_call_ok_not_true:{detail}"
    return ""


def _model_call_trace_item(
    *, result: dict[str, Any], call_role: str, pass_number: int,
    requested_scope: tuple[str, ...], already_selected_ids: tuple[str, ...],
    prompt_budget: dict[str, Any],
) -> dict[str, Any]:
    """Sanitized model telemetry stored in the existing semantic audit trace."""
    return {
        "model_id": result.get("response_model_id") or result.get("model_id"),
        "call_role": call_role,
        "pass_number": pass_number,
        "requested_scope": requested_scope,
        "already_selected_ids": already_selected_ids,
        "model_call_attempted": result.get("model_call_attempted"),
        "model_call_succeeded": result.get("model_call_succeeded"),
        "model_call_used": False,
        "raw_output_present": result.get("raw_output_present"),
        "schema_valid": None,
        "validation_error": "",
        "done": result.get("done"),
        "done_reason": result.get("done_reason"),
        "prompt_eval_count": result.get("prompt_eval_count"),
        "eval_count": result.get("eval_count"),
        "prompt_eval_duration": result.get("prompt_eval_duration"),
        "eval_duration": result.get("eval_duration"),
        "load_duration": result.get("load_duration"),
        "total_duration": result.get("total_duration"),
        "configured_num_ctx": result.get("configured_num_ctx"),
        "requested_num_ctx": result.get("requested_num_ctx"),
        "observed_context_length": result.get("observed_context_length"),
        "budget_num_ctx": prompt_budget.get("budget_num_ctx"),
        "context_authority_source": result.get("context_authority_source"),
        "model_role": result.get("model_role"),
        "configured_component_timeout_seconds": result.get(
            "configured_component_timeout_seconds"
        ),
        "timeout_policy_source": result.get("timeout_policy_source"),
        "request_deadline_remaining_before_call": result.get(
            "request_deadline_remaining_before_call"
        ),
        "effective_transport_timeout_seconds": result.get(
            "effective_transport_timeout_seconds"
        ),
        "transport_started_at": result.get("transport_started_at"),
        "transport_finished_at": result.get("transport_finished_at"),
        "transport_duration_seconds": result.get("transport_duration_seconds"),
        "cold_warm_state": result.get("cold_warm_state", "UNKNOWN"),
        "truncation": result.get("truncation"),
        "transport_error": result.get("transport_error"),
        "error_type": result.get("error_type"),
        "error_message": result.get("error_message"),
        "sanitized_structured_model_content": result.get("content", ""),
        "raw_response_sha256": result.get("raw_response_sha256"),
        "raw_model_result": result.get("raw_model_result"),
        "prompt_budget": prompt_budget,
    }


def _canonical_memory_filter(registry_projection: dict[str, Any]) -> dict[str, str] | None:
    filters = tuple(validate_memory_filter(goal["memory_filter"])
        for goal in registry_projection.get("selection_goalframes", ())
        if isinstance(goal, dict) and goal.get("memory_filter") is not None)
    if not filters:
        return None
    if any(value != filters[0] for value in filters[1:]):
        raise ValueError("multiple_memory_filters_need_distinct_operation_binding")
    return filters[0]


def _hydrate_host_owned_understanding_fields(
    content: Any, registry_projection: dict[str, Any],
) -> dict[str, Any]:
    """Hydrate registry/contract facts after the model has supplied meaning and parameters."""
    raw = json.loads(content) if isinstance(content, str) else dict(content)
    canonical_artifact_requirements = {
        str(item["requirement_id"]): item
        for item in registry_projection.get("selection_artifact_operation_requirements", ())
        if isinstance(item, dict) and item.get("requirement_id")
    }
    canonical_filter = _canonical_memory_filter(registry_projection)
    for operation_parameters in (raw.get("operation_requirements") or {}).values():
        if not isinstance(operation_parameters, dict):
            continue
        if canonical_filter is not None and "memory_filter" in operation_parameters:
            supplied = operation_parameters["memory_filter"]
            supplied = json.loads(supplied) if isinstance(supplied, str) else supplied
            if validate_memory_filter(supplied) != canonical_filter:
                raise ValueError("memory_filter_drift_from_canonical_goal")
        logical_spec = operation_parameters.get("logical_spec")
        if isinstance(logical_spec, dict):
            logical_spec["_canonical_requirement_ids"] = list(canonical_artifact_requirements)
            hydrated_semantics = []
            for reference in logical_spec.get("semantic_requirements") or ():
                if not isinstance(reference, dict):
                    raise ValueError("artifact_operation_reference_invalid")
                requirement_id = str(reference.get("requirement_id", ""))
                canonical = canonical_artifact_requirements.get(requirement_id)
                if canonical is None:
                    raise ValueError("artifact_operation_reference_unknown")
                hydrated_semantics.append({
                    "requirement_id": requirement_id,
                    "operation_class": str(canonical["operation_class"]),
                    "source_grounding": str(canonical["source_grounding"]),
                    "step_id": str(reference.get("step_id", "")),
                    "provider_name": str(canonical.get("provider_name", "")),
                    "provider_provenance": str(canonical.get("provider_provenance", "NONE")),
                    "provider_inference_justification": str(
                        canonical.get("provider_inference_justification", "")
                    ),
                })
            logical_spec["semantic_requirements"] = hydrated_semantics
        if isinstance(logical_spec, dict) and isinstance(logical_spec.get("constraints"), list):
            logical_spec["constraints"] = list(dict.fromkeys(logical_spec["constraints"]))
    entries = tuple(registry_projection.get("entries", ()))
    catalog = load_operation_catalog(registry_projection)
    if not catalog:
        raise ValueError("host_hydration_operation_catalog_empty")
    effect_rank = {"OBSERVE": 0, "MUTATE": 1, "EXECUTE": 2, "EXPORT": 3, "PERSIST": 4, "UNKNOWN": 5}
    risk_rank = {"READ_ONLY": 0, "MUTATION": 1, "DANGEROUS": 2, "UNKNOWN": 3}
    reversibility_rank = {
        "REVERSIBLE": 0, "PARTIALLY_REVERSIBLE": 1, "IRREVERSIBLE": 2, "UNKNOWN": 3,
    }
    governing = max(catalog, key=lambda item: effect_rank[str(item["effect_type"])])
    goalframes = tuple(
        item for item in registry_projection.get("selection_goalframes", ())
        if isinstance(item, dict)
    )
    if not goalframes:
        raise ValueError("host_hydration_goalframes_empty")
    if "selection_response_requirements" in registry_projection:
        presentation = hydrate_response_requirements(goalframes, tuple(registry_projection["selection_response_requirements"]))
        violations = _goalframe_response_requirement_violations(list(goalframes), presentation)
        if violations:
            raise ValueError(";".join(reason for _, reason in violations))
        # Copy existing model-authored obligations, never compose answer prose.
        # Reference IDs follow the SAME canonical response-reference validator.
        raw["response_requirements"] = [{
            "response_requirement_id": f"goalframe_response_{index}",
            "applies_to_goal_ids": list(requirement["applies_to_goal_ids"]),
            "description": requirement.get("description", ""),
            **({"memory_query_kind": requirement["memory_query_kind"]} if "memory_query_kind" in requirement else {}),
            **({"subject_binding": dict(requirement["subject_binding"])} if requirement.get("subject_binding") is not None else {}),
            **({"requirement_kind": requirement["requirement_kind"]} if requirement.get("requirement_kind") is not None else {}),
        } for index, requirement in enumerate(presentation)]
    if "selection_response_requirements" in registry_projection:
        expected = hydrate_response_requirements(goalframes, tuple(registry_projection["selection_response_requirements"]))
        validate_response_obligation_coverage(expected, tuple({"schema_version": "response_requirement.v1", **q} for q in raw["response_requirements"]))
    raw.update({
        "goals": [{
            "goal_id": str(item["goal_id"]),
            "description": str(item.get("requested_outcome", ""))[:160],
        } for item in goalframes],
        "required_capabilities": [{
            "capability_id": str(entry["capability_id"]),
            "purpose": str(entry.get("description", "authoritative selected capability"))[:96],
            "required": True,
        } for entry in entries],
        "effect_type": str(governing["effect_type"]),
        "target_scope": str(governing["target_scope"]),
        "reversibility": max(
            (str(item["reversibility"]) for item in catalog), key=reversibility_rank.__getitem__,
        ),
        "external_side_effect": any(item.get("external_side_effect") is True for item in catalog),
        "unresolved_capabilities": [],
        "risk_class": max((str(item["risk_class"]) for item in catalog), key=risk_rank.__getitem__),
        "execution_restriction": str(
            registry_projection.get("selection_execution_restriction", "NONE")
        ),
        "execution_restriction_source": str(
            registry_projection.get("selection_execution_restriction_source", "")
        ),
    })
    return raw


def _understand(model_port: ModelUnderstandingPort, deadline: RequestDeadline, request_id: str, text: str,
                identity: IdentityContext, session_context: dict[str, Any], replan_reason: str = "",
                input_preparation: dict[str, Any] | None = None,
                audit_trace: dict[str, Any] | None = None,
                registry_projection: dict[str, Any] | None = None) -> RequestUnderstanding | None:
    system_prompt, user_prompt = build_request_understanding_prompt(
        request_id=request_id, original_text=text, identity=identity, session_context=session_context,
        input_preparation=input_preparation, registry_projection=registry_projection,
    )
    if replan_reason:
        if audit_trace is not None and int(audit_trace.get("model_backed_repair_count", 0)) >= 1:
            audit_trace["model_backed_repair_blocked"] = "single_repair_limit_reached"
            return None
        if audit_trace is not None:
            audit_trace["model_backed_repair_count"] = int(audit_trace.get("model_backed_repair_count", 0)) + 1
        # Preserve the full validation reason in the trace, but keep the
        # same-model repair instruction within the already admitted context.
        violation_codes = tuple(dict.fromkeys(
            item.removeprefix("logical_spec_")
            for item in replan_reason.removeprefix("contract_violations:").split(",")
            if item and item != "structured_semantics_consistent"
        ))
        system_prompt += (
            " Repair typed violations; preserve intent and copy exact source spans: "
            + ";".join(violation_codes)[:190]
        )
        if any(code in {"assignment_not_set_field", "transform_not_transform"} for code in violation_codes):
            system_prompt += (
                " Re-evaluate each cited step from meaning: ASSIGN is only set_field; computation deriving new "
                "content is TRANSFORM with action transform. Remove semantic_requirements for condition, route, "
                "merge, and other mere control-flow steps."
            )
        if any(code in {
            "intrinsic_trigger_not_canonical", "host_operation_used_as_artifact_trigger",
            "host_capability_used_as_artifact_trigger",
        } for code in violation_codes):
            system_prompt += " Use the intrinsic trigger literal, never catalog_query."
        if "catalog_operation_repeats_semantic_class" in violation_codes:
            system_prompt += (
                " catalog_query.semantic_operation is the concise intended action verb, not its class; "
                "arguments use semantic display names."
            )
        if "explicit_provider_has_inference" in violation_codes:
            system_prompt += " SOURCE_EXPLICIT has empty inference justification."
        if "unreferenced_real_operation_step" in violation_codes:
            system_prompt += " Remove every real operation step not referenced by a canonical requirement."
        if any(code in {
            "all_intrinsic_set_no_capability_coverage",
            "real_operation_misrepresented_as_set_field",
            "real_operation_not_operational_step",
            "explicit_provider_constraint_not_covered",
            "provider_provenance_mismatch",
        } for code in violation_codes):
            system_prompt += (
                " Decorative fields cannot stand for a requested operation. Replace them with the real semantic "
                "step: transform for intrinsic computation, jarvis_capability for another selected canonical "
                "capability, or catalog_query for a named/external provider. Keep an unavailable named provider "
                "as catalog_query so the host can report its truthful disposition. condition, route, and merge are "
                "only control flow and cannot substitute for that real operation."
            )
    try:
        call_schema = request_understanding_schema_for_projection(registry_projection, source_text=text)
        prompt_budget = require_prompt_budget(
            system_prompt, user_prompt, reserved_output_tokens=REQUEST_UNDERSTANDING_RESERVED_OUTPUT_TOKENS,
            output_schema=call_schema,
            components=_prompt_material_components(system_prompt, user_prompt),
            num_ctx=REQUEST_UNDERSTANDING_NUM_CTX,
        )
        model_call = getattr(model_port, "repair", None) if replan_reason else model_port.understand
        if not callable(model_call):
            model_call = model_port.understand
        call_kwargs = {
            "system_prompt": system_prompt, "user_prompt": user_prompt, "deadline": deadline,
        }
        if getattr(model_port, "supports_call_scoped_understanding_schema", False) is True:
            call_kwargs["output_schema"] = call_schema
        result = model_call(**call_kwargs)
        if audit_trace is not None:
            attempts = audit_trace.setdefault("main_model_attempts", [])
            attempt = _model_call_trace_item(
                result=result, call_role="request_understanding_repair" if replan_reason else "request_understanding",
                pass_number=len(attempts) + 1, requested_scope=(), already_selected_ids=(),
                prompt_budget=prompt_budget,
            )
            attempt["repair_reason"] = replan_reason
            attempts.append(attempt)
        verification_error = _model_call_verification_error(result)
        if verification_error:
            if audit_trace is not None:
                audit_trace["main_model_attempts"][-1]["validation_error"] = verification_error
            return None
        if int(prompt_budget["budget_num_ctx"]) != int(result.get("requested_num_ctx", -1)):
            if audit_trace is not None:
                audit_trace["main_model_attempts"][-1]["validation_error"] = (
                    "budget_transport_num_ctx_mismatch"
                )
            return None
        host_context_trace_ids = tuple(
            str(turn.get("trace_id", ""))
            for turn in session_context.get("bounded_chronological_turns", ())
            if isinstance(turn, dict) and str(turn.get("trace_id", "")).strip()
        )
        model_content: Any = result.get("content", "")
        if (
            registry_projection is not None
            and getattr(model_port, "supports_call_scoped_understanding_schema", False) is True
        ):
            model_content = _hydrate_host_owned_understanding_fields(
                model_content, registry_projection,
            )
        parsed = parse_request_understanding_payload(
            model_content,
            host_request_id=request_id,
            host_original_text=text,
            host_relevant_context_trace_ids=host_context_trace_ids,
            authoritative_operation_catalog=(
                tuple(load_operation_catalog(registry_projection))
                if getattr(model_port, "supports_call_scoped_understanding_schema", False) is True
                else None
            ),
        )
        if audit_trace is not None:
            audit_trace["main_model_attempts"][-1]["schema_valid"] = True
            audit_trace["main_model_attempts"][-1]["model_call_used"] = True
            audit_trace["main_model_attempts"][-1]["parsed_understanding"] = parsed.to_read_model()
        return parsed
    except (TimeoutError, ValueError, TypeError, KeyError) as exc:
        if audit_trace is not None and audit_trace.get("main_model_attempts"):
            audit_trace["main_model_attempts"][-1]["schema_valid"] = False
            audit_trace["main_model_attempts"][-1]["validation_error"] = f"{type(exc).__name__}:{exc}"
        if (
            isinstance(exc, ValueError)
            and not replan_reason
            and int((audit_trace or {}).get("model_backed_repair_count", 0)) < 1
        ):
            return _understand(
                model_port, deadline, request_id, text, identity, session_context,
                replan_reason=f"strict_model_output:{exc}",
                input_preparation=input_preparation, audit_trace=audit_trace,
                registry_projection=registry_projection,
            )
        return None


def _execute_evidence(understanding: RequestUnderstanding, plan: ExecutionPlan, trace_id: str,
                      identity: IdentityContext, session_context: dict[str, Any], deadline: RequestDeadline,
                      capability_ids: tuple[str, ...], ports: dict[str, Any], permissions: tuple[Any, ...] = (),
                      dependency_plan: ExecutionPlan | None = None) -> EvidenceBundle:
    bundles = []
    original_plan = dependency_plan or plan
    dependency_bound = any(step.declared_prerequisite_for_operation_ids for step in original_plan.steps)
    execution_units = (
        tuple((step.capability_id, (step,)) for step in plan.steps)
        if dependency_bound else tuple(
            (capability_id, tuple(step for step in plan.steps if step.capability_id == capability_id))
            for capability_id in capability_ids
        )
    )
    for capability_id, capability_steps in execution_units:
        prerequisites = tuple(step for step in original_plan.steps if any(
            target.operation in step.declared_prerequisite_for_operation_ids for target in capability_steps
        ))
        if prerequisites:
            accumulated = EvidenceBundle(understanding.request_id, "+".join(capability_ids), trace_id,
                "PARTIAL", tuple(item for b in bundles for item in b.items), (),
                tuple(receipt for b in bundles for receipt in b.receipts), ())
            missing = tuple(step.operation for step in prerequisites if not all(
                truth["executed"] for truth in _step_execution_truth((step,), accumulated,
                    expected_provider_id=str(getattr(ports.get(step.capability_id), "provider_id", "")))
            ))
            if missing:
                bundles.append(EvidenceBundle(understanding.request_id, capability_id, trace_id,
                    "UNAVAILABLE", (), (), (), ("operation_dependency_unproven:" + ",".join(missing),)))
                continue
        if not capability_steps:
            continue
        subplan = ExecutionPlan(request_id=plan.request_id, steps=capability_steps)
        port = ports[capability_id]
        bind_permission = getattr(port, "bind_host_permission", None)
        if callable(bind_permission):
            bind_permission(permissions=tuple(permissions), plan=subplan, trace_id=trace_id)
        if capability_id == "conversation.respond":
            bundle = port.collect_evidence(understanding, subplan, trace_id, identity, session_context, deadline)
            # Context/identity evidence is not execution of the user-visible response.
            if bundle.receipts:
                bundle = EvidenceBundle(
                    request_id=bundle.request_id, capability_id=bundle.capability_id, trace_id=bundle.trace_id,
                    status=bundle.status, items=bundle.items, limitations=bundle.limitations,
                    receipts=(), errors=bundle.errors, capability_ids=bundle.capability_ids,
                )
        else:
            bundle = port.collect_evidence(understanding, subplan, trace_id, deadline)
        # Sandbox review is a post-execution gate.  The simulation provider already
        # emitted the typed result/evidence; review consumes that same result before
        # this canonical bundle is finalized.  Keep the import lazy to preserve the
        # existing dependency direction and avoid making SANDBOX_REVIEW an executor.
        # Dispatch by the typed evidence contract, not by a concrete provider
        # or skill identifier.  Any provider that emits a valid simulation
        # result receives the same review treatment; unrelated evidence does
        # not enter the simulation review path.
        if any(item.kind == "simulation_result" for item in bundle.items):
            from MAKSIMAR_CORE_LIB.workers_registry.simulation_io_contracts import SimulationEngineResult
            from MAKSIMAR_SERVER.SANDBOX_REVIEW.sandbox_result_reader import review_simulation_result

            review_items: list[EvidenceItem] = []
            review_errors = list(bundle.errors)
            for item in bundle.items:
                if item.kind != "simulation_result":
                    continue
                try:
                    result_payload = json.loads(item.observation)
                    simulation_result = SimulationEngineResult(**result_payload)
                    review = review_simulation_result(simulation_result)
                except (TypeError, ValueError, KeyError, json.JSONDecodeError) as exc:
                    review = {"review_status": "REJECTED", "reason": f"review_input_invalid:{type(exc).__name__}"}
                review_status = str(review.get("review_status", "REJECTED"))
                review_observation = json.dumps(review, ensure_ascii=False, sort_keys=True)
                review_digest = hashlib.sha256(review_observation.encode("utf-8")).hexdigest()
                review_items.append(EvidenceItem(
                    kind="sandbox_review",
                    source="MAKSIMAR_SERVER.SANDBOX_REVIEW.sandbox_result_reader:review_simulation_result",
                    observation=review_observation,
                    scope="local_simulation_runtime",
                    confidence=1.0 if review_status == "REVIEWED" else 0.0,
                    trace_id=trace_id,
                    observed_at=utc_observed_at(),
                    content_hash=f"sha256:{review_digest}",
                    source_reference=f"review://simulation/{item.request_id}/{item.step_id}",
                    request_id=item.request_id,
                    step_id=item.step_id,
                    capability_id=item.capability_id,
                    operation_id=item.operation_id,
                    provider_id="sandbox_review",
                ))
                if review_status != "REVIEWED":
                    review_errors.append(f"sandbox_review:{item.step_id}:{review.get('reason', 'rejected')}")
            if review_items or review_errors != list(bundle.errors):
                bundle = EvidenceBundle(
                    request_id=bundle.request_id, capability_id=bundle.capability_id,
                    trace_id=bundle.trace_id, status=("PARTIAL" if review_errors else bundle.status),
                    items=bundle.items + tuple(review_items), limitations=bundle.limitations,
                    receipts=bundle.receipts, errors=tuple(review_errors), capability_ids=bundle.capability_ids,
                )
        bundles.append(bundle)
    statuses = {bundle.status for bundle in bundles}
    status = "COMPLETE" if bundles and statuses == {"COMPLETE"} else "PARTIAL" if bundles else "UNAVAILABLE"
    return EvidenceBundle(
        request_id=understanding.request_id,
        capability_id="+".join(capability_ids),
        trace_id=trace_id,
        status=status,
        items=tuple(item for bundle in bundles for item in bundle.items),
        limitations=tuple(item for bundle in bundles for item in bundle.limitations),
        receipts=tuple(item for bundle in bundles for item in bundle.receipts),
        errors=tuple(item for bundle in bundles for item in bundle.errors),
        capability_ids=capability_ids,
    )


def _record_completed_conversation_response(
    *, evidence: EvidenceBundle, plan: ExecutionPlan, capability_truth: list[dict[str, Any]],
) -> tuple[EvidenceBundle, list[dict[str, Any]]]:
    response_steps = tuple(
        step for step in plan.steps if step.capability_id == "conversation.respond" and step.operation == "respond"
    )
    if not response_steps:
        return evidence, capability_truth
    receipts = evidence.receipts + tuple(ExecutionReceipt(
        receipt_id=f"{evidence.trace_id}:{step.step_id}:final_brain",
        request_id=evidence.request_id, trace_id=evidence.trace_id, step_id=step.step_id,
        capability_id=step.capability_id, operation_id=step.operation,
        provider_id="existing_jarvis_final_brain", status="COMPLETE",
        result="visible Final Brain response generated and canonically validated",
    ) for step in response_steps)
    updated_evidence = EvidenceBundle(
        request_id=evidence.request_id, capability_id=evidence.capability_id, trace_id=evidence.trace_id,
        status=evidence.status, items=evidence.items, limitations=evidence.limitations,
        receipts=receipts, errors=evidence.errors, capability_ids=evidence.capability_ids,
    )
    updated_truth = [dict(item) for item in capability_truth]
    for item in updated_truth:
        if item.get("capability_id") != "conversation.respond":
            continue
        step_truth = _step_execution_truth(
            response_steps, updated_evidence, expected_provider_id="existing_jarvis_final_brain",
        )
        item["step_execution_truth"] = step_truth
        item["executed"] = bool(step_truth) and all(step["executed"] for step in step_truth)
        item["execution_receipt_present"] = bool(step_truth) and all(
            step["execution_receipt_present"] for step in step_truth
        )
    return updated_evidence, updated_truth


def _select_relevant_session_context(context: dict[str, Any],
                                     understanding: RequestUnderstanding) -> dict[str, Any]:
    """Use host-bounded chronology; model output never owns trace identifiers."""
    chronological = tuple(context.get("bounded_chronological_turns", ()))
    result = dict(context)
    result["recent_relevant_turns"] = chronological
    result["semantic_selection_trace_ids"] = understanding.relevant_context_trace_ids
    result["selection_basis"] = "host_bounded_chronological_context"
    return result


def _projection_capability_truth(
    capability_ids: tuple[str, ...], registry_projection: dict[str, Any] | None, *, identity: IdentityContext,
) -> tuple[dict[str, Any], ...]:
    entries = {
        str(item["capability_id"]): item for item in (registry_projection or {}).get("entries", ())
    }
    return tuple({
        "capability_id": capability_id,
        "capability_exists": capability_id in entries,
        "operation_contract_source": str(entries.get(capability_id, {}).get("operation_contract_source", "VISIBILITY_ONLY")),
        "execution_contract_available": entries.get(capability_id, {}).get("execution_contract_available") is True,
        "selection_mode": str(entries.get(capability_id, {}).get("selection_mode", "VISIBILITY_ONLY")),
        "provider_id": next(iter(entries.get(capability_id, {}).get("provider_ids", ())), ""),
        "provider_exists": entries.get(capability_id, {}).get("provider_exists") is True,
        "provider_binding_status": str(entries.get(capability_id, {}).get("provider_binding_status", "UNBOUND")),
        "provider_available": entries.get(capability_id, {}).get("provider_available"),
        "identity_eligible": bool(identity.trusted), "policy_execution_allowed": False,
        "permissions_granted": False, "executed": False, "execution_receipt_present": False,
        "step_execution_truth": (),
    } for capability_id in capability_ids)


def _step_execution_truth(
    steps: tuple[PlanStep, ...], evidence: EvidenceBundle, *, expected_provider_id: str,
) -> tuple[dict[str, Any], ...]:
    truths = []
    for step in steps:
        receipts = tuple(receipt for receipt in evidence.receipts if (
            receipt.request_id == evidence.request_id and receipt.trace_id == evidence.trace_id
            and receipt.step_id == step.step_id and receipt.capability_id == step.capability_id
            and receipt.operation_id == step.operation and receipt.provider_id == expected_provider_id
        ))
        complete = tuple(receipt for receipt in receipts if receipt.status == "COMPLETE")
        step_evidence = tuple(item.to_read_model() for item in evidence.items if (
            item.step_id == step.step_id and item.capability_id == step.capability_id
            and item.operation_id == step.operation
        ))
        truths.append({
            "request_id": evidence.request_id, "trace_id": evidence.trace_id,
            "step_id": step.step_id, "capability_id": step.capability_id,
            "operation_id": step.operation,
            "provider_id": complete[0].provider_id if complete else receipts[0].provider_id if receipts else "",
            "executed": bool(complete), "execution_receipt_present": bool(receipts),
            "receipt_ids": tuple(receipt.receipt_id for receipt in receipts),
            "execution_status": complete[0].status if complete else receipts[0].status if receipts else "NOT_EXECUTED",
            "evidence_items": step_evidence,
        })
    return tuple(truths)


def _discover_providers(
    capability_ids: tuple[str, ...], registry_projection: dict[str, Any] | None,
) -> dict[str, tuple[dict[str, object], ...]]:
    if registry_projection is None:
        return {capability_id: discover_capability_providers(capability_id) for capability_id in capability_ids}
    return {
        capability_id: discover_projected_capability_providers(registry_projection, capability_id)
        for capability_id in capability_ids
    }


def _operation_resolution_error(understanding: RequestUnderstanding, capability_ids: tuple[str, ...],
                                providers: dict[str, tuple[dict[str, object], ...]],
                                registry_projection: dict[str, Any] | None = None) -> str:
    if not capability_ids:
        return "capability_unresolved"
    requirements = {
        item.capability_id: item for item in understanding.required_capabilities if item.required
    }
    execution_required = {
        capability_id for capability_id, item in requirements.items() if item.operation_contract_required
    }
    entries = {
        str(item["capability_id"]): item for item in (registry_projection or {}).get("entries", ())
    }
    for capability_id in execution_required:
        entry = entries.get(capability_id)
        if registry_projection is not None and (
            entry is None or entry.get("execution_contract_available") is not True
        ):
            return f"execution_contract_unavailable:{capability_id}"
        if not providers.get(capability_id):
            return f"provider_binding_unresolved:{capability_id}"
    declared_capabilities = set(capability_ids)
    for requirement in understanding.operation_requirements:
        contract = operation_contract(requirement.operation_id, registry_projection)
        if requirement.capability_id not in declared_capabilities:
            return f"operation_capability_not_declared:{requirement.capability_id}"
        if contract is None or contract["capability_id"] != requirement.capability_id:
            return f"operation_not_resolved:{requirement.operation_id}"
        if requirement.declared_prerequisite_for_operation_ids != validate_operation_dependency_references(contract):
            return f"operation_dependency_contract_drift:{requirement.operation_id}"
        if set(requirement.required_evidence) != set(contract["evidence_kinds"]):
            return f"operation_evidence_contract_mismatch:{requirement.operation_id}"
        if requirement.capability_id not in execution_required:
            return f"operation_not_required_for_consideration_only_capability:{requirement.capability_id}"
    operation_capabilities = {item.capability_id for item in understanding.operation_requirements if item.required}
    missing = execution_required - operation_capabilities
    if missing:
        return "operation_requirement_missing:" + ",".join(sorted(missing))
    return ""


def _trace(trace_id: str, request_id: str, stages: list[str], capabilities: tuple[str, ...],
           providers: tuple[str, ...], policy: str, evidence: str, final: str, reason: str) -> OrchestrationTrace:
    return OrchestrationTrace(
        trace_id=trace_id, request_id=request_id, route="canonical_semantic_turn_v2", stages=tuple(stages),
        selected_capabilities=capabilities, selected_providers=providers, policy_result=policy,
        evidence_status=evidence, final_brain_status=final, rollback_reason=reason,
    )


def _failure(trace_id: str, request_id: str, stages: list[str], status: str, reason: str,
             understanding: RequestUnderstanding | None = None, *, selected_capabilities: tuple[str, ...] = (),
             permission: Any = None, safety_validation: dict[str, object] | None = None) -> dict[str, Any]:
    trace = _trace(trace_id, request_id, stages, selected_capabilities, (), "NOT_ALLOWED",
                   "NOT_COLLECTED", "NOT_CALLED", reason)
    return {
        "handled": True, "orchestration_path": "canonical_semantic_turn_v2", "trace_id": trace_id,
        "understanding": understanding.to_read_model() if understanding else None,
        "understanding_schema_version": understanding.schema_version if understanding else "",
        "selected_capabilities": selected_capabilities, "selected_provider_operation": (),
        "selection_source": "model_semantic_registry" if understanding else "none",
        "fallback_used": False, "fallback_reason": "", "capability_status": status,
        "operation_status": status, "degradation": status, "response_text": _degraded_response(reason),
        "permission_decision": permission, "safety_validation": safety_validation,
        "evidence_bundle": None, "execution_plan": None,
        "trace": trace.to_read_model(), "project_tools_used": False,
    }


def _degraded_response(detail: str) -> str:
    return f"Не могу достоверно завершить запрос: {detail}. Запрошенная цель не была подменена другой операцией."
