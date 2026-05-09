from __future__ import annotations

from MAKSIMAR_SERVER.architecture_map_runtime import (
    build_domain_cube_memory_locator_contract,
)


def test_domain_cube_slug_identity_preserved_smoke() -> None:
    contract = build_domain_cube_memory_locator_contract()

    entries_by_slug = {entry.cube_slug: entry for entry in contract.entries}

    assert "3d_cube" in entries_by_slug

    entry = entries_by_slug["3d_cube"]

    assert entry.cube_slug == "3d_cube"
    assert entry.cube_path == "DOMAIN_CUBES/3d_cube"
    assert entry.locator_id == "domain_cube_memory_locator_cube_3d_cube"
