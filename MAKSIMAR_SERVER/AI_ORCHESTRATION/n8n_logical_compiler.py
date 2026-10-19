"""Provider-neutral logical automation spec -> installed n8n graph compiler.

The 8B model expresses WHAT automation is wanted (a logical spec: trigger, steps,
desired output, constraints). This HOST-side compiler resolves each logical step to an
exact installed n8n 2.26.0 node contract via the version-pinned LOCAL catalog.

Resolution uses typed intrinsic actions and exact installed provider/operation contracts.
Catalog search supplies discovery evidence to the existing Semantic Spine; search scores
and description tokens never select an executable provider or operation.
"""
from __future__ import annotations

import json
from typing import Any

from MAKSIMAR_SERVER.AI_ORCHESTRATION.n8n_local_catalog import (
    credential_requirements,
    network_scope,
    node_contract,
    operation_candidates,
    parameter_contract,
    runtime_role,
    transport_requirement,
)

# Small set of universal intrinsic primitives with deterministic value. NOT a capability
# catalog: everything else resolves through the installed catalog. The MODEL-FACING schema
# advertises only the canonical names (set_field / transform / condition / http_request);
# the synonym keys below remain for backward compatibility with already-created specs.
LOGICAL_ACTION_TO_N8N_TYPE: dict[str, str] = {
    "manual_trigger": "n8n-nodes-base.manualTrigger",
    "schedule_trigger": "n8n-nodes-base.scheduleTrigger",
    "webhook_trigger": "n8n-nodes-base.webhook",
    "set_field": "n8n-nodes-base.set",
    "set_value": "n8n-nodes-base.set",
    "set": "n8n-nodes-base.set",
    "assign": "n8n-nodes-base.set",
    "transform": "n8n-nodes-base.code",
    "code_transform": "n8n-nodes-base.code",
    "http_request": "n8n-nodes-base.httpRequest",
    "jarvis_capability": "n8n-nodes-base.httpRequest",
    "condition": "n8n-nodes-base.if",
    "branch": "n8n-nodes-base.if",
    "if": "n8n-nodes-base.if",
}

JARVIS_CANONICAL_HOT_ENDPOINT = "http://127.0.0.1:8000/jarvis-live/hot"

# Tiny intrinsic comparison operator map for the IF node (universal primitive, NOT a
# capability catalog). The condition compares a field against a literal value.
_CONDITION_OPERATORS: dict[str, dict[str, str]] = {
    "equals": {"type": "string", "operation": "equals"},
    "equal": {"type": "number", "operation": "equal"},
    "not_equals": {"type": "string", "operation": "notEquals"},
    "contains": {"type": "string", "operation": "contains"},
    "greater": {"type": "number", "operation": "larger"},
    "less": {"type": "number", "operation": "smaller"},
    "exists": {"type": "string", "operation": "exists", "singleValue": True},
    "not_exists": {"type": "string", "operation": "notExists", "singleValue": True},
}

class LogicalSpecCompileError(ValueError):
    """Raised when a logical spec cannot be compiled to installed n8n contracts."""


def _installed(n8n_type: str) -> dict[str, Any] | None:
    contract = node_contract(n8n_type)
    if not contract.get("found"):
        return None
    return contract["node"]


def resolve_logical_step(step: dict[str, Any]) -> tuple[str | None, dict[str, Any] | None]:
    """Bind a typed model choice to its exact installed contract, never search rank."""
    intent = str(step.get("intent") or step.get("action") or "")
    n8n_type = LOGICAL_ACTION_TO_N8N_TYPE.get(intent)
    if n8n_type:
        return n8n_type, _installed(n8n_type)
    provider_identity = str(step.get("provider_name") or "")
    if not provider_identity:
        return None, None
    result = node_contract(provider_identity)
    if not result.get("found") and "_" in provider_identity:
        # Existing typed provider names admit identifier separators; compare a
        # complete installed display identity, never tokens from a natural query.
        result = node_contract(provider_identity.replace("_", " "))
    if not result.get("found"):
        return None, None
    node = result["node"]
    if runtime_role(node) != "USER_USABLE":
        return None, None
    return str(node["type"]), node


def installed_provider_operation_ids(provider_name: str) -> tuple[str, ...]:
    """Return bounded exact operation IDs from the installed provider contract."""
    n8n_type, node = resolve_logical_step({
        "provider_name": provider_name, "catalog_query": provider_name,
    })
    if n8n_type is None or node is None:
        return ()
    return tuple(dict.fromkeys(
        str(item.get("operation") or "") for item in operation_candidates(node)
        if str(item.get("operation") or "") and str(item.get("operation") or "") != "__CUSTOM_API_CALL__"
    ))


def _semantic_tokens(value: Any) -> tuple[str, ...]:
    import re
    return tuple(token for token in re.findall(r"[^\W_]+", str(value or "").casefold()) if len(token) > 1)


def _source_mentions_provider(source_text: str | None, provider_name: str) -> bool:
    """Mechanically verify an explicit provider surface, admitting identifier separators."""
    provider_tokens = _semantic_tokens(provider_name)
    source_tokens = _semantic_tokens(source_text)
    if not provider_tokens:
        return False
    width = len(provider_tokens)
    return any(source_tokens[index:index + width] == provider_tokens
               for index in range(len(source_tokens) - width + 1))


def _operation_matches(node: dict[str, Any], semantic_operation: str) -> tuple[dict[str, str], ...]:
    candidates = operation_candidates(node)
    if not candidates:
        return ({"resource": "", "resource_name": "", "operation": "", "operation_name": "", "description": ""},)
    # The existing Semantic Spine constrains this field to installed operation IDs.
    # Exact installed display labels remain compatibility identities; descriptions
    # and token similarity never choose an executable operation.
    return tuple(candidate for candidate in candidates if any(
        str(candidate.get(field) or "").casefold() == str(semantic_operation).casefold()
        for field in ("operation", "operation_name")
    ))


def _select_operation(node: dict[str, Any], semantic_operation: str) -> dict[str, str] | None:
    matches = _operation_matches(node, semantic_operation)
    return matches[0] if len(matches) == 1 else None


def _bind_arguments(contract: tuple[dict[str, Any], ...], arguments: dict[str, Any]) -> tuple[
    dict[str, Any], tuple[str, ...], tuple[str, ...], dict[str, tuple[str, ...]],
]:
    parameters: dict[str, Any] = {}
    by_semantic_name: dict[str, list[str]] = {}
    for prop in contract:
        name = str(prop.get("name") or "")
        for label in (name, prop.get("displayName")):
            key = "".join(_semantic_tokens(label))
            if key:
                by_semantic_name.setdefault(key, []).append(name)
        if "default" in prop and prop.get("default") not in (None, ""):
            parameters[name] = prop.get("default")
    unmapped = []
    ambiguity_candidates: dict[str, tuple[str, ...]] = {}
    for semantic_name, value in arguments.items():
        key = "".join(_semantic_tokens(semantic_name))
        names = tuple(dict.fromkeys(by_semantic_name.get(key, ())))
        if len(names) != 1:
            unmapped.append(str(semantic_name))
            ambiguity_candidates[str(semantic_name)] = names
            continue
        parameters[names[0]] = value
    def missing_value(value: Any) -> bool:
        if value in (None, ""):
            return True
        if isinstance(value, (list, tuple)):
            return not value or all(missing_value(item) for item in value)
        if isinstance(value, dict):
            substantive = [item for key, item in value.items() if str(key) not in {"mode"}]
            return not substantive or all(missing_value(item) for item in substantive)
        return False

    missing = tuple(
        str(prop.get("name")) for prop in contract
        if prop.get("required") and missing_value(parameters.get(str(prop.get("name"))))
    )
    return parameters, missing, tuple(unmapped), ambiguity_candidates


def bind_catalog_step(step: dict[str, Any], *, source_text: str | None = None) -> dict[str, Any]:
    """Bind a model-owned semantic requirement to exact installed provider truth."""
    provider_name = str(step.get("provider_name") or "").strip()
    claimed_provenance = str(step.get("provider_provenance") or "").strip()
    inference_justification = str(step.get("provider_inference_justification") or "").strip()
    provider_provenance = "NONE"
    if provider_name:
        source_explicit = _source_mentions_provider(source_text, provider_name)
        if claimed_provenance == "SOURCE_EXPLICIT" and not source_explicit:
            return {
                "disposition": "AMBIGUOUS", "reason": "explicit_provider_not_source_grounded",
                "catalog_query": str(step.get("catalog_query") or ""), "provider_name": provider_name,
                "provider_provenance": "INVALID_EXPLICIT_CLAIM", "provider_inference_justification": "",
                "node_type": None, "operation_candidates": (), "parameter_ambiguity_candidates": {},
            }
        if claimed_provenance == "SEMANTIC_INFERENCE":
            if not inference_justification:
                return {
                    "disposition": "AMBIGUOUS", "reason": "inferred_provider_missing_justification",
                    "catalog_query": str(step.get("catalog_query") or ""), "provider_name": provider_name,
                    "provider_provenance": "SEMANTIC_INFERENCE", "provider_inference_justification": "",
                    "node_type": None, "operation_candidates": (), "parameter_ambiguity_candidates": {},
                }
            provider_provenance = "SEMANTIC_INFERENCE"
        elif source_explicit:
            provider_provenance = "SOURCE_EXPLICIT"
        elif source_text is not None:
            return {
                "disposition": "AMBIGUOUS", "reason": "provider_provenance_untyped",
                "catalog_query": str(step.get("catalog_query") or ""), "provider_name": provider_name,
                "provider_provenance": "UNTYPED", "provider_inference_justification": "",
                "node_type": None, "operation_candidates": (), "parameter_ambiguity_candidates": {},
            }
        else:
            provider_provenance = "UNVERIFIED_BINDING_INPUT"
    n8n_type, node = resolve_logical_step(step)
    if n8n_type is None or node is None:
        disposition = "UNAVAILABLE" if provider_name and not node_contract(provider_name).get("found") else "AMBIGUOUS"
        return {"disposition": disposition, "catalog_query": str(step.get("catalog_query") or ""),
                "provider_name": provider_name, "provider_provenance": provider_provenance,
                "provider_inference_justification": inference_justification, "node_type": None, "resource": None,
                "operation": None, "parameters": {}, "parameter_contract": (),
                "operation_candidates": (), "parameter_ambiguity_candidates": {},
                "missing_required_parameters": (), "unmapped_semantic_arguments": (),
                "credential_requirements": (), "missing_credential_types": (),
                "source_catalog": "installed frozen n8n export:nodes (offline, authoritative)"}
    if not provider_name:
        resolved_provider_name = str(node.get("displayName") or node.get("name") or "").strip()
        if resolved_provider_name and _source_mentions_provider(source_text, resolved_provider_name):
            provider_name = resolved_provider_name
            provider_provenance = "SOURCE_EXPLICIT"
    semantic_operation = str(step.get("semantic_operation") or "")
    selected = _select_operation(node, semantic_operation)
    if selected is None:
        matches = _operation_matches(node, semantic_operation)
        return {
            "disposition": "AMBIGUOUS", "catalog_query": str(step.get("catalog_query") or ""),
            "provider_name": provider_name, "provider_provenance": provider_provenance,
            "provider_inference_justification": inference_justification,
            "node_type": n8n_type, "reason": "semantic_operation_not_decisive",
            "operation_candidates": tuple({
                "resource": item.get("resource", ""), "operation": item.get("operation", ""),
            } for item in matches), "parameter_ambiguity_candidates": {},
        }
    schema = parameter_contract(node, selected["resource"], selected["operation"])
    bound, missing, unmapped, parameter_ambiguity = _bind_arguments(schema, dict(step.get("arguments") or {}))
    if selected["resource"]:
        bound["resource"] = selected["resource"]
    if selected["operation"]:
        bound["operation"] = selected["operation"]
    credentials = credential_requirements(node, bound)
    missing_credentials = tuple(
        item["credential_type"] for item in credentials if item["required"] and not item["instance_available"]
    )
    disposition = "PRECONDITION_REQUIRED" if missing or missing_credentials else "BOUND"
    if unmapped:
        disposition = "AMBIGUOUS"
    return {
        "disposition": disposition, "catalog_query": str(step.get("catalog_query") or ""),
        "provider_name": provider_name, "provider_provenance": provider_provenance,
        "provider_inference_justification": inference_justification,
        "node_type": n8n_type, "node_display_name": str(node.get("displayName") or node.get("name") or ""),
        "resource": selected["resource"], "operation": selected["operation"],
        "parameters": bound, "parameter_contract": schema,
        "missing_required_parameters": missing, "unmapped_semantic_arguments": unmapped,
        "operation_candidates": (), "parameter_ambiguity_candidates": parameter_ambiguity,
        "credential_requirements": credentials, "missing_credential_types": missing_credentials,
        "source_catalog": "installed frozen n8n export:nodes (offline, authoritative)",
    }


def _step_parameters(n8n_type: str, step: dict[str, Any], binding: dict[str, Any] | None = None) -> dict[str, Any]:
    """Bind a resolved step to its installed node parameter schema (generic, not node-id
    guessing beyond the universal intrinsic primitives)."""
    if n8n_type == "n8n-nodes-base.set":
        field = str(step.get("field") or "value")
        return {"assignments": {"assignments": [
            {"id": field, "name": field, "value": str(step.get("value") or ""), "type": "string"},
        ]}}
    if n8n_type == "n8n-nodes-base.code":
        return {"jsCode": str(step.get("code") or "return [{ json: {} }];")}
    if str(step.get("action") or "") == "jarvis_capability":
        return {
            "method": "POST", "url": JARVIS_CANONICAL_HOT_ENDPOINT,
            "sendBody": True, "contentType": "raw", "rawContentType": "application/json",
            "body": json.dumps({
                "text": str(step.get("request") or ""),
                "expected_capability_id": str(step.get("capability_id") or ""),
            }, ensure_ascii=False),
            "options": {"timeout": 120000},
        }
    if n8n_type == "n8n-nodes-base.if":
        field = str(step.get("field") or "value")
        value = step.get("value")
        operator = _CONDITION_OPERATORS.get(str(step.get("operator") or "equals"), _CONDITION_OPERATORS["equals"])
        return {
            "conditions": {
                "options": {"caseSensitive": True, "leftValue": "", "typeValidation": "strict", "version": 2},
                "conditions": [{
                    "leftValue": "={{ $json." + field + " }}",
                    "rightValue": str(value) if value is not None else "",
                    "operator": operator,
                }],
                "combinator": "and",
            },
            "options": {},
        }
    if binding is not None:
        return dict(binding.get("parameters") or {})
    return {}


def _check_local_only(constraints: set[str], n8n_type: str, contract: dict[str, Any]) -> None:
    """Transport/scope truth for local_only: NONE allowed; NETWORK+LOCALHOST/LAN allowed
    (LAN != Internet); NETWORK+EXTERNAL_SERVICE rejected; UNKNOWN fails closed."""
    if "local_only" not in constraints:
        return
    tr = transport_requirement(contract)
    if tr == "NETWORK_TRANSPORT" and network_scope(contract) == "EXTERNAL_SERVICE":
        raise LogicalSpecCompileError(f"external_service_violates_local_only:{n8n_type}")
    if tr == "UNKNOWN":
        raise LogicalSpecCompileError(f"unknown_transport_violates_local_only:{n8n_type}")


def _type_version(node_type: str, contract: dict[str, Any]) -> int | float:
    preferred = contract.get("defaultVersion") or contract.get("version") or 1
    if isinstance(preferred, list):
        numeric = [value for value in preferred if isinstance(value, (int, float))]
        return max(numeric) if numeric else 1
    return preferred if isinstance(preferred, (int, float)) else 1


def _connect(connections: dict[str, Any], source: str, source_output: int,
             target: str, target_input: int = 0) -> None:
    outputs = connections.setdefault(source, {}).setdefault("main", [])
    while len(outputs) <= source_output:
        outputs.append([])
    outputs[source_output].append({"node": target, "type": "main", "index": target_input})


def _new_node(nodes: list[dict[str, Any]], counter: list[int], node_type: str,
              contract: dict[str, Any], parameters: dict[str, Any], *, label: str = "Step") -> str:
    counter[0] += 1
    name = f"{label}{counter[0]}"
    nodes.append({
        "parameters": parameters, "type": node_type, "typeVersion": _type_version(node_type, contract),
        "position": [220 * counter[0], 0], "name": name,
    })
    return name


def _switch_parameters(step: dict[str, Any]) -> dict[str, Any]:
    field = str(step.get("field") or "value")
    values = []
    branches = tuple(branch for branch in step.get("branches") or () if not branch.get("default"))
    for branch in branches:
        value = branch.get("value")
        values.append({
            "conditions": {
                "options": {"caseSensitive": True, "leftValue": "", "typeValidation": "strict", "version": 3},
                "conditions": [{
                    "leftValue": "={{ $json." + field + " }}", "rightValue": str(value),
                    "operator": {"type": "string", "operation": "equals"},
                }],
                "combinator": "and",
            },
            "renameOutput": True, "outputKey": str(branch.get("label") or value),
        })
    has_default = bool(step.get("default_steps")) or any(branch.get("default") for branch in step.get("branches") or ())
    options = {"fallbackOutput": "extra", "renameFallbackOutput": "default"} if has_default else {}
    return {"mode": "rules", "rules": {"values": values}, "options": options}


def _validate_jarvis_capability_step(
    step: dict[str, Any], allowed_jarvis_capability_ids: frozenset[str],
) -> None:
    capability_id = str(step.get("capability_id") or "").strip()
    if not capability_id or capability_id not in allowed_jarvis_capability_ids:
        raise LogicalSpecCompileError(f"jarvis_capability_not_selected:{capability_id or 'missing'}")
    if capability_id in {"workflow_automation:n8n", "conversation.respond"}:
        raise LogicalSpecCompileError(f"jarvis_capability_recursive_or_non_executable:{capability_id}")


def _validate_flat_steps(
    steps: list[dict[str, Any]], allowed_jarvis_capability_ids: frozenset[str],
) -> dict[str, dict[str, Any]]:
    by_id: dict[str, dict[str, Any]] = {}
    for step in steps:
        step_id = str(step.get("step_id") or "")
        if not step_id or step_id in by_id:
            raise LogicalSpecCompileError("flat_topology_requires_unique_step_ids")
        by_id[step_id] = step
        action = str(step.get("action") or "")
        required = {
            "set_field": ("field", "value"), "transform": ("code",), "http_request": ("url",),
            "catalog_query": ("catalog_query", "semantic_operation"),
            "jarvis_capability": ("capability_id", "request"),
            "condition": ("field", "operator", "true_step_id", "false_step_id"),
            "route": ("field", "branches"), "merge": (),
        }.get(action)
        if required is None or any(step.get(key) in (None, "", [], ()) for key in required):
            raise LogicalSpecCompileError(f"invalid_logical_step_contract:{step_id}:{action}")
        if action == "jarvis_capability":
            _validate_jarvis_capability_step(step, allowed_jarvis_capability_ids)
    adjacency: dict[str, set[str]] = {step_id: set() for step_id in by_id}
    for step_id, step in by_id.items():
        for target in step.get("next_step_ids") or ():
            target = str(target)
            if target not in by_id or target == step_id:
                raise LogicalSpecCompileError(f"invalid_topology_successor:{step_id}:{target}")
            adjacency[step_id].add(target)
        targets = []
        if step.get("action") == "condition":
            targets = [step.get("true_step_id"), step.get("false_step_id")]
        elif step.get("action") == "route":
            targets = [branch.get("target_step_id") for branch in step.get("branches") or ()]
        for target in targets:
            target = str(target or "")
            if target not in by_id or target == step_id:
                raise LogicalSpecCompileError(f"invalid_topology_branch:{step_id}:{target}")
            adjacency[step_id].add(target)
    visiting: set[str] = set()
    visited: set[str] = set()
    def visit(step_id: str) -> None:
        if step_id in visiting:
            raise LogicalSpecCompileError("logical_topology_cycle")
        if step_id in visited:
            return
        visiting.add(step_id)
        for target in adjacency[step_id]:
            visit(target)
        visiting.remove(step_id)
        visited.add(step_id)
    for step_id in by_id:
        visit(step_id)
    return by_id


def _compile_flat_steps(steps: list[dict[str, Any]], nodes: list[dict[str, Any]], connections: dict[str, Any],
                        constraints: set[str], counter: list[int], binding_report: list[dict[str, Any]],
                        source_text: str | None = None,
                        allowed_jarvis_capability_ids: frozenset[str] = frozenset()) -> None:
    by_id = _validate_flat_steps(steps, allowed_jarvis_capability_ids)
    names: dict[str, str] = {}
    contracts: dict[str, dict[str, Any]] = {}
    branch_targets = {
        str(target) for step in steps for target in (
            ([step.get("true_step_id"), step.get("false_step_id")] if step.get("action") == "condition" else
             [branch.get("target_step_id") for branch in step.get("branches") or ()] if step.get("action") == "route" else [])
        ) if target
    }
    for step in steps:
        action = str(step["action"])
        binding = None
        if action == "route":
            n8n_type, contract = "n8n-nodes-base.switch", _installed("n8n-nodes-base.switch")
            parameters = _switch_parameters(step)
        elif action == "merge":
            n8n_type, contract = "n8n-nodes-base.merge", _installed("n8n-nodes-base.merge")
            mode = "combine" if step.get("merge_mode") == "combine_by_position" else "append"
            parameters = {"mode": mode, "numberInputs": 2}
            if mode == "combine":
                parameters["combineBy"] = "combineByPosition"
        else:
            if action == "catalog_query":
                binding = bind_catalog_step(step, source_text=source_text)
                if binding["disposition"] == "UNAVAILABLE":
                    raise LogicalSpecCompileError(
                        "unavailable_catalog_binding:" + str(binding.get("provider_name") or "unknown")
                    )
                if binding["disposition"] == "AMBIGUOUS":
                    raise LogicalSpecCompileError("ambiguous_catalog_binding")
                n8n_type = str(binding.get("node_type") or "")
                contract = _installed(n8n_type) if n8n_type else None
                if contract is not None:
                    _check_local_only(constraints, n8n_type, contract)
                if binding.get("missing_required_parameters"):
                    raise LogicalSpecCompileError(
                        "precondition_required:missing_parameters:" + ",".join(binding["missing_required_parameters"])
                    )
                binding_report.append(binding)
            elif action == "jarvis_capability":
                n8n_type, contract = resolve_logical_step(step)
                binding_report.append({
                    "disposition": "BOUND", "provider_name": "JARVIS canonical semantic spine",
                    "provider_provenance": "INSTALLED_PROVIDER_CONTRACT",
                    "node_type": "n8n-nodes-base.httpRequest", "operation": "semantic_turn",
                    "parameters": {"capability_id": str(step.get("capability_id") or ""),
                                   "request": str(step.get("request") or "")},
                    "endpoint": JARVIS_CANONICAL_HOT_ENDPOINT,
                    "source_catalog": "CONTROL_PLANE canonical /jarvis-live/hot contract",
                })
            else:
                n8n_type, contract = resolve_logical_step(step)
            if n8n_type is None or contract is None:
                raise LogicalSpecCompileError(f"unresolved_logical_step:{action}")
            _check_local_only(constraints, n8n_type, contract)
            parameters = _step_parameters(n8n_type, step, binding)
        if contract is None:
            raise LogicalSpecCompileError(f"node_not_installed:{action}")
        names[str(step["step_id"])] = _new_node(nodes, counter, n8n_type, contract, parameters)
        contracts[str(step["step_id"])] = contract

    incoming: dict[str, list[str]] = {step_id: [] for step_id in by_id}
    outgoing: dict[str, list[str]] = {step_id: [] for step_id in by_id}
    for step in steps:
        step_id = str(step["step_id"])
        if step.get("action") not in {"condition", "route"}:
            for target in step.get("next_step_ids") or ():
                target = str(target)
                outgoing[step_id].append(target)
                incoming[target].append(step_id)
    for index, step in enumerate(steps):
        step_id = str(step["step_id"])
        action = str(step["action"])
        parents = list(incoming[step_id])
        if not parents and step_id not in branch_targets:
            if index == 0:
                _connect(connections, "Trigger", 0, names[step_id])
            elif ("next_step_ids" not in step and not outgoing[str(steps[index - 1]["step_id"])]
                  and steps[index - 1].get("action") not in {"condition", "route"}):
                parents = [str(steps[index - 1]["step_id"])]
                incoming[step_id].append(parents[0])
                outgoing[parents[0]].append(step_id)
        if action == "merge":
            if len(parents) < 2:
                raise LogicalSpecCompileError(f"merge_requires_multiple_inputs:{step_id}")
            node = next(value for value in nodes if value["name"] == names[step_id])
            node["parameters"]["numberInputs"] = len(parents)
        for input_index, parent in enumerate(parents):
            _connect(connections, names[parent], 0, names[step_id], input_index if action == "merge" else 0)
        if action == "condition":
            _connect(connections, names[step_id], 0, names[str(step["true_step_id"])])
            _connect(connections, names[step_id], 1, names[str(step["false_step_id"])])
        elif action == "route":
            output_index = 0
            regular_count = sum(1 for branch in step.get("branches") or () if not branch.get("default"))
            for branch in step.get("branches") or ():
                output = regular_count if branch.get("default") else output_index
                _connect(connections, names[step_id], output, names[str(branch["target_step_id"])])
                if not branch.get("default"):
                    output_index += 1


def _compile_steps(steps: list[dict[str, Any]], nodes: list[dict[str, Any]], connections: dict[str, Any],
                   constraints: set[str], parents: list[tuple[str, int]], counter: list[int],
                   binding_report: list[dict[str, Any]], source_text: str | None = None,
                   allowed_jarvis_capability_ids: frozenset[str] = frozenset(),
                   ) -> tuple[str, list[tuple[str, int]]]:
    """Compile a provider-neutral chain; control steps return all terminal graph ports."""
    entry = ""
    current = list(parents)
    for step in steps:
        action = str(step.get("intent") or step.get("action") or "")
        if action == "parallel":
            branches = tuple(step.get("branches") or ())
            if not branches:
                raise LogicalSpecCompileError("parallel_requires_branches")
            branch_tails: list[list[tuple[str, int]]] = []
            for branch in branches:
                branch_steps = [value for value in branch.get("steps", ()) if isinstance(value, dict)]
                if not branch_steps:
                    raise LogicalSpecCompileError("parallel_branch_requires_steps")
                branch_entry, tails = _compile_steps(
                    branch_steps, nodes, connections, constraints, list(current), counter, binding_report, source_text,
                    allowed_jarvis_capability_ids,
                )
                entry = entry or branch_entry
                branch_tails.append(tails)
            if step.get("merge"):
                merge_contract = _installed("n8n-nodes-base.merge")
                if merge_contract is None:
                    raise LogicalSpecCompileError("node_not_installed:merge")
                merge_name = _new_node(
                    nodes, counter, "n8n-nodes-base.merge", merge_contract,
                    {"mode": "append", "numberInputs": len(branches)}, label="Merge",
                )
                for input_index, tails in enumerate(branch_tails):
                    for source, output in tails:
                        _connect(connections, source, output, merge_name, input_index)
                current = [(merge_name, 0)]
            else:
                current = [tail for tails in branch_tails for tail in tails]
            continue

        if action == "route":
            branches = tuple(step.get("branches") or ())
            if not branches:
                raise LogicalSpecCompileError("route_requires_branches")
            switch_contract = _installed("n8n-nodes-base.switch")
            if switch_contract is None:
                raise LogicalSpecCompileError("node_not_installed:switch")
            name = _new_node(nodes, counter, "n8n-nodes-base.switch", switch_contract, _switch_parameters(step), label="Route")
            for source, output in current:
                _connect(connections, source, output, name)
            entry = entry or name
            tails: list[tuple[str, int]] = []
            for output_index, branch in enumerate(branches):
                branch_steps = [value for value in branch.get("steps", ()) if isinstance(value, dict)]
                _, branch_tail = _compile_steps(
                    branch_steps, nodes, connections, constraints, [(name, output_index)], counter, binding_report, source_text,
                    allowed_jarvis_capability_ids,
                )
                tails.extend(branch_tail)
            default_steps = [value for value in step.get("default_steps", ()) if isinstance(value, dict)]
            if default_steps:
                _, default_tail = _compile_steps(
                    default_steps, nodes, connections, constraints, [(name, len(branches))], counter, binding_report, source_text,
                    allowed_jarvis_capability_ids,
                )
                tails.extend(default_tail)
            current = tails
            continue

        binding: dict[str, Any] | None = None
        if step.get("catalog_query"):
            binding = bind_catalog_step(step, source_text=source_text)
            if binding["disposition"] == "UNAVAILABLE":
                raise LogicalSpecCompileError(
                    "unavailable_catalog_binding:" + str(binding.get("provider_name") or "unknown")
                )
            if binding["disposition"] == "AMBIGUOUS":
                raise LogicalSpecCompileError("ambiguous_catalog_binding")
            n8n_type = str(binding.get("node_type") or "")
            contract = _installed(n8n_type) if n8n_type else None
            if contract is not None:
                _check_local_only(constraints, n8n_type, contract)
            if binding.get("missing_required_parameters"):
                raise LogicalSpecCompileError(
                    "precondition_required:missing_parameters:" + ",".join(binding["missing_required_parameters"])
                )
            binding_report.append(binding)
        elif action == "jarvis_capability":
            n8n_type, contract = resolve_logical_step(step)
            _validate_jarvis_capability_step(step, allowed_jarvis_capability_ids)
            binding_report.append({
                "disposition": "BOUND", "provider_name": "JARVIS canonical semantic spine",
                "provider_provenance": "INSTALLED_PROVIDER_CONTRACT",
                "node_type": "n8n-nodes-base.httpRequest", "operation": "semantic_turn",
                "parameters": {"capability_id": str(step.get("capability_id") or ""),
                               "request": str(step.get("request") or "")},
                "endpoint": JARVIS_CANONICAL_HOT_ENDPOINT,
                "source_catalog": "CONTROL_PLANE canonical /jarvis-live/hot contract",
            })
        else:
            n8n_type, contract = resolve_logical_step(step)
        if n8n_type is None or contract is None:
            raise LogicalSpecCompileError(f"unresolved_logical_step:{action or 'catalog_query'}")
        _check_local_only(constraints, n8n_type, contract)
        name = _new_node(nodes, counter, n8n_type, contract, _step_parameters(n8n_type, step, binding))
        for source, output in current:
            _connect(connections, source, output, name)
        entry = entry or name
        if n8n_type == "n8n-nodes-base.if":
            true_steps = [value for value in step.get("true_steps", ()) if isinstance(value, dict)]
            false_steps = [value for value in step.get("false_steps", ()) if isinstance(value, dict)]
            if not true_steps or not false_steps:
                raise LogicalSpecCompileError("condition_requires_true_and_false_steps")
            _, true_tails = _compile_steps(
                true_steps, nodes, connections, constraints, [(name, 0)], counter, binding_report, source_text,
                allowed_jarvis_capability_ids,
            )
            _, false_tails = _compile_steps(
                false_steps, nodes, connections, constraints, [(name, 1)], counter, binding_report, source_text,
                allowed_jarvis_capability_ids,
            )
            current = true_tails + false_tails
        else:
            current = [(name, 0)]
    return entry, current


def compile_logical_automation_spec(
    spec: dict[str, Any], *, source_text: str | None = None,
    allowed_jarvis_capability_ids: frozenset[str] = frozenset(),
) -> dict[str, Any]:
    """Compile a logical spec to a validated n8n graph. Fails closed on any gap."""
    trigger_raw = spec.get("trigger")
    steps = spec.get("steps")
    constraints = set(str(c) for c in (spec.get("constraints") or []))
    if not isinstance(steps, list) or not steps:
        raise LogicalSpecCompileError("logical_spec_missing_steps")
    if spec.get("semantic_requirements") or "_canonical_requirement_ids" in spec:
        by_id = {
            str(step.get("step_id") or ""): step for step in steps
            if isinstance(step, dict) and step.get("step_id")
        }
        semantic_requirements = tuple(spec.get("semantic_requirements") or ())
        covered_ids = tuple(
            str(item.get("requirement_id") or "") for item in semantic_requirements
            if isinstance(item, dict)
        )
        if "_canonical_requirement_ids" in spec:
            required_ids = tuple(str(item) for item in spec.get("_canonical_requirement_ids") or ())
            if set(required_ids) != set(covered_ids):
                raise LogicalSpecCompileError("canonical_semantic_requirement_coverage_mismatch")
        if len(covered_ids) != len(set(covered_ids)):
            raise LogicalSpecCompileError("duplicate_semantic_requirement_coverage")
        covered_step_ids = {
            str(item.get("step_id") or "") for item in semantic_requirements
            if isinstance(item, dict)
        }
        if any(
            str(step.get("action") or "") in {"catalog_query", "jarvis_capability", "http_request"}
            and str(step.get("step_id") or "") not in covered_step_ids
            for step in steps if isinstance(step, dict)
        ):
            raise LogicalSpecCompileError("unreferenced_real_operation_step")
        for requirement in semantic_requirements:
            if not isinstance(requirement, dict):
                raise LogicalSpecCompileError("invalid_semantic_requirement")
            grounding = str(requirement.get("source_grounding") or "").strip()
            if source_text is not None and (not grounding or grounding.casefold() not in source_text.casefold()):
                raise LogicalSpecCompileError("semantic_requirement_not_source_grounded")
            step = by_id.get(str(requirement.get("step_id") or ""))
            if step is None:
                raise LogicalSpecCompileError("semantic_requirement_step_missing")
            operation_class = str(requirement.get("operation_class") or "")
            action = str(step.get("action") or "")
            if operation_class == "ASSIGN" and action != "set_field":
                raise LogicalSpecCompileError("assignment_requirement_wrong_operation")
            if operation_class == "TRANSFORM" and action != "transform":
                raise LogicalSpecCompileError("transform_requirement_wrong_operation")
            if operation_class not in {"ASSIGN", "TRANSFORM"}:
                if action == "set_field":
                    raise LogicalSpecCompileError("real_operation_misrepresented_as_set_field")
                if action not in {"catalog_query", "jarvis_capability", "http_request"}:
                    raise LogicalSpecCompileError("real_operation_not_operational_step")
            if action == "catalog_query" and str(
                step.get("semantic_operation") or ""
            ).strip().casefold() == operation_class.casefold():
                raise LogicalSpecCompileError("catalog_operation_repeats_semantic_class")
            provider_name = str(requirement.get("provider_name") or "").strip()
            if provider_name:
                step_provider = str(step.get("provider_name") or "").strip()
                if not _source_mentions_provider(step_provider, provider_name):
                    raise LogicalSpecCompileError("provider_constraint_not_covered")
                if str(step.get("provider_provenance") or "") != str(
                    requirement.get("provider_provenance") or ""
                ):
                    raise LogicalSpecCompileError("provider_provenance_mismatch")
                if str(requirement.get("provider_provenance") or "") == "SOURCE_EXPLICIT" \
                        and str(step.get("provider_inference_justification") or "").strip():
                    raise LogicalSpecCompileError("explicit_provider_has_inference")
    if source_text is not None:
        def validate_http_sources(items: list[dict[str, Any]]) -> None:
            for item in items:
                if str(item.get("action") or item.get("intent") or "") == "http_request":
                    url = str(item.get("url") or "").strip()
                    if not url or url not in source_text:
                        raise LogicalSpecCompileError("http_request_endpoint_not_source_grounded")
                for child_key in ("true_steps", "false_steps", "default_steps"):
                    children = item.get(child_key)
                    if isinstance(children, list):
                        validate_http_sources(children)
                for branch in item.get("branches") or ():
                    children = branch.get("steps") if isinstance(branch, dict) else None
                    if isinstance(children, list):
                        validate_http_sources(children)
        validate_http_sources(steps)

    nodes: list[dict[str, Any]] = []
    connections: dict[str, Any] = {}

    # Trigger: a small enum ("manual" / "schedule" / "webhook") OR a {catalog_query} object.
    if isinstance(trigger_raw, dict):
        trigger_step = {
            "catalog_query": str(trigger_raw.get("catalog_query") or trigger_raw.get("intent") or ""),
            "provider_name": str(trigger_raw.get("provider_name") or ""),
        }
    elif trigger_raw == "manual":
        trigger_step = {"intent": "manual_trigger"}
    elif trigger_raw == "schedule":
        trigger_step = {"intent": "schedule_trigger"}
    elif trigger_raw == "webhook":
        trigger_step = {"intent": "webhook_trigger"}
    else:
        trigger_step = {"catalog_query": str(trigger_raw or "")}
    ttype, contract = resolve_logical_step(trigger_step)
    if ttype is None or contract is None:
        raise LogicalSpecCompileError("node_not_installed:trigger")
    trigger_groups = {str(item).casefold() for item in contract.get("group") or ()}
    if "trigger" not in trigger_groups and not str(ttype).casefold().endswith("trigger"):
        raise LogicalSpecCompileError("resolved_node_is_not_trigger")
    nodes.append({"parameters": {}, "type": ttype, "typeVersion": 1, "position": [0, 0], "name": "Trigger"})

    binding_report: list[dict[str, Any]] = []
    if all(isinstance(step, dict) and step.get("step_id") for step in steps):
        _compile_flat_steps(
            steps, nodes, connections, constraints, [0], binding_report, source_text,
            allowed_jarvis_capability_ids,
        )
    else:
        _compile_steps(
            steps, nodes, connections, constraints, [("Trigger", 0)], [0], binding_report, source_text,
            allowed_jarvis_capability_ids,
        )

    return {
        "name": str(spec.get("name") or "jarvis_local_automation"),
        "nodes": nodes,
        "connections": connections,
        "settings": {"executionOrder": "v1"},
        "_jarvis_binding_report": binding_report,
    }


__all__ = [
    "LogicalSpecCompileError", "bind_catalog_step", "compile_logical_automation_spec", "resolve_logical_step",
]
