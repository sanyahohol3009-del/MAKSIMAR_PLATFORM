from __future__ import annotations

from dataclasses import dataclass
from typing import Tuple

from MAKSIMAR_SERVER.WORKFLOW_AUTOMATION_RUNTIME.n8n_adapter_contract import N8nAdapterContract


ALLOWED_VENDOR_GATE_DECISIONS: Tuple[str, ...] = (
    "blocked",
    "sandbox_probe_allowed",
)


def _require_non_empty_text(value: str, field_name: str) -> str:
    if not isinstance(value, str):
        raise TypeError(f"{field_name} must be a string")
    normalized = value.strip()
    if not normalized:
        raise ValueError(f"{field_name} must not be empty")
    return normalized


def _normalize_text_tuple(values: Tuple[str, ...], field_name: str, *, require_non_empty: bool) -> Tuple[str, ...]:
    if not isinstance(values, tuple):
        raise TypeError(f"{field_name} must be a tuple of strings")
    normalized = tuple(_require_non_empty_text(value, field_name) for value in values)
    if require_non_empty and not normalized:
        raise ValueError(f"{field_name} must not be empty")
    if len(set(normalized)) != len(normalized):
        raise ValueError(f"{field_name} must not contain duplicates")
    return normalized


def _require_true(value: bool, field_name: str) -> None:
    if value is not True:
        raise ValueError(f"{field_name} must be True in n8n vendor gate runtime")


def _require_false(value: bool, field_name: str) -> None:
    if value is not False:
        raise ValueError(f"{field_name} must be False in n8n vendor gate runtime")


@dataclass(frozen=True)
class N8nVendorGateDecision:
    decision_id: str
    adapter_id: str
    decision: str
    reason: str
    approved_vendor_refs: Tuple[str, ...] = ()
    sandbox_path_ref: str = "EXTERNAL_BACKENDS/n8n/sandbox"
    download_allowed: bool = False
    install_allowed: bool = False
    runtime_probe_allowed: bool = False
    production_runtime_allowed: bool = False
    direct_core_write_allowed: bool = False
    direct_server_canonical_write_allowed: bool = False

    def __post_init__(self) -> None:
        object.__setattr__(self, "decision_id", _require_non_empty_text(self.decision_id, "decision_id"))
        object.__setattr__(self, "adapter_id", _require_non_empty_text(self.adapter_id, "adapter_id"))
        if self.decision not in ALLOWED_VENDOR_GATE_DECISIONS:
            raise ValueError(f"decision must be one of {ALLOWED_VENDOR_GATE_DECISIONS}")
        object.__setattr__(self, "reason", _require_non_empty_text(self.reason, "reason"))
        object.__setattr__(
            self,
            "approved_vendor_refs",
            _normalize_text_tuple(
                self.approved_vendor_refs,
                "approved_vendor_refs",
                require_non_empty=False,
            ),
        )
        object.__setattr__(self, "sandbox_path_ref", _require_non_empty_text(self.sandbox_path_ref, "sandbox_path_ref"))

        if self.decision == "blocked":
            _require_false(self.download_allowed, "download_allowed")
            _require_false(self.install_allowed, "install_allowed")
            _require_false(self.runtime_probe_allowed, "runtime_probe_allowed")
            _require_false(self.production_runtime_allowed, "production_runtime_allowed")

        if self.decision == "sandbox_probe_allowed":
            _require_true(self.download_allowed, "download_allowed")
            _require_true(self.install_allowed, "install_allowed")
            _require_true(self.runtime_probe_allowed, "runtime_probe_allowed")
            _require_false(self.production_runtime_allowed, "production_runtime_allowed")
            if not self.approved_vendor_refs:
                raise ValueError("sandbox probe allowance requires approved_vendor_refs")

        _require_false(self.direct_core_write_allowed, "direct_core_write_allowed")
        _require_false(self.direct_server_canonical_write_allowed, "direct_server_canonical_write_allowed")

    def to_read_model(self) -> dict[str, object]:
        return {
            "decision_id": self.decision_id,
            "adapter_id": self.adapter_id,
            "decision": self.decision,
            "reason": self.reason,
            "approved_vendor_refs": self.approved_vendor_refs,
            "sandbox_path_ref": self.sandbox_path_ref,
            "download_allowed": self.download_allowed,
            "install_allowed": self.install_allowed,
            "runtime_probe_allowed": self.runtime_probe_allowed,
            "production_runtime_allowed": self.production_runtime_allowed,
            "direct_core_write_allowed": self.direct_core_write_allowed,
            "direct_server_canonical_write_allowed": self.direct_server_canonical_write_allowed,
        }


@dataclass(frozen=True)
class N8nVendorGateRuntime:
    runtime_id: str
    allowed_vendor_refs: Tuple[str, ...]
    sandbox_root_ref: str = "EXTERNAL_BACKENDS/n8n/sandbox"
    requires_security_scan: bool = True
    requires_license_review: bool = True
    requires_operator_approval: bool = True
    requires_network_isolation: bool = True
    requires_container_boundary: bool = True
    contract_only: bool = True
    live_download_performed: bool = False
    live_install_performed: bool = False
    direct_core_write_allowed: bool = False
    direct_server_canonical_write_allowed: bool = False
    network_allowed_by_default: bool = False

    def __post_init__(self) -> None:
        object.__setattr__(self, "runtime_id", _require_non_empty_text(self.runtime_id, "runtime_id"))
        object.__setattr__(
            self,
            "allowed_vendor_refs",
            _normalize_text_tuple(
                self.allowed_vendor_refs,
                "allowed_vendor_refs",
                require_non_empty=True,
            ),
        )
        object.__setattr__(self, "sandbox_root_ref", _require_non_empty_text(self.sandbox_root_ref, "sandbox_root_ref"))

        _require_true(self.requires_security_scan, "requires_security_scan")
        _require_true(self.requires_license_review, "requires_license_review")
        _require_true(self.requires_operator_approval, "requires_operator_approval")
        _require_true(self.requires_network_isolation, "requires_network_isolation")
        _require_true(self.requires_container_boundary, "requires_container_boundary")
        _require_true(self.contract_only, "contract_only")

        _require_false(self.live_download_performed, "live_download_performed")
        _require_false(self.live_install_performed, "live_install_performed")
        _require_false(self.direct_core_write_allowed, "direct_core_write_allowed")
        _require_false(self.direct_server_canonical_write_allowed, "direct_server_canonical_write_allowed")
        _require_false(self.network_allowed_by_default, "network_allowed_by_default")

    def evaluate_sandbox_probe_request(
        self,
        *,
        adapter: N8nAdapterContract,
        requested_vendor_ref: str,
        security_scan_passed: bool,
        license_review_passed: bool,
        operator_approval_granted: bool,
        sandbox_boundary_ready: bool,
        container_boundary_ready: bool,
    ) -> N8nVendorGateDecision:
        if not isinstance(adapter, N8nAdapterContract):
            raise TypeError("adapter must be an N8nAdapterContract")

        vendor_ref = _require_non_empty_text(requested_vendor_ref, "requested_vendor_ref")
        if vendor_ref not in self.allowed_vendor_refs:
            return N8nVendorGateDecision(
                decision_id=f"{adapter.adapter_id}.vendor.blocked",
                adapter_id=adapter.adapter_id,
                decision="blocked",
                reason="requested vendor ref is not in allowed_vendor_refs",
            )

        if not (
            security_scan_passed
            and license_review_passed
            and operator_approval_granted
            and sandbox_boundary_ready
            and container_boundary_ready
        ):
            return N8nVendorGateDecision(
                decision_id=f"{adapter.adapter_id}.vendor.blocked",
                adapter_id=adapter.adapter_id,
                decision="blocked",
                reason="vendor gate prerequisites are incomplete",
            )

        return N8nVendorGateDecision(
            decision_id=f"{adapter.adapter_id}.vendor.sandbox_probe_allowed",
            adapter_id=adapter.adapter_id,
            decision="sandbox_probe_allowed",
            reason="vendor gate prerequisites are complete for sandbox probe only",
            approved_vendor_refs=(vendor_ref,),
            sandbox_path_ref=self.sandbox_root_ref,
            download_allowed=True,
            install_allowed=True,
            runtime_probe_allowed=True,
            production_runtime_allowed=False,
        )


def build_n8n_vendor_gate_runtime() -> N8nVendorGateRuntime:
    return N8nVendorGateRuntime(
        runtime_id="phase6.n8n.vendor.gate.runtime.v1",
        allowed_vendor_refs=("n8n-io/n8n",),
    )


__all__ = [
    "ALLOWED_VENDOR_GATE_DECISIONS",
    "N8nVendorGateDecision",
    "N8nVendorGateRuntime",
    "build_n8n_vendor_gate_runtime",
]
