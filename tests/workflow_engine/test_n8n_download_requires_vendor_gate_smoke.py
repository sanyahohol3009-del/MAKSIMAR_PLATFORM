from MAKSIMAR_SERVER.WORKFLOW_AUTOMATION_RUNTIME.n8n_adapter_contract import build_n8n_adapter_contract
from MAKSIMAR_SERVER.WORKFLOW_AUTOMATION_RUNTIME.n8n_vendor_gate_runtime import (
    build_n8n_vendor_gate_runtime,
)


def test_n8n_download_is_not_allowed_by_adapter_contract_before_vendor_gate() -> None:
    adapter = build_n8n_adapter_contract()

    assert adapter.requires_vendor_gate is True
    assert adapter.requires_sandbox_boundary is True
    assert adapter.download_allowed_now is False
    assert adapter.install_allowed_now is False
    assert adapter.runtime_execution_allowed_now is False


def test_n8n_sandbox_probe_decision_is_separate_from_production_runtime() -> None:
    adapter = build_n8n_adapter_contract()
    gate = build_n8n_vendor_gate_runtime()

    decision = gate.evaluate_sandbox_probe_request(
        adapter=adapter,
        requested_vendor_ref="n8n-io/n8n",
        security_scan_passed=True,
        license_review_passed=True,
        operator_approval_granted=True,
        sandbox_boundary_ready=True,
        container_boundary_ready=True,
    )

    assert decision.download_allowed is True
    assert decision.install_allowed is True
    assert decision.runtime_probe_allowed is True
    assert decision.production_runtime_allowed is False
    assert decision.sandbox_path_ref == "EXTERNAL_BACKENDS/n8n/sandbox"
