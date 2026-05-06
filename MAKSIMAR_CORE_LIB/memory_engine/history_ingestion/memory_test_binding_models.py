from __future__ import annotations

from dataclasses import dataclass


def _ensure_non_empty_str(value: str, field_name: str) -> str:
    normalized = value.strip()
    if not normalized:
        raise ValueError(f"{field_name} must be a non-empty string")
    return normalized


@dataclass(frozen=True)
class MemoryTestBinding:
    memory_id: str
    test_ref: str
    binding_ready: bool

    def __post_init__(self) -> None:
        memory_id = _ensure_non_empty_str(self.memory_id, "memory_id")
        test_ref = _ensure_non_empty_str(self.test_ref, "test_ref")

        if not self.binding_ready:
            raise ValueError("binding_ready must be True")

        object.__setattr__(self, "memory_id", memory_id)
        object.__setattr__(self, "test_ref", test_ref)
