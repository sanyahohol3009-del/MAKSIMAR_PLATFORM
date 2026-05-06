from __future__ import annotations

from dataclasses import dataclass

from MAKSIMAR_CORE_LIB.memory_engine.history_ingestion.memory_object_models import (
    MemoryObject,
)


def _ensure_non_empty_str(value: str, field_name: str) -> str:
    normalized = value.strip()
    if not normalized:
        raise ValueError(f"{field_name} must be a non-empty string")
    return normalized


@dataclass(frozen=True)
class NormalizedHistoryRecord:
    record_id: str
    memory_object: MemoryObject
    storage_node_id: str
    write_path: str
    readable_by_jarvis: bool
    canonical_truth: bool
    deterministic_output: bool
    parallel_safe_by_design: bool

    def __post_init__(self) -> None:
        record_id = _ensure_non_empty_str(self.record_id, "record_id")
        storage_node_id = _ensure_non_empty_str(self.storage_node_id, "storage_node_id")
        write_path = _ensure_non_empty_str(self.write_path, "write_path")

        if self.canonical_truth:
            raise ValueError("canonical_truth must be False for normalized history")

        if not self.readable_by_jarvis:
            raise ValueError("readable_by_jarvis must be True")

        if not self.deterministic_output:
            raise ValueError("deterministic_output must be True")

        if not self.parallel_safe_by_design:
            raise ValueError("parallel_safe_by_design must be True")

        object.__setattr__(self, "record_id", record_id)
        object.__setattr__(self, "storage_node_id", storage_node_id)
        object.__setattr__(self, "write_path", write_path)
