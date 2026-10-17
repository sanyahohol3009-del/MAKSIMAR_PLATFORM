from __future__ import annotations

import subprocess
import sys
from pathlib import Path

from tools.git_stage_guard import check_files


def test_git_stage_guard_help_smoke() -> None:
    tool = Path("tools/git_stage_guard.py")

    completed = subprocess.run(
        [sys.executable, str(tool), "--help"],
        text=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        check=False,
    )

    assert completed.returncode == 0
    assert "MAKSIMAR git stage guard" in completed.stdout


def test_git_stage_guard_blocks_forbidden_paths() -> None:
    result = check_files(
        (
            ".pymon",
            "EXTERNAL_BACKENDS/mempalace/source/file.py",
            "EXTERNAL_BACKENDS/mempalace/venv/bin/python",
            "tests/runtime_core/test_tmp.py",
        )
    )

    assert result.passed is False
    assert len(result.violations) == 4


import pytest
from tools.git_stage_guard import get_staged_files


def _synthetic_git(repo: Path, *args: str) -> None:
    subprocess.run(["git", *args], cwd=repo, check=True, capture_output=True)


def _generated_fixture_repo(tmp_path, monkeypatch, path, *, tracked):
    _synthetic_git(tmp_path, "init", "-q")
    target = tmp_path / path
    target.parent.mkdir(parents=True, exist_ok=True)
    target.write_bytes(b"synthetic generated payload")
    if tracked:
        _synthetic_git(tmp_path, "add", "--", path)
        _synthetic_git(tmp_path, "-c", "user.name=Fixture", "-c", "user.email=fixture@example.invalid",
                       "-c", "commit.gpgsign=false", "commit", "-qm", "seed fixture")
    monkeypatch.chdir(tmp_path)
    monkeypatch.delenv("MAKSIMAR_ALLOW_RUNTIME_CORE_STAGE", raising=False)
    return target


@pytest.mark.parametrize("path", [".pymon", "frontend/node_modules/pkg/index.js"])
@pytest.mark.parametrize("tracked", [False, True])
def test_generated_additions_and_modifications_remain_blocked(tmp_path, monkeypatch, path, tracked):
    target = _generated_fixture_repo(tmp_path, monkeypatch, path, tracked=tracked)
    target.write_bytes(b"new synthetic payload")
    _synthetic_git(tmp_path, "add", "--", path)
    assert check_files(get_staged_files()).violations == (path,)


@pytest.mark.parametrize("path", [".pymon", ".coverage", ".pytest_cache/data", "pkg/__pycache__/x.pyc", "pkg/a.pyc", "frontend/node_modules/pkg/index.js"])
def test_generated_index_removal_is_allowed_and_file_preserved(tmp_path, monkeypatch, path):
    target = _generated_fixture_repo(tmp_path, monkeypatch, path, tracked=True)
    before = target.read_bytes()
    _synthetic_git(tmp_path, "rm", "--cached", "--", path)
    assert target.read_bytes() == before
    assert check_files(get_staged_files()).passed
    assert path not in get_staged_files()


@pytest.mark.parametrize("path", ["EXTERNAL_BACKENDS/example/source/file.py", "tests/runtime_core/test_retained.py"])
def test_protected_source_and_test_removals_still_blocked(tmp_path, monkeypatch, path):
    _generated_fixture_repo(tmp_path, monkeypatch, path, tracked=True)
    _synthetic_git(tmp_path, "rm", "--cached", "--", path)
    assert check_files(get_staged_files()).violations == (path,)
