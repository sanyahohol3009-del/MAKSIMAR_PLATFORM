import pytest

from shared_mobile_core.mobile_sync_models.mobile_sync_policy import MobileSyncPolicy
from shared_mobile_core.mobile_sync_models.server_presence_sync_trigger import ServerPresenceSyncTrigger


def test_server_presence_trigger_enables_sync_only_for_trusted_server() -> None:
    policy = MobileSyncPolicy.strict_default(policy_id="mobile_sync_policy_001")

    trusted = ServerPresenceSyncTrigger.evaluate(
        trigger_id="server_presence_trigger_001",
        policy=policy,
        server_presence_ref="server-presence://primary",
        server_present=True,
        trusted_server_presence=True,
    )
    absent = ServerPresenceSyncTrigger.evaluate(
        trigger_id="server_presence_trigger_002",
        policy=policy,
        server_presence_ref="server-presence://primary",
        server_present=False,
        trusted_server_presence=False,
    )
    untrusted = ServerPresenceSyncTrigger.evaluate(
        trigger_id="server_presence_trigger_003",
        policy=policy,
        server_presence_ref="server-presence://primary",
        server_present=True,
        trusted_server_presence=False,
    )

    assert trusted.automatic_sync_enabled is True
    assert trusted.deferred_reason == "not_deferred"
    assert trusted.network_allowed is False
    assert trusted.opens_runtime_connection is False
    assert absent.automatic_sync_enabled is False
    assert absent.deferred_reason == "server_absent"
    assert untrusted.automatic_sync_enabled is False
    assert untrusted.deferred_reason == "server_untrusted"


def test_server_presence_trigger_rejects_forced_auto_sync_without_trust() -> None:
    policy = MobileSyncPolicy.strict_default(policy_id="mobile_sync_policy_001")

    with pytest.raises(ValueError, match="automatic_sync_enabled requires trusted_server_presence"):
        ServerPresenceSyncTrigger(
            trigger_id="bad_server_presence_trigger",
            policy=policy,
            server_presence_ref="server-presence://primary",
            server_present=True,
            trusted_server_presence=False,
            automatic_sync_enabled=True,
            deferred_reason="not_deferred",
            core_write_allowed=False,
            direct_server_write_allowed=False,
            network_allowed=False,
            socket_allowed=False,
            tunnel_allowed=False,
            runtime_mutation_allowed=False,
            opens_runtime_connection=False,
        )
