from __future__ import annotations

from dataclasses import asdict, dataclass
from typing import Any


@dataclass(frozen=True, slots=True)
class ObjectStorageArtifactReference:
    artifact_ref: str
    object_storage_uri: str
    backend_id: str
    sha256: str
    size_bytes: int
    content_type: str
    producer_layer_id: str
    trace_id: str
    dashboard_safe: bool = True
    inline_payload_allowed: bool = False
    control_path_payload_allowed: bool = False
    runtime_mutation_allowed: bool = False
    canonical_write_allowed: bool = False

    def __post_init__(self) -> None:
        for field_name, value in (
            ("artifact_ref", self.artifact_ref),
            ("object_storage_uri", self.object_storage_uri),
            ("backend_id", self.backend_id),
            ("sha256", self.sha256),
            ("content_type", self.content_type),
            ("producer_layer_id", self.producer_layer_id),
            ("trace_id", self.trace_id),
        ):
            if not value:
                raise ValueError(f"{field_name} must not be empty")
        if self.size_bytes < 0:
            raise ValueError("size_bytes must not be negative")
        if len(self.sha256) != 64:
            raise ValueError("sha256 must be a 64-character sha256 hex string")
        int(self.sha256, 16)
        if not self.dashboard_safe:
            raise ValueError("dashboard_safe must remain true")
        if self.inline_payload_allowed:
            raise ValueError("inline_payload_allowed must remain false")
        if self.control_path_payload_allowed:
            raise ValueError("control_path_payload_allowed must remain false")
        if self.runtime_mutation_allowed:
            raise ValueError("runtime_mutation_allowed must remain false")
        if self.canonical_write_allowed:
            raise ValueError("canonical_write_allowed must remain false")

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)


@dataclass(frozen=True, slots=True)
class ObjectStorageReadinessReadModel:
    backend_id: str
    artifact_ref: str
    object_storage_ready: bool
    reason_codes: tuple[str, ...]
    dashboard_safe: bool = True
    runtime_mutation_allowed: bool = False
    canonical_write_allowed: bool = False

    def __post_init__(self) -> None:
        if not self.backend_id:
            raise ValueError("backend_id must not be empty")
        if not self.artifact_ref:
            raise ValueError("artifact_ref must not be empty")
        if not self.object_storage_ready:
            raise ValueError("object_storage_ready must remain true")
        if not isinstance(self.reason_codes, tuple):
            raise TypeError("reason_codes must be a tuple")
        if not self.reason_codes:
            raise ValueError("reason_codes must not be empty")
        if not self.dashboard_safe:
            raise ValueError("dashboard_safe must remain true")
        if self.runtime_mutation_allowed:
            raise ValueError("runtime_mutation_allowed must remain false")
        if self.canonical_write_allowed:
            raise ValueError("canonical_write_allowed must remain false")
