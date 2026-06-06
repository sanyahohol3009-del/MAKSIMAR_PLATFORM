from __future__ import annotations

from dataclasses import dataclass
from typing import Any


def _require_non_empty(value: str, field_name: str) -> None:
    if not isinstance(value, str) or not value.strip():
        raise ValueError(f"{field_name} must be a non-empty string")


def _require_non_empty_tuple(value: tuple[str, ...], field_name: str) -> None:
    if not isinstance(value, tuple) or not value:
        raise ValueError(f"{field_name} must be a non-empty tuple")
    for item in value:
        _require_non_empty(item, field_name)


XRAY_COMMAND_HINT = "python tools/architecture_xray_radar.py"
DRIFT_COMMAND_HINT = "python tools/roadmap_post_step_drift_check.py"
FULL_AUTO_COMMAND_HINT = (
    "MAKSIMAR_FULL_PLATFORM_REPORTS=1 python -m pytest -q -n auto "
    "--maksimar-full-platform-reports"
)


FORBIDDEN_PARALLEL_WORLD_ROOTS: tuple[str, ...] = (
    "JARVIS_LIVE_AI_REGISTRY",
    "JARVIS_LIVE_WORKER_REGISTRY",
    "JARVIS_LIVE_AGENT_WORLD",
    "JARVIS_LIVE_VOICE_ROOT",
    "JARVIS_LIVE_MEMORY_ENGINE",
    "JARVIS_LIVE_RUNTIME_QUEUE",
    "MAKSIMAR_CORE_LIB/jarvis_live_ai_registry",
    "MAKSIMAR_CORE_LIB/jarvis_live_worker_registry",
    "MAKSIMAR_CORE_LIB/jarvis_live_agents",
    "MAKSIMAR_CORE_LIB/jarvis_live_memory_engine",
    "MAKSIMAR_CORE_LIB/jarvis_live_runtime_queue",
    "MAKSIMAR_SERVER/JARVIS_LIVE_DIRECT_EXECUTION",
)


@dataclass(frozen=True, slots=True)
class JarvisLiveRoadmapBatch:
    batch_id: str
    title: str
    purpose: str
    expected_files: tuple[str, ...]
    target_tests: tuple[str, ...]
    download_allowed: bool
    runtime_allowed: bool
    voice_allowed: bool
    pc_control_allowed: bool
    depends_on: tuple[str, ...]
    status_rule: str

    def __post_init__(self) -> None:
        _require_non_empty(self.batch_id, "batch_id")
        _require_non_empty(self.title, "title")
        _require_non_empty(self.purpose, "purpose")
        _require_non_empty_tuple(self.expected_files, "expected_files")
        _require_non_empty_tuple(self.target_tests, "target_tests")
        _require_non_empty(self.status_rule, "status_rule")
        for dependency in self.depends_on:
            _require_non_empty(dependency, "depends_on")

    def to_read_model(self) -> dict[str, Any]:
        return {
            "batch_id": self.batch_id,
            "title": self.title,
            "purpose": self.purpose,
            "expected_files": self.expected_files,
            "target_tests": self.target_tests,
            "download_allowed": self.download_allowed,
            "runtime_allowed": self.runtime_allowed,
            "voice_allowed": self.voice_allowed,
            "pc_control_allowed": self.pc_control_allowed,
            "depends_on": self.depends_on,
            "status_rule": self.status_rule,
        }


JARVIS_LIVE_FULL_ROADMAP_BATCHES: tuple[JarvisLiveRoadmapBatch, ...] = (
    JarvisLiveRoadmapBatch(
        batch_id="JL-0",
        title="Roadmap / CI / Anti-Drift Control",
        purpose="Declare roadmap, expected files, status builder, and no-parallel-world guard.",
        expected_files=(
            "docs/architecture/jarvis_live/jarvis_live_roadmap_v0_1.md",
            "docs/architecture/jarvis_live/jarvis_live_no_drift_rules_v0.md",
            "MAKSIMAR_SERVER/OBSERVABILITY/memory_skill_metrics/jarvis_live_roadmap_status_builder.py",
            "tools/project_readiness_control/jarvis_live_roadmap_expected_files.py",
            "tests/jarvis_live/test_jarvis_live_roadmap_status_builder_smoke.py",
            "tests/jarvis_live/test_jarvis_live_no_parallel_world_guard_smoke.py",
        ),
        target_tests=(
            "tests/jarvis_live/test_jarvis_live_roadmap_status_builder_smoke.py",
            "tests/jarvis_live/test_jarvis_live_no_parallel_world_guard_smoke.py",
        ),
        download_allowed=False,
        runtime_allowed=False,
        voice_allowed=False,
        pc_control_allowed=False,
        depends_on=(),
        status_rule="ready_when_all_expected_files_exist_and_no_parallel_roots_exist",
    ),
    JarvisLiveRoadmapBatch(
        batch_id="JL-1",
        title="JARVIS-LIVE Contract Entry",
        purpose="Add disabled model conductor, disabled live gate, readiness summary, and tests.",
        expected_files=(
            "MAKSIMAR_CORE_LIB/ai_orchestration/jarvis_live_model_conductor_contract.py",
            "MAKSIMAR_CORE_LIB/real_voice_runtime/jarvis_live_disabled_gate_contract.py",
            "MAKSIMAR_SERVER/OBSERVABILITY/memory_skill_metrics/jarvis_live_readiness_summary_builder.py",
            "tests/jarvis_live/test_jarvis_live_contract_entry_smoke.py",
        ),
        target_tests=("tests/jarvis_live/test_jarvis_live_contract_entry_smoke.py",),
        download_allowed=False,
        runtime_allowed=False,
        voice_allowed=False,
        pc_control_allowed=False,
        depends_on=("JL-0",),
        status_rule="ready_when_contract_entry_files_exist",
    ),
    JarvisLiveRoadmapBatch(
        batch_id="JL-2",
        title="Model Profile / Resource Registry Binding",
        purpose="Bind model roles to profiles and resource requirements without downloads.",
        expected_files=(
            "MAKSIMAR_CORE_LIB/ai_orchestration/model_profile_registry_contract.py",
            "MAKSIMAR_CORE_LIB/ai_orchestration/model_resource_requirements_contract.py",
            "MAKSIMAR_CORE_LIB/ai_orchestration/model_role_binding_contract.py",
            "MAKSIMAR_SERVER/AI_ORCHESTRATION/model_profile_read_model_builder.py",
            "tests/ai_orchestration/test_model_profile_registry_contract_smoke.py",
            "tests/ai_orchestration/test_model_resource_requirements_contract_smoke.py",
        ),
        target_tests=(
            "tests/ai_orchestration/test_model_profile_registry_contract_smoke.py",
            "tests/ai_orchestration/test_model_resource_requirements_contract_smoke.py",
        ),
        download_allowed=False,
        runtime_allowed=False,
        voice_allowed=False,
        pc_control_allowed=False,
        depends_on=("JL-1",),
        status_rule="next_after_jl1_until_model_profile_contracts_exist",
    ),
    JarvisLiveRoadmapBatch(
        batch_id="JL-3",
        title="Worker Identity / Alias Binding",
        purpose="Bind model, voice, and screen roles to existing worker registry identities.",
        expected_files=(
            "MAKSIMAR_CORE_LIB/workers_registry/worker_role_binding_contract.py",
            "MAKSIMAR_CORE_LIB/workers_registry/worker_alias_binding_contract.py",
            "MAKSIMAR_SERVER/AI_ORCHESTRATION/adapters/model_worker_binding_adapter.py",
            "tests/workers_registry/test_worker_role_alias_binding_smoke.py",
            "tests/workers_registry/test_model_worker_binding_adapter_smoke.py",
        ),
        target_tests=(
            "tests/workers_registry/test_worker_role_alias_binding_smoke.py",
            "tests/workers_registry/test_model_worker_binding_adapter_smoke.py",
        ),
        download_allowed=False,
        runtime_allowed=False,
        voice_allowed=False,
        pc_control_allowed=False,
        depends_on=("JL-2",),
        status_rule="ready_when_worker_bindings_reuse_existing_registry",
    ),
    JarvisLiveRoadmapBatch(
        batch_id="JL-4",
        title="Runtime Storage Boundary",
        purpose="Define model, retrieval, embedding, vector, and cache storage boundaries.",
        expected_files=(
            "MAKSIMAR_CORE_LIB/memory_engine/storage_registry/runtime_model_storage_policy_contract.py",
            "MAKSIMAR_CORE_LIB/memory_engine/storage_registry/runtime_retrieval_storage_policy_contract.py",
            "MAKSIMAR_CORE_LIB/memory_engine/storage_registry/runtime_cache_boundary_contract.py",
            "tests/memory_engine/test_runtime_model_storage_policy_smoke.py",
            "tests/memory_engine/test_runtime_retrieval_storage_policy_smoke.py",
            "tests/memory_engine/test_runtime_cache_boundary_smoke.py",
        ),
        target_tests=(
            "tests/memory_engine/test_runtime_model_storage_policy_smoke.py",
            "tests/memory_engine/test_runtime_retrieval_storage_policy_smoke.py",
            "tests/memory_engine/test_runtime_cache_boundary_smoke.py",
        ),
        download_allowed=False,
        runtime_allowed=False,
        voice_allowed=False,
        pc_control_allowed=False,
        depends_on=("JL-3",),
        status_rule="blocks_model_download_until_storage_boundary_exists",
    ),
    JarvisLiveRoadmapBatch(
        batch_id="JL-5",
        title="Voice Live Disabled Status",
        purpose="Expose voice live disabled state for mic, STT, TTS, and wake word.",
        expected_files=(
            "MAKSIMAR_SERVER/VOICE_ROUTING/jarvis_live_voice_status_models.py",
            "MAKSIMAR_SERVER/VOICE_ROUTING/jarvis_live_voice_status_read_model.py",
            "MAKSIMAR_CORE_LIB/oob_dashboard/jarvis_voice_status_panel_contract.py",
            "tests/voice_routing/test_jarvis_live_voice_status_read_model_smoke.py",
            "tests/oob_dashboard/test_jarvis_voice_status_panel_contract_smoke.py",
            "tests/real_voice_runtime/test_jarvis_live_voice_disabled_by_default_smoke.py",
            "tests/real_voice_runtime/test_jarvis_live_no_audio_runtime_smoke.py",
        ),
        target_tests=(
            "tests/voice_routing/test_jarvis_live_voice_status_read_model_smoke.py",
            "tests/oob_dashboard/test_jarvis_voice_status_panel_contract_smoke.py",
            "tests/real_voice_runtime/test_jarvis_live_voice_disabled_by_default_smoke.py",
            "tests/real_voice_runtime/test_jarvis_live_no_audio_runtime_smoke.py",
        ),
        download_allowed=False,
        runtime_allowed=False,
        voice_allowed=False,
        pc_control_allowed=False,
        depends_on=("JL-4",),
        status_rule="voice_status_visible_but_audio_runtime_disabled",
    ),
    JarvisLiveRoadmapBatch(
        batch_id="JL-6",
        title="Screen Observer / Vision-OCR Candidate Binding",
        purpose="Bind read-only screen observer to vision/OCR candidates without capture/control.",
        expected_files=(
            "MAKSIMAR_CORE_LIB/mobile_screen_observer/screen_vision_candidate_contract.py",
            "MAKSIMAR_SERVER/MOBILE_SCREEN_OBSERVER_RUNTIME/screen_vision_status_read_model.py",
            "tests/mobile_screen_observer/test_screen_vision_candidate_contract_smoke.py",
            "tests/mobile_screen_observer/test_screen_vision_status_read_model_smoke.py",
            "tests/mobile_screen_observer/test_screen_observer_no_control_bypass_smoke.py",
        ),
        target_tests=(
            "tests/mobile_screen_observer/test_screen_vision_candidate_contract_smoke.py",
            "tests/mobile_screen_observer/test_screen_vision_status_read_model_smoke.py",
            "tests/mobile_screen_observer/test_screen_observer_no_control_bypass_smoke.py",
        ),
        download_allowed=False,
        runtime_allowed=False,
        voice_allowed=False,
        pc_control_allowed=False,
        depends_on=("JL-5",),
        status_rule="screen_summary_candidate_only_no_control",
    ),
    JarvisLiveRoadmapBatch(
        batch_id="JL-7",
        title="Security / Action Allowlist Binding",
        purpose="Bind commands to security, approval, audit, and action allowlist.",
        expected_files=(
            "MAKSIMAR_CORE_LIB/security_layer/jarvis_command_security_binding_contract.py",
            "MAKSIMAR_CORE_LIB/security_layer/jarvis_action_allowlist_contract.py",
            "MAKSIMAR_SERVER/PROPOSAL_AUDIT/jarvis_command_audit_binding.py",
            "tests/security_layer/test_jarvis_command_security_binding_smoke.py",
            "tests/security_layer/test_jarvis_action_allowlist_contract_smoke.py",
            "tests/proposal_audit/test_jarvis_command_audit_binding_smoke.py",
        ),
        target_tests=(
            "tests/security_layer/test_jarvis_command_security_binding_smoke.py",
            "tests/security_layer/test_jarvis_action_allowlist_contract_smoke.py",
            "tests/proposal_audit/test_jarvis_command_audit_binding_smoke.py",
        ),
        download_allowed=False,
        runtime_allowed=False,
        voice_allowed=False,
        pc_control_allowed=False,
        depends_on=("JL-6",),
        status_rule="actions_policy_bound_but_no_control_enabled",
    ),
    JarvisLiveRoadmapBatch(
        batch_id="JL-8",
        title="Dashboard Observability",
        purpose="Expose JARVIS model, voice, resource, approval, and rejection status.",
        expected_files=(
            "MAKSIMAR_CORE_LIB/oob_dashboard/jarvis_live_status_panel_contract.py",
            "MAKSIMAR_CORE_LIB/oob_dashboard/jarvis_model_status_panel_contract.py",
            "MAKSIMAR_CORE_LIB/oob_dashboard/jarvis_resource_status_panel_contract.py",
            "MAKSIMAR_CORE_LIB/oob_dashboard/jarvis_queue_status_panel_contract.py",
            "MAKSIMAR_SERVER/OBSERVABILITY/jarvis_live/jarvis_live_observability_read_model.py",
            "tests/oob_dashboard/test_jarvis_live_status_panel_contract_smoke.py",
            "tests/oob_dashboard/test_jarvis_model_resource_status_panels_smoke.py",
            "tests/oob_dashboard/test_jarvis_queue_status_panel_contract_smoke.py",
        ),
        target_tests=(
            "tests/oob_dashboard/test_jarvis_live_status_panel_contract_smoke.py",
            "tests/oob_dashboard/test_jarvis_model_resource_status_panels_smoke.py",
            "tests/oob_dashboard/test_jarvis_queue_status_panel_contract_smoke.py",
        ),
        download_allowed=False,
        runtime_allowed=False,
        voice_allowed=False,
        pc_control_allowed=False,
        depends_on=("JL-7",),
        status_rule="dashboard_read_only_no_execution",
    ),
    JarvisLiveRoadmapBatch(
        batch_id="JL-9",
        title="External Task Broker Contract: Codex/Gemini",
        purpose="Define external task broker packets as proposal-only artifacts.",
        expected_files=(
            "MAKSIMAR_CORE_LIB/ai_orchestration/external_task_broker_contract.py",
            "MAKSIMAR_SERVER/AI_ORCHESTRATION/external_task_broker_read_model.py",
            "MAKSIMAR_SERVER/PROPOSAL_AUDIT/external_task_broker_audit_binding.py",
            "tests/ai_orchestration/test_external_task_broker_contract_smoke.py",
            "tests/proposal_audit/test_external_task_broker_audit_binding_smoke.py",
        ),
        target_tests=(
            "tests/ai_orchestration/test_external_task_broker_contract_smoke.py",
            "tests/proposal_audit/test_external_task_broker_audit_binding_smoke.py",
        ),
        download_allowed=False,
        runtime_allowed=False,
        voice_allowed=False,
        pc_control_allowed=False,
        depends_on=("JL-8",),
        status_rule="external_tools_are_proposal_producers_not_executors",
    ),
    JarvisLiveRoadmapBatch(
        batch_id="JL-10",
        title="Live Sandbox / Vendor / Download Gate",
        purpose="Define live sandbox and vendor boundary required before model download.",
        expected_files=(
            "MAKSIMAR_SERVER/AI_ORCHESTRATION/live_sandbox_vendor_boundary_contract.py",
            "MAKSIMAR_SERVER/AI_ORCHESTRATION/live_model_download_gate_contract.py",
            "MAKSIMAR_SERVER/AI_ORCHESTRATION/live_sandbox_runtime_policy.py",
            "tests/ai_orchestration/test_live_sandbox_vendor_boundary_contract_smoke.py",
            "tests/ai_orchestration/test_live_model_download_gate_contract_smoke.py",
        ),
        target_tests=(
            "tests/ai_orchestration/test_live_sandbox_vendor_boundary_contract_smoke.py",
            "tests/ai_orchestration/test_live_model_download_gate_contract_smoke.py",
        ),
        download_allowed=True,
        runtime_allowed=False,
        voice_allowed=False,
        pc_control_allowed=False,
        depends_on=("JL-4", "JL-9"),
        status_rule="download_candidate_only_after_storage_and_vendor_boundaries_exist",
    ),
    JarvisLiveRoadmapBatch(
        batch_id="JL-11",
        title="First Voice / Project Read-Only Live Smoke",
        purpose="First voice smoke for project read-only response path, no PC control.",
        expected_files=(
            "MAKSIMAR_SERVER/VOICE_ROUTING/jarvis_live_read_only_voice_smoke_contract.py",
            "tests/jarvis_live/test_jarvis_live_read_only_voice_smoke.py",
        ),
        target_tests=("tests/jarvis_live/test_jarvis_live_read_only_voice_smoke.py",),
        download_allowed=False,
        runtime_allowed=True,
        voice_allowed=True,
        pc_control_allowed=False,
        depends_on=("JL-10",),
        status_rule="first_voice_smoke_read_only_no_pc_control",
    ),
    JarvisLiveRoadmapBatch(
        batch_id="JL-12",
        title="Microphone Push-to-Talk STT",
        purpose="Add push-to-talk STT path after gates; wake word remains separate.",
        expected_files=(
            "MAKSIMAR_SERVER/VOICE_ROUTING/jarvis_live_push_to_talk_stt_contract.py",
            "tests/jarvis_live/test_jarvis_live_push_to_talk_stt_gate_smoke.py",
        ),
        target_tests=("tests/jarvis_live/test_jarvis_live_push_to_talk_stt_gate_smoke.py",),
        download_allowed=False,
        runtime_allowed=True,
        voice_allowed=True,
        pc_control_allowed=False,
        depends_on=("JL-11",),
        status_rule="push_to_talk_only_no_wake_word_no_control",
    ),
    JarvisLiveRoadmapBatch(
        batch_id="JL-13",
        title="Read-Only Screen Summary",
        purpose="Summarize screen state read-only through existing observer and vision binding.",
        expected_files=(
            "MAKSIMAR_SERVER/MOBILE_SCREEN_OBSERVER_RUNTIME/jarvis_live_screen_summary_read_model.py",
            "tests/jarvis_live/test_jarvis_live_screen_summary_read_only_smoke.py",
        ),
        target_tests=("tests/jarvis_live/test_jarvis_live_screen_summary_read_only_smoke.py",),
        download_allowed=False,
        runtime_allowed=True,
        voice_allowed=True,
        pc_control_allowed=False,
        depends_on=("JL-12",),
        status_rule="screen_summary_read_only_no_app_control",
    ),
    JarvisLiveRoadmapBatch(
        batch_id="JL-14",
        title="Controlled PC Action Adapter",
        purpose="First controlled PC action adapter behind allowlist, approval, audit, and queue.",
        expected_files=(
            "MAKSIMAR_SERVER/AI_ORCHESTRATION/jarvis_live_controlled_pc_action_adapter_contract.py",
            "tests/jarvis_live/test_jarvis_live_controlled_pc_action_adapter_smoke.py",
        ),
        target_tests=("tests/jarvis_live/test_jarvis_live_controlled_pc_action_adapter_smoke.py",),
        download_allowed=False,
        runtime_allowed=True,
        voice_allowed=True,
        pc_control_allowed=True,
        depends_on=("JL-13",),
        status_rule="first_pc_control_adapter_requires_allowlist_approval_audit_queue",
    ),
)


def list_jarvis_live_batches() -> tuple[JarvisLiveRoadmapBatch, ...]:
    return JARVIS_LIVE_FULL_ROADMAP_BATCHES


def get_jarvis_live_batch(batch_id: str) -> JarvisLiveRoadmapBatch:
    for batch in JARVIS_LIVE_FULL_ROADMAP_BATCHES:
        if batch.batch_id == batch_id:
            return batch
    raise KeyError(f"unknown JARVIS-LIVE batch_id: {batch_id}")


def build_jarvis_live_full_roadmap_read_model() -> dict[str, Any]:
    return {
        "roadmap_id": "JARVIS-LIVE",
        "roadmap_version": "0.1",
        "total_batches": len(JARVIS_LIVE_FULL_ROADMAP_BATCHES),
        "batch_ids": tuple(batch.batch_id for batch in JARVIS_LIVE_FULL_ROADMAP_BATCHES),
        "batches": tuple(batch.to_read_model() for batch in JARVIS_LIVE_FULL_ROADMAP_BATCHES),
        "forbidden_parallel_world_roots": FORBIDDEN_PARALLEL_WORLD_ROOTS,
        "xray_command_hint": XRAY_COMMAND_HINT,
        "drift_command_hint": DRIFT_COMMAND_HINT,
        "full_auto_command_hint": FULL_AUTO_COMMAND_HINT,
        "read_only": True,
        "runtime_start_allowed_now": False,
        "model_download_allowed_now": True,
        "voice_allowed_now": False,
        "pc_control_allowed_now": False,
    }
