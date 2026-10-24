from __future__ import annotations

from pathlib import Path


REQUIRED_ACTIONS = (
    "open_browser",
    "open_opera",
    "close_opera",
    "close_all_opera",
    "type_text",
    "volume_up",
    "volume_down",
    "volume_mute",
    "read_screen",
    "browser_search",
)


def _parse_action_blocks(text: str) -> list[dict[str, str]]:
    blocks: list[dict[str, str]] = []
    current: dict[str, str] | None = None
    for raw_line in text.splitlines():
        line = raw_line.strip()
        if line.startswith("- action_id:"):
            if current is not None:
                blocks.append(current)
            current = {"action_id": line.split(":", 1)[1].strip()}
        elif current is not None and ":" in line:
            key, value = line.split(":", 1)
            current[key.strip()] = value.strip().strip('"')
    if current is not None:
        blocks.append(current)
    return blocks


def test_jarvis_pc_action_allowlist_yaml_is_safe_contract() -> None:
    root = Path(__file__).resolve().parents[2]
    path = root / "WORKFLOW_ENGINE/config/jarvis_pc_action_allowlist.yaml"
    text = path.read_text(encoding="utf-8")
    actions = _parse_action_blocks(text)

    assert tuple(action["action_id"] for action in actions) == REQUIRED_ACTIONS
    assert "allowlist_id: jarvis_pc_action_allowlist_v1" in text
    for action in actions:
        assert action["requires_owner_command"] == "true"
        assert action["requires_approval"] == "false"
        assert action["requires_audit"] == "true"
        assert action["operation_allowlisted"] == "true"
        assert action["direct_shell_allowed"] == "false"
        assert action["owner_low_risk_policy_eligible"] == "true"
        assert "runtime_execution_allowed" not in action

    lowered = text.lower()
    for marker in (
        "\ncommand:",
        "\r\ncommand:",
        " executable:",
        "\nexecutable:",
        "\r\nexecutable:",
        " path:",
        "\npath:",
        "\r\npath:",
        "http://",
        "https://",
        "hidden",
    ):
        assert marker not in lowered
