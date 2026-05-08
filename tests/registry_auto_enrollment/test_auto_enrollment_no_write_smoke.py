from __future__ import annotations

from pathlib import Path

from MAKSIMAR_SERVER.REGISTRY_AUTO_ENROLLMENT import (
    build_auto_enrollment_dry_run_result,
)


def test_auto_enrollment_no_write_smoke(tmp_path: Path) -> None:
    cube = tmp_path / "DOMAIN_CUBES" / "demo_cube"
    cube.mkdir(parents=True)

    manifest = cube / "manifest.json"
    assert not manifest.exists()

    result = build_auto_enrollment_dry_run_result(tmp_path)

    assert result.total_entries == 1
    assert result.write_allowed_entries == 1
    assert result.dry_run is True
    assert not manifest.exists()
