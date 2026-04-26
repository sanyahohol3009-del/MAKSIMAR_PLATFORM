from __future__ import annotations

from pathlib import Path


def test_oob_dashboard_ctl_references_oob_session() -> None:
    ctl_file = Path.home() / "MAKSIMAR_PLATFORM" / "tools" / "oob_dashboard_ctl"
    content = ctl_file.read_text(encoding="utf-8")

    assert 'SESSION_NAME="maksimar_oob"' in content
    assert "oob_foundation_monitor.py" in content


def test_oob_dashboard_ctl_uses_canonical_python() -> None:
    ctl_file = Path.home() / "MAKSIMAR_PLATFORM" / "tools" / "oob_dashboard_ctl"
    content = ctl_file.read_text(encoding="utf-8")

    assert '".venv/bin/python"' in content or '"/venv/bin/python"' in content
