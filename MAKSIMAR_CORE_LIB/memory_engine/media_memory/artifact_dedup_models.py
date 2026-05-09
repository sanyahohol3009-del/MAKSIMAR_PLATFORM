from __future__ import annotations

import re
from dataclasses import dataclass
from typing import Literal


ArtifactDedupStatus = Literal[
    "existing_artifact",
    "new_artifact_candidate",
]


_ARTIFACT_ID_PATTERN = re.compile(r"^media_artifact_[a-z][a-z0-9_]*$")
_FINGERPRINT_PATTERN = re.compile(r"^sha256:[a-f0-9]{64}$")


def _ensure_non_empty_str(value: str, field_name: str) -> str:
    if not isinstance(value, str):
        raise ValueError(f"{field_name} must be a string")
    normalized = value.strip()
    if not normalized:
        raise ValueError(f"{field_name} must be a non-empty string")
    return normalized


def _ensure_bool(value: bool, field_name: str) -> bool:
    if not isinstance(value, bool):
        raise ValueError(f"{field_name} must be bool")
    return value


def _ensure_non_negative_int(value: int, field_name: str) -> int:
    if not isinstance(value, int):
        raise ValueError(f"{field_name} must be an int")
    if value < 0:
        raise ValueError(f"{field_name} must be >= 0")
    return value


@dataclass(frozen=True, slots=True)
class ArtifactDedupDecision:
    """Dedup decision for media/model/artifact memory.

    This does not write artifacts. It only states whether a candidate should be
    treated as already known or eligible for a future controlled write path.
    """

    artifact_id: str
    artifact_fingerprint: str
    status: ArtifactDedupStatus
    existing_record_ref: str
    write_allowed: bool
    rewrite_forbidden: bool

    def __post_init__(self) -> None:
        artifact_id = _ensure_non_empty_str(self.artifact_id, "artifact_id")
        artifact_fingerprint = _ensure_non_empty_str(
            self.artifact_fingerprint,
            "artifact_fingerprint",
        )
        existing_record_ref = self.existing_record_ref.strip() if isinstance(self.existing_record_ref, str) else ""

        if not _ARTIFACT_ID_PATTERN.fullmatch(artifact_id):
            raise ValueError(f"Invalid artifact_id: {artifact_id}")
        if not _FINGERPRINT_PATTERN.fullmatch(artifact_fingerprint):
            raise ValueError(f"Invalid artifact_fingerprint: {artifact_fingerprint}")

        _ensure_bool(self.write_allowed, "write_allowed")
        _ensure_bool(self.rewrite_forbidden, "rewrite_forbidden")

        if self.status == "existing_artifact":
            if not existing_record_ref:
                raise ValueError("existing artifacts must carry existing_record_ref")
            if self.write_allowed:
                raise ValueError("existing artifacts must not be write_allowed")
            if not self.rewrite_forbidden:
                raise ValueError("existing artifacts must set rewrite_forbidden=True")

        if self.status == "new_artifact_candidate":
            if existing_record_ref:
                raise ValueError("new artifact candidates must not carry existing_record_ref")
            if not self.write_allowed:
                raise ValueError("new artifact candidates must be write_allowed")
            if self.rewrite_forbidden:
                raise ValueError("new artifact candidates must not be rewrite_forbidden")

        object.__setattr__(self, "artifact_id", artifact_id)
        object.__setattr__(self, "artifact_fingerprint", artifact_fingerprint)
        object.__setattr__(self, "existing_record_ref", existing_record_ref)


@dataclass(frozen=True, slots=True)
class ArtifactDedupContract:
    total_decisions: int
    existing_artifacts: int
    new_artifact_candidates: int
    write_allowed_candidates: int
    rewrite_forbidden_existing: int
    decisions: tuple[ArtifactDedupDecision, ...]

    def __post_init__(self) -> None:
        total_decisions = _ensure_non_negative_int(self.total_decisions, "total_decisions")
        existing_artifacts = _ensure_non_negative_int(self.existing_artifacts, "existing_artifacts")
        new_artifact_candidates = _ensure_non_negative_int(
            self.new_artifact_candidates,
            "new_artifact_candidates",
        )
        write_allowed_candidates = _ensure_non_negative_int(
            self.write_allowed_candidates,
            "write_allowed_candidates",
        )
        rewrite_forbidden_existing = _ensure_non_negative_int(
            self.rewrite_forbidden_existing,
            "rewrite_forbidden_existing",
        )

        if total_decisions != len(self.decisions):
            raise ValueError("total_decisions must match decisions length")

        if existing_artifacts != sum(1 for decision in self.decisions if decision.status == "existing_artifact"):
            raise ValueError("existing_artifacts must match computed count")

        if new_artifact_candidates != sum(
            1 for decision in self.decisions if decision.status == "new_artifact_candidate"
        ):
            raise ValueError("new_artifact_candidates must match computed count")

        if write_allowed_candidates != sum(1 for decision in self.decisions if decision.write_allowed):
            raise ValueError("write_allowed_candidates must match computed count")

        if rewrite_forbidden_existing != sum(1 for decision in self.decisions if decision.rewrite_forbidden):
            raise ValueError("rewrite_forbidden_existing must match computed count")

        object.__setattr__(self, "total_decisions", total_decisions)
        object.__setattr__(self, "existing_artifacts", existing_artifacts)
        object.__setattr__(self, "new_artifact_candidates", new_artifact_candidates)
        object.__setattr__(self, "write_allowed_candidates", write_allowed_candidates)
        object.__setattr__(self, "rewrite_forbidden_existing", rewrite_forbidden_existing)
