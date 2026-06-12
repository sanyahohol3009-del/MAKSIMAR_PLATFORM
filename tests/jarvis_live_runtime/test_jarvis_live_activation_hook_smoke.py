from tools.jarvis_live_runtime.install_venv_activation_hook import (
    BLOCK_END,
    BLOCK_START,
    HOOK_BLOCK,
    _insert_block,
    _strip_block,
)


def test_install_tool_preview_mode_does_not_edit_activate_content() -> None:
    original = "original\n"
    preview = _insert_block(original)

    assert original == "original\n"
    assert BLOCK_START in preview
    assert BLOCK_END in preview
    assert HOOK_BLOCK in preview


def test_activation_hook_idempotency_and_remove_logic() -> None:
    original = "activate-body\n"
    once = _insert_block(original)
    twice = _insert_block(once)
    removed = _strip_block(twice)

    assert once == twice
    assert BLOCK_START in once
    assert BLOCK_END in once
    assert removed == original


def test_activation_hook_snippet_exposes_only_manual_chat_launcher() -> None:
    from pathlib import Path

    text = Path("tools/jarvis_live_runtime/activate_hook_snippet.sh").read_text(
        encoding="utf-8"
    )

    assert "chat()" in text
    assert "jarvis_live_chat_launcher.py" in text
    assert "JARVIS_LIVE_AUTO_START" not in text
    assert "jarvis_live_start.py --background" not in text
    assert "JARVIS_LIVE_ALWAYS_LISTEN" not in text
    assert "JARVIS_LIVE_LISTEN_SECONDS" not in text
    assert "JARVIS_LIVE_LISTEN_INTERVAL_SECONDS" not in text


def test_activate_cleanup_uses_fake_activate_content_not_local_venv() -> None:
    fake_activate = (
        "activate-body\n"
        f"{BLOCK_START}\n"
        "source tools/jarvis_live_runtime/activate_hook_snippet.sh\n"
        f"{BLOCK_END}\n"
        "activate-tail\n"
    )

    cleaned = _strip_block(fake_activate)

    assert cleaned == "activate-body\nactivate-tail\n"
    assert "JARVIS_LIVE_AUTO_START" not in cleaned
    assert "activate_hook_snippet.sh" not in cleaned
    assert "jarvis_live_start.py --background" not in cleaned


def test_activation_hook_snippet_has_no_autostart_branch() -> None:
    from pathlib import Path

    text = Path("tools/jarvis_live_runtime/activate_hook_snippet.sh").read_text(
        encoding="utf-8"
    )

    assert 'JARVIS_LIVE_AUTO_START:-0' not in text
    assert 'jarvis_live_start.py --background' not in text
    assert 'starting/background/status' not in text
