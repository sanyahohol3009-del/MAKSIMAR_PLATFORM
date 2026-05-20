from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
from typing import Any


EXPECTED_NETWORK_CONTAINERIZATION_PATHS: tuple[str, ...] = (
    "NETWORK_SEGMENTATION/network_segments.yaml",
    "NETWORK_SEGMENTATION/container_network_rules.yaml",
    "NETWORK_SEGMENTATION/boundaries/container_adapter_boundary.yaml",
    "CONTAINER_DEPLOYMENT/container_deployment_blueprint.yaml",
    "CONTAINER_DEPLOYMENT/container_contract.schema.yaml",
    "CONTAINER_DEPLOYMENT/deployment_gates/security_required_gate.yaml",
    "CONTAINER_DEPLOYMENT/no_production_deploy_until_foundation_green.yaml",
    "MAKSIMAR_CORE_LIB/network_containerization/container_deployment_read_model.py",
)

BLOCKED_EDGES: tuple[str, ...] = (
    "production_deployment",
    "active_docker_deployment",
    "active_compose_deployment",
    "public_exposure",
    "runtime_network_mutation",
)


@dataclass(frozen=True, slots=True)
class NetworkContainerizationPreviewReadModel:
    read_model_id: str
    layer_id: str
    dashboard_safe: bool
    read_only: bool
    deployment_allowed_now: bool
    public_exposure_allowed: bool
    runtime_network_mutation_allowed: bool
    active_docker_deployment_allowed: bool
    active_compose_deployment_allowed: bool
    blocked_edges: tuple[str, ...]
    expected_contract_paths: tuple[str, ...]
    present_contract_paths: tuple[str, ...]
    missing_contract_paths: tuple[str, ...]
    xray_layer_id: str
    xray_non_regression_required: bool
    drift_guard_required: bool
    provenance_index_update_considered: bool
    reason_codes: tuple[str, ...]

    def __post_init__(self) -> None:
        _validate_non_empty("read_model_id", self.read_model_id)
        _validate_non_empty("layer_id", self.layer_id)
        _validate_true("dashboard_safe", self.dashboard_safe)
        _validate_true("read_only", self.read_only)
        _validate_false("deployment_allowed_now", self.deployment_allowed_now)
        _validate_false("public_exposure_allowed", self.public_exposure_allowed)
        _validate_false("runtime_network_mutation_allowed", self.runtime_network_mutation_allowed)
        _validate_false("active_docker_deployment_allowed", self.active_docker_deployment_allowed)
        _validate_false("active_compose_deployment_allowed", self.active_compose_deployment_allowed)
        _validate_non_empty_tuple("blocked_edges", self.blocked_edges)
        _validate_non_empty_tuple("expected_contract_paths", self.expected_contract_paths)
        _validate_tuple("present_contract_paths", self.present_contract_paths)
        _validate_tuple("missing_contract_paths", self.missing_contract_paths)
        _validate_non_empty("xray_layer_id", self.xray_layer_id)
        _validate_true("xray_non_regression_required", self.xray_non_regression_required)
        _validate_true("drift_guard_required", self.drift_guard_required)
        _validate_true("provenance_index_update_considered", self.provenance_index_update_considered)
        _validate_non_empty_tuple("reason_codes", self.reason_codes)

    def to_dict(self) -> dict[str, Any]:
        return {
            "read_model_id": self.read_model_id,
            "layer_id": self.layer_id,
            "dashboard_safe": self.dashboard_safe,
            "read_only": self.read_only,
            "deployment_allowed_now": self.deployment_allowed_now,
            "public_exposure_allowed": self.public_exposure_allowed,
            "runtime_network_mutation_allowed": self.runtime_network_mutation_allowed,
            "active_docker_deployment_allowed": self.active_docker_deployment_allowed,
            "active_compose_deployment_allowed": self.active_compose_deployment_allowed,
            "blocked_edges": self.blocked_edges,
            "expected_contract_paths": self.expected_contract_paths,
            "present_contract_paths": self.present_contract_paths,
            "missing_contract_paths": self.missing_contract_paths,
            "xray_layer_id": self.xray_layer_id,
            "xray_non_regression_required": self.xray_non_regression_required,
            "drift_guard_required": self.drift_guard_required,
            "provenance_index_update_considered": self.provenance_index_update_considered,
            "reason_codes": self.reason_codes,
        }


def build_network_containerization_preview_read_model(
    project_root: Path | None = None,
) -> NetworkContainerizationPreviewReadModel:
    root = Path.cwd() if project_root is None else project_root

    present_paths = tuple(
        contract_path
        for contract_path in EXPECTED_NETWORK_CONTAINERIZATION_PATHS
        if (root / contract_path).exists()
    )
    missing_paths = tuple(
        contract_path
        for contract_path in EXPECTED_NETWORK_CONTAINERIZATION_PATHS
        if not (root / contract_path).exists()
    )

    return NetworkContainerizationPreviewReadModel(
        read_model_id="network_containerization_preview_read_model_v1",
        layer_id="NETWORK_CONTAINERIZATION",
        dashboard_safe=True,
        read_only=True,
        deployment_allowed_now=False,
        public_exposure_allowed=False,
        runtime_network_mutation_allowed=False,
        active_docker_deployment_allowed=False,
        active_compose_deployment_allowed=False,
        blocked_edges=BLOCKED_EDGES,
        expected_contract_paths=EXPECTED_NETWORK_CONTAINERIZATION_PATHS,
        present_contract_paths=present_paths,
        missing_contract_paths=missing_paths,
        xray_layer_id="NETWORK_CONTAINERIZATION",
        xray_non_regression_required=True,
        drift_guard_required=True,
        provenance_index_update_considered=True,
        reason_codes=(
            "preview_read_model_only",
            "blocked_edges_visible_before_deployment",
            "missing_contracts_visible_before_deployment",
            "no_public_exposure",
            "no_runtime_network_mutation",
        ),
    )


def render_network_containerization_terminal_preview(
    project_root: Path | None = None,
) -> str:
    read_model = build_network_containerization_preview_read_model(project_root)
    lines = [
        "NETWORK_CONTAINERIZATION PREVIEW",
        f"read_model_id: {read_model.read_model_id}",
        f"dashboard_safe: {read_model.dashboard_safe}",
        f"read_only: {read_model.read_only}",
        f"deployment_allowed_now: {read_model.deployment_allowed_now}",
        f"public_exposure_allowed: {read_model.public_exposure_allowed}",
        f"runtime_network_mutation_allowed: {read_model.runtime_network_mutation_allowed}",
        f"blocked_edges: {', '.join(read_model.blocked_edges)}",
        f"missing_contract_count: {len(read_model.missing_contract_paths)}",
        f"present_contract_count: {len(read_model.present_contract_paths)}",
        f"xray_layer_id: {read_model.xray_layer_id}",
    ]

    if read_model.missing_contract_paths:
        lines.append("missing_contracts:")
        lines.extend(f"- {path}" for path in read_model.missing_contract_paths)
    else:
        lines.append("missing_contracts: none")

    return "\n".join(lines)


def main() -> int:
    print(render_network_containerization_terminal_preview())
    return 0


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


if __name__ == "__main__":
    raise SystemExit(main())
