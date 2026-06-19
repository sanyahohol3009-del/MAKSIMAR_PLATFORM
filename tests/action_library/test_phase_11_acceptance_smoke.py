from __future__ import annotations

from pathlib import Path

from MAKSIMAR_CORE_LIB.action_library_adapters.computer_use_worker_contract import (
    build_action_request_from_intent,
)
from MAKSIMAR_SERVER.WORKERS.sandboxed_action_worker_runtime import run_sandboxed_action_worker
from tools.jarvis_live_runtime.owner_identity_claim import (
    OwnerIdentityClaim,
    build_owner_identity_claim_for_voice_unverified,
)


def _verified_terminal_claim() -> OwnerIdentityClaim:
    return OwnerIdentityClaim(
        claim_id="phase11_verified_terminal_claim_v1",
        source="local_terminal_session",
        verified=True,
        verification_method="test_override",
        session_token_present=False,
        process_owner_matches_os_user=True,
        reason_codes=("os_user_verified",),
    )


def test_phase_11_acceptance_smoke(monkeypatch) -> None:
    monkeypatch.delenv("JARVIS_LOCAL_SAFE_ACTION_EXECUTION", raising=False)
    assert Path("docs/architecture/action_library/phase_11_action_library_acceptance_v1.md").exists()

    browser_request = build_action_request_from_intent(
        "open browser",
        input_channel="text",
        owner_identity_claim=_verified_terminal_claim(),
    )
    voice_request = build_action_request_from_intent(
        "open browser",
        input_channel="voice",
        owner_identity_claim=build_owner_identity_claim_for_voice_unverified(),
    )
    risk_request = build_action_request_from_intent(
        "sudo rm -rf /tmp/demo",
        input_channel="text",
        owner_identity_claim=_verified_terminal_claim(),
    )
    assert browser_request is not None
    assert voice_request is not None
    assert risk_request is not None

    browser = run_sandboxed_action_worker(browser_request).to_read_model()
    voice = run_sandboxed_action_worker(voice_request).to_read_model()
    risk = run_sandboxed_action_worker(risk_request).to_read_model()

    assert browser_request.capability_id == "browser_worker"
    assert browser["direct_execution_allowed"] is True
    assert browser["would_execute"] is True
    assert voice["direct_execution_allowed"] is False
    assert voice["denial_reason"] == "voice_unverified_cannot_execute_directly"
    assert risk["risk_gate_required"] is True
    assert risk["executed"] is False
    assert browser["recording"]["recording_required"] is True
    assert browser["replay_preview"]["replay_preview_required"] is True
