from __future__ import annotations

from dataclasses import dataclass
from typing import Any


CANONICAL_WORKER_IDS: tuple[str, ...] = (
    "worker_ai_001",
    "worker_sim_001",
    "worker_voice_001",
)


@dataclass(frozen=True, slots=True)
class WorkerAliasBinding:
    alias_worker_id: str
    canonical_worker_id: str

    def __post_init__(self) -> None:
        _require_non_empty(self.alias_worker_id, "alias_worker_id")
        _require_non_empty(self.canonical_worker_id, "canonical_worker_id")
        if self.alias_worker_id == self.canonical_worker_id:
            raise ValueError("worker alias must not point to itself")

    def to_read_model(self) -> dict[str, str]:
        return {
            "alias_worker_id": self.alias_worker_id,
            "canonical_worker_id": self.canonical_worker_id,
        }


@dataclass(frozen=True, slots=True)
class WorkerAliasBindingContract:
    canonical_worker_ids: tuple[str, ...]
    alias_bindings: tuple[WorkerAliasBinding, ...]

    def __post_init__(self) -> None:
        _require_non_empty_tuple(self.canonical_worker_ids, "canonical_worker_ids")
        if len(set(self.canonical_worker_ids)) != len(self.canonical_worker_ids):
            raise ValueError("canonical_worker_ids must be unique")
        for canonical_worker_id in self.canonical_worker_ids:
            _require_non_empty(canonical_worker_id, "canonical_worker_ids")
        _reject_alias_loops(self.alias_bindings)
        for binding in self.alias_bindings:
            if binding.alias_worker_id in self.canonical_worker_ids:
                raise ValueError("alias_worker_id must not be a canonical worker id")
            if binding.canonical_worker_id not in self.canonical_worker_ids:
                raise ValueError("alias points to an unknown canonical worker id")

    def resolve_worker_id(self, worker_id: str) -> str:
        _require_non_empty(worker_id, "worker_id")
        if worker_id in self.canonical_worker_ids:
            return worker_id
        alias_map = {
            binding.alias_worker_id: binding.canonical_worker_id
            for binding in self.alias_bindings
        }
        if worker_id not in alias_map:
            raise ValueError(f"unknown worker id: {worker_id}")
        return alias_map[worker_id]

    def to_read_model(self) -> dict[str, Any]:
        return {
            "canonical_worker_ids": self.canonical_worker_ids,
            "alias_bindings": tuple(binding.to_read_model() for binding in self.alias_bindings),
            "alias_count": len(self.alias_bindings),
        }


def _reject_alias_loops(alias_bindings: tuple[WorkerAliasBinding, ...]) -> None:
    alias_map = {
        binding.alias_worker_id: binding.canonical_worker_id
        for binding in alias_bindings
    }
    if len(alias_map) != len(alias_bindings):
        raise ValueError("alias_worker_id values must be unique")
    for alias_worker_id in alias_map:
        seen: set[str] = set()
        current = alias_worker_id
        while current in alias_map:
            if current in seen:
                raise ValueError("worker alias loop is not allowed")
            seen.add(current)
            current = alias_map[current]


def _require_non_empty(value: str, field_name: str) -> None:
    if not isinstance(value, str) or not value.strip():
        raise ValueError(f"{field_name} must be a non-empty string")


def _require_non_empty_tuple(value: tuple[str, ...], field_name: str) -> None:
    if not isinstance(value, tuple) or not value:
        raise ValueError(f"{field_name} must be a non-empty tuple")


DEFAULT_WORKER_ALIAS_BINDINGS: tuple[WorkerAliasBinding, ...] = (
    WorkerAliasBinding(
        alias_worker_id="worker_simulation_analysis_001",
        canonical_worker_id="worker_sim_001",
    ),
)


def build_worker_alias_binding_contract() -> WorkerAliasBindingContract:
    return WorkerAliasBindingContract(
        canonical_worker_ids=CANONICAL_WORKER_IDS,
        alias_bindings=DEFAULT_WORKER_ALIAS_BINDINGS,
    )


def resolve_worker_alias(worker_id: str) -> str:
    return build_worker_alias_binding_contract().resolve_worker_id(worker_id)
