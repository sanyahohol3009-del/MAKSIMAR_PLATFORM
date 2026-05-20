from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
from typing import Any


MANIFEST_PATHS: tuple[str, ...] = (
    "NETWORK_SEGMENTATION/layer_manifest.yaml",
    "CONTAINER_DEPLOYMENT/layer_manifest.yaml",
)

REQUIRED_DEPLOYMENT_GATES: tuple[str, ...] = (
    "security_layer_green",
    "data_plane_green",
    "update_recovery_green",
)

ACCEPTANCE_TEST_COMMANDS: tuple[str, ...] = (
    "tests/network_containerization -q",
    "tests/network_trust_boundaries -q",
    "tests/architecture_map_runtime/test_architecture_control_no_mutation_no_network_smoke.py -q",
    "tests/architecture_map/test_architecture_blueprint_drift_guard.py -q",
    "tools/architecture_xray_radar.py --show-missing-laws",
    "pytest -q -n auto",
)


@dataclass(frozen=True, slots=True)
class NetworkContainerizationAcceptanceReadModel:
    read_model_id: str
    layer_id: str
    dashboard_safe: bool
    read_only: bool
    no_public_exposure_by_default: bool
    security_layer_green_required: bool
    data_plane_green_required: bool
    update_recovery_green_required: bool
    network_trust_boundaries_accounted: bool
    manifest_present: bool
    manifest_paths: tuple[str, ...]
    required_deployment_gates: tuple[str, ...]
    acceptance_test_commands: tuple[str, ...]
    deployment_allowed_now: bool
    production_deployment_allowed: bool
    active_docker_deployment_allowed: bool
    active_compose_deployment_allowed: bool
    public_exposure_allowed: bool
    runtime_network_mutation_allowed: bool
    full_auto_pytest_required: bool
    reason_codes: tuple[str, ...]

    def __post_init__(self) -> None:
        _validate_non_empty("read_model_id", self.read_model_id)
        _validate_non_empty("layer_id", self.layer_id)
        _validate_true("dashboard_safe", self.dashboard_safe)
        _validate_true("read_only", self.read_only)
        _validate_true("no_public_exposure_by_default", self.no_public_exposure_by_default)
        _validate_true("security_layer_green_required", self.security_layer_green_required)
        _validate_true("data_plane_green_required", self.data_plane_green_required)
        _validate_true("update_recovery_green_required", self.update_recovery_green_required)
        _validate_true("network_trust_boundaries_accounted", self.network_trust_boundaries_accounted)
        _validate_true("manifest_present", self.manifest_present)
        _validate_non_empty_tuple("manifest_paths", self.manifest_paths)
        _validate_non_empty_tuple("required_deployment_gates", self.required_deployment_gates)
        _validate_non_empty_tuple("acceptance_test_commands", self.acceptance_test_commands)
        _validate_false("deployment_allowed_now", self.deployment_allowed_now)
        _validate_false("production_deployment_allowed", self.production_deployment_allowed)
        _validate_false("active_docker_deployment_allowed", self.active_docker_deployment_allowed)
        _validate_false("active_compose_deployment_allowed", self.active_compose_deployment_allowed)
        _validate_false("public_exposure_allowed", self.public_exposure_allowed)
        _validate_false("runtime_network_mutation_allowed", self.runtime_network_mutation_allowed)
        _validate_true("full_auto_pytest_required", self.full_auto_pytest_required)
        _validate_non_empty_tuple("reason_codes", self.reason_codes)

    def to_dict(self) -> dict[str, Any]:
        return {
            "read_model_id": self.read_model_id,
            "layer_id": self.layer_id,
            "dashboard_safe": self.dashboard_safe,
            "read_only": self.read_only,
            "no_public_exposure_by_default": self.no_public_exposure_by_default,
            "security_layer_green_required": self.security_layer_green_required,
            "data_plane_green_required": self.data_plane_green_required,
            "update_recovery_green_required": self.update_recovery_green_required,
            "network_trust_boundaries_accounted": self.network_trust_boundaries_accounted,
            "manifest_present": self.manifest_present,
            "manifest_paths": self.manifest_paths,
            "required_deployment_gates": self.required_deployment_gates,
            "acceptance_test_commands": self.acceptance_test_commands,
            "deployment_allowed_now": self.deployment_allowed_now,
            "production_deployment_allowed": self.production_deployment_allowed,
            "active_docker_deployment_allowed": self.active_docker_deployment_allowed,
            "active_compose_deployment_allowed": self.active_compose_deployment_allowed,
            "public_exposure_allowed": self.public_exposure_allowed,
            "runtime_network_mutation_allowed": self.runtime_network_mutation_allowed,
            "full_auto_pytest_required": self.full_auto_pytest_required,
            "reason_codes": self.reason_codes,
        }


def build_network_containerization_acceptance_read_model(
    *,
    project_root: Path | None = None,
    security_layer_green_required: bool = True,
    data_plane_green_required: bool = True,
    update_recovery_green_required: bool = True,
) -> NetworkContainerizationAcceptanceReadModel:
    root = Path.cwd() if project_root is None else project_root
    manifest_present = all((root / path).exists() for path in MANIFEST_PATHS)

    return NetworkContainerizationAcceptanceReadModel(
        read_model_id="network_containerization_acceptance_read_model_v1",
        layer_id="NETWORK_CONTAINERIZATION",
        dashboard_safe=True,
        read_only=True,
        no_public_exposure_by_default=True,
        security_layer_green_required=security_layer_green_required,
        data_plane_green_required=data_plane_green_required,
        update_recovery_green_required=update_recovery_green_required,
        network_trust_boundaries_accounted=True,
        manifest_present=manifest_present,
        manifest_paths=MANIFEST_PATHS,
        required_deployment_gates=REQUIRED_DEPLOYMENT_GATES,
        acceptance_test_commands=ACCEPTANCE_TEST_COMMANDS,
        deployment_allowed_now=False,
        production_deployment_allowed=False,
        active_docker_deployment_allowed=False,
        active_compose_deployment_allowed=False,
        public_exposure_allowed=False,
        runtime_network_mutation_allowed=False,
        full_auto_pytest_required=True,
        reason_codes=(
            "network_containerization_acceptance_read_model",
            "no_public_exposure_by_default",
            "security_data_update_gates_required",
            "network_trust_boundaries_accounted",
            "manifest_present",
            "full_auto_pytest_required",
        ),
    )


def _validate_non_empty(field_name: str, value: str) -> None:
    if not isinstance(value, str):
        raise TypeError(f"{field_name} must be a string")
    if not value:
        raise ValueError(f"{field_name} must not be empty")


def _validate_tuple(field_name: str, value: tuple[str, ...]) -> None:
    if not isinstance(value, tuple):
        raise TypeError(f"{field_name} must be a tuple")
    for item in value:
        _validate_non_empty(field_name, item)


def _validate_non_empty_tuple(field_name: str, value: tuple[str, ...]) -> None:
    _validate_tuple(field_name, value)
    if not value:
        raise ValueError(f"{field_name} must not be empty")


def _validate_true(field_name: str, value: bool) -> None:
    if not value:
        raise ValueError(f"{field_name} must remain true")


def _validate_false(field_name: str, value: bool) -> None:
    if value:
        raise ValueError(f"{field_name} must remain false")
