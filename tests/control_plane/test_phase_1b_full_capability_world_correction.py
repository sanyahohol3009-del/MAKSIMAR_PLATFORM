from __future__ import annotations

import json
import inspect
from pathlib import Path

import pytest

import CONTROL_PLANE.canonical_semantic_spine as spine
import MAKSIMAR_SERVER.WORKERS.simulation_worker  # noqa: F401 (registers runtime factory in CORE registry)
import CONTROL_PLANE.api_server as api_server
from MAKSIMAR_CORE_LIB.ai_orchestration.semantic_intent_contract import (
    CapabilityRequirement, EvidenceBundle, EvidenceItem, ExecutionPlan, ExecutionReceipt,
    Goal, IdentityContext, OperationRequirement, PermissionDecision, PlanStep,
    RequestDeadline, RequestUnderstanding,
    utc_observed_at,
)
from MAKSIMAR_CORE_LIB.ai_orchestration.helper_model_decision_parser import (
    parse_discovery_selection_payload, parse_request_understanding_payload,
)
from MAKSIMAR_CORE_LIB.capability_registry.capability_registry_loader import (
    project_semantic_capability_index, project_semantic_operation_catalog,
    select_semantic_projection_details, validate_semantic_capability_projection,
)
import MAKSIMAR_SERVER.AI_ORCHESTRATION.ollama_transport as transport
import MAKSIMAR_SERVER.AI_ORCHESTRATION.project_workspace_tools as project_tools
from MAKSIMAR_SERVER.AI_ORCHESTRATION.ollama_transport import _filter_private_reasoning
from MAKSIMAR_SERVER.AI_ORCHESTRATION.ollama_transport import _flush_private_reasoning
from MAKSIMAR_SERVER.SKILL_ADAPTER_REGISTRY.existing_capability_inventory import (
    build_semantic_capability_registry_projection,
)
from MAKSIMAR_SERVER.AI_ORCHESTRATION.memory_retrieval_adapter import (
    ExistingMemoryRetrievalAdapter,
    MEMORY_CAPABILITY_OPERATION_CONTRACTS,
    MEMORY_RETRIEVAL_OPERATION_CONTRACTS,
)
from MAKSIMAR_SERVER.AI_ORCHESTRATION.project_understanding_adapter import (
    ExistingProjectUnderstandingAdapter,
)
from MAKSIMAR_SERVER.AI_ORCHESTRATION.simulation_worker_adapter import (
    ExistingSimulationWorkerAdapter,
    SIMULATION_CAPABILITY_OPERATION_CONTRACTS,
)
from MAKSIMAR_SERVER.WORKFLOW_AUTOMATION_RUNTIME.jarvis_pc_action_adapter_contract import (
    PC_ACTION_OPERATION_CONTRACTS,
)


OWNER = IdentityContext(
    "aleksandr", "local_terminal_session", "owner", True, True, "Александр", "JARVIS",
)


def model_call_envelope(content):
    return {
        "ok": True, "content": content, "final_valid": True,
        "model_call_attempted": True, "model_call_succeeded": True,
        "model_call_used": False, "raw_output_present": bool(content),
        "requested_num_ctx": spine.SEMANTIC_SELECTION_NUM_CTX,
        "configured_num_ctx": spine.SEMANTIC_SELECTION_NUM_CTX,
    }


def understanding_call_envelope(content):
    """Request-understanding uses a dedicated larger context window (structured output)."""
    envelope = model_call_envelope(content)
    envelope["requested_num_ctx"] = 4096
    envelope["configured_num_ctx"] = 4096
    return envelope


def _candidate_slot_enum(schema):
    """Extract the allowed capability IDs from the sparse candidate schema (property names)."""
    return tuple(sorted(schema["properties"]["candidate_capability_ids"]["properties"]))


class Model:
    def __init__(self, projection, capability_ids):
        self.catalog = {item["capability_id"]: item for item in project_semantic_operation_catalog(projection)}
        self.entries = {item["capability_id"]: item for item in projection["entries"]}
        requested_ids = tuple(capability_ids)
        self.capability_ids = tuple(dict.fromkeys((
            *requested_ids,
            *(("conversation.respond",) if "conversation.respond" in self.entries else ()),
        )))

    def discover_candidates(self, **kwargs):
        schema_properties = kwargs["output_schema"]["properties"]
        if "candidate_operation_ids" in schema_properties:
            allowed = tuple(
                value
                for value in schema_properties["candidate_operation_ids"]["properties"]
            )
            # Fixed slots use slot names as properties and put the operation IDs in each
            # slot enum; sparse-map schemas put operation IDs directly in properties.
            if allowed and all(value.startswith("selection_") for value in allowed):
                slot_names = allowed
                operation_ids = tuple(
                    value for value in schema_properties["candidate_operation_ids"]
                    ["properties"][slot_names[0]]["enum"] if value is not None
                )
                selected_operations = operation_ids[:spine.DISCOVERY_VALUES_PER_PASS]
                selection_payload = {
                    slot: selected_operations[index] if index < len(selected_operations) else None
                    for index, slot in enumerate(slot_names)
                }
            else:
                selected_operations = allowed[:spine.DISCOVERY_VALUES_PER_PASS]
                selection_payload = {value: True for value in selected_operations}
            supplied = json.loads(kwargs["user_prompt"])
            grounding = str(supplied.get("original_text", ""))
            return model_call_envelope(json.dumps({
                "candidate_operation_ids": selection_payload,
                "selection_justifications": {operation_id: {
                    "goal_id": "g1", "justification_kind": "DIRECT_GOAL_EFFECT",
                    "source_grounding": grounding,
                } for operation_id in selected_operations},
                "continuation_required": False, "continuation_reason": "",
                "ambiguity_present": False, "confidence": 0.99,
                "reason_codes": ["same_main_model_semantic_operation_discovery"],
            }))
        allowed = tuple(
            _candidate_slot_enum(kwargs["output_schema"])
        )
        available = kwargs["system_prompt"]
        selected = tuple(value for value in self.capability_ids if value in available and value in allowed)
        batch = selected[:spine.DISCOVERY_VALUES_PER_PASS]
        continuation = len(selected) > len(batch)
        return model_call_envelope(json.dumps({
            "candidate_capability_ids": {value: True for value in batch},
            "continuation_required": continuation,
            "continuation_reason": "more selected capabilities" if continuation else "",
            "ambiguity_present": False,
            "confidence": 0.99, "reason_codes": ["same_main_model_semantic_discovery"],
        }))

    def discover_kinds(self, **kwargs):
        allowed = tuple(
            kwargs["output_schema"]["properties"]["candidate_kinds"]["properties"]
        )
        kinds = tuple(dict.fromkeys(str(self.entries[value]["kind"]) for value in self.capability_ids))
        selected = tuple(value for value in kinds if value in allowed)
        batch = selected[:spine.DISCOVERY_VALUES_PER_PASS]
        continuation = len(selected) > len(batch)
        return model_call_envelope(json.dumps({
            "candidate_kinds": {value: True for value in batch},
            "continuation_required": continuation,
            "continuation_reason": "more selected kinds" if continuation else "",
            "ambiguity_present": False, "confidence": 0.99, "reason_codes": ["semantic_kind_discovery"],
        }))

    def understand(self, *, system_prompt, user_prompt, deadline):
        del system_prompt, deadline
        supplied = json.loads(user_prompt)
        operations = [self.catalog[value] for value in self.capability_ids if value in self.catalog]
        payload = {
            "schema_version": "request_understanding.v2", "language": "ru",
            "goals": [{"goal_id": f"g{index}", "description": f"Consider {value}"}
                      for index, value in enumerate(self.capability_ids, 1)],
            "required_capabilities": [{
                "capability_id": value, "purpose": self.entries[value]["semantic_description"], "required": True,
                "operation_contract_required": bool(self.entries[value]["execution_contract_available"]),
                "unresolved_operation_reason": "" if self.entries[value]["execution_contract_available"] else "execution_contract_unavailable",
            } for value in self.capability_ids],
            "response_requirements": [],
            "effect_type": operations[0]["effect_type"] if operations else "UNKNOWN",
            "target_scope": operations[0]["target_scope"] if operations else "UNKNOWN",
            "reversibility": operations[0]["reversibility"] if operations else "UNKNOWN",
            "external_side_effect": any(item["external_side_effect"] for item in operations) if operations else None,
            "unresolved_capabilities": [],
            "operation_requirements": [{
                "capability_id": item["capability_id"], "operation_id": item["operation_id"],
                "purpose": item["operation_description"], "required_evidence": list(item["evidence_kinds"]),
                "effect_type": item["effect_type"], "target_scope": item["target_scope"],
                "reversibility": item["reversibility"], "external_side_effect": item["external_side_effect"],
                "risk_class": item["risk_class"], "required": True,
            } for item in operations],
            "current_topic": "capability selection", "unresolved_reference": "",
            "risk_class": operations[0]["risk_class"] if operations else "UNKNOWN",
            "confidence": 0.99, "reason_codes": ["model_semantic_selection"],
        }
        if len({item["effect_type"] for item in operations}) > 1:
            payload["effect_type"] = "MUTATE"
        if len({item["risk_class"] for item in operations}) > 1:
            payload["risk_class"] = "MUTATION"
        return understanding_call_envelope(json.dumps(payload, ensure_ascii=False))


class EvidencePort:
    def __init__(self, provider_id="targeted_existing_provider"):
        self.provider_id = provider_id

    def health(self):
        return {"status": "AVAILABLE", "provider_id": self.provider_id}

    def collect_evidence(self, understanding, plan, trace_id, *args):
        del args
        items = tuple(
            EvidenceItem(
                kind=kind, source="targeted_existing_provider", observation=step.operation,
                scope=step.target_scope, confidence=1.0, trace_id=trace_id,
                observed_at=utc_observed_at(), source_reference="registry://targeted-provider",
                request_id=understanding.request_id, step_id=step.step_id,
                capability_id=step.capability_id, operation_id=step.operation,
                provider_id=self.provider_id,
            )
            for step in plan.steps for kind in step.required_evidence
        )
        receipts = tuple(ExecutionReceipt(
            receipt_id=f"{trace_id}:{step.step_id}", request_id=understanding.request_id,
            trace_id=trace_id, step_id=step.step_id, capability_id=step.capability_id,
            operation_id=step.operation, provider_id=self.provider_id,
            status="COMPLETE", result="targeted evidence collected",
        ) for step in plan.steps)
        return EvidenceBundle(
            understanding.request_id, "+".join(step.capability_id for step in plan.steps), trace_id,
            "COMPLETE", items, (), receipts, (), capability_ids=tuple(step.capability_id for step in plan.steps),
        )


class Final:
    def answer(self, **kwargs):
        del kwargs
        return {"ok": True, "response_text": "grounded", "model_call_attempted": True,
                "model_call_succeeded": True, "model_call_used": True, "raw_output_present": True,
                "done": True, "done_reason": "stop", "truncation": False}


def projection(readiness=None):
    return build_semantic_capability_registry_projection(readiness=readiness or {
        "pc_executor_available": False, "ollama_alive": True, "model_residency": {},
    })


def test_existing_memory_retrieval_owner_is_executable_without_synthetic_provider():
    registry = projection()
    entry = next(
        item for item in registry["entries"]
        if item["capability_id"] == "runtime_history_store"
    )

    assert entry["operation_contract_source"] == "EXISTING_TYPED_CONTRACT"
    assert entry["provider_binding_status"] == "BOUND"
    assert entry["provider_ids"] == ("existing_memory_retrieval_tools",)
    assert entry["execution_contract_available"] is True
    assert entry["selection_mode"] == "EXECUTABLE"
    assert tuple(
        item["operation_id"] for item in entry["operation_contracts"]
    ) == tuple(item["operation_id"] for item in MEMORY_RETRIEVAL_OPERATION_CONTRACTS)
    assert not any(
        str(provider_id).startswith("existing_inventory_provider::")
        for provider_id in entry["provider_ids"]
    )


@pytest.mark.parametrize(("capability_id", "operation_id"), (
    ("runtime_history_store", "inspect_retrieval_backends"),
    ("runtime_history_store", "inspect_memory_registry"),
    ("dashboard_memory_read_models", "read_dashboard_memory_models"),
    ("enterprise_business_memory", "read_enterprise_business_memory"),
    ("local_chat_memory", "read_local_chat_memory"),
    ("memory_engine_registry", "read_memory_engine_registry"),
    ("regulatory_memory_foundation", "read_regulatory_memory_foundation"),
    ("session_memory", "read_session_memory"),
    ("mempalace_read_only_sandbox", "read_mempalace_sandbox"),
    ("vector_runtime_indexes", "read_vector_runtime_indexes"),
))
def test_existing_memory_retrieval_provider_returns_matching_step_receipt(
    capability_id, operation_id,
):
    adapter = ExistingMemoryRetrievalAdapter()
    contract = next(
        item for item in MEMORY_CAPABILITY_OPERATION_CONTRACTS[capability_id]
        if item["operation_id"] == operation_id
    )
    understanding = RequestUnderstanding(
        request_id="request_memory",
        original_text="Покажи состояние локальных систем поиска знаний",
        language="ru",
        goals=(Goal("goal_memory", "Inspect retrieval availability"),),
        required_capabilities=(
            CapabilityRequirement(
                capability_id, "Inspect retrieval availability", True,
            ),
        ),
        effect_type="OBSERVE",
        target_scope="local_retrieval_runtime",
        reversibility="REVERSIBLE",
        external_side_effect=False,
        unresolved_capabilities=(),
        operation_requirements=(OperationRequirement(
            capability_id=capability_id,
            operation_id=str(contract["operation_id"]),
            purpose=str(contract["description"]),
            required_evidence=tuple(contract["evidence_kinds"]),
            effect_type=str(contract["effect_type"]),
            target_scope=str(contract["target_scope"]),
            reversibility=str(contract["reversibility"]),
            external_side_effect=bool(contract["external_side_effect"]),
            risk_class=str(contract["risk_class"]),
            required=True,
        ),),
        current_topic="retrieval availability",
        unresolved_reference="",
        relevant_context_trace_ids=(),
        risk_class="READ_ONLY",
        confidence=1.0,
        reason_codes=("typed_test",),
    )
    step = PlanStep(
        step_id="step_memory",
        goal_id="goal_memory",
        capability_id=capability_id,
        operation=operation_id,
        required_evidence=tuple(contract["evidence_kinds"]),
        effect_type="OBSERVE",
        target_scope=str(contract["target_scope"]),
        reversibility="REVERSIBLE",
        external_side_effect=False,
        risk_class="READ_ONLY",
    )

    bundle = adapter.collect_evidence(
        understanding,
        ExecutionPlan(request_id="request_memory", steps=(step,)),
        "trace_memory",
    )

    assert bundle.status == "COMPLETE"
    assert len(bundle.items) == 1
    assert len(bundle.receipts) == 1
    assert bundle.items[0].step_id == "step_memory"
    assert bundle.items[0].provider_id == adapter.provider_id
    assert bundle.receipts[0].step_id == "step_memory"
    assert bundle.receipts[0].operation_id == operation_id
    assert bundle.receipts[0].provider_id == adapter.provider_id
    assert bundle.capability_ids == (capability_id,)


def test_memory_operation_semantics_distinguish_history_content_from_status_metadata():
    descriptions = {
        item["operation_id"]: item["description"]
        for item in MEMORY_RETRIEVAL_OPERATION_CONTRACTS
    }
    assert "persisted conversation history" in descriptions["search_history"]
    assert "verified experiences" in descriptions["search_history"]
    assert "actual bounded recent records" in descriptions["inspect_recent_session_memory"]
    contracts = {item["operation_id"]: item for item in MEMORY_RETRIEVAL_OPERATION_CONTRACTS}
    assert contracts["search_history"]["required_parameters"] == ("query", "memory_filter")
    assert "query_kind" in contracts["search_history"]["parameter_schemas"]["memory_filter"]["required"]
    for operation_id in ("inspect_memory_registry", "inspect_retrieval_backends", "inspect_memory_federation"):
        assert contracts[operation_id]["required_parameters"] == ()
        assert contracts[operation_id]["evidence_kinds"] != ("history_search",)
        assert contracts[operation_id]["effect_type"] == "OBSERVE"
    registry = select_semantic_projection_details(projection(), ("runtime_history_store",))
    operation_prompt, _ = spine.build_operation_discovery_prompt(
        original_text="Что раньше фиксировалось в истории проекта?",
        session_context={},
        registry_projection=registry,
    )
    assert "For content retrieval, do not add registry, domain, federation" in operation_prompt
    candidate_prompt, _ = spine.build_candidate_discovery_prompt(
        original_text="Найди сохранённую историю проекта",
        session_context={},
        registry_projection=registry,
    )
    assert "bounded session context is not a prerequisite for retrieval" in candidate_prompt


def test_discovery_context_keeps_only_referent_while_understanding_keeps_recent_turns():
    context = {
        "bounded_chronological_turns": ({
            "user_text": "у" * 200, "assistant_text": "а" * 240,
            "topic": "recent topic", "trace_id": "trace_recent",
        },),
        "unresolved_reference": {"present": True, "description": "previous answer"},
    }
    selected = select_semantic_projection_details(projection(), ("conversation.respond",))
    _, discovery_user = spine.build_candidate_discovery_prompt(
        original_text="продолжи", session_context=context, registry_projection=selected,
    )
    candidate_system, _ = spine.build_candidate_discovery_prompt(
        original_text="продолжи", session_context=context, registry_projection=selected,
    )
    kind_system, _ = spine.build_kind_discovery_prompt(
        original_text="продолжи", session_context=context, registry_projection=selected,
    )
    understanding_system, understanding_user = spine.build_request_understanding_prompt(
        request_id="request_context_caps", original_text="продолжи", identity=OWNER,
        session_context=context, registry_projection=selected,
    )
    discovery_context = json.loads(discovery_user)["bounded_session_context"]
    understanding_context = json.loads(understanding_user)["bounded_session_context"]

    # Discovery stages carry only referential topic labels and an explicit unresolved
    # referent, never historical turn text: full turn text would create a new goal or
    # override the current domain under a long shared session.
    # CURRENT_EXPLICIT_REQUEST > HISTORICAL_CONTEXT.
    assert "recent_turns" not in discovery_context
    assert discovery_context["topic_history"] == ["recent topic"]
    assert discovery_context["unresolved_reference"]["description"] == "previous answer"
    # The understanding stage keeps full referential context for conversation continuity.
    assert len(understanding_context["recent_turns"][0]["user_text"]) == 120
    assert len(understanding_context["recent_turns"][0]["assistant_text"]) == 160
    assert "current original_text" in candidate_system
    assert "current original_text" in kind_system
    assert "Only original_text creates goals" in understanding_system


@pytest.mark.parametrize(("capability_id", "operation_id"), (
    ("skill_simulation_simulation_analysis", "analyze_simulation"),
    ("worker_sim_001", "run_simulation_task"),
))
def test_existing_simulation_owner_executes_skill_and_worker_with_matching_receipt(
    capability_id, operation_id,
):
    contract = SIMULATION_CAPABILITY_OPERATION_CONTRACTS[capability_id][0]
    assert "control_validation, safety_regression, or runtime_pressure_probe" in contract["description"]
    projected = next(
        item for item in projection()["entries"]
        if item["capability_id"] == capability_id
    )
    assert projected["provider_available"] is True
    assert projected["availability_status"] == "AVAILABLE"
    candidate_prompt, _ = spine.build_candidate_discovery_prompt(
        original_text="run a bounded local computation",
        session_context={},
        registry_projection=select_semantic_projection_details(
            projection(), (capability_id,),
        ),
    )
    assert "Delegated work or computation needs its indexed executable capability" in candidate_prompt
    parameters = (("scenario_type", "control_validation"), ("iteration_budget", "25"))
    understanding = RequestUnderstanding(
        request_id="request_simulation",
        original_text="Проведи локальную безопасную контрольную симуляцию на 25 итераций",
        language="ru",
        goals=(Goal("goal_simulation", "Run local simulation"),),
        required_capabilities=(CapabilityRequirement(
            capability_id, "Run local simulation", True,
        ),),
        effect_type="EXECUTE",
        target_scope="local_simulation_runtime",
        reversibility="REVERSIBLE",
        external_side_effect=False,
        unresolved_capabilities=(),
        operation_requirements=(OperationRequirement(
            capability_id=capability_id,
            operation_id=operation_id,
            purpose=str(contract["description"]),
            required_evidence=("simulation_result",),
            effect_type="EXECUTE",
            target_scope="local_simulation_runtime",
            reversibility="REVERSIBLE",
            external_side_effect=False,
            risk_class="MUTATION",
            required=True,
            parameters=parameters,
        ),),
        current_topic="local simulation",
        unresolved_reference="",
        relevant_context_trace_ids=(),
        risk_class="MUTATION",
        confidence=1.0,
        reason_codes=("typed_test",),
    )
    step = PlanStep(
        step_id="step_simulation",
        goal_id="goal_simulation",
        capability_id=capability_id,
        operation=operation_id,
        required_evidence=("simulation_result",),
        effect_type="EXECUTE",
        target_scope="local_simulation_runtime",
        reversibility="REVERSIBLE",
        external_side_effect=False,
        risk_class="MUTATION",
        parameters=parameters,
    )
    adapter = ExistingSimulationWorkerAdapter()
    bundle = adapter.collect_evidence(
        understanding,
        ExecutionPlan(request_id=understanding.request_id, steps=(step,)),
        "trace_simulation",
    )
    assert bundle.status == "COMPLETE"
    assert bundle.capability_ids == (capability_id,)
    assert bundle.items[0].capability_id == capability_id
    assert bundle.receipts[0].operation_id == operation_id
    assert json.loads(bundle.items[0].observation)["status"] == "completed"


def run_selection(capability_ids, *, response_envelope=True):
    registry = projection()
    if not response_envelope:
        registry = dict(registry)
        registry["entries"] = tuple(
            item for item in registry["entries"]
            if item["capability_id"] != "conversation.respond"
        )
        registry["capability_count"] = len(registry["entries"])
    entries = {item["capability_id"]: item for item in registry["entries"]}
    ports = {}
    for capability_id in capability_ids:
        entry = entries[capability_id]
        if entry["execution_contract_available"]:
            entry["provider_available"] = True
            entry["availability_status"] = "AVAILABLE"
            provider_id = entry["provider_ids"][0]
            ports[provider_id] = EvidencePort(provider_id)
    return spine.run_canonical_semantic_turn(
        text="unseen natural formulation", project_port=EvidencePort(), conversation_port=EvidencePort(),
        model_port=Model(registry, capability_ids), final_brain_port=Final(),
        permission_port=__import__("MAKSIMAR_CORE_LIB.security_layer.semantic_policy", fromlist=["SemanticPolicyEvaluator"]).SemanticPolicyEvaluator(),
        identity=OWNER, registry_projection=registry, provider_ports=ports, defer_final_brain=True,
    )


def test_full_projection_connects_current_inventory_two_manifests_and_five_model_roles():
    registry = validate_semantic_capability_projection(projection())
    assert registry["inventory_capability_count"] == 80
    assert "mempalace_read_only_sandbox" not in {item["capability_id"] for item in registry["entries"]}
    assert registry["manifest_only_capability_count"] == 2
    assert registry["model_role_count"] == 5
    assert registry["capability_count"] == 88
    serialized = json.dumps(registry, ensure_ascii=False)
    assert '"aliases"' not in serialized
    assert '"semantic_hints"' not in serialized


def test_path_exists_does_not_create_provider_or_synthetic_operation():
    registry = projection()
    entry = next(item for item in registry["entries"] if item["capability_id"] == "repo_git_status")
    assert entry["adapter_installed"] is True
    assert entry["provider_ids"] == () and entry["provider_exists"] is False
    assert entry["provider_binding_status"] == "UNBOUND"
    assert entry["execution_contract_available"] is False
    assert entry["operation_contracts"] == ()
    assert entry["supported_effects"] == ("UNKNOWN",)
    assert entry["target_restrictions"] == ("UNKNOWN",)
    assert "use__" not in json.dumps(registry, ensure_ascii=False)


def test_manifest_operations_are_authoritative_and_bound_to_existing_adapters():
    registry = projection()
    executable = [item for item in registry["entries"] if item["execution_contract_available"]]
    executable_ids = {item["capability_id"] for item in executable}
    assert {"conversation.respond", "project.read", "runtime_history_store"} <= executable_ids
    assert {
        "read_file_snippet", "read_file_outline", "project_codegraph_readonly",
        "build_project_workspace_read_model", "build_jarvis_live_tool_catalog_read_model",
        "build_jarvis_live_memory_federation_status", "status_tools", "model_runtime_status",
        "qdrant_readonly_status", "retrieval_backend_status_read_model",
        "jarvis_runtime_library:agents", "jarvis_runtime_library:skills",
        "jarvis_runtime_library:tools", "jarvis_runtime_library:manifests",
        "skill_simulation_simulation_analysis", "worker_sim_001",
        "code.proposal.generate", "content.metadata.generate",
        "runtime_tooling:flutter",
    } <= executable_ids
    assert {item["operation_contract_source"] for item in executable} == {
        "MANIFEST", "EXISTING_TYPED_CONTRACT",
    }
    assert all(item["provider_binding_status"] == "BOUND" for item in executable)
    executable_by_id = {item["capability_id"]: item for item in executable}
    for capability_id in ("code.proposal.generate", "content.metadata.generate"):
        assert executable_by_id[capability_id]["provider_available"] is True
        assert "model" not in capability_id
    for capability_id in ("model_role:daily_coder_model", "model_role:heavy_coder_model"):
        role = next(item for item in registry["entries"] if item["capability_id"] == capability_id)
        assert role["execution_contract_available"] is False
        assert role["selection_mode"] == "PLAN_ONLY"
    assert {item["provider_ids"][0] for item in executable} == {
        "existing_jarvis_final_brain", "existing_project_workspace_tools",
        "existing_memory_retrieval_tools", "existing_simulation_worker_runtime",
        "existing_ollama_model_roles", "windows_edge_adapter",
        "existing_n8n_workflow_automation", "existing_ffmpeg_media_tools",
        "browser_playwright_provider",
    }
    pc_safe_mutation = {"open_browser", "open_opera", "volume_up", "volume_down", "volume_mute", "open_project_workbench"}
    pc_dangerous = {"close_opera", "close_all_opera", "type_text", "browser_search"}
    for item in executable:
        for operation in item["operation_contracts"]:
            if item["capability_id"] in {
                "skill_simulation_simulation_analysis", "worker_sim_001",
            } | pc_safe_mutation:
                assert operation["risk_class"] == "MUTATION"
            elif item["capability_id"] == "content.shorts.generate":
                # Local content generation mutates the asset workspace but has no
                # external side effect; its typed contract remains operation-level.
                assert operation["risk_class"] == "MUTATION"
            elif item["capability_id"] in pc_dangerous:
                assert operation["risk_class"] == "DANGEROUS"
            elif item["capability_id"] == "workflow_automation:n8n":
                # Execution effects require actual stored graph observation before policy.
                expected = ("UNKNOWN" if operation["operation_id"] == "execute_workflow" else
                            "MUTATION" if operation["operation_id"] in {"build_workflow", "create_workflow", "modify_workflow"} else "READ_ONLY")
                assert operation["risk_class"] == expected
            elif item["capability_id"] == "browser.web":
                expected = "MUTATION" if operation["operation_id"] == "browser.fill_submit" else "READ_ONLY"
                assert operation["risk_class"] == expected
            else:
                expected = "MUTATION" if operation["operation_id"] == "refresh_mempalace_source" else "READ_ONLY"
                assert operation["risk_class"] == expected
    assert executable_by_id["read_screen"]["policy_metadata"]["approval_may_be_required"] is False
    assert executable_by_id["runtime_windows_edge"]["policy_metadata"]["approval_may_be_required"] is False
    assert executable_by_id["volume_up"]["policy_metadata"]["approval_may_be_required"] is False
    assert executable_by_id["type_text"]["policy_metadata"]["approval_may_be_required"] is True
    assert executable_by_id["browser_search"]["policy_metadata"]["approval_may_be_required"] is True
def test_complete_compact_index_activates_conservative_hierarchy_without_truncation():
    registry = projection()
    index = project_semantic_capability_index(registry)
    assert len(index) == 88
    assert "mempalace_read_only_sandbox" not in {item["capability_id"] for item in index}
    assert {item["capability_id"] for item in index} == {item["capability_id"] for item in registry["entries"]}
    system, user = spine.build_candidate_discovery_prompt(
        original_text="свободная формулировка", session_context={}, registry_projection=registry,
    )
    candidate_budget = spine.measure_prompt_budget(
        system, user, reserved_output_tokens=spine.CANDIDATE_DISCOVERY_RESERVED_OUTPUT_TOKENS,
        output_schema=spine.CANDIDATE_DISCOVERY_JSON_SCHEMA,
    )
    assert candidate_budget["within_budget"] is False
    assert candidate_budget["num_ctx"] == 3072 and candidate_budget["reserved_output_tokens"] == 256
    assert candidate_budget["estimated_prompt_tokens"] == max(
        (candidate_budget["utf8_bytes"] + 2) // 3, (candidate_budget["characters"] + 1) // 2,
    )
    assert candidate_budget["estimator_is_conservative"] is True
    assert candidate_budget["budget_decision_source"] == "CONSERVATIVE_STATIC_ESTIMATE"
    selected = select_semantic_projection_details(registry, ("conversation.respond", "project.read"))
    # RequestUnderstanding receives only the final operation set, never every contract
    # exposed by the selected capability during the earlier choice stage.
    for entry in selected["entries"]:
        entry["operation_contracts"] = entry["operation_contracts"][:1]
    system, user = spine.build_request_understanding_prompt(
        request_id="request_budget", original_text="ответь и проверь проект", identity=OWNER,
        session_context={}, input_preparation={}, registry_projection=selected,
    )
    understanding_budget = spine.require_prompt_budget(
        system, user, reserved_output_tokens=spine.REQUEST_UNDERSTANDING_RESERVED_OUTPUT_TOKENS,
        output_schema=spine.request_understanding_schema_for_projection(selected),
        num_ctx=spine.REQUEST_UNDERSTANDING_NUM_CTX,
    )
    assert understanding_budget["within_budget"] is True
    assert understanding_budget["reserved_output_tokens"] == 1600
    assert understanding_budget["actual_prompt_tokens"] is None
    assert understanding_budget["tokenizer_status"] == "NOT_EXECUTED"
    assert understanding_budget["schema_context_cost"] == "UNKNOWN"
    for host_field in ("request_id", "original_text", "relevant_context_trace_ids"):
        assert host_field not in spine.REQUEST_UNDERSTANDING_JSON_SCHEMA["properties"]
        assert host_field not in spine.REQUEST_UNDERSTANDING_JSON_SCHEMA["required"]
    assert "Host owns" in system
    with pytest.raises(ValueError, match="prompt_budget_exceeded"):
        spine.require_prompt_budget("x" * 20000, "y", reserved_output_tokens=1000)


def test_structured_output_reserves_cover_transport_num_predict_limits():
    adapter_source = Path(
        "MAKSIMAR_SERVER/AI_ORCHESTRATION/model_understanding_adapter.py"
    ).read_text(encoding="utf-8")
    assert "num_predict=192" not in adapter_source
    assert "num_predict=256" in adapter_source
    assert "num_predict=REQUEST_UNDERSTANDING_NUM_PREDICT" in adapter_source
    assert spine.CANDIDATE_DISCOVERY_RESERVED_OUTPUT_TOKENS >= 256
    assert spine.REQUEST_UNDERSTANDING_RESERVED_OUTPUT_TOKENS >= 1600
    assert '"think": OLLAMA_FAST_CHAT_THINK' in adapter_source


def test_request_understanding_schema_is_bound_to_selected_authoritative_ids():
    registry = projection()
    selected = select_semantic_projection_details(registry, ("project.read",))
    schema = spine.request_understanding_schema_for_projection(selected)
    assert "required_capabilities" not in schema["properties"]
    operations = schema["properties"]["operation_requirements"]
    assert operations["type"] == "object"
    assert operations["additionalProperties"] is False
    assert operations["maxProperties"] == len(spine.load_operation_catalog(selected))
    assert set(operations["required"]) == {
        item["operation_id"] for item in spine.load_operation_catalog(selected)
    }
    assert all(
        item["additionalProperties"] is False
        for item in operations["properties"].values()
    )
    assert "same model discovery stage" in operations["description"]
    assert "unresolved_capabilities" not in schema["properties"]
    assert "effect_type" not in schema["properties"]
    assert "not STT" in schema["properties"]["confidence"]["description"]


def test_artifact_operation_contract_narrows_topology_to_references_and_real_actions():
    selected = select_semantic_projection_details(projection(), ("workflow_automation:n8n",))
    selected["selection_artifact_operation_requirements"] = ({
        "requirement_id": "external_1", "goal_id": "g1", "operation_class": "PUBLISH",
        "source_grounding": "publish through Named Service", "provider_name": "Named Service",
        "provider_provenance": "SOURCE_EXPLICIT", "provider_inference_justification": "",
    },)
    schema = spine.request_understanding_schema_for_projection(
        selected, source_text="Create a workflow to publish through Named Service",
    )
    logical = schema["properties"]["operation_requirements"]["properties"]["create_workflow"][
        "properties"
    ]["logical_spec"]
    semantic = logical["properties"]["semantic_requirements"]
    assert semantic["minItems"] == semantic["maxItems"] == 1
    assert semantic["items"]["required"] == ["requirement_id", "step_id"]
    actions = {
        item["properties"]["action"]["const"]
        for item in logical["properties"]["steps"]["items"]["oneOf"]
    }
    assert "catalog_query" in actions
    assert "set_field" not in actions
    assert "transform" not in actions

    installed = select_semantic_projection_details(projection(), ("workflow_automation:n8n",))
    installed["selection_artifact_operation_requirements"] = ({
        "requirement_id": "fetch_1", "goal_id": "g1", "operation_class": "FETCH",
        "source_grounding": "download from Google Drive", "provider_name": "Google Drive",
        "provider_provenance": "SOURCE_EXPLICIT", "provider_inference_justification": "",
    },)
    installed_schema = spine.request_understanding_schema_for_projection(
        installed, source_text="Build a workflow to download from Google Drive",
    )
    installed_steps = installed_schema["properties"]["operation_requirements"]["properties"][
        "create_workflow"
    ]["properties"]["logical_spec"]["properties"]["steps"]["items"]["oneOf"]
    catalog_step = next(
        item for item in installed_steps
        if item["properties"]["action"].get("const") == "catalog_query"
    )
    assert "download" in catalog_step["properties"]["semantic_operation"]["enum"]
    assert catalog_step["properties"]["provider_name"]["enum"] == ["Google Drive"]
    installed_step_array = installed_schema["properties"]["operation_requirements"]["properties"][
        "create_workflow"
    ]["properties"]["logical_spec"]["properties"]["steps"]
    assert installed_step_array["minContains"] == installed_step_array["maxContains"] == 1


def test_understanding_required_capabilities_equals_final_selected_set_not_broad_pool():
    registry = projection()
    # The authoritative operation projection is the FINAL model-selected set, never the
    # broad candidate pool or a host-expanded union. The model-facing schema must not
    # expose a second capability-selection surface; the host hydrates the final set.
    selected = select_semantic_projection_details(registry, ("project.read", "runtime_history_store"))
    schema = spine.request_understanding_schema_for_projection(selected)
    assert "required_capabilities" not in schema["properties"]
    assert set(schema["properties"]["operation_requirements"]["required"]) == {
        item["operation_id"] for item in spine.load_operation_catalog(selected)
    }


def test_operation_discovery_catalog_exposes_required_parameters():
    registry = projection()
    selected = select_semantic_projection_details(registry, ("read_file_outline", "project.read"))
    system, _ = spine.build_operation_discovery_prompt(
        original_text="найди определение", session_context={}, registry_projection=selected,
    )
    assert "required_params" in system
    # read_file_outline carries a mandatory concrete target; project.read's search carries a query.
    catalog = json.loads(system.partition("CATALOG=")[2])
    legend = catalog["legend"]
    assert legend[6] == "required_params"
    by_op = {row[0]: row for row in catalog["rows"]}
    assert by_op["read_file_outline"][6] == ["path"]
    assert by_op["search"][6] == ["query"]
    assert by_op["inspect_structure"][6] == []
    system_prompt, _ = spine.build_request_understanding_prompt(
        request_id="request_operation_bound", original_text="проверь проект",
        identity=OWNER, session_context={}, registry_projection=selected,
    )
    assert "operation_requirements is an object keyed by every selected operation ID" in system_prompt


def test_conversation_manifest_describes_downstream_visible_response_not_tool_alternative():
    entry = next(
        item for item in projection()["entries"]
        if item["capability_id"] == "conversation.respond"
    )
    assert entry["semantic_description"].startswith("User-visible JARVIS reply for conversation")
    assert "conversation/social exchange" in entry["semantic_description"]
    assert "upstream EvidenceBundle" in entry["semantic_description"]
    assert "no evidence tools" in entry["semantic_description"]
    project = next(
        item for item in projection()["entries"]
        if item["capability_id"] == "project.read"
    )
    assert project["semantic_description"].startswith("Project worktree, Git, changed-file and diff")
    assert "never produces a user-visible response" in project["semantic_description"]


def test_candidate_prompt_keeps_evidence_collection_and_user_visible_response_distinct():
    registry = select_semantic_projection_details(
        projection(), ("conversation.respond", "project.read"),
    )
    system_prompt, _ = spine.build_candidate_discovery_prompt(
        original_text="Проверь проект и сообщи результат",
        session_context={},
        registry_projection=registry,
    )
    assert "RESPOND (conversation.respond) is mandatory when present" in system_prompt
    assert "RESPOND cannot supply OBSERVE/RETRIEVE evidence" in system_prompt
    assert "an evidence request with an answer needs both roles" in system_prompt
    assert "always select it for the visible answer" in system_prompt
    assert "MUST include conversation.respond" in system_prompt
    assert "User-visible JARVIS reply for conversation/social exchange" in system_prompt
    assert "Project worktree, Git, changed-file and diff" in system_prompt
    assert "no-change forbids MUTATE, not OBSERVE" in system_prompt
    assert "Do not mention a necessary ID only in reasons" in system_prompt
    assert "avoid redundant broad+narrow entries" in system_prompt
    assert "A confirmation or no-execution constraint never removes the requested capability" in system_prompt
    assert "let per-step policy block execution" in system_prompt
    assert "MUST include conversation.respond" in system_prompt
    assert "Return an empty object only when" not in system_prompt
    assert '"execution_contract"' in system_prompt
    assert '"authoritative_operation_ids"' not in system_prompt
    assert '"respond"' not in system_prompt
    assert '"inspect_git_status"' not in system_prompt

    memory_registry = select_semantic_projection_details(
        projection(), ("runtime_history_store",),
    )
    memory_prompt, _ = spine.build_candidate_discovery_prompt(
        original_text="прочитай ранее сохранённую историю",
        session_context={}, registry_projection=memory_registry,
    )
    assert "persisted conversation history" in memory_prompt
    assert "verified experiences" in memory_prompt
    assert "UNKNOWN availability defers to per-step runtime truth" in memory_prompt
    assert "Goals absent from this INDEX belong to another host pass" in memory_prompt
    assert "AVAILABLE plus execution_contract=true is executable" in memory_prompt
    assert "Do not call an AVAILABLE bound contract unavailable" in memory_prompt
    assert "RESPOND cannot substitute" in memory_prompt


def test_existing_executable_projection_uses_authoritative_operation_semantics():
    registry = projection()
    composite = next(
        item for item in registry["entries"]
        if item["capability_id"] == "build_project_workspace_read_model"
    )
    assert composite["semantic_description"].startswith("Read a broad composite project snapshot")
    assert "model and runtime status" in composite["semantic_description"]
    assert "Registered readonly_tool" not in composite["semantic_description"]
    status = next(
        item for item in registry["entries"]
        if item["capability_id"] == "status_tools"
    )
    assert "not a Git worktree or changed-file inspection" in status["semantic_description"]
    project = next(
        item for item in registry["entries"]
        if item["capability_id"] == "project.read"
    )
    assert project["semantic_description"].startswith("Project worktree, Git, changed-file and diff")


def test_understanding_prompt_requires_exact_operation_owner_capability_set():
    registry = select_semantic_projection_details(
        projection(), ("build_project_workspace_read_model", "status_tools"),
    )
    system_prompt, _ = spine.build_request_understanding_prompt(
        request_id="request_exact_operation_owners",
        original_text="Проверь состояние проекта без изменений",
        identity=OWNER,
        session_context={},
        registry_projection=registry,
    )
    assert "Operations and required executable capabilities must match exactly" in system_prompt
    assert "Top-level fields use maximum step severity" in system_prompt


def test_host_hydrates_mixed_top_level_severity_from_authoritative_operations():
    selected = select_semantic_projection_details(
        projection({"pc_executor_available": True}), ("read_screen", "type_text"),
    )
    catalog = spine.load_operation_catalog(selected)
    understanding = parse_request_understanding_payload({
        "schema_version": "request_understanding.v2", "language": "ru",
        "goals": [
            {"goal_id": "screen", "description": "capture screen"},
            {"goal_id": "typing", "description": "prepare typed input"},
        ],
        "required_capabilities": [
            {"capability_id": "read_screen", "purpose": "capture", "required": True},
            {"capability_id": "type_text", "purpose": "type", "required": True},
        ],
            "response_requirements": [],
        "effect_type": "OBSERVE", "target_scope": "owner_windows_screen",
        "reversibility": "REVERSIBLE", "external_side_effect": False,
        "unresolved_capabilities": [],
        "operation_requirements": {
            "observe_windows_screen": {}, "execute_type_text": {"text": "test"},
        },
        "current_topic": "mixed owner plan", "unresolved_reference": "",
        "risk_class": "READ_ONLY", "confidence": 1.0, "reason_codes": ["model_selected"],
    }, host_request_id="request_mixed", host_original_text="mixed request",
        authoritative_operation_catalog=catalog)
    assert understanding.effect_type == "MUTATE"
    assert understanding.risk_class == "DANGEROUS"
    assert understanding.reversibility == "IRREVERSIBLE"
    assert understanding.external_side_effect is True
    assert "host_hydrated_top_level_contract_aggregate" in understanding.reason_codes


def test_compact_candidate_index_exposes_authoritative_execution_as_json_boolean():
    registry = select_semantic_projection_details(
        projection(), ("repo_tree", "project.read"),
    )
    system_prompt, _ = spine.build_candidate_discovery_prompt(
        original_text="Проверь рабочее дерево без изменений",
        session_context={},
        registry_projection=registry,
    )
    payload = json.loads(system_prompt.split("INDEX=", 1)[1])
    assert payload["legend"][-1] == "execution_contract"
    rows = {row[0]: row for row in payload["rows"]}
    assert rows["repo_tree"][-1] is False
    assert rows["project.read"][-1] is True
    assert "exists" not in payload["legend"]


def test_compact_model_operation_selection_is_hydrated_only_from_authoritative_contract():
    registry = projection()
    selected = select_semantic_projection_details(registry, ("project.read",))
    full_catalog = tuple(spine.load_operation_catalog(selected))
    catalog = tuple(
        item for item in full_catalog if item["operation_id"] == "inspect_git_status"
    )
    payload = {
        "schema_version": "request_understanding.v2",
        "language": "ru",
        "goals": [{"goal_id": "g1", "description": "Проверить состояние проекта"}],
        "required_capabilities": [{
            "capability_id": "project.read",
            "purpose": "Прочитать состояние проекта",
            "required": True,
        }],
            "response_requirements": [],
        "effect_type": "OBSERVE",
        "target_scope": "local_project_worktree",
        "reversibility": "REVERSIBLE",
        "external_side_effect": False,
        "unresolved_capabilities": [],
        "operation_requirements": {"inspect_git_status": {}},
        "current_topic": "состояние проекта",
        "unresolved_reference": "",
        "risk_class": "READ_ONLY",
        "confidence": .98,
        "reason_codes": ["semantic_project_state"],
    }
    parsed = __import__(
        "MAKSIMAR_CORE_LIB.ai_orchestration.helper_model_decision_parser",
        fromlist=["parse_request_understanding_payload"],
    ).parse_request_understanding_payload(
        payload,
        host_request_id="request_compact_operation",
        host_original_text="проверь проект",
        authoritative_operation_catalog=catalog,
    )
    operation = parsed.operation_requirements[0]
    contract = next(item for item in catalog if item["operation_id"] == "inspect_git_status")
    assert parsed.required_capabilities[0].operation_contract_required is True
    assert parsed.required_capabilities[0].unresolved_operation_reason == ""
    assert operation.required_evidence == tuple(contract["evidence_kinds"])
    assert operation.effect_type == contract["effect_type"]
    assert operation.risk_class == contract["risk_class"]
    assert operation.parameters == ()
    carried = json.loads(json.dumps(payload))
    carried["operation_requirements"] = {}
    with pytest.raises(ValueError, match="parameter IDs must exactly match"):
        __import__(
            "MAKSIMAR_CORE_LIB.ai_orchestration.helper_model_decision_parser",
            fromlist=["parse_request_understanding_payload"],
        ).parse_request_understanding_payload(
            carried,
            host_request_id="request_carried_operations",
            host_original_text="проверь проект",
            authoritative_operation_catalog=catalog,
        )
    forged = json.loads(json.dumps(payload))
    forged["operation_requirements"]["inspect_git_status"] = {"path": "invented"}
    with pytest.raises(ValueError, match="parameters must exactly match"):
        __import__(
            "MAKSIMAR_CORE_LIB.ai_orchestration.helper_model_decision_parser",
            fromlist=["parse_request_understanding_payload"],
        ).parse_request_understanding_payload(
            forged,
            host_request_id="request_forged_operation",
            host_original_text="проверь проект",
            authoritative_operation_catalog=catalog,
        )

    consideration_only = json.loads(json.dumps(payload))
    consideration_only["required_capabilities"][0]["operation_contract_required"] = False
    with pytest.raises(
        ValueError,
        match="required capability fields must exactly match canonical model contract",
    ):
        __import__(
            "MAKSIMAR_CORE_LIB.ai_orchestration.helper_model_decision_parser",
            fromlist=["parse_request_understanding_payload"],
        ).parse_request_understanding_payload(
            consideration_only,
            host_request_id="request_consideration_only",
            host_original_text="проверь проект",
            authoritative_operation_catalog=catalog,
        )


def test_typed_operation_parameters_are_model_supplied_then_host_hydrated_and_executed(monkeypatch):
    registry = projection()
    selected = select_semantic_projection_details(registry, ("read_file_snippet",))
    catalog = tuple(spine.load_operation_catalog(selected))
    assert len(catalog) == 1
    schema = spine.request_understanding_schema_for_projection(selected)
    parameter_schema = schema["properties"]["operation_requirements"]["properties"]["read_file_snippet"]
    assert parameter_schema["required"] == ["path"]
    assert parameter_schema["additionalProperties"] is False

    payload = {
        "schema_version": "request_understanding.v2",
        "language": "ru",
        "goals": [{"goal_id": "g1", "description": "Прочитать начало указанного файла"}],
        "required_capabilities": [{
            "capability_id": "read_file_snippet",
            "purpose": "Прочитать точный файл",
            "required": True,
        }],
            "response_requirements": [],
        "effect_type": "OBSERVE",
        "target_scope": "local_project_worktree",
        "reversibility": "REVERSIBLE",
        "external_side_effect": False,
        "unresolved_capabilities": [],
        "operation_requirements": {
            "read_file_snippet": {"path": "AGENTS.md"},
        },
        "current_topic": "project file",
        "unresolved_reference": "",
        "risk_class": "READ_ONLY",
        "confidence": .99,
        "reason_codes": ["typed_file_target"],
    }
    understanding = parse_request_understanding_payload(
        payload,
        host_request_id="request_typed_path",
        host_original_text="Покажи начало файла с инструкциями агентов",
        authoritative_operation_catalog=catalog,
    )
    requirement = understanding.operation_requirements[0]
    assert requirement.parameters == (("path", "AGENTS.md"),)
    assert requirement.effect_type == catalog[0]["effect_type"]

    observed = {}
    monkeypatch.setattr(
        "MAKSIMAR_SERVER.AI_ORCHESTRATION.project_understanding_adapter.read_file_snippet",
        lambda path: observed.setdefault("path", path) or {"path": path},
    )
    step = PlanStep(
        step_id="step_typed_path",
        goal_id="g1",
        capability_id="read_file_snippet",
        operation="read_file_snippet",
        required_evidence=tuple(catalog[0]["evidence_kinds"]),
        effect_type=str(catalog[0]["effect_type"]),
        target_scope=str(catalog[0]["target_scope"]),
        reversibility=str(catalog[0]["reversibility"]),
        external_side_effect=False,
        risk_class=str(catalog[0]["risk_class"]),
        parameters=requirement.parameters,
    )
    bundle = ExistingProjectUnderstandingAdapter().collect_evidence(
        understanding,
        ExecutionPlan(request_id=understanding.request_id, steps=(step,)),
        "trace_typed_path",
    )
    assert observed["path"] == "AGENTS.md"
    assert bundle.status == "COMPLETE"
    assert bundle.receipts[0].capability_id == "read_file_snippet"
    assert bundle.receipts[0].step_id == "step_typed_path"


def test_project_provider_failure_payload_cannot_create_complete_evidence_or_receipt(monkeypatch):
    selected = select_semantic_projection_details(projection(), ("read_file_outline",))
    catalog = tuple(spine.load_operation_catalog(selected))
    understanding = parse_request_understanding_payload(
        {
            "schema_version": "request_understanding.v2",
            "language": "ru",
            "goals": [{"goal_id": "g1", "description": "Прочитать outline"}],
            "required_capabilities": [{
                "capability_id": "read_file_outline", "purpose": "read", "required": True,
            }],
            "response_requirements": [],
            "effect_type": "OBSERVE", "target_scope": "local_project_worktree",
            "reversibility": "REVERSIBLE", "external_side_effect": False,
            "unresolved_capabilities": [],
            "operation_requirements": {"read_file_outline": {"path": "missing.py"}},
            "current_topic": "project file", "unresolved_reference": "",
            "risk_class": "READ_ONLY", "confidence": .99,
            "reason_codes": ["typed_missing_path"],
        },
        host_request_id="request_failed_outline",
        host_original_text="Покажи outline отсутствующего файла",
        authoritative_operation_catalog=catalog,
    )
    operation = catalog[0]
    step = PlanStep(
        step_id="step_failed_outline", goal_id="g1",
        capability_id="read_file_outline", operation="read_file_outline",
        required_evidence=tuple(operation["evidence_kinds"]),
        effect_type=str(operation["effect_type"]), target_scope=str(operation["target_scope"]),
        reversibility=str(operation["reversibility"]), external_side_effect=False,
        risk_class=str(operation["risk_class"]), parameters=understanding.operation_requirements[0].parameters,
    )
    monkeypatch.setattr(
        "MAKSIMAR_SERVER.AI_ORCHESTRATION.project_understanding_adapter.read_file_outline",
        lambda path: {"path": path, "allowed": False, "error": "file_not_found", "read_only": True},
    )

    bundle = ExistingProjectUnderstandingAdapter().collect_evidence(
        understanding, ExecutionPlan(request_id=understanding.request_id, steps=(step,)),
        "trace_failed_outline",
    )

    assert bundle.status == "UNAVAILABLE"
    assert bundle.items == ()
    assert bundle.errors == ("read_file_outline:file_not_found",)
    assert len(bundle.receipts) == 1
    assert bundle.receipts[0].status == "FAILED"


def test_project_search_ranks_real_symbol_declaration_before_references():
    ranked = project_tools._rank_repo_search_results("EvidenceBundle", [
        {"path": "./docs/readme.md", "line_number": 1, "line": "EvidenceBundle is used here"},
        {"path": "./tests/test_contract.py", "line_number": 2, "line": "class EvidenceBundle:"},
        {
            "path": "./MAKSIMAR_CORE_LIB/ai_orchestration/semantic_intent_contract.py",
            "line_number": 456, "line": "class EvidenceBundle:",
        },
        {"path": "./CONTROL_PLANE/canonical_semantic_spine.py", "line_number": 29,
         "line": "EvidenceBundle,"},
    ])

    assert ranked[0] == {
        "path": "./MAKSIMAR_CORE_LIB/ai_orchestration/semantic_intent_contract.py",
        "line_number": 456, "line": "class EvidenceBundle:",
    }
    assert ranked[1]["path"] == "./tests/test_contract.py"


def test_missing_or_extra_typed_operation_parameters_fail_closed():
    selected = select_semantic_projection_details(projection(), ("read_file_snippet",))
    catalog = tuple(spine.load_operation_catalog(selected))
    base = {
        "schema_version": "request_understanding.v2",
        "language": "ru",
        "goals": [{"goal_id": "g1", "description": "Прочитать файл"}],
        "required_capabilities": [{
            "capability_id": "read_file_snippet", "purpose": "read", "required": True,
        }],
            "response_requirements": [],
        "effect_type": "OBSERVE", "target_scope": "local_project_worktree",
        "reversibility": "REVERSIBLE", "external_side_effect": False,
        "unresolved_capabilities": [], "current_topic": "file",
        "unresolved_reference": "", "risk_class": "READ_ONLY",
        "confidence": .9, "reason_codes": ["typed_file_target"],
    }
    for parameters in ({}, {"path": "AGENTS.md", "query": "extra"}):
        payload = dict(base)
        payload["operation_requirements"] = {"read_file_snippet": parameters}
        with pytest.raises(ValueError, match="parameters must exactly match"):
            parse_request_understanding_payload(
                payload,
                host_request_id="request_invalid_parameters",
                host_original_text="прочти файл",
                authoritative_operation_catalog=catalog,
            )


@pytest.mark.parametrize(("capability_id", "operation_id", "evidence_kind"), (
    ("qdrant_readonly_status", "read_qdrant_readonly_status", "qdrant_readonly_status"),
    ("retrieval_backend_status_read_model", "read_retrieval_backend_status", "retrieval_backend_status"),
    ("jarvis_runtime_library:agents", "read_runtime_library_agents", "runtime_library_agents"),
    ("jarvis_runtime_library:skills", "read_runtime_library_skills", "runtime_library_skills"),
    ("jarvis_runtime_library:tools", "read_runtime_library_tools", "runtime_library_tools"),
    ("jarvis_runtime_library:manifests", "read_runtime_library_manifests", "runtime_library_manifests"),
    ("runtime_tooling:flutter", "read_flutter_runtime_status", "flutter_runtime_status"),
))
def test_existing_project_owner_executes_remaining_local_read_operations(
    capability_id, operation_id, evidence_kind,
):
    selected = select_semantic_projection_details(projection(), (capability_id,))
    catalog = tuple(spine.load_operation_catalog(selected))
    operation = next(item for item in catalog if item["operation_id"] == operation_id)
    understanding = parse_request_understanding_payload(
        {
            "schema_version": "request_understanding.v2",
            "language": "ru",
            "goals": [{"goal_id": "g1", "description": "Прочитать локальный статус"}],
            "required_capabilities": [{
                "capability_id": capability_id, "purpose": "read status", "required": True,
            }],
            "response_requirements": [],
            "effect_type": operation["effect_type"],
            "target_scope": operation["target_scope"],
            "reversibility": operation["reversibility"],
            "external_side_effect": False,
            "unresolved_capabilities": [],
            "operation_requirements": {operation_id: {}},
            "current_topic": "local retrieval status",
            "unresolved_reference": "",
            "risk_class": operation["risk_class"],
            "confidence": .99,
            "reason_codes": ["typed_readonly_status"],
        },
        host_request_id="request_" + capability_id,
        host_original_text="Проверь локальный статус retrieval backend",
        authoritative_operation_catalog=catalog,
    )
    step = PlanStep(
        step_id="step_" + capability_id,
        goal_id="g1",
        capability_id=capability_id,
        operation=operation_id,
        required_evidence=tuple(operation["evidence_kinds"]),
        effect_type=str(operation["effect_type"]),
        target_scope=str(operation["target_scope"]),
        reversibility=str(operation["reversibility"]),
        external_side_effect=False,
        risk_class=str(operation["risk_class"]),
        parameters=(),
    )
    bundle = ExistingProjectUnderstandingAdapter().collect_evidence(
        understanding,
        ExecutionPlan(request_id=understanding.request_id, steps=(step,)),
        "trace_" + capability_id,
    )
    assert bundle.status == "COMPLETE"
    assert tuple(item.kind for item in bundle.items) == (evidence_kind,)
    assert bundle.receipts[0].capability_id == capability_id
    assert bundle.receipts[0].operation_id == operation_id


def test_operation_selection_continuation_is_host_owned_and_has_no_four_operation_ceiling():
    selected = select_semantic_projection_details(projection(), ("project.read",))
    allowed = tuple(item["operation_id"] for item in spine.load_operation_catalog(selected))[:8]
    calls = []

    def discover(**kwargs):
        prior_count = int(json.loads(kwargs["user_prompt"])["prior_selection_count"])
        batch = allowed[prior_count:prior_count + spine.DISCOVERY_VALUES_PER_PASS]
        calls.append(prior_count)
        return model_call_envelope(json.dumps({
            "candidate_operation_ids": {operation_id: True for operation_id in batch},
            "selection_justifications": {operation_id: {
                "goal_id": "g1",
                "justification_kind": "DIRECT_GOAL_EFFECT",
                "source_grounding": "проверь несколько аспектов проекта",
            } for operation_id in batch},
            "continuation_required": prior_count + len(batch) < len(allowed),
            "continuation_reason": (
                "distinct unmet explicit goal" if prior_count + len(batch) < len(allowed) else ""
            ),
            "ambiguity_present": False, "confidence": .98,
            "reason_codes": ["semantic_operation_discovery"],
        }))

    trace = []
    operation_ids = spine._run_discovery_continuation(
        call=discover, prompt_builder=spine.build_operation_discovery_prompt,
        value_key="candidate_operation_ids", allowed_values=allowed,
        original_text="проверь несколько аспектов проекта", session_context={},
        registry_projection=selected, deadline=RequestDeadline(30),
        output_schema=spine.OPERATION_DISCOVERY_JSON_SCHEMA, trace=trace,
    )
    assert len(operation_ids) > spine.DISCOVERY_VALUES_PER_PASS
    assert len(operation_ids) == len(set(operation_ids))
    assert calls == [0, 4]


def _discovery_operation_ids(count):
    selected = select_semantic_projection_details(projection(), ("project.read",))
    return tuple(item["operation_id"] for item in spine.load_operation_catalog(selected))[:count]


def test_continuation_allows_partial_pass_then_new_id_next_pass():
    # Continuation is bounded transport, not a demand to fill the pass to maximum capacity.
    allowed = _discovery_operation_ids(6)
    calls = []

    def discover(**kwargs):
        prior = int(json.loads(kwargs["user_prompt"])["prior_selection_count"])
        if prior == 0:
            batch = allowed[:2]  # under-filled pass
            cont = True
        else:
            batch = allowed[prior:prior + 1]
            cont = False
        calls.append(prior)
        return model_call_envelope(json.dumps({
            "candidate_operation_ids": {op: True for op in batch},
            "selection_justifications": {op: {
                "goal_id": "g1",
                "justification_kind": "DIRECT_GOAL_EFFECT", "source_grounding": "проверь проект",
            } for op in batch},
            "continuation_required": cont,
            "continuation_reason": "distinct unmet goal" if cont else "",
            "ambiguity_present": False, "confidence": 0.98,
            "reason_codes": ["semantic_operation_discovery"],
        }))

    trace = []
    ids = spine._run_discovery_continuation(
        call=discover, prompt_builder=spine.build_operation_discovery_prompt,
        value_key="candidate_operation_ids", allowed_values=allowed,
        original_text="проверь проект", session_context={},
        registry_projection=select_semantic_projection_details(projection(), ("project.read",)),
        deadline=RequestDeadline(30),
        output_schema=spine.OPERATION_DISCOVERY_JSON_SCHEMA, trace=trace,
    )
    assert ids == allowed[:3]
    assert calls == [0, 2]


def test_continuation_zero_new_ids_fails_closed():
    payload = {
        "candidate_kinds": {},
        "continuation_required": True,
        "continuation_reason": "more distinct goals",
        "ambiguity_present": False,
        "confidence": 0.9,
        "reason_codes": ["semantic_kind_discovery"],
    }
    with pytest.raises(ValueError, match="at least one new ID"):
        parse_discovery_selection_payload(
            payload, value_key="candidate_kinds",
            allowed_values=("kind_a", "kind_b"), max_values_per_pass=4,
        )


def test_continuation_duplicate_ids_in_pass_fail_closed():
    payload = {
        "candidate_kinds": ["kind_a", "kind_a"],
        "continuation_required": True,
        "continuation_reason": "more",
        "ambiguity_present": False,
        "confidence": 0.9,
        "reason_codes": ["semantic_continuation"],
    }
    with pytest.raises(ValueError, match="duplicate"):
        parse_discovery_selection_payload(
            payload, value_key="candidate_kinds",
            allowed_values=("kind_a", "kind_b"), max_values_per_pass=4,
        )


def test_continuation_unknown_id_fails_closed():
    payload = {
        "candidate_kinds": ["unknown_kind"],
        "continuation_required": False,
        "continuation_reason": "",
        "ambiguity_present": False,
        "confidence": 0.9,
        "reason_codes": ["semantic_continuation"],
    }
    with pytest.raises(ValueError, match="unregistered"):
        parse_discovery_selection_payload(
            payload, value_key="candidate_kinds",
            allowed_values=("kind_a", "kind_b"), max_values_per_pass=4,
        )


def test_continuation_repeated_prior_id_fails_closed():
    allowed = _discovery_operation_ids(6)

    def discover(**kwargs):
        return model_call_envelope(json.dumps({
            "candidate_operation_ids": {allowed[0]: True},
            "selection_justifications": {allowed[0]: {
                "goal_id": "g1",
                "justification_kind": "DIRECT_GOAL_EFFECT", "source_grounding": "проверь проект",
            }},
            "continuation_required": True,
            "continuation_reason": "unmet goal",
            "ambiguity_present": False, "confidence": 0.9,
            "reason_codes": ["semantic_continuation"],
        }))

    trace = []
    with pytest.raises(ValueError, match="repeats canonical state"):
        spine._run_discovery_continuation(
            call=discover, prompt_builder=spine.build_operation_discovery_prompt,
            value_key="candidate_operation_ids", allowed_values=allowed,
            original_text="проверь проект", session_context={},
            registry_projection=select_semantic_projection_details(projection(), ("project.read",)),
            deadline=RequestDeadline(30),
            output_schema=spine.OPERATION_DISCOVERY_JSON_SCHEMA, trace=trace,
        )


def test_continuation_bounded_maximum_respected():
    allowed = _discovery_operation_ids(3)

    def discover(**kwargs):
        prior = int(json.loads(kwargs["user_prompt"])["prior_selection_count"])
        return model_call_envelope(json.dumps({
            "candidate_operation_ids": {allowed[prior]: True},
            "selection_justifications": {allowed[prior]: {
                "goal_id": "g1",
                "justification_kind": "DIRECT_GOAL_EFFECT", "source_grounding": "проверь проект",
            }},
            "continuation_required": True,
            "continuation_reason": "unmet goal",
            "ambiguity_present": False, "confidence": 0.9,
            "reason_codes": ["semantic_continuation"],
        }))

    trace = []
    with pytest.raises(ValueError, match="exhausted_without_completion|progress_guard_exceeded"):
        spine._run_discovery_continuation(
            call=discover, prompt_builder=spine.build_operation_discovery_prompt,
            value_key="candidate_operation_ids", allowed_values=allowed,
            original_text="проверь проект", session_context={},
            registry_projection=select_semantic_projection_details(projection(), ("project.read",)),
            deadline=RequestDeadline(30),
            output_schema=spine.OPERATION_DISCOVERY_JSON_SCHEMA, trace=trace,
        )


def test_continuation_final_union_contains_only_model_selected_ids():
    allowed = _discovery_operation_ids(6)

    def discover(**kwargs):
        prior = int(json.loads(kwargs["user_prompt"])["prior_selection_count"])
        batch = allowed[prior:prior + 2]
        cont = prior + len(batch) < 4
        return model_call_envelope(json.dumps({
            "candidate_operation_ids": {op: True for op in batch},
            "selection_justifications": {op: {
                "goal_id": "g1",
                "justification_kind": "DIRECT_GOAL_EFFECT", "source_grounding": "проверь проект",
            } for op in batch},
            "continuation_required": cont,
            "continuation_reason": "unmet goal" if cont else "",
            "ambiguity_present": False, "confidence": 0.9,
            "reason_codes": ["semantic_continuation"],
        }))

    trace = []
    ids = spine._run_discovery_continuation(
        call=discover, prompt_builder=spine.build_operation_discovery_prompt,
        value_key="candidate_operation_ids", allowed_values=allowed,
        original_text="проверь проект", session_context={},
        registry_projection=select_semantic_projection_details(projection(), ("project.read",)),
        deadline=RequestDeadline(30),
        output_schema=spine.OPERATION_DISCOVERY_JSON_SCHEMA, trace=trace,
    )
    assert ids == tuple(dict.fromkeys(allowed[:4]))
    assert set(ids) <= set(allowed)
    assert len(ids) == len(set(ids))


def _candidate_response_projection():
    return select_semantic_projection_details(projection(), ("conversation.respond", "project.read"))


def _omitting_response_discover(**kwargs):
    return model_call_envelope(json.dumps({
        "candidate_capability_ids": {"project.read": True},
        "continuation_required": False,
        "continuation_reason": "",
        "ambiguity_present": False, "confidence": 0.9,
        "reason_codes": ["semantic_candidate_discovery"],
    }))


def test_response_preservation_requires_prior_authoritative_selection():
    selected = _candidate_response_projection()
    allowed = tuple(item["capability_id"] for item in selected["entries"])
    ids = spine._run_discovery_continuation(
        call=_omitting_response_discover, prompt_builder=spine.build_candidate_discovery_prompt,
        value_key="candidate_capability_ids", allowed_values=allowed,
        original_text="посмотри проект", session_context={},
        registry_projection=selected, deadline=RequestDeadline(30),
        output_schema=spine.CANDIDATE_DISCOVERY_JSON_SCHEMA, trace=[],
        prior_model_selected_ids=("conversation.respond",),
    )
    assert set(ids) == {"project.read", "conversation.respond"}


def test_response_omission_fails_closed_without_prior_selection():
    # conversation.respond is in the allowed scope but was never model-selected in a prior
    # authoritative pass; presence in allowed scope alone is NOT provenance.
    selected = _candidate_response_projection()
    allowed = tuple(item["capability_id"] for item in selected["entries"])
    with pytest.raises(ValueError, match="omitted canonical response"):
        spine._run_discovery_continuation(
            call=_omitting_response_discover, prompt_builder=spine.build_candidate_discovery_prompt,
            value_key="candidate_capability_ids", allowed_values=allowed,
            original_text="посмотри проект", session_context={},
            registry_projection=selected, deadline=RequestDeadline(30),
            output_schema=spine.CANDIDATE_DISCOVERY_JSON_SCHEMA, trace=[],
        )


def test_response_preservation_records_provenance_in_audit():
    selected = _candidate_response_projection()
    allowed = tuple(item["capability_id"] for item in selected["entries"])
    audit: list = []
    spine._run_discovery_continuation(
        call=_omitting_response_discover, prompt_builder=spine.build_candidate_discovery_prompt,
        value_key="candidate_capability_ids", allowed_values=allowed,
        original_text="посмотри проект", session_context={},
        registry_projection=selected, deadline=RequestDeadline(30),
        output_schema=spine.CANDIDATE_DISCOVERY_JSON_SCHEMA, trace=[],
        audit_trace=audit, prior_model_selected_ids=("conversation.respond",),
    )
    assert any(a.get("response_preserved") is True for a in audit)
    assert any(
        a.get("response_preservation_provenance") == ("conversation.respond",)
        for a in audit
    )


def test_simulation_iteration_budget_normalization_extracts_single_token():
    from MAKSIMAR_SERVER.AI_ORCHESTRATION import simulation_worker_adapter
    assert simulation_worker_adapter._coerce_positive_int("8") == 8
    assert simulation_worker_adapter._coerce_positive_int("user specified: 8") == 8
    assert simulation_worker_adapter._coerce_positive_int("8 iterations") == 8
    # zero tokens (placeholder) -> None (runtime default, never fabricated)
    assert simulation_worker_adapter._coerce_positive_int("") is None
    assert simulation_worker_adapter._coerce_positive_int("user_defined") is None
    assert simulation_worker_adapter._coerce_positive_int("no number") is None
    # multiple distinct numeric groups -> None (ambiguous, no concatenation)
    assert simulation_worker_adapter._coerce_positive_int("8 to 10") is None
    assert simulation_worker_adapter._coerce_positive_int("v2, 8 iterations") is None


def test_operation_discovery_slots_are_bounded_by_typed_goal_capability_justifications():
    selected = select_semantic_projection_details(projection(), ("project.read",))
    selected["selection_goalframes"] = ({
        "goal_id": "g1", "goal_role": "PRIMARY_OUTCOME", "effect_intent": "observe",
        "grounding": "проанализируй несколько аспектов проекта",
    },)
    selected["selection_capability_justifications"] = ({
        "goal_id": "g1", "capability_id": "project.read",
        "justification_kind": "PRIMARY_OUTCOME",
        "source_grounding": "проанализируй несколько аспектов проекта",
    },)
    calls = []

    class SlotModel:
        supports_call_scoped_understanding_schema = True

        def discover_candidates(self, **kwargs):
            selection_schema = kwargs["output_schema"]["properties"]["candidate_operation_ids"]
            slot_names = tuple(selection_schema["properties"])
            allowed = tuple(selection_schema["properties"])
            calls.append((slot_names, allowed, selection_schema))
            return model_call_envelope(json.dumps({
                "candidate_operation_ids": {allowed[0]: True},
                "selection_justifications": {allowed[0]: {
                    "goal_id": "g1",
                    "justification_kind": "DIRECT_GOAL_EFFECT",
                    "source_grounding": "проанализируй несколько аспектов проекта",
                }},
                "continuation_required": False,
                "continuation_reason": "",
                "ambiguity_present": False,
                "confidence": .98,
                "reason_codes": ["semantic_operation_selection"],
            }))

    audit = {}
    details = spine._model_selected_operation_details(
        model_port=SlotModel(), deadline=RequestDeadline(30),
        original_text="проанализируй несколько аспектов проекта",
        session_context={}, registry_projection=selected, audit_trace=audit,
    )

    assert details is not None
    assert calls[0][0] == calls[0][1]
    assert len(calls[0][1]) == 10
    assert calls[0][2]["maxProperties"] == 1
    assert len(audit["operation_discovery"]["candidate_operation_ids"]) == 1
    assert audit["operation_discovery"]["strategy"] == "UNIQUE_TYPED_KEYS_WITH_HOST_CONTINUATION"


def test_single_authoritative_operation_does_not_repeat_semantic_model_selection():
    selected = select_semantic_projection_details(projection(), ("conversation.respond",))

    class MustNotBeCalled:
        supports_call_scoped_understanding_schema = True

        def discover_candidates(self, **kwargs):
            del kwargs
            raise AssertionError("singleton operation discovery must not call the model")

    audit = {}
    details = spine._model_selected_operation_details(
        model_port=MustNotBeCalled(), deadline=RequestDeadline(30),
        original_text="ответь естественно", session_context={},
        registry_projection=selected, audit_trace=audit,
    )

    assert details is not None
    assert tuple(item["capability_id"] for item in details["entries"]) == ("conversation.respond",)
    assert tuple(
        operation["operation_id"]
        for operation in details["entries"][0]["operation_contracts"]
    ) == ("respond",)
    assert audit["operation_discovery"] == {
        "status": "NOT_REQUIRED_SINGLE_AUTHORITATIVE_OPERATION",
        "candidate_operation_ids": ("respond",),
        "strategy": "AUTHORITATIVE_REGISTRY_SINGLETON",
        "selection_justifications": ({
            "capability_id": "conversation.respond", "operation_id": "respond",
            "justification_kind": "ONLY_OPERATION_FOR_JUSTIFIED_CAPABILITY",
        },),
        "unjustified_operations": (),
        "schema_valid": True,
    }


def test_operation_discovery_drops_unselected_executable_candidate_without_reclassifying_it():
    selected = select_semantic_projection_details(
        projection(), ("project.read", "project_codegraph_readonly"),
    )

    class OperationModel:
        supports_call_scoped_understanding_schema = True

        def discover_candidates(self, **kwargs):
            slots = tuple(
                kwargs["output_schema"]["properties"]["candidate_operation_ids"]["properties"]
            )
            return model_call_envelope(json.dumps({
                "candidate_operation_ids": {"inspect_git_status": True},
                "selection_justifications": {"inspect_git_status": {
                    "goal_id": "g1",
                    "justification_kind": "DIRECT_GOAL_EFFECT",
                    "source_grounding": "Проверь состояние рабочего дерева",
                }},
                "continuation_required": False,
                "continuation_reason": "",
                "ambiguity_present": False,
                "confidence": .99,
                "reason_codes": ["exact_operation_sufficient"],
            }))

    result = spine._model_selected_operation_details(
        model_port=OperationModel(),
        deadline=RequestDeadline(30),
        original_text="Проверь состояние рабочего дерева",
        session_context={},
        registry_projection=selected,
        audit_trace={},
    )
    assert result is not None
    assert tuple(item["capability_id"] for item in result["entries"]) == ("project.read",)
    assert result["entries"][0]["selection_mode"] == "EXECUTABLE"
    assert tuple(
        item["operation_id"] for item in result["entries"][0]["operation_contracts"]
    ) == ("inspect_git_status",)


def test_semantic_prompt_does_not_expose_numeric_stt_confidence_as_semantic_confidence():
    selected = select_semantic_projection_details(projection(), ("project.read",))
    _, user_prompt = spine.build_request_understanding_prompt(
        request_id="request_stt_truth", original_text="шумный но понятный запрос",
        identity=OWNER, session_context={},
        input_preparation={
            "input_channel": "stt",
            "input_quality_metadata": {"stt_confidence": .61, "correction_requested": True},
        },
        registry_projection=selected,
    )
    supplied = json.loads(user_prompt)
    assert supplied["input_preparation"]["input_channel"] == "stt"
    assert supplied["input_preparation"]["input_quality_metadata"] == {
        "correction_requested": True,
    }
    assert "0.61" not in user_prompt


def test_truncated_model_output_fails_before_strict_semantic_parsing():
    result = model_call_envelope('{"schema_version":"request_understanding.v2"')
    result.update({"truncation": True, "done_reason": "length"})
    assert spine._model_call_verification_error(result) == "model_output_truncated"


def test_windows_edge_installed_is_not_live_availability():
    registry = projection({"pc_executor_available": False, "ollama_alive": True})
    edge = next(item for item in registry["entries"] if item["capability_id"] == "runtime_windows_edge")
    assert edge["capability_exists"] is True
    assert edge["adapter_installed"] is True
    assert edge["provider_exists"] is True
    assert edge["provider_available"] is False
    assert edge["availability_status"] == "UNAVAILABLE"
    assert edge["execution_contract_available"] is True
    assert edge["operation_contracts"][0]["operation_id"] == "read_windows_edge_status"
    assert edge["executed"] is False and edge["execution_receipt_present"] is False


@pytest.mark.parametrize("capability_id", [
    "repo_git_status", "history_query", "mgrep_readonly",
    "worker_ai_001", "architect_agent",
    "external_adapter:smolagents", "model_role:jarvis_chat_model",
])
def test_model_selected_full_world_capability_remains_visible_without_fake_operation(capability_id):
    result = run_selection((capability_id,))
    assert result["selected_capabilities"] == (capability_id, "conversation.respond")
    assert result["selection_source"] == "model_semantic_registry"
    assert result["operation_status"] == "UNRESOLVED_OPERATION"
    assert result["execution_plan"] is None  # no fake operation plan for unresolved visibility-only


def test_model_selected_multiple_visibility_only_tools_do_not_invent_plan():
    result = run_selection(("repo_git_status", "repo_search"))
    assert result["selected_capabilities"] == (
        "repo_git_status", "repo_search", "conversation.respond",
    )
    assert result["operation_status"] == "UNRESOLVED_OPERATION"
    assert result["execution_plan"] is None  # no fake operation plan for unresolved visibility-only


def test_two_bound_providers_have_isolated_step_receipts():
    result = run_selection(("conversation.respond", "project.read"))
    assert result["operation_status"] == "FINAL_BRAIN_PENDING"
    truths = {item["capability_id"]: item for item in result["capability_truth"]}
    assert truths["conversation.respond"]["executed"] is False
    assert truths["conversation.respond"]["execution_receipt_present"] is False
    assert truths["project.read"]["executed"] is True
    project_step = truths["project.read"]["step_execution_truth"][0]
    assert project_step["provider_id"] == "existing_project_workspace_tools"
    receipts = result["evidence_bundle"]["receipts"]
    assert {item["step_id"] for item in receipts} == {project_step["step_id"]}


def test_final_brain_response_step_is_preserved_from_model_semantic_selection():
    result = run_selection(("project.read",))
    assert result["selected_capabilities"] == ("project.read", "conversation.respond")
    assert result["candidate_discovery"]["candidate_capability_ids"] == (
        "project.read", "conversation.respond",
    )
    assert result["operation_status"] == "FINAL_BRAIN_PENDING"
    steps = result["execution_plan"]["steps"]
    response_steps = [
        step for step in steps
        if step["capability_id"] == "conversation.respond" and step["operation"] == "respond"
    ]
    assert len(response_steps) == 1
    truths = {item["capability_id"]: item for item in result["capability_truth"]}
    assert truths["project.read"]["executed"] is True
    assert truths["conversation.respond"]["executed"] is False
    assert truths["conversation.respond"]["execution_receipt_present"] is False
    assert not any(
        receipt["capability_id"] == "conversation.respond"
        for receipt in result["evidence_bundle"]["receipts"]
    )


def test_one_bounded_turn_deadline_owner_leaves_room_for_hierarchical_discovery_and_final_brain():
    public_default = inspect.signature(
        spine.run_canonical_semantic_turn,
    ).parameters["total_timeout_seconds"].default
    internal_default = inspect.signature(
        spine._run_canonical_semantic_turn_after_input,
    ).parameters["total_timeout_seconds"].default
    assert public_default == internal_default == spine.CANONICAL_TURN_TIMEOUT_SECONDS
    assert 180 < spine.CANONICAL_TURN_TIMEOUT_SECONDS <= 600


def test_read_only_execution_receipt_is_not_shared_with_approval_step():
    registry = projection()
    for item in registry["entries"]:
        if item["capability_id"] in {"conversation.respond", "project.read"}:
            item["provider_available"] = True

    class IsolatedPolicy:
        def evaluate(self, **kwargs):
            approval = kwargs["capability_id"] == "conversation.respond"
            return PermissionDecision(
                granted=not approval, capability_id=kwargs["capability_id"],
                identity_source=kwargs["identity"].identity_source, policy_version="test_isolated_step_policy",
                denial_reason="approval required" if approval else "", trace_id=kwargs["trace_id"],
                operation_id=kwargs["operation_id"], approval_required=approval,
            )

    result = spine.run_canonical_semantic_turn(
        text="two typed steps", project_port=EvidencePort("existing_project_workspace_tools"),
        conversation_port=EvidencePort("existing_jarvis_final_brain"),
        model_port=Model(registry, ("project.read", "conversation.respond")), final_brain_port=Final(),
        permission_port=IsolatedPolicy(), identity=OWNER, registry_projection=registry,
        provider_ports={
            "existing_project_workspace_tools": EvidencePort("existing_project_workspace_tools"),
            "existing_jarvis_final_brain": EvidencePort("existing_jarvis_final_brain"),
        }, defer_final_brain=True,
    )
    truths = {item["capability_id"]: item for item in result["capability_truth"]}
    assert truths["project.read"]["executed"] is True
    assert truths["project.read"]["execution_receipt_present"] is True
    assert truths["conversation.respond"]["executed"] is False
    assert truths["conversation.respond"]["execution_receipt_present"] is False
    assert result["approval_required_steps"][0]["capability_id"] == "conversation.respond"


def test_same_main_model_owns_candidate_discovery_and_understanding():
    result = run_selection(("project.read",))
    discovery = result["candidate_discovery"]
    assert discovery["same_main_model_as_understanding"] is True
    assert discovery["helper_used_for_discovery"] is False
    assert discovery["candidate_capability_ids"] == ("project.read", "conversation.respond")
    assert discovery["hierarchical_discovery"]["used"] is True
    assert discovery["prompt_budget"]["within_budget"] is False
    assert result["main_model_attempts"][0]["schema_valid"] is True
def test_over_budget_consolidation_uses_same_model_bounded_groups_until_prompt_fits():
    registry = projection()
    ids = tuple(item["capability_id"] for item in registry["entries"])[:40]
    roles = []

    def discover(**kwargs):
        allowed = tuple(
            _candidate_slot_enum(kwargs["output_schema"])
        )
        roles.append(allowed)
        return model_call_envelope(json.dumps({
            "candidate_capability_ids": {allowed[0]: True},
            "continuation_required": False, "continuation_reason": "",
            "ambiguity_present": False, "confidence": .99,
            "reason_codes": ["same_model_bounded_consolidation"],
        }))

    found = spine._consolidate_candidate_ids(
        call=discover, candidate_ids=ids, original_text="сводный смысловой запрос",
        session_context={}, registry_projection=registry, deadline=RequestDeadline(30),
        trace=[], audit_trace=[], repair_state={},
    )
    assert found == (ids[0],)
    assert len(roles) > 1
    assert all(len(scope) <= spine.DISCOVERY_VALUES_PER_PASS for scope in roles[:-1])


def test_understanding_budget_uses_same_model_consolidation_without_fixed_capability_ceiling():
    registry = projection()
    ids = tuple(item["capability_id"] for item in registry["entries"])[:60]
    calls = []

    def discover(**kwargs):
        allowed = tuple(
            _candidate_slot_enum(kwargs["output_schema"])
        )
        calls.append(allowed)
        return model_call_envelope(json.dumps({
            "candidate_capability_ids": {allowed[0]: True},
            "continuation_required": False, "continuation_reason": "",
            "ambiguity_present": False, "confidence": .99,
            "reason_codes": ["same_model_understanding_budget"],
        }))

    found = spine._consolidate_for_understanding_budget(
        call=discover, candidate_ids=ids, request_id="request_budget_consolidation",
        original_text="сводный запрос", identity=OWNER, session_context={},
        input_preparation={}, registry_projection=registry, deadline=RequestDeadline(30),
        trace=[], audit_trace=[], repair_state={},
    )
    details = select_semantic_projection_details(registry, found)
    prompt = spine.build_request_understanding_prompt(
        request_id="request_budget_consolidation", original_text="сводный запрос",
        identity=OWNER, session_context={}, input_preparation={}, registry_projection=details,
    )
    budget = spine.measure_prompt_budget(
        *prompt, reserved_output_tokens=spine.REQUEST_UNDERSTANDING_RESERVED_OUTPUT_TOKENS,
        output_schema=spine.REQUEST_UNDERSTANDING_JSON_SCHEMA,
        num_ctx=spine.REQUEST_UNDERSTANDING_NUM_CTX,
    )
    assert calls
    assert budget["within_budget"] is True
    assert len(found) < len(ids)


def test_cyrillic_budget_is_conservative_and_cannot_be_authorized_by_characters_div_four():
    measurement = spine.measure_prompt_budget("я" * 4000, "", reserved_output_tokens=256)
    assert measurement["estimated_prompt_tokens"] >= 2667
    assert measurement["estimated_prompt_tokens"] > measurement["characters"] // 4
    assert measurement["within_budget"] is False
    assert measurement["actual_prompt_tokens"] is None


def test_every_registry_kind_is_reachable_and_each_single_kind_prompt_fits():
    registry = projection()
    all_ids = {item["capability_id"] for item in registry["entries"]}
    kinds = sorted({item["kind"] for item in registry["entries"]})
    reached = set()
    for kind in kinds:
        selected = spine.projection_for_kinds(registry, (kind,))
        groups = spine._candidate_budget_groups(original_text="смысловой запрос",
            session_context={}, registry_projection=selected)
        covered = []
        for group, budget in groups:
            assert budget["within_budget"] is True, kind
            covered.extend(item["capability_id"] for item in group["entries"])
        assert len(covered) == len(set(covered))
        assert set(covered) == {item["capability_id"] for item in selected["entries"]}
        reached.update(covered)
    assert reached == all_ids
    assert {"conversation.respond", "runtime_history_store", "open_project_workbench"} <= reached
def test_candidate_continuation_collects_more_than_six_without_semantic_ceiling():
    candidate_schema = spine.CANDIDATE_DISCOVERY_JSON_SCHEMA["properties"]["candidate_capability_ids"]
    assert candidate_schema["maxProperties"] == spine.DISCOVERY_VALUES_PER_PASS
    assert candidate_schema["minProperties"] == 0
    assert spine.DISCOVERY_VALUES_PER_PASS == 4
    assert candidate_schema["additionalProperties"]["const"] is True
    assert spine.KIND_DISCOVERY_JSON_SCHEMA["properties"]["candidate_kinds"]["additionalProperties"]["const"] is True
    assert "already_selected_ids" not in spine.CANDIDATE_DISCOVERY_JSON_SCHEMA["properties"]
    assert "already_selected_ids" not in spine.KIND_DISCOVERY_JSON_SCHEMA["properties"]
    assert "discovery_complete" not in spine.CANDIDATE_DISCOVERY_JSON_SCHEMA["properties"]
    assert "discovery_complete" not in spine.KIND_DISCOVERY_JSON_SCHEMA["properties"]
    assert "maxItems" not in spine.REQUEST_UNDERSTANDING_JSON_SCHEMA["properties"]["operation_requirements"]
    registry = projection()
    ids = tuple(item["capability_id"] for item in registry["entries"] if item["kind"] == "readonly_tool")[:8]
    selected_projection = select_semantic_projection_details(registry, ids)
    calls = []
    transport_scopes = []

    def discover(**kwargs):
        supplied = json.loads(kwargs["user_prompt"])
        prior_count = int(supplied["prior_selection_count"])
        transport_scopes.append(tuple(
            _candidate_slot_enum(kwargs["output_schema"])
        ))
        index = json.loads(kwargs["system_prompt"].partition("INDEX=")[2])
        assert tuple(row[0] for row in index["rows"]) == ids[prior_count:]
        assert tuple(supplied["host_owned_already_selected_ids"]) == ids[:prior_count]
        batch = ids[prior_count:prior_count + spine.DISCOVERY_VALUES_PER_PASS]
        complete = prior_count + len(batch) == len(ids)
        calls.append(prior_count)
        return model_call_envelope(json.dumps({
                    "candidate_capability_ids": {value: True for value in batch},
                    "continuation_required": not complete, "continuation_reason": "more goals" if not complete else "",
                    "ambiguity_present": False, "confidence": .99,
                    "reason_codes": ["semantic_continuation"],
                }))

    trace = []
    found = spine._run_discovery_continuation(
        call=discover, prompt_builder=spine.build_candidate_discovery_prompt,
        value_key="candidate_capability_ids", allowed_values=ids, original_text="six goals",
        session_context={}, registry_projection=selected_projection, deadline=RequestDeadline(10),
        output_schema=spine.CANDIDATE_DISCOVERY_JSON_SCHEMA, trace=trace,
    )
    assert found == ids and len(found) == 8
    assert calls == [0, 4]
    assert transport_scopes == [ids, ids[4:]]


def test_candidate_scope_may_finish_with_no_relevant_selection_without_failing_turn():
    allowed = ("repo_tree", "repo_search")
    registry = select_semantic_projection_details(projection(), allowed)

    def discover(**kwargs):
        supplied = json.loads(kwargs["user_prompt"])
        assert supplied["host_owned_already_selected_ids"] == []
        return model_call_envelope(json.dumps({
            "candidate_capability_ids": {},
            "continuation_required": False,
            "continuation_reason": "",
            "ambiguity_present": False,
            "confidence": .99,
            "reason_codes": ["no_relevant_capability_in_scope"],
        }))

    trace = []
    found = spine._run_discovery_continuation(
        call=discover, prompt_builder=spine.build_candidate_discovery_prompt,
        value_key="candidate_capability_ids", allowed_values=allowed,
        original_text="привет", session_context={}, registry_projection=registry,
        deadline=RequestDeadline(10), output_schema=spine.CANDIDATE_DISCOVERY_JSON_SCHEMA,
        trace=trace,
    )
    assert found == ()
    assert trace[-1]["new_ids"] == ()
    assert trace[-1]["model_call_used"] is True


def test_candidate_empty_selection_cannot_request_continuation():
    payload = {
        "candidate_capability_ids": {},
        "continuation_required": True,
        "continuation_reason": "claimed more",
        "ambiguity_present": False,
        "confidence": .5,
        "reason_codes": ["invalid_no_progress"],
    }
    with pytest.raises(ValueError, match="continuation requires at least one new ID"):
        parse_discovery_selection_payload(
            payload,
            value_key="candidate_capability_ids",
            allowed_values=("conversation.respond",),
            allow_empty_complete=True,
        )


def test_candidate_partial_pass_may_request_continuation():
    # Continuation is bounded transport for further model discovery, not a demand to
    # fill the current pass to its maximum capacity.
    payload = {
        "candidate_capability_ids": {"project.read": True},
        "continuation_required": True,
        "continuation_reason": "another distinct explicit goal remains",
        "ambiguity_present": False,
        "confidence": 1.0,
        "reason_codes": ["semantic_continuation"],
    }
    parsed = parse_discovery_selection_payload(
        payload,
        value_key="candidate_capability_ids",
        allowed_values=(
            "project.read", "conversation.respond", "runtime_history_store",
            "project_codegraph_readonly", "read_file_snippet",
        ),
        max_values_per_pass=spine.DISCOVERY_VALUES_PER_PASS,
        allow_empty_complete=True,
    )
    assert parsed.continuation_required is True
    assert parsed.selected_values == ("project.read",)


def test_empty_terminal_kind_pass_stops_without_exhausting_remaining_domains():
    registry = projection()
    kinds = tuple(sorted({item["kind"] for item in registry["entries"]}))[:6]
    calls = []

    def discover(**kwargs):
        supplied = json.loads(kwargs["user_prompt"])
        prior = tuple(supplied["host_owned_already_selected_ids"])
        calls.append(prior)
        selected = {value: True for value in kinds[:spine.DISCOVERY_VALUES_PER_PASS]} if not prior else {}
        return model_call_envelope(json.dumps({
            "candidate_kinds": selected,
            "continuation_required": not prior,
            "continuation_reason": "verify remaining explicit goals" if not prior else "",
            "ambiguity_present": False,
            "confidence": .95,
            "reason_codes": ["semantic_scope_complete"],
        }))

    found = spine._run_discovery_continuation(
        call=discover,
        prompt_builder=spine.build_kind_discovery_prompt,
        value_key="candidate_kinds",
        allowed_values=kinds,
        original_text="привет",
        session_context={},
        registry_projection=registry,
        deadline=RequestDeadline(10),
        output_schema=spine.KIND_DISCOVERY_JSON_SCHEMA,
        trace=[],
    )
    assert found == kinds[:spine.DISCOVERY_VALUES_PER_PASS]
    assert calls == [(), kinds[:spine.DISCOVERY_VALUES_PER_PASS]]


def test_candidate_consolidation_preserves_model_selected_response_without_injecting_other_contracts():
    registry = projection()
    ids = ("conversation.respond", "worker_ai_001", "model_role:jarvis_chat_model")

    def consolidate(**kwargs):
        return model_call_envelope(json.dumps({
            "candidate_capability_ids": {
                "conversation.respond": True,
                "model_role:jarvis_chat_model": True,
            },
            "continuation_required": False,
            "continuation_reason": "",
            "ambiguity_present": False,
            "confidence": .9,
            "reason_codes": ["model_role_considered"],
        }))

    found = spine._consolidate_candidate_ids(
        call=consolidate,
        candidate_ids=ids,
        original_text="джарвис привет",
        session_context={},
        registry_projection=registry,
        deadline=RequestDeadline(10),
        trace=[],
        audit_trace=[],
        repair_state={},
    )
    assert found == ("conversation.respond", "model_role:jarvis_chat_model")
    details = select_semantic_projection_details(registry, found)
    by_id = {entry["capability_id"]: entry for entry in details["entries"]}
    assert by_id["model_role:jarvis_chat_model"]["execution_contract_available"] is False
    assert "Visibility-only installed model role" in by_id["model_role:jarvis_chat_model"]["semantic_description"]
    assert "no independent capability operation or provider binding" in by_id["model_role:jarvis_chat_model"]["semantic_description"]
    assert by_id["conversation.respond"]["execution_contract_available"] is True


def test_kind_continuation_collects_more_than_six_with_host_owned_state():
    registry = projection()
    kinds = tuple(sorted({item["kind"] for item in registry["entries"]}))[:8]
    calls = []

    def discover(**kwargs):
        supplied = json.loads(kwargs["user_prompt"])
        prior_count = int(supplied["prior_selection_count"])
        assert tuple(supplied["host_owned_already_selected_ids"]) == kinds[:prior_count]
        batch = kinds[prior_count:prior_count + spine.DISCOVERY_VALUES_PER_PASS]
        calls.append(prior_count)
        return model_call_envelope(json.dumps({
            "candidate_kinds": {value: True for value in batch},
            "continuation_required": prior_count + len(batch) < len(kinds),
            "continuation_reason": "more semantic kinds" if prior_count + len(batch) < len(kinds) else "",
            "ambiguity_present": False, "confidence": .99, "reason_codes": ["semantic_continuation"],
        }))

    trace = []
    found = spine._run_discovery_continuation(
        call=discover, prompt_builder=spine.build_kind_discovery_prompt,
        value_key="candidate_kinds", allowed_values=kinds, original_text="many semantic goals",
        session_context={}, registry_projection=registry, deadline=RequestDeadline(10),
        output_schema=spine.KIND_DISCOVERY_JSON_SCHEMA, trace=trace,
    )
    assert found == kinds and len(found) == 8
    assert calls == [0, 4]
    assert all("already_selected_ids" not in spine.KIND_DISCOVERY_JSON_SCHEMA["required"] for _ in (0,))


def test_kind_discovery_exposes_authoritative_operations_without_inventing_nonexecutable_ones():
    system, _ = spine.build_kind_discovery_prompt(
        original_text="прочитай проект", session_context={}, registry_projection=projection(),
    )
    domains = json.loads(system.partition("DOMAINS=")[2])
    by_kind = {row[0]: row for row in domains}
    canonical = by_kind["canonical_capability"]
    assert canonical[2] == 2
    readonly = by_kind["readonly_tool"]
    assert readonly[2] >= 1
    assert by_kind["memory_tool"][2] >= 1
    pc_action = by_kind["pc_action"]
    assert pc_action[2] == len(PC_ACTION_OPERATION_CONTRACTS) - 1
    assert any("screenshot" in description for description in pc_action[4])
    assert "with one, two or three candidate_kinds keys, continuation_required MUST be false" in system
    assert "operation_id" not in system
    assert "use__" not in system


def test_discovery_transport_schema_is_bound_to_registered_scope():
    allowed = ("readonly_tool", "memory_tool")
    schema = spine.discovery_schema_for_registered_values(
        spine.KIND_DISCOVERY_JSON_SCHEMA,
        value_key="candidate_kinds",
        allowed_values=allowed,
    )
    assert tuple(schema["properties"]["candidate_kinds"]["properties"]) == allowed
    assert schema["properties"]["candidate_kinds"]["maxProperties"] == len(allowed)
    assert schema["properties"]["continuation_required"]["const"] is False
    assert schema["properties"]["continuation_reason"]["const"] == ""
    assert "properties" not in spine.KIND_DISCOVERY_JSON_SCHEMA["properties"]["candidate_kinds"]


def test_candidate_schema_uses_sparse_property_names_that_cannot_duplicate():
    response_schema = spine.discovery_schema_for_registered_values(
        spine.CANDIDATE_DISCOVERY_JSON_SCHEMA,
        value_key="candidate_capability_ids",
        allowed_values=("conversation.respond", "project.read"),
    )
    response_selection = response_schema["properties"]["candidate_capability_ids"]
    assert response_selection["type"] == "object"
    assert response_selection["additionalProperties"] is False
    assert response_selection["maxProperties"] == 2
    # The allowed IDs are property NAMES (const true): JSON object keys are inherently
    # unique, so a duplicate capability ID is structurally unrepresentable.
    assert set(response_selection["properties"]) == {"conversation.respond", "project.read"}
    assert response_selection["properties"]["conversation.respond"]["const"] is True
    assert response_selection["properties"]["project.read"]["const"] is True

    tool_only_schema = spine.discovery_schema_for_registered_values(
        spine.CANDIDATE_DISCOVERY_JSON_SCHEMA,
        value_key="candidate_capability_ids",
        allowed_values=("repo_tree", "repo_search"),
    )
    assert "minItems" not in tool_only_schema["properties"]["candidate_capability_ids"]
    tool_only_prompt, _ = spine.build_candidate_discovery_prompt(
        original_text="привет",
        session_context={},
        registry_projection=select_semantic_projection_details(
            projection(), ("repo_tree", "repo_search"),
        ),
    )
    assert "Return an empty object only when" in tool_only_prompt
    assert "candidate_capability_ids must not be empty" not in tool_only_prompt


def test_operation_fixed_slots_are_fail_closed_not_structurally_unique():
    # Current schema reuses unique typed keys; the preserved parser also rejects
    # duplicate legacy slots. No host deduplication can turn them into a valid choice.
    op_schema = spine.discovery_schema_for_registered_values(
        spine.OPERATION_DISCOVERY_JSON_SCHEMA, value_key="candidate_operation_ids",
        allowed_values=("execute_volume_up", "read_screen"),
    )
    sel = op_schema["properties"]["candidate_operation_ids"]
    assert sel["properties"] == {"execute_volume_up": {"type": "boolean", "const": True}, "read_screen": {"type": "boolean", "const": True}}
    assert sel["maxProperties"] == 2
    # Duplicate values are representable, so the parser must still reject them fail-closed.
    import pytest
    from MAKSIMAR_CORE_LIB.ai_orchestration.helper_model_decision_parser import parse_discovery_selection_payload
    with pytest.raises(ValueError, match="duplicate"):
        parse_discovery_selection_payload(
            {"candidate_operation_ids": {"selection_1": "read_screen", "selection_2": "read_screen",
             "selection_3": None, "selection_4": None}, "continuation_required": False,
             "selection_justifications": {"read_screen": {
                 "goal_id": "g1",
                 "justification_kind": "DIRECT_GOAL_EFFECT", "source_grounding": "read screen",
             }},
             "continuation_reason": "", "ambiguity_present": False, "confidence": .9,
             "reason_codes": ["x"]},
            value_key="candidate_operation_ids",
            allowed_values=("execute_volume_up", "read_screen"),
        )


def test_discovery_no_progress_and_deadline_stop_fail_closed():
    allowed = ("project.read", "conversation.respond", "repo_tree", "repo_search", "repo_files")
    registry = select_semantic_projection_details(projection(), allowed)
    trace = []
    calls = 0

    def no_progress(**kwargs):
        nonlocal calls
        calls += 1
        selected = (
            {value: True for value in allowed[:spine.DISCOVERY_VALUES_PER_PASS]}
            if calls == 1 else
            {"project.read": True}
        )
        return model_call_envelope(json.dumps({
                    "candidate_capability_ids": selected,
                    "continuation_required": calls == 1,
                    "continuation_reason": "claimed more" if calls == 1 else "",
                    "ambiguity_present": False, "confidence": .8,
                    "reason_codes": ["test"],
                }))

    with pytest.raises(ValueError, match="repeats canonical state"):
        spine._run_discovery_continuation(
            call=no_progress, prompt_builder=spine.build_candidate_discovery_prompt,
            value_key="candidate_capability_ids", allowed_values=allowed, original_text="x",
            session_context={}, registry_projection=registry, deadline=RequestDeadline(10),
            output_schema=spine.CANDIDATE_DISCOVERY_JSON_SCHEMA, trace=trace,
        )
    assert trace[-1]["model_call_used"] is False
    assert trace[-1]["validation_error"] == "discovery selection repeats canonical state"
    deadline = RequestDeadline(10)
    deadline.cancel()
    with pytest.raises(TimeoutError, match="deadline"):
        spine._run_discovery_continuation(
            call=no_progress, prompt_builder=spine.build_candidate_discovery_prompt,
            value_key="candidate_capability_ids", allowed_values=allowed, original_text="x",
            session_context={}, registry_projection=registry, deadline=deadline,
            output_schema=spine.CANDIDATE_DISCOVERY_JSON_SCHEMA, trace=[],
        )


@pytest.mark.parametrize(("missing_field", "expected"), (
    ("model_call_attempted", "model_call_attempted_not_true"),
    ("model_call_succeeded", "model_call_succeeded_not_true"),
    ("raw_output_present", "raw_output_present_not_true"),
))
def test_discovery_reports_the_exact_missing_envelope_predicate(missing_field, expected):
    result = model_call_envelope("{}")
    result.pop(missing_field)
    assert spine._model_call_verification_error(result).startswith(expected)


def test_invalid_discovery_json_retains_sanitized_content_telemetry_and_validation_error():
    registry = select_semantic_projection_details(projection(), ("project.read",))
    attempts = []

    def invalid(**kwargs):
        del kwargs
        result = model_call_envelope('{"candidate_capability_ids":')
        result.update({
            "model_id": "jarvis:chat8b", "response_model_id": "jarvis:chat8b",
            "prompt_eval_count": 583, "eval_count": 192, "done_reason": "stop",
            "raw_response_sha256": "fixture-hash", "raw_model_result": {"content": "sanitized"},
        })
        return result

    with pytest.raises(ValueError, match="valid JSON"):
        spine._run_discovery_continuation(
            call=invalid, prompt_builder=spine.build_candidate_discovery_prompt,
            value_key="candidate_capability_ids", allowed_values=("project.read",),
            original_text="semantic request", session_context={}, registry_projection=registry,
            deadline=RequestDeadline(10), output_schema=spine.CANDIDATE_DISCOVERY_JSON_SCHEMA,
            trace=[], audit_trace=attempts, call_role="candidate_discovery",
        )
    assert attempts[0]["prompt_eval_count"] == 583
    assert attempts[0]["sanitized_structured_model_content"] == '{"candidate_capability_ids":'
    assert attempts[0]["schema_valid"] is False
    assert "valid JSON" in attempts[0]["validation_error"]


def test_discovery_parser_rejects_duplicate_semantic_fields():
    payload = (
        '{"candidate_kinds":{"skill":true},"candidate_kinds":{"agent":true},'
        '"continuation_required":false,"continuation_reason":"",'
        '"ambiguity_present":false,"confidence":1,'
        '"reason_codes":["strict"]}'
    )
    with pytest.raises(ValueError, match="duplicate field"):
        parse_discovery_selection_payload(
            payload, value_key="candidate_kinds", allowed_values=("skill", "agent"),
        )


def test_discovery_uses_at_most_one_same_model_strict_repair_for_duplicate_ids():
    registry = select_semantic_projection_details(projection(), ("project.read", "conversation.respond"))
    calls = []

    def discover(**kwargs):
        calls.append(kwargs["system_prompt"])
        if len(calls) == 1:
            return model_call_envelope(
                '{"candidate_capability_ids":{"project.read":true,"project.read":true},'
                '"continuation_required":false,"continuation_reason":"",'
                '"ambiguity_present":false,"confidence":0.99,"reason_codes":["strict"]}'
            )
        return model_call_envelope(json.dumps({
            "candidate_capability_ids": {
                "project.read": True, "conversation.respond": True,
            },
            "continuation_required": False, "continuation_reason": "",
            "ambiguity_present": False, "confidence": .99, "reason_codes": ["strict"],
        }))

    repair_state = {}
    found = spine._run_discovery_continuation(
        call=discover, prompt_builder=spine.build_candidate_discovery_prompt,
        value_key="candidate_capability_ids",
        allowed_values=("project.read", "conversation.respond"),
        original_text="прочитай проект", session_context={}, registry_projection=registry,
        deadline=RequestDeadline(10), output_schema=spine.CANDIDATE_DISCOVERY_JSON_SCHEMA,
        trace=[], audit_trace=[], repair_state=repair_state,
    )
    assert found == ("project.read", "conversation.respond")
    assert len(calls) == 2
    assert repair_state["model_backed_repair_count"] == 1


@pytest.mark.parametrize("replacement_invalid", [False, True])
def test_completed_schema_rejection_uses_one_existing_repair_and_never_bypasses_validation(replacement_invalid):
    registry = select_semantic_projection_details(projection(), ("project.read", "conversation.respond"))
    calls = []
    raw = json.dumps({"candidate_capability_ids": {"project.read": True, "conversation.respond": True},
        "continuation_required": False, "continuation_reason": "", "ambiguity_present": False,
        "confidence": .99, "reason_codes": ["strict"]})
    def discover(**kwargs):
        calls.append(kwargs["system_prompt"])
        result = model_call_envelope(raw)
        if len(calls) == 1 or replacement_invalid:
            result.update(final_valid=False, validation_error="schema_validation_error:extra_property")
        return result
    repair_state, attempts = {}, []
    kwargs = dict(call=discover, prompt_builder=spine.build_candidate_discovery_prompt,
        value_key="candidate_capability_ids", allowed_values=("project.read", "conversation.respond"),
        original_text="прочитай проект", session_context={}, registry_projection=registry,
        deadline=RequestDeadline(10), output_schema=spine.CANDIDATE_DISCOVERY_JSON_SCHEMA,
        trace=[], audit_trace=attempts, repair_state=repair_state)
    if replacement_invalid:
        with pytest.raises(ValueError, match="model_structured_schema_invalid"):
            spine._run_discovery_continuation(**kwargs)
    else:
        assert spine._run_discovery_continuation(**kwargs) == ("project.read", "conversation.respond")
        assert attempts[-1]["model_call_used"] is True
    assert len(calls) == 2 and repair_state["model_backed_repair_count"] == 1
    assert attempts[0]["schema_valid"] is False and attempts[0]["model_call_used"] is False


@pytest.mark.parametrize("replacement_invalid", [False, True])
def test_exhausted_operation_capacity_continuation_is_repaired_once_not_silently_coerced(replacement_invalid):
    registry = select_semantic_projection_details(projection(), ("runtime_history_store",))
    registry["selection_goalframes"] = ({"goal_id":"g1", "effect_intent":"retrieve", "requested_outcome":"history", "grounding":"прочитай историю"},)
    calls, attempts, repair_state = [], [], {}
    def discover(**kwargs):
        calls.append(kwargs)
        continuation = len(calls) == 1 or replacement_invalid
        return model_call_envelope(json.dumps({"candidate_operation_ids": {
            "selection_1":"search_history", "selection_2":None,"selection_3":None,"selection_4":None},
            "selection_justifications":{"search_history":{"goal_id":"g1","justification_kind":"DIRECT_GOAL_EFFECT","source_grounding":"прочитай историю"}},
            "continuation_required":continuation,"continuation_reason":"provider work still needed" if continuation else "",
            "ambiguity_present":False,"confidence":.99,"reason_codes":["strict"]}))
    kwargs = dict(call=discover,prompt_builder=spine.build_operation_discovery_prompt,
        value_key="candidate_operation_ids",allowed_values=("search_history","inspect_recent_session_memory"),
        original_text="прочитай историю",session_context={},registry_projection=registry,
        deadline=RequestDeadline(10),output_schema=spine.OPERATION_DISCOVERY_JSON_SCHEMA,
        trace=[],audit_trace=attempts,repair_state=repair_state,max_selected_values=1)
    if replacement_invalid:
        with pytest.raises(ValueError,match="operation_continuation_exceeds_typed_justification_capacity"):
            spine._run_discovery_continuation(**kwargs)
    else:
        assert spine._run_discovery_continuation(**kwargs) == ("search_history",)
    assert len(calls)==2 and repair_state["model_backed_repair_count"]==1
    assert attempts[0]["model_call_used"] is False
    assert "capacity=1 additional justified operation IDs" in calls[0]["system_prompt"]


def test_cross_kind_reconciliation_and_repair_fit_bounded_session_context():
    selected = select_semantic_projection_details(
        projection(), ("conversation.respond", "project.read"),
    )
    context = {
        "bounded_chronological_turns": ({
            "user_text": "у" * 120, "assistant_text": "а" * 160,
            "topic": "conversation", "trace_id": "prior_trace",
        },) * 3,
        "recent_relevant_turns": (),
    }
    output_schema = spine.discovery_schema_for_registered_values(
        spine.CANDIDATE_DISCOVERY_JSON_SCHEMA,
        value_key="candidate_capability_ids",
        allowed_values=("conversation.respond", "project.read"),
    )
    for builder in (
        spine.build_cross_kind_executable_reconciliation_prompt,
        spine.build_cross_kind_executable_reconciliation_repair_prompt,
    ):
        prompt = builder(
            original_text=(
                "Безопасно проверь текущий Git-статус рабочего дерева и кратко объясни, "
                "ничего не меняй."
            ),
            session_context=context, registry_projection=selected,
            selected_kinds=("readonly_tool",),
        )
        budget = spine.measure_prompt_budget(
            *prompt,
            reserved_output_tokens=spine.CANDIDATE_DISCOVERY_RESERVED_OUTPUT_TOKENS,
            output_schema=output_schema,
            components=spine._prompt_material_components(*prompt),
        )
        assert budget["within_budget"] is True, builder.__name__
def test_consolidation_skip_preserves_model_selected_set_without_injection():
    registry = projection()
    ids = ("conversation.respond", "project.read", "runtime_history_store")

    class NoConsolidationModel:
        def discover_candidates(self, **kwargs):
            raise AssertionError("consolidation must not re-select a bounded model-selected set")

    result, audit = spine._consolidate_candidate_ids_if_needed(
        call=NoConsolidationModel().discover_candidates,
        candidate_ids=ids,
        original_text="прочитай ранее сохранённую историю",
        session_context={},
        registry_projection=registry,
        deadline=RequestDeadline(10),
        trace=[],
        audit_trace=[],
        repair_state={},
    )
    assert tuple(result) == tuple(ids)
    assert audit["status"] == "NOT_REQUIRED_ALREADY_BOUNDED"
    fits = audit["operation_discovery_prompt_budget"]["within_budget"]
    assert audit["reason"] == ("DOWNSTREAM_BUDGET_FITS_MODEL_SELECTED_SET" if fits else "CAPABILITY_SET_PRESERVED_DESPITE_DOWNSTREAM_BUDGET")
    # The host injected nothing: the returned IDs are exactly the model-selected set.
    assert set(result) == set(ids)


def test_downstream_budget_cannot_reselect_already_justified_capabilities(monkeypatch):
    registry = projection()
    ids = ("conversation.respond", "project.read", "runtime_history_store", "session_memory")

    def over_budget(**kwargs):
        del kwargs
        return {"within_budget": False, "operation_count": 999, "candidate_count": len(ids)}

    monkeypatch.setattr(spine, "_measure_operation_discovery_budget", over_budget)

    class ConsolidateModel:
        def __init__(self):
            self.calls = 0

        def discover_candidates(self, **kwargs):
            self.calls += 1
            allowed = tuple(
                _candidate_slot_enum(kwargs["output_schema"])
            )
            selected = {value: True for value in allowed[:2]}
            return model_call_envelope(json.dumps({
                "candidate_capability_ids": selected,
                "continuation_required": False, "continuation_reason": "",
                "ambiguity_present": False, "confidence": .9,
                "reason_codes": ["bounded_subset"],
            }))

    model = ConsolidateModel()
    result, audit = spine._consolidate_candidate_ids_if_needed(
        call=model.discover_candidates,
        candidate_ids=ids,
        original_text="прочитай ранее сохранённую историю",
        session_context={},
        registry_projection=registry,
        deadline=RequestDeadline(10),
        trace=[],
        audit_trace=[],
        repair_state={},
    )
    assert model.calls == 0
    assert tuple(result) == ids
    assert audit["status"] == "NOT_REQUIRED_ALREADY_BOUNDED"
    assert audit["reason"] == "CAPABILITY_SET_PRESERVED_DESPITE_DOWNSTREAM_BUDGET"


def test_consolidation_rejects_unknown_output_fail_closed():
    registry = projection()
    ids = ("conversation.respond", "project.read")

    class InvalidModel:
        def discover_candidates(self, **kwargs):
            return model_call_envelope(json.dumps({
                "candidate_capability_ids": {"not_a_registered_capability": True},
                "continuation_required": False, "continuation_reason": "",
                "ambiguity_present": False, "confidence": .9,
                "reason_codes": ["invalid"],
            }))

    with pytest.raises(ValueError):
        spine._consolidate_candidate_ids(
            call=InvalidModel().discover_candidates,
            candidate_ids=ids,
            original_text="прочитай ранее сохранённую историю",
            session_context={},
            registry_projection=registry,
            deadline=RequestDeadline(10),
            trace=[],
            audit_trace=[],
            repair_state={},
        )


@pytest.mark.parametrize("noisy", (
    "Джарвис пажалуста коротка скажы что доступно",
    "джарвес пожалуста скажи што доступна",
    "пж скажы коротко что сичас доступно",
))
def test_requested_no_change_gets_one_same_helper_model_quality_review(noisy):
    class ReviewHelper:
        def __init__(self):
            self.first_calls = 0
            self.review_calls = 0

        def correct_input(self, **kwargs):
            self.first_calls += 1
            normalized = kwargs["safe_normalized_text"]
            return {"final_valid": True,
                "ok": True, "content": json.dumps({
                    "schema_version": "helper_input_correction.v2", "corrected_text": normalized,
                    "ambiguity_candidates": [], "confidence": 1.0,
                    "reason_codes": ["no_change_needed"], "preserve_original": True,
                    "no_change_needed": True,
                }, ensure_ascii=False),
                "model_call_attempted": True, "model_call_succeeded": True,
                "raw_output_present": True, "raw_model_result": {"model": "jarvis:helper3b"},
            }

        def review_input_correction(self, **kwargs):
            self.review_calls += 1
            assert kwargs["prior_correction"]["no_change_needed"] is True
            return {"final_valid": True,
                "ok": True, "content": json.dumps({
                    "schema_version": "helper_input_correction.v2",
                    "corrected_text": "Джарвис, пожалуйста, коротко скажи, что сейчас доступно",
                    "ambiguity_candidates": [], "confidence": .96,
                    "reason_codes": ["stt_orthography_review"], "preserve_original": True,
                    "no_change_needed": False,
                }, ensure_ascii=False),
                "model_call_attempted": True, "model_call_succeeded": True,
                "raw_output_present": True, "raw_model_result": {"model": "jarvis:helper3b"},
            }

    helper = ReviewHelper()
    preparation, trace = spine._prepare_input(
        model_port=helper, deadline=RequestDeadline(10), original_text=noisy,
        input_channel="stt", input_quality_metadata={
            "stt_confidence": .61, "correction_requested": True,
        },
    )
    assert helper.first_calls == helper.review_calls == 1
    assert trace["helper_quality_review_attempted"] is True
    assert trace["helper_quality_review_schema_valid"] is True
    assert trace["semantic_correction_accepted"] is True
    assert trace["correction_applied"] is True
    assert preparation["original_text"] == noisy


def test_requested_no_change_reviewed_as_no_change_is_not_semantically_accepted():
    original = "Джарвис пажалуста скажы што доступно"

    class NoChangeReview:
        def __init__(self):
            self.review_calls = 0

        @staticmethod
        def _result(text):
            return {"final_valid": True,
                "ok": True, "content": json.dumps({
                    "schema_version": "helper_input_correction.v2", "corrected_text": text,
                    "ambiguity_candidates": [], "confidence": 1.0,
                    "reason_codes": ["no_change_needed"], "preserve_original": True,
                    "no_change_needed": True,
                }, ensure_ascii=False),
                "model_call_attempted": True, "model_call_succeeded": True,
                "raw_output_present": True, "raw_model_result": {"model": "jarvis:helper3b"},
            }

        def correct_input(self, **kwargs):
            return self._result(kwargs["safe_normalized_text"])

        def review_input_correction(self, **kwargs):
            self.review_calls += 1
            return self._result(kwargs["safe_normalized_text"])

    helper = NoChangeReview()
    preparation, trace = spine._prepare_input(
        model_port=helper, deadline=RequestDeadline(10), original_text=original,
        input_channel="stt", input_quality_metadata={"correction_requested": True},
    )
    assert helper.review_calls == 1
    assert trace["helper_quality_review_schema_valid"] is True
    assert trace["correction_applied"] is False
    assert trace["semantic_correction_accepted"] is False
    assert preparation["normalized_text"] == original
    assert preparation["original_text"] == original
    assert trace["helper_call_used"] is True


def test_contradictory_changed_text_gets_one_strict_same_helper_review():
    original = "Джарвис пажалуста коротка скажы что доступно"

    class ContradictionThenCorrection:
        def __init__(self):
            self.first_calls = 0
            self.review_calls = 0

        def correct_input(self, **kwargs):
            self.first_calls += 1
            return {"final_valid": True,
                "ok": True, "content": json.dumps({
                    "schema_version": "helper_input_correction.v2",
                    "corrected_text": "Джарвис пожалуйста коротко скажи что доступно",
                    "ambiguity_candidates": [], "confidence": 1.0,
                    "reason_codes": ["no_change_needed"], "preserve_original": True,
                    "no_change_needed": True,
                }, ensure_ascii=False),
                "model_call_attempted": True, "model_call_succeeded": True,
                "raw_output_present": True, "raw_model_result": {"model": "jarvis:helper3b"},
            }

        def review_input_correction(self, **kwargs):
            self.review_calls += 1
            assert kwargs["validation_error"] == (
                "no_change_needed must exactly reflect whether corrected_text changed"
            )
            assert kwargs["prior_correction"]["no_change_needed"] is True
            return {"final_valid": True,
                "ok": True, "content": json.dumps({
                    "schema_version": "helper_input_correction.v2",
                    "corrected_text": "Джарвис пожалуйста коротко скажи что доступно",
                    "ambiguity_candidates": [], "confidence": .98,
                    "reason_codes": ["stt_orthography_review"], "preserve_original": True,
                    "no_change_needed": False,
                }, ensure_ascii=False),
                "model_call_attempted": True, "model_call_succeeded": True,
                "raw_output_present": True, "raw_model_result": {"model": "jarvis:helper3b"},
            }

    helper = ContradictionThenCorrection()
    preparation, trace = spine._prepare_input(
        model_port=helper, deadline=RequestDeadline(10), original_text=original,
        input_channel="stt", input_quality_metadata={
            "stt_confidence": .61, "correction_requested": True,
        },
    )
    assert helper.first_calls == helper.review_calls == 1
    assert trace["helper_first_call_attempted"] is True
    assert trace["helper_first_call_succeeded"] is True
    assert trace["helper_first_raw_output_present"] is True
    assert trace["helper_first_schema_valid"] is False
    assert trace["helper_first_result_used"] is False
    assert trace["helper_first_validation_error"] == (
        "no_change_needed must exactly reflect whether corrected_text changed"
    )
    assert trace["helper_quality_review_attempted"] is True
    assert trace["helper_quality_review_succeeded"] is True
    assert trace["helper_quality_review_schema_valid"] is True
    assert trace["helper_quality_review_result_used"] is True
    assert trace["helper_call_used"] is True
    assert trace["correction_applied"] is True
    assert trace["semantic_correction_accepted"] is True
    assert preparation["normalized_text"] == "Джарвис пожалуйста коротко скажи что доступно"


def test_contradictory_review_is_never_applied_and_original_continues():
    original = "Джарвис пажалуста скажы што доступно"
    contradictory = {
        "schema_version": "helper_input_correction.v2",
        "corrected_text": "Джарвис пожалуйста скажи что доступно",
        "ambiguity_candidates": [], "confidence": 1.0,
        "reason_codes": ["no_change_needed"], "preserve_original": True,
        "no_change_needed": True,
    }

    class TwiceContradictory:
        def __init__(self): self.review_calls = 0
        def correct_input(self, **kwargs):
            return {"final_valid": True,
                "ok": True, "content": json.dumps(contradictory, ensure_ascii=False),
                "model_call_attempted": True, "model_call_succeeded": True,
                "raw_output_present": True, "raw_model_result": {"call": "first"},
            }
        def review_input_correction(self, **kwargs):
            self.review_calls += 1
            return {"final_valid": True,
                "ok": True, "content": json.dumps(contradictory, ensure_ascii=False),
                "model_call_attempted": True, "model_call_succeeded": True,
                "raw_output_present": True, "raw_model_result": {"call": "review"},
            }

    helper = TwiceContradictory()
    preparation, trace = spine._prepare_input(
        model_port=helper, deadline=RequestDeadline(10), original_text=original,
        input_channel="stt", input_quality_metadata={"correction_requested": True},
    )
    assert helper.review_calls == 1
    assert trace["helper_quality_review_schema_valid"] is False
    assert trace["helper_call_used"] is False
    assert trace["correction_applied"] is False
    assert trace["semantic_correction_accepted"] is False
    assert "no_change_needed must exactly reflect" in trace["helper_quality_review_error"]
    assert trace["helper_quality_review_raw_output_present"] is True
    assert trace["helper_quality_review_raw_result"] == {"call": "review"}
    assert preparation["safe_normalized_text"] == original
    assert preparation["helper_correction_proposal"] == ""


def test_contradictory_review_timeout_keeps_original_without_fallback():
    original = "Джарвис пажалуста скажы што доступно"

    class ReviewTimeout:
        def correct_input(self, **kwargs):
            return {"final_valid": True,
                "ok": True, "content": json.dumps({
                    "schema_version": "helper_input_correction.v2",
                    "corrected_text": "Джарвис пожалуйста скажи что доступно",
                    "ambiguity_candidates": [], "confidence": 1.0,
                    "reason_codes": ["no_change_needed"], "preserve_original": True,
                    "no_change_needed": True,
                }, ensure_ascii=False),
                "model_call_attempted": True, "model_call_succeeded": True,
                "raw_output_present": True, "raw_model_result": {"call": "first"},
            }
        def review_input_correction(self, **kwargs):
            raise TimeoutError("review timeout")

    preparation, trace = spine._prepare_input(
        model_port=ReviewTimeout(), deadline=RequestDeadline(10), original_text=original,
        input_channel="stt", input_quality_metadata={"correction_requested": True},
    )
    assert trace["helper_quality_review_attempted"] is True
    assert trace["helper_quality_review_error"] == "TimeoutError:review timeout"
    assert trace["helper_call_used"] is False
    assert trace["correction_applied"] is False
    assert trace["semantic_correction_accepted"] is False
    assert preparation["original_text"] == preparation["safe_normalized_text"] == original


@pytest.mark.parametrize("review_mode", ("invalid", "timeout"))
def test_invalid_or_timeout_helper_review_keeps_original_and_semantic_acceptance_false(review_mode):
    original = "Джарвис пажалуста скажы што доступно"

    class FailingReview:
        def correct_input(self, **kwargs):
            normalized = kwargs["safe_normalized_text"]
            return {"final_valid": True,
                "ok": True, "content": json.dumps({
                    "schema_version": "helper_input_correction.v2", "corrected_text": normalized,
                    "ambiguity_candidates": [], "confidence": 1.0,
                    "reason_codes": ["no_change_needed"], "preserve_original": True,
                    "no_change_needed": True,
                }, ensure_ascii=False),
                "model_call_attempted": True, "model_call_succeeded": True,
                "raw_output_present": True, "raw_model_result": {"model": "jarvis:helper3b"},
            }

        def review_input_correction(self, **kwargs):
            del kwargs
            if review_mode == "timeout":
                raise TimeoutError("review timeout")
            return {"final_valid": True,
                "ok": True, "content": "not-json",
                "model_call_attempted": True, "model_call_succeeded": True,
                "raw_output_present": True, "raw_model_result": {"model": "jarvis:helper3b"},
            }

    preparation, trace = spine._prepare_input(
        model_port=FailingReview(), deadline=RequestDeadline(10), original_text=original,
        input_channel="stt", input_quality_metadata={"correction_requested": True},
    )
    assert trace["semantic_correction_accepted"] is False
    assert trace["correction_applied"] is False
    assert preparation["original_text"] == original
    assert preparation["safe_normalized_text"] == original


def test_clean_input_without_requested_correction_skips_review_without_helper_failure():
    class UnexpectedHelper:
        def correct_input(self, **kwargs):
            raise AssertionError(f"helper must not be called: {kwargs}")

        def review_input_correction(self, **kwargs):
            raise AssertionError(f"review must not be called: {kwargs}")

    preparation, trace = spine._prepare_input(
        model_port=UnexpectedHelper(), deadline=RequestDeadline(10),
        original_text="Джарвис, коротко скажи, что доступно.",
        input_channel="terminal", input_quality_metadata={},
    )
    assert trace["helper_failure_mode"] == "not_requested"
    assert trace["helper_call_attempted"] is False
    assert trace["helper_quality_review_attempted"] is False
    assert trace["semantic_correction_accepted"] is None
    assert preparation["safe_normalized_text"] == "Джарвис, коротко скажи, что доступно."


def test_model_backed_repair_is_globally_limited_to_one():
    registry = projection()
    selected = select_semantic_projection_details(registry, ("project.read",))
    audit = {"model_backed_repair_count": 1}
    parsed = spine._understand(
        Model(selected, ("project.read",)), RequestDeadline(10), "request_repair_limit", "probe",
        OWNER, {}, replan_reason="second repair", audit_trace=audit, registry_projection=selected,
    )
    assert parsed is None
    assert audit["model_backed_repair_blocked"] == "single_repair_limit_reached"


def test_offline_provider_remains_selected_visible_and_unexecuted():
    registry = projection({"pc_executor_available": False, "ollama_alive": True})
    result = spine.run_canonical_semantic_turn(
        text="natural offline capability request", project_port=EvidencePort(), conversation_port=EvidencePort(),
        model_port=Model(registry, ("runtime_windows_edge",)), final_brain_port=Final(),
        permission_port=__import__("MAKSIMAR_CORE_LIB.security_layer.semantic_policy", fromlist=["SemanticPolicyEvaluator"]).SemanticPolicyEvaluator(),
        identity=OWNER, registry_projection=registry, provider_ports={},
    )
    assert result["selected_capabilities"] == ("runtime_windows_edge", "conversation.respond")
    assert result["operation_status"] == "PARTIAL_UNAVAILABLE"
    edge_step = next(
        step for step in result["execution_plan"]["steps"]
        if step["capability_id"] == "runtime_windows_edge"
    )
    assert edge_step["operation"] == "read_windows_edge_status"
    assert result["provider_unavailable_steps"] == (edge_step,)
    edge_truth = next(
        item for item in result["capability_truth"]
        if item["capability_id"] == "runtime_windows_edge"
    )
    assert edge_truth["provider_available"] is False
    assert edge_truth["executed"] is False
    assert edge_truth["execution_receipt_present"] is False


def test_unbound_execution_request_fails_closed_without_fake_operation():
    registry = projection()

    class ExecutionSeekingModel(Model):
        def understand(self, **kwargs):
            result = super().understand(**kwargs)
            payload = json.loads(result["content"])
            payload["required_capabilities"][0]["operation_contract_required"] = True
            payload["required_capabilities"][0]["unresolved_operation_reason"] = "typed operation contract required"
            result["content"] = json.dumps(payload)
            return result

    result = spine.run_canonical_semantic_turn(
        text="execute the visible capability", project_port=EvidencePort(), conversation_port=EvidencePort(),
        model_port=ExecutionSeekingModel(registry, ("repo_git_status",)), final_brain_port=Final(),
        permission_port=__import__("MAKSIMAR_CORE_LIB.security_layer.semantic_policy", fromlist=["SemanticPolicyEvaluator"]).SemanticPolicyEvaluator(),
        identity=OWNER, registry_projection=registry, provider_ports={},
    )
    assert result["operation_status"] == "UNRESOLVED_OPERATION"
    assert result["execution_plan"] is None
    assert result["capability_truth"][0]["provider_binding_status"] == "UNBOUND"
    assert result["capability_truth"][0]["executed"] is False


def test_truthful_helper_valid_and_invalid_results():
    class Helper:
        def __init__(self, content): self.content = content
        def correct_input(self, **kwargs):
            del kwargs
            return {"final_valid": True, "ok": True, "content": self.content, "model_call_attempted": True,
                    "model_call_succeeded": True, "raw_output_present": True, "raw_model_result": {"model": "helper"}}
    valid = json.dumps({
        "schema_version": "helper_input_correction.v2", "corrected_text": "привет",
        "ambiguity_candidates": [], "confidence": 0.99, "reason_codes": ["typing_correction"],
        "preserve_original": True, "no_change_needed": False,
    }, ensure_ascii=False)
    _, valid_trace = spine._prepare_input(
        model_port=Helper(valid), deadline=RequestDeadline(10), original_text="превет",
        input_channel="stt", input_quality_metadata={},
    )
    assert all(valid_trace[key] is True for key in (
        "helper_call_attempted", "helper_call_succeeded", "helper_raw_output_present",
        "helper_schema_valid", "helper_correction_valid", "helper_call_used",
    ))
    preparation, invalid_trace = spine._prepare_input(
        model_port=Helper("not-json"), deadline=RequestDeadline(10), original_text="превет",
        input_channel="stt", input_quality_metadata={},
    )
    assert invalid_trace["helper_call_attempted"] is True
    assert invalid_trace["helper_call_succeeded"] is True
    assert invalid_trace["helper_schema_valid"] is False
    assert invalid_trace["helper_call_used"] is False
    assert preparation["original_text"] == "превет"
    assert preparation["helper_correction_proposal"] == ""

    class UnverifiedHelper(Helper):
        def correct_input(self, **kwargs):
            result = super().correct_input(**kwargs)
            result["model_call_succeeded"] = False
            return result

    unverified_preparation, unverified_trace = spine._prepare_input(
        model_port=UnverifiedHelper(valid), deadline=RequestDeadline(10), original_text="превет",
        input_channel="stt", input_quality_metadata={},
    )
    assert unverified_trace["helper_call_attempted"] is True
    assert unverified_trace["helper_call_succeeded"] is False
    assert unverified_trace["helper_raw_output_present"] is True
    assert unverified_trace["helper_schema_valid"] is False
    assert unverified_trace["helper_call_used"] is False
    assert unverified_preparation["original_text"] == "превет"


def test_available_step_executes_when_independent_provider_is_unavailable():
    registry = projection()
    entries = {item["capability_id"]: item for item in registry["entries"]}
    entries["conversation.respond"]["provider_available"] = True
    entries["project.read"]["provider_available"] = True
    result = spine.run_canonical_semantic_turn(
        text="two independent goals", project_port=EvidencePort(), conversation_port=EvidencePort(),
        model_port=Model(registry, ("conversation.respond", "project.read")),
        final_brain_port=Final(),
        permission_port=__import__("MAKSIMAR_CORE_LIB.security_layer.semantic_policy", fromlist=["SemanticPolicyEvaluator"]).SemanticPolicyEvaluator(),
        identity=OWNER, registry_projection=registry,
        provider_ports={"existing_jarvis_final_brain": EvidencePort("existing_jarvis_final_brain")},
        defer_final_brain=True,
    )
    assert result["operation_status"] == "FINAL_BRAIN_PENDING"
    assert result["evidence_bundle"]["items"]
    assert result["provider_unavailable_steps"]
    completed = next(item for item in result["capability_truth"] if item["capability_id"] == "conversation.respond")
    unavailable = next(item for item in result["capability_truth"] if item["capability_id"] == "project.read")
    assert completed["executed"] is False and completed["execution_receipt_present"] is False
    assert unavailable["executed"] is False and unavailable["execution_receipt_present"] is False


def test_unknown_identity_understands_but_cannot_mutate():
    registry = projection()
    result = spine.run_canonical_semantic_turn(
        text="understand this mutation", project_port=EvidencePort(), conversation_port=EvidencePort(),
        model_port=Model(registry, ("open_browser",)), final_brain_port=Final(),
        permission_port=__import__("MAKSIMAR_CORE_LIB.security_layer.semantic_policy", fromlist=["SemanticPolicyEvaluator"]).SemanticPolicyEvaluator(),
        identity=IdentityContext("unknown", "http_unverified", "unknown", False, False),
        registry_projection=registry, provider_ports={},
    )
    assert result["understanding"] is not None
    assert result["selected_capabilities"] == ("open_browser", "conversation.respond")
    assert result["operation_status"] == "PARTIAL_POLICY_DENIED"
    decisions = {item["capability_id"]: item for item in result["permission_decision"]}
    assert decisions["open_browser"]["granted"] is False
    assert decisions["open_browser"]["approval_required"] is False
    assert decisions["conversation.respond"]["granted"] is True
    denied_step = next(
        step for step in result["execution_plan"]["steps"]
        if step["capability_id"] == "open_browser"
    )
    assert result["policy_denied_steps"] == (denied_step,)
    assert result["approval_required_steps"] == ()
    browser_truth = next(
        item for item in result["capability_truth"]
        if item["capability_id"] == "open_browser"
    )
    assert browser_truth["executed"] is False
    assert browser_truth["execution_receipt_present"] is False


def _conversation_turn(final_brain, *, defer=False):
    registry = projection()
    entry = next(item for item in registry["entries"] if item["capability_id"] == "conversation.respond")
    entry["provider_available"] = True
    adapter = __import__(
        "MAKSIMAR_SERVER.AI_ORCHESTRATION.conversation_evidence_adapter",
        fromlist=["ExistingConversationEvidenceAdapter"],
    ).ExistingConversationEvidenceAdapter()
    return spine.run_canonical_semantic_turn(
        text="ответь естественно", project_port=EvidencePort(), conversation_port=adapter,
        model_port=Model(registry, ("conversation.respond",)), final_brain_port=final_brain,
        permission_port=__import__("MAKSIMAR_CORE_LIB.security_layer.semantic_policy", fromlist=["SemanticPolicyEvaluator"]).SemanticPolicyEvaluator(),
        identity=OWNER, registry_projection=registry,
        provider_ports={"existing_jarvis_final_brain": adapter}, defer_final_brain=defer,
    )


def test_conversation_evidence_alone_has_no_complete_response_receipt():
    pending = _conversation_turn(Final(), defer=True)
    assert pending["operation_status"] == "FINAL_BRAIN_PENDING"
    assert pending["evidence_bundle"]["receipts"] == ()
    assert pending["evidence_bundle"]["limitations"] == ()
    truth = pending["capability_truth"][0]
    assert truth["executed"] is False and truth["execution_receipt_present"] is False


def test_sync_final_brain_owns_response_execution_receipt_and_empty_or_timeout_does_not():
    completed = _conversation_turn(Final())
    receipts = completed["evidence_bundle"]["receipts"]
    assert len(receipts) == 1
    assert receipts[0]["provider_id"] == "existing_jarvis_final_brain"
    assert receipts[0]["capability_id"] == "conversation.respond"
    assert completed["capability_truth"][0]["executed"] is True
    assert completed["generation_completed"] is True and completed["response_execution_status"] == "COMPLETE"
    assert completed["final_brain_result"]["model_call_used"] is True

    class Empty:
        def answer(self, **kwargs):
            del kwargs
            return {"ok": True, "response_text": "", "model_call_attempted": True,
                    "model_call_succeeded": True, "raw_output_present": False}

    empty = _conversation_turn(Empty())
    assert empty["evidence_bundle"]["receipts"] == ()
    assert empty["capability_truth"][0]["executed"] is False
    assert empty["response_execution_status"] == "NOT_EXECUTED"

    class Timeout:
        def answer(self, **kwargs):
            del kwargs
            raise TimeoutError("bounded timeout")

    timeout = _conversation_turn(Timeout())
    assert timeout["evidence_bundle"]["receipts"] == ()
    assert timeout["capability_truth"][0]["executed"] is False

    class Truncated:
        def answer(self, **kwargs):
            del kwargs
            return {
                "ok": True, "response_text": "partial", "model_call_attempted": True,
                "model_call_succeeded": True, "raw_output_present": True,
                "done": True, "done_reason": "length", "truncation": True,
            }

    truncated = _conversation_turn(Truncated())
    assert truncated["evidence_bundle"]["receipts"] == ()
    assert truncated["capability_truth"][0]["executed"] is False
    assert truncated["response_execution_status"] == "NOT_EXECUTED"


def test_stream_order_trace_empty_error_and_no_thinking(monkeypatch):
    trace_id = "trace_stream_contract"
    pending = {
        "operation_status": "FINAL_BRAIN_PENDING", "trace_id": trace_id,
        "selected_capabilities": ("conversation.respond",), "selected_provider_operation": ("respond",),
        "trace": {"trace_id": trace_id, "stages": ("api", "policy", "evidence_bundle")},
        "final_brain_input": {}, "approval_required_steps": (),
    }
    monkeypatch.setattr(spine, "run_canonical_semantic_turn", lambda **kwargs: dict(pending))

    class StreamFinal:
        def stream_answer(self, **kwargs):
            del kwargs
            yield {"event": "chunk", "chunk": "Готов"}
            yield {"event": "chunk", "chunk": "о."}
            yield {"event": "done", "response_text": "Готово.", "model_call_attempted": True,
                   "model_call_succeeded": True, "raw_output_present": True,
                   "done": True, "done_reason": "stop", "truncation": False}

    events = list(spine.stream_canonical_semantic_turn(final_brain_port=StreamFinal()))
    assert [item["event"] for item in events] == ["accepted", "status", "chunk", "chunk", "done"]
    assert {item["trace_id"] for item in events} == {events[0]["trace_id"]}
    assert events[-1]["response_text"] == "Готово."

    class EmptyFinal:
        def stream_answer(self, **kwargs):
            del kwargs
            yield {"event": "done", "response_text": ""}

    empty = list(spine.stream_canonical_semantic_turn(final_brain_port=EmptyFinal()))
    assert empty[-1]["event"] == "error"
    assert empty[-1]["error_kind"] == "final_brain_empty_result"
    state = {"inside": False}
    assert _filter_private_reasoning("<think>private</think>Visible", state) == "Visible"
    split_state = {"inside": False}
    assert _filter_private_reasoning("<thi", split_state) == ""
    assert _filter_private_reasoning("nk>private</thi", split_state) == ""
    assert _filter_private_reasoning("nk>Visible<", split_state) == "Visible"
    assert _flush_private_reasoning(split_state) == "<"


def test_stream_converts_unexpected_turn_exception_to_terminal_error(monkeypatch):
    def fail_closed(**kwargs):
        del kwargs
        raise ValueError("private internal detail")

    monkeypatch.setattr(spine, "run_canonical_semantic_turn", fail_closed)
    events = list(spine.stream_canonical_semantic_turn(final_brain_port=object()))
    assert [event["event"] for event in events] == ["accepted", "error"]
    assert events[-1]["error_kind"] == "canonical_semantic_turn_exception"
    assert events[-1]["error_message"] == "ValueError"
    assert "private internal detail" not in json.dumps(events)


def test_empty_candidate_projection_is_controlled_operation_discovery_failure():
    audit = {}
    assert spine._model_selected_operation_details(
        model_port=object(), deadline=RequestDeadline(5), original_text="привет",
        session_context={}, registry_projection={"entries": ()}, audit_trace=audit,
    ) is None
    assert audit["operation_discovery_error"] == "empty_candidate_projection"


def test_stream_receipt_exists_only_after_verified_done_and_delivery_stays_unknown(monkeypatch):
    pending = _conversation_turn(Final(), defer=True)
    monkeypatch.setattr(spine, "run_canonical_semantic_turn", lambda **kwargs: dict(pending))

    class StreamFinal:
        def stream_answer(self, **kwargs):
            del kwargs
            yield {"event": "chunk", "chunk": "Ответ"}
            yield {"event": "done", "response_text": "Ответ", "model_call_attempted": True,
                   "model_call_succeeded": True, "raw_output_present": True,
                   "done": True, "done_reason": "stop", "truncation": False}

    stream = spine.stream_canonical_semantic_turn(final_brain_port=StreamFinal())
    assert next(stream)["event"] == "accepted"
    assert next(stream)["event"] == "status"
    assert next(stream)["event"] == "chunk"
    assert pending["evidence_bundle"]["receipts"] == ()
    done = next(stream)
    assert done["event"] == "done"
    assert done["result"]["evidence_bundle"]["receipts"][0]["status"] == "COMPLETE"
    assert done["result"]["capability_truth"][0]["executed"] is True
    assert done["result"]["delivery_completed"] is None


def test_broken_pipe_never_claims_delivery_success(monkeypatch):
    event = {"event": "done", "result": {"delivery_completed": None}}
    monkeypatch.setattr(api_server, "_hot_stream_lines", lambda payload: iter((json.dumps(event) + "\n",)))
    captured = []

    def broken(line):
        captured.append(json.loads(line))
        raise BrokenPipeError("client disconnected")

    assert api_server.write_hot_stream_to_callable(broken, {"text": "x"}) is False
    assert captured[0]["result"]["delivery_completed"] is None


def test_not_executed_audits_use_null_not_false():
    root = Path("RUNTIME/audits/PERSONAL_JARVIS_RECOVERY_PHASE_1B_20260717_170146")
    multi = json.loads((root / "multi_turn_live_result.json").read_text())
    understanding = json.loads((root / "understanding_live_result.json").read_text())
    assert multi["status"] == "NOT_EXECUTED"
    assert multi["initial_five_turn_gate_passed"] is None
    assert multi["fifteen_turn_stability_passed"] is None
    assert multi["continuity_valid"] is None
    assert understanding["schema_valid"] is None


def test_family_profiles_receive_the_same_semantic_registry_brain():
    registry = projection()
    systems = []
    for identity in (
        OWNER,
        IdentityContext("yulia", "local_terminal_session", "trusted_family", False, True, "Юлия", "JARVIS"),
        IdentityContext("maksim", "local_terminal_session", "child", False, True, "Максим", "JARVIS"),
        IdentityContext("makar", "local_terminal_session", "child", False, True, "Макар", "JARVIS"),
    ):
        system, _ = spine.build_request_understanding_prompt(
            request_id="request_family", original_text="свободная речь", identity=identity,
            session_context={}, registry_projection=registry,
        )
        systems.append(system)
    assert len(set(systems)) == 1


def test_hot_negotiates_streaming_without_a_second_endpoint(monkeypatch):
    monkeypatch.setattr(api_server, "_hot_stream_lines", lambda payload: iter((json.dumps({"event": "accepted"}) + "\n",)))
    response = api_server.jarvis_live_hot({"text": "hello", "stream": True})
    assert response.media_type == "application/x-ndjson"
    assert api_server._payload_stream_requested({"response_mode": "stream"}) is True


def test_canonical_hot_writer_treats_broken_pipe_as_disconnect(monkeypatch):
    monkeypatch.setattr(api_server, "_hot_stream_lines", lambda payload: iter(("one\n", "two\n")))
    calls = []
    def broken(line):
        calls.append(line)
        raise BrokenPipeError
    assert api_server.write_hot_stream_to_callable(broken, {"text": "hello"}) is False
    assert calls == ["one\n"]


def test_transport_streams_visible_chunks_and_suppresses_thinking(monkeypatch):
    captured = {}
    class Response:
        def __enter__(self): return self
        def __exit__(self, *args): return False
        def raise_for_status(self): return None
        def iter_lines(self):
            return iter((
                json.dumps({"model": "jarvis:chat8b", "message": {"thinking": "private", "content": "Готов"}}),
                json.dumps({
                    "model": "jarvis:chat8b", "message": {"content": "о."},
                    "done": True, "done_reason": "stop",
                }),
            ))
    def fake_stream(method, url, **kwargs):
        captured.update({"method": method, "url": url, **kwargs})
        return Response()
    monkeypatch.setattr(transport.httpx, "stream", fake_stream)
    events = list(transport.grounded_final_brain_stream(
        original_text="answer", understanding={}, execution_plan={}, evidence_bundle={"items": ()},
        capability_state=(), session_context={}, identity_facts={}, timeout_seconds=10,
    ))
    assert captured["json"]["stream"] is True
    assert [event["event"] for event in events] == ["chunk", "chunk", "done"]
    serialized = json.dumps(events, ensure_ascii=False)
    assert "private" not in serialized
    assert events[-1]["response_text"] == "Готово."


def test_final_brain_treats_completed_delegated_model_proposal_as_answer_evidence():
    proposal = "Раздели валидацию и преобразование данных на две функции."
    payload = transport._grounded_final_brain_payload(
        original_text="Попроси локальную модель предложить план.",
        understanding={"goals": ({"description": "получить план"},)},
        execution_plan={"steps": ({
            "step_id": "step_model", "capability_id": "model_role:daily_coder_model",
            "operation": "draft_daily_code_proposal",
        },)},
        evidence_bundle={
            "status": "COMPLETE", "capability_ids": ("model_role:daily_coder_model",),
            "items": ({
                "kind": "model_role_proposal",
                "observation": json.dumps({
                    "model_id": "jarvis:coder7b", "proposal": proposal,
                    "proposal_only": True,
                }, ensure_ascii=False),
            },),
            "limitations": (), "errors": (),
            "receipts": ({"status": "COMPLETE"},),
        },
        capability_state=(), session_context={}, identity_facts={}, stream=True,
    )
    prompt = "\n".join(message["content"] for message in payload["messages"])
    assert proposal in prompt
    assert "proposal evidence is already generated" in prompt
    assert '"completed_delegated_proposal"' in prompt


def test_final_brain_projects_pending_step_as_explicit_nonexecution_truth():
    payload = transport._grounded_final_brain_payload(
        original_text="подготовь ввод, но не выполняй без подтверждения",
        understanding={"goals": (), "operation_requirements": ()},
        execution_plan={"steps": ({
            "step_id": "step_pending", "capability_id": "type_text",
            "operation": "execute_type_text",
        },)},
        evidence_bundle={
            "status": "COMPLETE", "capability_ids": (), "items": (),
            "limitations": ("step_not_executed:step_pending:execute_type_text",),
            "errors": (), "receipts": (),
        },
        capability_state=({
            "capability_id": "type_text", "provider_id": "windows_edge_adapter",
            "provider_available": True, "policy_execution_allowed": False,
            "executed": False, "execution_receipt_present": False,
            "approval_required": True,
        },),
        session_context={}, identity_facts={}, stream=True,
    )
    prompt = "\n".join(message["content"] for message in payload["messages"])
    assert '"nonexecuted_steps":[["type_text","execute_type_text","PENDING_APPROVAL"]]' in prompt
    assert '"nonexecuted_operations":[["type_text","execute_type_text","PENDING_APPROVAL"]]' in prompt
    assert "PENDING_APPROVAL may be a prepared proposal, never execution" in prompt
    assert "never describe a nonexecuted operation as executed" in prompt
    assert transport._final_brain_prompt_budget(payload)["within_budget"] is True


def test_final_brain_prompt_bounds_large_git_evidence_and_preserves_dirty_truth():
    files = [f"path/{index}/file.py" for index in range(100)]
    evidence = {
        "request_id": "request", "trace_id": "trace", "status": "COMPLETE",
        "capability_ids": ("project.read",),
        "items": ({
            "kind": "git_status", "source": "existing_project_workspace_tools:inspect_git_status",
            "observation": json.dumps({
                "branch": "feature/live", "head": "abc123", "read_only": True,
                "modified_files": files, "modified_file_count": 100,
                "deleted_files": files, "deleted_file_count": 100,
                "untracked_files": files, "untracked_file_count": 100,
                "staged_files": [], "staged_file_count": 0,
                "dirty_files": files, "dirty_file_count": 300,
                "diff_stat": "x" * 10000,
            }),
        },),
        "limitations": (), "errors": (), "receipts": (),
    }
    payload = transport._grounded_final_brain_payload(
        original_text="кратко опиши состояние", understanding={"goals": (), "operation_requirements": ()},
        execution_plan={"request_id": "request", "steps": ()}, evidence_bundle=evidence,
        capability_state=(), session_context={}, identity_facts={}, stream=False,
    )
    budget = transport._final_brain_prompt_budget(payload)
    prompt = "".join(message["content"] for message in payload["messages"])
    assert budget["within_budget"] is True
    assert payload["options"]["num_predict"] == 420
    assert payload["think"] is False
    assert payload["messages"][-1]["content"].startswith("CURRENT REQUEST: кратко опиши состояние")
    assert "do not repeat a prior answer" in payload["messages"][0]["content"]
    assert "without service commentary" in payload["messages"][0]["content"]
    assert "under 80 words" in prompt
    assert "DIRTY with nonzero counts means uncommitted changes, never clean" in prompt
    assert '"git_worktree_status":"DIRTY"' in prompt
    assert '"dirty_tracked_total_count":300' in prompt
    assert '"mandatory_answer_facts":{"git_worktree":{"branch":"feature/live","git_worktree_status":"DIRTY","modified_tracked_count":100,"deleted_tracked_count":100,"untracked_count":100,"dirty_tracked_total_count":300}}' in prompt
    assert prompt.count('"mandatory_answer_facts"') == 1
    assert "Communicate every MANDATORY_ANSWER_FACTS value" in prompt
    assert "never relabel untracked as added/staged" in prompt
    assert "изменённых отслеживаемых: N; удалённых отслеживаемых: N" in prompt
    assert "N неотслеживаемых файлов; всего грязных отслеживаемых: N" in prompt
    assert "Omitting the fourth dirty-total count is invalid" in prompt
    assert "use «добавлено/добавленные» for untracked" in prompt
    assert '"read_only"' not in prompt
    assert '"risk_class":"READ_ONLY"' not in prompt
    assert "Execution constraints are not worktree state" in prompt
    assert "For every NONEXECUTED_STEPS row communicate its exact status naturally" in prompt
    assert "PENDING_APPROVAL may be a prepared proposal, never execution" in prompt
    assert files[0] not in prompt
    assert files[-1] not in prompt
    assert "x" * 100 not in prompt


def test_final_brain_preserves_complete_git_truth_with_other_bounded_project_evidence():
    files = [f"path/{index}.py" for index in range(100)]
    evidence = {
        "status": "COMPLETE", "capability_ids": ("project.read",),
        "items": (
            {"kind": "git_status", "observation": json.dumps({
                "branch": "deflation/live-hotpath-reset-v1", "head": "abc123", "read_only": True,
                "modified_files": files[:40], "modified_file_count": 100,
                "deleted_files": [], "deleted_file_count": 0,
                "untracked_files": files[:40], "untracked_file_count": 100,
                "staged_files": [], "staged_file_count": 0,
                "dirty_files": files[:40], "dirty_file_count": 200,
            })},
            {"kind": "changed_files", "observation": json.dumps({
                "branch": "deflation/live-hotpath-reset-v1",
                "modified_files": files[:40], "modified_file_count": 100,
                "deleted_files": [], "deleted_file_count": 0,
                "untracked_files": files[:40], "untracked_file_count": 100,
                "staged_files": [], "staged_file_count": 0,
            })},
            {"kind": "inspect_structure", "observation": json.dumps({
                "files": {"files": files[:40], "total_files": 6075},
                "tree": {"entries": files[:40], "entry_count": 120},
            })},
        ),
        "limitations": ("large collections retain explicit counts and bounded samples",),
        "errors": (), "receipts": (),
    }
    payload = transport._grounded_final_brain_payload(
        original_text="кратко опиши состояние", understanding={"goals": (), "operation_requirements": ()},
        execution_plan={"steps": ()}, evidence_bundle=evidence, capability_state=(),
        session_context={}, identity_facts={}, stream=False,
    )
    prompt = "".join(message["content"] for message in payload["messages"])
    assert transport._final_brain_prompt_budget(payload)["within_budget"] is True
    assert '"branch":"deflation/live-hotpath-reset-v1"' in prompt
    assert '"count":100' in prompt
    assert '"modified_tracked_files"' in prompt
    assert '"dirty_tracked_total_count":200' in prompt
    assert '"git_worktree_status":"DIRTY"' in prompt
    assert '"read_only"' not in prompt
    assert '"detail_compacted_for_prompt":true' not in prompt
    assert "COMPLETE counted evidence stays complete despite bounded samples" in prompt
    assert "never call it partial merely for sampling" in prompt
    assert "never echo JSON field names or internal schema labels" in prompt


def test_final_brain_prompt_recursively_bounds_nested_project_evidence():
    nested = {
        "files": {
            "files": [f"path/{index}/file.py" for index in range(500)],
            "total_files": 6075,
        },
        "tree": {
            "entries": [f"directory/{index}/" for index in range(500)],
            "entry_count": 500,
        },
    }
    evidence = {
        "request_id": "request", "trace_id": "trace", "status": "COMPLETE",
        "capability_ids": ("project.read",),
        "items": ({
            "kind": "inspect_structure",
            "source": "existing_project_workspace_tools:inspect_structure",
            "observation": json.dumps(nested),
        },),
        "limitations": (), "errors": (), "receipts": (),
    }
    payload = transport._grounded_final_brain_payload(
        original_text="кратко опиши состояние",
        understanding={"goals": (), "operation_requirements": ()},
        execution_plan={"request_id": "request", "steps": ()},
        evidence_bundle=evidence, capability_state=(), session_context={},
        identity_facts={}, stream=False,
    )
    prompt = "".join(message["content"] for message in payload["messages"])
    budget = transport._final_brain_prompt_budget(payload)
    assert budget["within_budget"] is True
    assert '"observed_bounded_count":500' in prompt
    assert "path/499/file.py" not in prompt
    assert "directory/499/" not in prompt


def test_final_brain_preserves_exact_project_search_locators_without_prompt_overflow():
    evidence = {
        "status": "COMPLETE", "capability_ids": ("project.read",),
        "items": (
            {"kind": "inspect_structure", "observation": json.dumps({
                "files": {"files": [f"path/{index}.py" for index in range(40)], "total_files": 6075},
                "tree": {"entries": [f"directory/{index}/" for index in range(120)], "entry_count": 120},
            })},
            {"kind": "search", "observation": json.dumps({
                "query": "EvidenceBundle", "result_count": 20,
                "results": [
                    {"path": "./CONTROL_PLANE/canonical_semantic_spine.py", "line_number": 29,
                     "line": "EvidenceBundle,"},
                    {"path": "./MAKSIMAR_CORE_LIB/ai_orchestration/semantic_intent_contract.py",
                     "line_number": 303, "line": "class EvidenceBundle:"},
                ] + [
                    {"path": f"./other/{index}.py", "line_number": index, "line": "EvidenceBundle"}
                    for index in range(18)
                ],
            })},
        ),
        "limitations": (), "errors": (), "receipts": ({"status": "COMPLETE"},),
    }
    payload = transport._grounded_final_brain_payload(
        original_text="покажи структуру и где определяется EvidenceBundle",
        understanding={"goals": (), "operation_requirements": ()},
        execution_plan={"steps": ()}, evidence_bundle=evidence,
        capability_state=(), session_context={
            "current_topic": "project structure and source search",
            "unresolved_reference": {"present": False, "description": ""},
            "recent_relevant_turns": ({
                "user_text": "Безопасно проверь текущий Git-статус рабочего дерева и кратко объясни.",
                "assistant_text": "Рабочее дерево содержит подтверждённые незакоммиченные изменения.",
                "topic": "project status",
            },) * 4,
        }, identity_facts=OWNER.to_read_model(), stream=True,
    )
    prompt = "".join(message["content"] for message in payload["messages"])

    assert transport._final_brain_prompt_budget(payload)["within_budget"] is True
    assert "./CONTROL_PLANE/canonical_semantic_spine.py" in prompt
    assert "./MAKSIMAR_CORE_LIB/ai_orchestration/semantic_intent_contract.py" in prompt
    assert '"primary_project_search_match"' in prompt
    assert '"line_number":29' in prompt
    assert "never synthesize a conventional path" in prompt
    assert "/src/main/java" not in prompt


def test_final_brain_does_not_duplicate_conversation_identity_and_context_evidence():
    evidence = {
        "request_id": "request", "trace_id": "trace", "status": "COMPLETE",
        "capability_ids": ("project.read", "conversation.respond"),
        "items": (
            {"kind": "git_status", "observation": json.dumps({"branch": "feature/live"})},
            {"kind": "identity_facts", "observation": json.dumps({"identity_id": "aleksandr"})},
            {"kind": "bounded_session_context", "observation": json.dumps({
                "bounded_chronological_turns": [{"text": "duplicate me"}] * 40,
            })},
        ),
        "limitations": (), "errors": (), "receipts": (),
    }
    payload = transport._grounded_final_brain_payload(
        original_text="кратко опиши состояние",
        understanding={"goals": (), "operation_requirements": ()},
        execution_plan={"request_id": "request", "steps": ()},
        evidence_bundle=evidence, capability_state=(), session_context={},
        identity_facts={"identity_id": "aleksandr"}, stream=False,
    )
    prompt = "".join(message["content"] for message in payload["messages"])
    assert transport._final_brain_prompt_budget(payload)["within_budget"] is True
    assert prompt.count('"identity_id":"aleksandr"') == 1
    assert "duplicate me" not in prompt
    assert '"identity_and_context_supplied_separately":true' in prompt


def test_final_brain_bounds_multi_turn_context_with_multi_operation_evidence():
    evidence_items = tuple({
        "kind": kind,
        "observation": json.dumps({
            "summary": "x" * 800,
            "rows": [f"{kind}-{index}-" + ("y" * 200) for index in range(40)],
        }),
    } for kind in (
        "diff_summary", "inspect_structure", "inspect_dependencies",
        "inspect_imports", "inspect_tests", "inspect_architecture",
    ))
    session_context = {
        "current_topic": "project structure",
        "unresolved_reference": {"present": True, "description": "previous project state"},
        "recent_relevant_turns": tuple({
            "user_text": "u" * 400,
            "assistant_text": "a" * 800,
            "topic": "t" * 200,
            "trace_id": f"trace-{index}",
        } for index in range(6)),
    }
    payload = transport._grounded_final_brain_payload(
        original_text="подведи итог по структуре проекта",
        understanding={
            "goals": ({"description": "project summary"},),
            "operation_requirements": tuple(
                {"capability_id": "project.read", "operation_id": kind}
                for kind in (
                    "inspect_diff_summary", "inspect_structure", "inspect_dependencies",
                    "inspect_imports", "inspect_tests", "inspect_architecture",
                )
            ),
        },
        execution_plan={"request_id": "request", "steps": ()},
        evidence_bundle={
            "status": "COMPLETE", "capability_ids": ("project.read",),
            "items": evidence_items, "limitations": (), "errors": (), "receipts": (),
        },
        capability_state=(), session_context=session_context,
        identity_facts={"identity_id": "aleksandr"}, stream=False,
    )
    prompt = "".join(message["content"] for message in payload["messages"])

    assert transport._final_brain_prompt_budget(payload)["within_budget"] is True
    assert '"recent_relevant_turn_count":6' in prompt
    assert '"context_bounded_for_prompt":true' in prompt
    assert "trace-0" not in prompt
    assert ("a" * 300) not in prompt


def test_authoritative_pass_covers_canonical_owner_when_kind_misses_it():
    # The authoritative executable pass selects the canonical owners even when the
    # model-selected kinds omit canonical_capability (reconciliation-by-authoritative).
    result = run_selection(("project.read",))
    assert result["selected_capabilities"] == ("project.read", "conversation.respond")
    trace = result["trace"] if isinstance(result.get("trace"), dict) else {}
    cd = trace.get("candidate_discovery") or {}
    hd = cd.get("hierarchical_discovery") or {}
    assert "authoritative_executable_selected_ids" in hd


def test_coarse_kind_miss_cannot_hide_authoritative_executable_candidate_scope():
    registry = projection()
    class CoarseModel:
        def __init__(self):
            self.kind_calls = 0
        def discover_kinds(self, **kwargs):
            self.kind_calls += 1
            # Select only one coarse non-canonical kind, omitting canonical_capability.
            selected = {"readonly_tool": True}
            return model_call_envelope(json.dumps({
                "candidate_kinds": selected, "continuation_required": False, "continuation_reason": "",
                "ambiguity_present": False, "confidence": .9, "reason_codes": ["coarse_kind"],
            }))
        def discover_candidates(self, **kwargs):
            allowed = tuple(_candidate_slot_enum(kwargs["output_schema"]))
            selected = {v: True for v in allowed if v in ("conversation.respond", "project.read")}
            return model_call_envelope(json.dumps({
                "candidate_capability_ids": selected, "continuation_required": False, "continuation_reason": "",
                "ambiguity_present": False, "confidence": .9, "reason_codes": ["authoritative"],
            }))
        def understand(self, *, system_prompt, user_prompt, deadline):
            return model_call_envelope(json.dumps({
                "schema_version": "request_understanding.v2", "language": "ru",
                "goals": [{"goal_id": "g1", "description": "git status"}],
                "required_capabilities": [
                    {"capability_id": "project.read", "purpose": "read worktree", "required": True,
                     "operation_contract_required": True, "unresolved_operation_reason": ""},
                    {"capability_id": "conversation.respond", "purpose": "answer", "required": True,
                     "operation_contract_required": True, "unresolved_operation_reason": ""},
                ],
            "response_requirements": [],
                "effect_type": "OBSERVE", "target_scope": "local_project_worktree", "reversibility": "reversible",
                "external_side_effect": False, "unresolved_capabilities": [], "operation_requirements": [],
                "current_topic": "", "unresolved_reference": "", "risk_class": "READ_ONLY", "confidence": .9,
                "reason_codes": ["git"],
            }))
    m = CoarseModel()
    registry["entries"] = tuple(e for e in registry["entries"] if e["capability_id"] != "read_file_outline")
    details = spine._model_selected_registry_details(
        model_port=m, deadline=RequestDeadline(60),
        original_text="Безопасно проверь текущий Git-статус рабочего дерева.",
        session_context={}, registry_projection=registry, audit_trace={},
        request_id="r", identity=OWNER, input_preparation={},
    )
    assert details is not None
    ids = {str(e["capability_id"]) for e in details["entries"]}
    assert "conversation.respond" in ids and "project.read" in ids


def test_large_kind_uses_neutral_budget_chunks_without_losing_any_capability():
    registry = projection()
    kp = spine.projection_for_kinds(registry, ("readonly_tool",))
    groups = spine._candidate_budget_groups(
        original_text="покажи структуру", session_context={}, registry_projection=kp,
    )
    union = [str(e["capability_id"]) for gp, _ in groups for e in gp["entries"]]
    assert len(union) == len(set(union))
    assert set(union) == {str(e["capability_id"]) for e in kp["entries"]}


def test_bounded_cross_kind_union_is_preserved_without_consolidation_re_selection():
    registry = projection()
    ids = ("conversation.respond", "project.read")
    class NoConsolidationModel:
        def discover_candidates(self, **kwargs):
            raise AssertionError("must not re-select a bounded model-selected set")
    result, audit = spine._consolidate_candidate_ids_if_needed(
        call=NoConsolidationModel().discover_candidates, candidate_ids=ids,
        original_text="прочитай проект", session_context={}, registry_projection=registry,
        deadline=RequestDeadline(10), trace=[], audit_trace=[], repair_state={},
    )
    assert tuple(result) == ids
    assert audit["status"] == "NOT_REQUIRED_ALREADY_BOUNDED"


def test_over_budget_selected_kind_combination_preserves_authoritative_set(monkeypatch):
    registry = projection()
    ids = ("conversation.respond", "project.read", "runtime_history_store", "session_memory", "vector_runtime_indexes")
    def over_budget(**kwargs):
        return {"within_budget": False, "operation_count": 999, "candidate_count": len(ids)}
    monkeypatch.setattr(spine, "_measure_operation_discovery_budget", over_budget)
    class ConsolidateModel:
        def __init__(self):
            self.calls = 0
        def discover_candidates(self, **kwargs):
            self.calls += 1
            allowed = tuple(_candidate_slot_enum(kwargs["output_schema"]))
            selected = {v: True for v in allowed[:2]}
            return model_call_envelope(json.dumps({
                "candidate_capability_ids": selected, "continuation_required": False, "continuation_reason": "",
                "ambiguity_present": False, "confidence": .9, "reason_codes": ["bounded_subset"],
            }))
    model = ConsolidateModel()
    result, audit = spine._consolidate_candidate_ids_if_needed(
        call=model.discover_candidates, candidate_ids=ids, original_text="прочитай историю",
        session_context={}, registry_projection=registry, deadline=RequestDeadline(10),
        trace=[], audit_trace=[], repair_state={},
    )
    assert model.calls == 0
    assert tuple(result) == ids
    assert audit["status"] == "NOT_REQUIRED_ALREADY_BOUNDED"


def test_response_only_candidate_continues_through_model_selected_executable_evidence_kind():
    result = run_selection(("conversation.respond",))
    assert result["selected_capabilities"] == ("conversation.respond",)


def test_kind_false_positive_may_finish_empty_without_blocking_response():
    registry = projection()
    class FalsePositiveModel:
        def discover_kinds(self, **kwargs):
            allowed = tuple(kwargs["output_schema"]["properties"]["candidate_kinds"]["properties"])
            selected = {k: True for k in allowed if k == "retrieval_tool"}
            return model_call_envelope(json.dumps({
                "candidate_kinds": selected, "continuation_required": False, "continuation_reason": "",
                "ambiguity_present": False, "confidence": .5, "reason_codes": ["retrieval"],
            }))
        def discover_candidates(self, **kwargs):
            allowed = tuple(_candidate_slot_enum(kwargs["output_schema"]))
            selected = {v: True for v in allowed if v in ("conversation.respond", "project.read")}
            return model_call_envelope(json.dumps({
                "candidate_capability_ids": selected, "continuation_required": False, "continuation_reason": "",
                "ambiguity_present": False, "confidence": .9, "reason_codes": ["authoritative"],
            }))
        def understand(self, *, system_prompt, user_prompt, deadline):
            return model_call_envelope(json.dumps({
                "schema_version": "request_understanding.v2", "language": "ru",
                "goals": [{"goal_id": "g1", "description": "greeting"}],
                "required_capabilities": [
                    {"capability_id": "conversation.respond", "purpose": "answer", "required": True,
                     "operation_contract_required": True, "unresolved_operation_reason": ""},
                ],
            "response_requirements": [],
                "effect_type": "OBSERVE", "target_scope": "bounded_same_identity_session", "reversibility": "reversible",
                "external_side_effect": False, "unresolved_capabilities": [], "operation_requirements": [],
                "current_topic": "", "unresolved_reference": "", "risk_class": "READ_ONLY", "confidence": .9,
                "reason_codes": ["conversation"],
            }))
    m = FalsePositiveModel()
    details = spine._model_selected_registry_details(
        model_port=m, deadline=RequestDeadline(60), original_text="Как дела, брат мой?",
        session_context={}, registry_projection=registry, audit_trace={},
        request_id="r", identity=OWNER, input_preparation={},
    )
    assert details is not None
    ids = {str(e["capability_id"]) for e in details["entries"]}
    assert "conversation.respond" in ids


def test_goalframe_projection_is_safety_monotonic():
    registry = projection()
    # observe intent must never recover MUTATE/EXECUTE caps (safety-monotonic ceiling)
    obs = spine._goalframe_projection(registry, semantic_domain="windows", effect_intent="observe")
    assert "read_screen" in obs
    assert not any(c in obs for c in ("volume_up", "volume_down", "type_text", "browser_search", "open_browser"))
    # change_state may recover MUTATE, but never EXECUTE
    cs = spine._goalframe_projection(registry, semantic_domain="windows", effect_intent="change_state")
    assert "volume_up" in cs and "type_text" in cs
    # compute_run (danger 2) still recovers the read-only project owner (T14 drift)
    pr = spine._goalframe_projection(registry, semantic_domain="project", effect_intent="compute_run")
    assert "project.read" in pr
    # invariant: every recovered cap's max effect danger <= intent danger
    for dom, eff in (("windows", "observe"), ("windows", "change_state"), ("project", "compute_run"),
                     ("model", "reason_propose"), ("simulation", "compute_run")):
        intent_danger = max(spine._effect_danger(t) for t in spine.SEMANTIC_EFFECT_INTENTS[eff])
        for cid in spine._goalframe_projection(registry, semantic_domain=dom, effect_intent=eff):
            entry = next(e for e in registry["entries"] if str(e["capability_id"]) == cid)
            effects = {str(o["effect_type"]) for o in entry.get("operation_contracts") or () if o.get("effect_type")}
            assert effects, cid
            assert max(spine._effect_danger(e) for e in effects) <= intent_danger, (dom, eff, cid, effects)


def test_goalframe_owns_precise_source_grounded_artifact_operations():
    prefix = "Create a local inactive workflow with several harmless preparation details, validation branches, and review notes. "
    late = "Later the workflow must send the final record through Named Service."
    source = prefix + late
    goal = {
        "goal_id": "g1", "semantic_domain": "automation", "effect_intent": "change_state",
        "requested_outcome": "create the workflow", "grounding": source,
        "goal_role": "PRIMARY_OUTCOME", "parent_goal_id": "",
        "subgoal_justification_kind": "NONE",
        "artifact_operation_requirements": ({
            "requirement_id": "send_1", "goal_id": "g1", "operation_class": "SEND",
            "source_grounding": "send the final record through Named Service",
            "provider_name": "Named Service", "provider_provenance": "SOURCE_EXPLICIT",
            "provider_inference_justification": "",
        },),
    }
    assert spine._goalframe_validation_violations([goal], source_text=source) == ()
    assert len(source) > 160
    assert source.index("send the final record") > 100

    missing = dict(goal, artifact_operation_requirements=())
    assert ("g1", "automation_artifact_operations_missing") in spine._goalframe_validation_violations(
        [missing], source_text=source,
    )

    intrinsic_source = "Create an n8n workflow that doubles each amount."
    intrinsic = dict(goal, grounding=intrinsic_source, artifact_operation_requirements=({
        "requirement_id": "transform_1", "goal_id": "g1", "operation_class": "TRANSFORM",
        "source_grounding": "doubles each amount", "provider_name": "n8n",
        "provider_provenance": "SOURCE_EXPLICIT", "provider_inference_justification": "",
    },))
    assert ("transform_1", "intrinsic_artifact_operation_has_provider") in (
        spine._goalframe_validation_violations([intrinsic], source_text=intrinsic_source)
    )

    duplicated_goal = dict(goal, grounding=intrinsic_source, artifact_operation_requirements=({
        "requirement_id": "host_create", "goal_id": "g1", "operation_class": "GENERATE",
        "source_grounding": intrinsic_source, "provider_name": "",
        "provider_provenance": "NONE", "provider_inference_justification": "",
    },))
    assert ("host_create", "artifact_operation_duplicates_goal_fact") in (
        spine._goalframe_validation_violations([duplicated_goal], source_text=intrinsic_source)
    )

    missing_provider = dict(goal, artifact_operation_requirements=({
        "requirement_id": "send_missing_provider", "goal_id": "g1", "operation_class": "SEND",
        "source_grounding": "send the final record through Named Service", "provider_name": "",
        "provider_provenance": "NONE", "provider_inference_justification": "",
    },))
    assert ("send_missing_provider", "real_artifact_operation_provider_missing") in (
        spine._goalframe_validation_violations([missing_provider], source_text=source)
    )


def test_goalframe_discovery_path_binds_every_goal():
    registry = projection()

    class GFModel:
        def __init__(self):
            self.understand_calls = 0
            self.discover_calls = 0

        def understand(self, *, system_prompt, user_prompt, deadline, output_schema=None):
            self.understand_calls += 1
            return model_call_envelope(json.dumps({"goals": [
                {"goal_id": "w1", "semantic_domain": "windows", "effect_intent": "observe",
                 "requested_outcome": "see screen", "grounding": "посмотри экран", "ambiguity": "",
                 "goal_role": "PRIMARY_OUTCOME", "parent_goal_id": "",
                 "subgoal_justification_kind": "NONE"},
                {"goal_id": "w2", "semantic_domain": "windows", "effect_intent": "change_state",
                 "requested_outcome": "type text", "grounding": "введи текст", "ambiguity": "",
                 "goal_role": "PRIMARY_OUTCOME", "parent_goal_id": "",
                 "subgoal_justification_kind": "NONE"},
            ]}))

        def discover_candidates(self, **kwargs):
            self.discover_calls += 1
            # GoalBinding schema: {status, capability_id, reason}
            goal_id = json.loads(kwargs["user_prompt"])["goal_id"]
            cap = {"w1": "read_screen", "w2": "type_text"}[goal_id]
            return model_call_envelope(json.dumps({
                "status": "BOUND", "capability_id": cap, "reason": "x",
            }))

        def verify_source_candidate(self, *, source_text, candidate, deadline):
            # Explicit controlled judgment for this test request, not natural proof.
            verdict = {"status": "COMPLETE", "supported": list(("goal:w1", "goal:w2")),
                       "missing": [], "contradictions": [], "unsupported_claims": [],
                       "reason": "Independent controlled fixture judgment"}
            return {"verdict": verdict, "model_call": model_call_envelope(json.dumps(verdict))}

    m = GFModel()
    audit = {}
    result = spine._model_selected_registry_details(
        model_port=m, deadline=RequestDeadline(60), original_text="посмотри экран и введи текст",
        session_context={}, registry_projection=registry, audit_trace=audit,
        request_id="r", identity=OWNER, input_preparation={},
    )
    assert result is not None
    ids = {str(e["capability_id"]) for e in result["entries"]}
    assert "read_screen" in ids and "type_text" in ids and "conversation.respond" in ids
    assert m.understand_calls == 1
    assert audit.get("candidate_discovery", {}).get("strategy") == "GOALFRAME_V3_INTENT_TO_BINDING"


def test_goalframe_prompt_preserves_comparison_effect_under_project_file_restriction():
    system, _user = spine.build_goalframe_understanding_prompt(
        original_text="Compare two approaches on identical checks without changing project files.",
        global_projection={"entries": ({"semantic_owner_id": "simulation.run", "supported_effects": ("EXECUTE",)},)},
    )
    assert "restriction constrains effects" in system
    assert "(simulation, compute_run)" in system


def test_semantic_owner_operation_candidates_are_compact_and_exact() -> None:
    """Compact semantic owners must yield exactly their own operations (no cross-owner leak)."""
    from MAKSIMAR_SERVER.SKILL_ADAPTER_REGISTRY.existing_capability_inventory import (
        resolve_semantic_owner_operation_candidates,
    )

    def ids(owner):
        return tuple(sorted(o["operation_id"] for o in resolve_semantic_owner_operation_candidates(owner)))

    assert ids("windows.volume") == (
        "execute_volume_down", "execute_volume_mute_toggle", "execute_volume_up",
    )
    assert ids("windows.input") == ("execute_type_text",)
    assert ids("screen.observe") == ("observe_windows_screen",)
    browser = ids("windows.browser")
    assert "execute_open_browser" in browser and "execute_browser_search" in browser
    assert "execute_volume_up" not in browser  # no cross-owner leakage
    assert resolve_semantic_owner_operation_candidates("owner_does_not_exist") == ()

    vol = resolve_semantic_owner_operation_candidates("windows.volume")[0]
    assert "operation_id" in vol and "evidence_kinds" in vol and "effect_type" in vol
    assert "required_parameters" in vol and "reversibility" in vol


def test_operation_contract_required_is_semantic_need_not_catalog_membership() -> None:
    """Authoritative mode: a goal for an unsupported capability keeps operation_contract_required=true
    (semantic need); catalog absence only sets the unresolved reason. It never becomes false."""
    from MAKSIMAR_CORE_LIB.ai_orchestration.helper_model_decision_parser import (
        parse_request_understanding_payload,
    )
    catalog = ({
        "capability_id": "conversation.respond", "operation_id": "respond",
        "required_parameters": (), "operation_description": "respond",
        "evidence_kinds": ("conversation",), "effect_type": "OBSERVE",
        "target_scope": "bounded_same_identity_session", "reversibility": "REVERSIBLE",
        "external_side_effect": False, "risk_class": "READ_ONLY",
    },)
    payload = {
        "schema_version": "request_understanding.v2", "language": "en",
        "goals": [
            {"goal_id": "g1", "description": "do an unsupported external action"},
            {"goal_id": "g2", "description": "respond"},
        ],
        "required_capabilities": [
            {"capability_id": "some.unsupported", "purpose": "unsupported", "required": True},
            {"capability_id": "conversation.respond", "purpose": "respond", "required": True},
        ],
            "response_requirements": [],
        "effect_type": "EXECUTE", "target_scope": "unknown", "reversibility": "UNKNOWN",
        "external_side_effect": None, "unresolved_capabilities": [],
        "operation_requirements": {"respond": {}},
        "current_topic": "", "unresolved_reference": "",
        "risk_class": "UNKNOWN", "confidence": 0.8, "reason_codes": ["unsupported"],
    }
    understanding = parse_request_understanding_payload(
        payload, host_request_id="r1", host_original_text="do unsupported",
        authoritative_operation_catalog=catalog,
    )
    unsupported = next(
        r for r in understanding.required_capabilities if r.capability_id == "some.unsupported"
    )
    assert unsupported.operation_contract_required is True  # semantic need, NOT catalog membership
    assert unsupported.unresolved_operation_reason == "authoritative_operation_not_selected"


def test_response_requirement_is_distinct_typed_object_not_a_capability() -> None:
    """T11 A/F: a ResponseRequirement is parsed as its own type and never enters
    required_capabilities / operation discovery."""
    from MAKSIMAR_CORE_LIB.ai_orchestration.helper_model_decision_parser import (
        parse_request_understanding_payload,
    )
    from MAKSIMAR_CORE_LIB.ai_orchestration.semantic_intent_contract import ResponseRequirement
    catalog = ({
        "capability_id": "conversation.respond", "operation_id": "respond",
        "required_parameters": (), "operation_description": "respond",
        "evidence_kinds": ("conversation",), "effect_type": "OBSERVE",
        "target_scope": "bounded_same_identity_session", "reversibility": "REVERSIBLE",
        "external_side_effect": False, "risk_class": "READ_ONLY",
    },)
    payload = {
        "schema_version": "request_understanding.v2", "language": "en",
        "goals": [{"goal_id": "g1", "description": "change volume"}],
        "required_capabilities": [
            {"capability_id": "conversation.respond", "purpose": "respond", "required": True},
        ],
        "response_requirements": [
            {"response_requirement_id": "r1", "applies_to_goal_ids": ["g1"], "description": "report result"},
        ],
        "effect_type": "OBSERVE", "target_scope": "bounded_same_identity_session",
        "reversibility": "REVERSIBLE", "external_side_effect": None, "unresolved_capabilities": [],
        "operation_requirements": {"respond": {}},
        "current_topic": "", "unresolved_reference": "",
        "risk_class": "READ_ONLY", "confidence": 0.9, "reason_codes": ["typed"],
    }
    understanding = parse_request_understanding_payload(
        payload, host_request_id="r1", host_original_text="change volume and tell me",
        authoritative_operation_catalog=catalog,
    )
    assert len(understanding.response_requirements) == 1
    rr = understanding.response_requirements[0]
    assert isinstance(rr, ResponseRequirement)
    assert rr.response_requirement_id == "r1"
    assert rr.applies_to_goal_ids == ("g1",)
    assert understanding.to_read_model()["response_requirements"] == (rr.to_read_model(),)
    import pytest
    with pytest.raises(ValueError, match="every response requirement must be an object"):
        parse_request_understanding_payload(
            {**payload, "response_requirements": [*payload["response_requirements"], None]},
            host_request_id="r1", host_original_text="change volume and tell me",
            authoritative_operation_catalog=catalog,
        )
    # r1 is NOT a CapabilityRequirement -> never enters operation discovery
    assert [c.capability_id for c in understanding.required_capabilities] == ["conversation.respond"]


def test_response_requirement_referencing_unknown_goal_fails_closed() -> None:
    """T11 D: a ResponseRequirement referencing an unknown goal_id fails typed validation."""
    from MAKSIMAR_CORE_LIB.ai_orchestration.helper_model_decision_parser import (
        parse_request_understanding_payload,
    )
    import pytest
    catalog = ({
        "capability_id": "conversation.respond", "operation_id": "respond",
        "required_parameters": (), "operation_description": "respond",
        "evidence_kinds": ("conversation",), "effect_type": "OBSERVE",
        "target_scope": "bounded_same_identity_session", "reversibility": "REVERSIBLE",
        "external_side_effect": False, "risk_class": "READ_ONLY",
    },)
    payload = {
        "schema_version": "request_understanding.v2", "language": "en",
        "goals": [{"goal_id": "g1", "description": "change volume"}],
        "required_capabilities": [
            {"capability_id": "conversation.respond", "purpose": "respond", "required": True},
        ],
        "response_requirements": [
            {"response_requirement_id": "r1", "applies_to_goal_ids": ["g_unknown"]},
        ],
        "effect_type": "OBSERVE", "target_scope": "bounded_same_identity_session",
        "reversibility": "REVERSIBLE", "external_side_effect": None, "unresolved_capabilities": [],
        "operation_requirements": {"respond": {}},
        "current_topic": "", "unresolved_reference": "",
        "risk_class": "READ_ONLY", "confidence": 0.9, "reason_codes": ["typed"],
    }
    with pytest.raises(ValueError, match="unknown goal_id"):
        parse_request_understanding_payload(
            payload, host_request_id="r1", host_original_text="x",
            authoritative_operation_catalog=catalog,
        )


def test_shared_response_requirement_covers_multiple_goals_without_extra_operation() -> None:
    """T11 C: two independent goals + one shared response requirement = two operation lifecycles
    + one response dependency, no extra operation for the response requirement."""
    from MAKSIMAR_CORE_LIB.ai_orchestration.helper_model_decision_parser import (
        parse_request_understanding_payload,
    )
    catalog = ({
        "capability_id": "conversation.respond", "operation_id": "respond",
        "required_parameters": (), "operation_description": "respond",
        "evidence_kinds": ("conversation",), "effect_type": "OBSERVE",
        "target_scope": "bounded_same_identity_session", "reversibility": "REVERSIBLE",
        "external_side_effect": False, "risk_class": "READ_ONLY",
    },)
    payload = {
        "schema_version": "request_understanding.v2", "language": "en",
        "goals": [
            {"goal_id": "g1", "description": "execute A"},
            {"goal_id": "g2", "description": "inspect B"},
        ],
        "required_capabilities": [
            {"capability_id": "conversation.respond", "purpose": "respond", "required": True},
        ],
        "response_requirements": [
            {"response_requirement_id": "r1", "applies_to_goal_ids": ["g1", "g2"]},
        ],
        "effect_type": "OBSERVE", "target_scope": "bounded_same_identity_session",
        "reversibility": "REVERSIBLE", "external_side_effect": None, "unresolved_capabilities": [],
        "operation_requirements": {"respond": {}},
        "current_topic": "", "unresolved_reference": "",
        "risk_class": "READ_ONLY", "confidence": 0.9, "reason_codes": ["typed"],
    }
    understanding = parse_request_understanding_payload(
        payload, host_request_id="r1", host_original_text="execute A and inspect B",
        authoritative_operation_catalog=catalog,
    )
    assert [g.goal_id for g in understanding.goals] == ["g1", "g2"]
    rr = understanding.response_requirements[0]
    assert rr.applies_to_goal_ids == ("g1", "g2")
    # response requirement is not an operation; only the respond operation exists
    assert [c.capability_id for c in understanding.required_capabilities] == ["conversation.respond"]


def test_identical_independent_goals_are_not_deduplicated() -> None:
    """T11 E: two identical independently requested goals both survive (no source-text/equality dedup)."""
    from MAKSIMAR_CORE_LIB.ai_orchestration.helper_model_decision_parser import (
        parse_request_understanding_payload,
    )
    catalog = ({
        "capability_id": "conversation.respond", "operation_id": "respond",
        "required_parameters": (), "operation_description": "respond",
        "evidence_kinds": ("conversation",), "effect_type": "OBSERVE",
        "target_scope": "bounded_same_identity_session", "reversibility": "REVERSIBLE",
        "external_side_effect": False, "risk_class": "READ_ONLY",
    },)
    payload = {
        "schema_version": "request_understanding.v2", "language": "en",
        "goals": [
            {"goal_id": "g1", "description": "increase volume"},
            {"goal_id": "g2", "description": "increase volume"},
        ],
        "required_capabilities": [
            {"capability_id": "conversation.respond", "purpose": "respond", "required": True},
        ],
        "response_requirements": [],
        "effect_type": "OBSERVE", "target_scope": "bounded_same_identity_session",
        "reversibility": "REVERSIBLE", "external_side_effect": None, "unresolved_capabilities": [],
        "operation_requirements": {"respond": {}},
        "current_topic": "", "unresolved_reference": "",
        "risk_class": "READ_ONLY", "confidence": 0.9, "reason_codes": ["typed"],
    }
    understanding = parse_request_understanding_payload(
        payload, host_request_id="r1", host_original_text="increase volume twice",
        authoritative_operation_catalog=catalog,
    )
    assert [g.goal_id for g in understanding.goals] == ["g1", "g2"]  # both survive, no dedup


def test_pc_action_binding_derives_from_canonical_metadata_not_hardcoded() -> None:
    """Screen/volume operation -> PC action binding comes from existing OPERATION_TO_ACTION_ID."""
    from MAKSIMAR_SERVER.WORKFLOW_AUTOMATION_RUNTIME.jarvis_pc_action_adapter_contract import (
        resolve_pc_action_for_operation,
    )
    screen = resolve_pc_action_for_operation("observe_windows_screen")
    assert screen["ok"] is True
    assert screen["action_id"] == "read_screen"
    assert screen["executor_function"] == "read_screen"
    assert screen["action_family"] == "screen_read"

    volume = resolve_pc_action_for_operation("execute_volume_up")
    assert volume["ok"] is True
    assert volume["action_id"] == "volume_up"

    unknown = resolve_pc_action_for_operation("no_such_operation")
    assert unknown["ok"] is False
    assert unknown["status"] == "unknown_operation"


def test_goalframe_constraint_and_subgoal_do_not_independently_bind() -> None:
    registry = projection()

    class GFModel:
        def __init__(self):
            self.discover_calls = 0

        def understand(self, *, system_prompt, user_prompt, deadline, output_schema=None):
            return model_call_envelope(json.dumps({"goals": [
                {"goal_id": "g1", "semantic_domain": "automation", "effect_intent": "compute_run",
                 "requested_outcome": "create automation", "grounding": "создай автоматизацию", "ambiguity": "",
                 "goal_role": "PRIMARY_OUTCOME", "parent_goal_id": "",
                 "subgoal_justification_kind": "NONE"},
                {"goal_id": "g2", "semantic_domain": "code", "effect_intent": "reason_propose",
                 "requested_outcome": "propose workflow", "grounding": "implicit", "ambiguity": "",
                 "goal_role": "SUBGOAL", "parent_goal_id": "g1",
                 "subgoal_justification_kind": "EXPLICIT_INTERMEDIATE"},
            ]}))

        def discover_candidates(self, **kwargs):
            self.discover_calls += 1
            return model_call_envelope(json.dumps({
                "status": "BOUND", "capability_id": "workflow_automation:n8n", "reason": "x",
            }))

    m = GFModel()
    audit = {}
    result = spine._model_selected_registry_details(
        model_port=m, deadline=RequestDeadline(60), original_text="создай автоматизацию",
        session_context={}, registry_projection=registry, audit_trace=audit,
        request_id="r", identity=OWNER, input_preparation={},
    )
    # A SUBGOAL whose grounding is "implicit" (not source-grounded) is a typed provenance
    # violation; the ONE bounded repair re-runs the same mock (still ungrounded) -> fail closed.
    assert result is None


def test_goalframe_provenance_validator_flags_bad_parent_graph() -> None:
    goals = [
        {"goal_id": "a", "semantic_domain": "automation", "effect_intent": "compute_run",
         "requested_outcome": "x", "grounding": "создай", "goal_role": "PRIMARY_OUTCOME", "parent_goal_id": ""},
        {"goal_id": "b", "semantic_domain": "code", "effect_intent": "reason_propose",
         "requested_outcome": "y", "grounding": "создай", "goal_role": "SUBGOAL", "parent_goal_id": "a"},
        {"goal_id": "c", "semantic_domain": "project", "effect_intent": "change_state",
         "requested_outcome": "z", "grounding": "", "goal_role": "SUBGOAL", "parent_goal_id": "b"},
    ]
    violations = spine._goalframe_validation_violations(goals, source_text="создай")
    reasons = {r for _, r in violations}
    assert "goal_not_source_grounded" in reasons  # c has empty grounding
    # a->b->c is acyclic, so no cycle violation
    assert "goal_parent_cycle" not in reasons


def test_goalframe_provenance_rejects_fabricated_grounding_and_duplicate_ids() -> None:
    goals = [
        {"goal_id": "g", "semantic_domain": "automation", "effect_intent": "change_state",
         "requested_outcome": "create", "grounding": "fabricated evidence",
         "goal_role": "PRIMARY_OUTCOME", "parent_goal_id": "",
         "subgoal_justification_kind": "NONE"},
        {"goal_id": "g", "semantic_domain": "automation", "effect_intent": "change_state",
         "requested_outcome": "create again", "grounding": "создай автоматизацию",
         "goal_role": "PRIMARY_OUTCOME", "parent_goal_id": "",
         "subgoal_justification_kind": "NONE"},
    ]
    violations = spine._goalframe_validation_violations(
        goals, source_text="создай автоматизацию",
    )
    reasons = {reason for _, reason in violations}
    assert "goal_not_source_grounded" in reasons
    assert "duplicate_goal_id" in reasons


def test_subgoal_requires_distinct_source_fragment_and_typed_basis() -> None:
    goals = [
        {"goal_id": "p", "semantic_domain": "automation", "effect_intent": "change_state",
         "requested_outcome": "create", "grounding": "создай автоматизацию",
         "goal_role": "PRIMARY_OUTCOME", "parent_goal_id": "",
         "subgoal_justification_kind": "NONE"},
        {"goal_id": "s", "semantic_domain": "code", "effect_intent": "reason_propose",
         "requested_outcome": "internal design", "grounding": "создай автоматизацию",
         "goal_role": "SUBGOAL", "parent_goal_id": "p",
         "subgoal_justification_kind": "EXPLICIT_INTERMEDIATE"},
    ]
    violations = spine._goalframe_validation_violations(
        goals, source_text="создай автоматизацию",
    )
    assert ("s", "subgoal_not_distinct_source_fragment") in violations


def test_goalframe_execution_restriction_requires_current_source_grounding() -> None:
    source = "создай автоматизацию, но без разрешения ничего не публикуй"
    assert spine._goalframe_restriction_violations(
        "NO_EXECUTE", "без разрешения ничего не публикуй", source_text=source,
    ) == ()
    assert spine._goalframe_restriction_violations(
        "NO_EXECUTE", "fabricated prohibition", source_text=source,
    ) == (("execution_restriction", "restriction_not_source_grounded"),)
    assert spine._goalframe_restriction_violations(
        "NONE", "без разрешения ничего не публикуй", source_text=source,
    ) == (("execution_restriction", "none_restriction_has_source"),)


def test_operation_single_remaining_justified_slot_cannot_request_continuation():
    import jsonschema
    allowed = ("search_history", "inspect_history", "read_history")
    schema = spine.discovery_schema_for_registered_values(spine.OPERATION_DISCOVERY_JSON_SCHEMA,
        value_key="candidate_operation_ids", allowed_values=allowed, max_selected_values=1)
    payload = {"candidate_operation_ids": {"search_history": True}, "selection_justifications": {"search_history": {
        "goal_id": "g1", "justification_kind": "DIRECT_GOAL_EFFECT", "source_grounding": "retrieve history"}},
        "continuation_required": False, "continuation_reason": "", "ambiguity_present": False,
        "confidence": 1.0, "reason_codes": ["direct_goal"]}
    jsonschema.validate(payload, schema)
    payload["continuation_required"] = True
    with pytest.raises(jsonschema.ValidationError):
        jsonschema.validate(payload, schema)
    larger = spine.discovery_schema_for_registered_values(spine.OPERATION_DISCOVERY_JSON_SCHEMA,
        value_key="candidate_operation_ids", allowed_values=allowed, max_selected_values=2)
    assert "const" not in larger["properties"]["continuation_required"]


@pytest.mark.parametrize("kind,basis,start,end", (
    ("HISTORY", "ANY_TIME", "", ""),
    ("VERIFIED_EXPERIENCE", "TODAY_UTC", "", ""),
    ("HISTORY", "EXPLICIT_RANGE", "2026-10-11T00:00:00Z", "2026-10-12T00:00:00Z"),
))
def test_first_goal_memory_object_and_time_cannot_drift_in_parameter_binding(kind,basis,start,end):
    import jsonschema
    filter_value = dict(query_kind=kind,time_basis=basis,time_start=start,time_end=end)
    raw_goal = dict(goal_id="g1",semantic_domain="memory",effect_intent="retrieve",
        requested_outcome="Retrieve a persisted record",grounding="Retrieve a persisted record",
        goal_role="PRIMARY_OUTCOME",parent_goal_id=None,subgoal_justification_kind="NONE",
        memory_filter=filter_value)
    goals = spine._parse_goalframe_goals({"goals": [raw_goal]})
    assert goals[0]["memory_filter"] == filter_value
    assert not spine._goalframe_validation_violations(goals,source_text=raw_goal["grounding"],require_artifact_operations=False)
    selected = select_semantic_projection_details(projection(), ("runtime_history_store",))
    selected["selection_goalframes"] = tuple(goals)
    schema = spine.request_understanding_schema_for_projection(selected)
    parameter_schema = schema["properties"]["operation_requirements"]["properties"]["search_history"]["properties"]["memory_filter"]
    jsonschema.validate(filter_value,parameter_schema)
    wrong = dict(filter_value,query_kind="REVIEW_STATUS")
    with pytest.raises(jsonschema.ValidationError):jsonschema.validate(wrong,parameter_schema)
    wrong = dict(filter_value,time_basis="TODAY_UTC" if basis!="TODAY_UTC" else "ANY_TIME",time_start="",time_end="")
    raw = {"operation_requirements": {"search_history": {"query": "record", "memory_filter": wrong}}}
    with pytest.raises(ValueError,match="memory_filter_drift_from_canonical_goal"):
        spine._hydrate_host_owned_understanding_fields(raw,selected)
    assert raw["operation_requirements"]["search_history"]["memory_filter"] == wrong
    raw["operation_requirements"]["search_history"]["memory_filter"] = dict(filter_value)
    bound = spine._hydrate_host_owned_understanding_fields(raw,selected)
    assert bound["operation_requirements"]["search_history"]["memory_filter"] == filter_value


def test_goal_memory_filter_wrong_domain_and_multiple_distinct_bindings_fail_closed():
    goal = dict(goal_id="g1",semantic_domain="conversation",effect_intent="retrieve",
        grounding="Read persisted utterances",goal_role="PRIMARY_OUTCOME",parent_goal_id="",
        subgoal_justification_kind="NONE",memory_filter=dict(query_kind="HISTORY",time_basis="ANY_TIME",time_start="",time_end=""))
    violations = spine._goalframe_validation_violations([goal],source_text=goal["grounding"],require_artifact_operations=False)
    assert ("g1","goal_memory_filter_domain_effect_invalid") in violations
    second = dict(goal,goal_id="g2",memory_filter=dict(goal["memory_filter"],query_kind="VERIFIED_EXPERIENCE"))
    with pytest.raises(ValueError,match="multiple_memory_filters_need_distinct_operation_binding"):
        spine._canonical_memory_filter({"selection_goalframes": [goal,second]})


def test_memory_filter_schema_is_shared_with_existing_core_owner():
    from MAKSIMAR_CORE_LIB.memory_engine.history_ingestion import jarvis_history_query_models as models
    from MAKSIMAR_SERVER.AI_ORCHESTRATION import memory_retrieval_adapter as adapter
    assert adapter.MEMORY_FILTER_SCHEMA is models.MEMORY_FILTER_SCHEMA
    assert spine.MEMORY_FILTER_SCHEMA is models.MEMORY_FILTER_SCHEMA


def test_typed_history_goal_candidates_require_existing_filter_input_contract():
    registry = projection()
    plain = spine._goalframe_projection(registry,semantic_domain="memory",effect_intent="retrieve")
    typed = spine._goalframe_projection(registry,semantic_domain="memory",effect_intent="retrieve",
        memory_filter=dict(query_kind="HISTORY",time_basis="ANY_TIME",time_start="",time_end=""))
    assert typed and set(typed).issubset(plain)
    entries = {entry["capability_id"]:entry for entry in registry["entries"]}
    for capability_id in typed:
        assert any("memory_filter" in op.get("parameter_schemas",{})
            for op in entries[capability_id]["operation_contracts"])
    assert "runtime_history_store" in typed
    assert "memory_engine_registry" not in typed
    assert "enterprise_business_memory" not in typed


def test_memory_binding_exposes_existing_typed_filter_input_contract():
    from CONTROL_PLANE.canonical_semantic_spine import build_goalframe_binding_prompt
    from MAKSIMAR_CORE_LIB.memory_engine.history_ingestion.jarvis_history_query_models import HISTORY_MEMORY_FILTER_SCHEMA
    goal = {"goal_id": "g1", "semantic_domain": "memory", "effect_intent": "retrieve",
            "memory_filter": {"query_kind": "VERIFIED_EXPERIENCE", "time_basis": "EXPLICIT_RANGE",
                              "time_start": "2026-10-11T00:00:00Z", "time_end": "2026-10-12T00:00:00Z"}}
    projection = select_semantic_projection_details(build_semantic_capability_registry_projection(),
                                                  ("runtime_history_store",))
    system, _ = build_goalframe_binding_prompt(goal=goal, registry_projection=projection)
    contracts = json.loads(system.split("TYPED_INPUT_CONTRACTS=", 1)[1].split(" The authoritative goal", 1)[0])
    assert contracts[0]["parameter_schemas"]["memory_filter"] == HISTORY_MEMORY_FILTER_SCHEMA
    assert json.dumps(goal, ensure_ascii=False) in system


def test_goalframe_schema_matches_typed_historical_filter_relationship():
    from jsonschema import validate, ValidationError
    schema = spine._goalframe_item_schema("PRIMARY_OUTCOME")
    goal = {"goal_id": "g1", "semantic_domain": "memory", "effect_intent": "observe",
            "requested_outcome": "live data status", "grounding": "live data status", "ambiguity": "",
            "goal_role": "PRIMARY_OUTCOME", "parent_goal_id": None, "subgoal_justification_kind": "NONE"}
    validate(goal, schema)
    validate({**goal, "memory_filter": None}, schema)
    historical_filter = {"query_kind": "VERIFIED_EXPERIENCE", "time_basis": "ANY_TIME", "time_start": "", "time_end": ""}
    with pytest.raises(ValidationError):
        validate({**goal, "memory_filter": historical_filter}, schema)
    validate({**goal, "effect_intent": "retrieve", "memory_filter": historical_filter}, schema)


def test_binding_goal_retains_first_pass_required_evidence_fields():
    raw = {"goals": [{"goal_id": "g1", "semantic_domain": "memory", "effect_intent": "retrieve",
        "requested_outcome": "document", "grounding": "document", "goal_role": "PRIMARY_OUTCOME",
        "parent_goal_id": None, "subgoal_justification_kind": "NONE", "memory_filter": None}],
        "response_requirements": [{"applies_to_goal_ids": ["g1"], "description": "actual source/index SHA and freshness"}]}
    goal = spine._parse_goalframe_goals(raw)[0]
    assert goal["response_requirements"] == tuple(raw["response_requirements"])
    projection = select_semantic_projection_details(build_semantic_capability_registry_projection(), ("mempalace_search",))
    system, _ = spine.build_goalframe_binding_prompt(goal=goal, registry_projection=projection)
    assert "actual source/index SHA and freshness" in system


def test_source_document_filter_uses_existing_archive_owner_and_excludes_history():
    from MAKSIMAR_CORE_LIB.memory_engine.history_ingestion.jarvis_history_query_models import validate_memory_filter
    source = {"query_kind": "SOURCE_DOCUMENT", "time_basis": "ANY_TIME", "time_start": "", "time_end": ""}
    assert validate_memory_filter(source) == source
    projection = build_semantic_capability_registry_projection()
    assert spine._goalframe_projection(projection, semantic_domain="memory", effect_intent="retrieve",
                                       memory_filter=source) == ("mempalace_search",)
    historical = {**source, "query_kind": "VERIFIED_EXPERIENCE"}
    assert spine._goalframe_projection(projection, semantic_domain="memory", effect_intent="retrieve",
                                       memory_filter=historical) == ("runtime_history_store",)
    with pytest.raises(ValueError, match="source_document_temporal_filter_not_supported"):
        validate_memory_filter({**source, "time_basis": "TODAY_UTC"})


def test_archive_retrieval_contract_is_not_a_live_dataset_inspection_owner():
    projection = build_semantic_capability_registry_projection()
    observed = spine._goalframe_projection(projection, semantic_domain="memory", effect_intent="observe")
    retrieved = spine._goalframe_projection(projection, semantic_domain="memory", effect_intent="retrieve")
    assert "mempalace_search" not in observed
    assert "enterprise_business_memory" in observed and "regulatory_memory_foundation" in observed
    assert "mempalace_search" in retrieved
    native = next(op for op in spine.load_operation_catalog(projection) if op["operation_id"] == "search_mempalace")
    assert native["supported_goal_effect_intents"] == ("retrieve",)


@pytest.mark.parametrize("replacement_invalid", [False, True])
def test_operation_justification_coverage_is_repaired_once_without_host_filling_missing_entries(replacement_invalid):
    registry = select_semantic_projection_details(projection(), ("runtime_history_store",))
    registry["selection_goalframes"] = ({"goal_id": "g1", "effect_intent": "retrieve",
        "requested_outcome": "history", "grounding": "прочитай историю"},)
    calls, attempts, repair_state = [], [], {}
    def discover(**kwargs):
        calls.append(kwargs)
        invalid = len(calls) == 1 or replacement_invalid
        return model_call_envelope(json.dumps({"candidate_operation_ids": {
            "selection_1": "search_history", "selection_2": None,
            "selection_3": None, "selection_4": None},
            "selection_justifications": {} if invalid else {"search_history": {
                "goal_id": "g1", "justification_kind": "DIRECT_GOAL_EFFECT",
                "source_grounding": "прочитай историю"}},
            "continuation_required": False, "continuation_reason": "",
            "ambiguity_present": False, "confidence": .99, "reason_codes": ["strict"]}))
    kwargs = dict(call=discover, prompt_builder=spine.build_operation_discovery_prompt,
        value_key="candidate_operation_ids", allowed_values=("search_history",),
        original_text="прочитай историю", session_context={}, registry_projection=registry,
        deadline=RequestDeadline(10), output_schema=spine.OPERATION_DISCOVERY_JSON_SCHEMA,
        trace=[], audit_trace=attempts, repair_state=repair_state)
    if replacement_invalid:
        with pytest.raises(ValueError, match="operation selection justification coverage mismatch"):
            spine._run_discovery_continuation(**kwargs)
    else:
        assert spine._run_discovery_continuation(**kwargs) == ("search_history",)
        assert attempts[-1]["schema_valid"] is True
    assert len(calls) == 2 and repair_state["model_backed_repair_count"] == 1
    assert "exactly one entry keyed by each selected non-null" in calls[1]["system_prompt"]
    assert attempts[0]["schema_valid"] is False


@pytest.mark.parametrize("approval,denied,unavailable,expected", [
    (False, False, False, "COMPLETE"),
    (False, True, False, "PARTIAL_POLICY_DENIED"),
    (False, False, True, "PARTIAL_UNAVAILABLE"),
    (False, True, True, "PARTIAL_POLICY_DENIED"),
    (True, True, True, "PARTIAL_APPROVAL_REQUIRED"),
])
def test_stream_publication_preserves_policy_denied_plan_status(monkeypatch, approval, denied, unavailable, expected):
    pending = _conversation_turn(Final(), defer=True)
    pending["approval_required_steps"] = ({"step_id": "needs_approval"},) if approval else ()
    pending["policy_denied_steps"] = ({"step_id": "denied"},) if denied else ()
    pending["provider_unavailable_steps"] = ({"step_id": "unavailable"},) if unavailable else ()
    monkeypatch.setattr(spine, "run_canonical_semantic_turn", lambda **kwargs: dict(pending))

    class StreamFinal:
        def stream_answer(self, **kwargs):
            yield {"event": "chunk", "chunk": "Ответ"}
            yield {"event": "done", "response_text": "Ответ", "model_call_attempted": True,
                   "model_call_succeeded": True, "raw_output_present": True,
                   "done": True, "done_reason": "stop", "truncation": False}

    events = list(spine.stream_canonical_semantic_turn(final_brain_port=StreamFinal()))
    assert events[-1]["event"] == "done"
    result = events[-1]["result"]
    assert result["operation_status"] == expected
    assert result["policy_denied_steps"] == pending["policy_denied_steps"]
    assert result["trace"]["final_brain_status"] == "COMPLETE"
    assert result["generation_completed"] is True
    assert result["delivery_completed"] is None


@pytest.mark.parametrize("blocked_disposition", ("DENIED", "APPROVAL_REQUIRED"))
def test_same_operation_steps_cannot_share_policy_authority_or_receipts(blocked_disposition):
    registry = projection()
    for entry in registry["entries"]:
        if entry["capability_id"] in {"project.read", "conversation.respond"}:
            entry["provider_available"] = True
    class RepeatedOperationModel(Model):
        def understand(self, **kwargs):
            result = super().understand(**kwargs)
            payload = json.loads(result["content"])
            original = next(item for item in payload["operation_requirements"] if item["capability_id"] == "project.read")
            payload["operation_requirements"].insert(1, dict(original))
            result["content"] = json.dumps(payload)
            return result
    collected = []
    class RecordingPort(EvidencePort):
        def collect_evidence(self, understanding, plan, trace_id, *args):
            collected.extend(step.step_id for step in plan.steps)
            return super().collect_evidence(understanding, plan, trace_id, *args)
    class StepPolicy:
        def evaluate(self, **kwargs):
            blocked = kwargs["step_id"] == "step_2"
            return PermissionDecision(
                granted=not blocked, capability_id=kwargs["capability_id"],
                identity_source=kwargs["identity"].identity_source, policy_version="exact_step_test",
                denial_reason=blocked_disposition if blocked else "", trace_id=kwargs["trace_id"],
                operation_id=kwargs["operation_id"], step_id=kwargs["step_id"],
                approval_required=blocked and blocked_disposition == "APPROVAL_REQUIRED")
    result = spine.run_canonical_semantic_turn(
        text="two steps of the same operation with different exact step decisions",
        project_port=EvidencePort(), conversation_port=EvidencePort(),
        model_port=RepeatedOperationModel(registry, ("project.read",)),
        final_brain_port=Final(), permission_port=StepPolicy(), identity=OWNER,
        registry_projection=registry, provider_ports={
            "existing_project_workspace_tools": RecordingPort("existing_project_workspace_tools"),
            "existing_jarvis_final_brain": EvidencePort("existing_jarvis_final_brain")},
        session_id="exact-step-policy-test")
    steps = result["execution_plan"]["steps"]
    assert steps[0]["operation"] == steps[1]["operation"]
    assert "step_1" in collected
    assert "step_2" not in collected
    bundle = result["evidence_bundle"]
    assert not any(item["step_id"] == "step_2" for item in bundle["items"])
    assert not any(item["step_id"] == "step_2" for item in bundle["receipts"])
    assert any(item["step_id"] == "step_1" for item in bundle["receipts"])
    blocked_key = "approval_required_steps" if blocked_disposition == "APPROVAL_REQUIRED" else "policy_denied_steps"
    assert [step["step_id"] for step in result[blocked_key]] == ["step_2"]
    assert result["operation_status"] == "PARTIAL_" + blocked_disposition.replace("DENIED", "POLICY_DENIED")
    truths = {step["step_id"]: step for item in result["capability_truth"]
              for step in item["step_execution_truth"]}
    assert truths["step_1"]["executed"] is True
    assert truths["step_2"]["executed"] is False
    if blocked_disposition == "APPROVAL_REQUIRED":
        assert [item["step_id"] for item in result["pending_approvals"]] == ["step_2"]


def test_operation_discovery_reuses_unique_key_selection_and_keeps_exact_registry_scope():
    from MAKSIMAR_SERVER.AI_ORCHESTRATION.model_understanding_adapter import validate_structured_payload
    schema = spine.discovery_schema_for_registered_values(spine.OPERATION_DISCOVERY_JSON_SCHEMA,
        value_key="candidate_operation_ids", allowed_values=("first_operation", "second_operation"), max_selected_values=1)
    selection = schema["properties"]["candidate_operation_ids"]
    assert selection["properties"] == {"first_operation": {"type": "boolean", "const": True}, "second_operation": {"type": "boolean", "const": True}}
    assert selection["maxProperties"] == 1
    assert validate_structured_payload(json.dumps({"first_operation": True}), selection)[1]
    assert not validate_structured_payload(json.dumps({"first_operation": True, "second_operation": True}), selection)[1]
    assert not validate_structured_payload(json.dumps({"invented_operation": True}), selection)[1]
    assert not validate_structured_payload(json.dumps({"first_operation": False}), selection)[1]


def test_read_goal_operation_scope_excludes_mutation_before_singleton_selection():
    selected = select_semantic_projection_details(projection(), ("project.read",))
    entry = selected["entries"][0]
    read = dict(entry["operation_contracts"][0])
    mutation = {**read, "operation_id": "typed_mutation_candidate", "effect_type": "MUTATE"}
    entry["operation_contracts"] = (read, mutation)
    selected["selection_goalframes"] = ({"goal_id": "g_read", "effect_intent": "retrieve"},)
    selected["selection_capability_justifications"] = ({"goal_id": "g_read", "capability_id": "project.read"},)

    class MustNotSelectMutation:
        supports_call_scoped_understanding_schema = True
        def discover_candidates(self, **kwargs):
            raise AssertionError("one compatible operation must be resolved before model discovery")

    audit = {}
    result = spine._model_selected_operation_details(
        model_port=MustNotSelectMutation(), deadline=RequestDeadline(30),
        original_text="any request language does not determine eligibility", session_context={},
        registry_projection=selected, audit_trace=audit,
    )
    assert result is not None
    assert tuple(o["operation_id"] for e in result["entries"] for o in e["operation_contracts"]) == (read["operation_id"],)
    assert len(selected["entries"][0]["operation_contracts"]) == 2
    assert audit["operation_discovery"]["status"] == "NOT_REQUIRED_SINGLE_AUTHORITATIVE_OPERATION"


def test_goal_effect_operation_projection_preserves_only_its_bound_goal_effect():
    selected = select_semantic_projection_details(projection(), ("project.read",))
    entry = selected["entries"][0]
    read = dict(entry["operation_contracts"][0])
    mutation = {**read, "operation_id": "typed_mutation_candidate", "effect_type": "MUTATE", "supported_goal_effect_intents": ("change_state",)}
    entry["operation_contracts"] = (read, mutation)
    selected["selection_goalframes"] = (
        {"goal_id": "read", "effect_intent": "retrieve"},
        {"goal_id": "other_change", "effect_intent": "change_state"},
    )
    selected["selection_capability_justifications"] = ({"goal_id": "read", "capability_id": "project.read"},)
    filtered = spine._goal_effect_operation_projection(selected)
    assert tuple(o["operation_id"] for e in filtered["entries"] for o in e["operation_contracts"]) == (read["operation_id"],)
    selected["selection_capability_justifications"] = ({"goal_id": "other_change", "capability_id": "project.read"},)
    changed = spine._goal_effect_operation_projection(selected)
    assert tuple(o["operation_id"] for e in changed["entries"] for o in e["operation_contracts"]) == (mutation["operation_id"],)


def test_goal_effect_operation_projection_respects_declared_intent_support():
    selected = select_semantic_projection_details(projection(), ("project.read",))
    read = dict(selected["entries"][0]["operation_contracts"][0])
    selected["entries"][0]["operation_contracts"] = ({**read, "supported_goal_effect_intents": ("observe",)},)
    selected["selection_goalframes"] = ({"goal_id": "read", "effect_intent": "retrieve"},)
    assert spine._goal_effect_operation_projection(selected)["entries"] == []


def test_read_goal_mutation_only_catalog_fails_closed_without_discovery():
    selected = select_semantic_projection_details(projection(), ("project.read",))
    read = dict(selected["entries"][0]["operation_contracts"][0])
    selected["entries"][0]["operation_contracts"] = ({**read, "effect_type": "MUTATE"},)
    selected["selection_goalframes"] = ({"goal_id": "read", "effect_intent": "retrieve"},)
    class NoCall:
        supports_call_scoped_understanding_schema = True
        def discover_candidates(self, **kwargs):
            raise AssertionError("incompatible catalog must fail before model selection")
    audit = {}
    assert spine._model_selected_operation_details(
        model_port=NoCall(), deadline=RequestDeadline(30), original_text="arbitrary text",
        session_context={}, registry_projection=selected, audit_trace=audit,
    ) is None
    assert audit["operation_discovery_error"] == "goal_effect_has_no_compatible_operation"


@pytest.mark.parametrize("first_bad, correction_bad", [(True, False), (True, True), (False, False)])
def test_goalframe_response_references_are_validated_before_binding_and_follow_correction(first_bad, correction_bad):
    source = "Read current project state and provide its details."
    class GoalframeModel:
        def __init__(self):
            self.understanding_calls = 0
            self.binding_calls = 0
        def understand(self, **kwargs):
            self.understanding_calls += 1
            corrected = self.understanding_calls > 1
            bad = correction_bad if corrected else first_bad
            goal_id = "corrected_goal" if corrected else "original_goal"
            payload = {
                "goals": [{"goal_id": goal_id, "semantic_domain": "project", "effect_intent": "observe",
                    "requested_outcome": source, "grounding": source, "goal_role": "PRIMARY_OUTCOME",
                    "parent_goal_id": None, "subgoal_justification_kind": "NONE"}],
                "execution_restriction": "NONE", "execution_restriction_source": "",
                "response_requirements": [{"applies_to_goal_ids": ["undeclared_goal" if bad else goal_id], "description": "provide details"}],
            }
            return model_call_envelope(json.dumps(payload))
        def discover_candidates(self, **kwargs):
            self.binding_calls += 1
            return model_call_envelope(json.dumps({"status": "BOUND", "capability_id": "project.read", "reason": "typed project reader"}))

        def verify_source_candidate(self, *, source_text, candidate, deadline):
            # Explicit controlled judgment for this test request, not natural proof.
            verdict = {"status": "COMPLETE", "supported": list(("goal:corrected_goal" if self.understanding_calls > 1 else "goal:original_goal", "requirement:0")),
                       "missing": [], "contradictions": [], "unsupported_claims": [],
                       "reason": "Independent controlled fixture judgment"}
            return {"verdict": verdict, "model_call": model_call_envelope(json.dumps(verdict))}
    model = GoalframeModel()
    audit = {}
    result = spine._model_selected_registry_details_goalframe(
        model_port=model, deadline=RequestDeadline(30), original_text=source,
        session_context={}, registry_projection=projection(), audit_trace=audit,
    )
    assert model.understanding_calls == (2 if first_bad else 1)
    if first_bad and correction_bad:
        assert result is None
        assert model.binding_calls == 0
        assert audit["candidate_discovery_error"] == "goalframe_provenance_invalid"
    else:
        assert result is not None
        assert model.binding_calls == 1
        expected = "corrected_goal" if first_bad else "original_goal"
        assert audit["candidate_discovery"]["response_requirements"][0]["applies_to_goal_ids"] == [expected]
        assert result["selection_goalframes"][0]["goal_id"] == expected


@pytest.mark.parametrize("late_response", ([], [dict(response_requirement_id="late", applies_to_goal_ids=["g1"], description="general summary")]))
def test_canonical_model_response_obligations_survive_parameter_binding(late_response):
    from copy import deepcopy
    selected = select_semantic_projection_details(projection(), ("runtime_history_store",))
    selected["selection_goalframes"] = ({"goal_id": "g1", "requested_outcome": "Read prior evidence"},)
    original = [dict(applies_to_goal_ids=["g1"], description=description) for description in ("actual result", "source identity", "review state")]
    selected["selection_response_requirements"] = deepcopy(original)
    hydrated = spine._hydrate_host_owned_understanding_fields({"operation_requirements": {}, "response_requirements": late_response}, selected)
    actual = hydrated["response_requirements"]
    assert [x["description"] for x in actual] == [x["description"] for x in original]
    assert [x["applies_to_goal_ids"] for x in actual] == [["g1"]] * 3
    assert len({x["response_requirement_id"] for x in actual}) == 3
    actual[0]["description"] = "mutated downstream"
    assert selected["selection_response_requirements"] == original


def test_canonical_response_obligation_hydration_rejects_undeclared_goal():
    selected = select_semantic_projection_details(projection(), ("runtime_history_store",))
    selected["selection_goalframes"] = ({"goal_id": "g1", "requested_outcome": "Read prior evidence"},)
    selected["selection_response_requirements"] = [dict(applies_to_goal_ids=["g2"], description="unbound")]
    with pytest.raises(ValueError, match="unknown goal_id"):
        spine._hydrate_host_owned_understanding_fields({"operation_requirements": {}, "response_requirements": []}, selected)


def test_no_canonical_presentation_keeps_existing_parameter_stage_contract():
    selected = select_semantic_projection_details(projection(), ("runtime_history_store",))
    selected["selection_goalframes"] = ({"goal_id": "g1", "requested_outcome": "Read prior evidence"},)
    original = [dict(response_requirement_id="old", applies_to_goal_ids=["g1"], description="legacy caller presentation")]
    hydrated = spine._hydrate_host_owned_understanding_fields({"operation_requirements": {}, "response_requirements": original}, selected)
    assert hydrated["response_requirements"] == original


@pytest.mark.parametrize("goal_kind,requested_kind", (("SOURCE_DOCUMENT", "PROVENANCE"), ("PROVENANCE", "SOURCE_DOCUMENT")))
def test_response_memory_object_kind_must_share_existing_source_contract_family(goal_kind, requested_kind):
    goals = [dict(goal_id="g1", semantic_domain="memory", effect_intent="retrieve", memory_filter=dict(query_kind=goal_kind, time_basis="ANY_TIME", time_start="", time_end=""))]
    presentation = (dict(applies_to_goal_ids=["g1"], description="Required source evidence", memory_query_kind=requested_kind),)
    violations = spine._goalframe_response_requirement_violations(goals, presentation)
    assert any("response_memory_object_incompatible_with_goal" in reason for _, reason in violations)


def test_response_memory_object_kind_uses_existing_history_family_without_selecting_operation():
    goals = [dict(goal_id="g1", semantic_domain="memory", effect_intent="retrieve", memory_filter=dict(query_kind="PROVENANCE", time_basis="ANY_TIME", time_start="", time_end=""))]
    presentation = (dict(applies_to_goal_ids=["g1"], description="Review state", memory_query_kind="REVIEW_STATUS"),)
    assert spine._goalframe_response_requirement_violations(goals, presentation) == ()
    assert goals[0]["memory_filter"]["query_kind"] == "PROVENANCE"


def test_response_memory_object_kind_rejects_unknown_and_wrong_domain():
    goals = [dict(goal_id="g1", semantic_domain="project", effect_intent="observe")]
    for kind in ("PROVENANCE", "invented_memory_kind"):
        presentation = (dict(applies_to_goal_ids=["g1"], description="Requested evidence", memory_query_kind=kind),)
        assert spine._goalframe_response_requirement_violations(goals, presentation)


def test_response_memory_object_kind_survives_existing_hydration_and_typed_contract():
    from MAKSIMAR_CORE_LIB.ai_orchestration.semantic_intent_contract import ResponseRequirement
    selected = select_semantic_projection_details(projection(), ("runtime_history_store",))
    selected["selection_goalframes"] = (dict(goal_id="g1", semantic_domain="memory", effect_intent="retrieve", requested_outcome="Read prior evidence", memory_filter=dict(query_kind="PROVENANCE", time_basis="ANY_TIME", time_start="", time_end="")),)
    selected["selection_response_requirements"] = [dict(applies_to_goal_ids=["g1"], description="Review state", memory_query_kind="REVIEW_STATUS")]
    hydrated = spine._hydrate_host_owned_understanding_fields({"operation_requirements": {}, "response_requirements": []}, selected)
    response = hydrated["response_requirements"][0]
    assert response["memory_query_kind"] == "REVIEW_STATUS"
    typed = ResponseRequirement(response_requirement_id=response["response_requirement_id"], applies_to_goal_ids=("g1",), description=response["description"], memory_query_kind=response["memory_query_kind"])
    assert typed.to_read_model()["memory_query_kind"] == "REVIEW_STATUS"


def test_goalframe_presentation_generation_requires_explicit_reused_memory_kind_field():
    import jsonschema
    schema = spine.GOALFRAME_UNDERSTANDING_JSON_SCHEMA["properties"]["response_requirements"]["items"]
    value = dict(applies_to_goal_ids=["g1"], description="Document source", memory_query_kind="SOURCE_DOCUMENT", requirement_kind="EVIDENCE")
    jsonschema.validate(value, schema)
    with pytest.raises(jsonschema.ValidationError):jsonschema.validate(dict(value, memory_query_kind="invented_memory_kind"), schema)
    with pytest.raises(jsonschema.ValidationError):jsonschema.validate({k:v for k,v in value.items() if k!="memory_query_kind"}, schema)


@pytest.mark.parametrize("kinds,expected_calls,expected_bound", ((("SOURCE_DOCUMENT", "PROVENANCE"), 2, True), (("SOURCE_DOCUMENT", "SOURCE_DOCUMENT"), 2, False), (("PROVENANCE",), 1, True)))
def test_requested_memory_kind_uses_existing_one_bounded_goalframe_correction(kinds, expected_calls, expected_bound):
    class TypedKindModel:
        def __init__(self):
            self.calls = 0
            self.bind_calls = 0
        def understand(self, **kwargs):
            kind = kinds[min(self.calls, len(kinds)-1)]
            self.calls += 1
            return model_call_envelope(json.dumps({"goals": [dict(goal_id="g1", semantic_domain="memory", effect_intent="retrieve", requested_outcome="Read prior record", grounding="Read prior record", ambiguity="", goal_role="PRIMARY_OUTCOME", parent_goal_id=None, subgoal_justification_kind="NONE", memory_filter=dict(query_kind=kind, time_basis="ANY_TIME", time_start="", time_end=""))], "execution_restriction":"NONE", "execution_restriction_source":"", "response_requirements":[dict(applies_to_goal_ids=["g1"], description="Record provenance", memory_query_kind="PROVENANCE")]}))
        def discover_candidates(self, **kwargs):
            self.bind_calls += 1
            return model_call_envelope(json.dumps({"status":"BOUND", "capability_id":"runtime_history_store", "reason":"existing typed history source"}))

        def verify_source_candidate(self, *, source_text, candidate, deadline):
            # Explicit controlled judgment for this test request, not natural proof.
            verdict = {"status": "COMPLETE", "supported": list(("goal:g1", "requirement:0")),
                       "missing": [], "contradictions": [], "unsupported_claims": [],
                       "reason": "Independent controlled fixture judgment"}
            return {"verdict": verdict, "model_call": model_call_envelope(json.dumps(verdict))}
    model = TypedKindModel()
    audit = {}
    result = spine._model_selected_registry_details_goalframe(model_port=model, deadline=RequestDeadline(60), original_text="Read prior record", session_context={}, registry_projection=projection(), audit_trace=audit)
    assert model.calls == expected_calls
    attempts = audit["goalframe_understanding_attempts"]
    assert len(attempts) == expected_calls
    assert json.loads(attempts[0]["raw_model_content"])["goals"][0]["memory_filter"]["query_kind"] == kinds[0]
    assert bool(attempts[0]["validation_violations"]) == (kinds[0] == "SOURCE_DOCUMENT")
    if expected_calls == 2:
        assert attempts[1]["attempt"] == 1
        assert json.loads(attempts[1]["raw_model_content"])["goals"][0]["memory_filter"]["query_kind"] == kinds[1]
    assert (result is not None) == expected_bound
    assert model.bind_calls == int(expected_bound)
    if expected_bound:
        assert result["selection_response_requirements"][0]["memory_query_kind"] == "PROVENANCE"
    else:
        assert audit["candidate_discovery_error"] == "goalframe_provenance_invalid"


def test_malformed_memory_kind_correction_cannot_enter_legacy_discovery():
    class MalformedCorrectionModel:
        def __init__(self):self.calls=0;self.fallback_calls=0
        def understand(self, **kwargs):
            self.calls += 1
            if self.calls > 1:return model_call_envelope("not_json")
            return model_call_envelope(json.dumps({"goals":[dict(goal_id="g1",semantic_domain="memory",effect_intent="retrieve",requested_outcome="Read prior record",grounding="Read prior record",ambiguity="",goal_role="PRIMARY_OUTCOME",parent_goal_id=None,subgoal_justification_kind="NONE",memory_filter=dict(query_kind="SOURCE_DOCUMENT",time_basis="ANY_TIME",time_start="",time_end=""))],"execution_restriction":"NONE","execution_restriction_source":"","response_requirements":[dict(applies_to_goal_ids=["g1"],description="Record provenance",memory_query_kind="PROVENANCE")]}))
        def discover_candidates(self, **kwargs):
            self.fallback_calls += 1
            raise AssertionError("rejected correction must fail closed before legacy discovery")
    model=MalformedCorrectionModel();audit={}
    result=spine._model_selected_registry_details(model_port=model,deadline=RequestDeadline(60),original_text="Read prior record",session_context={},registry_projection=select_semantic_projection_details(projection(),("runtime_history_store",)),audit_trace=audit,request_id="r",identity=OWNER,input_preparation={})
    assert result is None
    assert model.calls==2
    assert model.fallback_calls==0
    assert audit["candidate_discovery_error"]=="goalframe_provenance_invalid"
    assert len(audit["goalframe_understanding_attempts"])==2
    assert audit["goalframe_understanding_attempts"][1]["raw_model_content"]=="not_json"


@pytest.mark.parametrize("reject_correction", (False, True))
@pytest.mark.parametrize("failure_field", ("ok", "schema_valid", "final_valid"))
def test_native_scoped_goalframe_cannot_use_model_declared_schema_failure(reject_correction, failure_field):
    class InvalidEnvelopeModel:
        supports_call_scoped_understanding_schema = True
        def __init__(self):self.calls=0;self.bind_calls=0
        def understand(self, **kwargs):
            self.calls+=1
            kind="SOURCE_DOCUMENT" if reject_correction and self.calls==1 else "PROVENANCE"
            raw={"goals":[dict(goal_id="g1",semantic_domain="memory",effect_intent="retrieve",requested_outcome="Read prior record",grounding="Read prior record",ambiguity="",goal_role="PRIMARY_OUTCOME",parent_goal_id=None,subgoal_justification_kind="NONE",memory_filter=dict(query_kind=kind,time_basis="ANY_TIME",time_start="",time_end=""))],"execution_restriction":"NONE","execution_restriction_source":"","response_requirements":[dict(applies_to_goal_ids=["g1"],description="Record provenance",memory_query_kind="PROVENANCE")]}
            envelope=model_call_envelope(json.dumps(raw))
            valid=reject_correction and self.calls==1
            envelope.update(ok=True, schema_valid=None, final_valid=True)
            envelope[failure_field] = valid
            return envelope
        def discover_candidates(self, **kwargs):
            self.bind_calls+=1
            return model_call_envelope(json.dumps({"status":"BOUND","capability_id":"runtime_history_store","reason":"existing source"}))
    model=InvalidEnvelopeModel();audit={}
    result=spine._model_selected_registry_details_goalframe(model_port=model,deadline=RequestDeadline(60),original_text="Read prior record",session_context={},registry_projection=projection(),audit_trace=audit)
    assert result is None
    assert model.calls==(2 if reject_correction else 1)
    assert model.bind_calls==0
    assert audit["candidate_discovery_error"]=="goalframe_provenance_invalid"
    assert audit["goalframe_understanding_attempts"][-1]["validation_violations"]


def test_operation_dependency_generation_domain_matches_each_registered_contract():
    contracts = ({"operation_id": "prerequisite", "declared_prerequisite_for_operation_ids": ("target",)},
                 {"operation_id": "target"})
    schema = spine.discovery_schema_for_registered_values(
        spine.OPERATION_DISCOVERY_JSON_SCHEMA, value_key="candidate_operation_ids",
        allowed_values=("prerequisite", "target"), operation_contracts=contracts)
    items = schema["properties"]["selection_justifications"]["properties"]
    assert items["prerequisite"]["properties"]["justification_kind"]["enum"] == ["DIRECT_GOAL_EFFECT", "DECLARED_OPERATION_DEPENDENCY"]
    assert items["target"]["properties"]["justification_kind"]["enum"] == ["DIRECT_GOAL_EFFECT"]


@pytest.mark.parametrize("contracts", (None, ()))
def test_operation_dependency_generation_domain_does_not_invent_missing_contract(contracts):
    schema = spine.discovery_schema_for_registered_values(
        spine.OPERATION_DISCOVERY_JSON_SCHEMA, value_key="candidate_operation_ids",
        allowed_values=("unbound",), operation_contracts=contracts)
    item = schema["properties"]["selection_justifications"]["properties"]["unbound"]
    assert item["properties"]["justification_kind"]["enum"] == ["DIRECT_GOAL_EFFECT"]


def test_operation_discovery_pass_binds_dependency_domain_from_current_catalog():
    registry = select_semantic_projection_details(projection(), ("runtime_history_store",))
    registry["selection_goalframes"] = ({"goal_id": "g1", "effect_intent": "retrieve"},)
    catalog = spine.load_operation_catalog(registry)
    allowed = tuple(c["operation_id"] for c in catalog)
    calls = []
    def discover(**kwargs):
        items = kwargs["output_schema"]["properties"]["selection_justifications"]["properties"]
        for contract in catalog:
            kinds = items[contract["operation_id"]]["properties"]["justification_kind"]["enum"]
            assert ("DECLARED_OPERATION_DEPENDENCY" in kinds) == bool(contract.get("declared_prerequisite_for_operation_ids"))
        calls.append(kwargs)
        return model_call_envelope(json.dumps({"candidate_operation_ids":{"search_history":True},
            "selection_justifications":{"search_history":{"goal_id":"g1","justification_kind":"DIRECT_GOAL_EFFECT","source_grounding":"Read prior record"}},
            "continuation_required":False,"continuation_reason":"","ambiguity_present":False,"confidence":.99,"reason_codes":["semantic_operation_discovery"]}))
    found = spine._run_discovery_continuation(call=discover, prompt_builder=spine.build_operation_discovery_prompt,
        value_key="candidate_operation_ids", allowed_values=allowed, original_text="Read prior record", session_context={},
        registry_projection=registry, deadline=RequestDeadline(30), output_schema=spine.OPERATION_DISCOVERY_JSON_SCHEMA, trace=[])
    assert found == ("search_history",)
    assert len(calls) == 1


def _dependency_identity_fixture():
    import copy
    registry = copy.deepcopy(select_semantic_projection_details(projection(), ("runtime_history_store",)))
    entry = registry["entries"][0]
    ids = ("inspect_memory_registry", "inspect_recent_session_memory", "inspect_memory_domains")
    by_id = {c["operation_id"]: c for c in entry["operation_contracts"]}
    entry["operation_contracts"] = [by_id[x] for x in ids]
    entry["operation_contracts"][0]["declared_prerequisite_for_operation_ids"] = (ids[1],)
    registry["selection_goalframes"] = ({"goal_id":"g1", "effect_intent":"retrieve"},)
    return registry, ids


def _dependency_identity_understanding(catalog):
    return parse_request_understanding_payload({
        "schema_version":"request_understanding.v2", "language":"ru",
        "goals":[{"goal_id":"g1","description":"Read prior record"}],
        "required_capabilities":[{"capability_id":"runtime_history_store","purpose":"Read prior record","required":True}],
        "response_requirements":[], "effect_type":"OBSERVE","target_scope":"local_memory_runtime",
        "reversibility":"REVERSIBLE","external_side_effect":False,"unresolved_capabilities":[],
        "operation_requirements":{c["operation_id"]:{} for c in catalog},
        "current_topic":"history","unresolved_reference":"","risk_class":"READ_ONLY","confidence":.99,"reason_codes":["test"]},
        host_request_id="dep_request",host_original_text="Read prior record",authoritative_operation_catalog=catalog)


def _dependency_identity_plan(understanding):
    return ExecutionPlan(understanding.request_id, tuple(PlanStep(
        step_id="dep_step_"+str(i), goal_id="g1", capability_id=req.capability_id, operation=req.operation_id,
        required_evidence=req.required_evidence,effect_type=req.effect_type,target_scope=req.target_scope,
        reversibility=req.reversibility,external_side_effect=req.external_side_effect,risk_class=req.risk_class,
        parameters=req.parameters,declared_prerequisite_for_operation_ids=req.declared_prerequisite_for_operation_ids)
        for i,req in enumerate(understanding.operation_requirements)))


def test_dependency_identity_registry_parser_plan_and_executor_preserve_exact_declared_ids():
    registry, ids = _dependency_identity_fixture()
    catalog = spine.load_operation_catalog(registry)[:2]
    assert catalog[0]["declared_prerequisite_for_operation_ids"] == (ids[1],)
    understanding = _dependency_identity_understanding(catalog)
    assert understanding.operation_requirements[0].declared_prerequisite_for_operation_ids == (ids[1],)
    plan = _dependency_identity_plan(understanding)
    assert plan.to_read_model()["steps"][0]["declared_prerequisite_for_operation_ids"] == (ids[1],)
    seen = []
    class DependencyPort(EvidencePort):
        def collect_evidence(self, understanding, plan, trace_id, *args):
            seen.extend((s.operation,s.declared_prerequisite_for_operation_ids) for s in plan.steps)
            return super().collect_evidence(understanding,plan,trace_id,*args)
    port=DependencyPort()
    result=spine._execute_evidence(understanding,plan,"dep_trace",OWNER,{},RequestDeadline(30),("runtime_history_store",),{"runtime_history_store":port})
    assert result.status == "COMPLETE"
    assert seen == [(ids[0],(ids[1],)),(ids[1],())]


@pytest.mark.parametrize("targets", (("inspect_recent_session_memory","inspect_recent_session_memory"), "inspect_recent_session_memory", ("",)))
def test_dependency_identity_registry_rejects_malformed_or_duplicate_references(targets):
    registry, ids = _dependency_identity_fixture()
    registry["entries"][0]["operation_contracts"][0]["declared_prerequisite_for_operation_ids"] = targets
    with pytest.raises((ValueError,TypeError)):
        spine.load_operation_catalog(registry)


def test_dependency_identity_plan_rejects_self_and_reverse_or_cyclic_order():
    from dataclasses import replace
    registry, ids = _dependency_identity_fixture()
    u=_dependency_identity_understanding(spine.load_operation_catalog(registry)[:2]);p=_dependency_identity_plan(u)
    with pytest.raises(ValueError):ExecutionPlan(u.request_id,tuple(reversed(p.steps)))
    with pytest.raises(ValueError):replace(p.steps[0],declared_prerequisite_for_operation_ids=(ids[0],))
    with pytest.raises(ValueError):ExecutionPlan(u.request_id,(p.steps[0],replace(p.steps[1],declared_prerequisite_for_operation_ids=(ids[0],))))


@pytest.mark.parametrize("failed_prerequisite", (False,True))
def test_dependency_identity_executor_requires_original_qualified_receipt(failed_prerequisite):
    registry, ids = _dependency_identity_fixture();u=_dependency_identity_understanding(spine.load_operation_catalog(registry)[:2]);p=_dependency_identity_plan(u);seen=[]
    class Port(EvidencePort):
        def collect_evidence(self,u,plan,trace,*args):
            seen.extend(s.operation for s in plan.steps)
            if failed_prerequisite and plan.steps[0].operation==ids[0]:
                return EvidenceBundle(u.request_id,"runtime_history_store",trace,"UNAVAILABLE",(),(),(),("prerequisite failed",))
            return super().collect_evidence(u,plan,trace,*args)
    port=Port()
    e=spine._execute_evidence(u,p,"dep_trace",OWNER,{},RequestDeadline(30),("runtime_history_store",),{"runtime_history_store":port})
    if failed_prerequisite:
        assert seen==[ids[0]]
        assert any("operation_dependency_unproven" in err for err in e.errors)
    else:assert seen==list(ids[:2]) and e.status=="COMPLETE"


@pytest.mark.parametrize("unknown", ("not_registered", "previous_catalog_operation"))
def test_dependency_identity_generation_rejects_absent_or_stale_catalog_target(unknown):
    registry, ids=_dependency_identity_fixture()
    registry["entries"][0]["operation_contracts"][0]["declared_prerequisite_for_operation_ids"]=(unknown,)
    with pytest.raises(ValueError,match="not_uniquely_registered"):
        spine.discovery_schema_for_registered_values(spine.OPERATION_DISCOVERY_JSON_SCHEMA,
            value_key="candidate_operation_ids",allowed_values=ids,operation_contracts=spine.load_operation_catalog(registry))


def test_dependency_identity_multiple_targets_preserve_exact_registry_set():
    registry, ids=_dependency_identity_fixture()
    registry["entries"][0]["operation_contracts"][0]["declared_prerequisite_for_operation_ids"]=ids[1:]
    catalog=spine.load_operation_catalog(registry);u=_dependency_identity_understanding(catalog);plan=_dependency_identity_plan(u)
    assert plan.steps[0].declared_prerequisite_for_operation_ids == ids[1:]
    schema=spine.discovery_schema_for_registered_values(spine.OPERATION_DISCOVERY_JSON_SCHEMA,
        value_key="candidate_operation_ids",allowed_values=ids,operation_contracts=catalog)
    items=schema["properties"]["selection_justifications"]["properties"]
    assert items[ids[0]]["properties"]["justification_kind"]["enum"]==["DIRECT_GOAL_EFFECT","DECLARED_OPERATION_DEPENDENCY"]
    assert all(items[i]["properties"]["justification_kind"]["enum"]==["DIRECT_GOAL_EFFECT"] for i in ids[1:])


@pytest.mark.parametrize("correction_valid", (False,True))
def test_dependency_identity_bypassed_schema_and_one_correction_remain_registry_bound(correction_valid):
    registry, ids=_dependency_identity_fixture();calls=[];repair={};trace=[]
    def discover(**kwargs):
        calls.append(kwargs)
        source=ids[0] if correction_valid and len(calls)==2 else ids[2]
        payload={"candidate_operation_ids":{source:True,ids[1]:True},"selection_justifications":{
            source:{"goal_id":"g1","justification_kind":"DECLARED_OPERATION_DEPENDENCY","source_grounding":"Read prior record"},
            ids[1]:{"goal_id":"g1","justification_kind":"DIRECT_GOAL_EFFECT","source_grounding":"Read prior record"}},
            "continuation_required":False,"continuation_reason":"","ambiguity_present":False,"confidence":.99,"reason_codes":["test"]}
        result=model_call_envelope(json.dumps(payload));result["final_valid"]=True;return result
    def run():return spine._run_discovery_continuation(call=discover,prompt_builder=spine.build_operation_discovery_prompt,
        value_key="candidate_operation_ids",allowed_values=ids,original_text="Read prior record",session_context={},
        registry_projection=registry,deadline=RequestDeadline(30),output_schema=spine.OPERATION_DISCOVERY_JSON_SCHEMA,
        trace=trace,repair_state=repair)
    if correction_valid:assert run()==ids[:2]
    else:
        with pytest.raises(ValueError,match="operation_dependency_not_registry_declared"):run()
    assert len(calls)==2
    assert repair["model_backed_repair_count"]==1
    assert len(trace)==2


def test_dependency_identity_malformed_model_dependency_object_rejected():
    payload={"candidate_operation_ids":{"inspect_memory_registry":True},"selection_justifications":{
        "inspect_memory_registry":{"goal_id":"g1","justification_kind":"DECLARED_OPERATION_DEPENDENCY",
        "source_grounding":"Read prior record","dependency_id":{"made_up":"value"}}},
        "continuation_required":False,"continuation_reason":"","ambiguity_present":False,"confidence":.99,"reason_codes":["test"]}
    with pytest.raises(ValueError,match="fields invalid"):
        parse_discovery_selection_payload(json.dumps(payload),value_key="candidate_operation_ids",allowed_values=("inspect_memory_registry",))


def test_dependency_identity_filtered_prerequisite_cannot_be_bypassed_by_executor_fragment():
    registry, ids=_dependency_identity_fixture();u=_dependency_identity_understanding(spine.load_operation_catalog(registry)[:2]);full=_dependency_identity_plan(u)
    fragment=ExecutionPlan(u.request_id,(full.steps[1],));seen=[]
    class Port(EvidencePort):
        def collect_evidence(self,u,p,t,*args):
            seen.extend(s.operation for s in p.steps)
            return super().collect_evidence(u,p,t,*args)
    e=spine._execute_evidence(u,fragment,"dep_trace",OWNER,{},RequestDeadline(30),("runtime_history_store",),{"runtime_history_store":Port()},dependency_plan=full)
    assert seen==[] and any("operation_dependency_unproven" in err for err in e.errors)



def test_dependency_identity_actual_semantic_plan_builder_preserves_registry_metadata(monkeypatch):
    registry, ids=_dependency_identity_fixture()
    registry["entries"][0]["operation_contracts"]=registry["entries"][0]["operation_contracts"][:2]
    registry["entries"][0]["provider_available"]=True
    registry["entries"][0]["availability_status"]="AVAILABLE"
    u=_dependency_identity_understanding(spine.load_operation_catalog(registry))
    from dataclasses import replace
    monkeypatch.setattr(spine,"_understand",lambda *args,**kwargs:replace(u,request_id=args[2] if len(args)>2 else kwargs["request_id"]))
    response=next(e for e in projection()["entries"] if e["capability_id"]=="conversation.respond")
    registry["entries"]=tuple(registry["entries"])+(response,);registry["capability_count"]=2
    provider_id=registry["entries"][0]["provider_ids"][0];seen=[]
    class Port(EvidencePort):
        def collect_evidence(self,u,plan,trace,*args):
            seen.extend(plan.steps)
            return super().collect_evidence(u,plan,trace,*args)
    class DependencyModel(Model):
        def discover_candidates(self, **kwargs):
            result = super().discover_candidates(**kwargs)
            payload = json.loads(result["content"])
            if ids[0] in payload.get("selection_justifications", {}):
                payload["selection_justifications"][ids[0]]["justification_kind"]="DECLARED_OPERATION_DEPENDENCY"
                result["content"]=json.dumps(payload)
            return result
    result=spine.run_canonical_semantic_turn(text="Read prior record",request_id="dep_request",
        trace_id="dep_trace",project_port=EvidencePort(),conversation_port=EvidencePort(),
        model_port=DependencyModel(registry,("runtime_history_store",)),final_brain_port=Final(),
        permission_port=__import__("MAKSIMAR_CORE_LIB.security_layer.semantic_policy",fromlist=["SemanticPolicyEvaluator"]).SemanticPolicyEvaluator(),
        identity=OWNER,registry_projection=registry,provider_ports={provider_id:Port(provider_id)},defer_final_brain=True)
    assert [s.operation for s in seen]==list(ids[:2]),result
    assert seen[0].declared_prerequisite_for_operation_ids==(ids[1],)
    assert result["execution_plan"]["steps"][0]["declared_prerequisite_for_operation_ids"]==(ids[1],)


@pytest.mark.parametrize("value", (None,False,True,"ABSENT",1,"true"))
def test_semantic_final_valid_requires_explicit_boolean_true(value):
    result=model_call_envelope("{}")
    if value=="ABSENT":result.pop("final_valid",None)
    else:result["final_valid"]=value
    assert bool(spine._model_call_verification_error(result)) == (value is not True)


@pytest.mark.parametrize("scoped", (False,True))
@pytest.mark.parametrize("value", (None,False,True,"ABSENT",1,"true"))
def test_goalframe_final_valid_gate_cannot_be_bypassed_by_port_flag_or_null(scoped,value):
    class Port:
        supports_call_scoped_understanding_schema=scoped
        def __init__(self):self.calls=0;self.bind_calls=0
        def understand(self,**kwargs):
            self.calls+=1
            payload={"goals":[dict(goal_id="g1",semantic_domain="memory",effect_intent="retrieve",requested_outcome="Read prior record",grounding="Read prior record",ambiguity="",goal_role="PRIMARY_OUTCOME",parent_goal_id=None,subgoal_justification_kind="NONE",memory_filter=dict(query_kind="PROVENANCE",time_basis="ANY_TIME",time_start="",time_end=""))],"execution_restriction":"NONE","execution_restriction_source":"","response_requirements":[dict(applies_to_goal_ids=["g1"],description="Record provenance",memory_query_kind="PROVENANCE")]}
            result=model_call_envelope(json.dumps(payload))
            if value=="ABSENT":result.pop("final_valid",None)
            else:result["final_valid"]=value
            return result
        def discover_candidates(self,**kwargs):
            self.bind_calls+=1
            r=model_call_envelope(json.dumps({"status":"BOUND","capability_id":"runtime_history_store","reason":"existing canonical history"}));r['final_valid']=True;return r

        def verify_source_candidate(self, *, source_text, candidate, deadline):
            # Explicit controlled judgment for this test request, not natural proof.
            verdict = {"status": "COMPLETE", "supported": list(("goal:g1", "requirement:0")),
                       "missing": [], "contradictions": [], "unsupported_claims": [],
                       "reason": "Independent controlled fixture judgment"}
            return {"verdict": verdict, "model_call": model_call_envelope(json.dumps(verdict))}
    port=Port();audit={}
    result=spine._model_selected_registry_details_goalframe(model_port=port,deadline=RequestDeadline(30),original_text="Read prior record",session_context={},registry_projection=projection(),audit_trace=audit)
    assert (result is not None)==(value is True)
    assert port.bind_calls==int(value is True)
    assert port.calls==1


@pytest.mark.parametrize("unregistered", ("missing_dependency_operation","previous_catalog_dependency"))
def test_dependency_identity_model_cannot_reference_absent_or_stale_operation_id(unregistered):
    payload={"candidate_operation_ids":{unregistered:True},"selection_justifications":{
        unregistered:{"goal_id":"g1","justification_kind":"DECLARED_OPERATION_DEPENDENCY","source_grounding":"Read prior record"}},
        "continuation_required":False,"continuation_reason":"","ambiguity_present":False,"confidence":.99,"reason_codes":["test"]}
    with pytest.raises(ValueError,match="unregistered"):
        parse_discovery_selection_payload(json.dumps(payload),value_key="candidate_operation_ids",allowed_values=("inspect_memory_registry",))


def test_dependency_identity_duplicate_model_identity_key_is_not_silently_collapsed():
    raw='{"candidate_operation_ids":{"inspect_memory_registry":true,"inspect_memory_registry":true},"selection_justifications":{"inspect_memory_registry":{"goal_id":"g1","justification_kind":"DECLARED_OPERATION_DEPENDENCY","source_grounding":"Read prior record"}},"continuation_required":false,"continuation_reason":"","ambiguity_present":false,"confidence":0.99,"reason_codes":["test"]}'
    with pytest.raises(ValueError,match="duplicate"):
        parse_discovery_selection_payload(raw,value_key="candidate_operation_ids",allowed_values=("inspect_memory_registry",))


@pytest.mark.parametrize("value", (None,False,True,"ABSENT",1,"true"))
def test_goal_binding_requires_final_valid_before_accepting_registered_capability(value):
    goal=dict(goal_id="g1",semantic_domain="memory",effect_intent="retrieve",requested_outcome="Read prior record",grounding="Read prior record",ambiguity="",goal_role="PRIMARY_OUTCOME",parent_goal_id="",subgoal_justification_kind="NONE")
    def call(**kwargs):
        result=model_call_envelope(json.dumps({"status":"BOUND","capability_id":"runtime_history_store","reason":"existing canonical owner"}))
        if value=="ABSENT":result.pop("final_valid",None)
        else:result["final_valid"]=value
        return result
    audit={}
    cap,status=spine._bind_goalframe_goal(call=call,goal=goal,registry_projection=select_semantic_projection_details(projection(),("runtime_history_store",)),deadline=RequestDeadline(30),binding_audit=audit)
    assert (cap=="runtime_history_store") == (value is True)
    if value is not True:
        assert status=="UNRESOLVED"
        assert audit["semantic_verification_error"]


@pytest.mark.parametrize("value", (None,False,True,"ABSENT",1,"true"))
def test_artifact_extraction_uses_same_explicit_final_valid_guard(value):
    source="Create workflow and set x to one."
    goals=[dict(goal_id="g1",semantic_domain="automation",effect_intent="change_state",requested_outcome=source,grounding=source,ambiguity="",goal_role="PRIMARY_OUTCOME",parent_goal_id="",subgoal_justification_kind="NONE")]
    calls=[];audit={}
    def understand(**kwargs):
        calls.append(kwargs)
        payload={"artifact_operation_requirements":[dict(goal_id="g1",requirement_id="a1",operation_class="ASSIGN",source_grounding="set x to one",provider_name="",provider_provenance="NONE",provider_inference_justification="")]}
        result=model_call_envelope(json.dumps(payload))
        if value=="ABSENT":result.pop("final_valid",None)
        else:result["final_valid"]=value
        return result
    attached=spine._extract_artifact_operation_requirements(understand=understand,deadline=RequestDeadline(30),original_text=source,goals=goals,execution_restriction_source="",audit_trace=audit)
    assert (attached is not None)==(value is True)
    assert len(calls)==(1 if value is True else 2)
    if value is not True:
        assert all("semantic_result_invalid" in str(x["violations"]) for x in audit["artifact_operation_extraction_attempts"])


@pytest.mark.parametrize("method", ("understand","repair","discover_candidates","discover_kinds"))
@pytest.mark.parametrize("valid", (False,True))
def test_actual_semantic_producer_sets_final_valid_from_same_schema_owner(monkeypatch,method,valid):
    from MAKSIMAR_SERVER.AI_ORCHESTRATION.model_understanding_adapter import ExistingOllamaModelUnderstandingAdapter
    schema={"type":"object","additionalProperties":False,"required":["value"],"properties":{"value":{"type":"integer"}}}
    adapter=ExistingOllamaModelUnderstandingAdapter(json_schema=schema,candidate_json_schema=schema,kind_json_schema=schema)
    calls=[]
    def single(**kwargs):
        calls.append(kwargs)
        return {**model_call_envelope(json.dumps({"value":1 if valid else "bad"})),"schema_valid":None}
    monkeypatch.setattr(adapter,"_single_model_call",single)
    result=getattr(adapter,method)(system_prompt="typed test",user_prompt="typed test",deadline=RequestDeadline(30))
    assert result["ok"] is True and result["schema_valid"] is None
    assert result["final_valid"] is valid
    assert bool(spine._model_call_verification_error(result)) is (not valid)
    assert len(calls)==(1 if valid else 2)
    assert all(c["model_id"]==transport.PRIMARY_CONVERSATION_MODEL_ID for c in calls)


@pytest.mark.parametrize("review", (False,True))
@pytest.mark.parametrize("valid", (False,True))
def test_actual_helper_producer_sets_final_valid_without_an_extra_call(monkeypatch,review,valid):
    from MAKSIMAR_SERVER.AI_ORCHESTRATION import model_understanding_adapter as module
    calls=[]
    payload={"schema_version":"helper_input_correction.v2","corrected_text":"source","ambiguity_candidates":[],"confidence":1.0,"reason_codes":["no_change_needed"],"preserve_original":True,"no_change_needed":True} if valid else {}
    def post(url,body,**kwargs):
        calls.append(body)
        return {"model":transport.HELPER_INPUT_CORRECTION_MODEL_ID,"done":True,"done_reason":"stop","message":{"content":json.dumps(payload)}}
    monkeypatch.setattr(module,"ollama_post_json",post)
    adapter=module.ExistingOllamaModelUnderstandingAdapter(json_schema={})
    args=dict(original_text="source",safe_normalized_text="source",input_channel="text",input_quality_metadata={},deadline=RequestDeadline(30))
    if review:result=adapter.review_input_correction(**args,prior_correction={},validation_error="test")
    else:result=adapter.correct_input(**args)
    assert result["ok"] is True and result["schema_valid"] is None
    assert result["final_valid"] is valid
    assert len(calls)==1 and calls[0]["model"]==transport.HELPER_INPUT_CORRECTION_MODEL_ID


@pytest.mark.parametrize("requested,selected,expected", (
    ("HISTORY", "SOURCE_DOCUMENT", False),
    ("SOURCE_DOCUMENT", "HISTORY", False),
    ("HISTORY", "HISTORY", True),
    ("SOURCE_DOCUMENT", "SOURCE_DOCUMENT", True),
    (None, "HISTORY", False),
    (None, "SOURCE_DOCUMENT", False),
))
def test_requested_memory_nullable_family_contract_does_not_rewrite_filters(requested, selected, expected):
    from copy import deepcopy
    goals = [dict(goal_id="g1", memory_filter=dict(query_kind=selected, time_basis="ANY_TIME", time_start="", time_end=""))]
    presentation = (dict(applies_to_goal_ids=["g1"], description="Requested object", memory_query_kind=requested),)
    before = deepcopy((goals, presentation))
    violations = spine._goalframe_response_requirement_violations(goals, presentation)
    assert (not violations) is expected
    assert (goals, presentation) == before


def test_requested_memory_absent_and_null_do_not_invent_a_backend_or_kind():
    from MAKSIMAR_CORE_LIB.ai_orchestration.semantic_intent_contract import ResponseRequirement
    for raw in ({}, {"memory_query_kind": None}):
        typed = ResponseRequirement(response_requirement_id="response1", applies_to_goal_ids=("g1",),
                                    description="Unspecified presentation", **raw)
        assert typed.memory_query_kind is None
        assert "memory_query_kind" not in typed.to_read_model()
    goals = [dict(goal_id="g1", semantic_domain="project", effect_intent="observe")]
    assert spine._goalframe_response_requirement_violations(goals, (
        dict(applies_to_goal_ids=["g1"], description="Unspecified presentation", memory_query_kind=None),
    )) == ()
    # Legacy omission stays absent; it is not a request to search every backend.
    assert spine._goalframe_response_requirement_violations(goals, (
        dict(applies_to_goal_ids=["g1"], description="Legacy unspecified presentation"),
    )) == ()
    assert "memory_filter" not in goals[0]


@pytest.mark.parametrize("fits", [True, False])
def test_authoritative_understanding_admission_never_reselects_semantics(monkeypatch, fits):
    registry = select_semantic_projection_details(projection(), ("runtime_history_store",))
    registry["selection_goalframes"] = [{"goal_id": "g1", "requested_outcome": "read original evidence"}]
    presentation = [{"applies_to_goal_ids": ["g1"], "description": "retain independent review status"}]
    registry["selection_response_requirements"] = presentation
    before = json.dumps(registry, sort_keys=True)
    real_builder = spine.build_request_understanding_prompt
    observed = []

    def capture(**kwargs):
        observed.append(kwargs["registry_projection"]["selection_response_requirements"])
        return real_builder(**kwargs)

    def forbidden_selection(**kwargs):
        pytest.fail("Already selected operations must not trigger semantic reselection")

    monkeypatch.setattr(spine, "build_request_understanding_prompt", capture)
    monkeypatch.setattr(spine, "measure_prompt_budget", lambda *args, **kwargs: {
        "within_budget": fits, "estimated_prompt_tokens": 10 if fits else 10000,
        "available_input_tokens": 2336, "num_ctx": 4096,
    })
    audit = {}
    kwargs = dict(call=forbidden_selection, candidate_ids=("runtime_history_store",),
        request_id="admission", original_text="read original evidence", identity=OWNER,
        session_context={}, input_preparation={}, registry_projection=registry,
        deadline=RequestDeadline(30), trace=[], audit_trace=[], repair_state=audit,
        preserve_model_selected_scope=True)
    if fits:
        assert spine._consolidate_for_understanding_budget(**kwargs) == ("runtime_history_store",)
    else:
        with pytest.raises(ValueError, match="understanding_prompt_budget_exceeded_for_model_selected_operations"):
            spine._consolidate_for_understanding_budget(**kwargs)
    assert observed == [presentation]
    assert json.dumps(registry, sort_keys=True) == before
    diagnostic = audit["understanding_prompt_admission"]
    assert diagnostic["semantic_reselection_attempted"] is False
    assert diagnostic["selected_capability_ids"] == ("runtime_history_store",)
    assert set(diagnostic["selected_operation_ids"]) == {
        op["operation_id"] for entry in registry["entries"] for op in entry["operation_contracts"]}
    assert diagnostic["status"] == ("ADMITTED" if fits else "BUDGET_EXCEEDED")


@pytest.mark.parametrize("filters", [
    ({"query_kind":"REVIEW_STATUS","time_basis":"ANY_TIME"},)*4,
    ({"query_kind":"HISTORY"},{"query_kind":"REVIEW_STATUS"}),
    (None,{"query_kind":"HISTORY"}),
])
def test_goalframe_row_projection_is_lossless_without_collapsing_distinct_memory_objects(filters):
    rows = tuple({"goal_id": f"g{i}", "requested_outcome": f"opaque outcome {i}",
                  **({"memory_filter": value} if value is not None else {})}
                 for i,value in enumerate(filters))
    frozen = json.dumps(rows, sort_keys=True)
    compact = spine._compact_goalframe_prompt_records(rows)
    resolved = (tuple(dict(compact["defaults"], **dict(zip(compact["legend"], row)))
                      for row in compact["rows"]) if isinstance(compact,dict) else compact)
    assert resolved == rows
    assert json.dumps(rows, sort_keys=True) == frozen
    assert len(json.dumps(compact,separators=(",",":")).encode()) <= len(json.dumps(rows,separators=(",",":")).encode())


def test_transport_const_projection_preserves_exact_constraints_and_canonical_schema():
    import copy
    import jsonschema
    from MAKSIMAR_SERVER.AI_ORCHESTRATION.model_understanding_adapter import model_visible_structured_schema
    literal = {"owner":"CanonicalSessionContextStore", "writer":"owner.append", "count":13,
               "path":"/actual/journal.jsonl", "configured":False, "stamp":"2026-10-15T12:00:00Z"}
    full = {"type":"object", "additionalProperties":False, "required":["fact"], "properties": {
        "fact":{"type":"object", "required":list(literal), "const":literal},
        "const":{"type":"string"}}}  # A field named const is not a schema const keyword.
    frozen = copy.deepcopy(full)
    visible = model_visible_structured_schema(full)
    assert full == frozen
    assert visible["properties"]["fact"] == {"const":literal}
    assert visible["properties"]["const"] == {"type":"string"}
    candidates = [{"fact":literal}, {}, {"fact":literal,"extra":True}, {"fact":None}]
    for key in literal:
        candidates += [{"fact":dict(literal,**{key:"altered"})}, {"fact":{k:v for k,v in literal.items() if k!=key}}]
    for value in candidates:
        assert jsonschema.Draft202012Validator(full).is_valid(value) == jsonschema.Draft202012Validator(visible).is_valid(value)
    impossible = {"type":"string", "const":17}
    assert model_visible_structured_schema(impossible) == impossible


def test_same_adapter_transports_compact_grammar_but_validates_full_original_on_both_attempts(monkeypatch):
    import copy
    from MAKSIMAR_SERVER.AI_ORCHESTRATION import model_understanding_adapter as adapter
    schema = {"type":"object", "additionalProperties":False, "required":["kind"],
              "properties":{"kind":{"type":"string", "enum":["HISTORY","REVIEW_STATUS"],"const":"REVIEW_STATUS"}}}
    original = copy.deepcopy(schema)
    posted, validated = [], []
    responses = iter([{"kind":"HISTORY"},{"kind":"REVIEW_STATUS"}])
    real_validate = adapter.validate_structured_payload
    def validate(content, authority):
        validated.append(copy.deepcopy(authority))
        return real_validate(content,authority)
    def post(url,payload,**kwargs):
        posted.append(copy.deepcopy(payload))
        return {"ok":True,"content":json.dumps(next(responses))}
    monkeypatch.setattr(adapter,"validate_structured_payload",validate)
    monkeypatch.setattr(adapter,"ollama_post_json",post)
    monkeypatch.setattr(adapter,"ollama_model_call_result",lambda raw,**kwargs:raw)
    port=adapter.ExistingOllamaModelUnderstandingAdapter(json_schema=schema)
    result=port.understand(system_prompt="typed contract",user_prompt="original",deadline=RequestDeadline(30))
    assert result["final_valid"] is True and result["retry_used"] is True
    assert validated == [original,original] and schema == original
    assert len(posted) == 2
    assert all(x["format"]["properties"]["kind"] == {"const":"REVIEW_STATUS"} for x in posted)
    assert all(x["model"] == adapter.PRIMARY_CONVERSATION_MODEL_ID and x["options"]["num_ctx"]==4096 for x in posted)
