"""Acceptance evidence collector for project readiness control.

This collector reuses existing readiness runners. It does not mutate the repo,
does not auto-fix, and does not create a second readiness engine.
"""

from __future__ import annotations

import subprocess
import sys
from dataclasses import dataclass
from pathlib import Path

from MAKSIMAR_CORE_LIB.readiness_control.readiness_status_read_model import (
    ReadinessEvidenceEntry,
    ReadinessStatusReadModel,
    build_readiness_status_read_model,
)
from tools.project_readiness_control.dirty_surface_classifier import classify_dirty_surfaces
from tools.project_readiness_control.surface_inventory import run_surface_inventory


@dataclass(frozen=True, slots=True)
class AcceptanceEvidenceCollectionResult:
    batch_id: str
    read_model: ReadinessStatusReadModel
    repo_mutation_allowed: bool = False
    auto_fix_allowed: bool = False
    shell_execution_allowed: bool = False

    def __post_init__(self) -> None:
        if not self.batch_id:
            raise ValueError("batch_id must not be empty")
        if not isinstance(self.read_model, ReadinessStatusReadModel):
            raise TypeError("read_model must be ReadinessStatusReadModel")
        if self.repo_mutation_allowed:
            raise ValueError("repo_mutation_allowed must remain false")
        if self.auto_fix_allowed:
            raise ValueError("auto_fix_allowed must remain false")
        if self.shell_execution_allowed:
            raise ValueError("shell_execution_allowed must remain false")

    def to_dict(self) -> dict[str, object]:
        return {
            "batch_id": self.batch_id,
            "repo_mutation_allowed": self.repo_mutation_allowed,
            "auto_fix_allowed": self.auto_fix_allowed,
            "shell_execution_allowed": self.shell_execution_allowed,
            "read_model": self.read_model.to_dict(),
        }


def build_project_readiness_command(
    batch_id: str,
    *,
    python_executable: str | None = None,
) -> tuple[str, ...]:
    if not batch_id:
        raise ValueError("batch_id must not be empty")
    executable = python_executable or sys.executable
    if not executable:
        raise ValueError("python_executable must not be empty")
    return (
        executable,
        "tools/project_readiness_control/project_file_readiness_map.py",
        "--batch-id",
        batch_id,
    )


def _readiness_status_from_stdout(stdout: str) -> str:
    if "status=READY" in stdout:
        return "passed"
    if "status=MISSING" in stdout or "status=FAILED" in stdout:
        return "failed"
    return "warning"


def collect_acceptance_evidence(
    *,
    batch_id: str,
    project_root: str | Path = ".",
    python_executable: str | None = None,
) -> AcceptanceEvidenceCollectionResult:
    root = Path(project_root)

    readiness_command = build_project_readiness_command(
        batch_id,
        python_executable=python_executable,
    )
    readiness = subprocess.run(
        readiness_command,
        text=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        check=False,
        shell=False,
        cwd=str(root),
    )
    readiness_status = (
        _readiness_status_from_stdout(readiness.stdout)
        if readiness.returncode == 0
        else "failed"
    )

    surface_inventory = run_surface_inventory(root)
    dirty_surfaces = classify_dirty_surfaces(project_root=root)

    evidence = (
        ReadinessEvidenceEntry(
            evidence_id="project_file_readiness_map",
            source="tools/project_readiness_control/project_file_readiness_map.py",
            status=readiness_status,
            summary="Batch file readiness map collected.",
            command=readiness_command,
            details={
                "returncode": readiness.returncode,
                "stdout_contains_ready": "status=READY" in readiness.stdout,
                "stderr_present": bool(readiness.stderr.strip()),
            },
        ),
        ReadinessEvidenceEntry(
            evidence_id="surface_inventory",
            source="tools/project_readiness_control/surface_inventory.py",
            status="passed" if surface_inventory.critical_surfaces_present else "failed",
            summary="Project surface inventory collected through existing audit surface.",
            details={
                "total_surfaces": surface_inventory.total_surfaces,
                "tracked_surfaces": surface_inventory.tracked_surfaces,
                "untracked_surfaces": surface_inventory.untracked_surfaces,
                "critical_surfaces_present": surface_inventory.critical_surfaces_present,
            },
        ),
        ReadinessEvidenceEntry(
            evidence_id="dirty_surface_classifier",
            source="tools/project_readiness_control/dirty_surface_classifier.py",
            status="warning" if dirty_surfaces.dirty_count else "passed",
            summary="Dirty surfaces classified read-only; existing unrelated dirt is not auto-fixed.",
            details={
                "dirty_count": dirty_surfaces.dirty_count,
                "untracked_count": dirty_surfaces.untracked_count,
            },
        ),
    )

    readiness_failed = any(entry.status == "failed" for entry in evidence)
    read_model = build_readiness_status_read_model(
        batch_id=batch_id,
        status="FAILED" if readiness_failed else "READY",
        evidence=evidence,
    )

    return AcceptanceEvidenceCollectionResult(
        batch_id=batch_id,
        read_model=read_model,
    )
