from pathlib import Path

import pytest

from shared_mobile_core.mobile_sync_models.mobile_sync_policy import MobileSyncPolicy


def test_mobile_sync_policy_forbids_direct_writes_and_runtime_network() -> None:
    policy = MobileSyncPolicy.strict_default(policy_id="mobile_sync_policy_001")

    assert policy.policy_boundary_required is True
    assert policy.encryption_required is True
    assert policy.retention_required is True
    assert policy.audit_required is True
    assert policy.conflict_policy_required is True
    assert policy.owner_approval_required_for_replay is True
    assert policy.device_approval_required_for_replay is True
    assert policy.trusted_server_presence_required is True
    assert policy.core_write_allowed is False
    assert policy.direct_server_write_allowed is False
    assert policy.network_allowed is False
    assert policy.socket_allowed is False
    assert policy.tunnel_allowed is False
    assert policy.runtime_mutation_allowed is False
    assert policy.mutates_app_memory_store is False
    assert policy.mutates_chat_memory_store is False
    assert policy.allows_domain("app_memory") is True
    assert policy.allows_domain("chat_memory") is True


def test_mobile_sync_policy_rejects_core_or_server_write() -> None:
    with pytest.raises(ValueError, match="core_write_allowed must be False"):
        MobileSyncPolicy(
            policy_id="bad_policy_core",
            policy_ref="policy://bad_policy_core",
            allowed_memory_domains=("app_memory", "chat_memory"),
            policy_boundary_required=True,
            encryption_required=True,
            retention_required=True,
            audit_required=True,
            conflict_policy_required=True,
            offline_first_required=True,
            owner_approval_required_for_replay=True,
            device_approval_required_for_replay=True,
            trusted_server_presence_required=True,
            automatic_sync_allowed=True,
            core_write_allowed=True,
            direct_server_write_allowed=False,
            network_allowed=False,
            socket_allowed=False,
            tunnel_allowed=False,
            runtime_mutation_allowed=False,
            mutates_app_memory_store=False,
            mutates_chat_memory_store=False,
        )

    with pytest.raises(ValueError, match="direct_server_write_allowed must be False"):
        MobileSyncPolicy(
            policy_id="bad_policy_server",
            policy_ref="policy://bad_policy_server",
            allowed_memory_domains=("app_memory", "chat_memory"),
            policy_boundary_required=True,
            encryption_required=True,
            retention_required=True,
            audit_required=True,
            conflict_policy_required=True,
            offline_first_required=True,
            owner_approval_required_for_replay=True,
            device_approval_required_for_replay=True,
            trusted_server_presence_required=True,
            automatic_sync_allowed=True,
            core_write_allowed=False,
            direct_server_write_allowed=True,
            network_allowed=False,
            socket_allowed=False,
            tunnel_allowed=False,
            runtime_mutation_allowed=False,
            mutates_app_memory_store=False,
            mutates_chat_memory_store=False,
        )


def test_mobile_sync_models_do_not_import_runtime_or_platform_surfaces() -> None:
    root = Path("shared_mobile_core/mobile_sync_models")
    forbidden_tokens = (
        "MAKSIMAR_SERVER",
        "ANDROID_SHELL",
        "IOS_SHELL",
        "socket.",
        "requests.",
        "subprocess.",
    )

    for source_file in root.glob("*.py"):
        text = source_file.read_text(encoding="utf-8")
        for token in forbidden_tokens:
            assert token not in text
