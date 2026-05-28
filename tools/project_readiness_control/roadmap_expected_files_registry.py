"""Roadmap expected files registry for MAKSIMAR project readiness control.

The registry must include the full active phase, not only completed batches.
This prevents false READY reports when only a subset of roadmap batches exists.
"""

from __future__ import annotations

from dataclasses import dataclass

from MAKSIMAR_CORE_LIB.architecture_map.project_file_readiness_models import (
    ExpectedProjectFile,
)


@dataclass(frozen=True)
class RoadmapExpectedBatch:
    """Expected files for one roadmap batch."""

    batch_id: str
    title: str
    expected_files: tuple[ExpectedProjectFile, ...]

    def __post_init__(self) -> None:
        if not self.batch_id:
            raise ValueError("batch_id must be non-empty")

        if not self.title:
            raise ValueError("title must be non-empty")

        if not self.expected_files:
            raise ValueError("expected_files must be non-empty")


ROADMAP_EXPECTED_BATCHES: tuple[RoadmapExpectedBatch, ...] = (
    RoadmapExpectedBatch(
        batch_id="0.1",
        title="Existing Scanner Discovery",
        expected_files=(
            ExpectedProjectFile(
                path="docs/architecture/open_source_integration/existing_scanner_discovery_v1.md",
                role="doc",
                description="Scanner discovery acceptance document.",
            ),
            ExpectedProjectFile(
                path="tools/project_readiness_control/scanner_discovery.py",
                role="tool",
                description="Read-only scanner/vendor gate discovery wrapper.",
            ),
            ExpectedProjectFile(
                path="tests/vendor_security_gate/test_existing_repo_scanner_discovery_smoke.py",
                role="test",
                description="Discovery report smoke test.",
            ),
            ExpectedProjectFile(
                path="tests/vendor_security_gate/test_existing_scanner_extend_not_duplicate_smoke.py",
                role="test",
                description="No duplicate scanner smoke test.",
            ),
        ),
    ),
    RoadmapExpectedBatch(
        batch_id="0.2",
        title="Repository Scan Models",
        expected_files=(
            ExpectedProjectFile(
                path="MAKSIMAR_CORE_LIB/security_layer/repository_scan_models.py",
                role="source",
                description="Repository scan result models.",
            ),
            ExpectedProjectFile(
                path="MAKSIMAR_CORE_LIB/security_layer/repository_risk_summary_builder.py",
                role="source",
                description="Repository risk summary builder.",
            ),
            ExpectedProjectFile(
                path="MAKSIMAR_CORE_LIB/security_layer/repository_quarantine_policy.py",
                role="source",
                description="Repository quarantine decision policy.",
            ),
            ExpectedProjectFile(
                path="tests/vendor_security_gate/test_repository_secret_detection_contract_smoke.py",
                role="test",
                description="Secret detection contract smoke test.",
            ),
            ExpectedProjectFile(
                path="tests/vendor_security_gate/test_repository_license_scan_contract_smoke.py",
                role="test",
                description="License scan contract smoke test.",
            ),
            ExpectedProjectFile(
                path="tests/vendor_security_gate/test_repository_dependency_risk_scan_contract_smoke.py",
                role="test",
                description="Dependency risk scan contract smoke test.",
            ),
            ExpectedProjectFile(
                path="tests/vendor_security_gate/test_repository_quarantine_decision_smoke.py",
                role="test",
                description="Repository quarantine decision smoke test.",
            ),
        ),
    ),
    RoadmapExpectedBatch(
        batch_id="0.3",
        title="Repository Scan Runtime",
        expected_files=(
            ExpectedProjectFile(
                path="MAKSIMAR_SERVER/EXTERNAL_REPO_SECURITY_RUNTIME/__init__.py",
                role="source",
                description="External repository security runtime package.",
            ),
            ExpectedProjectFile(
                path="MAKSIMAR_SERVER/EXTERNAL_REPO_SECURITY_RUNTIME/repository_scan_runtime.py",
                role="source",
                description="Repository scan runtime flow.",
            ),
            ExpectedProjectFile(
                path="tests/vendor_security_gate/test_repository_scan_runtime_smoke.py",
                role="test",
                description="Repository scan runtime smoke test.",
            ),
            ExpectedProjectFile(
                path="tests/vendor_security_gate/test_repository_dangerous_script_detection_contract_smoke.py",
                role="test",
                description="Dangerous script detection smoke test.",
            ),
        ),
    ),
    RoadmapExpectedBatch(
        batch_id="0.4",
        title="Pytest Output Hygiene",
        expected_files=(
            ExpectedProjectFile(
                path="conftest.py",
                role="config",
                description="Root pytest hooks with full-platform report gate.",
            ),
            ExpectedProjectFile(
                path="MAKSIMAR_CORE_LIB/architecture_map/pytest_architecture_plugin.py",
                role="source",
                description="Architecture pytest plugin guarded by full-platform report mode.",
            ),
            ExpectedProjectFile(
                path="MAKSIMAR_CORE_LIB/architecture_map/pytest_report_gate.py",
                role="source",
                description="Core-local pytest full-platform report gate.",
            ),
            ExpectedProjectFile(
                path="tests/architecture_map/test_pytest_report_gate_env_contract_smoke.py",
                role="test",
                description="Report gate env/option contract smoke test.",
            ),
            ExpectedProjectFile(
                path="tests/architecture_map/test_pytest_target_mode_does_not_emit_full_reports_smoke.py",
                role="test",
                description="Target pytest output hygiene smoke test.",
            ),
            ExpectedProjectFile(
                path="tests/architecture_map/test_pytest_full_auto_mode_emits_full_reports_smoke.py",
                role="test",
                description="Full-platform report mode smoke test.",
            ),
        ),
    ),
    RoadmapExpectedBatch(
        batch_id="0.5",
        title="Project Readiness Runner Core",
        expected_files=(
            ExpectedProjectFile(
                path="tools/project_readiness_control/__init__.py",
                role="tool",
                description="Project readiness control package.",
            ),
            ExpectedProjectFile(
                path="tools/project_readiness_control/run_readiness_gate.py",
                role="tool",
                description="Unified readiness gate runner.",
            ),
            ExpectedProjectFile(
                path="tools/project_readiness_control/target_test_runner.py",
                role="tool",
                description="Target test runner.",
            ),
            ExpectedProjectFile(
                path="tools/project_readiness_control/batch_gate_runner.py",
                role="tool",
                description="Batch gate runner.",
            ),
            ExpectedProjectFile(
                path="tools/project_readiness_control/full_platform_auto_runner.py",
                role="tool",
                description="Full platform auto runner.",
            ),
            ExpectedProjectFile(
                path="tests/project_readiness_control/test_target_test_runner_smoke.py",
                role="test",
                description="Target test runner smoke test.",
            ),
            ExpectedProjectFile(
                path="tests/project_readiness_control/test_batch_gate_runner_smoke.py",
                role="test",
                description="Batch gate runner smoke test.",
            ),
            ExpectedProjectFile(
                path="tests/project_readiness_control/test_full_platform_auto_runner_smoke.py",
                role="test",
                description="Full platform auto runner smoke test.",
            ),
        ),
    ),
    RoadmapExpectedBatch(
        batch_id="0.6",
        title="Project Readiness Sub-Runners",
        expected_files=(
            ExpectedProjectFile(
                path="tools/project_readiness_control/surface_inventory.py",
                role="tool",
                description="Surface inventory runner.",
            ),
            ExpectedProjectFile(
                path="tools/project_readiness_control/semantic_duplicate_scan_runner.py",
                role="tool",
                description="Semantic duplicate scan runner.",
            ),
            ExpectedProjectFile(
                path="tools/project_readiness_control/roadmap_ci_runner.py",
                role="tool",
                description="Roadmap CI runner.",
            ),
            ExpectedProjectFile(
                path="tools/project_readiness_control/forbidden_marker_scan.py",
                role="tool",
                description="Forbidden marker scan runner.",
            ),
            ExpectedProjectFile(
                path="tools/project_readiness_control/xray_runner.py",
                role="tool",
                description="X-Ray runner.",
            ),
            ExpectedProjectFile(
                path="tools/project_readiness_control/drift_guard_runner.py",
                role="tool",
                description="Drift Guard runner.",
            ),
            ExpectedProjectFile(
                path="tools/project_readiness_control/dirty_surface_classifier.py",
                role="tool",
                description="Dirty surface classifier.",
            ),
            ExpectedProjectFile(
                path="tests/project_readiness_control/test_surface_inventory_smoke.py",
                role="test",
                description="Surface inventory smoke test.",
            ),
            ExpectedProjectFile(
                path="tests/project_readiness_control/test_semantic_duplicate_runner_smoke.py",
                role="test",
                description="Semantic duplicate runner smoke test.",
            ),
            ExpectedProjectFile(
                path="tests/project_readiness_control/test_roadmap_ci_runner_smoke.py",
                role="test",
                description="Roadmap CI runner smoke test.",
            ),
            ExpectedProjectFile(
                path="tests/project_readiness_control/test_forbidden_marker_scan_smoke.py",
                role="test",
                description="Forbidden marker scan smoke test.",
            ),
            ExpectedProjectFile(
                path="tests/project_readiness_control/test_xray_runner_smoke.py",
                role="test",
                description="X-Ray runner smoke test.",
            ),
            ExpectedProjectFile(
                path="tests/project_readiness_control/test_drift_guard_runner_smoke.py",
                role="test",
                description="Drift Guard runner smoke test.",
            ),
            ExpectedProjectFile(
                path="tests/project_readiness_control/test_dirty_surface_classifier_smoke.py",
                role="test",
                description="Dirty surface classifier smoke test.",
            ),
        ),
    ),
    RoadmapExpectedBatch(
        batch_id="0.7",
        title="Readiness Runtime JSON + Dashboard Export",
        expected_files=(
            ExpectedProjectFile(
                path="tools/project_readiness_control/acceptance_evidence_collector.py",
                role="tool",
                description="Acceptance evidence collector.",
            ),
            ExpectedProjectFile(
                path="tools/project_readiness_control/dashboard_readiness_export.py",
                role="tool",
                description="Dashboard readiness JSON export.",
            ),
            ExpectedProjectFile(
                path="MAKSIMAR_CORE_LIB/readiness_control/readiness_status_read_model.py",
                role="source",
                description="Readiness status read model.",
            ),
            ExpectedProjectFile(
                path="tests/project_readiness_control/test_acceptance_evidence_collector_smoke.py",
                role="test",
                description="Acceptance evidence collector smoke test.",
            ),
            ExpectedProjectFile(
                path="tests/project_readiness_control/test_dashboard_readiness_export_smoke.py",
                role="test",
                description="Dashboard readiness export smoke test.",
            ),
            ExpectedProjectFile(
                path="tests/project_readiness_control/test_readiness_status_read_model_smoke.py",
                role="test",
                description="Readiness status read model smoke test.",
            ),
        ),
    ),
    RoadmapExpectedBatch(
        batch_id="0.8",
        title="PHASE 0 Acceptance",
        expected_files=(
            ExpectedProjectFile(
                path="docs/architecture/foundation/phase_0_readiness_output_hygiene_acceptance_v1.md",
                role="doc",
                description="PHASE 0 acceptance document.",
            ),
            ExpectedProjectFile(
                path="tests/project_readiness_control/test_phase_0_acceptance_smoke.py",
                role="test",
                description="PHASE 0 acceptance smoke test.",
            ),
        ),
    ),
 RoadmapExpectedBatch(
  batch_id="1.1",
  title="Open Source Exclusion Registry",
  expected_files=(
   ExpectedProjectFile(
    path="docs/architecture/open_source_integration/open_source_exclusion_registry_v1.md",
    role="doc",
    description="Open-source exclusion registry documentation.",
   ),
   ExpectedProjectFile(
    path="docs/architecture/open_source_integration/open_source_exclusion_registry_v1.json",
    role="doc",
    description="Machine-readable open-source exclusion registry.",
   ),
   ExpectedProjectFile(
    path="tests/open_source_integration/test_open_source_exclusion_registry_schema_smoke.py",
    role="test",
    description="Open-source exclusion registry schema smoke test.",
   ),
   ExpectedProjectFile(
    path="tests/open_source_integration/test_exclusion_registry_no_core_dependencies_smoke.py",
    role="test",
    description="Open-source exclusion registry no-core-dependencies smoke test.",
   ),
  ),
 ),
 RoadmapExpectedBatch(
  batch_id="1.2",
  title="Canonical Capability Registry Models",
  expected_files=(
   ExpectedProjectFile(
    path="MAKSIMAR_CORE_LIB/capability_registry/__init__.py",
    role="source",
    description="Canonical capability registry package.",
   ),
   ExpectedProjectFile(
    path="MAKSIMAR_CORE_LIB/capability_registry/capability_registry_models.py",
    role="source",
    description="Canonical capability registry models.",
   ),
   ExpectedProjectFile(
    path="docs/architecture/open_source_integration/canonical_capability_registry_v1.yaml",
    role="doc",
    description="Canonical capability registry YAML.",
   ),
   ExpectedProjectFile(
    path="tests/capability_registry/test_capability_registry_models_smoke.py",
    role="test",
    description="Canonical capability registry models smoke test.",
   ),
  ),
 ),
 RoadmapExpectedBatch(
  batch_id="1.3",
  title="Capability Registry Loader / Summary",
  expected_files=(
   ExpectedProjectFile(
    path="MAKSIMAR_CORE_LIB/capability_registry/capability_registry_loader.py",
    role="source",
    description="Capability registry loader.",
   ),
   ExpectedProjectFile(
    path="MAKSIMAR_CORE_LIB/capability_registry/capability_registry_summary_builder.py",
    role="source",
    description="Capability registry summary builder.",
   ),
   ExpectedProjectFile(
    path="tests/capability_registry/test_capability_registry_loader_smoke.py",
    role="test",
    description="Capability registry loader smoke test.",
   ),
   ExpectedProjectFile(
    path="tests/capability_registry/test_capability_registry_summary_builder_smoke.py",
    role="test",
    description="Capability registry summary builder smoke test.",
   ),
  ),
 ),
 RoadmapExpectedBatch(
  batch_id="1.4",
  title="Truth Status Marking",
  expected_files=(
   ExpectedProjectFile(
    path="MAKSIMAR_CORE_LIB/capability_registry/capability_truth_status_models.py",
    role="source",
    description="Capability truth status models.",
   ),
   ExpectedProjectFile(
    path="MAKSIMAR_CORE_LIB/capability_registry/capability_truth_status_loader.py",
    role="source",
    description="Capability truth status loader.",
   ),
   ExpectedProjectFile(
    path="tests/capability_registry/test_capability_truth_status_models_smoke.py",
    role="test",
    description="Capability truth status models smoke test.",
   ),
   ExpectedProjectFile(
    path="tests/capability_registry/test_manifest_only_status_is_not_runtime_smoke.py",
    role="test",
    description="Manifest-only status does not count as runtime smoke test.",
   ),
   ExpectedProjectFile(
    path="tests/capability_registry/test_spec_only_docs_do_not_count_as_implemented_smoke.py",
    role="test",
    description="Spec-only docs do not count as implemented smoke test.",
   ),
  ),
 ),
 RoadmapExpectedBatch(
  batch_id="1.5",
  title="PHASE 1 Acceptance",
  expected_files=(
   ExpectedProjectFile(
    path="docs/architecture/open_source_integration/phase_1_open_source_canonicalization_acceptance_v1.md",
    role="doc",
    description="PHASE 1 open-source canonicalization acceptance document.",
   ),
   ExpectedProjectFile(
    path="tests/open_source_integration/test_phase_1_acceptance_smoke.py",
    role="test",
    description="PHASE 1 acceptance smoke test.",
   ),
  ),
 ),
 RoadmapExpectedBatch(
     batch_id="2.1",
     title="Network Backend Adapter Contract",
     expected_files=(
         ExpectedProjectFile(path="MAKSIMAR_CORE_LIB/network_security/__init__.py", role="source", description="Network security package marker."),
         ExpectedProjectFile(path="MAKSIMAR_CORE_LIB/network_security/network_backend_adapter_contract.py", role="source", description="Network backend adapter contract."),
         ExpectedProjectFile(path="MAKSIMAR_CORE_LIB/network_security/vpn_policy_disable_contract.py", role="source", description="VPN policy-disable contract."),
         ExpectedProjectFile(path="tests/network_security/test_network_backend_adapter_contract_smoke.py", role="test", description="Network backend adapter contract smoke test."),
         ExpectedProjectFile(path="tests/network_security/test_vpn_policy_can_disable_runtime_smoke.py", role="test", description="VPN policy can disable runtime smoke test."),
         ExpectedProjectFile(path="tests/network_security/test_vpn_disabled_state_dashboard_visible_smoke.py", role="test", description="VPN disabled state dashboard-visible smoke test."),
     ),
 ),
 RoadmapExpectedBatch(
     batch_id="2.2",
     title="VPN Profile / Session / Egress Contracts",
     expected_files=(
         ExpectedProjectFile(path="MAKSIMAR_CORE_LIB/network_security/vpn_profile_contract.py", role="source", description="VPN profile contract."),
         ExpectedProjectFile(path="MAKSIMAR_CORE_LIB/network_security/vpn_session_contract.py", role="source", description="VPN session contract."),
         ExpectedProjectFile(path="MAKSIMAR_CORE_LIB/network_security/egress_policy_contract.py", role="source", description="Egress policy contract."),
         ExpectedProjectFile(path="MAKSIMAR_CORE_LIB/network_security/mobile_vpn_hook_contract.py", role="source", description="Mobile VPN hook contract."),
         ExpectedProjectFile(path="tests/network_security/test_vpn_profile_contract_smoke.py", role="test", description="VPN profile contract smoke test."),
         ExpectedProjectFile(path="tests/network_security/test_vpn_capability_required_server_smoke.py", role="test", description="VPN capability required server smoke test."),
         ExpectedProjectFile(path="tests/network_security/test_egress_policy_contract_smoke.py", role="test", description="Egress policy contract smoke test."),
         ExpectedProjectFile(path="tests/network_security/test_mobile_vpn_hook_contract_smoke.py", role="test", description="Mobile VPN hook contract smoke test."),
     ),
 ),
 RoadmapExpectedBatch(
     batch_id="2.3",
     title="Server VPN Runtime / Read Model",
     expected_files=(
         ExpectedProjectFile(path="MAKSIMAR_SERVER/NETWORK_SECURITY_RUNTIME/__init__.py", role="source", description="Network security runtime package marker."),
         ExpectedProjectFile(path="MAKSIMAR_SERVER/NETWORK_SECURITY_RUNTIME/vpn_session_registry.py", role="source", description="VPN session registry."),
         ExpectedProjectFile(path="MAKSIMAR_SERVER/NETWORK_SECURITY_RUNTIME/vpn_policy_runtime.py", role="source", description="VPN policy runtime."),
         ExpectedProjectFile(path="MAKSIMAR_SERVER/NETWORK_SECURITY_RUNTIME/egress_guard_runtime.py", role="source", description="Egress guard runtime."),
         ExpectedProjectFile(path="MAKSIMAR_SERVER/NETWORK_SECURITY_RUNTIME/network_posture_summary_builder.py", role="source", description="Network posture summary builder."),
         ExpectedProjectFile(path="tests/network_security/test_vpn_session_registry_smoke.py", role="test", description="VPN session registry smoke test."),
         ExpectedProjectFile(path="tests/network_security/test_vpn_policy_runtime_smoke.py", role="test", description="VPN policy runtime smoke test."),
         ExpectedProjectFile(path="tests/network_security/test_egress_guard_runtime_smoke.py", role="test", description="Egress guard runtime smoke test."),
         ExpectedProjectFile(path="tests/network_security/test_network_posture_summary_builder_smoke.py", role="test", description="Network posture summary builder smoke test."),
     ),
 ),
 RoadmapExpectedBatch(
     batch_id="2.4",
     title="VPN Dashboard Read Models / Preview",
     expected_files=(
         ExpectedProjectFile(path="MAKSIMAR_SERVER/NETWORK_SECURITY_RUNTIME/vpn_dashboard_read_model_builder.py", role="source", description="VPN dashboard read-model builder."),
         ExpectedProjectFile(path="MAKSIMAR_CORE_LIB/network_security/vpn_status_read_model.py", role="source", description="VPN status read model."),
         ExpectedProjectFile(path="MAKSIMAR_CORE_LIB/network_security/egress_policy_read_model.py", role="source", description="Egress policy read model."),
         ExpectedProjectFile(path="tools/vpn_status_preview.py", role="tool", description="VPN status terminal preview."),
         ExpectedProjectFile(path="tests/network_security/test_vpn_dashboard_read_model_builder_smoke.py", role="test", description="VPN dashboard read-model builder smoke test."),
         ExpectedProjectFile(path="tests/network_security/test_vpn_status_preview_smoke.py", role="test", description="VPN status preview smoke test."),
     ),
 ),
 RoadmapExpectedBatch(
     batch_id="2.5",
     title="Android VPN Integration",
     expected_files=(
         ExpectedProjectFile(path="ANDROID_SHELL/network_vpn/README.md", role="doc", description="Android VPN integration README."),
         ExpectedProjectFile(path="ANDROID_SHELL/network_vpn/vpn_profile_models.py", role="source", description="Android VPN profile models."),
         ExpectedProjectFile(path="ANDROID_SHELL/network_vpn/vpn_state_bridge.py", role="source", description="Android VPN state bridge."),
         ExpectedProjectFile(path="ANDROID_SHELL/network_vpn/vpn_sync_contract.py", role="source", description="Android VPN sync contract."),
         ExpectedProjectFile(path="ANDROID_SHELL/network_vpn/vpn_permission_state.py", role="source", description="Android VPN permission state."),
         ExpectedProjectFile(path="ANDROID_SHELL/network_vpn/android_vpn_policy_binding.py", role="source", description="Android VPN policy binding."),
         ExpectedProjectFile(path="tests/mobile_network/test_vpn_capability_required_android_smoke.py", role="test", description="Android VPN capability required smoke test."),
         ExpectedProjectFile(path="tests/mobile_network/test_android_vpn_profile_contract_smoke.py", role="test", description="Android VPN profile contract smoke test."),
         ExpectedProjectFile(path="tests/mobile_network/test_android_vpn_state_bridge_smoke.py", role="test", description="Android VPN state bridge smoke test."),
         ExpectedProjectFile(path="tests/mobile_network/test_android_vpn_sync_contract_smoke.py", role="test", description="Android VPN sync contract smoke test."),
         ExpectedProjectFile(path="tests/mobile_network/test_android_vpn_policy_binding_smoke.py", role="test", description="Android VPN policy binding smoke test."),
     ),
 ),
 RoadmapExpectedBatch(
     batch_id="2.6",
     title="iOS VPN Integration",
     expected_files=(
         ExpectedProjectFile(path="IOS_SHELL/network_vpn/README.md", role="doc", description="iOS VPN integration README."),
         ExpectedProjectFile(path="IOS_SHELL/network_vpn/vpn_profile_models.py", role="source", description="iOS VPN profile models."),
         ExpectedProjectFile(path="IOS_SHELL/network_vpn/vpn_state_bridge.py", role="source", description="iOS VPN state bridge."),
         ExpectedProjectFile(path="IOS_SHELL/network_vpn/vpn_sync_contract.py", role="source", description="iOS VPN sync contract."),
         ExpectedProjectFile(path="IOS_SHELL/network_vpn/vpn_permission_state.py", role="source", description="iOS VPN permission state."),
         ExpectedProjectFile(path="IOS_SHELL/network_vpn/ios_vpn_policy_binding.py", role="source", description="iOS VPN policy binding."),
         ExpectedProjectFile(path="tests/mobile_network/test_vpn_capability_required_ios_smoke.py", role="test", description="iOS VPN capability required smoke test."),
         ExpectedProjectFile(path="tests/mobile_network/test_ios_vpn_profile_contract_smoke.py", role="test", description="iOS VPN profile contract smoke test."),
         ExpectedProjectFile(path="tests/mobile_network/test_ios_vpn_state_bridge_smoke.py", role="test", description="iOS VPN state bridge smoke test."),
         ExpectedProjectFile(path="tests/mobile_network/test_ios_vpn_sync_contract_smoke.py", role="test", description="iOS VPN sync contract smoke test."),
         ExpectedProjectFile(path="tests/mobile_network/test_ios_vpn_policy_binding_smoke.py", role="test", description="iOS VPN policy binding smoke test."),
     ),
 ),
 RoadmapExpectedBatch(
     batch_id="2.7",
     title="P2P Mesh / Floating Master",
     expected_files=(
         ExpectedProjectFile(path="shared_mobile_core/p2p_mesh_network/__init__.py", role="source", description="Shared P2P mesh package marker."),
         ExpectedProjectFile(path="shared_mobile_core/p2p_mesh_network/p2p_mesh_contract.py", role="source", description="P2P mesh contract."),
         ExpectedProjectFile(path="shared_mobile_core/p2p_mesh_network/floating_master_contract.py", role="source", description="Floating Master contract."),
         ExpectedProjectFile(path="shared_mobile_core/p2p_mesh_network/device_role_election_contract.py", role="source", description="Device role election contract."),
         ExpectedProjectFile(path="shared_mobile_core/p2p_mesh_network/server_presence_contract.py", role="source", description="Server presence contract."),
         ExpectedProjectFile(path="MAKSIMAR_SERVER/NETWORK_SECURITY_RUNTIME/p2p_mesh_observer_read_model_builder.py", role="source", description="P2P mesh observer read-model builder."),
         ExpectedProjectFile(path="tests/mobile_p2p/test_p2p_mesh_contract_smoke.py", role="test", description="P2P mesh contract smoke test."),
         ExpectedProjectFile(path="tests/mobile_p2p/test_floating_master_contract_smoke.py", role="test", description="Floating Master contract smoke test."),
         ExpectedProjectFile(path="tests/mobile_p2p/test_device_role_election_contract_smoke.py", role="test", description="Device role election contract smoke test."),
         ExpectedProjectFile(path="tests/mobile_p2p/test_server_presence_switches_to_premium_mode_smoke.py", role="test", description="Server presence premium mode switch smoke test."),
         ExpectedProjectFile(path="tests/mobile_p2p/test_p2p_mesh_observer_read_model_builder_smoke.py", role="test", description="P2P mesh observer read-model builder smoke test."),
     ),
 ),
 RoadmapExpectedBatch(
     batch_id="2.8",
     title="Android/iOS P2P Node Adapters",
     expected_files=(
         ExpectedProjectFile(path="ANDROID_SHELL/p2p_node_adapter/README.md", role="doc", description="Android P2P node adapter README."),
         ExpectedProjectFile(path="ANDROID_SHELL/p2p_node_adapter/p2p_node_state_bridge.py", role="source", description="Android P2P node state bridge."),
         ExpectedProjectFile(path="ANDROID_SHELL/p2p_node_adapter/floating_master_state.py", role="source", description="Android Floating Master state."),
         ExpectedProjectFile(path="IOS_SHELL/p2p_node_adapter/README.md", role="doc", description="iOS P2P node adapter README."),
         ExpectedProjectFile(path="IOS_SHELL/p2p_node_adapter/p2p_node_state_bridge.py", role="source", description="iOS P2P node state bridge."),
         ExpectedProjectFile(path="IOS_SHELL/p2p_node_adapter/floating_master_state.py", role="source", description="iOS Floating Master state."),
         ExpectedProjectFile(path="tests/mobile_p2p/test_android_p2p_node_state_bridge_smoke.py", role="test", description="Android P2P node state bridge smoke test."),
         ExpectedProjectFile(path="tests/mobile_p2p/test_ios_p2p_node_state_bridge_smoke.py", role="test", description="iOS P2P node state bridge smoke test."),
     ),
 ),
 RoadmapExpectedBatch(
     batch_id="2.9",
     title="Network Container Readiness",
     expected_files=(
         ExpectedProjectFile(path="CONTAINER_DEPLOYMENT/cubes/network_security/container_contract.yaml", role="config", description="Network security container contract."),
         ExpectedProjectFile(path="CONTAINER_DEPLOYMENT/cubes/network_security/network_policy.yaml", role="config", description="Network security network policy."),
         ExpectedProjectFile(path="CONTAINER_DEPLOYMENT/cubes/network_security/runtime_profile.yaml", role="config", description="Network security runtime profile."),
         ExpectedProjectFile(path="CONTAINER_DEPLOYMENT/cubes/network_security/healthcheck_contract.yaml", role="config", description="Network security healthcheck contract."),
         ExpectedProjectFile(path="CONTAINER_DEPLOYMENT/cubes/network_security/readiness_probe_contract.yaml", role="config", description="Network security readiness probe contract."),
         ExpectedProjectFile(path="tests/container_readiness/test_network_security_container_contract_smoke.py", role="test", description="Network security container contract smoke test."),
         ExpectedProjectFile(path="tests/container_readiness/test_network_security_core_write_false_smoke.py", role="test", description="Network security core write false smoke test."),
         ExpectedProjectFile(path="tests/container_readiness/test_network_security_runtime_mutation_false_smoke.py", role="test", description="Network security runtime mutation false smoke test."),
     ),
 ),
 RoadmapExpectedBatch(
     batch_id="2.10",
     title="PHASE 2 Acceptance",
     expected_files=(
         ExpectedProjectFile(path="docs/architecture/network_security/phase_2_network_security_acceptance_v1.md", role="doc", description="PHASE 2 network security acceptance document."),
         ExpectedProjectFile(path="tests/network_security/test_phase_2_acceptance_smoke.py", role="test", description="PHASE 2 network security acceptance smoke test."),
     ),
 ),

    RoadmapExpectedBatch(
        batch_id="3.1",
        title="Chat Core Contracts",
        expected_files=(
            ExpectedProjectFile(path="MAKSIMAR_CORE_LIB/chat_command/__init__.py", role="source", description="Chat command package marker."),
            ExpectedProjectFile(path="MAKSIMAR_CORE_LIB/chat_command/chat_message_contract.py", role="source", description="Chat message contract."),
            ExpectedProjectFile(path="MAKSIMAR_CORE_LIB/chat_command/command_message_contract.py", role="source", description="Command message contract."),
            ExpectedProjectFile(path="MAKSIMAR_CORE_LIB/chat_command/chat_room_contract.py", role="source", description="Chat room contract."),
            ExpectedProjectFile(path="MAKSIMAR_CORE_LIB/chat_command/chat_identity_contract.py", role="source", description="Chat identity contract."),
            ExpectedProjectFile(path="tests/chat_command/test_chat_message_contract_smoke.py", role="test", description="Chat message contract smoke test."),
            ExpectedProjectFile(path="tests/chat_command/test_command_message_contract_smoke.py", role="test", description="Command message contract smoke test."),
            ExpectedProjectFile(path="tests/chat_command/test_chat_room_contract_smoke.py", role="test", description="Chat room contract smoke test."),
            ExpectedProjectFile(path="tests/chat_command/test_chat_identity_contract_smoke.py", role="test", description="Chat identity contract smoke test."),
        ),
    ),
    RoadmapExpectedBatch(
        batch_id="3.2",
        title="Attachments / Offline Delivery Contracts",
        expected_files=(
            ExpectedProjectFile(path="MAKSIMAR_CORE_LIB/chat_command/file_transfer_contract.py", role="source", description="File transfer contract."),
            ExpectedProjectFile(path="MAKSIMAR_CORE_LIB/chat_command/media_attachment_contract.py", role="source", description="Media attachment contract."),
            ExpectedProjectFile(path="MAKSIMAR_CORE_LIB/chat_command/offline_delivery_contract.py", role="source", description="Offline delivery contract."),
            ExpectedProjectFile(path="MAKSIMAR_CORE_LIB/chat_command/server_sync_contract.py", role="source", description="Server sync contract."),
            ExpectedProjectFile(path="MAKSIMAR_CORE_LIB/chat_command/message_encryption_contract.py", role="source", description="Message encryption contract."),
            ExpectedProjectFile(path="tests/chat_command/test_file_transfer_contract_smoke.py", role="test", description="File transfer contract smoke test."),
            ExpectedProjectFile(path="tests/chat_command/test_media_attachment_contract_smoke.py", role="test", description="Media attachment contract smoke test."),
            ExpectedProjectFile(path="tests/chat_command/test_offline_delivery_contract_smoke.py", role="test", description="Offline delivery contract smoke test."),
            ExpectedProjectFile(path="tests/chat_command/test_server_sync_contract_smoke.py", role="test", description="Server sync contract smoke test."),
            ExpectedProjectFile(path="tests/chat_command/test_message_encryption_contract_smoke.py", role="test", description="Message encryption contract smoke test."),
        ),
    ),
    RoadmapExpectedBatch(
        batch_id="3.3",
        title="Chat Command Boundary / OpenIM Adapter Contract",
        expected_files=(
            ExpectedProjectFile(path="MAKSIMAR_CORE_LIB/chat_command/chat_to_command_handoff_contract.py", role="source", description="Chat-to-command handoff contract."),
            ExpectedProjectFile(path="MAKSIMAR_CORE_LIB/chat_command/openim_reference_adapter_contract.py", role="source", description="OpenIM reference adapter contract."),
            ExpectedProjectFile(path="tests/chat_command/test_chat_to_command_handoff_contract_smoke.py", role="test", description="Chat-to-command handoff contract smoke test."),
            ExpectedProjectFile(path="tests/chat_command/test_openim_reference_adapter_contract_smoke.py", role="test", description="OpenIM reference adapter contract smoke test."),
            ExpectedProjectFile(path="tests/chat_command/test_openim_adapter_does_not_define_chat_truth_smoke.py", role="test", description="OpenIM adapter does not define chat truth smoke test."),
            ExpectedProjectFile(path="tests/chat_command/test_spika_matrix_research_only_until_acceptance_smoke.py", role="test", description="Spika/Matrix research-only until acceptance smoke test."),
        ),
    ),
    RoadmapExpectedBatch(
        batch_id="3.4",
        title="Server Chat Runtime",
        expected_files=(
            ExpectedProjectFile(path="MAKSIMAR_SERVER/CHAT_COMMAND_RUNTIME/__init__.py", role="source", description="Server chat runtime package marker."),
            ExpectedProjectFile(path="MAKSIMAR_SERVER/CHAT_COMMAND_RUNTIME/chat_session_registry.py", role="source", description="Chat session registry."),
            ExpectedProjectFile(path="MAKSIMAR_SERVER/CHAT_COMMAND_RUNTIME/message_router_runtime.py", role="source", description="Message router runtime."),
            ExpectedProjectFile(path="MAKSIMAR_SERVER/CHAT_COMMAND_RUNTIME/offline_queue_runtime.py", role="source", description="Offline queue runtime."),
            ExpectedProjectFile(path="MAKSIMAR_SERVER/CHAT_COMMAND_RUNTIME/chat_audit_runtime.py", role="source", description="Chat audit runtime."),
            ExpectedProjectFile(path="tests/chat_command/test_chat_session_registry_smoke.py", role="test", description="Chat session registry smoke test."),
            ExpectedProjectFile(path="tests/chat_command/test_message_router_runtime_smoke.py", role="test", description="Message router runtime smoke test."),
            ExpectedProjectFile(path="tests/chat_command/test_offline_queue_runtime_smoke.py", role="test", description="Offline queue runtime smoke test."),
            ExpectedProjectFile(path="tests/chat_command/test_chat_audit_runtime_smoke.py", role="test", description="Chat audit runtime smoke test."),
            ExpectedProjectFile(path="tests/chat_command/test_chat_runtime_no_direct_execution_smoke.py", role="test", description="Chat runtime no direct execution smoke test."),
        ),
    ),
    RoadmapExpectedBatch(
        batch_id="3.5",
        title="Server File / Media Chat Runtime",
        expected_files=(
            ExpectedProjectFile(path="MAKSIMAR_SERVER/CHAT_COMMAND_RUNTIME/file_transfer_runtime.py", role="source", description="File transfer runtime."),
            ExpectedProjectFile(path="MAKSIMAR_SERVER/CHAT_COMMAND_RUNTIME/media_attachment_runtime.py", role="source", description="Media attachment runtime."),
            ExpectedProjectFile(path="MAKSIMAR_SERVER/CHAT_COMMAND_RUNTIME/server_to_server_sync_runtime.py", role="source", description="Server-to-server sync runtime."),
            ExpectedProjectFile(path="tests/chat_command/test_file_transfer_runtime_smoke.py", role="test", description="File transfer runtime smoke test."),
            ExpectedProjectFile(path="tests/chat_command/test_media_attachment_runtime_smoke.py", role="test", description="Media attachment runtime smoke test."),
            ExpectedProjectFile(path="tests/chat_command/test_server_to_server_sync_runtime_smoke.py", role="test", description="Server-to-server sync runtime smoke test."),
        ),
    ),
    RoadmapExpectedBatch(
        batch_id="3.6",
        title="Android Chat Client",
        expected_files=(
            ExpectedProjectFile(path="ANDROID_SHELL/chat_client/README.md", role="doc", description="Android chat client README."),
            ExpectedProjectFile(path="ANDROID_SHELL/chat_client/chat_sync_contract.py", role="source", description="Android chat sync contract."),
            ExpectedProjectFile(path="ANDROID_SHELL/chat_client/chat_state_bridge.py", role="source", description="Android chat state bridge."),
            ExpectedProjectFile(path="ANDROID_SHELL/chat_client/chat_message_store.py", role="source", description="Android chat message store."),
            ExpectedProjectFile(path="ANDROID_SHELL/chat_client/offline_queue_bridge.py", role="source", description="Android offline queue bridge."),
            ExpectedProjectFile(path="ANDROID_SHELL/chat_client/chat_notification_bridge.py", role="source", description="Android chat notification bridge."),
            ExpectedProjectFile(path="tests/mobile_chat/test_android_chat_sync_contract_smoke.py", role="test", description="Android chat sync contract smoke test."),
            ExpectedProjectFile(path="tests/mobile_chat/test_android_chat_state_bridge_smoke.py", role="test", description="Android chat state bridge smoke test."),
            ExpectedProjectFile(path="tests/mobile_chat/test_android_chat_message_store_smoke.py", role="test", description="Android chat message store smoke test."),
            ExpectedProjectFile(path="tests/mobile_chat/test_android_offline_queue_bridge_smoke.py", role="test", description="Android offline queue bridge smoke test."),
        ),
    ),
    RoadmapExpectedBatch(
        batch_id="3.7",
        title="Android Chat Attachments",
        expected_files=(
            ExpectedProjectFile(path="ANDROID_SHELL/chat_client/file_attachment_bridge.py", role="source", description="Android file attachment bridge."),
            ExpectedProjectFile(path="ANDROID_SHELL/chat_client/media_attachment_bridge.py", role="source", description="Android media attachment bridge."),
            ExpectedProjectFile(path="tests/mobile_chat/test_android_file_attachment_bridge_smoke.py", role="test", description="Android file attachment bridge smoke test."),
            ExpectedProjectFile(path="tests/mobile_chat/test_android_media_attachment_bridge_smoke.py", role="test", description="Android media attachment bridge smoke test."),
        ),
    ),
    RoadmapExpectedBatch(
        batch_id="3.8",
        title="iOS Chat Client",
        expected_files=(
            ExpectedProjectFile(path="IOS_SHELL/chat_client/README.md", role="doc", description="iOS chat client README."),
            ExpectedProjectFile(path="IOS_SHELL/chat_client/chat_sync_contract.py", role="source", description="iOS chat sync contract."),
            ExpectedProjectFile(path="IOS_SHELL/chat_client/chat_state_bridge.py", role="source", description="iOS chat state bridge."),
            ExpectedProjectFile(path="IOS_SHELL/chat_client/chat_message_store.py", role="source", description="iOS chat message store."),
            ExpectedProjectFile(path="IOS_SHELL/chat_client/offline_queue_bridge.py", role="source", description="iOS offline queue bridge."),
            ExpectedProjectFile(path="IOS_SHELL/chat_client/chat_notification_bridge.py", role="source", description="iOS chat notification bridge."),
            ExpectedProjectFile(path="tests/mobile_chat/test_ios_chat_sync_contract_smoke.py", role="test", description="iOS chat sync contract smoke test."),
            ExpectedProjectFile(path="tests/mobile_chat/test_ios_chat_state_bridge_smoke.py", role="test", description="iOS chat state bridge smoke test."),
            ExpectedProjectFile(path="tests/mobile_chat/test_ios_chat_message_store_smoke.py", role="test", description="iOS chat message store smoke test."),
            ExpectedProjectFile(path="tests/mobile_chat/test_ios_offline_queue_bridge_smoke.py", role="test", description="iOS offline queue bridge smoke test."),
        ),
    ),
    RoadmapExpectedBatch(
        batch_id="3.9",
        title="iOS Chat Attachments",
        expected_files=(
            ExpectedProjectFile(path="IOS_SHELL/chat_client/file_attachment_bridge.py", role="source", description="iOS file attachment bridge."),
            ExpectedProjectFile(path="IOS_SHELL/chat_client/media_attachment_bridge.py", role="source", description="iOS media attachment bridge."),
            ExpectedProjectFile(path="tests/mobile_chat/test_ios_file_attachment_bridge_smoke.py", role="test", description="iOS file attachment bridge smoke test."),
            ExpectedProjectFile(path="tests/mobile_chat/test_ios_media_attachment_bridge_smoke.py", role="test", description="iOS media attachment bridge smoke test."),
        ),
    ),
    RoadmapExpectedBatch(
        batch_id="3.10",
        title="Chat Dashboard / Reactive Buttons",
        expected_files=(
            ExpectedProjectFile(path="MAKSIMAR_CORE_LIB/chat_command/chat_system_read_model.py", role="source", description="Chat system read model."),
            ExpectedProjectFile(path="MAKSIMAR_CORE_LIB/chat_command/chat_session_read_model.py", role="source", description="Chat session read model."),
            ExpectedProjectFile(path="MAKSIMAR_CORE_LIB/chat_command/message_queue_read_model.py", role="source", description="Message queue read model."),
            ExpectedProjectFile(path="MAKSIMAR_CORE_LIB/chat_command/file_transfer_read_model.py", role="source", description="File transfer read model."),
            ExpectedProjectFile(path="MAKSIMAR_CORE_LIB/chat_command/chat_operator_intent_models.py", role="source", description="Chat operator intent models."),
            ExpectedProjectFile(path="MAKSIMAR_CORE_LIB/chat_command/chat_button_state_models.py", role="source", description="Chat button state models."),
            ExpectedProjectFile(path="tests/chat_command/test_chat_system_read_model_smoke.py", role="test", description="Chat system read model smoke test."),
            ExpectedProjectFile(path="tests/chat_command/test_chat_session_read_model_smoke.py", role="test", description="Chat session read model smoke test."),
            ExpectedProjectFile(path="tests/chat_command/test_message_queue_read_model_smoke.py", role="test", description="Message queue read model smoke test."),
            ExpectedProjectFile(path="tests/chat_command/test_chat_operator_intent_models_smoke.py", role="test", description="Chat operator intent models smoke test."),
            ExpectedProjectFile(path="tests/chat_command/test_chat_button_does_not_execute_directly_smoke.py", role="test", description="Chat button does not execute directly smoke test."),
        ),
    ),
    RoadmapExpectedBatch(
        batch_id="3.11",
        title="Chat Preview / Container",
        expected_files=(
            ExpectedProjectFile(path="tools/chat_system_preview.py", role="tool", description="Chat system preview tool."),
            ExpectedProjectFile(path="tools/chat_sync_preview.py", role="tool", description="Chat sync preview tool."),
            ExpectedProjectFile(path="CONTAINER_DEPLOYMENT/cubes/chat_command/container_contract.yaml", role="config", description="Chat command container contract."),
            ExpectedProjectFile(path="CONTAINER_DEPLOYMENT/cubes/chat_command/network_policy.yaml", role="config", description="Chat command network policy."),
            ExpectedProjectFile(path="CONTAINER_DEPLOYMENT/cubes/chat_command/runtime_profile.yaml", role="config", description="Chat command runtime profile."),
            ExpectedProjectFile(path="tests/container_readiness/test_chat_command_container_contract_smoke.py", role="test", description="Chat command container contract smoke test."),
            ExpectedProjectFile(path="tests/container_readiness/test_chat_command_core_write_false_smoke.py", role="test", description="Chat command core write false smoke test."),
            ExpectedProjectFile(path="tests/container_readiness/test_chat_command_dashboard_control_false_smoke.py", role="test", description="Chat command dashboard control false smoke test."),
        ),
    ),
    RoadmapExpectedBatch(
        batch_id="3.12",
        title="PHASE 3 Acceptance",
        expected_files=(
            ExpectedProjectFile(path="docs/architecture/chat_command/phase_3_chat_command_acceptance_v1.md", role="doc", description="PHASE 3 chat command acceptance document."),
            ExpectedProjectFile(path="tests/chat_command/test_phase_3_acceptance_smoke.py", role="test", description="PHASE 3 chat command acceptance smoke test."),
        ),
    ),
 RoadmapExpectedBatch(
  batch_id="4.1",
  title="Screen Observer Contracts",
  expected_files=(
   ExpectedProjectFile(path="MAKSIMAR_CORE_LIB/mobile_screen_observer/__init__.py", role="source", description="Mobile screen observer package."),
   ExpectedProjectFile(path="MAKSIMAR_CORE_LIB/mobile_screen_observer/mobile_screen_session_contract.py", role="source", description="Mobile screen session contract."),
   ExpectedProjectFile(path="MAKSIMAR_CORE_LIB/mobile_screen_observer/mobile_screen_frame_contract.py", role="source", description="Mobile screen frame contract."),
   ExpectedProjectFile(path="MAKSIMAR_CORE_LIB/mobile_screen_observer/mobile_screen_consent_contract.py", role="source", description="Mobile screen consent contract."),
   ExpectedProjectFile(path="tests/mobile_screen_observer/test_mobile_screen_session_contract_smoke.py", role="test", description="Mobile screen session contract smoke test."),
   ExpectedProjectFile(path="tests/mobile_screen_observer/test_mobile_screen_frame_contract_smoke.py", role="test", description="Mobile screen frame contract smoke test."),
   ExpectedProjectFile(path="tests/mobile_screen_observer/test_mobile_screen_consent_contract_smoke.py", role="test", description="Mobile screen consent contract smoke test."),
  ),
 ),
 RoadmapExpectedBatch(
  batch_id="4.2",
  title="Screen Policy / Remote Assistance / Family Child Device Control Contracts",
  expected_files=(
   ExpectedProjectFile(path="MAKSIMAR_CORE_LIB/mobile_screen_observer/mobile_screen_policy_contract.py", role="source", description="Mobile screen policy contract."),
   ExpectedProjectFile(path="MAKSIMAR_CORE_LIB/mobile_screen_observer/remote_assistance_intent_contract.py", role="source", description="Remote assistance intent contract."),
   ExpectedProjectFile(path="MAKSIMAR_CORE_LIB/mobile_screen_observer/screen_stream_audit_contract.py", role="source", description="Screen stream audit contract."),
   ExpectedProjectFile(path="tests/mobile_screen_observer/test_mobile_screen_policy_contract_smoke.py", role="test", description="Mobile screen policy contract smoke test."),
   ExpectedProjectFile(path="tests/mobile_screen_observer/test_remote_assistance_intent_contract_smoke.py", role="test", description="Remote assistance intent contract smoke test."),
   ExpectedProjectFile(path="tests/mobile_screen_observer/test_screen_stream_audit_contract_smoke.py", role="test", description="Screen stream audit contract smoke test."),
   ExpectedProjectFile(path="MAKSIMAR_CORE_LIB/family_child_device_control/__init__.py", role="source", description="Family child device control package."),
   ExpectedProjectFile(path="MAKSIMAR_CORE_LIB/family_child_device_control/child_device_profile_contract.py", role="source", description="Child managed device profile contract."),
   ExpectedProjectFile(path="MAKSIMAR_CORE_LIB/family_child_device_control/guardian_authority_contract.py", role="source", description="Guardian authority contract."),
   ExpectedProjectFile(path="MAKSIMAR_CORE_LIB/family_child_device_control/child_screen_control_policy_contract.py", role="source", description="Child screen control policy contract."),
   ExpectedProjectFile(path="MAKSIMAR_CORE_LIB/family_child_device_control/child_remote_control_intent_contract.py", role="source", description="Child remote control intent contract."),
   ExpectedProjectFile(path="MAKSIMAR_CORE_LIB/family_child_device_control/child_device_audit_contract.py", role="source", description="Child device audit contract."),
   ExpectedProjectFile(path="MAKSIMAR_CORE_LIB/family_child_device_control/child_app_control_policy_contract.py", role="source", description="Child app control policy contract."),
   ExpectedProjectFile(path="MAKSIMAR_CORE_LIB/family_child_device_control/child_screen_time_policy_contract.py", role="source", description="Child screen time policy contract."),
   ExpectedProjectFile(path="tests/family_child_device_control/test_child_device_profile_contract_smoke.py", role="test", description="Child device profile contract smoke test."),
   ExpectedProjectFile(path="tests/family_child_device_control/test_guardian_authority_contract_smoke.py", role="test", description="Guardian authority contract smoke test."),
   ExpectedProjectFile(path="tests/family_child_device_control/test_child_screen_control_policy_contract_smoke.py", role="test", description="Child screen control policy contract smoke test."),
   ExpectedProjectFile(path="tests/family_child_device_control/test_child_remote_control_intent_contract_smoke.py", role="test", description="Child remote control intent contract smoke test."),
   ExpectedProjectFile(path="tests/family_child_device_control/test_child_device_audit_contract_smoke.py", role="test", description="Child device audit contract smoke test."),
   ExpectedProjectFile(path="tests/family_child_device_control/test_child_app_control_policy_contract_smoke.py", role="test", description="Child app control policy contract smoke test."),
   ExpectedProjectFile(path="tests/family_child_device_control/test_child_screen_time_policy_contract_smoke.py", role="test", description="Child screen time policy contract smoke test."),
   ExpectedProjectFile(path="tests/family_child_device_control/test_child_control_requires_guardian_authority_smoke.py", role="test", description="Child control requires guardian authority smoke test."),
   ExpectedProjectFile(path="tests/family_child_device_control/test_child_control_rejects_dashboard_bypass_smoke.py", role="test", description="Child control rejects dashboard bypass smoke test."),
   ExpectedProjectFile(path="tests/family_child_device_control/test_normal_screen_observer_remote_control_stays_disabled_smoke.py", role="test", description="Normal screen observer remote control stays disabled smoke test."),
  ),
 ),
 RoadmapExpectedBatch(
  batch_id="4.3",
  title="Server Screen Observer / Family Child Device Runtime",
  expected_files=(
   ExpectedProjectFile(path="MAKSIMAR_SERVER/MOBILE_SCREEN_OBSERVER_RUNTIME/__init__.py", role="source", description="Mobile screen observer server runtime package."),
   ExpectedProjectFile(path="MAKSIMAR_SERVER/MOBILE_SCREEN_OBSERVER_RUNTIME/mobile_screen_observer_session_registry.py", role="source", description="Mobile screen observer session registry."),
   ExpectedProjectFile(path="MAKSIMAR_SERVER/MOBILE_SCREEN_OBSERVER_RUNTIME/screen_frame_ingest_runtime.py", role="source", description="Screen frame ingest runtime."),
   ExpectedProjectFile(path="MAKSIMAR_SERVER/MOBILE_SCREEN_OBSERVER_RUNTIME/screen_observer_read_model_builder.py", role="source", description="Screen observer read-model builder."),
   ExpectedProjectFile(path="MAKSIMAR_SERVER/MOBILE_SCREEN_OBSERVER_RUNTIME/remote_assistance_policy_runtime.py", role="source", description="Remote assistance policy runtime."),
   ExpectedProjectFile(path="tests/mobile_screen_observer/test_screen_observer_session_registry_smoke.py", role="test", description="Screen observer session registry smoke test."),
   ExpectedProjectFile(path="tests/mobile_screen_observer/test_screen_frame_ingest_runtime_smoke.py", role="test", description="Screen frame ingest runtime smoke test."),
   ExpectedProjectFile(path="tests/mobile_screen_observer/test_screen_observer_read_model_builder_smoke.py", role="test", description="Screen observer read-model builder smoke test."),
   ExpectedProjectFile(path="tests/mobile_screen_observer/test_remote_assistance_policy_runtime_smoke.py", role="test", description="Remote assistance policy runtime smoke test."),
   ExpectedProjectFile(path="MAKSIMAR_SERVER/FAMILY_CHILD_DEVICE_RUNTIME/__init__.py", role="source", description="Family child device runtime package."),
   ExpectedProjectFile(path="MAKSIMAR_SERVER/FAMILY_CHILD_DEVICE_RUNTIME/child_device_session_registry.py", role="source", description="Child device session registry."),
   ExpectedProjectFile(path="MAKSIMAR_SERVER/FAMILY_CHILD_DEVICE_RUNTIME/guardian_authority_runtime.py", role="source", description="Guardian authority runtime decision layer."),
   ExpectedProjectFile(path="MAKSIMAR_SERVER/FAMILY_CHILD_DEVICE_RUNTIME/child_screen_control_policy_runtime.py", role="source", description="Child screen control policy runtime."),
   ExpectedProjectFile(path="MAKSIMAR_SERVER/FAMILY_CHILD_DEVICE_RUNTIME/child_remote_control_intent_runtime.py", role="source", description="Child remote control intent runtime."),
   ExpectedProjectFile(path="MAKSIMAR_SERVER/FAMILY_CHILD_DEVICE_RUNTIME/child_device_audit_runtime.py", role="source", description="Child device audit runtime."),
   ExpectedProjectFile(path="MAKSIMAR_SERVER/FAMILY_CHILD_DEVICE_RUNTIME/child_app_control_policy_runtime.py", role="source", description="Child app control policy runtime."),
   ExpectedProjectFile(path="MAKSIMAR_SERVER/FAMILY_CHILD_DEVICE_RUNTIME/child_screen_time_policy_runtime.py", role="source", description="Child screen time policy runtime."),
   ExpectedProjectFile(path="MAKSIMAR_SERVER/FAMILY_CHILD_DEVICE_RUNTIME/family_child_device_read_model_builder.py", role="source", description="Family child device read model builder."),
   ExpectedProjectFile(path="tests/family_child_device_runtime/test_child_device_session_registry_smoke.py", role="test", description="Child device session registry smoke test."),
   ExpectedProjectFile(path="tests/family_child_device_runtime/test_guardian_authority_runtime_smoke.py", role="test", description="Guardian authority runtime smoke test."),
   ExpectedProjectFile(path="tests/family_child_device_runtime/test_child_screen_control_policy_runtime_smoke.py", role="test", description="Child screen control policy runtime smoke test."),
   ExpectedProjectFile(path="tests/family_child_device_runtime/test_child_remote_control_intent_runtime_smoke.py", role="test", description="Child remote control intent runtime smoke test."),
   ExpectedProjectFile(path="tests/family_child_device_runtime/test_child_device_audit_runtime_smoke.py", role="test", description="Child device audit runtime smoke test."),
   ExpectedProjectFile(path="tests/family_child_device_runtime/test_child_app_control_policy_runtime_smoke.py", role="test", description="Child app control policy runtime smoke test."),
   ExpectedProjectFile(path="tests/family_child_device_runtime/test_child_screen_time_policy_runtime_smoke.py", role="test", description="Child screen time policy runtime smoke test."),
   ExpectedProjectFile(path="tests/family_child_device_runtime/test_family_child_device_read_model_builder_smoke.py", role="test", description="Family child device read model builder smoke test."),
   ExpectedProjectFile(path="tests/family_child_device_runtime/test_child_runtime_requires_guardian_authority_smoke.py", role="test", description="Child runtime requires guardian authority smoke test."),
   ExpectedProjectFile(path="tests/family_child_device_runtime/test_child_runtime_rejects_dashboard_bypass_smoke.py", role="test", description="Child runtime rejects dashboard bypass smoke test."),
   ExpectedProjectFile(path="tests/family_child_device_runtime/test_child_runtime_does_not_call_platform_api_smoke.py", role="test", description="Child runtime does not call platform API smoke test."),
   ExpectedProjectFile(path="tests/family_child_device_runtime/test_normal_observer_runtime_does_not_enable_child_control_smoke.py", role="test", description="Normal observer runtime does not enable child control smoke test."),
  ),
 ),
 RoadmapExpectedBatch(
  batch_id="4.4",
  title="Android Screen Observer / Family Child Device Client",
  expected_files=(
   ExpectedProjectFile(path="ANDROID_SHELL/screen_observer_client/README.md", role="doc", description="Android screen observer client README."),
   ExpectedProjectFile(path="ANDROID_SHELL/screen_observer_client/android_screen_observer_client.py", role="source", description="Android screen observer client contract."),
   ExpectedProjectFile(path="ANDROID_SHELL/screen_observer_client/android_screen_consent_state.py", role="source", description="Android screen consent state."),
   ExpectedProjectFile(path="ANDROID_SHELL/screen_observer_client/android_screen_stream_bridge.py", role="source", description="Android screen stream bridge."),
   ExpectedProjectFile(path="ANDROID_SHELL/screen_observer_client/android_remote_assistance_intent_bridge.py", role="source", description="Android remote assistance intent bridge."),
   ExpectedProjectFile(path="tests/mobile_screen_observer/test_android_screen_observer_client_smoke.py", role="test", description="Android screen observer client smoke test."),
   ExpectedProjectFile(path="tests/mobile_screen_observer/test_android_screen_consent_state_smoke.py", role="test", description="Android screen consent state smoke test."),
   ExpectedProjectFile(path="tests/mobile_screen_observer/test_android_screen_stream_bridge_smoke.py", role="test", description="Android screen stream bridge smoke test."),
   ExpectedProjectFile(path="tests/mobile_screen_observer/test_android_remote_assistance_intent_bridge_smoke.py", role="test", description="Android remote assistance intent bridge smoke test."),
   ExpectedProjectFile(path="ANDROID_SHELL/family_child_device/README.md", role="doc", description="Android family child device bridge overview."),
   ExpectedProjectFile(path="ANDROID_SHELL/family_child_device/android_child_device_profile_bridge.py", role="source", description="Android child device profile bridge."),
   ExpectedProjectFile(path="ANDROID_SHELL/family_child_device/android_guardian_authority_bridge.py", role="source", description="Android guardian authority bridge."),
   ExpectedProjectFile(path="ANDROID_SHELL/family_child_device/android_child_screen_control_policy_bridge.py", role="source", description="Android child screen control policy bridge."),
   ExpectedProjectFile(path="ANDROID_SHELL/family_child_device/android_child_remote_control_intent_bridge.py", role="source", description="Android child remote control intent bridge."),
   ExpectedProjectFile(path="ANDROID_SHELL/family_child_device/android_child_device_audit_bridge.py", role="source", description="Android child device audit bridge."),
   ExpectedProjectFile(path="ANDROID_SHELL/family_child_device/android_child_app_control_policy_bridge.py", role="source", description="Android child app control policy bridge."),
   ExpectedProjectFile(path="ANDROID_SHELL/family_child_device/android_child_screen_time_policy_bridge.py", role="source", description="Android child screen time policy bridge."),
   ExpectedProjectFile(path="ANDROID_SHELL/family_child_device/android_family_child_device_policy_binding.py", role="source", description="Android family child device policy binding."),
   ExpectedProjectFile(path="tests/family_child_device_android/test_android_child_device_profile_bridge_smoke.py", role="test", description="Android child device profile bridge smoke test."),
   ExpectedProjectFile(path="tests/family_child_device_android/test_android_guardian_authority_bridge_smoke.py", role="test", description="Android guardian authority bridge smoke test."),
   ExpectedProjectFile(path="tests/family_child_device_android/test_android_child_screen_control_policy_bridge_smoke.py", role="test", description="Android child screen control policy bridge smoke test."),
   ExpectedProjectFile(path="tests/family_child_device_android/test_android_child_remote_control_intent_bridge_smoke.py", role="test", description="Android child remote control intent bridge smoke test."),
   ExpectedProjectFile(path="tests/family_child_device_android/test_android_child_device_audit_bridge_smoke.py", role="test", description="Android child device audit bridge smoke test."),
   ExpectedProjectFile(path="tests/family_child_device_android/test_android_child_app_control_policy_bridge_smoke.py", role="test", description="Android child app control policy bridge smoke test."),
   ExpectedProjectFile(path="tests/family_child_device_android/test_android_child_screen_time_policy_bridge_smoke.py", role="test", description="Android child screen time policy bridge smoke test."),
   ExpectedProjectFile(path="tests/family_child_device_android/test_android_family_child_device_policy_binding_smoke.py", role="test", description="Android family child device policy binding smoke test."),
   ExpectedProjectFile(path="tests/family_child_device_android/test_android_child_bridge_requires_guardian_authority_smoke.py", role="test", description="Android child bridge requires guardian authority smoke test."),
   ExpectedProjectFile(path="tests/family_child_device_android/test_android_child_bridge_rejects_dashboard_bypass_smoke.py", role="test", description="Android child bridge rejects dashboard bypass smoke test."),
   ExpectedProjectFile(path="tests/family_child_device_android/test_android_child_bridge_does_not_call_platform_api_smoke.py", role="test", description="Android child bridge does not call platform API smoke test."),
   ExpectedProjectFile(path="tests/family_child_device_android/test_android_normal_observer_cannot_enable_child_control_smoke.py", role="test", description="Android normal observer cannot enable child control smoke test."),
  ),
 ),
 RoadmapExpectedBatch(
  batch_id="4.5",
  title="iOS Screen Observer / Family Child Device Client",
  expected_files=(
   ExpectedProjectFile(path="IOS_SHELL/screen_observer_client/README.md", role="doc", description="iOS screen observer client README."),
   ExpectedProjectFile(path="IOS_SHELL/screen_observer_client/ios_screen_observer_client.py", role="source", description="iOS screen observer client contract."),
   ExpectedProjectFile(path="IOS_SHELL/screen_observer_client/ios_screen_consent_state.py", role="source", description="iOS screen consent state."),
   ExpectedProjectFile(path="IOS_SHELL/screen_observer_client/ios_screen_stream_bridge.py", role="source", description="iOS screen stream bridge."),
   ExpectedProjectFile(path="IOS_SHELL/screen_observer_client/ios_remote_assistance_intent_bridge.py", role="source", description="iOS remote assistance intent bridge."),
   ExpectedProjectFile(path="tests/mobile_screen_observer/test_ios_screen_observer_client_smoke.py", role="test", description="iOS screen observer client smoke test."),
   ExpectedProjectFile(path="tests/mobile_screen_observer/test_ios_screen_consent_state_smoke.py", role="test", description="iOS screen consent state smoke test."),
   ExpectedProjectFile(path="tests/mobile_screen_observer/test_ios_screen_stream_bridge_smoke.py", role="test", description="iOS screen stream bridge smoke test."),
   ExpectedProjectFile(path="tests/mobile_screen_observer/test_ios_remote_assistance_intent_bridge_smoke.py", role="test", description="iOS remote assistance intent bridge smoke test."),
   ExpectedProjectFile(path="IOS_SHELL/family_child_device/README.md", role="doc", description="iOS family child device bridge overview."),
   ExpectedProjectFile(path="IOS_SHELL/family_child_device/ios_child_device_profile_bridge.py", role="source", description="iOS child device profile bridge."),
   ExpectedProjectFile(path="IOS_SHELL/family_child_device/ios_guardian_authority_bridge.py", role="source", description="iOS guardian authority bridge."),
   ExpectedProjectFile(path="IOS_SHELL/family_child_device/ios_child_screen_control_policy_bridge.py", role="source", description="iOS child screen control policy bridge."),
   ExpectedProjectFile(path="IOS_SHELL/family_child_device/ios_child_remote_control_intent_bridge.py", role="source", description="iOS child remote control intent bridge."),
   ExpectedProjectFile(path="IOS_SHELL/family_child_device/ios_child_device_audit_bridge.py", role="source", description="iOS child device audit bridge."),
   ExpectedProjectFile(path="IOS_SHELL/family_child_device/ios_child_app_control_policy_bridge.py", role="source", description="iOS child app control policy bridge."),
   ExpectedProjectFile(path="IOS_SHELL/family_child_device/ios_child_screen_time_policy_bridge.py", role="source", description="iOS child screen time policy bridge."),
   ExpectedProjectFile(path="IOS_SHELL/family_child_device/ios_family_child_device_policy_binding.py", role="source", description="iOS family child device policy binding."),
   ExpectedProjectFile(path="tests/family_child_device_ios/test_ios_child_device_profile_bridge_smoke.py", role="test", description="iOS child device profile bridge smoke test."),
   ExpectedProjectFile(path="tests/family_child_device_ios/test_ios_guardian_authority_bridge_smoke.py", role="test", description="iOS guardian authority bridge smoke test."),
   ExpectedProjectFile(path="tests/family_child_device_ios/test_ios_child_screen_control_policy_bridge_smoke.py", role="test", description="iOS child screen control policy bridge smoke test."),
   ExpectedProjectFile(path="tests/family_child_device_ios/test_ios_child_remote_control_intent_bridge_smoke.py", role="test", description="iOS child remote control intent bridge smoke test."),
   ExpectedProjectFile(path="tests/family_child_device_ios/test_ios_child_device_audit_bridge_smoke.py", role="test", description="iOS child device audit bridge smoke test."),
   ExpectedProjectFile(path="tests/family_child_device_ios/test_ios_child_app_control_policy_bridge_smoke.py", role="test", description="iOS child app control policy bridge smoke test."),
   ExpectedProjectFile(path="tests/family_child_device_ios/test_ios_child_screen_time_policy_bridge_smoke.py", role="test", description="iOS child screen time policy bridge smoke test."),
   ExpectedProjectFile(path="tests/family_child_device_ios/test_ios_family_child_device_policy_binding_smoke.py", role="test", description="iOS family child device policy binding smoke test."),
   ExpectedProjectFile(path="tests/family_child_device_ios/test_ios_child_bridge_requires_guardian_authority_smoke.py", role="test", description="iOS child bridge requires guardian authority smoke test."),
   ExpectedProjectFile(path="tests/family_child_device_ios/test_ios_child_bridge_rejects_dashboard_bypass_smoke.py", role="test", description="iOS child bridge rejects dashboard bypass smoke test."),
   ExpectedProjectFile(path="tests/family_child_device_ios/test_ios_child_bridge_does_not_call_platform_api_smoke.py", role="test", description="iOS child bridge does not call platform API smoke test."),
   ExpectedProjectFile(path="tests/family_child_device_ios/test_ios_normal_observer_cannot_enable_child_control_smoke.py", role="test", description="iOS normal observer cannot enable child control smoke test."),
  ),
 ),
 RoadmapExpectedBatch(
  batch_id="4.6",
  title="PC Phone Screen Window",
  expected_files=(
   ExpectedProjectFile(path="MAKSIMAR_CORE_LIB/mobile_screen_observer/phone_screen_window_read_model.py", role="source", description="Phone screen window read model."),
   ExpectedProjectFile(path="MAKSIMAR_CORE_LIB/mobile_screen_observer/phone_screen_window_panel_contract.py", role="source", description="Phone screen window panel contract."),
   ExpectedProjectFile(path="MAKSIMAR_CORE_LIB/mobile_screen_observer/phone_screen_button_intent_contract.py", role="source", description="Phone screen button intent contract."),
   ExpectedProjectFile(path="tools/phone_screen_window_preview.py", role="tool", description="Phone screen window preview tool."),
   ExpectedProjectFile(path="frontend/contracts/phone_screen_window_contract.ts", role="source", description="Phone screen window frontend contract."),
   ExpectedProjectFile(path="tests/mobile_screen_observer/test_phone_screen_window_read_model_smoke.py", role="test", description="Phone screen window read model smoke test."),
   ExpectedProjectFile(path="tests/mobile_screen_observer/test_phone_screen_window_panel_contract_smoke.py", role="test", description="Phone screen window panel contract smoke test."),
   ExpectedProjectFile(path="tests/mobile_screen_observer/test_phone_screen_button_intent_contract_smoke.py", role="test", description="Phone screen button intent contract smoke test."),
   ExpectedProjectFile(path="tests/mobile_screen_observer/test_phone_screen_dashboard_read_only_default_smoke.py", role="test", description="Phone screen dashboard read-only default smoke test."),
   ExpectedProjectFile(path="tests/mobile_screen_observer/test_remote_assistance_requires_approval_smoke.py", role="test", description="Remote assistance requires approval smoke test."),
  ),
 ),
 RoadmapExpectedBatch(
  batch_id="4.7",
  title="PHASE 4 Acceptance",
  expected_files=(
   ExpectedProjectFile(path="docs/architecture/mobile_screen_observer/phase4_mobile_screen_observer_acceptance_v1.md", role="doc", description="PHASE 4 mobile screen observer acceptance document."),
   ExpectedProjectFile(path="tests/mobile_screen_observer/test_phase4_acceptance_smoke.py", role="test", description="PHASE 4 mobile screen observer acceptance smoke test."),
  ),
 ),
 RoadmapExpectedBatch(
  batch_id="5.1",
  title="App Memory Core Contracts",
  expected_files=(
   ExpectedProjectFile(path="shared_mobile_core/app_memory/__init__.py", role="source", description="Shared mobile app memory package."),
   ExpectedProjectFile(path="shared_mobile_core/app_memory/app_memory_record_contract.py", role="source", description="App memory record contract."),
   ExpectedProjectFile(path="shared_mobile_core/app_memory/app_memory_store_contract.py", role="source", description="App memory store contract."),
   ExpectedProjectFile(path="shared_mobile_core/app_memory/app_memory_retention_policy.py", role="source", description="App memory retention policy."),
   ExpectedProjectFile(path="shared_mobile_core/app_memory/app_memory_encryption_contract.py", role="source", description="App memory encryption contract."),
   ExpectedProjectFile(path="tests/mobile_memory/test_app_memory_record_contract_smoke.py", role="test", description="App memory record contract smoke test."),
   ExpectedProjectFile(path="tests/mobile_memory/test_app_memory_store_contract_smoke.py", role="test", description="App memory store contract smoke test."),
   ExpectedProjectFile(path="tests/mobile_memory/test_app_memory_retention_policy_smoke.py", role="test", description="App memory retention policy smoke test."),
   ExpectedProjectFile(path="tests/mobile_memory/test_app_memory_encryption_contract_smoke.py", role="test", description="App memory encryption contract smoke test."),
   ExpectedProjectFile(path="tests/mobile_memory/test_app_memory_requires_post_init_validation_smoke.py", role="test", description="App memory requires post-init validation smoke test."),
  ),
 ),
 RoadmapExpectedBatch(
  batch_id="5.2",
  title="Chat Memory Core Contracts",
  expected_files=(
   ExpectedProjectFile(path="shared_mobile_core/chat_memory/__init__.py", role="source", description="Shared mobile chat memory package."),
   ExpectedProjectFile(path="shared_mobile_core/chat_memory/chat_memory_record_contract.py", role="source", description="Chat memory record contract."),
   ExpectedProjectFile(path="shared_mobile_core/chat_memory/chat_memory_store_contract.py", role="source", description="Chat memory store contract."),
   ExpectedProjectFile(path="shared_mobile_core/chat_memory/chat_memory_index_contract.py", role="source", description="Chat memory index contract."),
   ExpectedProjectFile(path="shared_mobile_core/chat_memory/chat_memory_retention_policy.py", role="source", description="Chat memory retention policy."),
   ExpectedProjectFile(path="tests/mobile_memory/test_chat_memory_record_contract_smoke.py", role="test", description="Chat memory record contract smoke test."),
   ExpectedProjectFile(path="tests/mobile_memory/test_chat_memory_store_contract_smoke.py", role="test", description="Chat memory store contract smoke test."),
   ExpectedProjectFile(path="tests/mobile_memory/test_chat_memory_index_contract_smoke.py", role="test", description="Chat memory index contract smoke test."),
   ExpectedProjectFile(path="tests/mobile_memory/test_chat_memory_retention_policy_smoke.py", role="test", description="Chat memory retention policy smoke test."),
   ExpectedProjectFile(path="tests/mobile_memory/test_chat_memory_is_not_openim_truth_smoke.py", role="test", description="Chat memory is not OpenIM truth smoke test."),
  ),
 ),
 RoadmapExpectedBatch(
  batch_id="5.3",
  title="Android App Memory Store",
  expected_files=(
   ExpectedProjectFile(path="ANDROID_SHELL/memory_adapter/android_app_memory_store.py", role="source", description="Android app memory store adapter."),
   ExpectedProjectFile(path="ANDROID_SHELL/memory_adapter/android_secure_local_store.py", role="source", description="Android secure local store adapter."),
   ExpectedProjectFile(path="ANDROID_SHELL/memory_adapter/android_memory_encryption_bridge.py", role="source", description="Android memory encryption bridge."),
   ExpectedProjectFile(path="ANDROID_SHELL/memory_adapter/android_memory_retention_runtime.py", role="source", description="Android memory retention runtime."),
   ExpectedProjectFile(path="ANDROID_SHELL/memory_adapter/android_memory_state_bridge.py", role="source", description="Android memory state bridge."),
   ExpectedProjectFile(path="tests/mobile_memory/test_android_app_memory_store_smoke.py", role="test", description="Android app memory store smoke test."),
   ExpectedProjectFile(path="tests/mobile_memory/test_android_secure_local_store_smoke.py", role="test", description="Android secure local store smoke test."),
   ExpectedProjectFile(path="tests/mobile_memory/test_android_memory_encryption_bridge_smoke.py", role="test", description="Android memory encryption bridge smoke test."),
   ExpectedProjectFile(path="tests/mobile_memory/test_android_memory_retention_runtime_smoke.py", role="test", description="Android memory retention runtime smoke test."),
   ExpectedProjectFile(path="tests/mobile_memory/test_android_memory_state_bridge_smoke.py", role="test", description="Android memory state bridge smoke test."),
  ),
 ),
 RoadmapExpectedBatch(
  batch_id="5.4",
  title="Android Chat Memory Store",
  expected_files=(
   ExpectedProjectFile(path="ANDROID_SHELL/memory_adapter/android_chat_memory_store.py", role="source", description="Android chat memory store adapter."),
   ExpectedProjectFile(path="ANDROID_SHELL/memory_adapter/android_chat_memory_index.py", role="source", description="Android chat memory index adapter."),
   ExpectedProjectFile(path="ANDROID_SHELL/memory_adapter/android_chat_offline_replay_state.py", role="source", description="Android chat offline replay state."),
   ExpectedProjectFile(path="ANDROID_SHELL/memory_adapter/android_chat_memory_export_bridge.py", role="source", description="Android chat memory export bridge."),
   ExpectedProjectFile(path="tests/mobile_memory/test_android_chat_memory_store_smoke.py", role="test", description="Android chat memory store smoke test."),
   ExpectedProjectFile(path="tests/mobile_memory/test_android_chat_memory_index_smoke.py", role="test", description="Android chat memory index smoke test."),
   ExpectedProjectFile(path="tests/mobile_memory/test_android_chat_offline_replay_state_smoke.py", role="test", description="Android chat offline replay state smoke test."),
   ExpectedProjectFile(path="tests/mobile_memory/test_android_chat_memory_export_bridge_smoke.py", role="test", description="Android chat memory export bridge smoke test."),
  ),
 ),
 RoadmapExpectedBatch(
  batch_id="5.5",
  title="iOS App Memory Store",
  expected_files=(
   ExpectedProjectFile(path="IOS_SHELL/memory_adapter/ios_app_memory_store.py", role="source", description="iOS app memory store adapter."),
   ExpectedProjectFile(path="IOS_SHELL/memory_adapter/ios_secure_local_store.py", role="source", description="iOS secure local store adapter."),
   ExpectedProjectFile(path="IOS_SHELL/memory_adapter/ios_memory_encryption_bridge.py", role="source", description="iOS memory encryption bridge."),
   ExpectedProjectFile(path="IOS_SHELL/memory_adapter/ios_memory_retention_runtime.py", role="source", description="iOS memory retention runtime."),
   ExpectedProjectFile(path="IOS_SHELL/memory_adapter/ios_memory_state_bridge.py", role="source", description="iOS memory state bridge."),
   ExpectedProjectFile(path="tests/mobile_memory/test_ios_app_memory_store_smoke.py", role="test", description="iOS app memory store smoke test."),
   ExpectedProjectFile(path="tests/mobile_memory/test_ios_secure_local_store_smoke.py", role="test", description="iOS secure local store smoke test."),
   ExpectedProjectFile(path="tests/mobile_memory/test_ios_memory_encryption_bridge_smoke.py", role="test", description="iOS memory encryption bridge smoke test."),
   ExpectedProjectFile(path="tests/mobile_memory/test_ios_memory_retention_runtime_smoke.py", role="test", description="iOS memory retention runtime smoke test."),
   ExpectedProjectFile(path="tests/mobile_memory/test_ios_memory_state_bridge_smoke.py", role="test", description="iOS memory state bridge smoke test."),
  ),
 ),
 RoadmapExpectedBatch(
  batch_id="5.6",
  title="iOS Chat Memory Store",
  expected_files=(
   ExpectedProjectFile(path="IOS_SHELL/memory_adapter/ios_chat_memory_store.py", role="source", description="iOS chat memory store adapter."),
   ExpectedProjectFile(path="IOS_SHELL/memory_adapter/ios_chat_memory_index.py", role="source", description="iOS chat memory index adapter."),
   ExpectedProjectFile(path="IOS_SHELL/memory_adapter/ios_chat_offline_replay_state.py", role="source", description="iOS chat offline replay state."),
   ExpectedProjectFile(path="IOS_SHELL/memory_adapter/ios_chat_memory_export_bridge.py", role="source", description="iOS chat memory export bridge."),
   ExpectedProjectFile(path="tests/mobile_memory/test_ios_chat_memory_store_smoke.py", role="test", description="iOS chat memory store smoke test."),
   ExpectedProjectFile(path="tests/mobile_memory/test_ios_chat_memory_index_smoke.py", role="test", description="iOS chat memory index smoke test."),
   ExpectedProjectFile(path="tests/mobile_memory/test_ios_chat_offline_replay_state_smoke.py", role="test", description="iOS chat offline replay state smoke test."),
   ExpectedProjectFile(path="tests/mobile_memory/test_ios_chat_memory_export_bridge_smoke.py", role="test", description="iOS chat memory export bridge smoke test."),
  ),
 ),
 RoadmapExpectedBatch(
  batch_id="5.7",
  title="Mobile Sync Protocol",
  expected_files=(
   ExpectedProjectFile(path="shared_mobile_core/mobile_sync_models/mobile_sync_envelope_contract.py", role="source", description="Mobile sync envelope contract."),
   ExpectedProjectFile(path="shared_mobile_core/mobile_sync_models/mobile_sync_cursor_contract.py", role="source", description="Mobile sync cursor contract."),
   ExpectedProjectFile(path="shared_mobile_core/mobile_sync_models/mobile_sync_conflict_contract.py", role="source", description="Mobile sync conflict contract."),
   ExpectedProjectFile(path="shared_mobile_core/mobile_sync_models/mobile_sync_policy.py", role="source", description="Mobile sync policy."),
   ExpectedProjectFile(path="shared_mobile_core/mobile_sync_models/server_presence_sync_trigger.py", role="source", description="Server presence sync trigger."),
   ExpectedProjectFile(path="shared_mobile_core/mobile_sync_models/offline_to_server_replay_contract.py", role="source", description="Offline to server replay contract."),
   ExpectedProjectFile(path="tests/mobile_sync/test_mobile_sync_envelope_contract_smoke.py", role="test", description="Mobile sync envelope contract smoke test."),
   ExpectedProjectFile(path="tests/mobile_sync/test_mobile_sync_cursor_contract_smoke.py", role="test", description="Mobile sync cursor contract smoke test."),
   ExpectedProjectFile(path="tests/mobile_sync/test_mobile_sync_conflict_contract_smoke.py", role="test", description="Mobile sync conflict contract smoke test."),
   ExpectedProjectFile(path="tests/mobile_sync/test_mobile_sync_policy_smoke.py", role="test", description="Mobile sync policy smoke test."),
   ExpectedProjectFile(path="tests/mobile_sync/test_server_presence_triggers_auto_sync_smoke.py", role="test", description="Server presence triggers auto sync smoke test."),
   ExpectedProjectFile(path="tests/mobile_sync/test_offline_to_server_replay_contract_smoke.py", role="test", description="Offline to server replay contract smoke test."),
  ),
 ),
 RoadmapExpectedBatch(
  batch_id="5.8",
  title="Server Mobile Sync Runtime",
  expected_files=(
   ExpectedProjectFile(path="MAKSIMAR_SERVER/MOBILE_SYNC_RUNTIME/__init__.py", role="source", description="Server mobile sync runtime package."),
   ExpectedProjectFile(path="MAKSIMAR_SERVER/MOBILE_SYNC_RUNTIME/mobile_sync_session_registry.py", role="source", description="Mobile sync session registry."),
   ExpectedProjectFile(path="MAKSIMAR_SERVER/MOBILE_SYNC_RUNTIME/app_memory_sync_runtime.py", role="source", description="App memory sync runtime."),
   ExpectedProjectFile(path="MAKSIMAR_SERVER/MOBILE_SYNC_RUNTIME/chat_memory_sync_runtime.py", role="source", description="Chat memory sync runtime."),
   ExpectedProjectFile(path="MAKSIMAR_SERVER/MOBILE_SYNC_RUNTIME/mobile_sync_conflict_resolver.py", role="source", description="Mobile sync conflict resolver."),
   ExpectedProjectFile(path="tests/mobile_sync/test_mobile_sync_session_registry_smoke.py", role="test", description="Mobile sync session registry smoke test."),
   ExpectedProjectFile(path="tests/mobile_sync/test_app_memory_sync_runtime_smoke.py", role="test", description="App memory sync runtime smoke test."),
   ExpectedProjectFile(path="tests/mobile_sync/test_chat_memory_sync_runtime_smoke.py", role="test", description="Chat memory sync runtime smoke test."),
   ExpectedProjectFile(path="tests/mobile_sync/test_mobile_sync_conflict_resolver_smoke.py", role="test", description="Mobile sync conflict resolver smoke test."),
   ExpectedProjectFile(path="tests/mobile_sync/test_mobile_sync_does_not_write_core_directly_smoke.py", role="test", description="Mobile sync does not write core directly smoke test."),
  ),
 ),
 RoadmapExpectedBatch(
  batch_id="5.9",
  title="Sync Dashboard / Preview",
  expected_files=(
   ExpectedProjectFile(path="MAKSIMAR_CORE_LIB/mobile_bridge/mobile_sync_status_read_model.py", role="source", description="Mobile sync status read model."),
   ExpectedProjectFile(path="MAKSIMAR_CORE_LIB/mobile_bridge/mobile_memory_status_read_model.py", role="source", description="Mobile memory status read model."),
   ExpectedProjectFile(path="tools/mobile_memory_status_preview.py", role="tool", description="Mobile memory status preview tool."),
   ExpectedProjectFile(path="tools/mobile_sync_status_preview.py", role="tool", description="Mobile sync status preview tool."),
   ExpectedProjectFile(path="tests/mobile_sync/test_mobile_sync_status_read_model_smoke.py", role="test", description="Mobile sync status read model smoke test."),
   ExpectedProjectFile(path="tests/mobile_sync/test_mobile_memory_status_read_model_smoke.py", role="test", description="Mobile memory status read model smoke test."),
   ExpectedProjectFile(path="tests/mobile_sync/test_mobile_memory_status_preview_smoke.py", role="test", description="Mobile memory status preview smoke test."),
   ExpectedProjectFile(path="tests/mobile_sync/test_mobile_sync_status_preview_smoke.py", role="test", description="Mobile sync status preview smoke test."),
  ),
 ),
 RoadmapExpectedBatch(
  batch_id="5.10",
  title="PHASE 5 Acceptance",
  expected_files=(
   ExpectedProjectFile(path="docs/architecture/mobile_memory/phase_5_app_chat_memory_sync_acceptance_v1.md", role="doc", description="PHASE 5 app/chat memory sync acceptance document."),
   ExpectedProjectFile(path="tests/mobile_memory/test_phase_5_mobile_memory_acceptance_smoke.py", role="test", description="PHASE 5 mobile memory acceptance smoke test."),
   ExpectedProjectFile(path="tests/mobile_sync/test_phase_5_mobile_sync_acceptance_smoke.py", role="test", description="PHASE 5 mobile sync acceptance smoke test."),
  ),
 ),

)


def get_expected_batch(batch_id: str) -> RoadmapExpectedBatch:
    """Return one expected batch by id."""
    for batch in ROADMAP_EXPECTED_BATCHES:
        if batch.batch_id == batch_id:
            return batch

    raise KeyError(f"Unknown roadmap expected batch id: {batch_id!r}")


def list_expected_batches() -> tuple[RoadmapExpectedBatch, ...]:
    """Return all registered expected batches."""
    return ROADMAP_EXPECTED_BATCHES
