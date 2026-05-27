from __future__ import annotations

from MAKSIMAR_CORE_LIB.network_security.mobile_vpn_hook_contract import build_default_mobile_vpn_hooks


def test_mobile_vpn_hook_contract_smoke() -> None:
    hooks = build_default_mobile_vpn_hooks()

    assert {hook.platform for hook in hooks} == {"android", "ios"}
    for hook in hooks:
        assert hook.system_api_call_allowed is False
        assert hook.tunnel_creation_allowed is False
        assert hook.permission_prompt_allowed is False
        assert hook.secret_material_embedded is False
        assert hook.dashboard_visible is True
        assert hook.disable_safe is True
        assert hook.policy_disable_supported is True
        assert hook.runtime_mutation_allowed is False
        assert hook.direct_core_import_allowed is False
        assert hook.source_of_truth_override_allowed is False
        assert hook.external_network_access_enabled is False
        assert hook.ports_opened is False
        assert hook.containers_started is False
        assert hook.active_deployment_created is False
        assert hook.containerization_ready is True
