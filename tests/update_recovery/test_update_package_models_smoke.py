from __future__ import annotations

import pytest

from MAKSIMAR_CORE_LIB.update_recovery.update_package_models import (
    UpdatePackageArtifactKind,
    UpdatePackageArtifactRef,
    UpdatePackageManifest,
    UpdatePackageSignatureAlgorithm,
    UpdatePackageSignatureEnvelope,
    compute_update_package_payload_sha256,
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


def _payload_hash() -> str:
    return compute_update_package_payload_sha256(
        package_id="update-package-001",
        package_version="1.0.0",
        target_layer_id="UPDATE_RECOVERY_INFRA",
        created_at_utc="2026-01-01T00:00:00Z",
        artifacts=(_artifact(),),
        requires_snapshot=True,
        rollback_ref="rollback://update-package-001",
    )


def test_update_package_manifest_validates_canonical_payload_hash() -> None:
    package_hash = _payload_hash()
    signature = UpdatePackageSignatureEnvelope(
        signature_id="signature-001",
        signer_id="owner-root-key",
        algorithm=UpdatePackageSignatureAlgorithm.ED25519,
        public_key_ref="vault://keys/owner-root-key",
        signature_ref="signature://update-package-001",
        signature_sha256=TWO,
        signed_payload_sha256=package_hash,
    )

    manifest = UpdatePackageManifest(
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

    assert manifest.is_signed is True
    assert manifest.direct_apply_allowed is False
    assert manifest.dashboard_execution_allowed is False
    assert manifest.canonical_write_allowed is False
    assert manifest.to_dict()["signature"]["signer_id"] == "owner-root-key"


def test_update_package_manifest_can_represent_unsigned_update_for_rejection() -> None:
    manifest = UpdatePackageManifest(
        package_id="update-package-001",
        package_version="1.0.0",
        target_layer_id="UPDATE_RECOVERY_INFRA",
        created_at_utc="2026-01-01T00:00:00Z",
        artifacts=(_artifact(),),
        package_sha256=_payload_hash(),
        signature=None,
        requires_snapshot=True,
        rollback_ref="rollback://update-package-001",
    )

    assert manifest.is_signed is False
    assert manifest.signed_update_required is True


def test_update_package_manifest_rejects_hash_mismatch() -> None:
    with pytest.raises(ValueError, match="package_sha256"):
        UpdatePackageManifest(
            package_id="update-package-001",
            package_version="1.0.0",
            target_layer_id="UPDATE_RECOVERY_INFRA",
            created_at_utc="2026-01-01T00:00:00Z",
            artifacts=(_artifact(),),
            package_sha256=TWO,
            signature=None,
            requires_snapshot=True,
            rollback_ref="rollback://update-package-001",
        )
