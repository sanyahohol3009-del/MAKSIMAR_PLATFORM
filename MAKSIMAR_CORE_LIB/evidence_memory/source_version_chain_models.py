from __future__ import annotations

import re
from dataclasses import dataclass


_SOURCE_VERSION_ID_PATTERN = re.compile(r"^source_version_[a-z][a-z0-9_]*$")
_SOURCE_EVENT_ID_PATTERN = re.compile(r"^source_event_[a-z][a-z0-9_]*$")
_VERSION_PATTERN = re.compile(r"^v[0-9]+$")


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


@dataclass(frozen=True, slots=True)
class SourceVersionChainRecord:
    source_version_id: str
    source_event_id: str
    source_version: str
    previous_source_version: str
    version_chain_ready: bool

    def __post_init__(self) -> None:
        source_version_id = _ensure_non_empty_str(
            self.source_version_id,
            "source_version_id",
        )
        source_event_id = _ensure_non_empty_str(
            self.source_event_id,
            "source_event_id",
        )
        source_version = _ensure_non_empty_str(
            self.source_version,
            "source_version",
        )

        if not _SOURCE_VERSION_ID_PATTERN.fullmatch(source_version_id):
            raise ValueError(f"Invalid source_version_id: {source_version_id}")
        if not _SOURCE_EVENT_ID_PATTERN.fullmatch(source_event_id):
            raise ValueError(f"Invalid source_event_id: {source_event_id}")
        if not _VERSION_PATTERN.fullmatch(source_version):
            raise ValueError("source_version must match v<number>")

        if self.previous_source_version and not _VERSION_PATTERN.fullmatch(
            self.previous_source_version
        ):
            raise ValueError("previous_source_version must be empty or match v<number>")

        version_chain_ready = _ensure_bool(
            self.version_chain_ready,
            "version_chain_ready",
        )
        if not version_chain_ready:
            raise ValueError("version_chain_ready must be True")

        object.__setattr__(self, "source_version_id", source_version_id)
        object.__setattr__(self, "source_event_id", source_event_id)
        object.__setattr__(self, "source_version", source_version)


@dataclass(frozen=True, slots=True)
class SourceVersionChainContract:
    total_versions: int
    ready_versions: int
    versions: tuple[SourceVersionChainRecord, ...]

    def __post_init__(self) -> None:
        if self.total_versions != len(self.versions):
            raise ValueError("total_versions must match versions length")
        if self.total_versions <= 0:
            raise ValueError("total_versions must be >= 1")
        if self.ready_versions != sum(
            1 for version in self.versions if version.version_chain_ready
        ):
            raise ValueError("ready_versions must match computed count")
        if self.ready_versions != self.total_versions:
            raise ValueError("all source versions must be ready")

        version_ids = tuple(version.source_version_id for version in self.versions)
        if len(set(version_ids)) != len(version_ids):
            raise ValueError("duplicate source_version_id values detected")
