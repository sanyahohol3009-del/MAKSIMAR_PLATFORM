from __future__ import annotations

from pathlib import Path
from typing import Any

import yaml


CUBE_DIR = Path("CONTAINER_DEPLOYMENT/cubes/network_security")


def _load_yaml(path: Path) -> dict[str, Any]:
    payload = yaml.safe_load(path.read_text(encoding="utf-8"))
    assert isinstance(payload, dict)
    return payload


def test_network_security_runtime_mutation_false_smoke() -> None:
    for path in sorted(CUBE_DIR.glob("*.yaml")):
        payload = _load_yaml(path)
        flags = payload["safety_flags"]

        assert flags["active_deployment_allowed"] is False
        assert flags["active_docker_deployment_allowed"] is False
        assert flags["active_compose_deployment_allowed"] is False
        assert flags["docker_start_allowed"] is False
        assert flags["compose_start_allowed"] is False
        assert flags["production_deployment_allowed"] is False
        assert flags["ports_opened"] is False
        assert flags["published_ports_allowed"] is False
        assert flags["public_exposure_allowed"] is False
        assert flags["external_network_access_enabled"] is False
        assert flags["runtime_mutation_allowed"] is False
        assert flags["runtime_network_mutation_allowed"] is False

    network_policy = _load_yaml(CUBE_DIR / "network_policy.yaml")
    assert network_policy["ingress"]["allowed"] is False
    assert network_policy["ingress"]["published_ports"] == []
    assert network_policy["egress"]["allowed"] is False
    assert network_policy["p2p"]["real_p2p_networking_allowed"] is False
    assert network_policy["p2p"]["peer_discovery_allowed"] is False
    assert network_policy["vpn"]["tunnel_creation_allowed"] is False

    runtime_profile = _load_yaml(CUBE_DIR / "runtime_profile.yaml")
    assert runtime_profile["runtime_profile"]["command_execution_allowed"] is False
    assert runtime_profile["runtime_profile"]["process_start_allowed"] is False
    assert runtime_profile["runtime_profile"]["service_start_allowed"] is False
