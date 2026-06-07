from __future__ import annotations

from pathlib import Path


REQUIRED_ACTIONS = (
    "open_browser",
    "open_youtube",
    "open_youtube_kids_search",
    "read_project_status",
    "show_test_status",
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
    assert "allowlist_id: jarvis_pc_action_allowlist_v0_1" in text
    for action in actions:
        assert action["requires_owner_command"] == "true"
        assert action["requires_approval"] == "true"
        assert action["requires_audit"] == "true"
        assert action["runtime_execution_allowed"] == "false"
        assert action["direct_shell_allowed"] == "false"
        assert action["direct_browser_automation_allowed"] == "false"
        assert action["direct_pc_control_allowed"] == "false"

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

