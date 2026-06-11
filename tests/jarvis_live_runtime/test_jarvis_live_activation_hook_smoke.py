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


def test_activation_hook_snippet_has_opt_out_and_project_guard() -> None:
    from pathlib import Path

    text = Path("tools/jarvis_live_runtime/activate_hook_snippet.sh").read_text(
        encoding="utf-8"
    )

    assert "JARVIS_LIVE_AUTO_START" in text
    assert "JARVIS_LIVE_AUTO_START:-0" in text
    assert "JARVIS_LIVE_AUTO_START=1" in text
    assert "jarvis_live_start.py --background" in text
    assert "JARVIS_LIVE_ALWAYS_LISTEN" in text
    assert "JARVIS_LIVE_ALWAYS_LISTEN:-0" in text
    assert "JARVIS_LIVE_LISTEN_SECONDS" in text
    assert "JARVIS_LIVE_LISTEN_INTERVAL_SECONDS" in text
    assert "not inside MAKSIMAR_PLATFORM root" in text
