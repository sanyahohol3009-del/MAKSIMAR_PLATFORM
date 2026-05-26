from __future__ import annotations

import re
from dataclasses import dataclass
from pathlib import Path

from MAKSIMAR_CORE_LIB.capability_registry.capability_registry_models import (
    CapabilityRegistryContract,
    build_canonical_capability_registry_contract,
)


DEFAULT_CAPABILITY_REGISTRY_YAML_PATH = Path(
    "docs/architecture/open_source_integration/canonical_capability_registry_v1.yaml"
)

_CANONICAL_REGISTRY_ROOT = Path("docs/architecture/open_source_integration")
_CAPABILITY_ID_PATTERN = re.compile(r"^\s*-\s+capability_id:\s*(cap_[a-z][a-z0-9_]*)\s*$", re.MULTILINE)


def _ensure_non_empty_str(value: str, field_name: str) -> str:
    if not isinstance(value, str):
        raise ValueError(f"{field_name} must be a string")
    normalized = value.strip()
    if not normalized:
        raise ValueError(f"{field_name} must be a non-empty string")
    return normalized


def _extract_scalar(text: str, key: str) -> str:
    match = re.search(rf"^\s*{re.escape(key)}:\s*(.+?)\s*$", text, re.MULTILINE)
    if match is None:
        raise ValueError(f"missing required YAML scalar: {key}")
    return _ensure_non_empty_str(match.group(1), key)


def _extract_bool(text: str, key: str) -> bool:
    raw_value = _extract_scalar(text, key).lower()
    if raw_value == "true":
        return True
    if raw_value == "false":
        return False
    raise ValueError(f"YAML scalar {key} must be true or false")


def _extract_capability_ids(text: str) -> tuple[str, ...]:
    capability_ids = tuple(match.group(1) for match in _CAPABILITY_ID_PATTERN.finditer(text))
    if not capability_ids:
        raise ValueError("canonical registry YAML must define capability_id entries")
    if len(set(capability_ids)) != len(capability_ids):
        raise ValueError("canonical registry YAML contains duplicate capability_id values")
    return capability_ids


def _validate_source_path(source_path: Path, allow_noncanonical_source: bool) -> Path:
    if not isinstance(source_path, Path):
        source_path = Path(source_path)

    normalized = Path(source_path.as_posix())

    if normalized.suffix in {".pyc", ".pyo"}:
        raise ValueError("capability registry loader must not read compiled Python files")
    if "__pycache__" in normalized.parts:
        raise ValueError("capability registry loader must not read __pycache__ files")

    if not allow_noncanonical_source:
        source_text = normalized.as_posix()
        root_text = _CANONICAL_REGISTRY_ROOT.as_posix()
        if not source_text.startswith(f"{root_text}/"):
            raise ValueError(
                "capability registry loader may only read the canonical docs registry by default"
            )

    if not normalized.exists():
        raise FileNotFoundError(f"capability registry source not found: {normalized}")
    if not normalized.is_file():
        raise ValueError(f"capability registry source must be a file: {normalized}")

    return normalized


@dataclass(frozen=True, slots=True)
class CapabilityRegistryLoadResult:
    """Read-only load result for the canonical capability registry."""

    source_path: str
    schema_version: str
    registry_id: str
    contract: CapabilityRegistryContract
    yaml_capability_ids: tuple[str, ...]
    missing_from_yaml: tuple[str, ...]
    extra_in_yaml: tuple[str, ...]
    direct_core_import_allowed: bool
    source_of_truth_override_allowed: bool
    runtime_mutation_allowed: bool
    dashboard_read_only: bool
    active_deployment_created: bool
    ports_opened: bool
    containers_started: bool
    read_only_load: bool = True

    def __post_init__(self) -> None:
        source_path = _ensure_non_empty_str(self.source_path, "source_path")
        schema_version = _ensure_non_empty_str(self.schema_version, "schema_version")
        registry_id = _ensure_non_empty_str(self.registry_id, "registry_id")

        if source_path.endswith((".pyc", ".pyo")) or "__pycache__" in source_path:
            raise ValueError("load result must not reference compiled Python cache files")
        if schema_version != "canonical_capability_registry.v1":
            raise ValueError("schema_version must be canonical_capability_registry.v1")
        if registry_id != "phase_1_canonical_capability_registry":
            raise ValueError("registry_id must be phase_1_canonical_capability_registry")
        if not isinstance(self.contract, CapabilityRegistryContract):
            raise TypeError("contract must be CapabilityRegistryContract")

        for field_name in (
            "yaml_capability_ids",
            "missing_from_yaml",
            "extra_in_yaml",
        ):
            value = getattr(self, field_name)
            if not isinstance(value, tuple):
                raise TypeError(f"{field_name} must be a tuple")
            for item in value:
                _ensure_non_empty_str(item, field_name)

        if self.missing_from_yaml:
            raise ValueError(f"YAML registry is missing capability ids: {self.missing_from_yaml}")
        if self.extra_in_yaml:
            raise ValueError(f"YAML registry contains unknown capability ids: {self.extra_in_yaml}")

        if self.direct_core_import_allowed:
            raise ValueError("direct_core_import_allowed must remain false")
        if self.source_of_truth_override_allowed:
            raise ValueError("source_of_truth_override_allowed must remain false")
        if self.runtime_mutation_allowed:
            raise ValueError("runtime_mutation_allowed must remain false")
        if not self.dashboard_read_only:
            raise ValueError("dashboard_read_only must remain true")
        if self.active_deployment_created:
            raise ValueError("active_deployment_created must remain false")
        if self.ports_opened:
            raise ValueError("ports_opened must remain false")
        if self.containers_started:
            raise ValueError("containers_started must remain false")
        if not self.read_only_load:
            raise ValueError("read_only_load must remain true")

        object.__setattr__(self, "source_path", source_path)
        object.__setattr__(self, "schema_version", schema_version)
        object.__setattr__(self, "registry_id", registry_id)


def load_canonical_capability_registry(
    source_path: Path = DEFAULT_CAPABILITY_REGISTRY_YAML_PATH,
    *,
    allow_noncanonical_source: bool = False,
) -> CapabilityRegistryLoadResult:
    """Load and validate the canonical capability registry as a read-only contract."""

    normalized_source = _validate_source_path(
        Path(source_path),
        allow_noncanonical_source=allow_noncanonical_source,
    )
    text = normalized_source.read_text(encoding="utf-8")

    schema_version = _extract_scalar(text, "schema_version")
    registry_id = _extract_scalar(text, "registry_id")
    yaml_capability_ids = _extract_capability_ids(text)

    contract = build_canonical_capability_registry_contract()
    contract_capability_ids = tuple(entry.capability_id for entry in contract.entries)

    missing_from_yaml = tuple(
        capability_id
        for capability_id in contract_capability_ids
        if capability_id not in yaml_capability_ids
    )
    extra_in_yaml = tuple(
        capability_id
        for capability_id in yaml_capability_ids
        if capability_id not in contract_capability_ids
    )

    return CapabilityRegistryLoadResult(
        source_path=normalized_source.as_posix(),
        schema_version=schema_version,
        registry_id=registry_id,
        contract=contract,
        yaml_capability_ids=yaml_capability_ids,
        missing_from_yaml=missing_from_yaml,
        extra_in_yaml=extra_in_yaml,
        direct_core_import_allowed=_extract_bool(text, "direct_core_import_allowed"),
        source_of_truth_override_allowed=_extract_bool(
            text,
            "source_of_truth_override_allowed",
        ),
        runtime_mutation_allowed=_extract_bool(text, "runtime_mutation_allowed"),
        dashboard_read_only=_extract_bool(text, "dashboard_read_only"),
        active_deployment_created=_extract_bool(text, "active_deployment_created"),
        ports_opened=_extract_bool(text, "ports_opened"),
        containers_started=_extract_bool(text, "containers_started"),
        read_only_load=True,
    )
