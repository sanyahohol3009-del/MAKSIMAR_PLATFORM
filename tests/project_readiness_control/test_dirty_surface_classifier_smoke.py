from __future__ import annotations

from tools.project_readiness_control.dirty_surface_classifier import (
    classify_dirty_surfaces_from_status,
)


def test_dirty_surface_classifier_is_read_only() -> None:
    result = classify_dirty_surfaces_from_status(
        " M .pymon\n"
        "A  tools/example.py\n"
        "?? tests/new_test.py\n"
        "R  old.py -> new.py\n"
    )

    assert result.dirty_count == 4
    assert result.untracked_count == 1
    assert result.entries[0].category == "modified"
    assert result.entries[1].category == "staged"
    assert result.entries[2].category == "untracked"
    assert result.entries[3].category == "renamed"
    assert result.entries[3].path == "new.py"
    assert result.repo_mutation_allowed is False
    assert result.auto_fix_allowed is False
