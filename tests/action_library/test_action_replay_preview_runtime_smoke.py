from __future__ import annotations

from MAKSIMAR_CORE_LIB.action_library_adapters.computer_use_worker_contract import (
    resolve_computer_use_action_request,
)
from MAKSIMAR_CORE_LIB.ai_orchestration.semantic_intent_contract import PlanStep
from MAKSIMAR_SERVER.WORKERS.action_recording_runtime import build_action_recording
from MAKSIMAR_SERVER.WORKERS.action_replay_preview_runtime import build_action_replay_preview
from MAKSIMAR_CORE_LIB.security_layer.owner_identity_claim import OwnerIdentityClaim


def test_action_replay_preview_runtime_smoke() -> None:
    request = resolve_computer_use_action_request(
        PlanStep("step", "goal", "pc.control", "open_browser", ("execution_receipt",), "MUTATE", "local_pc", "REVERSIBLE", True, "MUTATION"),
        target="default_browser",
        input_channel="text",
        owner_identity_claim=OwnerIdentityClaim(
            claim_id="action_replay_owner_v1",
            source="local_terminal_session",
            verified=True,
            verification_method="test_override",
            session_token_present=False,
            process_owner_matches_os_user=True,
            reason_codes=("os_user_verified",),
        ),
    )
    assert request is not None
    preview = build_action_replay_preview(build_action_recording(request)).to_read_model()

    assert preview["replay_preview_required"] is True
    assert preview["preview_steps"][-1] == "await_operator_or_env_execution"
