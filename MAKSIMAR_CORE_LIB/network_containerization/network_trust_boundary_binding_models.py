from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
from typing import Any

from MAKSIMAR_CORE_LIB.network_trust_boundaries import build_network_trust_boundaries_contract


NETWORK_TRUST_BOUNDARY_BINDING_ID = "network_trust_boundary_binding_v1"
NETWORK_SEGMENTATION_READ_MODEL_ID = "network_segmentation_read_model_v1"
TRUST_BOUNDARY_SOURCE_PATH = "MAKSIMAR_CORE_LIB/network_trust_boundaries/network_trust_boundaries_contract.py"
TRUST_BOUNDARY_TEST_PATH = "tests/network_trust_boundaries/test_network_trust_boundaries_contract_smoke.py"
TRUST_BOUNDARY_DOC_PATH = "docs/security_governance/TRUST_BOUNDARIES_v1.md"


@dataclass(frozen=True, slots=True)
class NetworkTrustBoundaryBindingReadModel:
    binding_id: str
    source_authority_path: str
    source_test_path: str
    source_doc_path: str
    source_exists: bool
    source_test_exists: bool
    source_doc_exists: bool
    existing_contract_importable: bool
    network_segmentation_is_source_authority: bool
    adapter_binding_only: bool
    replace_existing_source_allowed: bool
    move_existing_source_allowed: bool
    delete_existing_source_allowed: bool
    migrate_existing_source_allowed: bool
    production_deployment_allowed: bool
    public_exposure_allowed: bool
    runtime_network_mutation_allowed: bool
    canonical_write_allowed: bool
    dashboard_execution_allowed: bool
    dashboard_safe: bool
    reason_codes: tuple[str, ...]

    def __post_init__(self) -> None:
        if self.binding_id != NETWORK_TRUST_BOUNDARY_BINDING_ID:
            raise ValueError("binding_id must be network_trust_boundary_binding_v1")
        _validate_non_empty("source_authority_path", self.source_authority_path)
        _validate_non_empty("source_test_path", self.source_test_path)
        _validate_non_empty("source_doc_path", self.source_doc_path)
        if self.network_segmentation_is_source_authority:
            raise ValueError("NETWORK_SEGMENTATION must not become trust-boundary source authority")
        if not self.adapter_binding_only:
            raise ValueError("adapter_binding_only must remain true")
        _validate_false("replace_existing_source_allowed", self.replace_existing_source_allowed)
        _validate_false("move_existing_source_allowed", self.move_existing_source_allowed)
        _validate_false("delete_existing_source_allowed", self.delete_existing_source_allowed)
        _validate_false("migrate_existing_source_allowed", self.migrate_existing_source_allowed)
        _validate_false("production_deployment_allowed", self.production_deployment_allowed)
        _validate_false("public_exposure_allowed", self.public_exposure_allowed)
        _validate_false("runtime_network_mutation_allowed", self.runtime_network_mutation_allowed)
        _validate_false("canonical_write_allowed", self.canonical_write_allowed)
        _validate_false("dashboard_execution_allowed", self.dashboard_execution_allowed)
        if not self.dashboard_safe:
            raise ValueError("dashboard_safe must remain true")
        _validate_reason_codes(self.reason_codes)

    def to_dict(self) -> dict[str, Any]:
        return {
            "binding_id": self.binding_id,
            "source_authority_path": self.source_authority_path,
            "source_test_path": self.source_test_path,
            "source_doc_path": self.source_doc_path,
            "source_exists": self.source_exists,
            "source_test_exists": self.source_test_exists,
            "source_doc_exists": self.source_doc_exists,
            "existing_contract_importable": self.existing_contract_importable,
            "network_segmentation_is_source_authority": self.network_segmentation_is_source_authority,
            "adapter_binding_only": self.adapter_binding_only,
            "replace_existing_source_allowed": self.replace_existing_source_allowed,
            "move_existing_source_allowed": self.move_existing_source_allowed,
            "delete_existing_source_allowed": self.delete_existing_source_allowed,
            "migrate_existing_source_allowed": self.migrate_existing_source_allowed,
            "production_deployment_allowed": self.production_deployment_allowed,
            "public_exposure_allowed": self.public_exposure_allowed,
            "runtime_network_mutation_allowed": self.runtime_network_mutation_allowed,
            "canonical_write_allowed": self.canonical_write_allowed,
            "dashboard_execution_allowed": self.dashboard_execution_allowed,
            "dashboard_safe": self.dashboard_safe,
            "reason_codes": self.reason_codes,
        }


@dataclass(frozen=True, slots=True)
class NetworkSegmentationReadModel:
    read_model_id: str
    segment_ids: tuple[str, ...]
    healthcheck_required: bool
    restart_policy_required: bool
    no_public_exposure: bool
    production_deployment_allowed: bool
    runtime_network_mutation_allowed: bool
    binding: NetworkTrustBoundaryBindingReadModel
    dashboard_safe: bool
    reason_codes: tuple[str, ...]

    def __post_init__(self) -> None:
        if self.read_model_id != NETWORK_SEGMENTATION_READ_MODEL_ID:
            raise ValueError("read_model_id must be network_segmentation_read_model_v1")
        if not isinstance(self.segment_ids, tuple):
            raise TypeError("segment_ids must be a tuple")
        required_segments = {
            "net_core_safety",
            "net_control",
            "net_security",
            "net_governance",
            "net_data",
            "net_ai",
            "net_products",
            "net_observability",
            "net_update",
        }
        if set(self.segment_ids) != required_segments:
            raise ValueError("segment_ids must match required NETWORK_CONTAINERIZATION markers")
        if not self.healthcheck_required:
            raise ValueError("healthcheck_required must remain true")
        if not self.restart_policy_required:
            raise ValueError("restart_policy_required must remain true")
        if not self.no_public_exposure:
            raise ValueError("no_public_exposure must remain true")
        _validate_false("production_deployment_allowed", self.production_deployment_allowed)
        _validate_false("runtime_network_mutation_allowed", self.runtime_network_mutation_allowed)
        if not isinstance(self.binding, NetworkTrustBoundaryBindingReadModel):
            raise TypeError("binding must be NetworkTrustBoundaryBindingReadModel")
        if not self.dashboard_safe:
            raise ValueError("dashboard_safe must remain true")
        _validate_reason_codes(self.reason_codes)

    def to_dict(self) -> dict[str, Any]:
        return {
            "read_model_id": self.read_model_id,
            "segment_ids": self.segment_ids,
            "healthcheck_required": self.healthcheck_required,
            "restart_policy_required": self.restart_policy_required,
            "no_public_exposure": self.no_public_exposure,
            "production_deployment_allowed": self.production_deployment_allowed,
            "runtime_network_mutation_allowed": self.runtime_network_mutation_allowed,
            "binding": self.binding.to_dict(),
            "dashboard_safe": self.dashboard_safe,
            "reason_codes": self.reason_codes,
        }


def build_network_trust_boundary_binding_read_model(
    *,
    project_root: Path | None = None,
) -> NetworkTrustBoundaryBindingReadModel:
    root = Path.cwd() if project_root is None else project_root
    contract = build_network_trust_boundaries_contract()

    return NetworkTrustBoundaryBindingReadModel(
        binding_id=NETWORK_TRUST_BOUNDARY_BINDING_ID,
        source_authority_path=TRUST_BOUNDARY_SOURCE_PATH,
        source_test_path=TRUST_BOUNDARY_TEST_PATH,
        source_doc_path=TRUST_BOUNDARY_DOC_PATH,
        source_exists=(root / TRUST_BOUNDARY_SOURCE_PATH).exists(),
        source_test_exists=(root / TRUST_BOUNDARY_TEST_PATH).exists(),
        source_doc_exists=(root / TRUST_BOUNDARY_DOC_PATH).exists(),
        existing_contract_importable=contract is not None,
        network_segmentation_is_source_authority=False,
        adapter_binding_only=True,
        replace_existing_source_allowed=False,
        move_existing_source_allowed=False,
        delete_existing_source_allowed=False,
        migrate_existing_source_allowed=False,
        production_deployment_allowed=False,
        public_exposure_allowed=False,
        runtime_network_mutation_allowed=False,
        canonical_write_allowed=False,
        dashboard_execution_allowed=False,
        dashboard_safe=True,
        reason_codes=(
            "existing_network_trust_boundaries_reused",
            "network_segmentation_adapter_binding_only",
            "no_public_exposure",
            "no_production_deployment",
            "no_runtime_network_mutation",
        ),
    )


def build_network_segmentation_read_model(
    *,
    project_root: Path | None = None,
) -> NetworkSegmentationReadModel:
    return NetworkSegmentationReadModel(
        read_model_id=NETWORK_SEGMENTATION_READ_MODEL_ID,
        segment_ids=(
            "net_core_safety",
            "net_control",
            "net_security",
            "net_governance",
            "net_data",
            "net_ai",
            "net_products",
            "net_observability",
            "net_update",
        ),
        healthcheck_required=True,
        restart_policy_required=True,
        no_public_exposure=True,
        production_deployment_allowed=False,
        runtime_network_mutation_allowed=False,
        binding=build_network_trust_boundary_binding_read_model(project_root=project_root),
        dashboard_safe=True,
        reason_codes=(
            "network_segmentation_read_model_built",
            "healthcheck_required",
            "restart_policy_required",
            "no_public_exposure",
        ),
    )


def _validate_non_empty(field_name: str, value: str) -> None:
    if not isinstance(value, str):
        raise TypeError(f"{field_name} must be a string")
    if not value:
        raise ValueError(f"{field_name} must not be empty")


def _validate_false(field_name: str, value: bool) -> None:
    if value:
        raise ValueError(f"{field_name} must remain false")


def _validate_reason_codes(reason_codes: tuple[str, ...]) -> None:
    if not isinstance(reason_codes, tuple):
        raise TypeError("reason_codes must be a tuple")
    if not reason_codes:
        raise ValueError("reason_codes must not be empty")
    for reason_code in reason_codes:
        _validate_non_empty("reason_code", reason_code)


NETWORK_CONTAINERIZATION_XRAY_MARKER_READ_MODEL_ID = "network_containerization_xray_marker_read_model_v1"


@dataclass(frozen=True, slots=True)
class NetworkContainerizationXRayMarkerReadModel:
    read_model_id: str
    net_core_safety: bool
    net_control: bool
    net_security: bool
    net_governance: bool
    net_data: bool
    net_ai: bool
    net_products: bool
    net_observability: bool
    net_update: bool
    healthcheck: bool
    restart_policy: bool
    no_public_exposure: bool
    public_exposure_allowed: bool
    production_deployment_allowed: bool
    runtime_network_mutation_allowed: bool
    dashboard_safe: bool
    reason_codes: tuple[str, ...]

    def __post_init__(self) -> None:
        if self.read_model_id != NETWORK_CONTAINERIZATION_XRAY_MARKER_READ_MODEL_ID:
            raise ValueError("read_model_id must be network_containerization_xray_marker_read_model_v1")
        for marker_name in (
            "net_core_safety",
            "net_control",
            "net_security",
            "net_governance",
            "net_data",
            "net_ai",
            "net_products",
            "net_observability",
            "net_update",
            "healthcheck",
            "restart_policy",
            "no_public_exposure",
        ):
            if not getattr(self, marker_name):
                raise ValueError(f"{marker_name} must remain true")
        _validate_false("public_exposure_allowed", self.public_exposure_allowed)
        _validate_false("production_deployment_allowed", self.production_deployment_allowed)
        _validate_false("runtime_network_mutation_allowed", self.runtime_network_mutation_allowed)
        if not self.dashboard_safe:
            raise ValueError("dashboard_safe must remain true")
        _validate_reason_codes(self.reason_codes)

    def to_dict(self) -> dict[str, Any]:
        return {
            "read_model_id": self.read_model_id,
            "net_core_safety": self.net_core_safety,
            "net_control": self.net_control,
            "net_security": self.net_security,
            "net_governance": self.net_governance,
            "net_data": self.net_data,
            "net_ai": self.net_ai,
            "net_products": self.net_products,
            "net_observability": self.net_observability,
            "net_update": self.net_update,
            "healthcheck": self.healthcheck,
            "restart_policy": self.restart_policy,
            "no_public_exposure": self.no_public_exposure,
            "public_exposure_allowed": self.public_exposure_allowed,
            "production_deployment_allowed": self.production_deployment_allowed,
            "runtime_network_mutation_allowed": self.runtime_network_mutation_allowed,
            "dashboard_safe": self.dashboard_safe,
            "reason_codes": self.reason_codes,
        }


def build_network_containerization_xray_marker_read_model() -> NetworkContainerizationXRayMarkerReadModel:
    return NetworkContainerizationXRayMarkerReadModel(
        read_model_id=NETWORK_CONTAINERIZATION_XRAY_MARKER_READ_MODEL_ID,
        net_core_safety=True,
        net_control=True,
        net_security=True,
        net_governance=True,
        net_data=True,
        net_ai=True,
        net_products=True,
        net_observability=True,
        net_update=True,
        healthcheck=True,
        restart_policy=True,
        no_public_exposure=True,
        public_exposure_allowed=False,
        production_deployment_allowed=False,
        runtime_network_mutation_allowed=False,
        dashboard_safe=True,
        reason_codes=(
            "network_containerization_xray_markers_declared",
            "blueprint_read_model_only",
            "no_public_exposure",
            "no_production_deployment",
            "no_runtime_network_mutation",
        ),
    )


def validate_net_core_safety_marker(read_model: NetworkContainerizationXRayMarkerReadModel) -> bool:
    return _validate_network_marker("net_core_safety", read_model.net_core_safety)


def validate_net_control_marker(read_model: NetworkContainerizationXRayMarkerReadModel) -> bool:
    return _validate_network_marker("net_control", read_model.net_control)


def validate_net_security_marker(read_model: NetworkContainerizationXRayMarkerReadModel) -> bool:
    return _validate_network_marker("net_security", read_model.net_security)


def validate_net_governance_marker(read_model: NetworkContainerizationXRayMarkerReadModel) -> bool:
    return _validate_network_marker("net_governance", read_model.net_governance)


def validate_net_data_marker(read_model: NetworkContainerizationXRayMarkerReadModel) -> bool:
    return _validate_network_marker("net_data", read_model.net_data)


def validate_net_ai_marker(read_model: NetworkContainerizationXRayMarkerReadModel) -> bool:
    return _validate_network_marker("net_ai", read_model.net_ai)


def validate_net_products_marker(read_model: NetworkContainerizationXRayMarkerReadModel) -> bool:
    return _validate_network_marker("net_products", read_model.net_products)


def validate_net_observability_marker(read_model: NetworkContainerizationXRayMarkerReadModel) -> bool:
    return _validate_network_marker("net_observability", read_model.net_observability)


def validate_net_update_marker(read_model: NetworkContainerizationXRayMarkerReadModel) -> bool:
    return _validate_network_marker("net_update", read_model.net_update)


def validate_healthcheck_marker(read_model: NetworkContainerizationXRayMarkerReadModel) -> bool:
    return _validate_network_marker("healthcheck", read_model.healthcheck)


def validate_restart_policy_marker(read_model: NetworkContainerizationXRayMarkerReadModel) -> bool:
    return _validate_network_marker("restart_policy", read_model.restart_policy)


def validate_no_public_exposure_marker(read_model: NetworkContainerizationXRayMarkerReadModel) -> bool:
    _validate_network_marker("no_public_exposure", read_model.no_public_exposure)
    _validate_false("public_exposure_allowed", read_model.public_exposure_allowed)
    return True


def _validate_network_marker(marker_name: str, marker_value: bool) -> bool:
    _validate_non_empty("marker_name", marker_name)
    if not marker_value:
        raise ValueError(f"{marker_name} must remain true")
    return True

