from __future__ import annotations

from MAKSIMAR_CORE_LIB.update_recovery.update_package_models import (
    UpdatePackageArtifactKind,
    UpdatePackageArtifactRef,
    UpdatePackageManifest,
    UpdatePackageSignatureAlgorithm,
    UpdatePackageSignatureEnvelope,
    compute_update_package_payload_sha256,
)
from MAKSIMAR_CORE_LIB.update_recovery.update_signature_verifier_contract import (
    UpdateSignatureDecisionStatus,
    UpdateSignatureVerificationRequest,
    verify_update_package_signature,
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


def _package_hash() -> str:
    return compute_update_package_payload_sha256(
        package_id="update-package-001",
        package_version="1.0.0",
        target_layer_id="UPDATE_RECOVERY_INFRA",
        created_at_utc="2026-01-01T00:00:00Z",
        artifacts=(_artifact(),),
        requires_snapshot=True,
        rollback_ref="rollback://update-package-001",
    )


def _manifest(*, signer_id: str = "owner-root-key", signed: bool = True) -> UpdatePackageManifest:
    package_hash = _package_hash()
    signature = None
    if signed:
        signature = UpdatePackageSignatureEnvelope(
            signature_id="signature-001",
            signer_id=signer_id,
            algorithm=UpdatePackageSignatureAlgorithm.ED25519,
            public_key_ref=f"vault://keys/{signer_id}",
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


def _request(manifest: UpdatePackageManifest) -> UpdateSignatureVerificationRequest:
    return UpdateSignatureVerificationRequest(
        request_id="verify-update-package-001",
        package_manifest=manifest,
        trusted_signer_ids=("owner-root-key",),
        allowed_algorithms=(UpdatePackageSignatureAlgorithm.ED25519,),
        required_target_layer_ids=("UPDATE_RECOVERY_INFRA",),
    )


def test_update_signature_verifier_accepts_trusted_signed_update() -> None:
    decision = verify_update_package_signature(_request(_manifest()))

    assert decision.status is UpdateSignatureDecisionStatus.ACCEPTED
    assert decision.signature_verified is True
    assert decision.signer_trusted is True
    assert decision.algorithm_allowed is True
    assert decision.target_layer_allowed is True
    assert decision.package_hash_valid is True
    assert decision.direct_apply_allowed is False


def test_update_signature_verifier_rejects_unsigned_update() -> None:
    decision = verify_update_package_signature(_request(_manifest(signed=False)))

    assert decision.status is UpdateSignatureDecisionStatus.REJECTED
    assert decision.signature_verified is False
    assert decision.unsigned_update_rejected is True
    assert "unsigned_update_rejected" in decision.reason_codes


def test_update_signature_verifier_rejects_untrusted_signer() -> None:
    decision = verify_update_package_signature(_request(_manifest(signer_id="unknown-key")))

    assert decision.status is UpdateSignatureDecisionStatus.REJECTED
    assert decision.signature_verified is False
    assert decision.signer_trusted is False
    assert "untrusted_update_signer" in decision.reason_codes
