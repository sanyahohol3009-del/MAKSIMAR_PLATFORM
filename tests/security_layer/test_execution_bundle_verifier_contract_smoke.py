from __future__ import annotations

from MAKSIMAR_CORE_LIB.security_layer.execution_bundle_verifier_contract import (
    ExecutionBundle,
    ExecutionBundleVerificationStatus,
    verify_execution_bundle,
)
from MAKSIMAR_CORE_LIB.security_layer.signature_verifier_contract import (
    SignatureVerificationRequest,
    verify_generic_signature,
)


def test_execution_bundle_ready_when_signature_approval_and_voice_are_valid() -> None:
    signature = verify_generic_signature(
        SignatureVerificationRequest(
            subject_id="owner",
            artifact_id="bundle_001",
            payload_hash="hash_001",
            signature="sig_ok",
            algorithm="ed25519",
            trust_domain="security_layer",
        ),
        trusted_signature="sig_ok",
    )
    bundle = ExecutionBundle(
        bundle_id="bundle_001",
        request_id="sec_req_bundle_001",
        trace_id="trace_bundle_001",
        command_kind="execute",
        target_layer_id="CORE_ROOT",
        signature_result=signature,
        approval_present=True,
        voice_identity_verified=True,
        high_risk=True,
    )

    result = verify_execution_bundle(bundle)

    assert result.status is ExecutionBundleVerificationStatus.READY
    assert result.ready_for_execution is True


def test_execution_bundle_blocks_missing_voice_for_high_risk() -> None:
    signature = verify_generic_signature(
        SignatureVerificationRequest(
            subject_id="owner",
            artifact_id="bundle_002",
            payload_hash="hash_002",
            signature="sig_ok",
            algorithm="ed25519",
            trust_domain="security_layer",
        ),
        trusted_signature="sig_ok",
    )
    bundle = ExecutionBundle(
        bundle_id="bundle_002",
        request_id="sec_req_bundle_002",
        trace_id="trace_bundle_002",
        command_kind="execute",
        target_layer_id="CORE_ROOT",
        signature_result=signature,
        approval_present=True,
        voice_identity_verified=False,
        high_risk=True,
    )

    result = verify_execution_bundle(bundle)

    assert result.status is ExecutionBundleVerificationStatus.BLOCKED
    assert "voice_identity_missing_for_high_risk" in result.reason_codes
