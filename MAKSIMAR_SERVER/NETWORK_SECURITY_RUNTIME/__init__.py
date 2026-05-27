"""Server-side network security runtime.

This package contains policy-gated VPN/egress runtime read-models.
It does not open ports, create VPN tunnels, start containers, or enable external network access.
"""

from MAKSIMAR_SERVER.NETWORK_SECURITY_RUNTIME.vpn_session_registry import (
    VpnSessionRegistry,
    build_default_vpn_session_registry,
)
from MAKSIMAR_SERVER.NETWORK_SECURITY_RUNTIME.vpn_policy_runtime import (
    VpnPolicyRuntimeDecision,
    evaluate_vpn_policy_runtime,
)
from MAKSIMAR_SERVER.NETWORK_SECURITY_RUNTIME.egress_guard_runtime import (
    EgressGuardRuntimeDecision,
    evaluate_egress_guard_runtime,
)
from MAKSIMAR_SERVER.NETWORK_SECURITY_RUNTIME.network_posture_summary_builder import (
    NetworkPostureSummary,
    build_network_posture_summary,
)

__all__ = (
    "VpnSessionRegistry",
    "build_default_vpn_session_registry",
    "VpnPolicyRuntimeDecision",
    "evaluate_vpn_policy_runtime",
    "EgressGuardRuntimeDecision",
    "evaluate_egress_guard_runtime",
    "NetworkPostureSummary",
    "build_network_posture_summary",
)
