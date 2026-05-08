from __future__ import annotations

from MAKSIMAR_SERVER.REGISTRY_AUTO_ENROLLMENT import (
    build_auto_enrollment_dry_run_result,
)


def test_auto_enrollment_runner_smoke() -> None:
    result = build_auto_enrollment_dry_run_result()

    assert result.dry_run is True
    assert result.run_ready is True
    assert result.total_entries == len(result.entries)
    assert result.total_entries == (
        result.write_allowed_entries + result.write_blocked_entries
    )

    for entry in result.entries:
        assert entry.registry_entry_ready is True
        assert entry.dashboard_exposure_ready is True
        assert entry.observability_binding_ready is True
