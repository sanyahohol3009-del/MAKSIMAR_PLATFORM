from pathlib import Path

import pytest

from MAKSIMAR_SERVER.MOBILE_SYNC_RUNTIME.app_memory_sync_runtime import AppMemorySyncRuntime
from MAKSIMAR_SERVER.MOBILE_SYNC_RUNTIME.chat_memory_sync_runtime import ChatMemorySyncRuntime
from MAKSIMAR_SERVER.MOBILE_SYNC_RUNTIME.mobile_sync_conflict_resolver import MobileSyncConflictResolver
from shared_mobile_core.mobile_sync_models.mobile_sync_policy import MobileSyncPolicy


def _policy() -> MobileSyncPolicy:
    return MobileSyncPolicy.strict_default(policy_id="mobile_sync_policy_001")


def test_mobile_sync_runtime_classes_reject_direct_core_or_network_authority() -> None:
    with pytest.raises(ValueError, match="core_write_allowed must be False"):
        AppMemorySyncRuntime(
            runtime_id="bad_app_runtime",
            policy=_policy(),
            read_only_runtime=True,
            canonical_truth=False,
            core_write_allowed=True,
            direct_server_write_allowed=False,
            network_allowed=False,
            socket_allowed=False,
            tunnel_allowed=False,
            runtime_connection_allowed=False,
            mutates_app_memory_store=False,
            mutates_chat_memory_store=False,
        )

    with pytest.raises(ValueError, match="direct_server_write_allowed must be False"):
        ChatMemorySyncRuntime(
            runtime_id="bad_chat_runtime",
            policy=_policy(),
            read_only_runtime=True,
            openim_truth=False,
            core_chat_truth=False,
            canonical_truth=False,
            core_write_allowed=False,
            direct_server_write_allowed=True,
            network_allowed=False,
            socket_allowed=False,
            tunnel_allowed=False,
            runtime_connection_allowed=False,
            mutates_app_memory_store=False,
            mutates_chat_memory_store=False,
        )

    with pytest.raises(ValueError, match="socket_allowed must be False"):
        MobileSyncConflictResolver(
            resolver_id="bad_resolver",
            deterministic_only=True,
            read_only_runtime=True,
            mutates_records=False,
            core_write_allowed=False,
            direct_server_write_allowed=False,
            network_allowed=False,
            socket_allowed=True,
            tunnel_allowed=False,
            runtime_connection_allowed=False,
            runtime_mutation_allowed=False,
        )


def test_mobile_sync_runtime_sources_do_not_import_platform_or_dashboard_surfaces() -> None:
    root = Path("MAKSIMAR_SERVER/MOBILE_SYNC_RUNTIME")
    forbidden_tokens = (
        "ANDROID_SHELL",
        "IOS_SHELL",
        "MAKSIMAR_CORE_LIB/mobile_bridge",
        "tools/mobile_memory_status_preview",
        "tools/mobile_sync_status_preview",
        "socket.",
        "requests.",
        "subprocess.",
    )

    for source_file in root.glob("*.py"):
        text = source_file.read_text(encoding="utf-8")
        for token in forbidden_tokens:
            assert token not in text
