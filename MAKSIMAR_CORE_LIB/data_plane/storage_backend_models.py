from __future__ import annotations

from dataclasses import asdict, dataclass
from enum import Enum
from typing import Any


POSTGRES_MAIN_BACKEND_MARKER = "postgres_main"


class StorageBackendKind(str, Enum):
    POSTGRES_MAIN = "postgres_main"
    OBJECT_STORAGE = "object_storage"
    VECTOR_STORE = "vector_store"
    MEMORY_INDEX = "memory_index"
    LOCAL_APPEND_LOG = "local_append_log"


class StorageBackendStatus(str, Enum):
    READY = "ready"
    POLICY_GATED = "policy_gated"
    DISABLED = "disabled"


@dataclass(frozen=True, slots=True)
class StorageBackendDescriptor:
    backend_id: str
    backend_kind: StorageBackendKind
    status: StorageBackendStatus
    endpoint_ref: str
    capability_ids: tuple[str, ...]
    reason_codes: tuple[str, ...]
    dashboard_safe: bool = True
    runtime_mutation_allowed: bool = False
    canonical_write_allowed: bool = False
    heavy_payload_in_control_path_allowed: bool = False

    def __post_init__(self) -> None:
        for field_name, value in (
            ("backend_id", self.backend_id),
            ("endpoint_ref", self.endpoint_ref),
        ):
            if not value:
                raise ValueError(f"{field_name} must not be empty")

        if not isinstance(self.backend_kind, StorageBackendKind):
            raise TypeError("backend_kind must be StorageBackendKind")
        if not isinstance(self.status, StorageBackendStatus):
            raise TypeError("status must be StorageBackendStatus")

        for field_name, values in (
            ("capability_ids", self.capability_ids),
            ("reason_codes", self.reason_codes),
        ):
            if not isinstance(values, tuple):
                raise TypeError(f"{field_name} must be a tuple")
            if not values:
                raise ValueError(f"{field_name} must not be empty")
            for value in values:
                if not value:
                    raise ValueError(f"{field_name} must not contain empty values")

        if not self.dashboard_safe:
            raise ValueError("dashboard_safe must remain true")
        if self.runtime_mutation_allowed:
            raise ValueError("runtime_mutation_allowed must remain false")
        if self.canonical_write_allowed:
            raise ValueError("canonical_write_allowed must remain false")
        if self.heavy_payload_in_control_path_allowed:
            raise ValueError("heavy_payload_in_control_path_allowed must remain false")

    def to_dict(self) -> dict[str, Any]:
        payload = asdict(self)
        payload["backend_kind"] = self.backend_kind.value
        payload["status"] = self.status.value
        return payload


@dataclass(frozen=True, slots=True)
class StorageBackendReadinessReadModel:
    backend_id: str
    backend_kind: str
    status: str
    capability_count: int
    reason_codes: tuple[str, ...]
    dashboard_safe: bool = True
    runtime_mutation_allowed: bool = False
    canonical_write_allowed: bool = False
    heavy_payload_in_control_path_allowed: bool = False

    def __post_init__(self) -> None:
        for field_name, value in (
            ("backend_id", self.backend_id),
            ("backend_kind", self.backend_kind),
            ("status", self.status),
        ):
            if not value:
                raise ValueError(f"{field_name} must not be empty")
        if self.capability_count < 0:
            raise ValueError("capability_count must not be negative")
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
        if self.heavy_payload_in_control_path_allowed:
            raise ValueError("heavy_payload_in_control_path_allowed must remain false")

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)
