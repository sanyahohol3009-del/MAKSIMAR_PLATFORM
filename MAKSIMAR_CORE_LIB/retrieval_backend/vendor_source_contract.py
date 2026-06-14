from __future__ import annotations

import re
from dataclasses import dataclass
from typing import Literal


RetrievalVendorKind = Literal["mgrep", "sqlite_vec", "qdrant"]
VendorSourceStatus = Literal["verified_source_declared", "unresolved_until_verified"]
VendorLicenseStatus = Literal["pending_vendor_gate"]
VendorScanStatus = Literal["not_scanned"]


_VENDOR_ENTRY_ID_PATTERN = re.compile(r"^retrieval_vendor_source_[a-z][a-z0-9_]*$")


def _require_text(value: str, field_name: str) -> str:
    if not isinstance(value, str):
        raise TypeError(f"{field_name} must be a string")
    normalized = value.strip()
    if not normalized:
        raise ValueError(f"{field_name} must not be empty")
    return normalized


def _require_bool(value: bool, field_name: str) -> bool:
    if not isinstance(value, bool):
        raise TypeError(f"{field_name} must be bool")
    return value


@dataclass(frozen=True, slots=True)
class RetrievalVendorSourceContract:
    vendor_source_id: str
    backend_kind: RetrievalVendorKind
    source_url: str
    source_status: VendorSourceStatus
    source_ref: str
    version_ref: str
    license_status: VendorLicenseStatus = "pending_vendor_gate"
    scan_status: VendorScanStatus = "not_scanned"
    vendor_gate_required: bool = True
    vendor_gate_completed: bool = False
    runtime_enabled: bool = False
    install_allowed: bool = False
    download_allowed_now: bool = False
    write_allowed: bool = False
    source_of_truth: bool = False
    fail_closed_until_source_verified: bool = False
    direct_execution_allowed: bool = False
    network_allowed_by_default: bool = False

    def __post_init__(self) -> None:
        vendor_source_id = _require_text(self.vendor_source_id, "vendor_source_id")
        backend_kind = _require_text(self.backend_kind, "backend_kind")
        source_url = _require_text(self.source_url, "source_url")
        source_status = _require_text(self.source_status, "source_status")
        source_ref = _require_text(self.source_ref, "source_ref")
        version_ref = _require_text(self.version_ref, "version_ref")
        license_status = _require_text(self.license_status, "license_status")
        scan_status = _require_text(self.scan_status, "scan_status")

        if not _VENDOR_ENTRY_ID_PATTERN.fullmatch(vendor_source_id):
            raise ValueError(f"Invalid vendor_source_id: {vendor_source_id}")
        if backend_kind not in RetrievalVendorKind.__args__:
            raise ValueError(f"unsupported backend_kind: {backend_kind}")
        if source_status not in VendorSourceStatus.__args__:
            raise ValueError(f"unsupported source_status: {source_status}")
        if license_status != "pending_vendor_gate":
            raise ValueError("license_status must be pending_vendor_gate")
        if scan_status != "not_scanned":
            raise ValueError("scan_status must be not_scanned")

        for field_name in (
            "vendor_gate_required",
            "vendor_gate_completed",
            "runtime_enabled",
            "install_allowed",
            "download_allowed_now",
            "write_allowed",
            "source_of_truth",
            "fail_closed_until_source_verified",
            "direct_execution_allowed",
            "network_allowed_by_default",
        ):
            _require_bool(getattr(self, field_name), field_name)

        if not self.vendor_gate_required:
            raise ValueError("vendor_gate_required must be True")
        if self.vendor_gate_completed:
            raise ValueError("vendor_gate_completed must be False before vendor gate")
        if self.runtime_enabled:
            raise ValueError("runtime_enabled must be False")
        if self.install_allowed:
            raise ValueError("install_allowed must be False")
        if self.download_allowed_now:
            raise ValueError("download_allowed_now must be False")
        if self.write_allowed:
            raise ValueError("write_allowed must be False")
        if self.source_of_truth:
            raise ValueError("source_of_truth must be False")
        if self.direct_execution_allowed:
            raise ValueError("direct_execution_allowed must be False")
        if self.network_allowed_by_default:
            raise ValueError("network_allowed_by_default must be False")
        if backend_kind == "mgrep" and not self.fail_closed_until_source_verified:
            raise ValueError("mgrep must fail closed until official source is verified")
        if source_status == "unresolved_until_verified" and source_url != "unresolved_until_verified":
            raise ValueError("unresolved source must use unresolved_until_verified source_url")
        if source_status == "verified_source_declared" and not source_url.startswith("https://github.com/"):
            raise ValueError("verified source declarations must use a GitHub source URL")

        object.__setattr__(self, "vendor_source_id", vendor_source_id)
        object.__setattr__(self, "backend_kind", backend_kind)
        object.__setattr__(self, "source_url", source_url)
        object.__setattr__(self, "source_status", source_status)
        object.__setattr__(self, "source_ref", source_ref)
        object.__setattr__(self, "version_ref", version_ref)
        object.__setattr__(self, "license_status", license_status)
        object.__setattr__(self, "scan_status", scan_status)

    def to_read_model(self) -> dict[str, object]:
        return {
            "vendor_source_id": self.vendor_source_id,
            "backend_kind": self.backend_kind,
            "source_url": self.source_url,
            "source_status": self.source_status,
            "source_ref": self.source_ref,
            "version_ref": self.version_ref,
            "license_status": self.license_status,
            "scan_status": self.scan_status,
            "vendor_gate_required": self.vendor_gate_required,
            "vendor_gate_completed": self.vendor_gate_completed,
            "runtime_enabled": self.runtime_enabled,
            "install_allowed": self.install_allowed,
            "download_allowed_now": self.download_allowed_now,
            "write_allowed": self.write_allowed,
            "source_of_truth": self.source_of_truth,
            "fail_closed_until_source_verified": self.fail_closed_until_source_verified,
            "direct_execution_allowed": self.direct_execution_allowed,
            "network_allowed_by_default": self.network_allowed_by_default,
        }


def build_retrieval_vendor_source_contracts() -> tuple[RetrievalVendorSourceContract, ...]:
    return (
        RetrievalVendorSourceContract(
            vendor_source_id="retrieval_vendor_source_sqlite_vec",
            backend_kind="sqlite_vec",
            source_url="https://github.com/asg017/sqlite-vec",
            source_status="verified_source_declared",
            source_ref="EXTERNAL_BACKENDS/vendor_quarantine/retrieval_backend_manifest.yaml#sqlite_vec",
            version_ref="unresolved_until_vendor_gate",
        ),
        RetrievalVendorSourceContract(
            vendor_source_id="retrieval_vendor_source_qdrant",
            backend_kind="qdrant",
            source_url="https://github.com/qdrant/qdrant",
            source_status="verified_source_declared",
            source_ref="EXTERNAL_BACKENDS/vendor_quarantine/retrieval_backend_manifest.yaml#qdrant",
            version_ref="unresolved_until_vendor_gate",
        ),
        RetrievalVendorSourceContract(
            vendor_source_id="retrieval_vendor_source_mgrep",
            backend_kind="mgrep",
            source_url="unresolved_until_verified",
            source_status="unresolved_until_verified",
            source_ref="EXTERNAL_BACKENDS/vendor_quarantine/retrieval_backend_manifest.yaml#mgrep",
            version_ref="unresolved_until_verified",
            fail_closed_until_source_verified=True,
        ),
    )


__all__ = [
    "RetrievalVendorKind",
    "RetrievalVendorSourceContract",
    "VendorLicenseStatus",
    "VendorScanStatus",
    "VendorSourceStatus",
    "build_retrieval_vendor_source_contracts",
]
