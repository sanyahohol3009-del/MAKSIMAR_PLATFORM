from __future__ import annotations

from dataclasses import dataclass
from typing import Any

from MAKSIMAR_CORE_LIB.network_containerization.container_contract_models import (
    ContainerContractModel,
    build_default_container_contract_model,
)
from MAKSIMAR_CORE_LIB.network_containerization.network_segment_models import (
    NetworkSegmentModel,
    build_default_network_segments,
)


@dataclass(frozen=True, slots=True)
class NetworkTopologyReadModel:
    topology_id: str
    segments: tuple[NetworkSegmentModel, ...]
    container_contracts: tuple[ContainerContractModel, ...]
    public_exposure_allowed: bool
    runtime_network_mutation_allowed: bool
    production_deployment_allowed: bool
    dashboard_safe: bool
    reason_codes: tuple[str, ...]

    def __post_init__(self) -> None:
        _validate_non_empty("topology_id", self.topology_id)
        if not isinstance(self.segments, tuple) or not self.segments:
            raise ValueError("segments must be a non-empty tuple")
        if not isinstance(self.container_contracts, tuple) or not self.container_contracts:
            raise ValueError("container_contracts must be a non-empty tuple")

        for segment in self.segments:
            if not isinstance(segment, NetworkSegmentModel):
                raise TypeError("segments must contain NetworkSegmentModel values")
            if segment.public_exposure_allowed:
                raise ValueError("segments must not allow public exposure")

        known_segments = {segment.segment_id for segment in self.segments}
        for contract in self.container_contracts:
            if not isinstance(contract, ContainerContractModel):
                raise TypeError("container_contracts must contain ContainerContractModel values")
            if contract.network_segment not in known_segments:
                raise ValueError("container contract references unknown network segment")
            if contract.exposure_policy.public_exposure_allowed:
                raise ValueError("container contract must not allow public exposure")

        _validate_false("public_exposure_allowed", self.public_exposure_allowed)
        _validate_false("runtime_network_mutation_allowed", self.runtime_network_mutation_allowed)
        _validate_false("production_deployment_allowed", self.production_deployment_allowed)
        _validate_true("dashboard_safe", self.dashboard_safe)
        _validate_reason_codes(self.reason_codes)

    def to_dict(self) -> dict[str, Any]:
        return {
            "topology_id": self.topology_id,
            "segments": tuple(segment.to_dict() for segment in self.segments),
            "container_contracts": tuple(contract.to_dict() for contract in self.container_contracts),
            "public_exposure_allowed": self.public_exposure_allowed,
            "runtime_network_mutation_allowed": self.runtime_network_mutation_allowed,
            "production_deployment_allowed": self.production_deployment_allowed,
            "dashboard_safe": self.dashboard_safe,
            "reason_codes": self.reason_codes,
        }


def build_network_topology_read_model() -> NetworkTopologyReadModel:
    return NetworkTopologyReadModel(
        topology_id="network_container_topology_v1",
        segments=build_default_network_segments(),
        container_contracts=(build_default_container_contract_model(),),
        public_exposure_allowed=False,
        runtime_network_mutation_allowed=False,
        production_deployment_allowed=False,
        dashboard_safe=True,
        reason_codes=(
            "network_topology_builder_read_model_only",
            "no_public_exposure_by_default",
            "no_runtime_network_mutation",
            "no_production_deployment",
        ),
    )


def _validate_non_empty(field_name: str, value: str) -> None:
    if not isinstance(value, str):
        raise TypeError(f"{field_name} must be a string")
    if not value:
        raise ValueError(f"{field_name} must not be empty")


def _validate_true(field_name: str, value: bool) -> None:
    if not value:
        raise ValueError(f"{field_name} must remain true")


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
