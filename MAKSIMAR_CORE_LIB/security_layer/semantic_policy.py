from __future__ import annotations

"""General typed identity, safety and per-step permission policy."""

from MAKSIMAR_CORE_LIB.ai_orchestration.semantic_intent_contract import (
    IdentityContext, PermissionDecision, PermissionEvaluationPort, RequestUnderstanding,
)
from MAKSIMAR_CORE_LIB.security_layer.jarvis_speaker_profile_resolver import resolve_family_profile


class SemanticPolicyEvaluator(PermissionEvaluationPort):
    """Evaluate each typed plan step without changing the understood intention."""

    policy_version = "project_read_permission.v1"

    def evaluate(self, *, capability_id: str, operation_id: str = "", risk_class: str,
                 effect_type: str = "OBSERVE", target_scope: str = "unknown",
                 reversibility: str = "UNKNOWN", external_side_effect: bool = False,
                 identity: IdentityContext, trace_id: str, step_id: str = "") -> PermissionDecision:
        read_only = (
            effect_type == "OBSERVE" and risk_class == "READ_ONLY"
            and not external_side_effect
        )
        owner_low_risk_autonomy = (
            identity.owner_authorized
            and risk_class == "MUTATION"
            and reversibility == "REVERSIBLE"
            and not external_side_effect
        )
        approval_required = (
            not read_only and not owner_low_risk_autonomy
            and identity.owner_authorized
            and (risk_class in {"MUTATION", "DANGEROUS", "UNKNOWN"} or external_side_effect)
        )
        granted = read_only or owner_low_risk_autonomy
        denial_reason = ""
        if approval_required:
            denial_reason = "step_policy_requires_approval"
        elif not granted:
            denial_reason = "step_policy_denied"
        return PermissionDecision(
            granted=granted, capability_id=capability_id, identity_source=identity.identity_source,
            policy_version=self.policy_version,
            denial_reason=denial_reason, trace_id=trace_id, operation_id=operation_id,
            approval_required=approval_required, step_id=step_id,
        )


def validate_structured_safety(understanding: RequestUnderstanding) -> dict[str, object]:
    """Validate typed semantic effects without inspecting or rewriting raw text.

    Consistency is checked on TYPED fields only (effect_type, risk_class,
    external_side_effect, capability ownership), never on raw text or goal wording.
    """
    reasons: list[str] = []
    required_operations = tuple(item for item in understanding.operation_requirements if item.required)
    for requirement in understanding.operation_requirements:
        if requirement.effect_type == "OBSERVE" and requirement.risk_class != "READ_ONLY":
            reasons.append(f"observe_requires_read_only_risk:{requirement.operation_id}")
        if requirement.effect_type == "OBSERVE" and requirement.external_side_effect:
            reasons.append(f"observe_cannot_claim_external_side_effect:{requirement.operation_id}")
        if requirement.effect_type != "OBSERVE" and requirement.risk_class == "READ_ONLY":
            reasons.append(f"side_effecting_intent_cannot_be_read_only:{requirement.operation_id}")
        if requirement.capability_id == "conversation.respond" and (
            requirement.effect_type != "OBSERVE" or requirement.risk_class != "READ_ONLY"
            or requirement.external_side_effect
        ):
            reasons.append(f"conversation_response_must_be_observe_read_only:{requirement.operation_id}")
        if requirement.capability_id == "project.read" and (
            requirement.effect_type != "OBSERVE" or requirement.risk_class != "READ_ONLY"
            or requirement.external_side_effect
        ):
            reasons.append(f"project_read_must_be_observe_read_only:{requirement.operation_id}")
    operation_effects = {item.effect_type for item in required_operations}
    operation_risks = {item.risk_class for item in required_operations}
    if len(operation_effects) == 1 and understanding.effect_type not in operation_effects:
        reasons.append("top_level_effect_mismatch")
    if len(operation_risks) == 1 and understanding.risk_class not in operation_risks:
        reasons.append("top_level_risk_mismatch")
    if required_operations and understanding.external_side_effect != any(
        item.external_side_effect for item in required_operations
    ):
        reasons.append("top_level_external_side_effect_mismatch")
    if any(item.effect_type != "OBSERVE" for item in required_operations) and understanding.risk_class == "READ_ONLY":
        reasons.append("top_level_cannot_hide_side_effect_as_read_only")
    return {
        "schema_version": "structured_safety_validation.v1",
        "valid": not reasons,
        "effect_type": understanding.effect_type,
        "target_scope": understanding.target_scope,
        "reversibility": understanding.reversibility,
        "external_side_effect": understanding.external_side_effect,
        "risk_class": understanding.risk_class,
        "approval_decision_deferred_to_step_policy": True,
        "reason_codes": tuple(reasons) if reasons else ("structured_semantics_consistent",),
        "intent_rewritten": False,
        "raw_text_inspected": False,
    }


def identity_context_from_http_payload(payload: dict[str, object]) -> IdentityContext:
    claim = payload.get("identity")
    if not isinstance(claim, dict):
        return IdentityContext("anonymous", "http_unverified", "unknown", False, False, "", "JARVIS")
    source = str(claim.get("source", "http_unverified"))
    profile = str(claim.get("profile_type", "unknown"))
    verified = claim.get("verified") is True
    trusted_sources = {"verified_voice_identity", "local_terminal_session", "authenticated_http_session", "trusted_ui_session"}
    trusted_session = claim.get("trusted_session") is True
    source_trusted = source in trusted_sources
    # Voice/local terminal evidence is intrinsically local after verification; HTTP/UI additionally
    # requires the authentication layer to assert a trusted session.
    trust_satisfied = source_trusted and (source in {"verified_voice_identity", "local_terminal_session"} or trusted_session)
    trusted = verified and trust_satisfied and profile in {"owner", "trusted_family", "child"}
    identity_id = str(claim.get("identity_id", "unknown"))
    resolved_profile = resolve_family_profile(identity_id=identity_id, profile_type=profile) if trusted else None
    display_name = resolved_profile.display_name if resolved_profile is not None else ""
    return IdentityContext(
        identity_id, source, profile, trusted and profile == "owner", trusted,
        display_name, "JARVIS",
    )
