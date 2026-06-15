from __future__ import annotations

from dataclasses import dataclass
from typing import Any, Dict

from MAKSIMAR_CORE_LIB.app_safe_core.app_safe_core_boundary_contract import (
    build_app_safe_core_boundary_contract,
)
from MAKSIMAR_CORE_LIB.app_safe_core.app_safe_core_export_manifest import (
    build_app_safe_core_export_manifest,
)
from MAKSIMAR_CORE_LIB.mobile_bridge.core_sync_protocol_contract import (
    build_core_sync_protocol_contract,
)
from MAKSIMAR_CORE_LIB.mobile_bridge.junior_model_eval_contract import (
    build_junior_model_eval_contract,
)
from MAKSIMAR_CORE_LIB.mobile_bridge.junior_model_policy_contract import (
    build_junior_model_policy_contract,
)
from MAKSIMAR_CORE_LIB.mobile_bridge.mirror_drift_detection_contract import (
    build_mirror_drift_detection_contract,
)
from MAKSIMAR_CORE_LIB.mobile_bridge.mobile_core_mirror_contract import (
    build_mobile_core_mirror_contract,
)
from MAKSIMAR_SERVER.MEMORY_SYNC.junior_feedback_ingest_contract import (
    build_junior_feedback_ingest_contract,
)
from MAKSIMAR_SERVER.MEMORY_SYNC.junior_model_sync_policy import (
    build_junior_model_sync_policy,
)
from MAKSIMAR_SERVER.MEMORY_SYNC.senior_to_junior_model_sync_contract import (
    build_senior_to_junior_model_sync_contract,
)
from shared_mobile_core.intent_parser.mobile_intent_parser_contract import (
    build_mobile_intent_parser_contract,
)
from shared_mobile_core.llm_engine.local_llm_runtime_contract import (
    build_local_llm_runtime_contract,
)
from shared_mobile_core.mobile_sync_models.mobile_family_event_sync_contract import (
    build_mobile_family_event_sync_contract,
)


@dataclass(frozen=True, slots=True)
class MobileAiStatusReadModel:
    server_jARVIS_is_senior: bool
    mobile_junior_exists_as_app_safe_node: bool
    app_safe_core_mirror_read_only: bool
    junior_model_runtime_started: bool
    model_download_allowed: bool
    local_inference_started: bool
    junior_can_execute_core_actions: bool
    junior_can_write_canonical_memory: bool
    junior_sync_authority: bool
    feedback_is_proposal_only: bool
    windows_voice_edge_parked: bool
    push_to_talk_stt_live_parked: bool

    def __post_init__(self) -> None:
        for field_name in (
            "server_jARVIS_is_senior",
            "mobile_junior_exists_as_app_safe_node",
            "app_safe_core_mirror_read_only",
            "feedback_is_proposal_only",
            "windows_voice_edge_parked",
            "push_to_talk_stt_live_parked",
        ):
            if getattr(self, field_name) is not True:
                raise ValueError(f"{field_name} must be True")
        for field_name in (
            "junior_model_runtime_started",
            "model_download_allowed",
            "local_inference_started",
            "junior_can_execute_core_actions",
            "junior_can_write_canonical_memory",
            "junior_sync_authority",
        ):
            if getattr(self, field_name) is not False:
                raise ValueError(f"{field_name} must be False")

    def to_read_model(self) -> dict[str, Any]:
        return {
            "server_jARVIS_is_senior": self.server_jARVIS_is_senior,
            "mobile_junior_exists_as_app_safe_node": self.mobile_junior_exists_as_app_safe_node,
            "app_safe_core_mirror_read_only": self.app_safe_core_mirror_read_only,
            "junior_model_runtime_started": self.junior_model_runtime_started,
            "model_download_allowed": self.model_download_allowed,
            "local_inference_started": self.local_inference_started,
            "junior_can_execute_core_actions": self.junior_can_execute_core_actions,
            "junior_can_write_canonical_memory": self.junior_can_write_canonical_memory,
            "junior_sync_authority": self.junior_sync_authority,
            "feedback_is_proposal_only": self.feedback_is_proposal_only,
            "windows_voice_edge_parked": self.windows_voice_edge_parked,
            "push_to_talk_stt_live_parked": self.push_to_talk_stt_live_parked,
        }


def build_mobile_capability_summary() -> Dict[str, object]:
    local_llm = build_local_llm_runtime_contract().to_read_model()
    parser = build_mobile_intent_parser_contract().to_read_model()
    boundary = build_app_safe_core_boundary_contract().to_read_model()
    export_manifest = build_app_safe_core_export_manifest().to_read_model()
    mirror = build_mobile_core_mirror_contract().to_read_model()
    sync = build_core_sync_protocol_contract().to_read_model()
    drift = build_mirror_drift_detection_contract().to_read_model()
    policy = build_junior_model_policy_contract().to_read_model()
    eval_contract = build_junior_model_eval_contract().to_read_model()
    senior_sync = build_senior_to_junior_model_sync_contract().to_read_model()
    feedback = build_junior_feedback_ingest_contract().to_read_model()
    sync_policy = build_junior_model_sync_policy().to_read_model()
    family_event = build_mobile_family_event_sync_contract().to_read_model()

    return {
        "summary_id": "mobile_capability_summary_v0_1",
        "read_only": True,
        "server_remains_canonical_core": True,
        "server_remains_canonical_senior": bool(
            local_llm["senior_model_role"] == "server_jARVIS_senior"
            and policy["server_remains_canonical_authority"]
            and sync["server_remains_canonical_authority"]
            and drift["server_remains_canonical_authority"]
        ),
        "junior_is_mobile_app_safe_context_intent_node": bool(
            local_llm["app_safe_only"]
            and local_llm["text_intent_only"]
            and parser["app_safe_only"]
            and parser["text_intent_only"]
        ),
        "junior_is_canonical_truth": False,
        "junior_can_execute_core_actions": False,
        "junior_can_write_canonical_memory": False,
        "mirror_is_read_only": bool(mirror["mirror_is_read_only"]),
        "mirror_is_canonical_truth": bool(mirror["mirror_is_canonical_truth"]),
        "drift_detection_is_evidence_only": bool(
            drift["drift_report_is_evidence_only"]
            and drift["drift_detection_read_only"]
        ),
        "drift_detection_is_read_only": bool(drift["drift_detection_read_only"]),
        "junior_model_policy_runtime_started": bool(policy["local_inference_started"]),
        "windows_voice_edge_parked": True,
        "push_to_talk_stt_live_parked": True,
        "model_download_allowed": False,
        "local_inference_started": False,
        "shell_execution_allowed": False,
        "canonical_write_allowed": False,
        "pc_control_allowed": False,
        "network_sync_start_allowed": False,
        "deployment_allowed": False,
        "mobile_feedback_is_proposal_only": bool(sync["mobile_feedback_is_proposal_only"]),
        "junior_feedback_is_proposal_only": bool(
            feedback["feedback_ingest_is_proposal_only"]
        ),
        "junior_feedback_is_evidence_only": bool(
            feedback["feedback_ingest_is_evidence_only"]
        ),
        "sync_is_server_senior_to_mobile_junior_only": bool(
            senior_sync["sync_direction"] == "server_senior_to_mobile_junior"
            and senior_sync["server_jARVIS_is_senior"]
            and senior_sync["mobile_junior_is_subordinate"]
        ),
        "offline_queue_allowed": bool(sync_policy["offline_queue_allowed"]),
        "family_event_is_context_only": bool(family_event["family_event_is_context_only"]),
        "app_safe_export_is_read_only": bool(export_manifest["export_is_read_only"]),
        "owner_approval_required": bool(
            boundary["owner_approval_required"]
            and parser["approval_required_for_actions"]
            and eval_contract["owner_approval_required"]
        ),
    }


def build_mobile_ai_status_read_model() -> MobileAiStatusReadModel:
    summary = build_mobile_capability_summary()
    return MobileAiStatusReadModel(
        server_jARVIS_is_senior=bool(summary["server_remains_canonical_senior"]),
        mobile_junior_exists_as_app_safe_node=bool(
            summary["junior_is_mobile_app_safe_context_intent_node"]
        ),
        app_safe_core_mirror_read_only=bool(summary["mirror_is_read_only"]),
        junior_model_runtime_started=False,
        model_download_allowed=False,
        local_inference_started=False,
        junior_can_execute_core_actions=False,
        junior_can_write_canonical_memory=False,
        junior_sync_authority=False,
        feedback_is_proposal_only=bool(summary["junior_feedback_is_proposal_only"]),
        windows_voice_edge_parked=True,
        push_to_talk_stt_live_parked=True,
    )
