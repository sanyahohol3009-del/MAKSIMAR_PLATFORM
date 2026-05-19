from __future__ import annotations

from MAKSIMAR_CORE_LIB.update_recovery.signed_update_service_contract import (
    SignedUpdateServiceRequest,
    SignedUpdateServiceStatus,
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


def _service_request(manifest: UpdatePackageManifest) -> SignedUpdateServiceRequest:
    verification_request = UpdateSignatureVerificationRequest(
        request_id="verify-update-package-001",
        package_manifest=manifest,
        trusted_signer_ids=("owner-root-key",),
        allowed_algorithms=(UpdatePackageSignatureAlgorithm.ED25519,),
        required_target_layer_ids=("UPDATE_RECOVERY_INFRA",),
    )
    return SignedUpdateServiceRequest(
        service_request_id="signed-update-service-001",
        signature_verification_request=verification_request,
    )


def test_signed_update_service_accepts_verified_package_for_policy_gate_only() -> None:
    decision = evaluate_signed_update_service(_service_request(_manifest(signed=True)))

    assert decision.service_status is SignedUpdateServiceStatus.SIGNED_UPDATE_READY_FOR_POLICY
    assert decision.signed_update_accepted is True
    assert decision.update_package_apply_allowed is False
    assert decision.snapshot_required_before_apply is True
    assert decision.direct_apply_allowed is False
    assert decision.dashboard_execution_allowed is False


def test_signed_update_service_rejects_unsigned_package() -> None:
    decision = evaluate_signed_update_service(_service_request(_manifest(signed=False)))

    assert decision.service_status is SignedUpdateServiceStatus.SIGNED_UPDATE_REJECTED_BY_SIGNATURE_GATE
    assert decision.signed_update_accepted is False
    assert decision.update_package_apply_allowed is False
    assert "unsigned_update_rejected" in decision.reason_codes
