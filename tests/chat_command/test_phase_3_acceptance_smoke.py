from pathlib import Path


ACCEPTANCE_DOC = Path("docs/architecture/chat_command/phase_3_chat_command_acceptance_v1.md")
JARVIS_CONTEXT_DOC = Path("docs/architecture/chat_command/phase_3_chat_command_jarvis_context_v1.md")


REQUIRED_PHASE_FILES = (
    Path("MAKSIMAR_CORE_LIB/chat_command/chat_message_contract.py"),
    Path("MAKSIMAR_CORE_LIB/chat_command/command_message_contract.py"),
    Path("MAKSIMAR_CORE_LIB/chat_command/chat_room_contract.py"),
    Path("MAKSIMAR_CORE_LIB/chat_command/chat_identity_contract.py"),
    Path("MAKSIMAR_CORE_LIB/chat_command/file_transfer_contract.py"),
    Path("MAKSIMAR_CORE_LIB/chat_command/media_attachment_contract.py"),
    Path("MAKSIMAR_CORE_LIB/chat_command/offline_delivery_contract.py"),
    Path("MAKSIMAR_CORE_LIB/chat_command/server_sync_contract.py"),
    Path("MAKSIMAR_CORE_LIB/chat_command/message_encryption_contract.py"),
    Path("MAKSIMAR_CORE_LIB/chat_command/chat_to_command_handoff_contract.py"),
    Path("MAKSIMAR_CORE_LIB/chat_command/openim_reference_adapter_contract.py"),
    Path("MAKSIMAR_SERVER/CHAT_COMMAND_RUNTIME/chat_session_registry.py"),
    Path("MAKSIMAR_SERVER/CHAT_COMMAND_RUNTIME/message_router_runtime.py"),
    Path("MAKSIMAR_SERVER/CHAT_COMMAND_RUNTIME/offline_queue_runtime.py"),
    Path("MAKSIMAR_SERVER/CHAT_COMMAND_RUNTIME/chat_audit_runtime.py"),
    Path("MAKSIMAR_SERVER/CHAT_COMMAND_RUNTIME/file_transfer_runtime.py"),
    Path("MAKSIMAR_SERVER/CHAT_COMMAND_RUNTIME/media_attachment_runtime.py"),
    Path("MAKSIMAR_SERVER/CHAT_COMMAND_RUNTIME/server_to_server_sync_runtime.py"),
    Path("ANDROID_SHELL/chat_client/chat_sync_contract.py"),
    Path("ANDROID_SHELL/chat_client/file_attachment_bridge.py"),
    Path("IOS_SHELL/chat_client/chat_sync_contract.py"),
    Path("IOS_SHELL/chat_client/file_attachment_bridge.py"),
    Path("MAKSIMAR_CORE_LIB/chat_command/chat_system_read_model.py"),
    Path("MAKSIMAR_CORE_LIB/chat_command/chat_button_state_models.py"),
    Path("tools/chat_system_preview.py"),
    Path("tools/chat_sync_preview.py"),
    Path("CONTAINER_DEPLOYMENT/cubes/chat_command/container_contract.yaml"),
    Path("CONTAINER_DEPLOYMENT/cubes/chat_command/network_policy.yaml"),
    Path("CONTAINER_DEPLOYMENT/cubes/chat_command/runtime_profile.yaml"),
)


def test_phase_3_acceptance_documents_exist() -> None:
    assert ACCEPTANCE_DOC.exists()
    assert JARVIS_CONTEXT_DOC.exists()

    acceptance = ACCEPTANCE_DOC.read_text(encoding="utf-8")
    context = JARVIS_CONTEXT_DOC.read_text(encoding="utf-8")

    assert "PHASE 3" in acceptance
    assert "Chat Command / Sovereign Messenger" in acceptance
    assert "JARVIS context document" in acceptance
    assert "phase_3_chat_command_jarvis_context_v1.md" in acceptance

    assert "JARVIS Context" in context
    assert "sovereign messenger" in context
    assert "dashboard button does not execute directly" in context
    assert "external messenger is adapter-only" in context
    assert "control-plane + policy + approval + sandbox remain mandatory" in context


def test_phase_3_required_files_exist() -> None:
    missing = [str(path) for path in REQUIRED_PHASE_FILES if not path.exists()]
    assert missing == []


def test_phase_3_acceptance_safety_markers() -> None:
    combined = "\n".join(
        path.read_text(encoding="utf-8")
        for path in (
            ACCEPTANCE_DOC,
            JARVIS_CONTEXT_DOC,
            Path("CONTAINER_DEPLOYMENT/cubes/chat_command/container_contract.yaml"),
            Path("CONTAINER_DEPLOYMENT/cubes/chat_command/network_policy.yaml"),
            Path("CONTAINER_DEPLOYMENT/cubes/chat_command/runtime_profile.yaml"),
        )
    )

    assert "direct command execution" in combined
    assert "dashboard direct control" in combined
    assert "runtime mutation" in combined
    assert "canonical truth writes" in combined
    assert "direct_execution_allowed: false" in combined
    assert "dashboard_control_allowed: false" in combined
    assert "runtime_mutation_allowed: false" in combined
    assert "canonical_write_allowed: false" in combined
    assert "external_network_access_allowed: false" in combined
