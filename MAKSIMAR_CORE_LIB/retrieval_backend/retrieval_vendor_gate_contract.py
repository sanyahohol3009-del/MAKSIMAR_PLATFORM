from __future__ import annotations

from dataclasses import dataclass

from MAKSIMAR_CORE_LIB.retrieval_backend.vendor_source_contract import (
    RetrievalVendorSourceContract,
    build_retrieval_vendor_source_contracts,
)


RETRIEVAL_VENDOR_GATE_ID = "retrieval_vendor_gate_contract_v1"


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
class RetrievalVendorGateContract:
    gate_id: str
    vendor_sources: tuple[RetrievalVendorSourceContract, ...]
    vendor_gate_required: bool = True
    source_verified_required: bool = True
    license_review_required: bool = True
    scanner_required: bool = True
    manifest_required: bool = True
    runtime_enabled: bool = False
    install_allowed: bool = False
    download_allowed_now: bool = False
    direct_execution_allowed: bool = False
    runtime_mutation_allowed: bool = False
    source_of_truth: bool = False

    def __post_init__(self) -> None:
        gate_id = _require_text(self.gate_id, "gate_id")
        if not isinstance(self.vendor_sources, tuple):
            raise TypeError("vendor_sources must be a tuple")
        if len(self.vendor_sources) != 3:
            raise ValueError("vendor_sources must include mgrep, sqlite_vec and qdrant")
        if not all(isinstance(source, RetrievalVendorSourceContract) for source in self.vendor_sources):
            raise TypeError("vendor_sources entries must be RetrievalVendorSourceContract")
        backend_kinds = tuple(source.backend_kind for source in self.vendor_sources)
        if backend_kinds != ("sqlite_vec", "qdrant", "mgrep"):
            raise ValueError("vendor_sources must be ordered as sqlite_vec, qdrant, mgrep")

        for field_name in (
            "vendor_gate_required",
            "source_verified_required",
            "license_review_required",
            "scanner_required",
            "manifest_required",
            "runtime_enabled",
            "install_allowed",
            "download_allowed_now",
            "direct_execution_allowed",
            "runtime_mutation_allowed",
            "source_of_truth",
        ):
            _require_bool(getattr(self, field_name), field_name)

        for field_name in (
            "vendor_gate_required",
            "source_verified_required",
            "license_review_required",
            "scanner_required",
            "manifest_required",
        ):
            if not getattr(self, field_name):
                raise ValueError(f"{field_name} must be True")
        for field_name in (
            "runtime_enabled",
            "install_allowed",
            "download_allowed_now",
            "direct_execution_allowed",
            "runtime_mutation_allowed",
            "source_of_truth",
        ):
            if getattr(self, field_name):
                raise ValueError(f"{field_name} must be False")
        if any(source.vendor_gate_completed for source in self.vendor_sources):
            raise ValueError("vendor gate cannot be completed in source resolution batch")
        if any(source.runtime_enabled for source in self.vendor_sources):
            raise ValueError("vendor sources must keep runtime disabled")

        object.__setattr__(self, "gate_id", gate_id)

    def to_read_model(self) -> dict[str, object]:
        return {
            "gate_id": self.gate_id,
            "vendor_gate_required": self.vendor_gate_required,
            "source_verified_required": self.source_verified_required,
            "license_review_required": self.license_review_required,
            "scanner_required": self.scanner_required,
            "manifest_required": self.manifest_required,
            "runtime_enabled": self.runtime_enabled,
            "install_allowed": self.install_allowed,
            "download_allowed_now": self.download_allowed_now,
            "direct_execution_allowed": self.direct_execution_allowed,
            "runtime_mutation_allowed": self.runtime_mutation_allowed,
            "source_of_truth": self.source_of_truth,
            "vendor_sources": tuple(source.to_read_model() for source in self.vendor_sources),
        }


def build_retrieval_vendor_gate_contract() -> RetrievalVendorGateContract:
    return RetrievalVendorGateContract(
        gate_id=RETRIEVAL_VENDOR_GATE_ID,
        vendor_sources=build_retrieval_vendor_source_contracts(),
    )


__all__ = [
    "RETRIEVAL_VENDOR_GATE_ID",
    "RetrievalVendorGateContract",
    "build_retrieval_vendor_gate_contract",
]
