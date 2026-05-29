from pathlib import Path
import re


ROOT = Path(".")
DOC = ROOT / "docs/architecture/mobile_memory/phase_5_app_chat_memory_sync_acceptance_v1.md"

MEMORY_EXPECTED_FILES = (
    "shared_mobile_core/app_memory/__init__.py",
    "shared_mobile_core/app_memory/app_memory_record_contract.py",
    "shared_mobile_core/app_memory/app_memory_store_contract.py",
    "shared_mobile_core/app_memory/app_memory_retention_policy.py",
    "shared_mobile_core/app_memory/app_memory_encryption_contract.py",
    "shared_mobile_core/chat_memory/__init__.py",
    "shared_mobile_core/chat_memory/chat_memory_record_contract.py",
    "shared_mobile_core/chat_memory/chat_memory_store_contract.py",
    "shared_mobile_core/chat_memory/chat_memory_index_contract.py",
    "shared_mobile_core/chat_memory/chat_memory_retention_policy.py",
    "ANDROID_SHELL/memory_adapter/android_app_memory_store.py",
    "ANDROID_SHELL/memory_adapter/android_secure_local_store.py",
    "ANDROID_SHELL/memory_adapter/android_memory_encryption_bridge.py",
    "ANDROID_SHELL/memory_adapter/android_memory_retention_runtime.py",
    "ANDROID_SHELL/memory_adapter/android_memory_state_bridge.py",
    "ANDROID_SHELL/memory_adapter/android_chat_memory_store.py",
    "ANDROID_SHELL/memory_adapter/android_chat_memory_index.py",
    "ANDROID_SHELL/memory_adapter/android_chat_offline_replay_state.py",
    "ANDROID_SHELL/memory_adapter/android_chat_memory_export_bridge.py",
    "IOS_SHELL/memory_adapter/ios_app_memory_store.py",
    "IOS_SHELL/memory_adapter/ios_secure_local_store.py",
    "IOS_SHELL/memory_adapter/ios_memory_encryption_bridge.py",
    "IOS_SHELL/memory_adapter/ios_memory_retention_runtime.py",
    "IOS_SHELL/memory_adapter/ios_memory_state_bridge.py",
    "IOS_SHELL/memory_adapter/ios_chat_memory_store.py",
    "IOS_SHELL/memory_adapter/ios_chat_memory_index.py",
    "IOS_SHELL/memory_adapter/ios_chat_offline_replay_state.py",
    "IOS_SHELL/memory_adapter/ios_chat_memory_export_bridge.py",
)

SOURCE_FILES_TO_SCAN = tuple(path for path in MEMORY_EXPECTED_FILES if path.endswith(".py"))


def _read(path: str) -> str:
    return (ROOT / path).read_text(encoding="utf-8")


def test_phase_5_mobile_memory_acceptance_doc_exists_and_has_jarvis_markers() -> None:
    assert DOC.exists()
    text = DOC.read_text(encoding="utf-8")

    required_markers = (
        "PHASE 5",
        "JARVIS-readable architecture context",
        "App Memory Core Contracts",
        "Chat Memory Core Contracts",
        "Android App Memory Store",
        "Android Chat Memory Store",
        "iOS App Memory Store",
        "iOS Chat Memory Store",
        "Mobile Sync Protocol",
        "Server Mobile Sync Runtime",
        "Sync Dashboard / Preview",
        "Source of truth boundaries",
        "Forbidden behaviors",
        "JARVIS reasoning guidance",
    )

    for marker in required_markers:
        assert marker in text


def test_phase_5_mobile_memory_surfaces_exist() -> None:
    for relative_path in MEMORY_EXPECTED_FILES:
        assert (ROOT / relative_path).exists(), relative_path


def test_phase_5_mobile_memory_does_not_create_parallel_memory_engine_world() -> None:
    forbidden_roots = (
        ROOT / "shared_mobile_core/memory_engine",
        ROOT / "ANDROID_SHELL/memory_engine",
        ROOT / "IOS_SHELL/memory_engine",
        ROOT / "MAKSIMAR_SERVER/MOBILE_MEMORY_ENGINE",
        ROOT / "MAKSIMAR_CORE_LIB/mobile_memory_engine",
    )

    for forbidden_root in forbidden_roots:
        assert not forbidden_root.exists(), str(forbidden_root)


def test_phase_5_mobile_memory_sources_keep_local_reference_only_boundaries() -> None:
    app_memory_text = "\n".join(
        _read(path)
        for path in (
            "shared_mobile_core/app_memory/app_memory_record_contract.py",
            "shared_mobile_core/app_memory/app_memory_store_contract.py",
            "shared_mobile_core/app_memory/app_memory_retention_policy.py",
            "shared_mobile_core/app_memory/app_memory_encryption_contract.py",
        )
    )
    chat_memory_text = "\n".join(
        _read(path)
        for path in (
            "shared_mobile_core/chat_memory/chat_memory_record_contract.py",
            "shared_mobile_core/chat_memory/chat_memory_store_contract.py",
            "shared_mobile_core/chat_memory/chat_memory_index_contract.py",
            "shared_mobile_core/chat_memory/chat_memory_retention_policy.py",
        )
    )
    android_app_text = "\n".join(
        _read(path)
        for path in (
            "ANDROID_SHELL/memory_adapter/android_app_memory_store.py",
            "ANDROID_SHELL/memory_adapter/android_secure_local_store.py",
            "ANDROID_SHELL/memory_adapter/android_memory_encryption_bridge.py",
            "ANDROID_SHELL/memory_adapter/android_memory_retention_runtime.py",
            "ANDROID_SHELL/memory_adapter/android_memory_state_bridge.py",
        )
    )
    ios_chat_text = "\n".join(
        _read(path)
        for path in (
            "IOS_SHELL/memory_adapter/ios_chat_memory_store.py",
            "IOS_SHELL/memory_adapter/ios_chat_memory_index.py",
            "IOS_SHELL/memory_adapter/ios_chat_offline_replay_state.py",
            "IOS_SHELL/memory_adapter/ios_chat_memory_export_bridge.py",
        )
    )

    assert "app_memory" in app_memory_text
    assert "direct_server_write_allowed" in app_memory_text
    assert "core_write_allowed" in app_memory_text
    assert "global_project_memory" in app_memory_text or "canonical_truth" in app_memory_text

    assert "chat_memory" in chat_memory_text
    assert "direct_server_write_allowed" in chat_memory_text
    assert "core_write_allowed" in chat_memory_text
    assert "openim_truth" in chat_memory_text
    assert "core_chat_truth" in chat_memory_text

    assert "canonical_truth" in android_app_text
    assert "direct_server_write_allowed" in android_app_text
    assert "core_write_allowed" in android_app_text

    assert "openim_truth" in ios_chat_text
    assert "core_chat_truth" in ios_chat_text
    assert "direct_server_write_allowed" in ios_chat_text
    assert "core_write_allowed" in ios_chat_text


def test_phase_5_mobile_memory_sources_have_no_placeholder_runtime_logic() -> None:
    forbidden_patterns = (
        re.compile(r"\bpass\b"),
        re.compile(r"NotImplementedError"),
        re.compile(r"\bTODO\b"),
        re.compile(r"\bFIXME\b"),
        re.compile(r"fake success", re.IGNORECASE),
        re.compile(r"dummy runtime", re.IGNORECASE),
    )

    for relative_path in SOURCE_FILES_TO_SCAN:
        text = _read(relative_path)
        for pattern in forbidden_patterns:
            assert pattern.search(text) is None, f"{relative_path} contains {pattern.pattern}"
