from __future__ import annotations

from MAKSIMAR_CORE_LIB.security_layer.media_quarantine_contract import (
    MediaArtifactScan,
    MediaQuarantineStatus,
    evaluate_media_quarantine,
)
from MAKSIMAR_CORE_LIB.security_layer.usb_guard_contract import (
    UsbDeviceDescriptor,
    UsbGuardStatus,
    evaluate_usb_device,
)
from MAKSIMAR_CORE_LIB.security_layer.vault_boundary_contract import (
    VaultAccessRequest,
    VaultAccessStatus,
    evaluate_vault_access,
)


def test_vault_boundary_never_exposes_secret_material() -> None:
    decision = evaluate_vault_access(
        VaultAccessRequest(
            request_id="vault_req_001",
            subject_id="operator",
            secret_ref="service/api_key",
            purpose="metadata check",
            approval_present=True,
        )
    )

    assert decision.status is VaultAccessStatus.ALLOWED
    assert decision.secret_material_exposed is False


def test_usb_guard_blocks_unknown_device() -> None:
    decision = evaluate_usb_device(
        UsbDeviceDescriptor(
            device_id="usb_001",
            vendor_id="v",
            product_id="p",
            device_class="mass_storage",
            serial_hash="unknown",
        ),
        allowed_serial_hashes=("trusted",),
    )

    assert decision.status is UsbGuardStatus.BLOCKED


def test_media_quarantine_blocks_threat_labels() -> None:
    decision = evaluate_media_quarantine(
        MediaArtifactScan(
            artifact_id="media_001",
            content_hash="hash",
            media_type="application/octet-stream",
            scanner_ids=("scanner",),
            threat_labels=("suspicious_payload",),
        )
    )

    assert decision.status is MediaQuarantineStatus.QUARANTINED
