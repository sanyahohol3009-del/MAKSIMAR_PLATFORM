from __future__ import annotations

from pathlib import Path

from MAKSIMAR_SERVER.REGISTRY_AUTO_ENROLLMENT import (
    build_auto_enrollment_summary,
    build_registry_auto_enrollment_phase_readiness,
)


def test_enrollment_existing_manifest_reuse_gate_smoke(tmp_path: Path) -> None:
    cube = tmp_path / "DOMAIN_CUBES" / "demo_cube"
    cube.mkdir(parents=True)

    manifest = cube / "manifest.json"
    manifest.write_text('{"module_slug":"demo_cube"}', encoding="utf-8")

    readiness = build_registry_auto_enrollment_phase_readiness(tmp_path)
    summary = build_auto_enrollment_summary(tmp_path)

    assert readiness.phase_ready is True
    assert readiness.write_allowed_entries == 0
    assert readiness.write_blocked_entries == 1
    assert summary["entries"][0]["manifest_exists"] is True
    assert summary["entries"][0]["enrollment_action"] == "reuse_existing_manifest"
    assert summary["entries"][0]["write_allowed"] is False
    assert manifest.exists()
