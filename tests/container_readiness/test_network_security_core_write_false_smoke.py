from __future__ import annotations

from pathlib import Path
from typing import Any

import yaml


CUBE_DIR = Path("CONTAINER_DEPLOYMENT/cubes/network_security")


def _load_yaml(path: Path) -> dict[str, Any]:
    payload = yaml.safe_load(path.read_text(encoding="utf-8"))
    assert isinstance(payload, dict)
    return payload


def test_network_security_core_write_false_smoke() -> None:
    for path in sorted(CUBE_DIR.glob("*.yaml")):
        payload = _load_yaml(path)
        flags = payload["safety_flags"]

        assert flags["core_write_allowed"] is False
        assert flags["canonical_write_allowed"] is False
        assert flags["source_of_truth_override_allowed"] is False
        assert flags["direct_execution_allowed"] is False
        assert flags["privileged"] is False
        assert flags["host_network"] is False
        assert flags["host_pid"] is False
        assert flags["host_ipc"] is False
        assert flags["host_mount_allowed"] is False
        assert flags["secret_mount_allowed"] is False
        assert flags["run_as_non_root_required"] is True
        assert flags["read_only_filesystem_required"] is True
        assert flags["no_new_privileges_required"] is True
        assert flags["drop_capabilities_required"] is True
