import pytest

from MAKSIMAR_SERVER.CHAT_COMMAND_RUNTIME.chat_audit_runtime import (
    ChatAuditEvent,
    ChatAuditRuntime,
)


def test_chat_audit_runtime_smoke() -> None:
    audit = ChatAuditRuntime()
    event = ChatAuditEvent(
        event_id="audit_001",
        event_kind="message_routed",
        subject_id="msg_001",
        actor_identity_id="identity_owner_001",
        created_at_utc="2026-05-27T20:00:00Z",
        policy_checked=True,
        append_only=True,
        direct_execution_allowed=False,
        canonical_write_allowed=False,
        external_network_access_allowed=False,
    )

    audit.append_event(event)

    assert audit.list_events() == (event,)


def test_chat_audit_runtime_rejects_canonical_write() -> None:
    with pytest.raises(ValueError, match="canonical_write_allowed must be False"):
        ChatAuditEvent(
            event_id="audit_bad",
            event_kind="message_routed",
            subject_id="msg_001",
            actor_identity_id="identity_owner_001",
            created_at_utc="2026-05-27T20:00:00Z",
            policy_checked=True,
            append_only=True,
            direct_execution_allowed=False,
            canonical_write_allowed=True,
            external_network_access_allowed=False,
        )
