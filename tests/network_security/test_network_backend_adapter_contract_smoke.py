from __future__ import annotations

import pytest

from MAKSIMAR_CORE_LIB.network_security.network_backend_adapter_contract import (
    NetworkBackendAdapterContract,
    NetworkBackendAdapterRegistry,
    build_default_network_backend_adapter_registry,
)


def test_network_backend_adapter_contract_smoke() -> None:
    registry = build_default_network_backend_adapter_registry()

    assert isinstance(registry, NetworkBackendAdapterRegistry)
    assert registry.schema_version == "network_backend_adapter_contract.v1"
    assert registry.registry_id == "phase_2_network_backend_adapter_registry"
    assert len(registry.adapters) >= 4

    adapter_ids = {adapter.adapter_id for adapter in registry.adapters}
    assert "net_server_vpn_adapter" in adapter_ids
    assert "net_mobile_vpn_adapter" in adapter_ids
    assert "net_p2p_mesh_adapter" in adapter_ids
    assert "net_egress_guard_adapter" in adapter_ids

    for adapter in registry.adapters:
        assert adapter.dashboard_visible is True
        assert adapter.disable_safe is True
        assert adapter.policy_disable_supported is True
        assert adapter.runtime_implemented is False
        assert adapter.runtime_execution_verified is False
        assert adapter.runtime_evidence_paths == ()
        assert adapter.direct_core_import_allowed is False
        assert adapter.source_of_truth_override_allowed is False
        assert adapter.runtime_mutation_allowed is False
        assert adapter.network_egress_allowed_by_default is False
        assert adapter.external_network_access_enabled is False
        assert adapter.ports_opened is False
        assert adapter.containers_started is False
        assert adapter.active_deployment_created is False
        assert adapter.containerization_ready is True


def test_network_backend_adapter_rejects_direct_external_binding_smoke() -> None:
    with pytest.raises(ValueError):
        NetworkBackendAdapterContract(
            adapter_id="net_bad_external",
            title="Bad External Adapter",
            backend_kind="server_vpn",
            scope="server",
            runtime_mode="disabled",
            container_profile="server_service",
            owner_surface="MAKSIMAR_SERVER/NETWORK_SECURITY_RUNTIME",
            contract_paths=("EXTERNAL_BACKENDS/bad/vpn.py",),
            policy_refs=("MAKSIMAR_CORE_LIB/network_security/vpn_policy_disable_contract.py",),
            dashboard_visible=True,
            disable_safe=True,
            policy_disable_supported=True,
            runtime_implemented=False,
            runtime_execution_verified=False,
            runtime_evidence_paths=(),
            direct_core_import_allowed=False,
            source_of_truth_override_allowed=False,
            runtime_mutation_allowed=False,
            network_egress_allowed_by_default=False,
            external_network_access_enabled=False,
            ports_opened=False,
            containers_started=False,
            active_deployment_created=False,
            requires_operator_approval=True,
            containerization_ready=True,
            reason_codes=("direct_external_binding_rejected",),
        )


def test_network_backend_adapter_rejects_ports_and_containers_smoke() -> None:
    with pytest.raises(ValueError):
        NetworkBackendAdapterContract(
            adapter_id="net_bad_open_port",
            title="Bad Open Port Adapter",
            backend_kind="server_vpn",
            scope="server",
            runtime_mode="disabled",
            container_profile="server_service",
            owner_surface="MAKSIMAR_SERVER/NETWORK_SECURITY_RUNTIME",
            contract_paths=("MAKSIMAR_CORE_LIB/network_security/network_backend_adapter_contract.py",),
            policy_refs=("MAKSIMAR_CORE_LIB/network_security/vpn_policy_disable_contract.py",),
            dashboard_visible=True,
            disable_safe=True,
            policy_disable_supported=True,
            runtime_implemented=False,
            runtime_execution_verified=False,
            runtime_evidence_paths=(),
            direct_core_import_allowed=False,
            source_of_truth_override_allowed=False,
            runtime_mutation_allowed=False,
            network_egress_allowed_by_default=False,
            external_network_access_enabled=False,
            ports_opened=True,
            containers_started=False,
            active_deployment_created=False,
            requires_operator_approval=True,
            containerization_ready=True,
            reason_codes=("ports_must_not_open_in_contract_batch",),
        )
