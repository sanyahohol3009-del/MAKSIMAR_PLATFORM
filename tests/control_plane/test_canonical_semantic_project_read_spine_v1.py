"""Compatibility marker for the superseded v1 canonical project-read suite."""

from pathlib import Path


def test_phase_1b_v2_semantic_suite_is_present():
    assert Path("tests/control_plane/test_canonical_semantic_turn_v2.py").is_file()
