from __future__ import annotations

import pytest

from MAKSIMAR_CORE_LIB.security_layer.signature_verifier_contract import (
    SignatureVerificationRequest,
    SignatureVerificationStatus,
    verify_generic_signature,
)


def test_generic_signature_verifier_accepts_trusted_signature() -> None:
    request = SignatureVerificationRequest(
        subject_id="service",
        artifact_id="artifact_001",
        payload_hash="hash_001",
        signature="sig_ok",
        algorithm="ed25519",
        trust_domain="security_layer",
    )

    result = verify_generic_signature(request, trusted_signature="sig_ok")

    assert result.status is SignatureVerificationStatus.VALID
    assert result.verified is True
    assert result.update_package_specific is False


def test_signature_verifier_is_not_update_package_specific() -> None:
    request = SignatureVerificationRequest(
        subject_id="service",
        artifact_id="artifact_002",
        payload_hash="hash_002",
        signature="bad",
        algorithm="ed25519",
        trust_domain="security_layer",
    )

    result = verify_generic_signature(request, trusted_signature="sig_ok")

    assert result.status is SignatureVerificationStatus.INVALID
    assert result.verified is False

    with pytest.raises(ValueError, match="generic"):
        type(result)(
            status=SignatureVerificationStatus.VALID,
            artifact_id="artifact_003",
            reason_codes=("signature_valid",),
            trust_boundary="security_layer",
            verified=True,
            update_package_specific=True,
        )
