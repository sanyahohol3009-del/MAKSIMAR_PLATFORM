from __future__ import annotations

from MAKSIMAR_SERVER.REGISTRY_AUTO_ENROLLMENT import (
    build_enrollment_write_guard_decision,
)


def test_enrollment_write_guard_blocks_existing_without_overwrite(tmp_path) -> None:
    target = tmp_path / "manifest.json"
    target.write_text("{}", encoding="utf-8")

    decision = build_enrollment_write_guard_decision(target)

    assert decision.write_allowed is False
    assert decision.overwrite_existing is False
    assert decision.reason == "target_exists_no_overwrite"


def test_enrollment_write_guard_allows_missing_target(tmp_path) -> None:
    target = tmp_path / "manifest.json"

    decision = build_enrollment_write_guard_decision(target)

    assert decision.write_allowed is True
    assert decision.reason == "write_allowed"
