import ast
from pathlib import Path
import hashlib
import json
import subprocess
import pytest
from MAKSIMAR_SERVER.AI_ORCHESTRATION import external_agent_provider_adapter as provider
from MAKSIMAR_CORE_LIB.ai_orchestration.semantic_intent_contract import RequestDeadline

from MAKSIMAR_CORE_LIB.ai_orchestration.semantic_intent_contract import (
    CapabilityRequirement, ExecutionPlan, Goal, OperationRequirement, PlanStep,
    RequestUnderstanding,
)
from MAKSIMAR_SERVER.AI_ORCHESTRATION.external_agent_provider_adapter import (
    ExistingExternalAgentProviderAdapter,
    PROVIDER_CLASSIFICATIONS,
    resolve_external_provider,
)



@pytest.fixture
def external_child(monkeypatch):
    """Parent adapter contract only; generated child source is never executed."""
    from MAKSIMAR_SERVER.AI_ORCHESTRATION.model_role_adapter import MODEL_ROLE_BINDINGS
    from MAKSIMAR_SERVER.AI_ORCHESTRATION.ollama_transport import model_role_for_model_id
    model = {operation: model for model, operation in MODEL_ROLE_BINDINGS.values()}["generate_code_proposal"]
    role = model_role_for_model_id(model)
    model_text = "synthetic bounded code"
    state = {"calls": [], "role": role, "exception": None, "returncode": 0, "stdout": None,
             "proof": {"agent_result": "42", "model_response": {"sha256": hashlib.sha256(model_text.encode()).hexdigest(),
                       "chars": len(model_text), "model_role": role}}}
    def run(argv, *, check, capture_output, text, timeout, env):
        assert argv[:2] == [str(provider.RUNTIME_PYTHON), "-c"]
        assert check is False and capture_output is True and text is True
        assert 0 < timeout and env["PYTHONPATH"] == str(Path(provider.__file__).resolve().parents[2])
        state["calls"].append({"argv": argv, "timeout": timeout})
        if state["exception"] is not None:
            raise state["exception"]
        script = argv[2]
        if "from smolagents import" in script:
            stdout = "SMOLAGENTS_PROOF=" + json.dumps(state["proof"])
        else:
            assert "from langgraph.graph import" in script or "from mcp import" in script
            stdout = "42\n"
        return subprocess.CompletedProcess(argv, state["returncode"], state["stdout"] if state["stdout"] is not None else stdout,
                                           "synthetic child refusal" if state["returncode"] else "")
    monkeypatch.setattr(provider.subprocess, "run", run)
    return state

def test_langgraph_provider_uses_canonical_evidence_boundary(external_child) -> None:
    understanding = RequestUnderstanding(
        request_id="lg-local", original_text="run local deterministic graph", language="en",
        goals=(Goal("g1", "run graph"),),
        required_capabilities=(CapabilityRequirement("external_agent_provider", "run", True),),
        effect_type="EXECUTE", target_scope="local_external_agent_runtime", reversibility="REVERSIBLE",
        external_side_effect=False, unresolved_capabilities=(), operation_requirements=(
            OperationRequirement(
                capability_id="external_agent_provider", operation_id="run_local_graph", purpose="run",
                required_evidence=("external_provider_result",), effect_type="EXECUTE",
                target_scope="local_external_agent_runtime", reversibility="REVERSIBLE",
                external_side_effect=False, risk_class="MUTATION", required=True,
            ),
        ), current_topic="graph", unresolved_reference="", relevant_context_trace_ids=(),
        risk_class="MUTATION", confidence=1.0, reason_codes=("typed_test",),
    )
    step = PlanStep(
        step_id="s1", goal_id="g1", capability_id="external_agent_provider", operation="run_local_graph",
        required_evidence=("external_provider_result",), effect_type="EXECUTE",
        target_scope="local_external_agent_runtime", reversibility="REVERSIBLE",
        external_side_effect=False, risk_class="MUTATION",
    )
    evidence = ExistingExternalAgentProviderAdapter().collect_evidence(
        understanding, ExecutionPlan("lg-local", (step,)), "trace-lg-local"
    )
    assert evidence.status == "COMPLETE"
    assert evidence.items[0].observation == '{"value": 42}'
    assert evidence.items[0].provider_id == "external_langgraph_provider"
    assert evidence.receipts[0].status == "COMPLETE"


def test_external_provider_resolution_is_host_owned_and_fails_closed() -> None:
    assert PROVIDER_CLASSIFICATIONS["external_adapter:langgraph"] == "AVAILABLE_PROVIDER"
    assert resolve_external_provider("external_adapter:langgraph").provider_id == "external_langgraph_provider"
    assert PROVIDER_CLASSIFICATIONS["external_adapter:autogen_agentchat"] == "PRECONDITION_REQUIRED"
    try:
        resolve_external_provider("external_adapter:autogen_agentchat")
    except ValueError as exc:
        assert "PRECONDITION_REQUIRED" in str(exc)
    else:
        raise AssertionError("gated framework must not be executable through provider port")


def test_smolagents_provider_executes_bounded_tool_with_receipt(external_child) -> None:
    understanding = RequestUnderstanding(
        request_id="sm-local", original_text="run bounded provider", language="en",
        goals=(Goal("g1", "run"),),
        required_capabilities=(CapabilityRequirement("external_agent_provider", "run", True),),
        effect_type="EXECUTE", target_scope="local_external_agent_runtime", reversibility="REVERSIBLE",
        external_side_effect=False, unresolved_capabilities=(), operation_requirements=(),
        current_topic="provider", unresolved_reference="", relevant_context_trace_ids=(),
        risk_class="MUTATION", confidence=1.0, reason_codes=("typed_test",),
    )
    step = PlanStep(
        step_id="s1", goal_id="g1", capability_id="external_agent_provider", operation="run_local_smolagent",
        required_evidence=("external_provider_result",), effect_type="EXECUTE",
        target_scope="local_external_agent_runtime", reversibility="REVERSIBLE",
        external_side_effect=False, risk_class="MUTATION",
    )
    adapter = resolve_external_provider("external_adapter:smolagents")
    deadline = RequestDeadline(3)
    evidence = adapter.collect_evidence(understanding, ExecutionPlan("sm-local", (step,)), "trace-sm-local", deadline=deadline)
    assert evidence.status == "COMPLETE"
    assert '"agent_result"' in evidence.items[0].observation
    assert '"sha256"' in evidence.items[0].observation
    assert '"model_role": "daily_coder_model"' in evidence.items[0].observation
    assert evidence.receipts[0].status == "COMPLETE"
    assert adapter.provider_id == "external_smolagents_provider"
    assert len(external_child["calls"]) == 1
    call = external_child["calls"][0]
    assert 0 < call["timeout"] <= 3
    tree = ast.parse(call["argv"][2])
    agent = next(node for node in ast.walk(tree) if isinstance(node, ast.Call) and isinstance(node.func, ast.Name) and node.func.id == "CodeAgent")
    options = {keyword.arg: keyword.value for keyword in agent.keywords}
    assert isinstance(options["tools"], ast.List) and not options["tools"].elts
    assert ast.literal_eval(options["max_steps"]) == 1
    assert "ExistingOllamaModelRoleAdapter().generate_bounded_text" in call["argv"][2]
    item, receipt = evidence.items[0], evidence.receipts[0]
    for value in (item, receipt):
        assert (value.request_id, value.trace_id, value.step_id, value.capability_id, value.operation_id, value.provider_id) == (
            understanding.request_id, "trace-sm-local", step.step_id, step.capability_id, step.operation, adapter.provider_id)
    assert item.kind == "external_provider_result"
    assert json.loads(item.observation) == external_child["proof"]
    assert item.content_hash == "sha256:" + hashlib.sha256(item.observation.encode()).hexdigest()
    assert item.source_reference == str(provider.RUNTIME_PYTHON)
    assert receipt.receipt_id == "trace-sm-local:s1"
    assert not evidence.errors


def test_mcp_provider_executes_local_stdio_tool_with_receipt(external_child) -> None:
    understanding = RequestUnderstanding(
        request_id="mcp-local", original_text="run bounded mcp tool", language="en",
        goals=(Goal("g1", "run"),), required_capabilities=(CapabilityRequirement("external_agent_provider", "run", True),),
        effect_type="EXECUTE", target_scope="local_external_agent_runtime", reversibility="REVERSIBLE",
        external_side_effect=False, unresolved_capabilities=(), operation_requirements=(), current_topic="mcp",
        unresolved_reference="", relevant_context_trace_ids=(), risk_class="MUTATION", confidence=1.0, reason_codes=("typed_test",),
    )
    step = PlanStep(step_id="s1", goal_id="g1", capability_id="external_agent_provider", operation="run_local_mcp",
                    required_evidence=("external_provider_result",), effect_type="EXECUTE", target_scope="local_external_agent_runtime",
                    reversibility="REVERSIBLE", external_side_effect=False, risk_class="MUTATION")
    evidence = resolve_external_provider("external_adapter:mcp_python_sdk").collect_evidence(
        understanding, ExecutionPlan("mcp-local", (step,)), "trace-mcp-local")
    assert evidence.status == "COMPLETE"
    assert '"value": 42' in evidence.items[0].observation
    assert evidence.receipts[0].status == "COMPLETE"


@pytest.fixture
def smol_request():
    # Reuse the original typed request/plan shape, without invoking another test.
    understanding = RequestUnderstanding(request_id="sm-negative", original_text="bounded offline fixture", language="en",
        goals=(Goal("g1", "run"),), required_capabilities=(CapabilityRequirement("external_agent_provider", "run", True),),
        effect_type="EXECUTE", target_scope="local_external_agent_runtime", reversibility="REVERSIBLE",
        external_side_effect=False, unresolved_capabilities=(), operation_requirements=(), current_topic="provider",
        unresolved_reference="", relevant_context_trace_ids=(), risk_class="MUTATION", confidence=1.0, reason_codes=("typed_test",))
    step = PlanStep(step_id="s1", goal_id="g1", capability_id="external_agent_provider", operation="run_local_smolagent",
        required_evidence=("external_provider_result",), effect_type="EXECUTE", target_scope="local_external_agent_runtime",
        reversibility="REVERSIBLE", external_side_effect=False, risk_class="MUTATION")
    return understanding, ExecutionPlan(understanding.request_id, (step,))


@pytest.mark.parametrize("case", ["missing_marker", "empty_proof", "array", "string", "number", "null", "invalid_json",
    "empty_digest", "invalid_digest", "short_digest", "digest_type", "missing_model_response", "response_type",
    "invalid_result", "result_type", "duplicate_marker", "conflicting_markers", "duplicate_json_key",
    "missing_chars", "chars_zero", "chars_negative", "chars_bool", "chars_float", "chars_string",
    "missing_role", "wrong_role", "role_type", "empty_role", "conflicting_metadata", "nonzero", "timeout",
    "deadline_before", "deadline_during", "unexpected_exception"])
def test_smolagents_invalid_or_failed_child_never_issues_success(external_child, smol_request, case):
    state = external_child; proof = state["proof"]; metadata = proof["model_response"]
    deadline = RequestDeadline(3)
    if case == "missing_marker": state["stdout"] = "42 sha256 without proof marker"
    elif case == "empty_proof": state["stdout"] = "SMOLAGENTS_PROOF="
    elif case in {"array", "string", "number", "null"}:
        state["proof"] = {"array": ["42", "sha256"], "string": "42 sha256", "number": 42, "null": None}[case]
    elif case == "invalid_json": state["stdout"] = 'SMOLAGENTS_PROOF={"agent_result":"42",sha256}'
    elif case == "empty_digest": metadata["sha256"] = ""
    elif case == "invalid_digest": metadata["sha256"] = "g" * 64
    elif case == "short_digest": metadata["sha256"] = "a" * 63
    elif case == "digest_type": metadata["sha256"] = 42
    elif case == "missing_model_response": state["proof"] = {"agent_result": "42", "unrelated_metadata": "sha256"}
    elif case == "response_type": proof["model_response"] = [metadata]
    elif case == "invalid_result": proof["agent_result"] = "unrelated 42 in prose"
    elif case == "result_type": proof["agent_result"] = 42
    elif case == "duplicate_marker": state["stdout"] = ("SMOLAGENTS_PROOF=" + json.dumps(proof) + "\n") * 2
    elif case == "conflicting_markers": state["stdout"] = "SMOLAGENTS_PROOF={}\nSMOLAGENTS_PROOF=" + json.dumps(proof)
    elif case == "duplicate_json_key": state["stdout"] = "SMOLAGENTS_PROOF=" + json.dumps(proof).replace('"chars":', '"chars":0,"chars":')
    elif case == "missing_chars": metadata.pop("chars")
    elif case.startswith("chars_"): metadata["chars"] = {"chars_zero": 0, "chars_negative": -1, "chars_bool": True,
        "chars_float": 2.0, "chars_string": "20"}[case]
    elif case == "missing_role": metadata.pop("model_role")
    elif case == "wrong_role": metadata["model_role"] = "unregistered-fixture-role"
    elif case == "role_type": metadata["model_role"] = []
    elif case == "empty_role": metadata["model_role"] = ""
    elif case == "conflicting_metadata": proof["sha256"] = "0" * 64
    elif case == "nonzero": state["returncode"] = 1
    elif case == "timeout": state["exception"] = subprocess.TimeoutExpired("synthetic child", 3)
    elif case == "deadline_before": deadline.cancel()
    elif case == "deadline_during":
        # Cancel at the controlled subprocess boundary, without sleeping or a live child.
        state["exception"] = None
        original = provider.subprocess.run
        def late(*args, **kwargs):
            result = original(*args, **kwargs); deadline.cancel(); return result
        # Local patch context avoids leaking the seam into other tests.
        from unittest.mock import patch
        with patch.object(provider.subprocess, "run", late):
            result = resolve_external_provider("external_adapter:smolagents").collect_evidence(
                *smol_request, "trace-sm-negative", deadline=deadline)
        assert result.status == "UNAVAILABLE" and not result.items and not result.receipts and result.errors
        return
    else: state["exception"] = RuntimeError("synthetic unexpected exception")
    result = resolve_external_provider("external_adapter:smolagents").collect_evidence(*smol_request, "trace-sm-negative", deadline=deadline)
    assert result.status == "UNAVAILABLE" and not result.items and not result.receipts
    assert result.errors and all(error.startswith("run_local_smolagent:") for error in result.errors)
    assert len(state["calls"]) == (0 if case == "deadline_before" else 1)


@pytest.mark.parametrize("provider_id", ["external_adapter:autogen_agentchat", "external_adapter:autogen_ext",
    "external_adapter:openai_agents_sdk", "external_adapter:unknown"])
def test_unregistered_or_gated_provider_never_calls_child(external_child, provider_id):
    with pytest.raises(ValueError, match="provider_not_runtime_executable"):
        resolve_external_provider(provider_id)
    assert not external_child["calls"]


def test_unsupported_external_operation_has_no_child_or_receipt(external_child, smol_request):
    from dataclasses import replace
    understanding, plan = smol_request
    plan = replace(plan, steps=(replace(plan.steps[0], operation="unsupported_fixture_operation"),))
    result = resolve_external_provider("external_adapter:smolagents").collect_evidence(understanding, plan, "unsupported")
    assert result.status == "UNAVAILABLE" and result.errors and not result.items and not result.receipts
    assert not external_child["calls"]


def test_current_child_producer_metadata_matches_existing_model_role_contract(external_child, smol_request, monkeypatch):
    """Execute only producer glue with fake smolagents/HTTP, never a model or child process."""
    import contextlib
    import io
    import sys
    import types
    from MAKSIMAR_SERVER.AI_ORCHESTRATION import ollama_transport as transport
    calls = []
    def post(_url, payload, **kwargs):
        calls.append(payload)
        return {"model": payload["model"], "message": {"content": "print(42)"}, "done": True, "done_reason": "stop"}
    monkeypatch.setattr(transport, "ollama_post_json", post)
    class CodeAgent:
        def __init__(self, *, tools, model, max_steps):
            assert tools == [] and max_steps == 1
            self.model = model
        def run(self, _task):
            message = self.model.generate([])
            assert message.role == "assistant" and message.content == "print(42)"
            return 42  # Controlled agent result; model text is NOT executed.
    module = types.ModuleType("smolagents")
    module.CodeAgent, module.Model, module.ChatMessage = CodeAgent, object, types.SimpleNamespace
    monkeypatch.setitem(sys.modules, "smolagents", module)
    def child(argv, **kwargs):
        assert argv[:2] == [str(provider.RUNTIME_PYTHON), "-c"] and 0 < kwargs["timeout"] <= 3
        output = io.StringIO()
        with contextlib.redirect_stdout(output):
            exec(compile(argv[2], "<synthetic-child-producer>", "exec"), {"__name__": "synthetic_child"})
        return subprocess.CompletedProcess(argv, 0, output.getvalue(), "")
    monkeypatch.setattr(provider.subprocess, "run", child)
    bundle = resolve_external_provider("external_adapter:smolagents").collect_evidence(
        *smol_request, "producer-contract", deadline=RequestDeadline(3))
    assert bundle.status == "COMPLETE" and len(calls) == 1
    result = json.loads(bundle.items[0].observation)
    assert result["model_response"] == {"sha256": hashlib.sha256(b"print(42)").hexdigest(),
        "chars": len("print(42)"), "model_role": external_child["role"]}
    assert bundle.receipts[0].status == "COMPLETE"
