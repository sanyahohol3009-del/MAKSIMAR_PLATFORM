from __future__ import annotations

from dataclasses import asdict, dataclass
from enum import Enum
from typing import Any


class VectorStoreBackendKind(str, Enum):
    QDRANT = "qdrant"
    SQLITE_VEC = "sqlite_vec"
    CONTRACT_ONLY = "contract_only"


@dataclass(frozen=True, slots=True)
class VectorStoreReference:
    vector_ref: str
    vector_store_id: str
    namespace_id: str
    backend_kind: VectorStoreBackendKind
    embedding_model_ref: str
    dimension: int
    metadata_ref: str
    payload_ref: str
    producer_layer_id: str
    trace_id: str
    dashboard_safe: bool = True
    vector_payload_inline_allowed: bool = False
    backend_runtime_enabled: bool = False
    runtime_mutation_allowed: bool = False
    canonical_write_allowed: bool = False

    def __post_init__(self) -> None:
        for field_name, value in (
            ("vector_ref", self.vector_ref),
            ("vector_store_id", self.vector_store_id),
            ("namespace_id", self.namespace_id),
            ("embedding_model_ref", self.embedding_model_ref),
            ("metadata_ref", self.metadata_ref),
            ("payload_ref", self.payload_ref),
            ("producer_layer_id", self.producer_layer_id),
            ("trace_id", self.trace_id),
        ):
            if not value:
                raise ValueError(f"{field_name} must not be empty")
        if not isinstance(self.backend_kind, VectorStoreBackendKind):
            raise TypeError("backend_kind must be VectorStoreBackendKind")
        if self.dimension <= 0:
            raise ValueError("dimension must be positive")
        if not self.dashboard_safe:
            raise ValueError("dashboard_safe must remain true")
        if self.vector_payload_inline_allowed:
            raise ValueError("vector_payload_inline_allowed must remain false")
        if self.backend_runtime_enabled:
            raise ValueError("backend_runtime_enabled must remain false in contract layer")
        if self.runtime_mutation_allowed:
            raise ValueError("runtime_mutation_allowed must remain false")
        if self.canonical_write_allowed:
            raise ValueError("canonical_write_allowed must remain false")

    def to_dict(self) -> dict[str, Any]:
        payload = asdict(self)
        payload["backend_kind"] = self.backend_kind.value
        return payload


@dataclass(frozen=True, slots=True)
class VectorStoreReadinessReadModel:
    vector_store_id: str
    backend_kind: str
    namespace_id: str
    dimension: int
    reason_codes: tuple[str, ...]
    dashboard_safe: bool = True
    backend_runtime_enabled: bool = False
    runtime_mutation_allowed: bool = False
    canonical_write_allowed: bool = False

    def __post_init__(self) -> None:
        for field_name, value in (
            ("vector_store_id", self.vector_store_id),
            ("backend_kind", self.backend_kind),
            ("namespace_id", self.namespace_id),
        ):
            if not value:
                raise ValueError(f"{field_name} must not be empty")
        if self.dimension <= 0:
            raise ValueError("dimension must be positive")
        if not isinstance(self.reason_codes, tuple):
            raise TypeError("reason_codes must be a tuple")
        if not self.reason_codes:
            raise ValueError("reason_codes must not be empty")
        if not self.dashboard_safe:
            raise ValueError("dashboard_safe must remain true")
        if self.backend_runtime_enabled:
            raise ValueError("backend_runtime_enabled must remain false in contract layer")
        if self.runtime_mutation_allowed:
            raise ValueError("runtime_mutation_allowed must remain false")
        if self.canonical_write_allowed:
            raise ValueError("canonical_write_allowed must remain false")
