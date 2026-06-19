from __future__ import annotations

from MAKSIMAR_CORE_LIB.action_library_adapters.computer_use_worker_contract import (
    build_action_request_from_intent,
)
from MAKSIMAR_SERVER.WORKERS.action_recording_runtime import build_action_recording
from tools.jarvis_live_runtime.owner_identity_claim import OwnerIdentityClaim


def test_action_recording_required_smoke() -> None:
    request = build_action_request_from_intent(
        "open browser",
        input_channel="text",
        owner_identity_claim=OwnerIdentityClaim(
            claim_id="action_recording_owner_v1",
            source="local_terminal_session",
            verified=True,
            verification_method="test_override",
            session_token_present=False,
            process_owner_matches_os_user=True,
            reason_codes=("os_user_verified",),
        ),
    )
    assert request is not None
    recording = build_action_recording(request).to_read_model()

    assert recording["recording_required"] is True
    assert "validate_owner_identity" in recording["recorded_steps"]
