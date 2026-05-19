from __future__ import annotations

import pytest

from MAKSIMAR_CORE_LIB.update_recovery.signed_update_service_contract import (
    SignedUpdateServiceRequest,
    evaluate_signed_update_service,
)
from MAKSIMAR_CORE_LIB.update_recovery.update_package_models import (
    UpdatePackageArtifactKind,
    UpdatePackageArtifactRef,
    UpdatePackageManifest,
    UpdatePackageSignatureAlgorithm,
    UpdatePackageSignatureEnvelope,
    compute_update_package_payload_sha256,
)
from MAKSIMAR_CORE_LIB.update_recovery.update_recovery_policy import (
    UpdateRecoveryPolicy,
    build_default_update_recovery_policy,
    evaluate_update_recovery_policy,
)
from MAKSIMAR_CORE_LIB.update_recovery.update_signature_verifier_contract import (
    UpdateSignatureVerificationRequest,
)

ONE = "1" * 64
TWO = "2" * 64


def _artifact() -> UpdatePackageArtifactRef:
    return UpdatePackageArtifactRef(
        artifact_id="update-artifact-001",
        artifact_kind=UpdatePackageArtifactKind.CODE_BUNDLE,
        artifact_uri="artifact://updates/code/update-artifact-001",
        artifact_sha256=ONE,
        size_bytes=1024,
        content_type="application/vnd.maksimar.update.code+json",
    )


def _manifest(*, signed: bool) -> UpdatePackageManifest:
    package_hash = compute_update_package_payload_sha256(
        package_id="update-package-001",
        package_version="1.0.0",
        target_layer_id="UPDATE_RECOVERY_INFRA",
        created_at_utc="2026-01-01T00:00:00Z",
        artifacts=(_artifact(),),
        requires_snapshot=True,
        rollback_ref="rollback://update-package-001",
    )
    signature = None
    if signed:
        signature = UpdatePackageSignatureEnvelope(
            signature_id="signature-001",
            signer_id="owner-root-key",
            algorithm=UpdatePackageSignatureAlgorithm.ED25519,
            public_key_ref="vault://keys/owner-root-key",
            signature_ref="signature://update-package-001",
            signature_sha256=TWO,
            signed_payload_sha256=package_hash,
        )
    return UpdatePackageManifest(
        package_id="update-package-001",
        package_version="1.0.0",
        target_layer_id="UPDATE_RECOVERY_INFRA",
        created_at_utc="2026-01-01T00:00:00Z",
        artifacts=(_artifact(),),
        package_sha256=package_hash,
        signature=signature,
        requires_snapshot=True,
        rollback_ref="rollback://update-package-001",
    )


def _service_decision(*, signed: bool):
    verification_request = UpdateSignatureVerificationRequest(
        request_id="verify-update-package-001",
        package_manifest=_manifest(signed=signed),
        trusted_signer_ids=("owner-root-key",),
        allowed_algorithms=(UpdatePackageSignatureAlgorithm.ED25519,),
        required_target_layer_ids=("UPDATE_RECOVERY_INFRA",),
    )
    service_request = SignedUpdateServiceRequest(
        service_request_id="signed-update-service-001",
        signature_verification_request=verification_request,
    )
    return evaluate_signed_update_service(service_request)


def test_update_recovery_policy_accepts_signed_update_for_next_gate_only() -> None:
    policy = build_default_update_recovery_policy()
    decision = evaluate_update_recovery_policy(
        policy=policy,
        signed_update_service_decision=_service_decision(signed=True),
    )

    assert decision.policy_accepted_for_next_gate is True
    assert decision.update_signature_required is True
    assert decision.unsigned_update_allowed is False
    assert decision.snapshot_required_before_apply is True
    assert decision.update_package_apply_allowed is False
    assert decision.security_layer_signature_replacement_allowed is False
    assert decision.dashboard_execution_allowed is False


def test_update_recovery_policy_rejects_unsigned_update() -> None:
    policy = build_default_update_recovery_policy()
    decision = evaluate_update_recovery_policy(
        policy=policy,
        signed_update_service_decision=_service_decision(signed=False),
    )

    assert decision.policy_accepted_for_next_gate is False
    assert decision.unsigned_update_allowed is False
    assert "unsigned_update_rejected" in decision.reason_codes


def test_update_recovery_policy_rejects_security_signature_replacement() -> None:
    with pytest.raises(ValueError, match="security_layer_signature_replacement_allowed"):
        UpdateRecoveryPolicy(
            policy_id="update_recovery_policy_v1",
            update_signature_required=True,
            unsigned_update_allowed=False,
            snapshot_required_before_apply=True,
            direct_apply_allowed=False,
            canonical_write_allowed=False,
            dashboard_execution_allowed=False,
            security_layer_signature_replacement_allowed=True,
            reason_codes=("bad",),
        )
