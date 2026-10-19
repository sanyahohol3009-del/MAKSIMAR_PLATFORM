"""Offline typed/security boundary proof for the real canonical contracts."""
import copy
import pytest
from MAKSIMAR_CORE_LIB.ai_orchestration.semantic_intent_contract import (
    IdentityContext, validate_source_candidate_verdict, validate_response_obligation_coverage,
)
from MAKSIMAR_CORE_LIB.ai_orchestration.helper_model_decision_parser import parse_helper_input_correction_payload
from MAKSIMAR_CORE_LIB.security_layer.semantic_policy import SemanticPolicyEvaluator


def test_declared_obligations_survive_without_duplicate_or_subject_substitution():
    expected=({"response_requirement_id":"r1","applies_to_goal_ids":["g1"],"description":"first"},{"response_requirement_id":"r2","applies_to_goal_ids":["g2"],"description":"second"})
    validate_response_obligation_coverage(expected,copy.deepcopy(expected))
    for bad in [expected[:1],(expected[0],expected[0]),(expected[0],{**expected[1],"applies_to_goal_ids":["g1"]}),(expected[0],{**expected[1],"response_requirement_id":"invented"})]:
        with pytest.raises(ValueError):validate_response_obligation_coverage(expected,bad)


@pytest.mark.parametrize("bad",["invented","missing","contradiction"])
def test_completeness_verdict_cannot_promote_invalid_candidate_coverage(bad):
    verdict={"status":"COMPLETE","supported":["f1","f2"],"missing":[],"contradictions":[],"unsupported_claims":[],"reason":"synthetic evidence"}
    assert validate_source_candidate_verdict(verdict,("f1","f2"))=="COMPLETE"
    if bad=="invented":verdict["supported"].append("foreign")
    elif bad=="missing":verdict["supported"].pop()
    else:verdict["contradictions"].append("unsupported relation")
    assert validate_source_candidate_verdict(verdict,("f1","f2"))=="UNPROVEN"


@pytest.mark.parametrize("field",["capability_id","operation_id","provider_id","selected_tools","policy_decision"])
def test_helper_remains_correction_only(field):
    payload={"schema_version":"helper_input_correction.v2","corrected_text":"unchanged","ambiguity_candidates":[],"confidence":1.0,"reason_codes":["preserved"],"preserve_original":True,"no_change_needed":True}
    assert parse_helper_input_correction_payload(payload,expected_safe_normalized_text="unchanged").corrected_text=="unchanged"
    payload[field]="forbidden-selection"
    with pytest.raises(ValueError):parse_helper_input_correction_payload(payload,expected_safe_normalized_text="unchanged")


@pytest.mark.parametrize("trusted_owner",[False,True])
def test_typed_mutation_authority_is_not_inferred_from_a_model_or_profile_label(trusted_owner):
    identity=IdentityContext("synthetic-owner","authenticated_http_session","owner",trusted_owner,trusted_owner)
    policy=SemanticPolicyEvaluator()
    harmless=policy.evaluate(capability_id="example",operation_id="read",risk_class="READ_ONLY",effect_type="OBSERVE",identity=identity,trace_id="trace")
    assert harmless.granted
    dangerous=policy.evaluate(capability_id="example",operation_id="send",risk_class="DANGEROUS",effect_type="EXPORT",external_side_effect=True,identity=identity,trace_id="trace",step_id="s1")
    assert not dangerous.granted
    assert dangerous.approval_required is trusted_owner
