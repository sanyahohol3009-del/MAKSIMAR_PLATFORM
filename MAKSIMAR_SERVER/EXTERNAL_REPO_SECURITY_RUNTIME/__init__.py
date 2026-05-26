"""External repository security runtime facade.

This package binds already-produced vendor security gate payloads to canonical
repository scan contracts. It does not execute scanners and does not import
tools/vendor_security_gate.py.
"""

from MAKSIMAR_SERVER.EXTERNAL_REPO_SECURITY_RUNTIME.repository_scan_runtime import (
    RepositoryScanRuntimeEvaluation,
    build_repository_scan_result_from_vendor_gate_payload,
    build_vendor_gate_security_signal_from_repository_scan_result,
    evaluate_repository_scan_runtime_from_vendor_gate_payload,
)

__all__ = (
    "RepositoryScanRuntimeEvaluation",
    "build_repository_scan_result_from_vendor_gate_payload",
    "build_vendor_gate_security_signal_from_repository_scan_result",
    "evaluate_repository_scan_runtime_from_vendor_gate_payload",
)
