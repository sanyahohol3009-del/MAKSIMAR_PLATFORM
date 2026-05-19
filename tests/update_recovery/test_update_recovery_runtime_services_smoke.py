from __future__ import annotations

from MAKSIMAR_CORE_LIB.update_recovery.offline_import_gate_contract import OfflineImportCandidate
from MAKSIMAR_CORE_LIB.update_recovery.rollback_manager_contract import RollbackPlanReference
from MAKSIMAR_CORE_LIB.update_recovery.signed_update_service_contract import SignedUpdateServiceRequest
from MAKSIMAR_CORE_LIB.update_recovery.snapshot_manager_contract import SnapshotReference
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
from MAKSIMAR_SERVER.UPDATE_RECOVERY.offline_import_gate import run_offline_import_gate
from MAKSIMAR_SERVER.UPDATE_RECOVERY.recovery_service import run_recovery_service_ready
from MAKSIMAR_SERVER.UPDATE_RECOVERY.rollback_manager import run_rollback_manager_ready
from MAKSIMAR_SERVER.UPDATE_RECOVERY.signed_update_service import run_signed_update_service
from MAKSIMAR_SERVER.UPDATE_RECOVERY.snapshot_manager import run_snapshot_manager_ready
from MAKSIMAR_SERVER.UPDATE_RECOVERY.update_signature_verifier import run_update_signature_verifier

ONE = "1" * 64
TWO = "2" * 64
THREE = "3" * 64


def _artifact() -> UpdatePackageArtifactRef:
    return UpdatePackageArtifactRef(
        artifact_id="update-artifact-runtime-001",
        artifact_kind=UpdatePackageArtifactKind.CODE_BUNDLE,
        artifact_uri="artifact://updates/runtime/update-artifact-runtime-001",
        artifact_sha256=ONE,
        size_bytes=1024,
        content_type="application/vnd.maksimar.update.code+json",
    )


def _manifest() -> UpdatePackageManifest:
    package_hash = compute_update_package_payload_sha256(
        package_id="update-package-runtime-001",
        package_version="1.0.0",
        target_layer_id="UPDATE_RECOVERY_INFRA",
        created_at_utc="2026-01-01T00:00:00Z",
        artifacts=(_artifact(),),
        requires_snapshot=True,
        rollback_ref="rollback://update-package-runtime-001",
    )
    signature = UpdatePackageSignatureEnvelope(
        signature_id="signature-runtime-001",
        signer_id="owner-root-key",
        algorithm=UpdatePackageSignatureAlgorithm.ED25519,
        public_key_ref="vault://keys/owner-root-key",
        signature_ref="signature://update-package-runtime-001",
        signature_sha256=TWO,
        signed_payload_sha256=package_hash,
    )
    return UpdatePackageManifest(
        package_id="update-package-runtime-001",
        package_version="1.0.0",
        target_layer_id="UPDATE_RECOVERY_INFRA",
        created_at_utc="2026-01-01T00:00:00Z",
        artifacts=(_artifact(),),
        package_sha256=package_hash,
        signature=signature,
        requires_snapshot=True,
        rollback_ref="rollback://update-package-runtime-001",
    )


def _signature_request() -> UpdateSignatureVerificationRequest:
    return UpdateSignatureVerificationRequest(
        request_id="verify-runtime-001",
        package_manifest=_manifest(),
        trusted_signer_ids=("owner-root-key",),
        allowed_algorithms=(UpdatePackageSignatureAlgorithm.ED25519,),
        required_target_layer_ids=("UPDATE_RECOVERY_INFRA",),
    )


def test_update_signature_and_signed_update_runtime_wrappers_do_not_apply_update() -> None:
    signature_runtime = run_update_signature_verifier(_signature_request())

    assert signature_runtime.wrapper_only is True
    assert signature_runtime.decision.signature_verified is True
    assert signature_runtime.runtime_apply_allowed is False
    assert signature_runtime.canonical_write_allowed is False
    assert signature_runtime.dashboard_execution_allowed is False

    signed_runtime = run_signed_update_service(
        SignedUpdateServiceRequest(
            service_request_id="signed-runtime-001",
            signature_verification_request=_signature_request(),
        )
    )

    assert signed_runtime.wrapper_only is True
    assert signed_runtime.decision.signed_update_accepted is True
    assert signed_runtime.decision.update_package_apply_allowed is False
    assert signed_runtime.runtime_apply_allowed is False
    assert signed_runtime.canonical_write_allowed is False
    assert signed_runtime.dashboard_execution_allowed is False


def test_snapshot_rollback_recovery_offline_runtime_wrappers_do_not_apply_update() -> None:
    package_id = "update-package-runtime-001"
    snapshot_runtime = run_snapshot_manager_ready(
        package_id=package_id,
        snapshot_reference=SnapshotReference(
            snapshot_id="snapshot-runtime-001",
            snapshot_uri="snapshot://runtime/snapshot-runtime-001",
            snapshot_sha256=ONE,
            created_at_utc="2026-01-01T00:00:00Z",
            immutable=True,
            state_manifest_present=True,
            rollback_compatible=True,
        ),
    )
    rollback_runtime = run_rollback_manager_ready(
        package_id=package_id,
        rollback_plan_reference=RollbackPlanReference(
            rollback_plan_id="rollback-runtime-001",
            rollback_uri="rollback://runtime/rollback-runtime-001",
            rollback_sha256=THREE,
            target_snapshot_id="snapshot-runtime-001",
            tested=True,
            reversible=True,
        ),
        snapshot_readiness=snapshot_runtime.read_model,
    )
    recovery_runtime = run_recovery_service_ready(
        package_id=package_id,
        snapshot_readiness=snapshot_runtime.read_model,
        rollback_readiness=rollback_runtime.read_model,
    )
    offline_runtime = run_offline_import_gate(
        OfflineImportCandidate(
            import_id="offline-runtime-001",
            package_id=package_id,
            source_uri="offline-media://runtime/update-package-runtime-001",
            package_sha256=ONE,
            created_at_utc="2026-01-01T00:00:00Z",
            signature_present=True,
            air_gap_transfer_confirmed=True,
            media_quarantined=True,
            operator_approval_present=True,
        )
    )

    for result in (snapshot_runtime, rollback_runtime, recovery_runtime, offline_runtime):
        assert result.wrapper_only is True
        assert result.runtime_apply_allowed is False
        assert result.canonical_write_allowed is False
        assert result.dashboard_execution_allowed is False

    assert snapshot_runtime.read_model.snapshot_ready is True
    assert rollback_runtime.read_model.rollback_ready is True
    assert recovery_runtime.read_model.recovery_ready is True
    assert offline_runtime.decision.offline_import_allowed_for_verification is True
