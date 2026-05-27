from __future__ import annotations

from pathlib import Path
import json
from typing import Any

import yaml


ACCEPTANCE_DOC = Path("docs/architecture/network_security/phase_2_network_security_acceptance_v1.md")
ARCHITECTURE_BLUEPRINT = Path("MAKSIMAR_CORE_LIB/architecture_map/architecture_blueprint.json")
JARVIS_CONTEXT_DOC = Path("docs/architecture/network_security/phase_2_network_security_jarvis_context_v1.md")

PHASE_2_REQUIRED_FILES = (
    # 2.1
    Path("MAKSIMAR_CORE_LIB/network_security/__init__.py"),
    Path("MAKSIMAR_CORE_LIB/network_security/network_backend_adapter_contract.py"),
    Path("MAKSIMAR_CORE_LIB/network_security/vpn_policy_disable_contract.py"),
    Path("tests/network_security/test_network_backend_adapter_contract_smoke.py"),
    Path("tests/network_security/test_vpn_policy_can_disable_runtime_smoke.py"),
    Path("tests/network_security/test_vpn_disabled_state_dashboard_visible_smoke.py"),
    # 2.2
    Path("MAKSIMAR_CORE_LIB/network_security/vpn_profile_contract.py"),
    Path("MAKSIMAR_CORE_LIB/network_security/vpn_session_contract.py"),
    Path("MAKSIMAR_CORE_LIB/network_security/egress_policy_contract.py"),
    Path("MAKSIMAR_CORE_LIB/network_security/mobile_vpn_hook_contract.py"),
    Path("tests/network_security/test_vpn_profile_contract_smoke.py"),
    Path("tests/network_security/test_vpn_capability_required_server_smoke.py"),
    Path("tests/network_security/test_egress_policy_contract_smoke.py"),
    Path("tests/network_security/test_mobile_vpn_hook_contract_smoke.py"),
    # 2.3
    Path("MAKSIMAR_SERVER/NETWORK_SECURITY_RUNTIME/__init__.py"),
    Path("MAKSIMAR_SERVER/NETWORK_SECURITY_RUNTIME/vpn_session_registry.py"),
    Path("MAKSIMAR_SERVER/NETWORK_SECURITY_RUNTIME/vpn_policy_runtime.py"),
    Path("MAKSIMAR_SERVER/NETWORK_SECURITY_RUNTIME/egress_guard_runtime.py"),
    Path("MAKSIMAR_SERVER/NETWORK_SECURITY_RUNTIME/network_posture_summary_builder.py"),
    Path("tests/network_security/test_vpn_session_registry_smoke.py"),
    Path("tests/network_security/test_vpn_policy_runtime_smoke.py"),
    Path("tests/network_security/test_egress_guard_runtime_smoke.py"),
    Path("tests/network_security/test_network_posture_summary_builder_smoke.py"),
    # 2.4
    Path("MAKSIMAR_SERVER/NETWORK_SECURITY_RUNTIME/vpn_dashboard_read_model_builder.py"),
    Path("MAKSIMAR_CORE_LIB/network_security/vpn_status_read_model.py"),
    Path("MAKSIMAR_CORE_LIB/network_security/egress_policy_read_model.py"),
    Path("tools/vpn_status_preview.py"),
    Path("tests/network_security/test_vpn_dashboard_read_model_builder_smoke.py"),
    Path("tests/network_security/test_vpn_status_preview_smoke.py"),
    # 2.5
    Path("ANDROID_SHELL/network_vpn/README.md"),
    Path("ANDROID_SHELL/network_vpn/vpn_profile_models.py"),
    Path("ANDROID_SHELL/network_vpn/vpn_state_bridge.py"),
    Path("ANDROID_SHELL/network_vpn/vpn_sync_contract.py"),
    Path("ANDROID_SHELL/network_vpn/vpn_permission_state.py"),
    Path("ANDROID_SHELL/network_vpn/android_vpn_policy_binding.py"),
    Path("tests/mobile_network/test_vpn_capability_required_android_smoke.py"),
    Path("tests/mobile_network/test_android_vpn_profile_contract_smoke.py"),
    Path("tests/mobile_network/test_android_vpn_state_bridge_smoke.py"),
    Path("tests/mobile_network/test_android_vpn_sync_contract_smoke.py"),
    Path("tests/mobile_network/test_android_vpn_policy_binding_smoke.py"),
    # 2.6
    Path("IOS_SHELL/network_vpn/README.md"),
    Path("IOS_SHELL/network_vpn/vpn_profile_models.py"),
    Path("IOS_SHELL/network_vpn/vpn_state_bridge.py"),
    Path("IOS_SHELL/network_vpn/vpn_sync_contract.py"),
    Path("IOS_SHELL/network_vpn/vpn_permission_state.py"),
    Path("IOS_SHELL/network_vpn/ios_vpn_policy_binding.py"),
    Path("tests/mobile_network/test_vpn_capability_required_ios_smoke.py"),
    Path("tests/mobile_network/test_ios_vpn_profile_contract_smoke.py"),
    Path("tests/mobile_network/test_ios_vpn_state_bridge_smoke.py"),
    Path("tests/mobile_network/test_ios_vpn_sync_contract_smoke.py"),
    Path("tests/mobile_network/test_ios_vpn_policy_binding_smoke.py"),
    # 2.7
    Path("shared_mobile_core/p2p_mesh_network/__init__.py"),
    Path("shared_mobile_core/p2p_mesh_network/p2p_mesh_contract.py"),
    Path("shared_mobile_core/p2p_mesh_network/floating_master_contract.py"),
    Path("shared_mobile_core/p2p_mesh_network/device_role_election_contract.py"),
    Path("shared_mobile_core/p2p_mesh_network/server_presence_contract.py"),
    Path("MAKSIMAR_SERVER/NETWORK_SECURITY_RUNTIME/p2p_mesh_observer_read_model_builder.py"),
    Path("tests/mobile_p2p/test_p2p_mesh_contract_smoke.py"),
    Path("tests/mobile_p2p/test_floating_master_contract_smoke.py"),
    Path("tests/mobile_p2p/test_device_role_election_contract_smoke.py"),
    Path("tests/mobile_p2p/test_server_presence_switches_to_premium_mode_smoke.py"),
    Path("tests/mobile_p2p/test_p2p_mesh_observer_read_model_builder_smoke.py"),
    # 2.8
    Path("ANDROID_SHELL/p2p_node_adapter/README.md"),
    Path("ANDROID_SHELL/p2p_node_adapter/p2p_node_state_bridge.py"),
    Path("ANDROID_SHELL/p2p_node_adapter/floating_master_state.py"),
    Path("IOS_SHELL/p2p_node_adapter/README.md"),
    Path("IOS_SHELL/p2p_node_adapter/p2p_node_state_bridge.py"),
    Path("IOS_SHELL/p2p_node_adapter/floating_master_state.py"),
    Path("tests/mobile_p2p/test_android_p2p_node_state_bridge_smoke.py"),
    Path("tests/mobile_p2p/test_ios_p2p_node_state_bridge_smoke.py"),
    # 2.9
    Path("CONTAINER_DEPLOYMENT/cubes/network_security/container_contract.yaml"),
    Path("CONTAINER_DEPLOYMENT/cubes/network_security/network_policy.yaml"),
    Path("CONTAINER_DEPLOYMENT/cubes/network_security/runtime_profile.yaml"),
    Path("CONTAINER_DEPLOYMENT/cubes/network_security/healthcheck_contract.yaml"),
    Path("CONTAINER_DEPLOYMENT/cubes/network_security/readiness_probe_contract.yaml"),
    Path("tests/container_readiness/test_network_security_container_contract_smoke.py"),
    Path("tests/container_readiness/test_network_security_core_write_false_smoke.py"),
    Path("tests/container_readiness/test_network_security_runtime_mutation_false_smoke.py"),
    # 2.10
    ACCEPTANCE_DOC,
    JARVIS_CONTEXT_DOC,
    Path("tests/network_security/test_phase_2_acceptance_smoke.py"),
)

CUBE_YAML_FILES = (
    Path("CONTAINER_DEPLOYMENT/cubes/network_security/container_contract.yaml"),
    Path("CONTAINER_DEPLOYMENT/cubes/network_security/network_policy.yaml"),
    Path("CONTAINER_DEPLOYMENT/cubes/network_security/runtime_profile.yaml"),
    Path("CONTAINER_DEPLOYMENT/cubes/network_security/healthcheck_contract.yaml"),
    Path("CONTAINER_DEPLOYMENT/cubes/network_security/readiness_probe_contract.yaml"),
)


def _load_yaml(path: Path) -> dict[str, Any]:
    payload = yaml.safe_load(path.read_text(encoding="utf-8"))
    assert isinstance(payload, dict)
    return payload


def test_phase_2_acceptance_all_expected_files_exist() -> None:
    missing = [str(path) for path in PHASE_2_REQUIRED_FILES if not path.exists()]
    assert missing == []


def test_phase_2_acceptance_document_declares_boundaries_and_blocks_execution() -> None:
    text = ACCEPTANCE_DOC.read_text(encoding="utf-8")

    required_markers = (
        "PHASE 2",
        "MAKSIMAR_CORE_LIB/network_security",
        "MAKSIMAR_SERVER/NETWORK_SECURITY_RUNTIME",
        "shared_mobile_core/p2p_mesh_network",
        "CONTAINER_DEPLOYMENT/cubes/network_security",
        "No real VPN tunnel creation",
        "No real P2P networking",
        "No peer discovery",
        "No sockets opened",
        "No ports opened",
        "No external network access enabled",
        "No Android/iOS system network API execution",
        "No floating-master election execution",
        "No runtime mutation",
        "No core write",
        "No canonical write",
        "No source-of-truth override",
        "No active Docker deployment",
        "No active Compose deployment",
        "No production deployment",
        "Operator approval is required",
    )

    for marker in required_markers:
        assert marker in text


def test_phase_2_acceptance_container_readiness_remains_read_only() -> None:
    for path in CUBE_YAML_FILES:
        payload = _load_yaml(path)
        flags = payload["safety_flags"]

        assert flags["read_only_readiness_only"] is True
        assert flags["dashboard_visible"] is True
        assert flags["operator_approval_required"] is True
        assert flags["active_deployment_allowed"] is False
        assert flags["active_docker_deployment_allowed"] is False
        assert flags["active_compose_deployment_allowed"] is False
        assert flags["docker_start_allowed"] is False
        assert flags["compose_start_allowed"] is False
        assert flags["production_deployment_allowed"] is False
        assert flags["ports_opened"] is False
        assert flags["external_network_access_enabled"] is False
        assert flags["runtime_mutation_allowed"] is False
        assert flags["runtime_network_mutation_allowed"] is False
        assert flags["core_write_allowed"] is False
        assert flags["canonical_write_allowed"] is False
        assert flags["source_of_truth_override_allowed"] is False
        assert flags["direct_execution_allowed"] is False
        assert flags["privileged"] is False
        assert flags["host_network"] is False
        assert flags["host_pid"] is False


def test_phase_2_jarvis_context_document_explains_architecture_without_being_gate() -> None:
    assert JARVIS_CONTEXT_DOC.exists()

    text = JARVIS_CONTEXT_DOC.read_text(encoding="utf-8")

    required_markers = (
        "JARVIS Context",
        "not a blocking policy gate",
        "not a restriction against future optimization",
        "MAKSIMAR_CORE_LIB/network_security",
        "MAKSIMAR_SERVER/NETWORK_SECURITY_RUNTIME",
        "shared_mobile_core/p2p_mesh_network",
        "ANDROID_SHELL/network_vpn",
        "IOS_SHELL/network_vpn",
        "ANDROID_SHELL/p2p_node_adapter",
        "IOS_SHELL/p2p_node_adapter",
        "CONTAINER_DEPLOYMENT/cubes/network_security",
        "real VPN adapter implementation",
        "real P2P discovery implementation",
        "Floating Master election",
        "dashboard control-plane handoff",
        "container runtime integration",
        "telemetry and observability",
    )

    for marker in required_markers:
        assert marker in text


def test_phase_2_acceptance_blueprint_registers_mobile_and_shared_surfaces() -> None:
    text = ARCHITECTURE_BLUEPRINT.read_text(encoding="utf-8")

    required_markers = (
        "ANDROID_SHELL",
        "IOS_SHELL",
        "shared_mobile_core",
    )

    for marker in required_markers:
        assert marker in text


def test_phase_2_acceptance_blueprint_import_mapping_is_registered() -> None:
    payload = json.loads(ARCHITECTURE_BLUEPRINT.read_text(encoding="utf-8"))

    def walk(obj):
        if isinstance(obj, dict):
            yield obj
            for value in obj.values():
                yield from walk(value)
        elif isinstance(obj, list):
            for item in obj:
                yield from walk(item)

    layers = [item for item in walk(payload) if isinstance(item, dict)]

    clients = next(
        item for item in layers
        if item.get("id") == "CLIENTS_MOBILE"
    )
    platform = next(
        item for item in layers
        if item.get("id") == "PLATFORM_BINDINGS_READ_MODELS"
    )

    assert "ANDROID_SHELL" in clients["path_prefixes"]
    assert "IOS_SHELL" in clients["path_prefixes"]
    assert "ANDROID_SHELL" in clients["module_prefixes"]
    assert "IOS_SHELL" in clients["module_prefixes"]
    assert "PLATFORM_BINDINGS_READ_MODELS" in clients["allowed_import_layer_ids"]

    assert "shared_mobile_core" in platform["path_prefixes"]
    assert "shared_mobile_core" in platform["module_prefixes"]
