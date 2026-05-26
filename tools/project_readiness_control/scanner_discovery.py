"""Read-only scanner/vendor-gate discovery for MAKSIMAR Roadmap v4.2.

This module is intentionally a discovery wrapper, not a second scanner engine.
It detects existing scanner/security/vendor-gate surfaces and returns an
EXTEND_EXISTING decision when the canonical vendor gate is present.
"""

from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
from typing import Iterable


PROJECT_ROOT = Path(__file__).resolve().parents[2]

CANONICAL_VENDOR_GATE = Path("tools/vendor_security_gate.py")
SERVER_VENDOR_GATE_ADAPTER = Path(
    "MAKSIMAR_SERVER/SECURITY_LAYER/adapters/security_vendor_gate_adapter.py"
)

VENDOR_SECURITY_TESTS = (
    Path("tests/vendor_security_gate/test_vendor_security_gate_tool_smoke.py"),
    Path("tests/vendor_security_gate/test_vendor_security_gate_report_shape_smoke.py"),
    Path("tests/vendor_security_gate/test_vendor_security_gate_mempalace_smoke.py"),
)

SECURITY_SURFACES = (
    Path("MAKSIMAR_CORE_LIB/security_layer"),
    Path("MAKSIMAR_SERVER/SECURITY_LAYER"),
    Path("docs/security_governance"),
    Path("EXTERNAL_BACKENDS/mempalace/security_reports"),
)

FORBIDDEN_DUPLICATE_SCANNER_ROOTS = (
    Path("tools/project_scanner.py"),
    Path("tools/security_scanner.py"),
    Path("tools/vendor_scanner.py"),
    Path("MAKSIMAR_CORE_LIB/scanner"),
    Path("MAKSIMAR_SERVER/SCANNER"),
)


@dataclass(frozen=True)
class ScannerDiscoveryReport:
    """Read-only scanner discovery report.

    Attributes:
        decision: Discovery decision. Expected canonical value is
            ``EXTEND_EXISTING`` when the existing vendor gate is present.
        canonical_vendor_gate: Existing canonical vendor-gate path.
        canonical_vendor_gate_exists: Whether canonical vendor gate exists.
        server_vendor_gate_adapter: Existing server adapter path.
        server_vendor_gate_adapter_exists: Whether server adapter exists.
        existing_vendor_security_tests: Existing vendor security test paths.
        existing_security_surfaces: Existing security/governance/report surfaces.
        forbidden_duplicate_roots_present: Duplicate scanner roots that were found.
        duplicate_scanner_allowed: Always false for this roadmap batch.
    """

    decision: str
    canonical_vendor_gate: str
    canonical_vendor_gate_exists: bool
    server_vendor_gate_adapter: str
    server_vendor_gate_adapter_exists: bool
    existing_vendor_security_tests: tuple[str, ...]
    existing_security_surfaces: tuple[str, ...]
    forbidden_duplicate_roots_present: tuple[str, ...]
    duplicate_scanner_allowed: bool

    def __post_init__(self) -> None:
        """Validate report invariants."""
        if self.decision not in {"EXTEND_EXISTING", "DISCOVERY_BLOCKED"}:
            raise ValueError(f"Unsupported scanner discovery decision: {self.decision!r}")

        if not self.canonical_vendor_gate:
            raise ValueError("canonical_vendor_gate must be non-empty")

        if not self.server_vendor_gate_adapter:
            raise ValueError("server_vendor_gate_adapter must be non-empty")

        if self.duplicate_scanner_allowed:
            raise ValueError("duplicate scanner roots are never allowed")

        if self.decision == "EXTEND_EXISTING" and not self.canonical_vendor_gate_exists:
            raise ValueError("EXTEND_EXISTING requires canonical vendor gate to exist")


def _existing_relative_paths(paths: Iterable[Path], project_root: Path) -> tuple[str, ...]:
    """Return existing paths as deterministic POSIX strings."""
    existing: list[str] = []
    for relative_path in paths:
        absolute_path = project_root / relative_path
        if absolute_path.exists():
            existing.append(relative_path.as_posix())
    return tuple(sorted(existing))


def discover_existing_scanner_surfaces(
    project_root: Path | None = None,
) -> ScannerDiscoveryReport:
    """Discover existing scanner/vendor/security surfaces.

    Args:
        project_root: Optional project root. Defaults to repository root inferred
            from this file location.

    Returns:
        ScannerDiscoveryReport: Deterministic read-only discovery report.
    """
    root = (project_root or PROJECT_ROOT).resolve()

    canonical_vendor_gate_exists = (root / CANONICAL_VENDOR_GATE).is_file()
    server_vendor_gate_adapter_exists = (root / SERVER_VENDOR_GATE_ADAPTER).is_file()

    existing_tests = _existing_relative_paths(VENDOR_SECURITY_TESTS, root)
    existing_security_surfaces = _existing_relative_paths(SECURITY_SURFACES, root)
    forbidden_duplicates = _existing_relative_paths(FORBIDDEN_DUPLICATE_SCANNER_ROOTS, root)

    decision = "EXTEND_EXISTING" if canonical_vendor_gate_exists else "DISCOVERY_BLOCKED"

    return ScannerDiscoveryReport(
        decision=decision,
        canonical_vendor_gate=CANONICAL_VENDOR_GATE.as_posix(),
        canonical_vendor_gate_exists=canonical_vendor_gate_exists,
        server_vendor_gate_adapter=SERVER_VENDOR_GATE_ADAPTER.as_posix(),
        server_vendor_gate_adapter_exists=server_vendor_gate_adapter_exists,
        existing_vendor_security_tests=existing_tests,
        existing_security_surfaces=existing_security_surfaces,
        forbidden_duplicate_roots_present=forbidden_duplicates,
        duplicate_scanner_allowed=False,
    )


def render_scanner_discovery_report(report: ScannerDiscoveryReport) -> str:
    """Render a stable human-readable scanner discovery report."""
    lines = [
        "Scanner Discovery Report",
        f"decision={report.decision}",
        f"canonical_vendor_gate={report.canonical_vendor_gate}",
        f"canonical_vendor_gate_exists={report.canonical_vendor_gate_exists}",
        f"server_vendor_gate_adapter={report.server_vendor_gate_adapter}",
        f"server_vendor_gate_adapter_exists={report.server_vendor_gate_adapter_exists}",
        f"duplicate_scanner_allowed={report.duplicate_scanner_allowed}",
        "existing_vendor_security_tests:",
    ]

    lines.extend(f"- {path}" for path in report.existing_vendor_security_tests)
    lines.append("existing_security_surfaces:")
    lines.extend(f"- {path}" for path in report.existing_security_surfaces)
    lines.append("forbidden_duplicate_roots_present:")
    lines.extend(f"- {path}" for path in report.forbidden_duplicate_roots_present)

    return "\n".join(lines) + "\n"


def main() -> int:
    """CLI entry point."""
    report = discover_existing_scanner_surfaces()
    print(render_scanner_discovery_report(report), end="")
    return 0 if report.decision == "EXTEND_EXISTING" else 1


if __name__ == "__main__":
    raise SystemExit(main())
