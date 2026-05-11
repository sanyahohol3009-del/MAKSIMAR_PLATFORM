from __future__ import annotations

import json
import subprocess
from pathlib import Path

from MAKSIMAR_SERVER.CONTROL_PLANE.memory_routing.adapters import (
    build_mempalace_probe_result_binding_preview,
    build_mempalace_read_only_routing_integration_preview,
    build_mempalace_real_backend_approval_envelope_preview,
    build_mempalace_runtime_sandbox_preview,
)


def test_phase_5_1_final_acceptance_evidence_reports_exist() -> None:
    reports = (
        "EXTERNAL_BACKENDS/mempalace/manifests/mempalace_source_manifest.json",
        "EXTERNAL_BACKENDS/mempalace/manifests/mempalace_version_lock.json",
        "EXTERNAL_BACKENDS/mempalace/smoke_reports/mempalace_sandbox_smoke_report.json",
        "EXTERNAL_BACKENDS/mempalace/security_reports/mempalace_integrity_security_report.json",
        "EXTERNAL_BACKENDS/mempalace/security_reports/mempalace_bandit_report.json",
        "EXTERNAL_BACKENDS/mempalace/security_reports/mempalace_pip_audit_report.json",
        "EXTERNAL_BACKENDS/mempalace/security_reports/mempalace_clamscan_report.txt",
        "EXTERNAL_BACKENDS/mempalace/security_reports/mempalace_vendor_gate_report.json",
        "EXTERNAL_BACKENDS/mempalace/security_reports/mempalace_risk_review_classification_report.json",
        "EXTERNAL_BACKENDS/mempalace/security_reports/mempalace_real_backend_approval_envelope_report.json",
        "EXTERNAL_BACKENDS/mempalace/smoke_reports/mempalace_controlled_real_backend_probe_report.json",
        "EXTERNAL_BACKENDS/mempalace/smoke_reports/mempalace_probe_result_binding_report.json",
        "EXTERNAL_BACKENDS/mempalace/smoke_reports/mempalace_read_only_routing_integration_report.json",
    )

    for report in reports:
        assert Path(report).exists(), report


def test_phase_5_1_final_acceptance_mempalace_read_only_state() -> None:
    sandbox = build_mempalace_runtime_sandbox_preview()
    approval = build_mempalace_real_backend_approval_envelope_preview()
    binding = build_mempalace_probe_result_binding_preview()
    routing = build_mempalace_read_only_routing_integration_preview()

    assert sandbox["preview_ready"] is True
    assert sandbox["fake_backend_used"] is True
    assert sandbox["real_backend_candidate_detected"] is True
    assert sandbox["real_backend_enabled"] is False
    assert sandbox["real_backend_query_allowed"] is False

    assert approval["approval_envelope_ready"] is True
    assert approval["controlled_real_backend_probe_allowed"] is True
    assert approval["full_real_backend_enablement_allowed"] is False
    assert approval["general_real_backend_query_allowed"] is False
    assert approval["network_allowed"] is False
    assert approval["subprocess_allowed"] is False
    assert approval["secrets_access_allowed"] is False

    assert binding["binding_ready"] is True
    assert binding["controlled_probe_success"] is True
    assert binding["real_import_verified"] is True
    assert binding["vendor_venv_used"] is True
    assert binding["read_only_adapter_binding_allowed"] is True

    assert routing["routing_integration_ready"] is True
    assert routing["subordinate_backend"] is True
    assert routing["read_only_routing_enabled"] is True
    assert routing["query_count"] == 4
    assert routing["write_routing_enabled"] is False
    assert routing["write_request_allowed_count"] == 0


def test_phase_5_1_final_acceptance_no_authority_leak() -> None:
    routing = build_mempalace_read_only_routing_integration_preview()

    assert routing["full_real_backend_enablement_allowed"] is False
    assert routing["general_real_backend_query_allowed"] is False
    assert routing["canonical_write_allowed"] is False
    assert routing["runtime_mutation_allowed"] is False
    assert routing["auto_promotion_allowed"] is False
    assert routing["auto_conflict_resolution_allowed"] is False


def test_phase_5_1_final_acceptance_external_code_not_committed() -> None:
    tracked = subprocess.check_output(
        [
            "git",
            "ls-files",
            "EXTERNAL_BACKENDS/mempalace/source",
            "EXTERNAL_BACKENDS/mempalace/venv",
            "EXTERNAL_BACKENDS/mempalace/sandbox_data",
        ],
        text=True,
    ).strip()

    assert tracked == ""


def test_phase_5_1_final_acceptance_report_payloads() -> None:
    vendor_gate = json.loads(
        Path("EXTERNAL_BACKENDS/mempalace/security_reports/mempalace_vendor_gate_report.json").read_text(
            encoding="utf-8"
        )
    )
    routing = json.loads(
        Path("EXTERNAL_BACKENDS/mempalace/smoke_reports/mempalace_read_only_routing_integration_report.json").read_text(
            encoding="utf-8"
        )
    )

    assert vendor_gate["hard_gate_passed"] is True
    assert vendor_gate["manual_security_review_required"] is True

    assert routing["routing_integration_ready"] is True
    assert routing["read_only_routing_enabled"] is True
    assert routing["write_routing_enabled"] is False
    assert routing["canonical_write_allowed"] is False
    assert routing["runtime_mutation_allowed"] is False
