from __future__ import annotations

import json
import subprocess
import sys
from pathlib import Path


def test_project_file_readiness_map_cli_smoke() -> None:
    project_root = Path(__file__).resolve().parents[2]

    completed = subprocess.run(
        [
            sys.executable,
            "tools/project_readiness_control/project_file_readiness_map.py",
            "--batch-id",
            "0.1",
            "--json",
        ],
        cwd=project_root,
        text=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        check=False,
    )

    assert completed.returncode == 0, completed.stdout + completed.stderr

    payload = json.loads(completed.stdout)
    assert payload["status"] == "READY"
    assert payload["total_batches"] == 1
    assert payload["reports"][0]["batch_id"] == "0.1"
