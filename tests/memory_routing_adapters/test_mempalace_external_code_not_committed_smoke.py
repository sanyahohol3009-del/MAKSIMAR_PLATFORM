from __future__ import annotations

import subprocess


def test_mempalace_external_code_not_committed_smoke() -> None:
    tracked = subprocess.check_output(
        ["git", "ls-files", "EXTERNAL_BACKENDS/mempalace/source", "EXTERNAL_BACKENDS/mempalace/venv"],
        text=True,
    ).strip()

    assert tracked == ""
