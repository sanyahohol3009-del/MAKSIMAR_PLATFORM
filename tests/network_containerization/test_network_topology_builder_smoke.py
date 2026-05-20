from __future__ import annotations

import pytest

from MAKSIMAR_CORE_LIB.network_containerization.network_segment_models import (
    build_default_network_segments,
)
from MAKSIMAR_CORE_LIB.network_containerization.network_topology_builder import (
    NetworkTopologyReadModel,
    build_network_topology_read_model,
)


def test_network_topology_builder_returns_dashboard_safe_read_model() -> None:
    topology = build_network_topology_read_model()

    assert topology.topology_id == "network_container_topology_v1"
    assert topology.public_exposure_allowed is False
    assert topology.runtime_network_mutation_allowed is False
    assert topology.production_deployment_allowed is False
    assert topology.dashboard_safe is True
    assert topology.segments
    assert topology.container_contracts


def test_network_topology_rejects_public_exposure() -> None:
    topology = build_network_topology_read_model()

    with pytest.raises(ValueError, match="public_exposure_allowed"):
        NetworkTopologyReadModel(
            topology_id=topology.topology_id,
            segments=build_default_network_segments(),
            container_contracts=topology.container_contracts,
            public_exposure_allowed=True,
            runtime_network_mutation_allowed=False,
            production_deployment_allowed=False,
            dashboard_safe=True,
            reason_codes=("bad",),
        )
