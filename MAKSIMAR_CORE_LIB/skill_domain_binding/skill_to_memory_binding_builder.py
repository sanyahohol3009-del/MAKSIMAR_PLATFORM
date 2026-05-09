from __future__ import annotations

import re
from dataclasses import dataclass
from typing import Literal


MemoryBindingStatus = Literal["bound", "not_required"]

_BINDING_ID_PATTERN = re.compile(r"^skill_to_memory_binding_[a-z][a-z0-9_]*$")


def _ensure_non_empty_str(value: str, field_name: str) -> str:
    if not isinstance(value, str):
        raise ValueError(f"{field_name} must be a string")
    normalized = value.strip()
    if not normalized:
        raise ValueError(f"{field_name} must be a non-empty string")
    return normalized


def _ensure_non_negative_int(value: int, field_name: str) -> int:
    if not isinstance(value, int):
        raise ValueError(f"{field_name} must be an int")
    if value < 0:
        raise ValueError(f"{field_name} must be >= 0")
    return value


def _ensure_bool(value: bool, field_name: str) -> bool:
    if not isinstance(value, bool):
        raise ValueError(f"{field_name} must be bool")
    return value


def safe_id_suffix(value: str) -> str:
    suffix = re.sub(r"[^a-zA-Z0-9_]+", "_", value.strip().lower()).strip("_")
    if not suffix:
        raise ValueError("id suffix must be non-empty")
    if not suffix[0].isalpha():
        suffix = f"item_{suffix}"
    return suffix


@dataclass(frozen=True, slots=True)
class SkillToMemoryBindingEntry:
    binding_id: str
    skill_id: str
    module_slug: str
    memory_tier_id: str
    memory_binding_required: bool
    memory_reference_bound: bool
    evidence_required: bool
    conflict_resolution_required: bool
    binding_status: MemoryBindingStatus
    read_only: bool
    binding_ready: bool

    def __post_init__(self) -> None:
        binding_id = _ensure_non_empty_str(self.binding_id, "binding_id")
        skill_id = _ensure_non_empty_str(self.skill_id, "skill_id")
        module_slug = _ensure_non_empty_str(self.module_slug, "module_slug")

        if not isinstance(self.memory_tier_id, str):
            raise ValueError("memory_tier_id must be a string")
        memory_tier_id = self.memory_tier_id.strip()

        if not _BINDING_ID_PATTERN.fullmatch(binding_id):
            raise ValueError(f"Invalid binding_id: {binding_id}")

        for field_name in (
            "memory_binding_required",
            "memory_reference_bound",
            "evidence_required",
            "conflict_resolution_required",
            "read_only",
            "binding_ready",
        ):
            _ensure_bool(getattr(self, field_name), field_name)

        if self.memory_binding_required and not memory_tier_id:
            raise ValueError("required memory binding must have memory_tier_id")
        if self.memory_binding_required and not self.memory_reference_bound:
            raise ValueError("required memory binding must be reference-bound")
        if self.binding_status == "bound" and not self.memory_reference_bound:
            raise ValueError("bound status requires memory_reference_bound")
        if self.binding_status == "not_required" and self.memory_binding_required:
            raise ValueError("not_required status cannot require memory binding")
        if not self.evidence_required:
            raise ValueError("evidence_required must be True")
        if not self.conflict_resolution_required:
            raise ValueError("conflict_resolution_required must be True")
        if not self.read_only:
            raise ValueError("read_only must be True")
        if not self.binding_ready:
            raise ValueError("binding_ready must be True")

        object.__setattr__(self, "binding_id", binding_id)
        object.__setattr__(self, "skill_id", skill_id)
        object.__setattr__(self, "module_slug", module_slug)
        object.__setattr__(self, "memory_tier_id", memory_tier_id)


@dataclass(frozen=True, slots=True)
class SkillToMemoryBindingContract:
    total_bindings: int
    ready_bindings: int
    memory_required_bindings: int
    memory_reference_bound_bindings: int
    non_memory_backed_bindings: int
    read_only_bindings: int
    entries: tuple[SkillToMemoryBindingEntry, ...]

    def __post_init__(self) -> None:
        total_bindings = _ensure_non_negative_int(
            self.total_bindings,
            "total_bindings",
        )
        if total_bindings != len(self.entries):
            raise ValueError("total_bindings must match entries length")
        if total_bindings <= 0:
            raise ValueError("total_bindings must be >= 1")

        computed_ready = sum(1 for entry in self.entries if entry.binding_ready)
        computed_required = sum(
            1 for entry in self.entries if entry.memory_binding_required
        )
        computed_bound = sum(1 for entry in self.entries if entry.memory_reference_bound)
        computed_non_memory = sum(
            1 for entry in self.entries if not entry.memory_binding_required
        )
        computed_read_only = sum(1 for entry in self.entries if entry.read_only)

        expected = {
            "ready_bindings": computed_ready,
            "memory_required_bindings": computed_required,
            "memory_reference_bound_bindings": computed_bound,
            "non_memory_backed_bindings": computed_non_memory,
            "read_only_bindings": computed_read_only,
        }

        for field_name, expected_value in expected.items():
            if getattr(self, field_name) != expected_value:
                raise ValueError(f"{field_name} must match computed count")

        if self.ready_bindings != total_bindings:
            raise ValueError("all skill-to-memory bindings must be ready")
        if self.read_only_bindings != total_bindings:
            raise ValueError("all skill-to-memory bindings must be read-only")

        binding_ids = tuple(entry.binding_id for entry in self.entries)
        if len(set(binding_ids)) != len(binding_ids):
            raise ValueError("duplicate skill-to-memory binding ids detected")


def build_skill_to_memory_binding_contract() -> SkillToMemoryBindingContract:
    from MAKSIMAR_CORE_LIB.skill_domain_binding.skill_binding_models import (
        build_skill_binding_contract,
    )

    skills = build_skill_binding_contract()

    entries = tuple(
        SkillToMemoryBindingEntry(
            binding_id=f"skill_to_memory_binding_{safe_id_suffix(skill.skill_id)}",
            skill_id=skill.skill_id,
            module_slug=skill.module_slug,
            memory_tier_id=skill.memory_tier_id,
            memory_binding_required=bool(skill.memory_tier_id),
            memory_reference_bound=skill.memory_reference_bound,
            evidence_required=True,
            conflict_resolution_required=True,
            binding_status="bound" if skill.memory_reference_bound else "not_required",
            read_only=True,
            binding_ready=True,
        )
        for skill in skills.entries
    )

    return SkillToMemoryBindingContract(
        total_bindings=len(entries),
        ready_bindings=sum(1 for entry in entries if entry.binding_ready),
        memory_required_bindings=sum(
            1 for entry in entries if entry.memory_binding_required
        ),
        memory_reference_bound_bindings=sum(
            1 for entry in entries if entry.memory_reference_bound
        ),
        non_memory_backed_bindings=sum(
            1 for entry in entries if not entry.memory_binding_required
        ),
        read_only_bindings=sum(1 for entry in entries if entry.read_only),
        entries=entries,
    )
