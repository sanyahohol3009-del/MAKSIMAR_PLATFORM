from __future__ import annotations

from pathlib import Path

from MAKSIMAR_CORE_LIB.security_layer.repository_quarantine_policy import (
    RepositoryQuarantineAction,
)
from MAKSIMAR_CORE_LIB.security_layer.repository_scan_models import (
    RepositoryFindingSeverity,
)
from MAKSIMAR_SERVER.EXTERNAL_REPO_SECURITY_RUNTIME.repository_scan_runtime import (
    evaluate_repository_scan_runtime_from_vendor_gate_payload,
)


def test_repository_scan_runtime_maps_clean_vendor_gate_payload_smoke() -> None:
    payload = {
        "vendor_name": "clean_vendor",
        "source_dir": "EXTERNAL_BACKENDS/clean_vendor/source",
        "official_remote_verified": True,
        "commit_seen_in_remote_refs": True,
        "canonical_memory_access": False,
        "runtime_mutation_allowed": False,
        "risky_static_findings_count": 0,
        "dependency_vulnerabilities_count": 0,
        "scanner_results": {},
        "hard_gate_passed": True,
        "manual_security_review_required": False,
        "hard_blockers": (),
        "risky_static_findings": (),
    }

    evaluation = evaluate_repository_scan_runtime_from_vendor_gate_payload(payload)

    assert evaluation.scan_result.repository_id == "clean_vendor"
    assert evaluation.scan_result.findings == ()
    assert evaluation.risk_summary.risk_level is RepositoryFindingSeverity.INFO
    assert evaluation.quarantine_decision.action is RepositoryQuarantineAction.ALLOW_READ_ONLY
    assert evaluation.vendor_gate_decision.allowed_for_runtime is True
    assert evaluation.scanner_runtime_executed is False
    assert evaluation.direct_execution_allowed is False


def test_repository_scan_runtime_does_not_import_or_execute_scanner_smoke() -> None:
    source = Path(
        "MAKSIMAR_SERVER/EXTERNAL_REPO_SECURITY_RUNTIME/repository_scan_runtime.py"
    ).read_text(encoding="utf-8")

    forbidden_markers = (
        "import subprocess",
        "subprocess.",
        "os.system",
        "tools.vendor_security_gate",
        "from tools.vendor_security_gate",
        "build_vendor_gate_report(",
    )

    for marker in forbidden_markers:
        assert marker not in source
