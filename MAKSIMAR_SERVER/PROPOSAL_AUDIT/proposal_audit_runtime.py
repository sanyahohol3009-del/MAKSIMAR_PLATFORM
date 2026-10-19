"""Deterministic runtime audit for an already-generated proposal artifact."""
from __future__ import annotations

from dataclasses import dataclass
from typing import Any



@dataclass(frozen=True, slots=True)
class ProposalAuditResult:
    proposal_id: str
    verdict: str
    reasons: tuple[str, ...]
    sandbox_required: bool
    production_mutation_allowed: bool
    gate_ready: bool

    def to_read_model(self) -> dict[str, Any]:
        return {
            "proposal_id": self.proposal_id,
            "verdict": self.verdict,
            "reasons": self.reasons,
            "sandbox_required": self.sandbox_required,
            "production_mutation_allowed": self.production_mutation_allowed,
            "gate_ready": self.gate_ready,
        }


def audit_proposal_runtime(proposal: dict[str, Any]) -> ProposalAuditResult:
    """Audit a proposal artifact without invoking another model or mutating state."""
    if not isinstance(proposal, dict):
        raise TypeError("proposal must be an object")
    proposal_id = str(proposal.get("proposal_id") or proposal.get("package_id") or "proposal_unknown")
    reasons: list[str] = []
    # This owner audits a proposal artifact, never authorizes its described
    # actions. Authority is evaluated on the canonical typed execution plan by
    # SemanticPolicyEvaluator; proposal wording cannot create a second policy.
    # Existing typed requests for production mutation remain rejected here.
    if bool(proposal.get("production_mutation", False)) or bool(proposal.get("auto_apply", False)):
        reasons.append("production_mutation_requested")
    if not str(proposal.get("rollback_plan", "")).strip():
        reasons.append("missing_rollback")
    if not str(proposal.get("validation_plan", "")).strip():
        reasons.append("missing_validation")
    if not proposal.get("affected_components") and not proposal.get("observed_problem_refs"):
        reasons.append("missing_grounded_scope")
    # Lazy import avoids the existing SELF_EXPANSION_GATE -> PROPOSAL_AUDIT
    # package initialization cycle.
    from MAKSIMAR_SERVER.SELF_EXPANSION_GATE.self_expansion_gate import build_self_expansion_gate
    gate = build_self_expansion_gate()
    if not gate.get("gate_ready"):
        reasons.append("self_expansion_gate_not_ready")
    if "production_mutation_requested" in reasons:
        verdict = "REJECTED"
    elif reasons:
        verdict = "REVISE"
    else:
        verdict = "ACCEPTED_FOR_EXPERIMENT"
    return ProposalAuditResult(
        proposal_id=proposal_id,
        verdict=verdict,
        reasons=tuple(dict.fromkeys(reasons)),
        sandbox_required=True,
        production_mutation_allowed=False,
        gate_ready=bool(gate.get("gate_ready")),
    )
