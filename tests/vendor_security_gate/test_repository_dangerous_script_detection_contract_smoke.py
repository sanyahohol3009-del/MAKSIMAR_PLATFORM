from __future__ import annotations

from MAKSIMAR_CORE_LIB.security_layer.repository_quarantine_policy import (
    RepositoryQuarantineAction,
)
from MAKSIMAR_CORE_LIB.security_layer.repository_scan_models import (
    RepositoryFindingKind,
    RepositoryFindingSeverity,
)
from MAKSIMAR_SERVER.EXTERNAL_REPO_SECURITY_RUNTIME.repository_scan_runtime import (
    evaluate_repository_scan_runtime_from_vendor_gate_payload,
)


def test_repository_dangerous_script_detection_from_vendor_gate_payload_smoke() -> None:
    payload = {
        "vendor_name": "risky_vendor",
        "source_dir": "EXTERNAL_BACKENDS/risky_vendor/source",
        "official_remote_verified": True,
        "commit_seen_in_remote_refs": True,
        "canonical_memory_access": False,
        "runtime_mutation_allowed": False,
        "risky_static_findings_count": 1,
        "dependency_vulnerabilities_count": 0,
        "scanner_results": {},
        "hard_gate_passed": False,
        "manual_security_review_required": True,
        "hard_blockers": (),
        "risky_static_findings": (
            {
                "file": "setup.py",
                "line": "10",
                "call": "os.system",
            },
        ),
    }

    evaluation = evaluate_repository_scan_runtime_from_vendor_gate_payload(payload)

    assert len(evaluation.scan_result.findings) == 1
    finding = evaluation.scan_result.findings[0]

    assert finding.kind is RepositoryFindingKind.DANGEROUS_SCRIPT
    assert finding.severity is RepositoryFindingSeverity.HIGH
    assert "os.system" in finding.message
    assert evaluation.risk_summary.dangerous_script_findings == 1
    assert evaluation.quarantine_decision.action is RepositoryQuarantineAction.QUARANTINE
    assert evaluation.vendor_gate_decision.allowed_for_runtime is False
    assert "risky_static_findings_present" in evaluation.vendor_gate_decision.reason_codes


def test_repository_runtime_maps_detect_secrets_to_block_smoke() -> None:
    payload = {
        "vendor_name": "secret_vendor",
        "source_dir": "EXTERNAL_BACKENDS/secret_vendor/source",
        "official_remote_verified": True,
        "commit_seen_in_remote_refs": True,
        "canonical_memory_access": False,
        "runtime_mutation_allowed": False,
        "risky_static_findings_count": 0,
        "dependency_vulnerabilities_count": 0,
        "scanner_results": {
            "detect_secrets": {
                "available": True,
                "returncode": 1,
                "output_path": "security_reports/vendor_detect_secrets_report.json",
            }
        },
        "hard_gate_passed": False,
        "manual_security_review_required": True,
        "hard_blockers": (),
        "risky_static_findings": (),
    }

    evaluation = evaluate_repository_scan_runtime_from_vendor_gate_payload(payload)

    assert evaluation.scan_result.verified_secret_count == 1
    assert evaluation.risk_summary.risk_level is RepositoryFindingSeverity.CRITICAL
    assert evaluation.quarantine_decision.action is RepositoryQuarantineAction.BLOCK
    assert evaluation.quarantine_decision.allowed_for_read_only_reference is False
    assert evaluation.vendor_gate_decision.allowed_for_runtime is False
    assert "verified_secret_found" in evaluation.vendor_gate_decision.reason_codes
