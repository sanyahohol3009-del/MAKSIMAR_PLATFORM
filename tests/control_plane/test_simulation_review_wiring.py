import json
from dataclasses import replace
from types import SimpleNamespace

from CONTROL_PLANE.canonical_semantic_spine import _execute_evidence
from MAKSIMAR_CORE_LIB.ai_orchestration.semantic_intent_contract import (
    EvidenceBundle,
    EvidenceItem,
    ExecutionPlan,
    ExecutionReceipt,
    PlanStep,
    utc_observed_at,
)
from MAKSIMAR_CORE_LIB.workers_registry.simulation_io_contracts import SimulationEngineResult


TRACE_ID = "trace-review-test"
REQUEST_ID = "request-review-test"
STEP_ID = "step-1"
CAPABILITY_ID = "skill_simulation_simulation_analysis"


def _plan() -> ExecutionPlan:
    return ExecutionPlan(
        request_id=REQUEST_ID,
        steps=(PlanStep(
            step_id=STEP_ID,
            goal_id="goal-1",
            capability_id=CAPABILITY_ID,
            operation="analyze_simulation",
            required_evidence=("simulation_result",),
            effect_type="OBSERVE",
            target_scope="local_simulation_runtime",
            reversibility="REVERSIBLE",
            external_side_effect=False,
            risk_class="READ_ONLY",
        ),),
    )


def _simulation_bundle() -> EvidenceBundle:
    result = SimulationEngineResult(
        task_id=f"{REQUEST_ID}:{STEP_ID}",
        backend_kind="python",
        status="completed",
        score=1.0,
        output_payload_ref="artifact://simulation/result",
        summary="comparison complete",
        trace_id=TRACE_ID,
    )
    item = EvidenceItem(
        kind="simulation_result",
        source="simulation_worker",
        observation=json.dumps(result.__dict__ if hasattr(result, "__dict__") else {
            name: getattr(result, name) for name in result.__dataclass_fields__
        }),
        scope="local_simulation_runtime",
        confidence=1.0,
        trace_id=TRACE_ID,
        observed_at=utc_observed_at(),
        request_id=REQUEST_ID,
        step_id=STEP_ID,
        capability_id=CAPABILITY_ID,
        operation_id="analyze_simulation",
        provider_id="existing_simulation_worker_runtime",
        source_reference="artifact://simulation/result",
    )
    receipt = ExecutionReceipt(
        receipt_id="receipt-1",
        request_id=REQUEST_ID,
        trace_id=TRACE_ID,
        step_id=STEP_ID,
        capability_id=CAPABILITY_ID,
        operation_id="analyze_simulation",
        provider_id="existing_simulation_worker_runtime",
        status="COMPLETE",
        result="simulation_result",
    )
    return EvidenceBundle(
        request_id=REQUEST_ID,
        capability_id=CAPABILITY_ID,
        trace_id=TRACE_ID,
        status="COMPLETE",
        items=(item,),
        limitations=(),
        receipts=(receipt,),
        errors=(),
    )


class _SimulationPort:
    def collect_evidence(self, understanding, plan, trace_id, deadline):
        return _simulation_bundle()


class _NonSimulationPort:
    def collect_evidence(self, understanding, plan, trace_id, deadline):
        item = EvidenceItem(
            kind="generic_result", source="other_worker", observation="{}",
            scope="local", confidence=1.0, trace_id=TRACE_ID,
            observed_at=utc_observed_at(), request_id=REQUEST_ID,
            step_id=STEP_ID, capability_id="other.capability",
            operation_id="other_operation", provider_id="other_provider",
        )
        return EvidenceBundle(
            request_id=REQUEST_ID, capability_id="other.capability",
            trace_id=TRACE_ID, status="COMPLETE", items=(item,), limitations=(),
            receipts=(), errors=(),
        )


class _MalformedSimulationPort:
    def collect_evidence(self, understanding, plan, trace_id, deadline):
        bundle = _simulation_bundle()
        return replace(bundle, items=(replace(bundle.items[0], observation="{"),))


def test_simulation_receipt_is_reviewed_before_bundle_completion():
    bundle = _execute_evidence(
        SimpleNamespace(request_id=REQUEST_ID),
        _plan(),
        TRACE_ID,
        identity=None,
        session_context={},
        deadline=None,
        capability_ids=(CAPABILITY_ID,),
        ports={CAPABILITY_ID: _SimulationPort()},
    )
    reviews = [item for item in bundle.items if item.kind == "sandbox_review"]
    assert bundle.status == "COMPLETE"
    assert len(reviews) == 1
    assert json.loads(reviews[0].observation)["review_status"] == "REVIEWED"
    assert bundle.receipts[0].operation_id == "analyze_simulation"


def test_review_rejection_fails_closed(monkeypatch):
    import MAKSIMAR_SERVER.SANDBOX_REVIEW.sandbox_result_reader as reader

    monkeypatch.setattr(reader, "review_simulation_result", lambda result: {
        "review_status": "REJECTED", "reason": "policy_rejected",
    })
    bundle = _execute_evidence(
        SimpleNamespace(request_id=REQUEST_ID), _plan(), TRACE_ID,
        identity=None, session_context={}, deadline=None,
        capability_ids=(CAPABILITY_ID,), ports={CAPABILITY_ID: _SimulationPort()},
    )
    reviews = [item for item in bundle.items if item.kind == "sandbox_review"]
    assert bundle.status == "PARTIAL"
    assert json.loads(reviews[0].observation)["review_status"] == "REJECTED"
    assert reviews[0].confidence == 0.0
    assert "sandbox_review:step-1:policy_rejected" in bundle.errors


def test_non_simulation_result_is_not_sent_to_simulation_review():
    capability = "other.capability"
    plan = ExecutionPlan(
        request_id=REQUEST_ID,
        steps=(PlanStep(
            step_id=STEP_ID, goal_id="goal-1", capability_id=capability,
            operation="other_operation", required_evidence=("generic_result",),
            effect_type="OBSERVE", target_scope="local", reversibility="REVERSIBLE",
            external_side_effect=False, risk_class="READ_ONLY",
        ),),
    )
    bundle = _execute_evidence(
        SimpleNamespace(request_id=REQUEST_ID), plan, TRACE_ID,
        identity=None, session_context={}, deadline=None,
        capability_ids=(capability,), ports={capability: _NonSimulationPort()},
    )
    assert not any(item.kind == "sandbox_review" for item in bundle.items)


def test_malformed_simulation_result_fails_closed():
    bundle = _execute_evidence(
        SimpleNamespace(request_id=REQUEST_ID), _plan(), TRACE_ID,
        identity=None, session_context={}, deadline=None,
        capability_ids=(CAPABILITY_ID,), ports={CAPABILITY_ID: _MalformedSimulationPort()},
    )
    review = next(item for item in bundle.items if item.kind == "sandbox_review")
    assert bundle.status == "PARTIAL"
    assert json.loads(review.observation)["review_status"] == "REJECTED"
    assert review.confidence == 0.0
