from __future__ import annotations

import json

import pytest

from MAKSIMAR_CORE_LIB.ai_orchestration.semantic_intent_contract import (
    CapabilityRequirement,
    EvidenceBundle,
    ExecutionPlan,
    ExecutionReceipt,
    Goal,
    PlanStep,
    RequestUnderstanding,
)
from MAKSIMAR_SERVER.AI_ORCHESTRATION import n8n_adapter


def _acceptance_workflow(value: str) -> dict:
    """Test/acceptance fixture (NOT production): deterministic local workflow."""
    return {
        "name": "jarvis_local_automation",
        "nodes": [
            {"parameters": {}, "type": "n8n-nodes-base.manualTrigger", "typeVersion": 1,
             "position": [0, 0], "name": "Manual"},
            {"parameters": {"assignments": {"assignments": [
                {"id": "value", "name": "value", "value": value, "type": "string"},
            ]}}, "type": "n8n-nodes-base.set", "typeVersion": 3.4,
             "position": [220, 0], "name": "Set Value"},
        ],
        "connections": {"Manual": {"main": [[{"node": "Set Value", "type": "main", "index": 0}]]}},
        "settings": {"executionOrder": "v1"},
    }


def _understanding() -> RequestUnderstanding:
    return RequestUnderstanding(
        request_id="n8n_test", original_text="create a local automation", language="en",
        goals=(Goal("g1", "create automation"),),
        required_capabilities=(CapabilityRequirement("workflow_automation:n8n", "create", True),),
        effect_type="MUTATE", target_scope="local_workflow_automation", reversibility="REVERSIBLE",
        external_side_effect=False, unresolved_capabilities=(), operation_requirements=(),
        current_topic="automation", unresolved_reference="", relevant_context_trace_ids=(),
        risk_class="MUTATION", confidence=1.0, reason_codes=("typed_test",),
    )


def _step(op: str, params: tuple[tuple[str, str], ...] = ()) -> PlanStep:
    return PlanStep(
        step_id=f"s_{op}", goal_id="g1", capability_id="workflow_automation:n8n",
        operation=op, required_evidence=("n8n_workflow",), effect_type="MUTATE",
        target_scope="local_workflow_automation", reversibility="REVERSIBLE",
        external_side_effect=False, risk_class="MUTATION", parameters=params,
    )


def _create_step(value: str = "M") -> PlanStep:
    spec = json.dumps(_acceptance_workflow(value))
    return _step("create_workflow", (("workflow", spec),))


def test_n8n_create_without_spec_fails_closed():
    adapter = n8n_adapter.ExistingN8nAdapter()
    bundle = adapter.collect_evidence(
        _understanding(),
        ExecutionPlan(request_id="n8n_test", steps=(_step("create_workflow", (("workflow_name", "x"),)),)),
        "t_no_spec",
    )
    assert bundle.status != "COMPLETE"
    assert any("missing_workflow_spec" in e for e in bundle.errors)


def test_n8n_unavailable_never_reports_complete(monkeypatch):
    monkeypatch.setattr(n8n_adapter, "_n8n_request", lambda *a, **k: {"error": "http_503"})
    monkeypatch.setattr(n8n_adapter, "_run_cli_execute", lambda *a, **k: {"error": "TimeoutError"})
    adapter = n8n_adapter.ExistingN8nAdapter()
    bundle = adapter.collect_evidence(
        _understanding(), ExecutionPlan(request_id="n8n_test", steps=(_create_step(),)), "t_unavailable",
    )
    assert bundle.status != "COMPLETE"
    assert bundle.errors


def test_n8n_create_failure_fails_closed(monkeypatch):
    monkeypatch.setattr(n8n_adapter, "_n8n_request", lambda *a, **k: {"error": "http_400", "detail": "bad"})
    adapter = n8n_adapter.ExistingN8nAdapter()
    bundle = adapter.collect_evidence(
        _understanding(), ExecutionPlan(request_id="n8n_test", steps=(_create_step(),)), "t_create_fail",
    )
    assert bundle.status == "UNAVAILABLE"
    assert any("create_workflow" in e for e in bundle.errors)
    assert not any(r.status == "COMPLETE" for r in bundle.receipts)


def test_n8n_execute_non_success_is_not_complete(monkeypatch):
    monkeypatch.setattr(n8n_adapter, "_n8n_request", lambda *a, **k: {"id": "wf_test", "name": "x"})
    monkeypatch.setattr(n8n_adapter, "_run_cli_execute", lambda *a, **k: {"returncode": 1, "output": "crashed"})
    adapter = n8n_adapter.ExistingN8nAdapter()
    bundle = adapter.collect_evidence(
        _understanding(),
        ExecutionPlan(request_id="n8n_test", steps=(_step("execute_workflow", (("workflow_id", "wf_test"),)),)),
        "t_execute_fail",
    )
    assert bundle.status != "COMPLETE"
    assert not any(r.status == "COMPLETE" for r in bundle.receipts)


def test_n8n_operation_contracts_expose_automation_owner():
    contracts = n8n_adapter.N8N_CAPABILITY_OPERATION_CONTRACTS["workflow_automation:n8n"]
    by_op = {c["operation_id"]: c for c in contracts}
    assert by_op["create_workflow"]["semantic_owner_id"] == "automation.create"
    assert by_op["inspect_workflow"]["semantic_owner_id"] == "automation.inspect"
    assert by_op["execute_workflow"]["semantic_owner_id"] == "automation.run"
    assert by_op["modify_workflow"]["semantic_owner_id"] == "automation.modify"
    assert all(c["target_scope"] == "local_workflow_automation" for c in contracts)


def test_local_workflow_uses_only_local_installed_nodes():
    wf = _acceptance_workflow("M")
    types = {n["type"] for n in wf["nodes"]}
    assert types == {"n8n-nodes-base.manualTrigger", "n8n-nodes-base.set"}
    assert "connections" in wf and "settings" in wf


def test_logical_spec_compiles_to_installed_nodes():
    from MAKSIMAR_SERVER.AI_ORCHESTRATION.n8n_logical_compiler import (
        LogicalSpecCompileError,
        compile_logical_automation_spec,
    )
    spec = {"trigger": "manual", "steps": [{"action": "set_field", "field": "value", "value": "alpha"}], "constraints": ["local_only"]}
    graph = compile_logical_automation_spec(spec)
    assert [n["type"] for n in graph["nodes"]] == ["n8n-nodes-base.manualTrigger", "n8n-nodes-base.set"]
    assert graph["nodes"][1]["parameters"]["assignments"]["assignments"][0]["value"] == "alpha"


def test_logical_spec_unknown_action_fails_closed():
    from MAKSIMAR_SERVER.AI_ORCHESTRATION.n8n_logical_compiler import (
        LogicalSpecCompileError,
        compile_logical_automation_spec,
    )
    with pytest.raises(LogicalSpecCompileError):
        compile_logical_automation_spec({"trigger": "manual", "steps": [{"action": "nonexistent"}]})


def test_logical_spec_external_service_violates_local_only():
    from MAKSIMAR_SERVER.AI_ORCHESTRATION.n8n_logical_compiler import (
        LogicalSpecCompileError,
        compile_logical_automation_spec,
    )
    with pytest.raises(LogicalSpecCompileError, match="local_only"):
        compile_logical_automation_spec(
            {"trigger": "manual", "steps": [{
                "provider_name": "Telegram", "catalog_query": "Telegram messaging integration", "semantic_operation": "sendMessage",
            }], "constraints": ["local_only"]}
        )


def test_network_truth_ftp_is_not_local():
    from MAKSIMAR_SERVER.AI_ORCHESTRATION import n8n_local_catalog as cat

    assert "ftp" not in cat._LOCAL_INTRINSIC_NAMES
    assert "ftp" in cat._NETWORK_TRANSPORT_NAMES


def test_transport_and_scope_are_orthogonal():
    from MAKSIMAR_SERVER.AI_ORCHESTRATION.n8n_local_catalog import (
        network_scope,
        node_contract,
        transport_requirement,
    )

    assert transport_requirement(node_contract("n8n-nodes-base.set")["node"]) == "NONE"
    # postgres requires a network transport but may be localhost/LAN (not necessarily Internet)
    assert transport_requirement(node_contract("n8n-nodes-base.postgres")["node"]) == "NETWORK_TRANSPORT"
    assert network_scope(node_contract("n8n-nodes-base.postgres")["node"]) == "LOCALHOST_OR_LAN_CAPABLE"
    # telegram is an external internet service
    assert network_scope(node_contract("n8n-nodes-base.telegram")["node"]) == "EXTERNAL_SERVICE"


def test_generic_resolver_fails_closed_on_ambiguous_or_weak():
    from MAKSIMAR_SERVER.AI_ORCHESTRATION.n8n_logical_compiler import resolve_logical_step

    assert resolve_logical_step({"intent": "nonexistent"}) == (None, None)
    # database_query is too generic -> unresolved (not a random top-1)
    assert resolve_logical_step({"intent": "database_query"})[0] is None


def test_runtime_role_classifies_internal_nodes():
    from MAKSIMAR_SERVER.AI_ORCHESTRATION.n8n_local_catalog import node_contract, runtime_role

    assert runtime_role(node_contract("n8n-nodes-base.stickyNote")["node"]) == "INTERNAL_ONLY"
    assert runtime_role(node_contract("n8n-nodes-base.oneSimpleApi")["node"]) == "USER_USABLE"  # genuine integration node
    assert runtime_role(node_contract("n8n-nodes-base.set")["node"]) == "USER_USABLE"


def test_catalog_never_advertises_parameter_names_as_nodes():
    from MAKSIMAR_SERVER.AI_ORCHESTRATION.n8n_local_catalog import node_contract

    # Regression: 'extractionValues' is an INodeProperties parameter of the Html node,
    # not a node type. The catalog must not advertise it as an executable node (this used
    # to happen when the generator picked the first `name:` in the file).
    assert node_contract("n8n-nodes-base.extractionValues")["found"] is False
    # The real Html node must be reachable instead.
    assert node_contract("n8n-nodes-base.html")["found"] is True


def test_catalog_runtime_registerability_consistency():
    """Every catalog node type must resolve through the same catalog contract layer."""
    from MAKSIMAR_SERVER.AI_ORCHESTRATION import n8n_local_catalog as cat

    catalog = cat._load()
    unresolved = [n["name"] for n in catalog["nodes"] if cat.node_contract(n["name"])["found"] is False]
    assert unresolved == []


def test_execution_restriction_requires_source_grounding():
    from MAKSIMAR_CORE_LIB.ai_orchestration.semantic_intent_contract import RequestUnderstanding
    import pytest as _pytest

    base = dict(
        request_id="r", original_text="измени value на gamma, но не запускай", language="ru",
        goals=(Goal("g1", "modify"),),
        required_capabilities=(CapabilityRequirement("workflow_automation:n8n", "modify", True),),
        effect_type="MUTATE", target_scope="local_workflow_automation", reversibility="REVERSIBLE",
        external_side_effect=False, unresolved_capabilities=(), operation_requirements=(),
        current_topic="automation", unresolved_reference="", relevant_context_trace_ids=(),
        risk_class="MUTATION", confidence=1.0, reason_codes=("typed_test",),
    )
    # Non-NONE without source grounding must fail closed.
    with _pytest.raises(ValueError):
        RequestUnderstanding(**base, execution_restriction="NO_EXECUTE", execution_restriction_source="")
    # With source grounding it is valid.
    u = RequestUnderstanding(**base, execution_restriction="NO_EXECUTE", execution_restriction_source="но не запускай")
    assert u.execution_restriction == "NO_EXECUTE"
    assert u.execution_restriction_source == "но не запускай"


def test_execution_restriction_drops_execute_but_keeps_modify():
    from CONTROL_PLANE.canonical_semantic_spine import _apply_execution_restriction

    modify = _step("modify_workflow", (("value", "gamma"),))
    execute = PlanStep(
        step_id="s_exec", goal_id="g1", capability_id="workflow_automation:n8n",
        operation="execute_workflow", required_evidence=("n8n_execution",), effect_type="EXECUTE",
        target_scope="local_workflow_automation", reversibility="REVERSIBLE",
        external_side_effect=False, risk_class="MUTATION",
    )
    steps = (modify, execute)
    filtered = _apply_execution_restriction(steps, "NO_EXECUTE")
    assert [s.operation for s in filtered] == ["modify_workflow"]
    # NONE leaves every step untouched.
    assert _apply_execution_restriction(steps, "NONE") == steps


def test_no_effect_without_receipt():
    from CONTROL_PLANE.canonical_semantic_spine import _unproven_effects

    modify = _step("modify_workflow", (("value", "gamma"),))
    plan = ExecutionPlan(request_id="n8n_test", steps=(modify,))
    # No COMPLETE receipt -> the modify effect is unproven and must not be reported complete.
    no_receipt = EvidenceBundle(
        request_id="n8n_test", capability_id="workflow_automation:n8n", trace_id="t",
        status="COMPLETE", items=(), limitations=(), receipts=(), errors=(),
    )
    assert _unproven_effects(plan, no_receipt) == ("modify_workflow",)
    # A COMPLETE receipt proves the effect.
    proven = EvidenceBundle(
        request_id="n8n_test", capability_id="workflow_automation:n8n", trace_id="t",
        status="COMPLETE", items=(), limitations=(),
        receipts=(ExecutionReceipt(
            receipt_id="t:s_modify_workflow", request_id="n8n_test", trace_id="t", step_id="s_modify_workflow",
            capability_id="workflow_automation:n8n", operation_id="modify_workflow",
            provider_id="existing_n8n_workflow_automation", status="COMPLETE", result="modified",
        ),),
        errors=(),
    )
    assert _unproven_effects(plan, proven) == ()


def test_logical_spec_compiles_branch_topology():
    from MAKSIMAR_SERVER.AI_ORCHESTRATION.n8n_logical_compiler import compile_logical_automation_spec

    spec = {
        "trigger": "manual",
        "steps": [
            {"action": "set_field", "field": "value", "value": "5"},
            {"action": "condition", "field": "value", "operator": "equals", "value": "5",
             "true_steps": [{"action": "set_field", "field": "result", "value": "passed"}],
             "false_steps": [{"action": "set_field", "field": "result", "value": "failed"}]},
        ],
        "constraints": ["local_only"],
    }
    graph = compile_logical_automation_spec(spec)
    types = [n["type"] for n in graph["nodes"]]
    # Manual -> set -> if -> set (true) -> set (false) = 5 functional nodes, real branch.
    assert types.count("n8n-nodes-base.manualTrigger") == 1
    assert types.count("n8n-nodes-base.if") == 1
    assert types.count("n8n-nodes-base.set") == 3
    assert len(graph["nodes"]) == 5
    if_node = next(n for n in graph["nodes"] if n["type"] == "n8n-nodes-base.if")
    assert len(graph["connections"][if_node["name"]]["main"]) == 2  # true + false outputs
    assert graph["connections"][if_node["name"]]["main"][0][0]["node"] != \
        graph["connections"][if_node["name"]]["main"][1][0]["node"]


def test_logical_spec_action_is_intrinsic_enum_not_platform_name():
    import json as _json
    from CONTROL_PLANE.canonical_semantic_spine import _LOGICAL_SPEC_PARAMETER_SCHEMA
    from MAKSIMAR_SERVER.AI_ORCHESTRATION.model_understanding_adapter import validate_structured_payload

    step_schema = _LOGICAL_SPEC_PARAMETER_SCHEMA["properties"]["steps"]["items"]
    # Provider/platform name is NOT an intrinsic action -> schema-invalid.
    bad, valid, _ = validate_structured_payload(_json.dumps({"action": "Google Drive"}), step_schema)
    assert valid is False
    # Provider-neutral catalog discovery is the open-ended path.
    _, valid2, _ = validate_structured_payload(
            _json.dumps({
                "step_id": "download", "next_step_ids": [], "action": "catalog_query", "catalog_query": "download a file from a cloud drive",
                "semantic_operation": "download a file", "provider_name": "cloud drive",
                "provider_provenance": "SEMANTIC_INFERENCE",
                "provider_inference_justification": "bounded provider candidate for the requested cloud file",
                "arguments": {},
            }), step_schema,
    )
    assert valid2 is True
    # Intrinsic primitive remains valid.
    _, valid3, _ = validate_structured_payload(
        _json.dumps({"step_id": "set", "next_step_ids": [], "action": "set_field", "field": "value", "value": "alpha"}), step_schema,
    )
    assert valid3 is True


def test_set_field_variant_requires_field_and_value():
    import json as _json
    from CONTROL_PLANE.canonical_semantic_spine import _LOGICAL_SPEC_PARAMETER_SCHEMA
    from MAKSIMAR_SERVER.AI_ORCHESTRATION.model_understanding_adapter import validate_structured_payload

    step_schema = _LOGICAL_SPEC_PARAMETER_SCHEMA["properties"]["steps"]["items"]
    # Model grammar and HOST both reject an incomplete variant.
    _, valid, _ = validate_structured_payload(_json.dumps({"action": "set_field", "value": "publish_to_youtube"}), step_schema)
    assert valid is False
    from MAKSIMAR_SERVER.AI_ORCHESTRATION.n8n_logical_compiler import LogicalSpecCompileError, compile_logical_automation_spec
    with pytest.raises(LogicalSpecCompileError, match="invalid_logical_step_contract"):
        compile_logical_automation_spec({"trigger": "manual", "steps": [
            {"step_id": "bad", "action": "set_field", "value": "publish_to_youtube"},
        ]})
    _, valid2, _ = validate_structured_payload(_json.dumps({
        "step_id": "set", "next_step_ids": [], "action": "set_field", "field": "task", "value": "alpha",
    }), step_schema)
    assert valid2 is True


def test_logical_spec_coverage_flags_all_set_degeneration():
    import json as _json
    from CONTROL_PLANE.canonical_semantic_spine import _logical_spec_coverage_reasons
    from MAKSIMAR_CORE_LIB.ai_orchestration.semantic_intent_contract import OperationRequirement, RequestUnderstanding

    degenerate_spec = _json.dumps({
        "trigger": "manual",
        "steps": [
            {"action": "set_field", "field": "a", "value": "video_from_drive"},
            {"action": "set_field", "field": "b", "value": "publish_to_youtube"},
        ],
    })
    u = RequestUnderstanding(
        request_id="r", original_text="content factory", language="ru",
        goals=(Goal("g1", "build content factory"),),
        required_capabilities=(CapabilityRequirement("workflow_automation:n8n", "build", True),),
        effect_type="MUTATE", target_scope="local_workflow_automation", reversibility="REVERSIBLE",
        external_side_effect=False, unresolved_capabilities=(),
        operation_requirements=(OperationRequirement(
            capability_id="workflow_automation:n8n", operation_id="create_workflow",
            purpose="create", required_evidence=("n8n_workflow",), effect_type="MUTATE",
            target_scope="local_workflow_automation", reversibility="REVERSIBLE",
            external_side_effect=False, risk_class="MUTATION", required=True,
            parameters=(("logical_spec", degenerate_spec),),
        ),),
        current_topic="automation", unresolved_reference="", relevant_context_trace_ids=(),
        risk_class="MUTATION", confidence=1.0, reason_codes=("typed_test",),
    )
    assert _logical_spec_coverage_reasons(u) == ("logical_spec_all_intrinsic_set_no_capability_coverage",)

    # A catalog_query step provides capability coverage -> no degeneration flag.
    covered_spec = _json.dumps({
        "trigger": "manual",
        "steps": [
            {"catalog_query": "download a file from a cloud drive"},
            {"action": "set_field", "field": "title", "value": "x"},
        ],
    })
    u2 = RequestUnderstanding(
        request_id="r2", original_text="content factory", language="ru",
        goals=(Goal("g1", "build content factory"),),
        required_capabilities=(CapabilityRequirement("workflow_automation:n8n", "build", True),),
        effect_type="MUTATE", target_scope="local_workflow_automation", reversibility="REVERSIBLE",
        external_side_effect=False, unresolved_capabilities=(),
        operation_requirements=(OperationRequirement(
            capability_id="workflow_automation:n8n", operation_id="create_workflow",
            purpose="create", required_evidence=("n8n_workflow",), effect_type="MUTATE",
            target_scope="local_workflow_automation", reversibility="REVERSIBLE",
            external_side_effect=False, risk_class="MUTATION", required=True,
            parameters=(("logical_spec", covered_spec),),
        ),),
        current_topic="automation", unresolved_reference="", relevant_context_trace_ids=(),
        risk_class="MUTATION", confidence=1.0, reason_codes=("typed_test",),
    )
    assert _logical_spec_coverage_reasons(u2) == ()


def test_logical_spec_coverage_rejects_recursive_jarvis_bridge_before_execution():
    import json as _json
    from CONTROL_PLANE.canonical_semantic_spine import _logical_spec_coverage_reasons
    from MAKSIMAR_CORE_LIB.ai_orchestration.semantic_intent_contract import OperationRequirement, RequestUnderstanding

    spec = _json.dumps({"trigger": "manual", "steps": [{
        "step_id": "publish", "next_step_ids": [], "action": "jarvis_capability",
        "capability_id": "workflow_automation:n8n", "request": "publish externally",
    }]})
    understanding = RequestUnderstanding(
        request_id="bridge-recursion", original_text="create a workflow", language="en",
        goals=(Goal("g1", "create a workflow"),),
        required_capabilities=(CapabilityRequirement("workflow_automation:n8n", "create", True),),
        effect_type="MUTATE", target_scope="local_workflow_automation", reversibility="REVERSIBLE",
        external_side_effect=False, unresolved_capabilities=(),
        operation_requirements=(OperationRequirement(
            capability_id="workflow_automation:n8n", operation_id="create_workflow", purpose="create",
            required_evidence=("n8n_workflow",), effect_type="MUTATE",
            target_scope="local_workflow_automation", reversibility="REVERSIBLE", external_side_effect=False,
            risk_class="MUTATION", required=True, parameters=(("logical_spec", spec),),
        ),), current_topic="workflow", unresolved_reference="", relevant_context_trace_ids=(),
        risk_class="MUTATION", confidence=1.0, reason_codes=("typed_test",),
    )
    assert _logical_spec_coverage_reasons(understanding) == (
        "logical_spec_jarvis_capability_recursive_or_non_executable",
    )


def test_generic_binding_reaches_node_operation_parameters_and_credential_precondition():
    from MAKSIMAR_SERVER.AI_ORCHESTRATION.n8n_logical_compiler import bind_catalog_step

    drive = bind_catalog_step({
        "provider_name": "Google Drive", "catalog_query": "download a file from Google Drive", "semantic_operation": "download",
        "arguments": {"File ID": "source-file-id"},
    })
    assert drive["node_type"] == "n8n-nodes-base.googleDrive"
    assert (drive["resource"], drive["operation"]) == ("file", "download")
    assert drive["parameters"]["fileId"] == "source-file-id"
    assert drive["missing_required_parameters"] == ()
    assert drive["missing_credential_types"] == ("googleDriveOAuth2Api",)
    assert drive["disposition"] == "PRECONDITION_REQUIRED"

    empty_drive = bind_catalog_step({
        "provider_name": "Google Drive", "catalog_query": "download a file from Google Drive", "semantic_operation": "download",
        "arguments": {},
    })
    assert empty_drive["disposition"] == "PRECONDITION_REQUIRED"
    assert "fileId" in empty_drive["missing_required_parameters"]

    youtube = bind_catalog_step({
        "provider_name": "YouTube", "catalog_query": "upload a video to YouTube", "semantic_operation": "upload",
        "arguments": {"Title": "Example", "Input Binary Field": "data"},
    })
    assert youtube["node_type"] == "n8n-nodes-base.youTube"
    assert (youtube["resource"], youtube["operation"]) == ("video", "upload")
    assert youtube["parameters"]["title"] == "Example"
    assert youtube["missing_credential_types"] == ("youTubeOAuth2Api",)


def test_unseen_installed_node_uses_same_generic_binding_without_aliases():
    from MAKSIMAR_SERVER.AI_ORCHESTRATION.n8n_logical_compiler import bind_catalog_step

    telegram = bind_catalog_step({
        "provider_name": "Telegram", "catalog_query": "Telegram messaging integration", "semantic_operation": "sendMessage",
        "arguments": {"Chat ID": "123", "Text": "hello"},
    })
    assert telegram["node_type"] == "n8n-nodes-base.telegram"
    assert (telegram["resource"], telegram["operation"]) == ("message", "sendMessage")
    assert telegram["missing_required_parameters"] == ()
    assert telegram["missing_credential_types"] == ("telegramApi",)


def test_explicit_uninstalled_provider_fails_closed_without_http_substitution():
    from MAKSIMAR_SERVER.AI_ORCHESTRATION.n8n_logical_compiler import (
        LogicalSpecCompileError, bind_catalog_step, compile_logical_automation_spec,
    )

    binding = bind_catalog_step({
        "provider_name": "TikTok", "catalog_query": "publish a short video",
        "semantic_operation": "publish a video", "arguments": {},
    })
    assert binding["disposition"] == "UNAVAILABLE"
    assert binding["node_type"] is None
    with pytest.raises(LogicalSpecCompileError, match="unavailable_catalog_binding:TikTok"):
        compile_logical_automation_spec({
            "trigger": "manual", "steps": [{
                "step_id": "publish", "next_step_ids": [], "action": "catalog_query",
                "provider_name": "TikTok", "provider_provenance": "SOURCE_EXPLICIT",
                "provider_inference_justification": "", "catalog_query": "publish a short video",
                "semantic_operation": "publish a video", "arguments": {},
            }],
        }, source_text="publish a short video through TikTok")


@pytest.mark.parametrize("query", [
    "скачать файл из Google Drive", "download a file from Google Drive", "Datei aus Google Drive herunterladen",
])
def test_multilingual_catalog_architecture_preserves_named_service(query):
    from MAKSIMAR_SERVER.AI_ORCHESTRATION.n8n_logical_compiler import bind_catalog_step

    binding = bind_catalog_step({
        "provider_name": "Google Drive", "catalog_query": query, "semantic_operation": "download", "arguments": {"File ID": "abc"},
    })
    assert binding["node_type"] == "n8n-nodes-base.googleDrive"
    assert binding["operation"] == "download"


@pytest.mark.parametrize("branch_count", [2, 3, 4, 7])
def test_generic_multiway_compiler_has_no_branch_count_special_case(branch_count):
    from MAKSIMAR_SERVER.AI_ORCHESTRATION.n8n_logical_compiler import compile_logical_automation_spec

    spec = {"trigger": "manual", "steps": [{
        "action": "route", "field": "choice",
        "branches": [{
            "label": f"path-{index}", "value": str(index),
            "steps": [{"action": "set_field", "field": "result", "value": str(index)}],
        } for index in range(branch_count)],
    }], "constraints": ["local_only"]}
    graph = compile_logical_automation_spec(spec)
    switch = next(node for node in graph["nodes"] if node["type"] == "n8n-nodes-base.switch")
    assert len(graph["connections"][switch["name"]]["main"]) == branch_count
    assert len(switch["parameters"]["rules"]["values"]) == branch_count


def test_parallel_fanout_and_real_merge_compile_generically():
    from MAKSIMAR_SERVER.AI_ORCHESTRATION.n8n_logical_compiler import compile_logical_automation_spec

    graph = compile_logical_automation_spec({"trigger": "manual", "steps": [{
        "action": "parallel", "merge": True,
        "branches": [{"label": str(index), "steps": [
            {"action": "set_field", "field": f"branch_{index}", "value": str(index)},
        ]} for index in range(3)],
    }, {"action": "set_field", "field": "complete", "value": "yes"}], "constraints": ["local_only"]})
    trigger_outputs = graph["connections"]["Trigger"]["main"][0]
    assert len(trigger_outputs) == 3
    merge = next(node for node in graph["nodes"] if node["type"] == "n8n-nodes-base.merge")
    assert merge["parameters"] == {"mode": "append", "numberInputs": 3}
    incoming_indexes = sorted(
        edge["index"] for source in graph["connections"].values()
        for output in source.get("main", ()) for edge in output if edge["node"] == merge["name"]
    )
    assert incoming_indexes == [0, 1, 2]


def test_nested_control_flow_schema_and_compiler():
    from CONTROL_PLANE.canonical_semantic_spine import _LOGICAL_SPEC_PARAMETER_SCHEMA
    from MAKSIMAR_SERVER.AI_ORCHESTRATION.model_understanding_adapter import validate_structured_payload
    from MAKSIMAR_SERVER.AI_ORCHESTRATION.n8n_logical_compiler import compile_logical_automation_spec

    steps = [
        {"step_id": "outer", "next_step_ids": ["inner", "b_result"], "action": "route", "field": "outer", "branches": [
            {"value": "a", "target_step_id": "inner"}, {"value": "b", "target_step_id": "b_result"},
        ]},
        {"step_id": "inner", "next_step_ids": ["ax", "other"], "action": "condition", "field": "inner", "operator": "equals", "value": "x",
         "true_step_id": "ax", "false_step_id": "other"},
        {"step_id": "ax", "next_step_ids": [], "action": "set_field", "field": "result", "value": "ax"},
        {"step_id": "other", "next_step_ids": [], "action": "set_field", "field": "result", "value": "other"},
        {"step_id": "b_result", "next_step_ids": [], "action": "set_field", "field": "result", "value": "b"},
    ]
    for step in steps:
        _, valid, error = validate_structured_payload(json.dumps(step), _LOGICAL_SPEC_PARAMETER_SCHEMA["properties"]["steps"]["items"])
        assert valid, error
    graph = compile_logical_automation_spec({"trigger": "manual", "steps": steps, "constraints": ["local_only"]})
    assert {node["type"] for node in graph["nodes"]} >= {"n8n-nodes-base.switch", "n8n-nodes-base.if"}


def test_missing_credentials_do_not_prevent_draft_graph_compilation():
    from MAKSIMAR_SERVER.AI_ORCHESTRATION.n8n_logical_compiler import compile_logical_automation_spec

    graph = compile_logical_automation_spec({"trigger": "manual", "steps": [{
        "provider_name": "Google Drive", "catalog_query": "download a file from Google Drive", "semantic_operation": "download",
        "arguments": {"File ID": "abc"},
    }]})
    report = graph["_jarvis_binding_report"][0]
    assert report["disposition"] == "PRECONDITION_REQUIRED"
    assert report["missing_credential_types"] == ("googleDriveOAuth2Api",)
    drive = next(node for node in graph["nodes"] if node["type"] == "n8n-nodes-base.googleDrive")
    assert "credentials" not in drive


def test_model_http_endpoint_must_be_present_in_current_source():
    from MAKSIMAR_SERVER.AI_ORCHESTRATION.n8n_logical_compiler import (
        LogicalSpecCompileError, compile_logical_automation_spec,
    )

    spec = {"trigger": "manual", "steps": [{
        "step_id": "call", "next_step_ids": [], "action": "http_request",
        "url": "https://invented.invalid/publish", "method": "POST",
    }]}
    with pytest.raises(LogicalSpecCompileError, match="endpoint_not_source_grounded"):
        compile_logical_automation_spec(spec, source_text="Publish through the named service API.")
    graph = compile_logical_automation_spec(
        spec, source_text="Call https://invented.invalid/publish with POST.",
    )
    assert any(node["type"] == "n8n-nodes-base.httpRequest" for node in graph["nodes"])


def test_catalog_trigger_must_resolve_to_an_installed_trigger_node():
    from MAKSIMAR_SERVER.AI_ORCHESTRATION.n8n_logical_compiler import (
        LogicalSpecCompileError, compile_logical_automation_spec,
    )

    with pytest.raises(LogicalSpecCompileError, match="resolved_node_is_not_trigger"):
        compile_logical_automation_spec({
            "trigger": {"catalog_query": "workflow_automation:n8n", "provider_name": "n8n-nodes-base.set"},
            "steps": [{"action": "set_field", "field": "status", "value": "pending"}],
        })


def test_real_semantic_operation_cannot_be_represented_as_set_field():
    from MAKSIMAR_SERVER.AI_ORCHESTRATION.n8n_logical_compiler import (
        LogicalSpecCompileError, compile_logical_automation_spec,
    )

    spec = {
        "trigger": "manual",
        "steps": [{
            "step_id": "metadata", "next_step_ids": [], "action": "set_field",
            "field": "title", "value": "decorative placeholder",
        }],
        "semantic_requirements": [{
            "requirement_id": "generate_metadata", "operation_class": "GENERATE",
            "source_grounding": "generate title", "step_id": "metadata",
        }],
    }
    with pytest.raises(LogicalSpecCompileError, match="real_operation_misrepresented_as_set_field"):
        compile_logical_automation_spec(spec, source_text="generate title and description")


def test_canonical_source_operation_cannot_be_omitted_or_covered_by_control_flow():
    from MAKSIMAR_SERVER.AI_ORCHESTRATION.n8n_logical_compiler import (
        LogicalSpecCompileError, compile_logical_automation_spec,
    )

    omitted = {
        "trigger": "manual", "_canonical_requirement_ids": ["publish_1"],
        "steps": [{
            "step_id": "route", "next_step_ids": [], "action": "condition",
            "field": "provider", "operator": "equals", "value": "ready",
            "true_step_id": "yes", "false_step_id": "no",
        }, {
            "step_id": "yes", "next_step_ids": [], "action": "set_field",
            "field": "provider", "value": "Named Service",
        }, {
            "step_id": "no", "next_step_ids": [], "action": "set_field",
            "field": "status", "value": "inactive",
        }],
        "semantic_requirements": [],
    }
    with pytest.raises(LogicalSpecCompileError, match="coverage_mismatch"):
        compile_logical_automation_spec(omitted)

    control_flow_coverage = dict(omitted)
    control_flow_coverage["semantic_requirements"] = [{
        "requirement_id": "publish_1", "operation_class": "PUBLISH",
        "source_grounding": "publish through Named Service", "step_id": "route",
        "provider_name": "Named Service", "provider_provenance": "SOURCE_EXPLICIT",
    }]
    with pytest.raises(LogicalSpecCompileError, match="real_operation_not_operational_step"):
        compile_logical_automation_spec(
            control_flow_coverage, source_text="Create a workflow to publish through Named Service",
        )

    unreferenced = {
        "trigger": "manual", "_canonical_requirement_ids": ["publish_1"],
        "steps": [{
            "step_id": "publish", "next_step_ids": ["host_create"], "action": "catalog_query",
            "catalog_query": "Named Service", "semantic_operation": "send",
            "provider_name": "Named Service", "provider_provenance": "SOURCE_EXPLICIT",
            "provider_inference_justification": "", "arguments": {},
        }, {
            "step_id": "host_create", "next_step_ids": [], "action": "catalog_query",
            "catalog_query": "workflow create", "semantic_operation": "create",
            "provider_name": "n8n", "provider_provenance": "SOURCE_EXPLICIT",
            "provider_inference_justification": "", "arguments": {},
        }],
        "semantic_requirements": [{
            "requirement_id": "publish_1", "operation_class": "SEND",
            "source_grounding": "send through Named Service", "step_id": "publish",
            "provider_name": "Named Service", "provider_provenance": "SOURCE_EXPLICIT",
        }],
    }
    with pytest.raises(LogicalSpecCompileError, match="unreferenced_real_operation_step"):
        compile_logical_automation_spec(
            unreferenced, source_text="Create an n8n workflow to send through Named Service",
        )


def test_provider_provenance_is_typed_and_source_verified():
    from MAKSIMAR_SERVER.AI_ORCHESTRATION.n8n_logical_compiler import bind_catalog_step

    explicit = bind_catalog_step({
        "provider_name": "Google Drive", "provider_provenance": "SOURCE_EXPLICIT",
        "catalog_query": "download a cloud file", "semantic_operation": "download",
        "arguments": {"File ID": "abc"},
    }, source_text="Download the file from Google Drive")
    assert explicit["provider_provenance"] == "SOURCE_EXPLICIT"
    assert explicit["node_type"] == "n8n-nodes-base.googleDrive"

    identifier_surface = bind_catalog_step({
        "provider_name": "google_drive", "provider_provenance": "SOURCE_EXPLICIT",
        "catalog_query": "download a cloud file", "semantic_operation": "download",
        "arguments": {"File ID": "abc"},
    }, source_text="Download the file from Google Drive")
    assert identifier_surface["provider_provenance"] == "SOURCE_EXPLICIT"
    assert identifier_surface["node_type"] == "n8n-nodes-base.googleDrive"

    fabricated = bind_catalog_step({
        "provider_name": "Google Drive", "provider_provenance": "SOURCE_EXPLICIT",
        "catalog_query": "download a cloud file", "semantic_operation": "download",
    }, source_text="Download the file from the service selected by policy")
    assert fabricated["disposition"] == "AMBIGUOUS"
    assert fabricated["reason"] == "explicit_provider_not_source_grounded"

    inferred = bind_catalog_step({
        "provider_name": "Google Drive", "provider_provenance": "SEMANTIC_INFERENCE",
        "provider_inference_justification": "bounded installed provider candidate chosen for cloud-file semantics",
        "catalog_query": "download a cloud file", "semantic_operation": "download",
        "arguments": {"File ID": "abc"},
    }, source_text="Download the file from the service selected by policy")
    assert inferred["provider_provenance"] == "SEMANTIC_INFERENCE"
    assert inferred["provider_inference_justification"]


def test_ambiguous_operation_and_parameter_mapping_fail_closed(monkeypatch):
    from MAKSIMAR_SERVER.AI_ORCHESTRATION import n8n_logical_compiler as compiler

    fake_node = {"name": "fake", "displayName": "Fake"}
    monkeypatch.setattr(compiler, "resolve_logical_step", lambda step: ("fake.node", fake_node))
    monkeypatch.setattr(compiler, "operation_candidates", lambda node: (
        {"resource": "record", "resource_name": "Record", "operation": "sendA", "operation_name": "Send", "description": "send item"},
        {"resource": "record", "resource_name": "Record", "operation": "sendB", "operation_name": "Send", "description": "send item"},
    ))
    ambiguous_operation = compiler.bind_catalog_step({
        "catalog_query": "send item", "semantic_operation": "send", "arguments": {},
    })
    assert ambiguous_operation["disposition"] == "AMBIGUOUS"
    assert len(ambiguous_operation["operation_candidates"]) == 2

    monkeypatch.setattr(compiler, "operation_candidates", lambda node: (
        {"resource": "record", "resource_name": "Record", "operation": "send", "operation_name": "Send", "description": "send item"},
    ))
    monkeypatch.setattr(compiler, "parameter_contract", lambda node, resource, operation: (
        {"name": "targetA", "displayName": "Target", "description": "message destination", "required": False},
        {"name": "targetB", "displayName": "Target", "description": "message destination", "required": False},
    ))
    monkeypatch.setattr(compiler, "credential_requirements", lambda node, parameters: ())
    ambiguous_parameter = compiler.bind_catalog_step({
        "catalog_query": "send item", "semantic_operation": "send",
        "arguments": {"Target": "destination"},
    })
    assert ambiguous_parameter["disposition"] == "AMBIGUOUS"
    assert ambiguous_parameter["unmapped_semantic_arguments"] == ("Target",)
    assert ambiguous_parameter["parameter_ambiguity_candidates"]["Target"] == ("targetA", "targetB")


def test_n8n_jarvis_bridge_calls_same_semantic_spine_without_model_or_provider_name():
    from MAKSIMAR_SERVER.AI_ORCHESTRATION.n8n_logical_compiler import (
        JARVIS_CANONICAL_HOT_ENDPOINT, compile_logical_automation_spec,
    )

    graph = compile_logical_automation_spec({
        "trigger": "manual",
        "steps": [{
            "step_id": "metadata", "next_step_ids": [], "action": "jarvis_capability",
            "capability_id": "content.metadata.generate",
            "request": "Generate a grounded title, description and hashtags for the supplied local transcript",
        }],
        "semantic_requirements": [{
            "requirement_id": "metadata_generation", "operation_class": "GENERATE",
            "source_grounding": "Generate a grounded title", "step_id": "metadata",
        }],
    }, source_text="Generate a grounded title for the supplied local transcript",
       allowed_jarvis_capability_ids=frozenset({"content.metadata.generate"}))
    node = next(item for item in graph["nodes"] if item["type"] == "n8n-nodes-base.httpRequest")
    assert node["parameters"]["url"] == JARVIS_CANONICAL_HOT_ENDPOINT
    body = json.loads(node["parameters"]["body"])
    assert body == {
        "text": "Generate a grounded title, description and hashtags for the supplied local transcript",
        "expected_capability_id": "content.metadata.generate",
    }
    assert "ollama" not in json.dumps(node, ensure_ascii=False).casefold()
    assert "qwen" not in json.dumps(node, ensure_ascii=False).casefold()
    report = graph["_jarvis_binding_report"][0]
    assert report["provider_provenance"] == "INSTALLED_PROVIDER_CONTRACT"
    assert report["operation"] == "semantic_turn"
    assert report["parameters"]["capability_id"] == "content.metadata.generate"


def test_n8n_jarvis_bridge_rejects_unselected_or_recursive_capability():
    from MAKSIMAR_SERVER.AI_ORCHESTRATION.n8n_logical_compiler import (
        LogicalSpecCompileError, compile_logical_automation_spec,
    )

    spec = {"trigger": "manual", "steps": [{
        "step_id": "publish", "next_step_ids": [], "action": "jarvis_capability",
        "capability_id": "publish:tiktok", "request": "Publish the video",
    }]}
    with pytest.raises(LogicalSpecCompileError, match="jarvis_capability_not_selected"):
        compile_logical_automation_spec(spec)
    spec["steps"][0]["capability_id"] = "workflow_automation:n8n"
    with pytest.raises(LogicalSpecCompileError, match="recursive_or_non_executable"):
        compile_logical_automation_spec(
            spec, allowed_jarvis_capability_ids=frozenset({"workflow_automation:n8n"}),
        )


def test_content_metadata_is_semantic_capability_over_local_model_provider(monkeypatch):
    from MAKSIMAR_SERVER.AI_ORCHESTRATION import model_role_adapter
    from MAKSIMAR_SERVER.SKILL_ADAPTER_REGISTRY.existing_capability_inventory import (
        _inventory_records, build_semantic_capability_registry_projection,
    )

    monkeypatch.setattr(model_role_adapter, "ollama_chat_once", lambda *args, **kwargs: {
        "ok": True,
        "content": json.dumps({
            "title": "Local semantic spine", "description": "One canonical provider path",
            "hashtags": ["#jarvis", "#local"],
        }),
        "done": True, "done_reason": "stop", "requested_num_ctx": 3072,
    })
    understanding = RequestUnderstanding(
        request_id="metadata_test", original_text="Generate metadata for a local semantic spine video", language="en",
        goals=(Goal("g1", "generate content metadata"),),
        required_capabilities=(CapabilityRequirement("content.metadata.generate", "generate metadata", True),),
        effect_type="OBSERVE", target_scope="provided_content_context", reversibility="REVERSIBLE",
        external_side_effect=False, unresolved_capabilities=(), operation_requirements=(),
        current_topic="content metadata", unresolved_reference="", relevant_context_trace_ids=(),
        risk_class="READ_ONLY", confidence=1.0, reason_codes=("typed_test",),
    )
    step = PlanStep(
        step_id="metadata", goal_id="g1", capability_id="content.metadata.generate",
        operation="generate_content_metadata", required_evidence=("content_metadata",), effect_type="OBSERVE",
        target_scope="provided_content_context", reversibility="REVERSIBLE", external_side_effect=False,
        risk_class="READ_ONLY", parameters=(("task", "Local semantic spine video transcript"),),
    )
    bundle = model_role_adapter.ExistingOllamaModelRoleAdapter().collect_evidence(
        understanding, ExecutionPlan(request_id="metadata_test", steps=(step,)), "trace_metadata",
    )
    assert bundle.status == "COMPLETE"
    assert bundle.items[0].kind == "content_metadata"
    assert bundle.items[0].capability_id == "content.metadata.generate"
    assert bundle.receipts[0].provider_id == model_role_adapter.PROVIDER_ID

    _inventory_records.cache_clear()
    projection = build_semantic_capability_registry_projection()
    entry = next(item for item in projection["entries"] if item["capability_id"] == "content.metadata.generate")
    assert entry["selection_mode"] == "EXECUTABLE"
    assert entry["provider_ids"] == (model_role_adapter.PROVIDER_ID,)
    assert entry["operation_contracts"][0]["operation_id"] == "generate_content_metadata"


def test_media_probe_uses_canonical_evidence_and_rejects_missing_local_file(tmp_path, monkeypatch):
    from MAKSIMAR_SERVER.AI_ORCHESTRATION import media_provider_adapter as media

    local_file = tmp_path / "sample.wav"
    local_file.write_bytes(b"RIFFtest")
    monkeypatch.setattr(media.subprocess, "run", lambda *args, **kwargs: type("Done", (), {
        "returncode": 0, "stdout": json.dumps({"format": {"duration": "1.0"}, "streams": []}),
    })())
    understanding = RequestUnderstanding(
        request_id="media_test", original_text=f"probe {local_file}", language="en",
        goals=(Goal("g1", "inspect local media"),),
        required_capabilities=(CapabilityRequirement("media.probe", "inspect", True),),
        effect_type="OBSERVE", target_scope="local_media_file", reversibility="REVERSIBLE",
        external_side_effect=False, unresolved_capabilities=(), operation_requirements=(),
        current_topic="media", unresolved_reference="", relevant_context_trace_ids=(),
        risk_class="READ_ONLY", confidence=1.0, reason_codes=("typed_test",),
    )
    step = PlanStep(
        step_id="probe", goal_id="g1", capability_id="media.probe", operation="probe_media",
        required_evidence=("media_probe",), effect_type="OBSERVE", target_scope="local_media_file",
        reversibility="REVERSIBLE", external_side_effect=False, risk_class="READ_ONLY",
        parameters=(("path", str(local_file)),),
    )
    bundle = media.ExistingFfprobeMediaAdapter().collect_evidence(
        understanding, ExecutionPlan(request_id="media_test", steps=(step,)), "trace_media",
    )
    assert bundle.status == "COMPLETE"
    assert bundle.items[0].kind == "media_probe"
    assert bundle.receipts[0].provider_id == media.PROVIDER_ID

    missing_step = PlanStep(
        step_id="missing", goal_id="g1", capability_id="media.probe", operation="probe_media",
        required_evidence=("media_probe",), effect_type="OBSERVE", target_scope="local_media_file",
        reversibility="REVERSIBLE", external_side_effect=False, risk_class="READ_ONLY",
        parameters=(("path", str(tmp_path / "missing.wav")),),
    )
    missing = media.ExistingFfprobeMediaAdapter().collect_evidence(
        understanding, ExecutionPlan(request_id="media_test", steps=(missing_step,)), "trace_missing",
    )
    assert missing.status == "UNAVAILABLE" and not missing.receipts


@pytest.mark.parametrize("readback_case", ["correct", "stale", "missing", "wrong_identity", "unavailable"])
def test_modify_workflow_requires_authoritative_readback(monkeypatch, readback_case):
    import copy
    initial = _acceptance_workflow("before")
    initial["id"] = "wf_readback"
    calls = []
    def request(method, path, payload=None):
        calls.append((method, path))
        if method == "PUT":
            return {"id": "wf_readback", **copy.deepcopy(payload)}
        if len(calls) == 1:
            return copy.deepcopy(initial)
        if readback_case == "unavailable":
            return {"error": "http_503"}
        result = copy.deepcopy(initial)
        if readback_case == "correct":
            result["nodes"][1]["parameters"]["assignments"]["assignments"][0]["value"] = "after"
        elif readback_case == "missing":
            result["nodes"] = result["nodes"][:1]
        elif readback_case == "wrong_identity":
            result["id"] = "different_workflow"
            result["nodes"][1]["parameters"]["assignments"]["assignments"][0]["value"] = "after"
        return result
    monkeypatch.setattr(n8n_adapter, "_n8n_request", request)
    bundle = n8n_adapter.ExistingN8nAdapter().collect_evidence(_understanding(),
        ExecutionPlan(request_id="n8n_test", steps=(
            _step("modify_workflow", (("workflow_id", "wf_readback"), ("value", "after"))),)),
        "trace_readback")
    assert [method for method, _ in calls] == ["GET", "PUT", "GET"]
    if readback_case == "correct":
        assert bundle.status == "COMPLETE"
        assert len(bundle.receipts) == 1 and bundle.receipts[0].status == "COMPLETE"
        assert json.loads(bundle.items[0].observation)["new_value"] == "after"
    else:
        assert bundle.status != "COMPLETE" and bundle.errors
        assert not bundle.items
        assert not any(receipt.status == "COMPLETE" for receipt in bundle.receipts)


def test_catalog_credentials_reuse_canonical_provider_database_without_legacy_fallback(monkeypatch, tmp_path):
    import hashlib
    import sqlite3
    from pathlib import Path
    from MAKSIMAR_SERVER.AI_ORCHESTRATION import n8n_adapter as provider, n8n_local_catalog as catalog
    home = tmp_path / "old_home"
    canonical = tmp_path / "canonical" / ".n8n"
    canonical.mkdir(parents=True)
    legacy = home / ".n8n"
    legacy.mkdir(parents=True)
    monkeypatch.setattr(Path, "home", classmethod(lambda cls: home))
    monkeypatch.setattr(provider, "_CANONICAL_DATA_ROOT", canonical)

    def database(path, identity):
        with sqlite3.connect(path) as db:
            db.execute("CREATE TABLE credentials_entity(id TEXT, name TEXT, type TEXT, data TEXT)")
            db.execute("INSERT INTO credentials_entity VALUES(?,?,?,?)", (identity, identity, "providerType", "private fixture payload"))
    database(legacy / "database.sqlite", "old_credential")
    # Missing canonical data must not read old migration credentials or create a DB.
    assert catalog.available_credential_instances() == ()
    assert not (canonical / "database.sqlite").exists()
    database(canonical / "database.sqlite", "canonical_credential")
    before = hashlib.sha256((canonical / "database.sqlite").read_bytes()).hexdigest()
    calls = []
    connect = sqlite3.connect
    def read_only(database_uri, **kwargs):
        calls.append((database_uri, kwargs))
        assert str(database_uri).endswith("?mode=ro") and kwargs["uri"] is True
        return connect(database_uri, **kwargs)
    monkeypatch.setattr(catalog.sqlite3, "connect", read_only)
    assert catalog.available_credential_instances() == ({"id": "canonical_credential", "name": "canonical_credential", "type": "providerType"},)
    assert str(canonical / "database.sqlite") in calls[-1][0]
    assert hashlib.sha256((canonical / "database.sqlite").read_bytes()).hexdigest() == before
    # An explicit diagnostic/test source remains supported, without becoming default authority.
    assert catalog.available_credential_instances(legacy / "database.sqlite")[0]["id"] == "old_credential"


def test_n8n_network_policy_is_identity_bound_not_description_bound():
    from MAKSIMAR_SERVER.AI_ORCHESTRATION.n8n_local_catalog import transport_requirement, network_truth, network_scope
    for description in ('consume cloud API integration upload webhook', 'safe local computation'):
        unknown = {'type': 'custom.unknown', 'name': 'unknown', 'description': description}
        assert transport_requirement(unknown) == 'UNKNOWN'
        assert network_truth(unknown) == 'UNKNOWN'
        assert network_scope(unknown) == 'UNKNOWN'
        foreign_same_name = {'type': 'custom.set', 'name': 'set', 'description': description}
        assert transport_requirement(foreign_same_name) == 'UNKNOWN'
        assert network_truth(foreign_same_name) == 'UNKNOWN'
        local = {'type': 'n8n-nodes-base.set', 'name': 'set', 'description': description}
        assert transport_requirement(local) == 'NONE'
        assert network_truth(local) == 'LOCAL'
        network = {'type': 'n8n-nodes-base.httpRequest', 'name': 'httpRequest', 'description': description}
        assert transport_requirement(network) == 'NETWORK_TRANSPORT'
        assert network_truth(network) == 'NETWORK_REQUIRED'


def test_n8n_compilation_never_selects_provider_by_text_search(monkeypatch):
    import MAKSIMAR_SERVER.AI_ORCHESTRATION.n8n_logical_compiler as compiler
    def forbidden_search(*args, **kwargs):
        raise AssertionError('search is discovery evidence, not provider authority')
    monkeypatch.setattr(compiler, 'search_n8n_catalog', forbidden_search, raising=False)
    assert compiler.resolve_logical_step({'action': 'catalog_query', 'catalog_query': 'send a telegram message'}) == (None, None)
    node_type, node = compiler.resolve_logical_step({'action': 'catalog_query', 'provider_name': 'n8n-nodes-base.telegram'})
    assert node_type == 'n8n-nodes-base.telegram' and node is not None


def test_n8n_operation_binding_never_selects_by_description_tokens():
    import MAKSIMAR_SERVER.AI_ORCHESTRATION.n8n_logical_compiler as compiler
    node = {'properties': [{'name': 'operation', 'type': 'options', 'options': [
        {'name': 'Download', 'value': 'download', 'description': 'download a file from the cloud'}]}]}
    assert compiler._select_operation(node, 'download a file') is None
    assert compiler._select_operation(node, 'download')['operation'] == 'download'


def test_n8n_architect_validates_structure_without_word_policy(monkeypatch):
    import json
    import MAKSIMAR_SERVER.AI_ORCHESTRATION.n8n_adapter as adapter
    import MAKSIMAR_SERVER.AI_ORCHESTRATION.model_role_adapter as models
    spec = {'name': 'local note', 'trigger': 'manual', 'steps': [
        {'action': 'set_field', 'field': 'note', 'value': 'docker credential secret shell publish'}]}
    class Author:
        def generate_bounded_text(self, *args, **kwargs):
            return {'ok': True, 'content': json.dumps(spec)}
    monkeypatch.setattr(models, 'ExistingOllamaModelRoleAdapter', Author)
    assert adapter._architect_logical_spec('original request') == spec
    spec['steps'] = [{'action': 'http_request', 'url': 'https://example.invalid'}]
    with pytest.raises(ValueError, match='logical_spec_'):
        adapter._architect_logical_spec('original request')
    spec['steps'] = [{'action': 'transform', 'kind': 'normalize', 'code': 'return []'}]
    with pytest.raises(ValueError, match='declarative'):
        adapter._architect_logical_spec('original request')


def test_n8n_compiled_declarative_data_does_not_become_action_policy():
    import MAKSIMAR_SERVER.AI_ORCHESTRATION.n8n_adapter as adapter
    spec = {'name': 'local data', 'trigger': 'manual', 'steps': [
        {'action': 'set_field', 'field': 'note', 'value': 'secret docker credential shell'}]}
    graph, error = adapter._compiled_workflow_spec({'logical_spec': spec})
    assert error is None and graph is not None
    data_node = next(node for node in graph['nodes'] if node['type'] == 'n8n-nodes-base.set')
    assert data_node['parameters']['assignments']['assignments'][0]['value'] == 'secret docker credential shell'
    spec['steps'] = [{'action': 'transform', 'kind': 'normalize', 'code': 'return []'}]
    with pytest.raises(ValueError, match='declarative'):
        adapter._compiled_workflow_spec({'logical_spec': spec})


def test_n8n_argument_mapping_requires_installed_field_identity():
    from MAKSIMAR_SERVER.AI_ORCHESTRATION.n8n_logical_compiler import _bind_arguments
    contract = ({'name': 'chatId', 'displayName': 'Chat ID', 'description': 'recipient destination', 'required': True},)
    bound, missing, unmapped, ambiguity = _bind_arguments(contract, {'recipient': '123'})
    assert 'chatId' not in bound and missing == ('chatId',) and unmapped == ('recipient',)
    assert _bind_arguments(contract, {'Chat ID': '123'})[:3] == ({'chatId': '123'}, (), ())


@pytest.mark.parametrize("kind", ["unknown_action", "unknown_field", "free_code", "malformed_node"])
def test_n8n_invalid_authoring_input_returns_failure_evidence_without_provider_write(monkeypatch, kind):
    calls = []
    def forbidden_request(*args, **kwargs):
        calls.append(args)
        raise AssertionError("invalid spec must not reach provider write")
    monkeypatch.setattr(n8n_adapter, "_n8n_request", forbidden_request)
    if kind == "malformed_node":
        parameter = ("workflow", json.dumps({"nodes": ["not a node"], "connections": {"source": {}}}))
    else:
        node = {"action": "set_field", "field": "note", "value": "source data"}
        if kind == "unknown_action": node["action"] = "unsupported_action"
        if kind == "unknown_field": node["unexpected"] = True
        if kind == "free_code": node = {"action": "transform", "kind": "normalize", "code": "return []"}
        parameter = ("logical_spec", json.dumps({"trigger": "manual", "steps": [node]}))
    bundle = n8n_adapter.ExistingN8nAdapter().collect_evidence(
        _understanding(), ExecutionPlan(request_id="n8n_test", steps=(
            _step("create_workflow", (parameter,)),)), "trace_invalid_input")
    assert bundle.status == "UNAVAILABLE"
    assert bundle.errors and any("create_workflow:" in error for error in bundle.errors)
    assert not bundle.items and not any(receipt.status == "COMPLETE" for receipt in bundle.receipts)
    assert calls == []


def test_adapter_accepts_existing_typed_dag_and_preserves_branch_edges():
    from MAKSIMAR_SERVER.AI_ORCHESTRATION import n8n_adapter as adapter
    spec = {"trigger": "manual", "steps": [
        {"step_id": "seed", "next_step_ids": ["choose"], "action": "set_field", "field": "value", "value": "5"},
        {"step_id": "choose", "next_step_ids": [], "action": "condition", "field": "value", "operator": "equals", "value": "5", "true_step_id": "yes", "false_step_id": "no"},
        {"step_id": "yes", "next_step_ids": [], "action": "set_field", "field": "result", "value": "passed"},
        {"step_id": "no", "next_step_ids": [], "action": "set_field", "field": "result", "value": "failed"},
    ], "constraints": ["local_only", "no_credentials"]}
    graph, error = adapter._compiled_workflow_spec({"logical_spec": spec})
    assert error is None
    condition = next(n for n in graph["nodes"] if n["type"] == "n8n-nodes-base.if")
    outputs = graph["connections"][condition["name"]]["main"]
    assert len(outputs) == 2
    assert outputs[0][0]["node"] != outputs[1][0]["node"]
    assert len(graph["nodes"]) == 5


@pytest.mark.parametrize("change", ["unknown_field", "unknown_action", "free_code", "cycle"])
def test_adapter_typed_dag_keeps_structural_and_declarative_rejections(change):
    from MAKSIMAR_SERVER.AI_ORCHESTRATION import n8n_adapter as adapter
    spec = {"trigger": "manual", "steps": [{"step_id": "one", "next_step_ids": [], "action": "set_field", "field": "value", "value": "5"}]}
    step = spec["steps"][0]
    if change == "unknown_field": step["run_shell"] = "do something"
    elif change == "unknown_action": step["action"] = "execute_shell"
    elif change == "free_code": step.update(action="transform", code="return items;")
    else: step["next_step_ids"] = ["one"]
    try:
        graph, error = adapter._compiled_workflow_spec({"logical_spec": spec})
    except ValueError:
        return
    assert graph is None and error


def _prepare_and_bind_graph(adapter, monkeypatch, graph, *, granted=True, trace="graph_trace"):
    from MAKSIMAR_CORE_LIB.ai_orchestration.semantic_intent_contract import PermissionDecision
    monkeypatch.setattr(n8n_adapter, "_read_stored_workflow", lambda wid: dict(graph, id=wid))
    plan = ExecutionPlan(request_id="n8n_test", steps=(
        _step("execute_workflow", (("workflow_id", "wf_bound"),)),))
    prepared = adapter.prepare_plan_for_policy(plan=plan, trace_id=trace)
    step = prepared.steps[0]
    permission = PermissionDecision(granted=granted, capability_id=step.capability_id,
        identity_source="verified_owner", policy_version="test", denial_reason="",
        trace_id=trace, operation_id=step.operation, step_id=step.step_id)
    adapter.bind_host_permission(permissions=(permission,), plan=prepared, trace_id=trace)
    return prepared


def test_stored_graph_cannot_execute_without_host_bound_permission(monkeypatch):
    called = []
    monkeypatch.setattr(n8n_adapter, "_run_cli_execute", lambda *a, **k: called.append(a))
    bundle = n8n_adapter.ExistingN8nAdapter().collect_evidence(_understanding(),
        ExecutionPlan(request_id="n8n_test", steps=(
            _step("execute_workflow", (("workflow_id", "wf_bound"), ("approved", "true"))),)),
        "graph_trace")
    assert not called and bundle.status != "COMPLETE"
    assert "execute_workflow:stored_graph_permission_not_bound" in bundle.errors


@pytest.mark.parametrize("mutation", ["http", "code", "expression", "credentials", "error_workflow"])
def test_stored_graph_unknown_effects_never_inherit_local_reversible_policy(monkeypatch, mutation):
    graph = _acceptance_workflow("literal")
    if mutation == "http": graph["nodes"][1]["type"] = "n8n-nodes-base.httpRequest"
    elif mutation == "code": graph["nodes"][1]["type"] = "n8n-nodes-base.code"
    elif mutation == "expression": graph["nodes"][1]["parameters"]["assignments"]["assignments"][0]["value"] = "={{ $env.SECRET }}"
    elif mutation == "credentials": graph["nodes"][1]["credentials"] = {"credential": {"id": "private"}}
    else: graph["settings"]["errorWorkflow"] = "other_workflow"
    adapter = n8n_adapter.ExistingN8nAdapter()
    prepared = _prepare_and_bind_graph(adapter, monkeypatch, graph, granted=False)
    step = prepared.steps[0]
    assert step.risk_class == "UNKNOWN" and step.reversibility == "UNKNOWN"
    assert step.external_side_effect is True
    called = []
    monkeypatch.setattr(n8n_adapter, "_run_cli_execute", lambda *a, **k: called.append(a))
    bundle = adapter.collect_evidence(_understanding(), prepared, "graph_trace")
    assert not called and bundle.status != "COMPLETE"


def test_stored_graph_literal_intrinsics_bind_exact_hash_and_actual_effects(monkeypatch):
    adapter = n8n_adapter.ExistingN8nAdapter()
    graph = _acceptance_workflow("literal")
    prepared = _prepare_and_bind_graph(adapter, monkeypatch, graph)
    step = prepared.steps[0]
    assert step.risk_class == "MUTATION" and step.reversibility == "REVERSIBLE"
    assert step.external_side_effect is False
    calls = []
    def run(wid, *, expected_graph_hash):
        assert expected_graph_hash == n8n_adapter._stored_workflow_hash(dict(graph, id=wid))
        calls.append(wid)
        return {"returncode": 0, "execution_status": "success", "execution_id": "42"}
    monkeypatch.setattr(n8n_adapter, "_run_cli_execute", run)
    bundle = adapter.collect_evidence(_understanding(), prepared, "graph_trace")
    assert calls == ["wf_bound"] and bundle.status == "COMPLETE"
    observation = json.loads(bundle.items[0].observation)
    assert observation["stored_graph_sha256"]


@pytest.mark.parametrize("mismatch", ["trace", "parameters", "step"])
def test_stored_graph_permission_cannot_be_replayed_for_other_execution(monkeypatch, mismatch):
    from dataclasses import replace
    adapter = n8n_adapter.ExistingN8nAdapter()
    prepared = _prepare_and_bind_graph(adapter, monkeypatch, _acceptance_workflow("literal"))
    trace = "graph_trace"
    if mismatch == "trace": trace = "other_trace"
    elif mismatch == "parameters": prepared = replace(prepared, steps=(replace(prepared.steps[0], parameters=(("workflow_id", "other"),)),))
    else: prepared = replace(prepared, steps=(replace(prepared.steps[0], step_id="other_step"),))
    calls = []
    monkeypatch.setattr(n8n_adapter, "_run_cli_execute", lambda *a, **k: calls.append(a))
    bundle = adapter.collect_evidence(_understanding(), prepared, trace)
    assert not calls and bundle.status != "COMPLETE"


@pytest.mark.parametrize("changed", [False, True])
def test_stored_graph_hash_checked_inside_existing_cli_handoff(monkeypatch, tmp_path, changed):
    runtime = tmp_path / "canonical"
    data = runtime / ".n8n"
    data.mkdir(parents=True)
    (data / "database.sqlite").touch()
    monkeypatch.setattr(n8n_adapter, "_CANONICAL_RUNTIME_ROOT", runtime)
    monkeypatch.setattr(n8n_adapter, "_CANONICAL_DATA_ROOT", data)
    monkeypatch.setattr(n8n_adapter, "_canonical_container", lambda **kw: None)
    monkeypatch.setattr(n8n_adapter, "_canonical_server_pid", lambda: None)
    original = dict(_acceptance_workflow("original"), id="wf_bound")
    stored = dict(_acceptance_workflow("changed" if changed else "original"), id="wf_bound")
    monkeypatch.setattr(n8n_adapter, "_read_stored_workflow", lambda wid: stored)
    calls = []
    monkeypatch.setattr(n8n_adapter, "_execute_cli_in_canonical_data_root",
        lambda wid: calls.append(wid) or {"execution_status": "success"})
    result = n8n_adapter._run_cli_execute("wf_bound",
        expected_graph_hash=n8n_adapter._stored_workflow_hash(original))
    if changed:
        assert result == {"error": "stored_graph_changed_after_policy"} and not calls
    else:
        assert result["execution_status"] == "success" and calls == ["wf_bound"]


@pytest.mark.parametrize("literal", [False, True])
def test_stored_graph_effects_are_evaluated_by_existing_single_policy_owner(monkeypatch, literal):
    from MAKSIMAR_CORE_LIB.security_layer.semantic_policy import SemanticPolicyEvaluator
    from MAKSIMAR_CORE_LIB.ai_orchestration.semantic_intent_contract import IdentityContext
    graph = _acceptance_workflow("literal" if literal else "={{ $env.SECRET }}")
    adapter = n8n_adapter.ExistingN8nAdapter()
    plan = _prepare_and_bind_graph(adapter, monkeypatch, graph, granted=False)
    step = plan.steps[0]
    decision = SemanticPolicyEvaluator().evaluate(capability_id=step.capability_id,
        operation_id=step.operation, risk_class=step.risk_class, effect_type=step.effect_type,
        target_scope=step.target_scope, reversibility=step.reversibility,
        external_side_effect=step.external_side_effect,
        identity=IdentityContext("owner", "local_terminal_session", "owner", True, True),
        trace_id="graph_trace", step_id=step.step_id)
    assert decision.granted is literal and decision.approval_required is not literal
    adapter.bind_host_permission(permissions=(decision,), plan=plan, trace_id="graph_trace")
    assert bool(adapter._approved_graphs) is literal


def test_stored_graph_same_plan_create_without_identity_cannot_inherit_draft_permission(monkeypatch):
    from dataclasses import replace
    adapter = n8n_adapter.ExistingN8nAdapter()
    read = []
    monkeypatch.setattr(n8n_adapter, "_read_stored_workflow", lambda wid: read.append(wid))
    step = replace(_step("execute_workflow"), parameters=())
    plan = adapter.prepare_plan_for_policy(plan=ExecutionPlan("n8n_test", (step,)), trace_id="graph_trace")
    assert not read and not adapter._policy_graphs
    assert plan.steps[0].risk_class == "UNKNOWN"
