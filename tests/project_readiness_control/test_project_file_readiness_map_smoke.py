from __future__ import annotations

from pathlib import Path

from tools.project_readiness_control.project_file_readiness_map import (
    build_readiness_reports,
    render_text,
    reports_to_payload,
)


def test_project_file_readiness_map_for_batch_0_1_smoke() -> None:
    project_root = Path(__file__).resolve().parents[2]

    reports = build_readiness_reports(project_root=project_root, batch_id="0.1")
    payload = reports_to_payload(reports)

    assert payload["status"] == "READY"
    assert payload["total_batches"] == 1
    assert payload["ready_batches"] == 1
    assert payload["partial_batches"] == 0
    assert payload["missing_batches"] == 0

    rendered = render_text(payload)
    assert "PHASE/BATCH 0.1" in rendered
    assert "Existing Scanner Discovery" in rendered
    assert "[OK] docs/architecture/open_source_integration/existing_scanner_discovery_v1.md" in rendered
    assert "[OK] tools/project_readiness_control/scanner_discovery.py" in rendered
def test_project_file_readiness_map_all_registered_batches_smoke() -> None:
    project_root = Path(__file__).resolve().parents[2]

    reports = build_readiness_reports(project_root=project_root)
    payload = reports_to_payload(reports)

    assert payload["status"] == "PARTIAL"
    assert payload["total_batches"] == 23
    assert payload["ready_batches"] == 14
    assert payload["partial_batches"] == 0
    assert payload["missing_batches"] == 9

    rendered = render_text(payload)

    assert "PHASE/BATCH 0.8" in rendered
    assert "[OK] docs/architecture/foundation/phase_0_readiness_output_hygiene_acceptance_v1.md" in rendered

    assert "PHASE/BATCH 1.5" in rendered
    assert "[OK] docs/architecture/open_source_integration/phase_1_open_source_canonicalization_acceptance_v1.md" in rendered
    assert "[OK] tests/open_source_integration/test_phase_1_acceptance_smoke.py" in rendered

    assert "PHASE/BATCH 2.1" in rendered
    assert "Network Backend Adapter Contract" in rendered
    assert "[OK] MAKSIMAR_CORE_LIB/network_security/network_backend_adapter_contract.py" in rendered
    assert "[OK] MAKSIMAR_CORE_LIB/network_security/vpn_policy_disable_contract.py" in rendered
    assert "[OK] tests/network_security/test_network_backend_adapter_contract_smoke.py" in rendered
    assert "[OK] tests/network_security/test_vpn_policy_can_disable_runtime_smoke.py" in rendered
    assert "[OK] tests/network_security/test_vpn_disabled_state_dashboard_visible_smoke.py" in rendered

    assert "PHASE/BATCH 2.10" in rendered
    assert "PHASE 2 Acceptance" in rendered
    assert "[MISSING] docs/architecture/network_security/phase_2_network_security_acceptance_v1.md" in rendered
    assert "[MISSING] tests/network_security/test_phase_2_acceptance_smoke.py" in rendered
