"""Dashboard-safe readiness export.

This tool exports a read-only readiness payload for dashboard consumption. It
writes only generated JSON output and never mutates canonical source files.
"""

from __future__ import annotations

import json
from dataclasses import dataclass
from pathlib import Path
from typing import Mapping

from MAKSIMAR_CORE_LIB.readiness_control.readiness_status_read_model import (
    ReadinessStatusReadModel,
)
from tools.project_readiness_control.acceptance_evidence_collector import (
    collect_acceptance_evidence,
)


_DEFAULT_OUTPUT_PATH = Path("RUNTIME/state/readiness/project_readiness_dashboard_export.json")


@dataclass(frozen=True, slots=True)
class DashboardReadinessExportResult:
    output_path: str
    payload: Mapping[str, object]
    bytes_written: int
    dashboard_safe: bool = True
    read_only_dashboard: bool = True
    runtime_mutation_allowed: bool = False
    canonical_write_allowed: bool = False
    dashboard_mutation_allowed: bool = False
    ui_to_execution_allowed: bool = False

    def __post_init__(self) -> None:
        if not self.output_path:
            raise ValueError("output_path must not be empty")
        if self.bytes_written <= 0:
            raise ValueError("bytes_written must be positive")
        if not self.dashboard_safe:
            raise ValueError("dashboard_safe must remain true")
        if not self.read_only_dashboard:
            raise ValueError("read_only_dashboard must remain true")
        if self.runtime_mutation_allowed:
            raise ValueError("runtime_mutation_allowed must remain false")
        if self.canonical_write_allowed:
            raise ValueError("canonical_write_allowed must remain false")
        if self.dashboard_mutation_allowed:
            raise ValueError("dashboard_mutation_allowed must remain false")
        if self.ui_to_execution_allowed:
            raise ValueError("ui_to_execution_allowed must remain false")

    def to_dict(self) -> dict[str, object]:
        return {
            "output_path": self.output_path,
            "payload": dict(self.payload),
            "bytes_written": self.bytes_written,
            "dashboard_safe": self.dashboard_safe,
            "read_only_dashboard": self.read_only_dashboard,
            "runtime_mutation_allowed": self.runtime_mutation_allowed,
            "canonical_write_allowed": self.canonical_write_allowed,
            "dashboard_mutation_allowed": self.dashboard_mutation_allowed,
            "ui_to_execution_allowed": self.ui_to_execution_allowed,
        }


def build_dashboard_readiness_payload(
    read_model: ReadinessStatusReadModel,
) -> dict[str, object]:
    if not isinstance(read_model, ReadinessStatusReadModel):
        raise TypeError("read_model must be ReadinessStatusReadModel")
    return {
        "schema_version": "project_readiness_dashboard_export.v1",
        "export_kind": "dashboard_readiness_read_model",
        "source_model": read_model.to_dict(),
        "dashboard_safe": True,
        "read_only_dashboard": True,
        "runtime_mutation_allowed": False,
        "canonical_write_allowed": False,
        "dashboard_mutation_allowed": False,
        "ui_to_execution_allowed": False,
    }


def write_dashboard_readiness_export(
    read_model: ReadinessStatusReadModel,
    *,
    output_path: str | Path = _DEFAULT_OUTPUT_PATH,
) -> DashboardReadinessExportResult:
    path = Path(output_path)
    payload = build_dashboard_readiness_payload(read_model)
    encoded = json.dumps(payload, ensure_ascii=False, indent=2, sort_keys=True)

    path.parent.mkdir(parents=True, exist_ok=True)
    tmp_path = path.with_suffix(path.suffix + ".tmp")
    tmp_path.write_text(encoded, encoding="utf-8")
    tmp_path.replace(path)

    return DashboardReadinessExportResult(
        output_path=str(path),
        payload=payload,
        bytes_written=len(encoded.encode("utf-8")),
    )


def export_dashboard_readiness(
    *,
    batch_id: str,
    project_root: str | Path = ".",
    output_path: str | Path = _DEFAULT_OUTPUT_PATH,
) -> DashboardReadinessExportResult:
    collection = collect_acceptance_evidence(
        batch_id=batch_id,
        project_root=project_root,
    )
    return write_dashboard_readiness_export(
        collection.read_model,
        output_path=output_path,
    )
