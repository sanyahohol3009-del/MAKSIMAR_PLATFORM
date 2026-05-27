import pytest

from MAKSIMAR_CORE_LIB.chat_command.chat_button_state_models import ChatButtonStateModel
from MAKSIMAR_CORE_LIB.chat_command.file_transfer_read_model import FileTransferReadModel


def test_chat_button_state_is_display_only() -> None:
    button = ChatButtonStateModel(
        button_id="button_001",
        label="Review intent",
        target_intent_id="intent_001",
        button_state="visible_requires_approval",
        display_only=True,
        approval_required=True,
        control_plane_handoff_required=True,
        direct_execution_allowed=False,
        dashboard_control_allowed=False,
        runtime_mutation_allowed=False,
    )

    assert button.display_only is True
    assert button.direct_execution_allowed is False
    assert button.dashboard_control_allowed is False


def test_chat_button_rejects_direct_execution() -> None:
    with pytest.raises(ValueError, match="direct_execution_allowed must be False"):
        ChatButtonStateModel(
            button_id="button_bad",
            label="Execute",
            target_intent_id="intent_001",
            button_state="visible_requires_approval",
            display_only=True,
            approval_required=True,
            control_plane_handoff_required=True,
            direct_execution_allowed=True,
            dashboard_control_allowed=False,
            runtime_mutation_allowed=False,
        )


def test_file_transfer_read_model_is_dashboard_only() -> None:
    model = FileTransferReadModel(
        read_model_id="file_transfer_rm_001",
        transfer_id="transfer_001",
        message_id="msg_001",
        attachment_id="att_001",
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

    assert model.dashboard_read_only is True
    assert model.runtime_execution_allowed is False
