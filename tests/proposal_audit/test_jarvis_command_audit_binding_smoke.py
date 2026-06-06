from __future__ import annotations

from pathlib import Path

from MAKSIMAR_CORE_LIB.security_layer.jarvis_action_allowlist_contract import (
    ALLOWED_JARVIS_ACTION_CANDIDATES,
    FORBIDDEN_JARVIS_ACTIONS,
)
from MAKSIMAR_SERVER.PROPOSAL_AUDIT.jarvis_command_audit_binding import (
    build_jarvis_command_audit_binding_read_model,
)


def test_jarvis_command_audit_binding_is_proposal_only() -> None:
    read_model = build_jarvis_command_audit_binding_read_model()

    assert read_model["read_only"] is True
    assert read_model["dashboard_safe"] is True
    assert read_model["proposal_only"] is True
    assert read_model["execution_enabled"] is False
    assert read_model["audit_required"] is True
    assert read_model["approval_required"] is True
    assert read_model["preview_required"] is True
    assert read_model["allowlist_required"] is True
    assert read_model["audit_event_kind"] == "jarvis_command_proposal"
    assert read_model["allowed_action_ids"] == ALLOWED_JARVIS_ACTION_CANDIDATES
    assert read_model["forbidden_actions"] == FORBIDDEN_JARVIS_ACTIONS


def test_jarvis_command_audit_binding_source_has_no_runtime_markers() -> None:
    root = Path(__file__).resolve().parents[2]
    source = (
        root / "MAKSIMAR_SERVER/PROPOSAL_AUDIT/jarvis_command_audit_binding.py"
    ).read_text(encoding="utf-8")
    lowered = source.lower()

    for marker in (
        "subprocess",
        "os.system",
        "shell=true",
        "pyautogui",
        "keyboard",
        "mouse",
        "webbrowser.open",
        "requests",
        "socket",
        "git commit",
        "git push",
    ):
        assert marker not in lowered

