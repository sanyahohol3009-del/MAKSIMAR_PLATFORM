from __future__ import annotations

import re
from dataclasses import dataclass

from MAKSIMAR_CORE_LIB.module_manifest import (
    ModuleKind,
    build_module_manifest_schema_contract,
)


_MODULE_ID_PATTERN = re.compile(r"^module_(skill|memory_tier|extension_cube)_[a-z][a-z0-9_]*$")
_SKILL_ID_PATTERN = re.compile(r"^skill_[a-z][a-z0-9_]*_[a-z][a-z0-9_]*$")
_MEMORY_TIER_ID_PATTERN = re.compile(r"^memory_[a-z][a-z0-9_]*$")
_WORKER_ID_PATTERN = re.compile(r"^worker_[a-z][a-z0-9_]*_001$")
_PANEL_ID_PATTERN = re.compile(r"^panel_[a-z][a-z0-9_]*$")
_ARTIFACT_REF_PREFIX_PATTERN = re.compile(r"^artifact://modules/[a-z][a-z0-9_]*$")
_TRACE_ID_PREFIX_PATTERN = re.compile(r"^trace_[a-z][a-z0-9_]*$")


def _view_id_to_panel_id(view_id: str) -> str:
    """Convert canonical view_id to canonical panel_id."""
    if not view_id.startswith("view_"):
        raise ValueError(f"view_id must start with 'view_': {view_id}")

    view_suffix = view_id.removeprefix("view_")
    return f"panel_{view_suffix}"


@dataclass(frozen=True, slots=True)
class CanonicalIdAllocationEntry:
    """Canonical ID allocation entry for extensible modules."""

    module_kind: ModuleKind
    module_slug: str
    module_id: str
    skill_id: str
    memory_tier_id: str
    worker_id: str
    panel_ids: tuple[str, ...]
    artifact_ref_prefix: str
    trace_id_prefix: str
    collision_free: bool

    def __post_init__(self) -> None:
        """Validate canonical ID allocation invariants."""
        if not self.module_slug.strip():
            raise ValueError("module_slug must not be empty")

        if not _MODULE_ID_PATTERN.fullmatch(self.module_id):
            raise ValueError(f"Invalid module_id: {self.module_id}")

        if not _ARTIFACT_REF_PREFIX_PATTERN.fullmatch(self.artifact_ref_prefix):
            raise ValueError(
                f"Invalid artifact_ref_prefix: {self.artifact_ref_prefix}"
            )

        if not _TRACE_ID_PREFIX_PATTERN.fullmatch(self.trace_id_prefix):
            raise ValueError(f"Invalid trace_id_prefix: {self.trace_id_prefix}")

        if len(set(self.panel_ids)) != len(self.panel_ids):
            raise ValueError(f"Duplicate panel_ids detected for {self.module_slug}")

        for panel_id in self.panel_ids:
            if not _PANEL_ID_PATTERN.fullmatch(panel_id):
                raise ValueError(f"Invalid panel_id: {panel_id}")

        if self.module_kind == "skill":
            if not self.skill_id:
                raise ValueError(
                    f"skill manifest must allocate skill_id: {self.module_slug}"
                )
            if not _SKILL_ID_PATTERN.fullmatch(self.skill_id):
                raise ValueError(f"Invalid skill_id: {self.skill_id}")
            if not self.worker_id:
                raise ValueError(
                    f"skill manifest must allocate worker_id: {self.module_slug}"
                )
            if not _WORKER_ID_PATTERN.fullmatch(self.worker_id):
                raise ValueError(f"Invalid worker_id: {self.worker_id}")
            if self.memory_tier_id != "":
                raise ValueError(
                    f"skill manifest must not allocate memory_tier_id: {self.module_slug}"
                )

        if self.module_kind == "memory_tier":
            if not self.memory_tier_id:
                raise ValueError(
                    f"memory_tier manifest must allocate memory_tier_id: {self.module_slug}"
                )
            if not _MEMORY_TIER_ID_PATTERN.fullmatch(self.memory_tier_id):
                raise ValueError(f"Invalid memory_tier_id: {self.memory_tier_id}")
            if self.skill_id != "":
                raise ValueError(
                    f"memory_tier manifest must not allocate skill_id: {self.module_slug}"
                )
            if self.worker_id != "":
                raise ValueError(
                    f"memory_tier manifest must not allocate worker_id: {self.module_slug}"
                )

        if self.module_kind == "extension_cube":
            if self.skill_id != "":
                raise ValueError(
                    f"extension_cube manifest must not allocate skill_id: {self.module_slug}"
                )
            if self.memory_tier_id != "":
                raise ValueError(
                    f"extension_cube manifest must not allocate memory_tier_id: {self.module_slug}"
                )
            if self.worker_id != "":
                raise ValueError(
                    f"extension_cube manifest must not allocate worker_id: {self.module_slug}"
                )

        if not self.collision_free:
            raise ValueError(
                f"collision_free must be True for allocated entry: {self.module_slug}"
            )


@dataclass(frozen=True, slots=True)
class CanonicalIdGenerationContract:
    """Unified canonical ID generation contract."""

    total_entries: int
    total_skill_ids: int
    total_memory_tier_ids: int
    total_worker_ids: int
    total_panel_ids: int
    entries: tuple[CanonicalIdAllocationEntry, ...]

    def __post_init__(self) -> None:
        """Validate canonical ID generation contract invariants."""
        if self.total_entries != len(self.entries):
            raise ValueError("total_entries must match entries length")

        computed_skill_ids = sum(1 for entry in self.entries if entry.skill_id != "")
        computed_memory_tier_ids = sum(
            1 for entry in self.entries if entry.memory_tier_id != ""
        )
        computed_worker_ids = sum(1 for entry in self.entries if entry.worker_id != "")
        computed_panel_ids = sum(len(entry.panel_ids) for entry in self.entries)

        if self.total_skill_ids != computed_skill_ids:
            raise ValueError("total_skill_ids must match computed count")

        if self.total_memory_tier_ids != computed_memory_tier_ids:
            raise ValueError("total_memory_tier_ids must match computed count")

        if self.total_worker_ids != computed_worker_ids:
            raise ValueError("total_worker_ids must match computed count")

        if self.total_panel_ids != computed_panel_ids:
            raise ValueError("total_panel_ids must match computed count")

        module_ids = tuple(entry.module_id for entry in self.entries)
        skill_ids = tuple(entry.skill_id for entry in self.entries if entry.skill_id)
        memory_tier_ids = tuple(
            entry.memory_tier_id for entry in self.entries if entry.memory_tier_id
        )
        worker_ids = tuple(entry.worker_id for entry in self.entries if entry.worker_id)
        panel_ids = tuple(
            panel_id
            for entry in self.entries
            for panel_id in entry.panel_ids
        )
        artifact_ref_prefixes = tuple(
            entry.artifact_ref_prefix for entry in self.entries
        )
        trace_id_prefixes = tuple(entry.trace_id_prefix for entry in self.entries)

        if len(set(module_ids)) != len(module_ids):
            raise ValueError("Duplicate module_ids detected")

        if len(set(skill_ids)) != len(skill_ids):
            raise ValueError("Duplicate skill_ids detected")

        if len(set(memory_tier_ids)) != len(memory_tier_ids):
            raise ValueError("Duplicate memory_tier_ids detected")

        if len(set(worker_ids)) != len(worker_ids):
            raise ValueError("Duplicate worker_ids detected")

        if len(set(panel_ids)) != len(panel_ids):
            raise ValueError("Duplicate panel_ids detected")

        if len(set(artifact_ref_prefixes)) != len(artifact_ref_prefixes):
            raise ValueError("Duplicate artifact_ref_prefix values detected")

        if len(set(trace_id_prefixes)) != len(trace_id_prefixes):
            raise ValueError("Duplicate trace_id_prefix values detected")


def build_canonical_id_generation_contract() -> CanonicalIdGenerationContract:
    """Build canonical ID generation contract from manifest schema."""
    manifest_contract = build_module_manifest_schema_contract()

    entries = []
    for manifest in manifest_contract.manifests:
        module_id = f"module_{manifest.module_kind}_{manifest.module_slug}"
        skill_id = ""
        memory_tier_id = ""
        worker_id = ""

        if manifest.module_kind == "skill":
            skill_id = f"skill_{manifest.domain_class}_{manifest.module_slug}"
            if manifest.engine_adapter_required and manifest.active:
                worker_id = f"worker_{manifest.module_slug}_001"

        if manifest.module_kind == "memory_tier":
            memory_tier_id = f"memory_{manifest.module_slug}"

        panel_ids = tuple(
            _view_id_to_panel_id(view_id)
            for view_id in manifest.dashboard_view_ids
        )

        artifact_ref_prefix = f"artifact://modules/{manifest.module_slug}"
        trace_id_prefix = f"trace_{manifest.module_slug}"

        entries.append(
            CanonicalIdAllocationEntry(
                module_kind=manifest.module_kind,
                module_slug=manifest.module_slug,
                module_id=module_id,
                skill_id=skill_id,
                memory_tier_id=memory_tier_id,
                worker_id=worker_id,
                panel_ids=panel_ids,
                artifact_ref_prefix=artifact_ref_prefix,
                trace_id_prefix=trace_id_prefix,
                collision_free=True,
            )
        )

    total_skill_ids = sum(1 for entry in entries if entry.skill_id != "")
    total_memory_tier_ids = sum(
        1 for entry in entries if entry.memory_tier_id != ""
    )
    total_worker_ids = sum(1 for entry in entries if entry.worker_id != "")
    total_panel_ids = sum(len(entry.panel_ids) for entry in entries)

    return CanonicalIdGenerationContract(
        total_entries=len(entries),
        total_skill_ids=total_skill_ids,
        total_memory_tier_ids=total_memory_tier_ids,
        total_worker_ids=total_worker_ids,
        total_panel_ids=total_panel_ids,
        entries=tuple(entries),
    )
