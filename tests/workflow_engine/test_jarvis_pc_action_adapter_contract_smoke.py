from __future__ import annotations

from pathlib import Path

import pytest

from MAKSIMAR_SERVER.WORKFLOW_AUTOMATION_RUNTIME.jarvis_pc_action_adapter_contract import (
    FALSE_ADAPTER_GATES,
    JARVIS_PC_ACTION_ALLOWLIST_IDS,
    JarvisPcActionAdapterContract,
    build_jarvis_pc_action_adapter_contract,
)


def test_jarvis_pc_action_adapter_is_controlled_candidate_only() -> None:
    read_model = build_jarvis_pc_action_adapter_contract().to_read_model()

    assert read_model["allowed_action_ids"] == JARVIS_PC_ACTION_ALLOWLIST_IDS
    assert read_model["controlled_pc_action_candidate"] is True
    assert read_model["owner_command_required"] is True
    assert read_model["allowlist_required"] is True
    assert read_model["approval_required"] is True
    assert read_model["audit_required"] is True
    assert read_model["screen_context_required"] is True
    assert read_model["explicit_action_preview_required"] is True
    for key in FALSE_ADAPTER_GATES:
        assert read_model[key] is False


def test_jarvis_pc_action_adapter_rejects_dangerous_true_flags() -> None:
    adapter = build_jarvis_pc_action_adapter_contract()
    gates = tuple(
        (key, True if key == "direct_pc_control_allowed" else value)
        for key, value in adapter.disabled_gates
    )

    with pytest.raises(ValueError, match="must remain disabled"):
        JarvisPcActionAdapterContract(
            adapter_id="jarvis_pc_action_adapter_contract_v0_1",
            allowed_action_ids=JARVIS_PC_ACTION_ALLOWLIST_IDS,
            disabled_gates=gates,
        )


def test_jarvis_pc_action_adapter_source_has_no_runtime_markers() -> None:
    root = Path(__file__).resolve().parents[2]
    lowered = (
        root
        / "MAKSIMAR_SERVER/WORKFLOW_AUTOMATION_RUNTIME/jarvis_pc_action_adapter_contract.py"
    ).read_text(encoding="utf-8").lower()
    for marker in (
        "pyautogui",
        "pynput",
        "xdotool",
        "keyboard.",
        "mouse.",
        "click(",
        "subprocess",
        "os.system",
        "powershell",
        "shell=true",
        "webbrowser",
        "socket",
    ):
        assert marker not in lowered

