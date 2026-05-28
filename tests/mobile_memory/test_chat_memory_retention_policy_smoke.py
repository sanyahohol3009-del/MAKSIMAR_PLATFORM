from shared_mobile_core.chat_memory import ChatMemoryRetentionPolicy


def test_chat_memory_retention_policy_is_local_and_policy_gated() -> None:
    policy = ChatMemoryRetentionPolicy.strict_default(retention_policy_id="chat-retention-1")

    assert policy.purge_on_owner_request is True
    assert policy.preserve_audit_refs is True
    assert policy.local_only is True
    assert policy.server_deletion_requires_sync_policy is True
    assert policy.offline_replay_policy_required is True
    assert policy.max_age_days > 0
