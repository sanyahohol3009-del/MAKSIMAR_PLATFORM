from __future__ import annotations

from dataclasses import dataclass
from enum import Enum


class UsbGuardStatus(str, Enum):
    ALLOWED = "allowed"
    BLOCKED = "blocked"


@dataclass(frozen=True, slots=True)
class UsbDeviceDescriptor:
    device_id: str
    vendor_id: str
    product_id: str
    device_class: str
    serial_hash: str

    def __post_init__(self) -> None:
        for field_name, value in (
            ("device_id", self.device_id),
            ("vendor_id", self.vendor_id),
            ("product_id", self.product_id),
            ("device_class", self.device_class),
            ("serial_hash", self.serial_hash),
        ):
            if not value:
                raise ValueError(f"{field_name} must not be empty")


@dataclass(frozen=True, slots=True)
class UsbGuardDecision:
    device_id: str
    status: UsbGuardStatus
    reason_codes: tuple[str, ...]
    dashboard_safe: bool = True
    runtime_mutation_allowed: bool = False
    canonical_write_allowed: bool = False

    def __post_init__(self) -> None:
        if not self.device_id:
            raise ValueError("device_id must not be empty")
        if not isinstance(self.status, UsbGuardStatus):
            raise TypeError("status must be UsbGuardStatus")
        if not self.reason_codes:
            raise ValueError("reason_codes must not be empty")
        if not self.dashboard_safe:
            raise ValueError("dashboard_safe must remain true")
        if self.runtime_mutation_allowed:
            raise ValueError("runtime_mutation_allowed must remain false")
        if self.canonical_write_allowed:
            raise ValueError("canonical_write_allowed must remain false")


def evaluate_usb_device(
    device: UsbDeviceDescriptor,
    *,
    allowed_serial_hashes: tuple[str, ...],
) -> UsbGuardDecision:
    if device.serial_hash not in allowed_serial_hashes:
        return UsbGuardDecision(
            device_id=device.device_id,
            status=UsbGuardStatus.BLOCKED,
            reason_codes=("usb_device_not_allowlisted",),
        )

    return UsbGuardDecision(
        device_id=device.device_id,
        status=UsbGuardStatus.ALLOWED,
        reason_codes=("usb_device_allowlisted",),
    )
