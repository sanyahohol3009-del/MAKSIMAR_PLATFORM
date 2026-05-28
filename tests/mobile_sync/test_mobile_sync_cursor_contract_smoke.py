import pytest

from shared_mobile_core.mobile_sync_models.mobile_sync_cursor_contract import MobileSyncCursorContract


def test_mobile_sync_cursor_accepts_forward_and_equal_non_decreasing_sequence() -> None:
    forward = MobileSyncCursorContract.advance(
        cursor_id="cursor_forward_001",
        memory_domain="app_memory",
        source_device_id="device_001",
        previous_sequence=4,
        accepted_sequence=5,
    )
    equal = MobileSyncCursorContract.advance(
        cursor_id="cursor_equal_001",
        memory_domain="chat_memory",
        source_device_id="device_001",
        previous_sequence=5,
        accepted_sequence=5,
    )

    assert forward.accepted_sequence == 5
    assert equal.accepted_sequence == 5
    assert forward.network_allowed is False
    assert equal.direct_server_write_allowed is False


def test_mobile_sync_cursor_rejects_regression_and_strict_equal_sequence() -> None:
    with pytest.raises(ValueError, match="accepted_sequence must be greater than or equal"):
        MobileSyncCursorContract.advance(
            cursor_id="cursor_regression_001",
            memory_domain="app_memory",
            source_device_id="device_001",
            previous_sequence=9,
            accepted_sequence=8,
        )

    with pytest.raises(ValueError, match="strictly_forward"):
        MobileSyncCursorContract.advance(
            cursor_id="cursor_strict_equal_001",
            memory_domain="chat_memory",
            source_device_id="device_001",
            previous_sequence=9,
            accepted_sequence=9,
            monotonic_policy="strictly_forward",
        )


def test_mobile_sync_cursor_rejects_runtime_mutation_flags() -> None:
    with pytest.raises(ValueError, match="network_allowed must be False"):
        MobileSyncCursorContract(
            cursor_id="bad_cursor",
            memory_domain="app_memory",
            source_device_id="device_001",
            previous_sequence=1,
            accepted_sequence=2,
            previous_checkpoint_ref="cursor://device_001/app_memory/1",
            accepted_checkpoint_ref="cursor://device_001/app_memory/2",
            monotonic_policy="non_decreasing",
            persistence_allowed=False,
            network_allowed=True,
            socket_allowed=False,
            tunnel_allowed=False,
            core_write_allowed=False,
            direct_server_write_allowed=False,
            runtime_mutation_allowed=False,
        )
