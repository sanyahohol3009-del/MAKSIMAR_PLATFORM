from __future__ import annotations

from pathlib import Path


def test_tools_ctl_uses_canonical_python() -> None:
    ctl_file = Path.home() / "MAKSIMAR_PLATFORM" / "tools" / "ctl"
    content = ctl_file.read_text(encoding="utf-8")

    assert 'CANONICAL_PYTHON="$ROOT/.venv/bin/python"' in content or '".venv/bin/python"' in content
    assert 'SUPERVISOR.process_supervisor' in content


def test_tools_ctl_does_not_use_plain_python3_startup() -> None:
    ctl_file = Path.home() / "MAKSIMAR_PLATFORM" / "tools" / "ctl"
    content = ctl_file.read_text(encoding="utf-8")

    assert "python3 -m SUPERVISOR.process_supervisor" not in content


def test_tools_ctl_uses_project_python_for_heartbeat_checks() -> None:
    ctl_file = Path.home() / "MAKSIMAR_PLATFORM" / "tools" / "ctl"
    content = ctl_file.read_text(encoding="utf-8")

    assert '"$CANONICAL_PYTHON" - "$HEARTBEAT_FILE"' in content
