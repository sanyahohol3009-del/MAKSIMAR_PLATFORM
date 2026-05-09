from __future__ import annotations

import re
from dataclasses import dataclass


_SKILL_BINDING_ID_PATTERN = re.compile(r"^skill_binding_[a-z][a-z0-9_]*$")


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


def _ensure_non_empty_tuple(value: tuple[str, ...], field_name: str) -> tuple[str, ...]:
    if not isinstance(value, tuple):
        raise ValueError(f"{field_name} must be a tuple")
    if not value:
        raise ValueError(f"{field_name} must be non-empty")
    normalized = tuple(_ensure_non_empty_str(item, field_name) for item in value)
    if len(set(normalized)) != len(normalized):
        raise ValueError(f"{field_name} must contain unique values")
    return normalized


def safe_id_suffix(value: str) -> str:
    suffix = re.sub(r"[^a-zA-Z0-9_]+", "_", value.strip().lower()).strip("_")
    if not suffix:
        raise ValueError("id suffix must be non-empty")
    if not suffix[0].isalpha():
        suffix = f"item_{suffix}"
    return suffix


@dataclass(frozen=True, slots=True)
class SkillBindingEntry:
    skill_binding_id: str
    module_slug: str
    module_id: str
    skill_id: str
    worker_id: str
    domain_class: str
    policy_profile: str
    observability_profile: str
    adapter_execution_mode: str
    memory_tier_id: str
    input_contract_ids: tuple[str, ...]
    output_contract_ids: tuple[str, ...]
    panel_ids: tuple[str, ...]
    supported_languages: tuple[str, ...]
    supported_scripts: tuple[str, ...]
    manifest_bound: bool
    registry_bound: bool
    memory_reference_bound: bool
    retrieval_reference_bound: bool
    dashboard_reference_bound: bool
    engine_adapter_required: bool
    active: bool
    binding_ready: bool
    description: str

    def __post_init__(self) -> None:
        skill_binding_id = _ensure_non_empty_str(
            self.skill_binding_id,
            "skill_binding_id",
        )
        module_slug = _ensure_non_empty_str(self.module_slug, "module_slug")
        module_id = _ensure_non_empty_str(self.module_id, "module_id")
        skill_id = _ensure_non_empty_str(self.skill_id, "skill_id")
        worker_id = _ensure_non_empty_str(self.worker_id, "worker_id")
        domain_class = _ensure_non_empty_str(self.domain_class, "domain_class")
        policy_profile = _ensure_non_empty_str(self.policy_profile, "policy_profile")
        observability_profile = _ensure_non_empty_str(
            self.observability_profile,
            "observability_profile",
        )
        adapter_execution_mode = _ensure_non_empty_str(
            self.adapter_execution_mode,
            "adapter_execution_mode",
        )
        if not isinstance(self.memory_tier_id, str):
            raise ValueError("memory_tier_id must be a string")
        memory_tier_id = self.memory_tier_id.strip()
        description = _ensure_non_empty_str(self.description, "description")

        if not _SKILL_BINDING_ID_PATTERN.fullmatch(skill_binding_id):
            raise ValueError(f"Invalid skill_binding_id: {skill_binding_id}")

        input_contract_ids = _ensure_non_empty_tuple(
            self.input_contract_ids,
            "input_contract_ids",
        )
        output_contract_ids = _ensure_non_empty_tuple(
            self.output_contract_ids,
            "output_contract_ids",
        )
        panel_ids = _ensure_non_empty_tuple(self.panel_ids, "panel_ids")
        supported_languages = _ensure_non_empty_tuple(
            self.supported_languages,
            "supported_languages",
        )
        supported_scripts = _ensure_non_empty_tuple(
            self.supported_scripts,
            "supported_scripts",
        )

        for field_name in (
            "manifest_bound",
            "registry_bound",
            "memory_reference_bound",
            "retrieval_reference_bound",
            "dashboard_reference_bound",
            "engine_adapter_required",
            "active",
            "binding_ready",
        ):
            _ensure_bool(getattr(self, field_name), field_name)

        if not self.manifest_bound:
            raise ValueError("manifest_bound must be True")
        if not self.registry_bound:
            raise ValueError("registry_bound must be True")
        # Some skills are dashboard/retrieval-visible without a direct memory tier.
        # Example: simulation_analysis can be skill-bound while linked_memory_tier_id is empty.
        if not self.retrieval_reference_bound:
            raise ValueError("retrieval_reference_bound must be True")
        if not self.dashboard_reference_bound:
            raise ValueError("dashboard_reference_bound must be True")
        if not self.active:
            raise ValueError("active must be True")
        if not self.binding_ready:
            raise ValueError("binding_ready must be True")

        object.__setattr__(self, "skill_binding_id", skill_binding_id)
        object.__setattr__(self, "module_slug", module_slug)
        object.__setattr__(self, "module_id", module_id)
        object.__setattr__(self, "skill_id", skill_id)
        object.__setattr__(self, "worker_id", worker_id)
        object.__setattr__(self, "domain_class", domain_class)
        object.__setattr__(self, "policy_profile", policy_profile)
        object.__setattr__(self, "observability_profile", observability_profile)
        object.__setattr__(self, "adapter_execution_mode", adapter_execution_mode)
        object.__setattr__(self, "memory_tier_id", memory_tier_id)
        object.__setattr__(self, "input_contract_ids", input_contract_ids)
        object.__setattr__(self, "output_contract_ids", output_contract_ids)
        object.__setattr__(self, "panel_ids", panel_ids)
        object.__setattr__(self, "supported_languages", supported_languages)
        object.__setattr__(self, "supported_scripts", supported_scripts)
        object.__setattr__(self, "description", description)


@dataclass(frozen=True, slots=True)
class SkillBindingContract:
    total_bindings: int
    active_bindings: int
    ready_bindings: int
    manifest_bound_bindings: int
    registry_bound_bindings: int
    memory_reference_bound_bindings: int
    retrieval_reference_bound_bindings: int
    dashboard_reference_bound_bindings: int
    engine_adapter_required_bindings: int
    entries: tuple[SkillBindingEntry, ...]

    def __post_init__(self) -> None:
        total_bindings = _ensure_non_negative_int(
            self.total_bindings,
            "total_bindings",
        )
        if total_bindings != len(self.entries):
            raise ValueError("total_bindings must match entries length")
        if total_bindings <= 0:
            raise ValueError("total_bindings must be >= 1")

        computed_active = sum(1 for entry in self.entries if entry.active)
        computed_ready = sum(1 for entry in self.entries if entry.binding_ready)
        computed_manifest = sum(1 for entry in self.entries if entry.manifest_bound)
        computed_registry = sum(1 for entry in self.entries if entry.registry_bound)
        computed_memory = sum(1 for entry in self.entries if entry.memory_reference_bound)
        computed_retrieval = sum(
            1 for entry in self.entries if entry.retrieval_reference_bound
        )
        computed_dashboard = sum(
            1 for entry in self.entries if entry.dashboard_reference_bound
        )
        computed_engine = sum(
            1 for entry in self.entries if entry.engine_adapter_required
        )

        expected_counts = {
            "active_bindings": computed_active,
            "ready_bindings": computed_ready,
            "manifest_bound_bindings": computed_manifest,
            "registry_bound_bindings": computed_registry,
            "memory_reference_bound_bindings": computed_memory,
            "retrieval_reference_bound_bindings": computed_retrieval,
            "dashboard_reference_bound_bindings": computed_dashboard,
            "engine_adapter_required_bindings": computed_engine,
        }

        for field_name, expected_value in expected_counts.items():
            if getattr(self, field_name) != expected_value:
                raise ValueError(f"{field_name} must match computed count")

        if self.active_bindings != total_bindings:
            raise ValueError("all skill bindings must be active")
        if self.ready_bindings != total_bindings:
            raise ValueError("all skill bindings must be ready")
        if self.manifest_bound_bindings != total_bindings:
            raise ValueError("all skill bindings must be manifest-bound")
        if self.registry_bound_bindings != total_bindings:
            raise ValueError("all skill bindings must be registry-bound")
        if self.memory_reference_bound_bindings > total_bindings:
            raise ValueError("memory_reference_bound_bindings cannot exceed total_bindings")
        if self.retrieval_reference_bound_bindings != total_bindings:
            raise ValueError("all skill bindings must be retrieval-reference-bound")
        if self.dashboard_reference_bound_bindings != total_bindings:
            raise ValueError("all skill bindings must be dashboard-reference-bound")

        binding_ids = tuple(entry.skill_binding_id for entry in self.entries)
        if len(set(binding_ids)) != len(binding_ids):
            raise ValueError("duplicate skill_binding_id values detected")


def _resolve_memory_tier_id(module_slug: str, manifest_by_module: dict[str, object]) -> str:
    manifest = manifest_by_module.get(module_slug)
    if manifest is None:
        return ""

    required_memory_tier_ids = getattr(manifest, "required_memory_tier_ids", ())
    if not required_memory_tier_ids:
        return ""

    return str(required_memory_tier_ids[0])

def build_skill_binding_contract() -> SkillBindingContract:
    from MAKSIMAR_CORE_LIB.module_manifest import build_module_manifest_schema_contract
    from MAKSIMAR_SERVER.MEMORY_REGISTRY import build_memory_registry_contract
    from MAKSIMAR_SERVER.SKILL_ADAPTER_REGISTRY import (
        build_skill_adapter_registry_contract,
    )

    manifests = build_module_manifest_schema_contract()
    skill_registry = build_skill_adapter_registry_contract()
    memory_registry = build_memory_registry_contract()

    manifest_by_module = {
        entry.module_slug: entry
        for entry in manifests.manifests
        if entry.active
    }
    memory_tier_ids = {
        entry.memory_tier_id
        for entry in memory_registry.entries
        if entry.active
    }

    entries = tuple(
        SkillBindingEntry(
            skill_binding_id=f"skill_binding_{safe_id_suffix(entry.module_slug)}",
            module_slug=entry.module_slug,
            module_id=entry.module_id,
            skill_id=entry.skill_id,
            worker_id=entry.worker_id,
            domain_class=str(entry.domain_class),
            policy_profile=str(entry.policy_profile),
            observability_profile=str(entry.observability_profile),
            adapter_execution_mode=str(entry.adapter_execution_mode),
            memory_tier_id=_resolve_memory_tier_id(
                entry.module_slug,
                manifest_by_module,
            ),
            input_contract_ids=entry.input_contract_ids,
            output_contract_ids=entry.output_contract_ids,
            panel_ids=entry.panel_ids,
            supported_languages=entry.supported_languages,
            supported_scripts=entry.supported_scripts,
            manifest_bound=entry.module_slug in manifest_by_module,
            registry_bound=entry.registration_status == "registered",
            memory_reference_bound=(
                _resolve_memory_tier_id(entry.module_slug, manifest_by_module)
                in memory_tier_ids
            ),
            retrieval_reference_bound=True,
            dashboard_reference_bound=bool(entry.panel_ids),
            engine_adapter_required=entry.engine_adapter_required,
            active=entry.active,
            binding_ready=(
                entry.active
                and entry.module_slug in manifest_by_module
                and entry.registration_status == "registered"
                and bool(entry.panel_ids)
            ),
            description=f"Skill/domain binding for {entry.module_slug}.",
        )
        for entry in skill_registry.entries
        if entry.active
    )

    return SkillBindingContract(
        total_bindings=len(entries),
        active_bindings=sum(1 for entry in entries if entry.active),
        ready_bindings=sum(1 for entry in entries if entry.binding_ready),
        manifest_bound_bindings=sum(1 for entry in entries if entry.manifest_bound),
        registry_bound_bindings=sum(1 for entry in entries if entry.registry_bound),
        memory_reference_bound_bindings=sum(
            1 for entry in entries if entry.memory_reference_bound
        ),
        retrieval_reference_bound_bindings=sum(
            1 for entry in entries if entry.retrieval_reference_bound
        ),
        dashboard_reference_bound_bindings=sum(
            1 for entry in entries if entry.dashboard_reference_bound
        ),
        engine_adapter_required_bindings=sum(
            1 for entry in entries if entry.engine_adapter_required
        ),
        entries=entries,
    )
