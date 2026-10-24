from MAKSIMAR_CORE_LIB.ai_orchestration.semantic_intent_contract import (
    CapabilityRequirement, ExecutionPlan, Goal, PlanStep, RequestUnderstanding,
)
from MAKSIMAR_SERVER.AI_ORCHESTRATION.memory_retrieval_adapter import ExistingMemoryRetrievalAdapter
from MAKSIMAR_CORE_LIB.retrieval_backend.retrieval_backend_adapter_contract import build_default_retrieval_backend_adapter_contract
import json
import hashlib
from MAKSIMAR_CORE_LIB.ai_orchestration.semantic_intent_contract import IdentityContext
from MAKSIMAR_SERVER.AI_ORCHESTRATION import session_memory_store as store


def test_canonical_memory_retrieval_returns_provenance_bound_evidence(monkeypatch, tmp_path) -> None:
    monkeypatch.setattr(store, "SESSION_MEMORY_ROOT", tmp_path)
    identity = IdentityContext("owner", "authenticated_http_session", "owner", True, True)
    written = store.CanonicalSessionContextStore().append("isolated-session", identity,
        user_text="Record the runtime truth path", assistant_text="Recorded from a real isolated append",
        topic="runtime", unresolved_reference="", trace_id="durable-runtime-truth")
    assert written["persistence_status"] == "PERSISTED"
    understanding = RequestUnderstanding(
        request_id="memory-e2e", original_text="What is the runtime truth path?", language="en",
        goals=(Goal("g1", "retrieve history"),),
        required_capabilities=(CapabilityRequirement("runtime_history_store", "search", True),),
        effect_type="OBSERVE", target_scope="local_project_history", reversibility="REVERSIBLE",
        external_side_effect=False, unresolved_capabilities=(), operation_requirements=(),
        current_topic="memory", unresolved_reference="", relevant_context_trace_ids=(),
        risk_class="READ_ONLY", confidence=1.0, reason_codes=("typed_test",),
    )
    step = PlanStep(
        step_id="search", goal_id="g1", capability_id="runtime_history_store", operation="search_history",
        required_evidence=("history_search",), effect_type="OBSERVE", target_scope="local_project_history",
        reversibility="REVERSIBLE", external_side_effect=False, risk_class="READ_ONLY",
        parameters=(("query", "runtime truth path"),),
    )
    bundle = ExistingMemoryRetrievalAdapter().collect_evidence(
        understanding, ExecutionPlan("memory-e2e", (step,)), "trace-memory-e2e"
    )
    assert bundle.status == "COMPLETE"
    assert bundle.receipts[0].status == "COMPLETE"
    assert bundle.items[0].kind == "history_search"
    observation = json.loads(bundle.items[0].observation)
    assert observation["history_query"]["matched_memory_ids"] == ["durable-runtime-truth"]
    assert observation["history_query"]["matches"][0]["user_text"] == written["user_text"]
    assert observation["source"] == str(tmp_path / store.SESSION_TURN_LOG_NAME)
    assert "ARCH-0001" not in bundle.items[0].observation
    assert bundle.items[0].content_hash == "sha256:" + hashlib.sha256(bundle.items[0].observation.encode()).hexdigest()
    assert bundle.receipts[0].step_id == bundle.items[0].step_id == "search"
    assert bundle.items[0].source_reference == "memory://search_history"


def test_retrieval_backend_is_not_canonical_memory_write_authority() -> None:
    contract = build_default_retrieval_backend_adapter_contract()
    assert contract.source_of_truth is False
    assert contract.direct_canonical_write_allowed is False
    assert contract.runtime_mutation_allowed is False
    assert contract.auto_promotion_allowed is False


def _read_session_bundle():
    understanding = RequestUnderstanding(
        request_id="session-source-contract", original_text="Read the current session", language="en",
        goals=(Goal("g1", "read session"),),
        required_capabilities=(CapabilityRequirement("session_memory", "read", True),),
        effect_type="OBSERVE", target_scope="local_session_history", reversibility="REVERSIBLE",
        external_side_effect=False, unresolved_capabilities=(), operation_requirements=(),
        current_topic="memory", unresolved_reference="", relevant_context_trace_ids=(),
        risk_class="READ_ONLY", confidence=1.0, reason_codes=("typed_test",),
    )
    step = PlanStep(
        step_id="session-read", goal_id="g1", capability_id="session_memory", operation="read_session_memory",
        required_evidence=("session_memory",), effect_type="OBSERVE", target_scope="local_session_history",
        reversibility="REVERSIBLE", external_side_effect=False, risk_class="READ_ONLY",
    )
    return ExistingMemoryRetrievalAdapter().collect_evidence(
        understanding, ExecutionPlan("session-source-contract", (step,)), "trace-session-source-contract"
    )


def test_typed_session_reader_uses_canonical_journal_instead_of_compatibility_cache(monkeypatch, tmp_path):
    monkeypatch.setattr(store, "SESSION_MEMORY_ROOT", tmp_path)
    monkeypatch.setattr(store, "SESSION_STATE_PATH", tmp_path / "compatibility.json")
    store.SESSION_STATE_PATH.write_text(json.dumps({"recent_turns": [{"user_text": "PHANTOM_IN_CACHE"}]}))
    identity = IdentityContext("owner", "authenticated_http_session", "owner", True, True)
    store.CanonicalSessionContextStore().append("isolated-session", identity,
        user_text="Current canonical user record", assistant_text="Current canonical answer",
        topic="memory", unresolved_reference="", trace_id="canonical-current-session-record")
    before = store._session_turn_log_path().read_bytes()
    bundle = _read_session_bundle()
    assert bundle.status == "COMPLETE"
    observed = json.loads(bundle.items[0].observation)
    assert observed["source"] == str(store._session_turn_log_path())
    assert observed["records"][0]["trace_id"] == "canonical-current-session-record"
    assert "PHANTOM_IN_CACHE" not in bundle.items[0].observation
    assert store._session_turn_log_path().read_bytes() == before


def test_typed_session_reader_cannot_fall_back_to_cache_after_journal_integrity_failure(monkeypatch, tmp_path):
    monkeypatch.setattr(store, "SESSION_MEMORY_ROOT", tmp_path)
    monkeypatch.setattr(store, "SESSION_STATE_PATH", tmp_path / "compatibility.json")
    store.SESSION_STATE_PATH.write_text(json.dumps({"recent_turns": [{"user_text": "PHANTOM_IN_CACHE"}]}))
    store._session_turn_log_path().write_bytes(b'{"source":BROKEN')
    bundle = _read_session_bundle()
    assert bundle.status != "COMPLETE"
    assert not bundle.items
    assert any("read_session_memory:ValueError" in error for error in bundle.errors)
