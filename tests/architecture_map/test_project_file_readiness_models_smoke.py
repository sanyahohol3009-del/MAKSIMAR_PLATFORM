from __future__ import annotations

from pathlib import Path

import pytest

from MAKSIMAR_CORE_LIB.architecture_map.project_file_readiness_models import (
    ExpectedProjectFile,
    build_project_batch_readiness_report,
)


def test_project_file_readiness_models_smoke(tmp_path: Path) -> None:
    expected_file_path = tmp_path / "demo.txt"
    expected_file_path.write_text("ok\n", encoding="utf-8")

    report = build_project_batch_readiness_report(
        batch_id="demo.1",
        title="Demo Batch",
        expected_files=(
            ExpectedProjectFile(path="demo.txt", role="doc"),
            ExpectedProjectFile(path="missing.txt", role="test"),
        ),
        project_root=tmp_path,
    )

    assert report.status == "PARTIAL"
    assert report.total_files == 2
    assert report.existing_files == 1
    assert report.missing_required_files == ("missing.txt",)


def test_project_file_readiness_rejects_absolute_paths() -> None:
    with pytest.raises(ValueError):
        ExpectedProjectFile(path="/absolute/path.py", role="source")


def test_project_file_readiness_rejects_invalid_role() -> None:
    with pytest.raises(ValueError):
        ExpectedProjectFile(path="demo.txt", role="invalid")
