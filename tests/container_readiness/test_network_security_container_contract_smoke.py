from __future__ import annotations

from pathlib import Path
from typing import Any

import yaml


CUBE_DIR = Path("CONTAINER_DEPLOYMENT/cubes/network_security")

REQUIRED_FILES = (
    CUBE_DIR / "container_contract.yaml",
    CUBE_DIR / "network_policy.yaml",
    CUBE_DIR / "runtime_profile.yaml",
    CUBE_DIR / "healthcheck_contract.yaml",
    CUBE_DIR / "readiness_probe_contract.yaml",
)


def _load_yaml(path: Path) -> dict[str, Any]:
    payload = yaml.safe_load(path.read_text(encoding="utf-8"))
    assert isinstance(payload, dict)
    return payload


def test_network_security_container_contract_smoke() -> None:
    for path in REQUIRED_FILES:
        assert path.exists(), f"missing {path}"

    contract = _load_yaml(CUBE_DIR / "container_contract.yaml")

    assert contract["schema_id"] == "network_security_container_contract_v1"
    assert contract["cube_id"] == "network_security"
    assert contract["service_id"] == "network_security_runtime"
    assert contract["network_segment"] == "net_security"
    assert contract["status"] == "readiness_projection_only"

    global_layer = contract["global_container_layer"]
    assert global_layer["schema_ref"] == "CONTAINER_DEPLOYMENT/container_contract.schema.yaml"
    assert global_layer["blueprint_ref"] == "CONTAINER_DEPLOYMENT/container_deployment_blueprint.yaml"
    assert global_layer["security_gate_ref"] == "CONTAINER_DEPLOYMENT/deployment_gates/security_required_gate.yaml"

    assert Path(global_layer["schema_ref"]).exists()
    assert Path(global_layer["blueprint_ref"]).exists()
    assert Path(global_layer["security_gate_ref"]).exists()

    flags = contract["safety_flags"]
    assert flags["read_only_readiness_only"] is True
    assert flags["dashboard_visible"] is True
    assert flags["operator_approval_required"] is True
    assert flags["healthcheck_required"] is True
    assert flags["readiness_probe_required"] is True
