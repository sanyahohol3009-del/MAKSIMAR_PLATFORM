from __future__ import annotations

import json
from dataclasses import asdict
from typing import Any, Dict

from ANDROID_SHELL.chat_client.chat_sync_contract import AndroidChatSyncContract
from IOS_SHELL.chat_client.chat_sync_contract import IOSChatSyncContract
from MAKSIMAR_CORE_LIB.chat_command.server_sync_contract import ServerSyncContract


def build_chat_sync_preview() -> Dict[str, Any]:
    android = AndroidChatSyncContract(
        sync_binding_id="android_chat_sync_preview_001",
        device_id="android_device_preview_001",
        server_node_id="server_main",
        sync_mode="server_available",
        message_scope="message_reference",
        encryption_required=True,
        direct_network_call_allowed=False,
        direct_server_write_allowed=False,
        background_service_start_allowed=False,
        canonical_truth_write_allowed=False,
    )
    ios = IOSChatSyncContract(
        sync_binding_id="ios_chat_sync_preview_001",
        device_id="ios_device_preview_001",
        server_node_id="server_main",
        sync_mode="server_available",
        message_scope="message_reference",
        encryption_required=True,
        direct_network_call_allowed=False,
        direct_server_write_allowed=False,
        background_task_start_allowed=False,
        canonical_truth_write_allowed=False,
    )
    server = ServerSyncContract(
        sync_id="server_chat_sync_preview_001",
        source_node_id="server_main",
        target_node_id="server_backup",
        sync_scope="message_reference",
        sync_state="declared",
        conflict_policy="owner_review",
        encryption_required=True,
        operator_approval_required=True,
        direct_sync_execution_allowed=False,
        external_network_access_allowed=False,
        runtime_mutation_allowed=False,
    )

    return {
        "preview_id": "chat_sync_preview_v1",
        "dashboard_read_only": True,
        "direct_sync_execution_allowed": False,
        "direct_network_call_allowed": False,
        "external_network_access_allowed": False,
        "runtime_mutation_allowed": False,
        "canonical_truth_write_allowed": False,
        "android": asdict(android),
        "ios": asdict(ios),
        "server": asdict(server),
    }


def main() -> None:
    print(json.dumps(build_chat_sync_preview(), ensure_ascii=False, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
