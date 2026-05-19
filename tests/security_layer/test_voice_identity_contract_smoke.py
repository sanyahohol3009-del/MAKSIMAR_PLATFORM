from __future__ import annotations

from MAKSIMAR_CORE_LIB.security_layer.voice_identity_contract import (
    VoiceIdentityClaim,
    VoiceIdentityStatus,
    verify_voice_identity,
)


def test_voice_identity_verified_when_threshold_met() -> None:
    claim = VoiceIdentityClaim(
        subject_id="owner",
        voiceprint_id="vp_001",
        confidence=0.91,
        threshold=0.85,
        sample_present=True,
    )

    result = verify_voice_identity(claim)

    assert result.status is VoiceIdentityStatus.VERIFIED
    assert result.verified is True


def test_voice_identity_blocks_missing_sample() -> None:
    claim = VoiceIdentityClaim(
        subject_id="owner",
        voiceprint_id="",
        confidence=0.0,
        threshold=0.85,
        sample_present=False,
    )

    result = verify_voice_identity(claim)

    assert result.status is VoiceIdentityStatus.MISSING_SAMPLE
    assert result.verified is False
