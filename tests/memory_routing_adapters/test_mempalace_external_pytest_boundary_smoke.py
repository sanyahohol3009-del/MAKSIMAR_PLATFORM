from __future__ import annotations

from pathlib import Path


def test_mempalace_external_pytest_boundary_smoke() -> None:
    conftest = Path("conftest.py")

    assert conftest.exists()

    text = conftest.read_text(encoding="utf-8")

    assert "collect_ignore" in text
    assert "EXTERNAL_BACKENDS" in text
