from __future__ import annotations

from MAKSIMAR_CORE_LIB.action_library_adapters.computer_use_worker_contract import (
    resolve_computer_use_action_request,
)
from MAKSIMAR_CORE_LIB.ai_orchestration.semantic_intent_contract import PlanStep
from MAKSIMAR_SERVER.WORKERS.sandboxed_action_worker_runtime import run_sandboxed_action_worker
from MAKSIMAR_CORE_LIB.security_layer.owner_identity_claim import OwnerIdentityClaim


def test_action_requires_approval_smoke() -> None:
    request = resolve_computer_use_action_request(
        PlanStep("step", "goal", "pc.control", "mutating_shell_request", ("execution_receipt",), "MUTATE", "repository", "REVERSIBLE", True, "DANGEROUS"),
        target="origin/main",
        input_channel="text",
        owner_identity_claim=OwnerIdentityClaim(
            claim_id="action_approval_owner_v1",
            source="local_terminal_session",
            verified=True,
            verification_method="test_override",
            session_token_present=False,
            process_owner_matches_os_user=True,
            reason_codes=("os_user_verified",),
        ),
    )
    assert request is not None
    decision = run_sandboxed_action_worker(request).to_read_model()

    assert decision["direct_execution_allowed"] is False
    assert decision["risk_gate_required"] is True
    assert decision["executed"] is False
