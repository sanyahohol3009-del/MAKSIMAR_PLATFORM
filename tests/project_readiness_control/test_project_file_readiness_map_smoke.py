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

    expected_ready = sum(1 for report in reports if report.status == "READY")
    expected_partial = sum(1 for report in reports if report.status == "PARTIAL")
    expected_missing = sum(1 for report in reports if report.status == "MISSING")
    expected_status = "READY" if expected_ready == len(reports) else "PARTIAL"

    assert payload["status"] == expected_status
    assert payload["total_batches"] == 35
    assert payload["ready_batches"] == expected_ready
    assert payload["partial_batches"] == expected_partial
    assert payload["missing_batches"] == expected_missing
    assert expected_ready + expected_partial + expected_missing == payload["total_batches"]

    rendered = render_text(payload)

    assert "PHASE/BATCH 0.8" in rendered
    assert "PHASE/BATCH 1.5" in rendered
    assert "PHASE/BATCH 2.1" in rendered
    assert "PHASE/BATCH 2.2" in rendered
    assert "PHASE/BATCH 2.3" in rendered
    assert "PHASE/BATCH 2.10" in rendered

    assert "Network Backend Adapter Contract" in rendered
    assert "VPN Profile / Session / Egress Contracts" in rendered
    assert "Server VPN Runtime / Read Model" in rendered
    assert "PHASE 2 Acceptance" in rendered

    assert "MAKSIMAR_CORE_LIB/network_security/network_backend_adapter_contract.py" in rendered
    assert "MAKSIMAR_CORE_LIB/network_security/vpn_profile_contract.py" in rendered
    assert "MAKSIMAR_SERVER/NETWORK_SECURITY_RUNTIME/network_posture_summary_builder.py" in rendered
    assert "docs/architecture/network_security/phase_2_network_security_acceptance_v1.md" in rendered
