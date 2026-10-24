from __future__ import annotations

from MAKSIMAR_CORE_LIB.action_library_adapters.computer_use_worker_contract import (
    resolve_computer_use_action_request,
)
from MAKSIMAR_CORE_LIB.ai_orchestration.semantic_intent_contract import PlanStep
from MAKSIMAR_CORE_LIB.security_layer.owner_identity_claim import (
    OwnerIdentityClaim,
)


def _verified_terminal_claim() -> OwnerIdentityClaim:
    return OwnerIdentityClaim(
        claim_id="tool_semantic_verified_terminal_v1",
        source="local_terminal_session",
        verified=True,
        verification_method="test_override",
        session_token_present=False,
        process_owner_matches_os_user=True,
        reason_codes=("os_user_verified",),
    )


def _step(operation: str, risk_class: str = "MUTATION") -> PlanStep:
    return PlanStep("step", "goal", "pc.control", operation, ("execution_receipt",),
                    "MUTATE", "local_pc", "REVERSIBLE", True, risk_class)


def test_typed_plan_step_resolves_computer_use_worker_contract() -> None:
    browser_request = resolve_computer_use_action_request(
        _step("open_browser"), target="default_browser",
        input_channel="text",
        owner_identity_claim=_verified_terminal_claim(),
    )
    risk_request = resolve_computer_use_action_request(
        _step("mutating_shell_request", "DANGEROUS"), target="repository",
        input_channel="text",
        owner_identity_claim=_verified_terminal_claim(),
    )

    assert browser_request is not None
    assert browser_request.capability_id == "browser_worker"
    assert browser_request.action_name == "open_browser"
    assert risk_request is not None
    assert risk_request.capability_id == "cli_worker"
