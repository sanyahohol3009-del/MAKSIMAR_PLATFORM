import pytest

from MAKSIMAR_SERVER.VOICE_ROUTING.jarvis_live_owner_identity_runtime_contract import (
    JarvisLiveOwnerIdentityRuntimeContract,
    build_jarvis_live_owner_identity_runtime_contract,
)


def test_owner_identity_runtime_contract_is_keyword_session_awareness_only() -> None:
    model = build_jarvis_live_owner_identity_runtime_contract().to_read_model()

    assert model["owner_display_name"] == "Александр"
    assert model["owner_detection_keywords"] == ("александр", "джарвис", "jarvis")
    assert model["owner_phrase_detection_required"] is True
    assert model["owner_visible_state_required"] is True
    assert model["unknown_speaker_no_action_required"] is True
    assert model["owner_command_required_before_actions"] is True
    assert model["biometric_auth_claimed"] is False
    assert model["speaker_verification_claimed"] is False
    assert model["unknown_speaker_action_allowed"] is False
    assert model["pc_control_allowed"] is False


def test_owner_identity_runtime_contract_rejects_false_identity_claims() -> None:
    with pytest.raises(ValueError):
        JarvisLiveOwnerIdentityRuntimeContract(biometric_auth_claimed=True)
    with pytest.raises(ValueError):
        JarvisLiveOwnerIdentityRuntimeContract(speaker_verification_claimed=True)
    with pytest.raises(ValueError):
        JarvisLiveOwnerIdentityRuntimeContract(unknown_speaker_action_allowed=True)
