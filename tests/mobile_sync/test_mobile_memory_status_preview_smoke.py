import json
from pathlib import Path

from tools.mobile_memory_status_preview import (
    build_mobile_memory_status_preview_payload,
    render_mobile_memory_status_preview_text,
)


def test_mobile_memory_status_preview_is_deterministic_and_read_only() -> None:
    first = build_mobile_memory_status_preview_payload()
    second = build_mobile_memory_status_preview_payload()

    assert first == second
    assert first["preview_kind"] == "read_only_mobile_memory_status"
    assert first["data"]["read_only"] is True
    assert first["data"]["preview_only"] is True
    assert first["data"]["core_write_allowed"] is False
    assert first["data"]["direct_server_write_allowed"] is False
    assert first["data"]["network_allowed"] is False
    assert first["data"]["mutates_app_memory_store"] is False
    assert first["data"]["mutates_chat_memory_store"] is False

    rendered = render_mobile_memory_status_preview_text()
    assert json.loads(rendered) == first


def test_mobile_memory_status_preview_does_not_call_runtime_or_platform_api() -> None:
    text = Path("tools/mobile_memory_status_preview.py").read_text(encoding="utf-8")
    forbidden_tokens = (
        "ANDROID_SHELL",
        "IOS_SHELL",
        "MAKSIMAR_SERVER.MOBILE_SYNC_RUNTIME",
        ".evaluate(",
        ".create_session(",
        "socket.",
        "requests.",
        "subprocess.",
    )

    for token in forbidden_tokens:
        assert token not in text
