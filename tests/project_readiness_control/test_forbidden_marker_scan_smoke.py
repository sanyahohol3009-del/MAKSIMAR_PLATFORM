from __future__ import annotations

from tools.project_readiness_control.forbidden_marker_scan import scan_forbidden_markers


def test_forbidden_marker_scan_is_explicit_and_read_only(tmp_path) -> None:
    candidate = tmp_path / "candidate.py"
    candidate.write_text("safe = True\nmarker = 'BAD_MARKER'\n", encoding="utf-8")

    result = scan_forbidden_markers((candidate,), markers=("BAD_MARKER",))

    assert result.clean is False
    assert result.scanned_files == 1
    assert len(result.findings) == 1
    assert result.findings[0].path == str(candidate)
    assert result.findings[0].line_number == 2
    assert result.repo_mutation_allowed is False
    assert result.auto_fix_allowed is False
