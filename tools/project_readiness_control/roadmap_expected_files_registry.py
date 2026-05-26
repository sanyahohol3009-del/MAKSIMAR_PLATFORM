"""Roadmap expected files registry for MAKSIMAR project readiness control.

The registry must include the full active phase, not only completed batches.
This prevents false READY reports when only a subset of roadmap batches exists.
"""

from __future__ import annotations

from dataclasses import dataclass

from MAKSIMAR_CORE_LIB.architecture_map.project_file_readiness_models import (
    ExpectedProjectFile,
)


@dataclass(frozen=True)
class RoadmapExpectedBatch:
    """Expected files for one roadmap batch."""

    batch_id: str
    title: str
    expected_files: tuple[ExpectedProjectFile, ...]

    def __post_init__(self) -> None:
        if not self.batch_id:
            raise ValueError("batch_id must be non-empty")

        if not self.title:
            raise ValueError("title must be non-empty")

        if not self.expected_files:
            raise ValueError("expected_files must be non-empty")


ROADMAP_EXPECTED_BATCHES: tuple[RoadmapExpectedBatch, ...] = (
    RoadmapExpectedBatch(
        batch_id="0.1",
        title="Existing Scanner Discovery",
        expected_files=(
            ExpectedProjectFile(
                path="docs/architecture/open_source_integration/existing_scanner_discovery_v1.md",
                role="doc",
                description="Scanner discovery acceptance document.",
            ),
            ExpectedProjectFile(
                path="tools/project_readiness_control/scanner_discovery.py",
                role="tool",
                description="Read-only scanner/vendor gate discovery wrapper.",
            ),
            ExpectedProjectFile(
                path="tests/vendor_security_gate/test_existing_repo_scanner_discovery_smoke.py",
                role="test",
                description="Discovery report smoke test.",
            ),
            ExpectedProjectFile(
                path="tests/vendor_security_gate/test_existing_scanner_extend_not_duplicate_smoke.py",
                role="test",
                description="No duplicate scanner smoke test.",
            ),
        ),
    ),
    RoadmapExpectedBatch(
        batch_id="0.2",
        title="Repository Scan Models",
        expected_files=(
            ExpectedProjectFile(
                path="MAKSIMAR_CORE_LIB/security_layer/repository_scan_models.py",
                role="source",
                description="Repository scan result models.",
            ),
            ExpectedProjectFile(
                path="MAKSIMAR_CORE_LIB/security_layer/repository_risk_summary_builder.py",
                role="source",
                description="Repository risk summary builder.",
            ),
            ExpectedProjectFile(
                path="MAKSIMAR_CORE_LIB/security_layer/repository_quarantine_policy.py",
                role="source",
                description="Repository quarantine decision policy.",
            ),
            ExpectedProjectFile(
                path="tests/vendor_security_gate/test_repository_secret_detection_contract_smoke.py",
                role="test",
                description="Secret detection contract smoke test.",
            ),
            ExpectedProjectFile(
                path="tests/vendor_security_gate/test_repository_license_scan_contract_smoke.py",
                role="test",
                description="License scan contract smoke test.",
            ),
            ExpectedProjectFile(
                path="tests/vendor_security_gate/test_repository_dependency_risk_scan_contract_smoke.py",
                role="test",
                description="Dependency risk scan contract smoke test.",
            ),
            ExpectedProjectFile(
                path="tests/vendor_security_gate/test_repository_quarantine_decision_smoke.py",
                role="test",
                description="Repository quarantine decision smoke test.",
            ),
        ),
    ),
    RoadmapExpectedBatch(
        batch_id="0.3",
        title="Repository Scan Runtime",
        expected_files=(
            ExpectedProjectFile(
                path="MAKSIMAR_SERVER/EXTERNAL_REPO_SECURITY_RUNTIME/__init__.py",
                role="source",
                description="External repository security runtime package.",
            ),
            ExpectedProjectFile(
                path="MAKSIMAR_SERVER/EXTERNAL_REPO_SECURITY_RUNTIME/repository_scan_runtime.py",
                role="source",
                description="Repository scan runtime flow.",
            ),
            ExpectedProjectFile(
                path="tests/vendor_security_gate/test_repository_scan_runtime_smoke.py",
                role="test",
                description="Repository scan runtime smoke test.",
            ),
            ExpectedProjectFile(
                path="tests/vendor_security_gate/test_repository_dangerous_script_detection_contract_smoke.py",
                role="test",
                description="Dangerous script detection smoke test.",
            ),
        ),
    ),
    RoadmapExpectedBatch(
        batch_id="0.4",
        title="Pytest Output Hygiene",
        expected_files=(
            ExpectedProjectFile(
                path="conftest.py",
                role="config",
                description="Root pytest hooks with full-platform report gate.",
            ),
            ExpectedProjectFile(
                path="MAKSIMAR_CORE_LIB/architecture_map/pytest_architecture_plugin.py",
                role="source",
                description="Architecture pytest plugin guarded by full-platform report mode.",
            ),
            ExpectedProjectFile(
                path="MAKSIMAR_CORE_LIB/architecture_map/pytest_report_gate.py",
                role="source",
                description="Core-local pytest full-platform report gate.",
            ),
            ExpectedProjectFile(
                path="tests/architecture_map/test_pytest_report_gate_env_contract_smoke.py",
                role="test",
                description="Report gate env/option contract smoke test.",
            ),
            ExpectedProjectFile(
                path="tests/architecture_map/test_pytest_target_mode_does_not_emit_full_reports_smoke.py",
                role="test",
                description="Target pytest output hygiene smoke test.",
            ),
            ExpectedProjectFile(
                path="tests/architecture_map/test_pytest_full_auto_mode_emits_full_reports_smoke.py",
                role="test",
                description="Full-platform report mode smoke test.",
            ),
        ),
    ),
    RoadmapExpectedBatch(
        batch_id="0.5",
        title="Project Readiness Runner Core",
        expected_files=(
            ExpectedProjectFile(
                path="tools/project_readiness_control/__init__.py",
                role="tool",
                description="Project readiness control package.",
            ),
            ExpectedProjectFile(
                path="tools/project_readiness_control/run_readiness_gate.py",
                role="tool",
                description="Unified readiness gate runner.",
            ),
            ExpectedProjectFile(
                path="tools/project_readiness_control/target_test_runner.py",
                role="tool",
                description="Target test runner.",
            ),
            ExpectedProjectFile(
                path="tools/project_readiness_control/batch_gate_runner.py",
                role="tool",
                description="Batch gate runner.",
            ),
            ExpectedProjectFile(
                path="tools/project_readiness_control/full_platform_auto_runner.py",
                role="tool",
                description="Full platform auto runner.",
            ),
            ExpectedProjectFile(
                path="tests/project_readiness_control/test_target_test_runner_smoke.py",
                role="test",
                description="Target test runner smoke test.",
            ),
            ExpectedProjectFile(
                path="tests/project_readiness_control/test_batch_gate_runner_smoke.py",
                role="test",
                description="Batch gate runner smoke test.",
            ),
            ExpectedProjectFile(
                path="tests/project_readiness_control/test_full_platform_auto_runner_smoke.py",
                role="test",
                description="Full platform auto runner smoke test.",
            ),
        ),
    ),
    RoadmapExpectedBatch(
        batch_id="0.6",
        title="Project Readiness Sub-Runners",
        expected_files=(
            ExpectedProjectFile(
                path="tools/project_readiness_control/surface_inventory.py",
                role="tool",
                description="Surface inventory runner.",
            ),
            ExpectedProjectFile(
                path="tools/project_readiness_control/semantic_duplicate_scan_runner.py",
                role="tool",
                description="Semantic duplicate scan runner.",
            ),
            ExpectedProjectFile(
                path="tools/project_readiness_control/roadmap_ci_runner.py",
                role="tool",
                description="Roadmap CI runner.",
            ),
            ExpectedProjectFile(
                path="tools/project_readiness_control/forbidden_marker_scan.py",
                role="tool",
                description="Forbidden marker scan runner.",
            ),
            ExpectedProjectFile(
                path="tools/project_readiness_control/xray_runner.py",
                role="tool",
                description="X-Ray runner.",
            ),
            ExpectedProjectFile(
                path="tools/project_readiness_control/drift_guard_runner.py",
                role="tool",
                description="Drift Guard runner.",
            ),
            ExpectedProjectFile(
                path="tools/project_readiness_control/dirty_surface_classifier.py",
                role="tool",
                description="Dirty surface classifier.",
            ),
            ExpectedProjectFile(
                path="tests/project_readiness_control/test_surface_inventory_smoke.py",
                role="test",
                description="Surface inventory smoke test.",
            ),
            ExpectedProjectFile(
                path="tests/project_readiness_control/test_semantic_duplicate_runner_smoke.py",
                role="test",
                description="Semantic duplicate runner smoke test.",
            ),
            ExpectedProjectFile(
                path="tests/project_readiness_control/test_roadmap_ci_runner_smoke.py",
                role="test",
                description="Roadmap CI runner smoke test.",
            ),
            ExpectedProjectFile(
                path="tests/project_readiness_control/test_forbidden_marker_scan_smoke.py",
                role="test",
                description="Forbidden marker scan smoke test.",
            ),
            ExpectedProjectFile(
                path="tests/project_readiness_control/test_xray_runner_smoke.py",
                role="test",
                description="X-Ray runner smoke test.",
            ),
            ExpectedProjectFile(
                path="tests/project_readiness_control/test_drift_guard_runner_smoke.py",
                role="test",
                description="Drift Guard runner smoke test.",
            ),
            ExpectedProjectFile(
                path="tests/project_readiness_control/test_dirty_surface_classifier_smoke.py",
                role="test",
                description="Dirty surface classifier smoke test.",
            ),
        ),
    ),
    RoadmapExpectedBatch(
        batch_id="0.7",
        title="Readiness Runtime JSON + Dashboard Export",
        expected_files=(
            ExpectedProjectFile(
                path="tools/project_readiness_control/acceptance_evidence_collector.py",
                role="tool",
                description="Acceptance evidence collector.",
            ),
            ExpectedProjectFile(
                path="tools/project_readiness_control/dashboard_readiness_export.py",
                role="tool",
                description="Dashboard readiness JSON export.",
            ),
            ExpectedProjectFile(
                path="MAKSIMAR_CORE_LIB/readiness_control/readiness_status_read_model.py",
                role="source",
                description="Readiness status read model.",
            ),
            ExpectedProjectFile(
                path="tests/project_readiness_control/test_acceptance_evidence_collector_smoke.py",
                role="test",
                description="Acceptance evidence collector smoke test.",
            ),
            ExpectedProjectFile(
                path="tests/project_readiness_control/test_dashboard_readiness_export_smoke.py",
                role="test",
                description="Dashboard readiness export smoke test.",
            ),
            ExpectedProjectFile(
                path="tests/project_readiness_control/test_readiness_status_read_model_smoke.py",
                role="test",
                description="Readiness status read model smoke test.",
            ),
        ),
    ),
    RoadmapExpectedBatch(
        batch_id="0.8",
        title="PHASE 0 Acceptance",
        expected_files=(
            ExpectedProjectFile(
                path="docs/architecture/foundation/phase_0_readiness_output_hygiene_acceptance_v1.md",
                role="doc",
                description="PHASE 0 acceptance document.",
            ),
            ExpectedProjectFile(
                path="tests/project_readiness_control/test_phase_0_acceptance_smoke.py",
                role="test",
                description="PHASE 0 acceptance smoke test.",
            ),
        ),
    ),
)


def get_expected_batch(batch_id: str) -> RoadmapExpectedBatch:
    """Return one expected batch by id."""
    for batch in ROADMAP_EXPECTED_BATCHES:
        if batch.batch_id == batch_id:
            return batch

    raise KeyError(f"Unknown roadmap expected batch id: {batch_id!r}")


def list_expected_batches() -> tuple[RoadmapExpectedBatch, ...]:
    """Return all registered expected batches."""
    return ROADMAP_EXPECTED_BATCHES
