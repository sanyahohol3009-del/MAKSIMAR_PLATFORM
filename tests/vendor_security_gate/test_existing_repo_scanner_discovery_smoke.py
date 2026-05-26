from __future__ import annotations

from tools.project_readiness_control.scanner_discovery import (
    discover_existing_scanner_surfaces,
    render_scanner_discovery_report,
)


def test_existing_repo_scanner_discovery_smoke() -> None:
    report = discover_existing_scanner_surfaces()

    assert report.decision == "EXTEND_EXISTING"
    assert report.canonical_vendor_gate == "tools/vendor_security_gate.py"
    assert report.canonical_vendor_gate_exists is True
    assert report.server_vendor_gate_adapter == (
        "MAKSIMAR_SERVER/SECURITY_LAYER/adapters/security_vendor_gate_adapter.py"
    )
    assert report.server_vendor_gate_adapter_exists is True
    assert report.duplicate_scanner_allowed is False

    rendered = render_scanner_discovery_report(report)
    assert "decision=EXTEND_EXISTING" in rendered
    assert "tools/vendor_security_gate.py" in rendered
