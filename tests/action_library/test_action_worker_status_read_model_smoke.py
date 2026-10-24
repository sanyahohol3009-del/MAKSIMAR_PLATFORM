from __future__ import annotations

from MAKSIMAR_CORE_LIB.action_library_adapters.action_worker_status_read_model import (
    build_action_worker_status_read_model,
)
from MAKSIMAR_CORE_LIB.action_library_adapters.computer_use_worker_contract import (
    resolve_computer_use_action_request,
)
from MAKSIMAR_CORE_LIB.ai_orchestration.semantic_intent_contract import PlanStep
from MAKSIMAR_SERVER.WORKERS.sandboxed_action_worker_runtime import run_sandboxed_action_worker
from MAKSIMAR_CORE_LIB.security_layer.owner_identity_claim import OwnerIdentityClaim


def test_action_worker_status_read_model_smoke() -> None:
    request = resolve_computer_use_action_request(
        PlanStep("step", "goal", "pc.control", "open_browser", ("execution_receipt",), "MUTATE", "local_pc", "REVERSIBLE", True, "MUTATION"),
        target="default_browser",
        input_channel="text",
        owner_identity_claim=OwnerIdentityClaim(
            claim_id="action_status_owner_v1",
            source="local_terminal_session",
            verified=True,
            verification_method="test_override",
            session_token_present=False,
            process_owner_matches_os_user=True,
            reason_codes=("os_user_verified",),
        ),
    )
    assert request is not None
    read_model = build_action_worker_status_read_model(run_sandboxed_action_worker(request)).to_read_model()

    assert read_model["capability_id"] == "browser_worker"
    assert read_model["safe_direct_allowed"] is True
    assert read_model["direct_execution_by_swarm"] is False
