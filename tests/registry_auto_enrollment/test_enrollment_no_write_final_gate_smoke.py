from __future__ import annotations

from pathlib import Path

from MAKSIMAR_SERVER.REGISTRY_AUTO_ENROLLMENT import (
    build_registry_auto_enrollment_phase_readiness,
)


def test_enrollment_no_write_final_gate_smoke(tmp_path: Path) -> None:
    cube = tmp_path / "DOMAIN_CUBES" / "demo_cube"
    cube.mkdir(parents=True)

    manifest = cube / "manifest.json"
    assert not manifest.exists()

    readiness = build_registry_auto_enrollment_phase_readiness(tmp_path)

    assert readiness.phase_ready is True
    assert readiness.no_write_verified is True
    assert readiness.write_allowed_entries == 1
    assert readiness.write_blocked_entries == 0
    assert not manifest.exists()
