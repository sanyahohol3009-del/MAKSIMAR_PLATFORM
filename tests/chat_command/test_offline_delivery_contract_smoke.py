import pytest

from MAKSIMAR_CORE_LIB.chat_command.offline_delivery_contract import OfflineDeliveryContract


def test_offline_delivery_contract_smoke() -> None:
    delivery = OfflineDeliveryContract(
        delivery_id="delivery_001",
        message_id="msg_001",
        target_identity_id="identity_family_001",
        target_device_id="android_device_001",
        delivery_state="queued_offline",
        retry_policy="bounded",
        max_retry_count=3,
        server_sync_required=True,
        external_network_access_allowed=False,
        direct_mobile_api_execution_allowed=False,
        runtime_mutation_allowed=False,
    )

    assert delivery.server_sync_required is True
    assert delivery.direct_mobile_api_execution_allowed is False


def test_offline_delivery_rejects_direct_mobile_api() -> None:
    with pytest.raises(ValueError, match="direct_mobile_api_execution_allowed must be False"):
        OfflineDeliveryContract(
            delivery_id="delivery_bad",
            message_id="msg_001",
            target_identity_id="identity_family_001",
            target_device_id="android_device_001",
            delivery_state="queued_offline",
            retry_policy="bounded",
            max_retry_count=3,
            server_sync_required=True,
            external_network_access_allowed=False,
            direct_mobile_api_execution_allowed=True,
            runtime_mutation_allowed=False,
        )
