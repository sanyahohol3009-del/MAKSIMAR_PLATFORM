from __future__ import annotations

import re
import json
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
DEFAULT_CAPABILITY_MANIFEST_DIR = _CANONICAL_REGISTRY_ROOT / "capability_manifests"
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


def discover_capability_providers(capability_id: str) -> tuple[dict[str, object], ...]:
    """Discover providers from versioned manifests in the canonical registry root."""
    registry = load_canonical_capability_registry()
    manifests = load_capability_manifests()
    manifest = next((item for item in manifests if item["id"] == capability_id), None)
    if manifest is None:
        return ()
    return ({
        "capability_id": manifest["id"],
        "provider_id": manifest["provider"],
        "registry_id": registry.registry_id,
        "manifest_version": manifest["version"],
        "permissions": tuple(manifest["permissions"]),
        "network_required": manifest["network_policy"] != "DENY",
        "disable_safe": manifest["degradation_state"] == "conversation_continues",
        "runtime_mutation_allowed": False,
        "timeout_policy": dict(manifest["timeout_policy"]),
        "operation_contracts": tuple(dict(item) for item in manifest["operation_contracts"]),
    },)


def validate_operation_dependency_references(
    operation: dict[str, object], registered_operation_ids: tuple[str, ...] | None = None,
) -> tuple[str, ...]:
    """Validate the same registry-owned operation IDs, without adding or choosing edges."""
    targets = operation.get("declared_prerequisite_for_operation_ids", ())
    if not isinstance(targets, (tuple, list)) or any(
        not isinstance(value, str) or not value or value != value.strip() for value in targets
    ):
        raise ValueError("operation_dependency_references_invalid")
    if len(set(targets)) != len(targets):
        raise ValueError("operation_dependency_reference_duplicate")
    if operation.get("operation_id") in targets:
        raise ValueError("operation_dependency_self_reference")
    if targets and registered_operation_ids is not None and any(
        registered_operation_ids.count(value) != 1
        for value in (str(operation["operation_id"]), *targets)
    ):
        raise ValueError("operation_dependency_target_not_uniquely_registered")
    return tuple(targets)


def validate_semantic_capability_projection(projection: dict[str, object]) -> dict[str, object]:
    """Validate the bounded runtime projection without importing its server owner."""
    if projection.get("schema_version") != "semantic_capability_registry_projection.v1":
        raise ValueError("unsupported semantic capability projection schema")
    entries = projection.get("entries")
    if not isinstance(entries, (tuple, list)) or not entries:
        raise ValueError("semantic capability projection entries must not be empty")
    seen: set[str] = set()
    normalized: list[dict[str, object]] = []
    for raw in entries:
        if not isinstance(raw, dict):
            raise TypeError("semantic capability projection entry must be an object")
        capability_id = _ensure_non_empty_str(str(raw.get("capability_id", "")), "capability_id")
        if capability_id in seen:
            raise ValueError(f"duplicate projected capability: {capability_id}")
        seen.add(capability_id)
        operations = raw.get("operation_contracts")
        if not isinstance(operations, (tuple, list)):
            raise ValueError(f"projected operation contracts must be a list: {capability_id}")
        for operation in operations:
            validate_operation_dependency_references(operation)
        executable = raw.get("execution_contract_available") is True
        if executable and not operations:
            raise ValueError(f"executable projected capability has no operations: {capability_id}")
        if not executable and operations:
            raise ValueError(f"non-executable projected capability exposes operations: {capability_id}")
        if raw.get("operation_contract_source") not in {"MANIFEST", "EXISTING_TYPED_CONTRACT", "VISIBILITY_ONLY"}:
            raise ValueError(f"invalid operation contract source: {capability_id}")
        if raw.get("provider_binding_status") not in {"BOUND", "UNBOUND", "UNKNOWN"}:
            raise ValueError(f"invalid provider binding status: {capability_id}")
        if raw.get("selection_mode") not in {"EXECUTABLE", "PLAN_ONLY", "VISIBILITY_ONLY"}:
            raise ValueError(f"invalid selection mode: {capability_id}")
        if raw.get("capability_exists") is not True:
            raise ValueError(f"projected capability must exist: {capability_id}")
        if raw.get("provider_available") not in (True, False, None):
            raise ValueError(f"provider_available must be bool or null: {capability_id}")
        normalized.append(dict(raw))
    result = dict(projection)
    result["entries"] = tuple(normalized)
    result["capability_count"] = len(normalized)
    return result


def project_semantic_capability_index(projection: dict[str, object]) -> tuple[dict[str, object], ...]:
    """Return all registered capabilities in a compact, text-independent discovery view."""
    validated = validate_semantic_capability_projection(projection)
    return tuple({
        "capability_id": str(entry["capability_id"]),
        "kind": str(entry.get("kind", "")),
        "description": str(entry.get("semantic_description", ""))[:96],
        "exists": entry.get("capability_exists") is True,
        "availability": str(entry.get("availability_status", "UNKNOWN")),
        "execution_contract": entry.get("execution_contract_available") is True,
    } for entry in validated["entries"])  # type: ignore[union-attr]


def select_semantic_projection_details(
    projection: dict[str, object], capability_ids: tuple[str, ...],
) -> dict[str, object]:
    """Select details solely by model-returned registry ids, never by request text."""
    validated = validate_semantic_capability_projection(projection)
    requested = tuple(dict.fromkeys(str(value) for value in capability_ids))
    by_id = {str(entry["capability_id"]): entry for entry in validated["entries"]}  # type: ignore[union-attr]
    unknown = tuple(value for value in requested if value not in by_id)
    if unknown:
        raise ValueError(f"candidate capability ids are not registered: {unknown!r}")
    result = dict(validated)
    result["entries"] = tuple(dict(by_id[value]) for value in requested)
    result["capability_count"] = len(requested)
    result["projection_scope"] = "model_selected_authoritative_details"
    return result


def project_semantic_operation_catalog(projection: dict[str, object]) -> tuple[dict[str, object], ...]:
    validated = validate_semantic_capability_projection(projection)
    catalog: list[dict[str, object]] = []
    for entry in validated["entries"]:  # type: ignore[union-attr]
        provider_ids = tuple(str(value) for value in entry.get("provider_ids", ()))
        for operation in entry["operation_contracts"]:
            catalog.append({
                "capability_id": str(entry["capability_id"]), "kind": str(entry.get("kind", "")),
                "semantic_description": str(entry.get("semantic_description", "")),
                "capability_exists": True, "provider_ids": provider_ids,
                "provider_exists": bool(entry.get("provider_exists")),
                "provider_available": entry.get("provider_available"),
                "availability_status": str(entry.get("availability_status", "UNKNOWN")),
                "operation_id": str(operation["operation_id"]),
                "operation_description": str(operation["description"]),
                "description": str(operation["description"]),
                **({"declared_prerequisite_for_operation_ids": tuple(operation["declared_prerequisite_for_operation_ids"])}
                   if operation.get("declared_prerequisite_for_operation_ids") else {}),
                "required_parameters": tuple(operation.get("required_parameters", ())),
                "parameter_schemas": dict(operation.get("parameter_schemas", {})),
                "optional_parameters": tuple(operation.get("optional_parameters", ())),
                "supported_goal_effect_intents": tuple(operation.get("supported_goal_effect_intents", ())),
                "evidence_kinds": tuple(operation["evidence_kinds"]),
                "effect_type": str(operation["effect_type"]),
                "target_scope": str(operation["target_scope"]),
                "reversibility": str(operation["reversibility"]),
                "external_side_effect": bool(operation["external_side_effect"]),
                "risk_class": str(operation["risk_class"]),
                "target_restrictions": tuple(entry.get("target_restrictions", ())),
                "identity_eligibility_metadata": dict(entry.get("identity_eligibility_metadata", {})),
                "policy_metadata": dict(entry.get("policy_metadata", {})),
                "model_role_requirements": tuple(entry.get("model_role_requirements", ())),
                "operation_contract_source": str(entry.get("operation_contract_source", "VISIBILITY_ONLY")),
                "provider_binding_status": str(entry.get("provider_binding_status", "UNKNOWN")),
                "execution_contract_available": entry.get("execution_contract_available") is True,
                "selection_mode": str(entry.get("selection_mode", "VISIBILITY_ONLY")),
            })
    return tuple(catalog)


def discover_projected_capability_providers(
    projection: dict[str, object], capability_id: str,
) -> tuple[dict[str, object], ...]:
    validated = validate_semantic_capability_projection(projection)
    entry = next((item for item in validated["entries"] if item["capability_id"] == capability_id), None)  # type: ignore[union-attr]
    if entry is None:
        return ()
    if entry.get("provider_binding_status") != "BOUND":
        return ()
    return tuple({
        "capability_id": capability_id, "provider_id": str(provider_id),
        "provider_exists": bool(entry.get("provider_exists")),
        "provider_available": entry.get("provider_available"),
        "availability_status": str(entry.get("availability_status", "UNKNOWN")),
    } for provider_id in entry.get("provider_ids", ()))


def load_capability_manifests(manifest_dir: Path = DEFAULT_CAPABILITY_MANIFEST_DIR,
                              *, allow_noncanonical_source: bool = False) -> tuple[dict[str, object], ...]:
    directory = Path(manifest_dir)
    if not allow_noncanonical_source and not directory.as_posix().startswith(_CANONICAL_REGISTRY_ROOT.as_posix() + "/"):
        raise ValueError("manifest directory must remain inside canonical registry root")
    required = {"schema_version", "id", "version", "purpose", "description", "public_operations", "operation_contracts",
                "input_schema", "output_schema", "risk_class", "permissions", "provider", "healthcheck",
                "timeout_policy", "network_policy", "filesystem_policy", "exclusions", "degradation_state",
                "examples", "non_examples"}
    loaded: list[dict[str, object]] = []
    for path in sorted(directory.glob("*.json")):
        raw = json.loads(path.read_text(encoding="utf-8"))
        if set(raw) != required or raw.get("schema_version") != "capability_manifest.v2":
            raise ValueError(f"invalid capability manifest schema: {path}")
        if not isinstance(raw.get("id"), str) or "." not in raw["id"]:
            raise ValueError(f"invalid public capability id: {path}")
        if raw.get("risk_class") != "READ_ONLY" or raw.get("filesystem_policy") != "READ_ONLY":
            raise ValueError(f"Phase 1 manifest must be read-only: {path}")
        operations = raw.get("public_operations")
        contracts = raw.get("operation_contracts")
        if not isinstance(operations, list) or not operations or not all(isinstance(item, str) and item.strip() for item in operations):
            raise ValueError(f"invalid public operations: {path}")
        if not isinstance(contracts, list) or not contracts:
            raise ValueError(f"missing operation contracts: {path}")
        contract_ids: list[str] = []
        for contract in contracts:
            if not isinstance(contract, dict) or set(contract) != {
                "operation_id", "description", "required_parameters", "evidence_kinds", "effect_type",
                "target_scope", "reversibility", "external_side_effect", "risk_class",
            }:
                raise ValueError(f"invalid operation contract schema: {path}")
            operation_id = contract.get("operation_id")
            description = contract.get("description")
            evidence_kinds = contract.get("evidence_kinds")
            if not isinstance(operation_id, str) or not operation_id.strip():
                raise ValueError(f"invalid operation contract id: {path}")
            if not isinstance(description, str) or not description.strip():
                raise ValueError(f"invalid operation contract description: {path}")
            if not isinstance(evidence_kinds, list) or not evidence_kinds or not all(isinstance(item, str) and item.strip() for item in evidence_kinds):
                raise ValueError(f"invalid operation evidence kinds: {path}")
            if contract.get("effect_type") not in {"OBSERVE", "MUTATE", "EXECUTE", "EXPORT", "PERSIST"}:
                raise ValueError(f"invalid operation effect: {path}")
            if contract.get("reversibility") not in {"REVERSIBLE", "PARTIALLY_REVERSIBLE", "IRREVERSIBLE", "UNKNOWN"}:
                raise ValueError(f"invalid operation reversibility: {path}")
            if contract.get("risk_class") not in {"READ_ONLY", "MUTATION", "DANGEROUS", "UNKNOWN"}:
                raise ValueError(f"invalid operation risk: {path}")
            if not isinstance(contract.get("required_parameters"), list) or not isinstance(contract.get("external_side_effect"), bool):
                raise ValueError(f"invalid operation parameters or external impact: {path}")
            contract_ids.append(operation_id)
        if contract_ids != operations or len(contract_ids) != len(set(contract_ids)):
            raise ValueError(f"operation contracts must exactly match public operations: {path}")
        loaded.append(raw)
    ids = [str(item["id"]) for item in loaded]
    if len(ids) != len(set(ids)):
        raise ValueError("duplicate capability manifest id")
    return tuple(loaded)
