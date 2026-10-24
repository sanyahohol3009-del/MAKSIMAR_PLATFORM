import hashlib
from copy import deepcopy
from MAKSIMAR_SERVER.CLIENT_LEARNING_INPUT.developer_experience_contract import qualify_provider_execution_experience


def evidence():
    ids = dict(request_id="r", trace_id="t", step_id="s", capability_id="browser.web",
               operation_id="browser.open_read", provider_id="browser_playwright_provider")
    observation = '{"title":"Example Domain"}'
    return {"status": "COMPLETE", "items": [{**ids, "kind": "browser_page_opened",
            "observation": observation, "content_hash": "sha256:" + hashlib.sha256(observation.encode()).hexdigest(),
            "observed_at": "2026-10-11T12:00:00Z"}],
            "receipts": [{**ids, "receipt_id": "t:s", "status": "COMPLETE"}]}


def test_real_host_receipt_and_readback_qualify_without_training_permission():
    result = qualify_provider_execution_experience(task_ref="read page", trace_id="t",
        operation_status="COMPLETE", evidence=evidence())
    assert result.verification_status == "VERIFIED"
    assert result.verification_refs == ("receipt://t:s",)
    assert result.training_export_allowed is False
    assert result.training_candidate_creation_allowed is False


def test_self_report_without_matching_host_receipt_does_not_qualify():
    source = evidence()
    for field in ("provider_id", "step_id", "capability_id", "trace_id"):
        altered = deepcopy(source)
        altered["receipts"][0][field] = "different"
        assert qualify_provider_execution_experience(task_ref="read page", trace_id="t",
            operation_status="COMPLETE", evidence=altered) is None


def test_partial_or_tampered_observation_does_not_qualify():
    source = evidence()
    assert qualify_provider_execution_experience(task_ref="read page", trace_id="t",
        operation_status="PARTIAL_EVIDENCE", evidence=source) is None
    source["items"][0]["observation"] = "model self-report without readback"
    assert qualify_provider_execution_experience(task_ref="read page", trace_id="t",
        operation_status="COMPLETE", evidence=source) is None


def test_revision_preserves_attempt_without_falsifying_rejection_or_verification():
    from MAKSIMAR_SERVER.CLIENT_LEARNING_INPUT.developer_experience_contract import capture_proposal_experience
    fields = dict(actor="CODEX", task_ref="bounded analysis", proposal_ref="proposal://p",
                  audit_ref="audit://a", verification_ref="evidence://e",
                  experience_kind="ARCHITECTURE_DESIGN", verified=False)
    revised = capture_proposal_experience(**fields, audit_verdict="REVISE")
    assert revised.verification_status == "PARTIAL"
    assert revised.failure_class == "proposal_audit_revision_required"
    assert revised.training_export_allowed is False
    assert revised.actor == "CODEX"
    assert capture_proposal_experience(**fields).verification_status == "REJECTED"
    assert capture_proposal_experience(**fields, audit_verdict="REJECTED").verification_status == "REJECTED"


def test_accepted_proposal_without_execution_stays_pending_and_cannot_train():
    from MAKSIMAR_SERVER.CLIENT_LEARNING_INPUT.developer_experience_contract import capture_proposal_experience
    result = capture_proposal_experience(actor="CODEX", task_ref="proposed design", proposal_ref="proposal://p",
        audit_ref="audit://a", verification_ref="evidence://delivery", experience_kind="ARCHITECTURE_DESIGN",
        verified=False, audit_verdict="ACCEPTED_FOR_EXPERIMENT")
    assert result.verification_status == "PENDING" and result.outcome == "pending"
    assert result.failure_class is None
    assert result.verification_refs == ()
    assert result.training_eligible is False and result.training_export_allowed is False
