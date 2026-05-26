"""Readiness status read-model for dashboard-safe project readiness export."""

from __future__ import annotations

from dataclasses import dataclass, field
from datetime import UTC, datetime
from typing import Mapping


_ALLOWED_EVIDENCE_STATUSES = {"passed", "failed", "warning", "skipped"}
_ALLOWED_READINESS_STATUSES = {"READY", "PARTIAL", "MISSING", "FAILED"}


def _ensure_non_empty(value: str, field_name: str) -> str:
    if not isinstance(value, str) or not value.strip():
        raise ValueError(f"{field_name} must be a non-empty string")
    return value.strip()


@dataclass(frozen=True, slots=True)
class ReadinessEvidenceEntry:
    evidence_id: str
    source: str
    status: str
    summary: str
    command: tuple[str, ...] = ()
    details: Mapping[str, object] = field(default_factory=dict)

    def __post_init__(self) -> None:
        object.__setattr__(self, "evidence_id", _ensure_non_empty(self.evidence_id, "evidence_id"))
        object.__setattr__(self, "source", _ensure_non_empty(self.source, "source"))
        object.__setattr__(self, "status", _ensure_non_empty(self.status, "status"))
        object.__setattr__(self, "summary", _ensure_non_empty(self.summary, "summary"))
        object.__setattr__(self, "details", dict(self.details))

        if self.status not in _ALLOWED_EVIDENCE_STATUSES:
            raise ValueError(f"unsupported evidence status: {self.status}")
        if any(not isinstance(part, str) or not part for part in self.command):
            raise ValueError("command entries must be non-empty strings")

    def to_dict(self) -> dict[str, object]:
        return {
            "evidence_id": self.evidence_id,
            "source": self.source,
            "status": self.status,
            "summary": self.summary,
            "command": list(self.command),
            "details": dict(self.details),
        }


@dataclass(frozen=True, slots=True)
class ReadinessStatusReadModel:
    schema_version: str
    model_id: str
    batch_id: str
    status: str
    generated_at_utc: str
    evidence: tuple[ReadinessEvidenceEntry, ...]
    dashboard_safe: bool = True
    read_only: bool = True
    runtime_mutation_allowed: bool = False
    canonical_write_allowed: bool = False
    dashboard_mutation_allowed: bool = False
    ui_to_execution_allowed: bool = False

    def __post_init__(self) -> None:
        object.__setattr__(self, "schema_version", _ensure_non_empty(self.schema_version, "schema_version"))
        object.__setattr__(self, "model_id", _ensure_non_empty(self.model_id, "model_id"))
        object.__setattr__(self, "batch_id", _ensure_non_empty(self.batch_id, "batch_id"))
        object.__setattr__(self, "status", _ensure_non_empty(self.status, "status"))
        object.__setattr__(self, "generated_at_utc", _ensure_non_empty(self.generated_at_utc, "generated_at_utc"))
        object.__setattr__(self, "evidence", tuple(self.evidence))

        if self.status not in _ALLOWED_READINESS_STATUSES:
            raise ValueError(f"unsupported readiness status: {self.status}")
        if any(not isinstance(entry, ReadinessEvidenceEntry) for entry in self.evidence):
            raise TypeError("evidence must contain ReadinessEvidenceEntry values")
        if self.status == "READY" and any(entry.status == "failed" for entry in self.evidence):
            raise ValueError("READY read-model must not contain failed evidence")
        if not self.dashboard_safe:
            raise ValueError("dashboard_safe must remain true")
        if not self.read_only:
            raise ValueError("read_only must remain true")
        if self.runtime_mutation_allowed:
            raise ValueError("runtime_mutation_allowed must remain false")
        if self.canonical_write_allowed:
            raise ValueError("canonical_write_allowed must remain false")
        if self.dashboard_mutation_allowed:
            raise ValueError("dashboard_mutation_allowed must remain false")
        if self.ui_to_execution_allowed:
            raise ValueError("ui_to_execution_allowed must remain false")

    @property
    def evidence_count(self) -> int:
        return len(self.evidence)

    @property
    def passed_count(self) -> int:
        return sum(1 for entry in self.evidence if entry.status == "passed")

    @property
    def failed_count(self) -> int:
        return sum(1 for entry in self.evidence if entry.status == "failed")

    @property
    def warning_count(self) -> int:
        return sum(1 for entry in self.evidence if entry.status == "warning")

    def to_dict(self) -> dict[str, object]:
        return {
            "schema_version": self.schema_version,
            "model_id": self.model_id,
            "batch_id": self.batch_id,
            "status": self.status,
            "generated_at_utc": self.generated_at_utc,
            "dashboard_safe": self.dashboard_safe,
            "read_only": self.read_only,
            "runtime_mutation_allowed": self.runtime_mutation_allowed,
            "canonical_write_allowed": self.canonical_write_allowed,
            "dashboard_mutation_allowed": self.dashboard_mutation_allowed,
            "ui_to_execution_allowed": self.ui_to_execution_allowed,
            "evidence_count": self.evidence_count,
            "passed_count": self.passed_count,
            "failed_count": self.failed_count,
            "warning_count": self.warning_count,
            "evidence": [entry.to_dict() for entry in self.evidence],
        }


def build_readiness_status_read_model(
    *,
    batch_id: str,
    status: str,
    evidence: tuple[ReadinessEvidenceEntry, ...],
    generated_at_utc: str | None = None,
) -> ReadinessStatusReadModel:
    return ReadinessStatusReadModel(
        schema_version="readiness_status_read_model.v1",
        model_id=f"project_readiness_{batch_id.replace('.', '_')}",
        batch_id=batch_id,
        status=status,
        generated_at_utc=generated_at_utc or datetime.now(UTC).isoformat(),
        evidence=tuple(evidence),
    )
