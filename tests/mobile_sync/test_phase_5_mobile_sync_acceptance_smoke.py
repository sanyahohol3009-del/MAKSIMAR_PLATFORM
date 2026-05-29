from pathlib import Path
import json
import re

from tools.mobile_memory_status_preview import build_mobile_memory_status_preview_payload
from tools.mobile_sync_status_preview import build_mobile_sync_status_preview_payload


ROOT = Path(".")

SYNC_EXPECTED_FILES = (
    "shared_mobile_core/mobile_sync_models/mobile_sync_envelope_contract.py",
    "shared_mobile_core/mobile_sync_models/mobile_sync_cursor_contract.py",
    "shared_mobile_core/mobile_sync_models/mobile_sync_conflict_contract.py",
    "shared_mobile_core/mobile_sync_models/mobile_sync_policy.py",
    "shared_mobile_core/mobile_sync_models/server_presence_sync_trigger.py",
    "shared_mobile_core/mobile_sync_models/offline_to_server_replay_contract.py",
    "MAKSIMAR_SERVER/MOBILE_SYNC_RUNTIME/__init__.py",
    "MAKSIMAR_SERVER/MOBILE_SYNC_RUNTIME/mobile_sync_session_registry.py",
    "MAKSIMAR_SERVER/MOBILE_SYNC_RUNTIME/app_memory_sync_runtime.py",
    "MAKSIMAR_SERVER/MOBILE_SYNC_RUNTIME/chat_memory_sync_runtime.py",
    "MAKSIMAR_SERVER/MOBILE_SYNC_RUNTIME/mobile_sync_conflict_resolver.py",
    "MAKSIMAR_CORE_LIB/mobile_bridge/mobile_sync_status_read_model.py",
    "MAKSIMAR_CORE_LIB/mobile_bridge/mobile_memory_status_read_model.py",
    "tools/mobile_memory_status_preview.py",
    "tools/mobile_sync_status_preview.py",
)

ALLOWED_SYNC_ROOTS = (
    ROOT / "shared_mobile_core/mobile_sync_models",
    ROOT / "MAKSIMAR_SERVER/MOBILE_SYNC_RUNTIME",
    ROOT / "MAKSIMAR_CORE_LIB/mobile_bridge",
    ROOT / "tools",
    ROOT / "tests/mobile_sync",
)


def _read(path: str) -> str:
    return (ROOT / path).read_text(encoding="utf-8")


def test_phase_5_mobile_sync_surfaces_exist() -> None:
    for relative_path in SYNC_EXPECTED_FILES:
        assert (ROOT / relative_path).exists(), relative_path


def test_phase_5_mobile_sync_has_no_duplicate_sync_root() -> None:
    forbidden_roots = (
        ROOT / "MAKSIMAR_CORE_LIB/mobile_sync_models",
        ROOT / "MAKSIMAR_CORE_LIB/mobile_sync_runtime",
        ROOT / "shared_mobile_core/mobile_sync_runtime",
        ROOT / "MAKSIMAR_SERVER/mobile_sync_models",
        ROOT / "DASHBOARD/mobile_sync",
        ROOT / "frontend/mobile_sync_runtime",
    )

    for forbidden_root in forbidden_roots:
        assert not forbidden_root.exists(), str(forbidden_root)

    for relative_path in SYNC_EXPECTED_FILES:
        path = ROOT / relative_path
        assert any(path.is_relative_to(allowed_root) for allowed_root in ALLOWED_SYNC_ROOTS), relative_path


def test_phase_5_mobile_sync_protocol_and_runtime_keep_safety_flags() -> None:
    envelope_text = _read("shared_mobile_core/mobile_sync_models/mobile_sync_envelope_contract.py")
    cursor_text = _read("shared_mobile_core/mobile_sync_models/mobile_sync_cursor_contract.py")
    conflict_text = _read("shared_mobile_core/mobile_sync_models/mobile_sync_conflict_contract.py")
    app_runtime_text = _read("MAKSIMAR_SERVER/MOBILE_SYNC_RUNTIME/app_memory_sync_runtime.py")
    chat_runtime_text = _read("MAKSIMAR_SERVER/MOBILE_SYNC_RUNTIME/chat_memory_sync_runtime.py")
    resolver_text = _read("MAKSIMAR_SERVER/MOBILE_SYNC_RUNTIME/mobile_sync_conflict_resolver.py")

    for marker in (
        "reference_only",
        "inline_payload_present",
        "message_body_present",
        "embedded_secret_present",
        "core_write_allowed",
        "direct_server_write_allowed",
        "network_allowed",
        "socket_allowed",
        "tunnel_allowed",
        "mutates_app_memory_store",
        "mutates_chat_memory_store",
    ):
        assert marker in envelope_text

    assert "accepted_sequence must be greater than or equal to previous_sequence" in cursor_text
    assert "deterministic_evidence_hash" in conflict_text

    for text in (app_runtime_text, chat_runtime_text, resolver_text):
        assert "core_write_allowed" in text
        assert "direct_server_write_allowed" in text
        assert "network_allowed" in text
        assert "socket_allowed" in text
        assert "tunnel_allowed" in text
        assert "silent_success_allowed" in text


def test_phase_5_mobile_sync_dashboard_and_preview_are_read_only_and_json_safe() -> None:
    memory_payload = build_mobile_memory_status_preview_payload()
    sync_payload = build_mobile_sync_status_preview_payload()

    assert json.loads(json.dumps(memory_payload, sort_keys=True)) == memory_payload
    assert json.loads(json.dumps(sync_payload, sort_keys=True)) == sync_payload

    assert memory_payload["data"]["read_only"] is True
    assert memory_payload["data"]["preview_only"] is True
    assert memory_payload["data"]["core_write_allowed"] is False
    assert memory_payload["data"]["direct_server_write_allowed"] is False
    assert memory_payload["data"]["network_allowed"] is False
    assert memory_payload["data"]["socket_allowed"] is False
    assert memory_payload["data"]["tunnel_allowed"] is False
    assert memory_payload["data"]["dashboard_action_execution_allowed"] is False
    assert memory_payload["data"]["mutates_app_memory_store"] is False
    assert memory_payload["data"]["mutates_chat_memory_store"] is False

    assert sync_payload["data"]["read_only"] is True
    assert sync_payload["data"]["preview_only"] is True
    assert sync_payload["data"]["sync_execution_allowed"] is False
    assert sync_payload["data"]["dashboard_action_execution_allowed"] is False
    assert sync_payload["data"]["core_write_allowed"] is False
    assert sync_payload["data"]["direct_server_write_allowed"] is False
    assert sync_payload["data"]["network_allowed"] is False
    assert sync_payload["data"]["socket_allowed"] is False
    assert sync_payload["data"]["tunnel_allowed"] is False
    assert sync_payload["data"]["runtime_mutation_allowed"] is False
    assert sync_payload["data"]["fake_success_allowed"] is False
    assert sync_payload["data"]["silent_success_allowed"] is False


def test_phase_5_mobile_sync_preview_tools_do_not_execute_runtime_or_platform_api() -> None:
    preview_files = (
        "tools/mobile_memory_status_preview.py",
        "tools/mobile_sync_status_preview.py",
    )
    forbidden_tokens = (
        "ANDROID_SHELL",
        "IOS_SHELL",
        "MAKSIMAR_SERVER.MOBILE_SYNC_RUNTIME",
        ".evaluate(",
        ".create_session(",
        ".resolve(",
        "socket.",
        "requests.",
        "subprocess.",
    )

    for relative_path in preview_files:
        text = _read(relative_path)
        for token in forbidden_tokens:
            assert token not in text, f"{relative_path} contains {token}"


def test_phase_5_mobile_sync_sources_have_no_placeholder_runtime_logic() -> None:
    forbidden_patterns = (
        re.compile(r"\bpass\b"),
        re.compile(r"NotImplementedError"),
        re.compile(r"\bTODO\b"),
        re.compile(r"\bFIXME\b"),
        re.compile(r"fake success", re.IGNORECASE),
        re.compile(r"silent success allowed", re.IGNORECASE),
        re.compile(r"dummy runtime", re.IGNORECASE),
    )

    for relative_path in SYNC_EXPECTED_FILES:
        if not relative_path.endswith(".py"):
            continue
        text = _read(relative_path)
        for pattern in forbidden_patterns:
            assert pattern.search(text) is None, f"{relative_path} contains {pattern.pattern}"
