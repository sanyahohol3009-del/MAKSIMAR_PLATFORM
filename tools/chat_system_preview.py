from __future__ import annotations

import json
from dataclasses import asdict
from typing import Any, Dict

from MAKSIMAR_CORE_LIB.chat_command.chat_button_state_models import ChatButtonStateModel
from MAKSIMAR_CORE_LIB.chat_command.chat_operator_intent_models import ChatOperatorIntentModel
from MAKSIMAR_CORE_LIB.chat_command.chat_session_read_model import ChatSessionReadModel
from MAKSIMAR_CORE_LIB.chat_command.chat_system_read_model import ChatSystemReadModel
from MAKSIMAR_CORE_LIB.chat_command.file_transfer_read_model import FileTransferReadModel
from MAKSIMAR_CORE_LIB.chat_command.message_queue_read_model import MessageQueueReadModel


def build_chat_system_preview() -> Dict[str, Any]:
    system = ChatSystemReadModel(
        read_model_id="chat_system_preview_rm_001",
        system_state="online_reference",
        active_session_count=1,
        queued_message_count=2,
        blocked_message_count=0,
        file_transfer_count=1,
        dashboard_read_only=True,
        direct_execution_allowed=False,
        runtime_mutation_allowed=False,
        canonical_truth_write_allowed=False,
    )
    session = ChatSessionReadModel(
        read_model_id="chat_session_preview_rm_001",
        session_id="session_preview_001",
        room_id="room_operator_preview_001",
        participant_count=2,
        session_state="active",
        unread_count=1,
        pending_outbound_count=1,
        dashboard_read_only=True,
        direct_execution_allowed=False,
        runtime_mutation_allowed=False,
        canonical_truth_write_allowed=False,
    )
    queue = MessageQueueReadModel(
        read_model_id="message_queue_preview_rm_001",
        queue_state="active",
        queued_count=2,
        waiting_for_sync_count=1,
        blocked_count=0,
        oldest_message_age_seconds=30,
        dashboard_read_only=True,
        direct_delivery_allowed=False,
        external_network_access_allowed=False,
        runtime_mutation_allowed=False,
    )
    transfer = FileTransferReadModel(
        read_model_id="file_transfer_preview_rm_001",
        transfer_id="transfer_preview_001",
        message_id="msg_preview_001",
        attachment_id="att_preview_001",
        transfer_state="inspection_required",
        size_bytes=1024,
        scan_required=True,
        checksum_required=True,
        encryption_required=True,
        dashboard_read_only=True,
        direct_file_system_write_allowed=False,
        external_network_access_allowed=False,
        runtime_execution_allowed=False,
    )
    intent = ChatOperatorIntentModel(
        intent_id="intent_preview_001",
        source_message_id="msg_preview_001",
        source_surface="chat_dashboard",
        normalized_intent="show chat system status",
        intent_state="approval_required",
        risk_level="low",
        policy_review_required=True,
        operator_approval_required=True,
        control_plane_handoff_required=True,
        sandbox_required=True,
        direct_execution_allowed=False,
        runtime_mutation_allowed=False,
    )
    button = ChatButtonStateModel(
        button_id="button_preview_001",
        label="Review intent",
        target_intent_id="intent_preview_001",
        button_state="visible_requires_approval",
        display_only=True,
        approval_required=True,
        control_plane_handoff_required=True,
        direct_execution_allowed=False,
        dashboard_control_allowed=False,
        runtime_mutation_allowed=False,
    )

    return {
        "preview_id": "chat_system_preview_v1",
        "dashboard_read_only": True,
        "direct_execution_allowed": False,
        "dashboard_control_allowed": False,
        "runtime_mutation_allowed": False,
        "canonical_truth_write_allowed": False,
        "external_network_access_allowed": False,
        "system": asdict(system),
        "session": asdict(session),
        "queue": asdict(queue),
        "file_transfer": asdict(transfer),
        "operator_intent": asdict(intent),
        "button": asdict(button),
    }


def main() -> None:
    print(json.dumps(build_chat_system_preview(), ensure_ascii=False, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
