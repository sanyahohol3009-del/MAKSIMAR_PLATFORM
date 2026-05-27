from __future__ import annotations

from dataclasses import dataclass
from typing import Any, Literal


MobilePlatform = Literal["android", "ios"]


@dataclass(frozen=True, slots=True)
class MobileVpnHookContract:
    """Mobile VPN hook contract.

    This is a shell binding contract only. It does not call Android/iOS VPN APIs.
    """

    hook_id: str
    platform: MobilePlatform
    profile_id: str
    system_api_call_allowed: bool
    tunnel_creation_allowed: bool
    permission_prompt_allowed: bool
    secret_material_embedded: bool
    dashboard_visible: bool
    disable_safe: bool
    policy_disable_supported: bool
    runtime_mutation_allowed: bool
    direct_core_import_allowed: bool
    source_of_truth_override_allowed: bool
    external_network_access_enabled: bool
    ports_opened: bool
    containers_started: bool
    active_deployment_created: bool
    containerization_ready: bool
    reason_codes: tuple[str, ...]

    def __post_init__(self) -> None:
        expected_prefix = f"mobile_vpn_{self.platform}_"
        if not isinstance(self.hook_id, str) or not self.hook_id.startswith(expected_prefix):
            raise ValueError("hook_id must include mobile platform prefix")
        if not isinstance(self.profile_id, str) or not self.profile_id.startswith("vpn_"):
            raise ValueError("profile_id must reference vpn profile")
        if not isinstance(self.reason_codes, tuple) or not self.reason_codes:
            raise ValueError("reason_codes must be a non-empty tuple")

        required_true = {
            "dashboard_visible": self.dashboard_visible,
            "disable_safe": self.disable_safe,
            "policy_disable_supported": self.policy_disable_supported,
            "containerization_ready": self.containerization_ready,
        }
        for field_name, value in required_true.items():
            if value is not True:
                raise ValueError(f"{field_name} must remain true")

        required_false = {
            "system_api_call_allowed": self.system_api_call_allowed,
            "tunnel_creation_allowed": self.tunnel_creation_allowed,
            "permission_prompt_allowed": self.permission_prompt_allowed,
            "secret_material_embedded": self.secret_material_embedded,
            "runtime_mutation_allowed": self.runtime_mutation_allowed,
            "direct_core_import_allowed": self.direct_core_import_allowed,
            "source_of_truth_override_allowed": self.source_of_truth_override_allowed,
            "external_network_access_enabled": self.external_network_access_enabled,
            "ports_opened": self.ports_opened,
            "containers_started": self.containers_started,
            "active_deployment_created": self.active_deployment_created,
        }
        for field_name, value in required_false.items():
            if value is not False:
                raise ValueError(f"{field_name} must remain false")

    def to_dict(self) -> dict[str, Any]:
        return {
            "hook_id": self.hook_id,
            "platform": self.platform,
            "profile_id": self.profile_id,
            "system_api_call_allowed": self.system_api_call_allowed,
            "tunnel_creation_allowed": self.tunnel_creation_allowed,
            "permission_prompt_allowed": self.permission_prompt_allowed,
            "secret_material_embedded": self.secret_material_embedded,
            "dashboard_visible": self.dashboard_visible,
            "disable_safe": self.disable_safe,
            "policy_disable_supported": self.policy_disable_supported,
            "runtime_mutation_allowed": self.runtime_mutation_allowed,
            "direct_core_import_allowed": self.direct_core_import_allowed,
            "source_of_truth_override_allowed": self.source_of_truth_override_allowed,
            "external_network_access_enabled": self.external_network_access_enabled,
            "ports_opened": self.ports_opened,
            "containers_started": self.containers_started,
            "active_deployment_created": self.active_deployment_created,
            "containerization_ready": self.containerization_ready,
            "reason_codes": list(self.reason_codes),
        }


def build_default_mobile_vpn_hooks() -> tuple[MobileVpnHookContract, ...]:
    return (
        MobileVpnHookContract(
            hook_id="mobile_vpn_android_disabled_hook",
            platform="android",
            profile_id="vpn_mobile_profile",
            system_api_call_allowed=False,
            tunnel_creation_allowed=False,
            permission_prompt_allowed=False,
            secret_material_embedded=False,
            dashboard_visible=True,
            disable_safe=True,
            policy_disable_supported=True,
            runtime_mutation_allowed=False,
            direct_core_import_allowed=False,
            source_of_truth_override_allowed=False,
            external_network_access_enabled=False,
            ports_opened=False,
            containers_started=False,
            active_deployment_created=False,
            containerization_ready=True,
            reason_codes=("android_vpn_hook_disabled_until_platform_batch",),
        ),
        MobileVpnHookContract(
            hook_id="mobile_vpn_ios_disabled_hook",
            platform="ios",
            profile_id="vpn_mobile_profile",
            system_api_call_allowed=False,
            tunnel_creation_allowed=False,
            permission_prompt_allowed=False,
            secret_material_embedded=False,
            dashboard_visible=True,
            disable_safe=True,
            policy_disable_supported=True,
            runtime_mutation_allowed=False,
            direct_core_import_allowed=False,
            source_of_truth_override_allowed=False,
            external_network_access_enabled=False,
            ports_opened=False,
            containers_started=False,
            active_deployment_created=False,
            containerization_ready=True,
            reason_codes=("ios_vpn_hook_disabled_until_platform_batch",),
        ),
    )
