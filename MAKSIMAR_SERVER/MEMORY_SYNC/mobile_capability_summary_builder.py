from __future__ import annotations

from typing import Dict

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
from shared_mobile_core.intent_parser.mobile_intent_parser_contract import (
    build_mobile_intent_parser_contract,
)
from shared_mobile_core.llm_engine.local_llm_runtime_contract import (
    build_local_llm_runtime_contract,
)


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
        "app_safe_export_is_read_only": bool(export_manifest["export_is_read_only"]),
        "owner_approval_required": bool(
            boundary["owner_approval_required"]
            and parser["approval_required_for_actions"]
            and eval_contract["owner_approval_required"]
        ),
    }
