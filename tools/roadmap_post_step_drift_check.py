from __future__ import annotations

import argparse
import json
import subprocess
import sys
from dataclasses import asdict, dataclass
from pathlib import Path
from typing import Tuple

PROJECT_ROOT = Path(__file__).resolve().parents[1]
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from MAKSIMAR_CORE_LIB.memory_engine.project_surface_audit import (  # noqa: E402
    build_project_surface_summary,
)


FORBIDDEN_STAGED_PREFIXES = (
    "EXTERNAL_BACKENDS/mempalace/source/",
    "EXTERNAL_BACKENDS/mempalace/venv/",
    "EXTERNAL_BACKENDS/mempalace/sandbox_data/",
    "tests/runtime_core/",
)

REQUIRED_RECONCILIATION_DOCS = (
    "docs/architecture/foundation/original_phase_4_memory_drift_contradiction_candidate_acceptance_v1.md",
    "docs/architecture/foundation/original_phase_5_jarvis_memory_self_readability_acceptance_v1.md",
    "docs/architecture/foundation/phase_5_1_mempalace_adapter_final_acceptance_v1.md",
    "docs/architecture/foundation/roadmap_v5_reconciliation_after_phase_5_1_v1.md",
)

REQUIRED_RECONCILIATION_TESTS = (
    "tests/memory_engine/test_roadmap_v5_reconciliation_final_smoke.py",
    "tests/memory_engine/test_memory_drift_flow_preview_smoke.py",
    "tests/memory_engine/test_jarvis_memory_self_read_flow_smoke.py",
    "tests/memory_routing_adapters/test_phase_5_1_final_acceptance_smoke.py",
)


@dataclass(frozen=True, slots=True)
class RoadmapPostStepDriftReport:
    report_id: str
    structural_drift_check_ready: bool
    roadmap_semantic_drift_check_ready: bool
    critical_surfaces_present: bool
    total_surfaces: int
    tracked_surfaces: int
    untracked_surfaces: int
    forbidden_staged_paths: Tuple[str, ...]
    missing_required_docs: Tuple[str, ...]
    missing_required_tests: Tuple[str, ...]
    mempalace_is_extension_not_replacement: bool
    original_phase_4_closed: bool
    original_phase_5_closed: bool
    phase_5_1_closed: bool
    drift_check_passed: bool


def _git(args: list[str]) -> str:
    return subprocess.check_output(["git", *args], cwd=PROJECT_ROOT, text=True).strip()


def _staged_files() -> tuple[str, ...]:
    output = _git(["diff", "--cached", "--name-only"])
    if not output:
        return ()
    return tuple(line.strip() for line in output.splitlines() if line.strip())


def _missing(paths: tuple[str, ...]) -> tuple[str, ...]:
    return tuple(path for path in paths if not (PROJECT_ROOT / path).exists())


def _forbidden_staged() -> tuple[str, ...]:
    staged = _staged_files()
    blocked: list[str] = []

    for path in staged:
        for prefix in FORBIDDEN_STAGED_PREFIXES:
            if path.startswith(prefix):
                blocked.append(path)

    return tuple(blocked)


def build_roadmap_post_step_drift_report() -> RoadmapPostStepDriftReport:
    summary = build_project_surface_summary(PROJECT_ROOT)

    missing_docs = _missing(REQUIRED_RECONCILIATION_DOCS)
    missing_tests = _missing(REQUIRED_RECONCILIATION_TESTS)
    forbidden_staged = _forbidden_staged()

    original_phase_4_closed = "docs/architecture/foundation/original_phase_4_memory_drift_contradiction_candidate_acceptance_v1.md" not in missing_docs
    original_phase_5_closed = "docs/architecture/foundation/original_phase_5_jarvis_memory_self_readability_acceptance_v1.md" not in missing_docs
    phase_5_1_closed = "docs/architecture/foundation/phase_5_1_mempalace_adapter_final_acceptance_v1.md" not in missing_docs

    mempalace_is_extension_not_replacement = (
        phase_5_1_closed
        and original_phase_5_closed
        and (PROJECT_ROOT / "MAKSIMAR_CORE_LIB/memory_engine/self_readability").exists()
        and (PROJECT_ROOT / "MAKSIMAR_SERVER/CONTROL_PLANE/memory_routing/adapters").exists()
    )

    structural_ready = (
        summary["critical_surfaces_present"] is True
        and len(forbidden_staged) == 0
    )

    semantic_ready = (
        len(missing_docs) == 0
        and len(missing_tests) == 0
        and original_phase_4_closed
        and original_phase_5_closed
        and phase_5_1_closed
        and mempalace_is_extension_not_replacement
    )

    passed = structural_ready and semantic_ready

    return RoadmapPostStepDriftReport(
        report_id="roadmap_post_step_drift_report_001",
        structural_drift_check_ready=structural_ready,
        roadmap_semantic_drift_check_ready=semantic_ready,
        critical_surfaces_present=bool(summary["critical_surfaces_present"]),
        total_surfaces=int(summary["total_surfaces"]),
        tracked_surfaces=int(summary["tracked_surfaces"]),
        untracked_surfaces=int(summary["untracked_surfaces"]),
        forbidden_staged_paths=forbidden_staged,
        missing_required_docs=missing_docs,
        missing_required_tests=missing_tests,
        mempalace_is_extension_not_replacement=mempalace_is_extension_not_replacement,
        original_phase_4_closed=original_phase_4_closed,
        original_phase_5_closed=original_phase_5_closed,
        phase_5_1_closed=phase_5_1_closed,
        drift_check_passed=passed,
    )


def main() -> int:
    parser = argparse.ArgumentParser(description="MAKSIMAR roadmap post-step full drift check.")
    parser.add_argument("--write-report", action="store_true")
    parser.add_argument(
        "--report-path",
        default="project_audit/roadmap_post_step_drift_report.json",
    )
    args = parser.parse_args()

    report = build_roadmap_post_step_drift_report()
    payload = asdict(report)

    print("===== ROADMAP POST-STEP FULL DRIFT CHECK =====")
    print(json.dumps(payload, indent=2, ensure_ascii=False))

    if args.write_report:
        report_path = PROJECT_ROOT / args.report_path
        report_path.parent.mkdir(parents=True, exist_ok=True)
        report_path.write_text(json.dumps(payload, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
        print(f"report_written: {report_path}")

    return 0 if report.drift_check_passed else 1


if __name__ == "__main__":
    raise SystemExit(main())
