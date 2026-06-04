import pytest

from MAKSIMAR_SERVER.WORKFLOW_AUTOMATION_RUNTIME.n8n_adapter_contract import build_n8n_adapter_contract
from MAKSIMAR_SERVER.WORKFLOW_AUTOMATION_RUNTIME.n8n_vendor_gate_runtime import (
    N8nVendorGateDecision,
    N8nVendorGateRuntime,
    build_n8n_vendor_gate_runtime,
)


def test_n8n_vendor_gate_blocks_until_all_prerequisites_are_ready() -> None:
    gate = build_n8n_vendor_gate_runtime()
    adapter = build_n8n_adapter_contract()

    decision = gate.evaluate_sandbox_probe_request(
        adapter=adapter,
        requested_vendor_ref="n8n-io/n8n",
        security_scan_passed=True,
        license_review_passed=True,
        operator_approval_granted=False,
        sandbox_boundary_ready=True,
        container_boundary_ready=True,
    )

    assert decision.decision == "blocked"
    assert decision.download_allowed is False
    assert decision.install_allowed is False
    assert decision.runtime_probe_allowed is False
    assert decision.production_runtime_allowed is False


def test_n8n_vendor_gate_allows_sandbox_probe_only_after_prerequisites() -> None:
    gate = build_n8n_vendor_gate_runtime()
    adapter = build_n8n_adapter_contract()

    decision = gate.evaluate_sandbox_probe_request(
        adapter=adapter,
        requested_vendor_ref="n8n-io/n8n",
        security_scan_passed=True,
        license_review_passed=True,
        operator_approval_granted=True,
        sandbox_boundary_ready=True,
        container_boundary_ready=True,
    )

    assert decision.decision == "sandbox_probe_allowed"
    assert decision.download_allowed is True
    assert decision.install_allowed is True
    assert decision.runtime_probe_allowed is True
    assert decision.production_runtime_allowed is False
    assert decision.direct_core_write_allowed is False
    assert decision.direct_server_canonical_write_allowed is False


def test_n8n_vendor_gate_rejects_unknown_vendor_and_live_runtime_flags() -> None:
    gate = build_n8n_vendor_gate_runtime()
    adapter = build_n8n_adapter_contract()

    decision = gate.evaluate_sandbox_probe_request(
        adapter=adapter,
        requested_vendor_ref="unknown/vendor",
        security_scan_passed=True,
        license_review_passed=True,
        operator_approval_granted=True,
        sandbox_boundary_ready=True,
        container_boundary_ready=True,
    )
    assert decision.decision == "blocked"

    with pytest.raises(ValueError):
        N8nVendorGateRuntime(
            runtime_id="vendor.gate.unsafe",
            allowed_vendor_refs=("n8n-io/n8n",),
            live_download_performed=True,
        )

    with pytest.raises(ValueError):
        N8nVendorGateDecision(
            decision_id="decision.production.unsafe",
            adapter_id=adapter.adapter_id,
            decision="sandbox_probe_allowed",
            reason="unsafe production runtime",
            approved_vendor_refs=("n8n-io/n8n",),
            download_allowed=True,
            install_allowed=True,
            runtime_probe_allowed=True,
            production_runtime_allowed=True,
        )
