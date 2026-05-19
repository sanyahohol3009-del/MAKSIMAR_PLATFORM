from __future__ import annotations

from dataclasses import asdict, dataclass
from enum import Enum
from typing import Any


class DataPlanePayloadReferenceKind(str, Enum):
    STORAGE_BACKEND = "storage_backend"
    OBJECT_ARTIFACT = "object_artifact"
    VECTOR_RECORD = "vector_record"
    MEMORY_INDEX_ENTRY = "memory_index_entry"


@dataclass(frozen=True, slots=True)
class DataPlanePayloadReference:
    reference_id: str
    reference_kind: DataPlanePayloadReferenceKind
    uri: str
    sha256: str
    size_bytes: int
    producer_layer_id: str
    trace_id: str
    backend_id: str
    content_type: str
    dashboard_safe: bool = True
    heavy_payload_inline_allowed: bool = False
    control_path_payload_allowed: bool = False
    runtime_mutation_allowed: bool = False
    canonical_write_allowed: bool = False

    def __post_init__(self) -> None:
        for field_name, value in (
            ("reference_id", self.reference_id),
            ("uri", self.uri),
            ("sha256", self.sha256),
            ("producer_layer_id", self.producer_layer_id),
            ("trace_id", self.trace_id),
            ("backend_id", self.backend_id),
            ("content_type", self.content_type),
        ):
            if not value:
                raise ValueError(f"{field_name} must not be empty")

        if not isinstance(self.reference_kind, DataPlanePayloadReferenceKind):
            raise TypeError("reference_kind must be DataPlanePayloadReferenceKind")

        if self.size_bytes < 0:
            raise ValueError("size_bytes must not be negative")

        if len(self.sha256) != 64:
            raise ValueError("sha256 must be a 64-character sha256 hex string")
        int(self.sha256, 16)

        if not self.dashboard_safe:
            raise ValueError("dashboard_safe must remain true")
        if self.heavy_payload_inline_allowed:
            raise ValueError("heavy_payload_inline_allowed must remain false")
        if self.control_path_payload_allowed:
            raise ValueError("control_path_payload_allowed must remain false")
        if self.runtime_mutation_allowed:
            raise ValueError("runtime_mutation_allowed must remain false")
        if self.canonical_write_allowed:
            raise ValueError("canonical_write_allowed must remain false")

    def to_dict(self) -> dict[str, Any]:
        payload = asdict(self)
        payload["reference_kind"] = self.reference_kind.value
        return payload
