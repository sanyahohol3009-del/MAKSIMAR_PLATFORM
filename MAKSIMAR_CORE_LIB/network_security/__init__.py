"""Network security contracts for VPN/P2P base.

This package contains policy-first network security contracts.
It does not open ports, start containers, create tunnels, mutate runtime,
or enable external network access.
"""

from MAKSIMAR_CORE_LIB.network_security.network_backend_adapter_contract import (
    NetworkBackendAdapterContract,
    NetworkBackendAdapterRegistry,
    build_default_network_backend_adapter_registry,
)
from MAKSIMAR_CORE_LIB.network_security.vpn_policy_disable_contract import (
    VpnDisabledRuntimeState,
    VpnPolicyDisableContract,
    build_default_vpn_policy_disable_contract,
)

__all__ = (
    "NetworkBackendAdapterContract",
    "NetworkBackendAdapterRegistry",
    "build_default_network_backend_adapter_registry",
    "VpnDisabledRuntimeState",
    "VpnPolicyDisableContract",
    "build_default_vpn_policy_disable_contract",
)
