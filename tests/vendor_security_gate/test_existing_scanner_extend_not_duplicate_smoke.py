from __future__ import annotations

from tools.project_readiness_control.scanner_discovery import (
    discover_existing_scanner_surfaces,
)


def test_existing_scanner_extend_not_duplicate_smoke() -> None:
    report = discover_existing_scanner_surfaces()

    assert report.decision == "EXTEND_EXISTING"
    assert report.duplicate_scanner_allowed is False
    assert report.forbidden_duplicate_roots_present == ()

    assert "tests/vendor_security_gate/test_vendor_security_gate_tool_smoke.py" in (
        report.existing_vendor_security_tests
    )
    assert "tests/vendor_security_gate/test_vendor_security_gate_report_shape_smoke.py" in (
        report.existing_vendor_security_tests
    )
    assert "tests/vendor_security_gate/test_vendor_security_gate_mempalace_smoke.py" in (
        report.existing_vendor_security_tests
    )

    assert "MAKSIMAR_CORE_LIB/security_layer" in report.existing_security_surfaces
    assert "MAKSIMAR_SERVER/SECURITY_LAYER" in report.existing_security_surfaces
