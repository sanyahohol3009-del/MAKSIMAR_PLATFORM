from __future__ import annotations

from pathlib import Path

from CORE_ROOT import runtime_paths


def test_root_path_is_path_instance() -> None:
    assert isinstance(runtime_paths.ROOT, Path)


def test_runtime_layout_creation(tmp_path: Path, monkeypatch) -> None:
    monkeypatch.setattr(runtime_paths, "RUNTIME_DIR", tmp_path / "RUNTIME")
    monkeypatch.setattr(runtime_paths, "RUNTIME_STATE_DIR", tmp_path / "RUNTIME" / "state")
    monkeypatch.setattr(runtime_paths, "RUNTIME_PIDS_DIR", tmp_path / "RUNTIME" / "pids")
    monkeypatch.setattr(runtime_paths, "LOGS_DIR", tmp_path / "logs")

    runtime_paths.ensure_runtime_layout()

    assert runtime_paths.RUNTIME_DIR.exists()
    assert runtime_paths.RUNTIME_STATE_DIR.exists()
    assert runtime_paths.RUNTIME_PIDS_DIR.exists()
    assert runtime_paths.LOGS_DIR.exists()


def test_python_candidates_are_ordered() -> None:
    candidates = runtime_paths.get_python_candidates()
    assert isinstance(candidates, tuple)
    assert len(candidates) >= 1


def test_canonical_python_prefers_override(tmp_path: Path, monkeypatch) -> None:
    fake_python = tmp_path / "python"
    fake_python.write_text("#!/bin/sh\n", encoding="utf-8")

    monkeypatch.setenv("MAKSIMAR_PYTHON", str(fake_python))

    resolved = runtime_paths.resolve_canonical_python()
    assert resolved == fake_python.resolve()
