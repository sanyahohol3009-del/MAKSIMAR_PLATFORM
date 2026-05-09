from __future__ import annotations

import re
from dataclasses import dataclass


_BINDING_ID_PATTERN = re.compile(r"^skill_to_retrieval_binding_[a-z][a-z0-9_]*$")


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
class SkillToRetrievalBindingEntry:
    binding_id: str
    skill_id: str
    module_slug: str
    selected_source_count: int
    evidence_item_count: int
    retrieval_reference_bound: bool
    retrieval_phase_ready: bool
    backend_execution_allowed: bool
    mgrep_blocked: bool
    sqlite_vec_blocked: bool
    read_only: bool
    binding_ready: bool

    def __post_init__(self) -> None:
        binding_id = _ensure_non_empty_str(self.binding_id, "binding_id")
        skill_id = _ensure_non_empty_str(self.skill_id, "skill_id")
        module_slug = _ensure_non_empty_str(self.module_slug, "module_slug")

        if not _BINDING_ID_PATTERN.fullmatch(binding_id):
            raise ValueError(f"Invalid binding_id: {binding_id}")

        _ensure_non_negative_int(self.selected_source_count, "selected_source_count")
        _ensure_non_negative_int(self.evidence_item_count, "evidence_item_count")

        for field_name in (
            "retrieval_reference_bound",
            "retrieval_phase_ready",
            "backend_execution_allowed",
            "mgrep_blocked",
            "sqlite_vec_blocked",
            "read_only",
            "binding_ready",
        ):
            _ensure_bool(getattr(self, field_name), field_name)

        if self.selected_source_count <= 0:
            raise ValueError("selected_source_count must be >= 1")
        if self.evidence_item_count <= 0:
            raise ValueError("evidence_item_count must be >= 1")
        if not self.retrieval_reference_bound:
            raise ValueError("retrieval_reference_bound must be True")
        if not self.retrieval_phase_ready:
            raise ValueError("retrieval_phase_ready must be True")
        if self.backend_execution_allowed:
            raise ValueError("backend_execution_allowed must be False")
        if not self.mgrep_blocked:
            raise ValueError("mgrep_blocked must be True")
        if not self.sqlite_vec_blocked:
            raise ValueError("sqlite_vec_blocked must be True")
        if not self.read_only:
            raise ValueError("read_only must be True")
        if not self.binding_ready:
            raise ValueError("binding_ready must be True")

        object.__setattr__(self, "binding_id", binding_id)
        object.__setattr__(self, "skill_id", skill_id)
        object.__setattr__(self, "module_slug", module_slug)


@dataclass(frozen=True, slots=True)
class SkillToRetrievalBindingContract:
    total_bindings: int
    ready_bindings: int
    retrieval_reference_bound_bindings: int
    backend_execution_allowed_bindings: int
    mgrep_blocked_bindings: int
    sqlite_vec_blocked_bindings: int
    read_only_bindings: int
    entries: tuple[SkillToRetrievalBindingEntry, ...]

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
        computed_retrieval = sum(
            1 for entry in self.entries if entry.retrieval_reference_bound
        )
        computed_backend = sum(
            1 for entry in self.entries if entry.backend_execution_allowed
        )
        computed_mgrep = sum(1 for entry in self.entries if entry.mgrep_blocked)
        computed_sqlite = sum(1 for entry in self.entries if entry.sqlite_vec_blocked)
        computed_read_only = sum(1 for entry in self.entries if entry.read_only)

        expected = {
            "ready_bindings": computed_ready,
            "retrieval_reference_bound_bindings": computed_retrieval,
            "backend_execution_allowed_bindings": computed_backend,
            "mgrep_blocked_bindings": computed_mgrep,
            "sqlite_vec_blocked_bindings": computed_sqlite,
            "read_only_bindings": computed_read_only,
        }

        for field_name, expected_value in expected.items():
            if getattr(self, field_name) != expected_value:
                raise ValueError(f"{field_name} must match computed count")

        if self.ready_bindings != total_bindings:
            raise ValueError("all skill-to-retrieval bindings must be ready")
        if self.retrieval_reference_bound_bindings != total_bindings:
            raise ValueError("all skills must be retrieval-bound")
        if self.backend_execution_allowed_bindings != 0:
            raise ValueError("backend execution must remain disabled")
        if self.mgrep_blocked_bindings != total_bindings:
            raise ValueError("mgrep must remain blocked for all bindings")
        if self.sqlite_vec_blocked_bindings != total_bindings:
            raise ValueError("sqlite-vec must remain blocked for all bindings")
        if self.read_only_bindings != total_bindings:
            raise ValueError("all skill-to-retrieval bindings must be read-only")


def build_skill_to_retrieval_binding_contract() -> SkillToRetrievalBindingContract:
    from MAKSIMAR_CORE_LIB.skill_domain_binding.skill_binding_models import (
        build_skill_binding_contract,
    )
    from MAKSIMAR_SERVER.CONTROL_PLANE.memory_routing import (
        build_retrieval_phase_readiness,
    )

    skills = build_skill_binding_contract()
    retrieval = build_retrieval_phase_readiness()

    entries = tuple(
        SkillToRetrievalBindingEntry(
            binding_id=f"skill_to_retrieval_binding_{safe_id_suffix(skill.skill_id)}",
            skill_id=skill.skill_id,
            module_slug=skill.module_slug,
            selected_source_count=retrieval.selected_source_count,
            evidence_item_count=retrieval.evidence_item_count,
            retrieval_reference_bound=skill.retrieval_reference_bound,
            retrieval_phase_ready=retrieval.phase_ready,
            backend_execution_allowed=retrieval.backend_execution_allowed,
            mgrep_blocked=retrieval.mgrep_blocked,
            sqlite_vec_blocked=retrieval.sqlite_vec_blocked,
            read_only=True,
            binding_ready=(
                skill.retrieval_reference_bound
                and retrieval.phase_ready
                and not retrieval.backend_execution_allowed
                and retrieval.mgrep_blocked
                and retrieval.sqlite_vec_blocked
            ),
        )
        for skill in skills.entries
    )

    return SkillToRetrievalBindingContract(
        total_bindings=len(entries),
        ready_bindings=sum(1 for entry in entries if entry.binding_ready),
        retrieval_reference_bound_bindings=sum(
            1 for entry in entries if entry.retrieval_reference_bound
        ),
        backend_execution_allowed_bindings=sum(
            1 for entry in entries if entry.backend_execution_allowed
        ),
        mgrep_blocked_bindings=sum(1 for entry in entries if entry.mgrep_blocked),
        sqlite_vec_blocked_bindings=sum(
            1 for entry in entries if entry.sqlite_vec_blocked
        ),
        read_only_bindings=sum(1 for entry in entries if entry.read_only),
        entries=entries,
    )
