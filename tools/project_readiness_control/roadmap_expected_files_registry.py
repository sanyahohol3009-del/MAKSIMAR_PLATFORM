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
