from __future__ import annotations

from tools.jarvis_live_runtime.owner_identity_claim import (
    build_owner_identity_claim_for_terminal,
    build_owner_identity_claim_for_voice_unverified,
)


def test_terminal_identity_claim_uses_os_user_fact() -> None:
    claim = build_owner_identity_claim_for_terminal()
    payload = claim.to_read_model()

    assert payload["claim_id"] == "terminal_session_claim_v1"
    assert payload["source"] == "local_terminal_session"
    assert payload["verification_method"] == "os_user_match"
    assert isinstance(payload["verified"], bool)
    assert "reason_codes" in payload


def test_voice_identity_claim_is_unverified_until_biometrics_exist() -> None:
    claim = build_owner_identity_claim_for_voice_unverified()
    payload = claim.to_read_model()

    assert payload["source"] == "voice_unverified"
    assert payload["verified"] is False
    assert payload["verification_method"] == "none_voice_biometric_not_implemented"
    assert "voice_cannot_authorize_direct_action" in payload["reason_codes"]
