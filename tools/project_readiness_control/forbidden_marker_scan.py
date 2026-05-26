"""Read-only forbidden marker scanner.

This scanner is intentionally small and explicit. It only scans caller-provided
paths for caller-provided markers and never edits files.
"""

from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
from typing import Sequence


@dataclass(frozen=True, slots=True)
class ForbiddenMarkerFinding:
    path: str
    line_number: int
    marker: str
    line_preview: str

    def __post_init__(self) -> None:
        if not self.path:
            raise ValueError("path must not be empty")
        if self.line_number <= 0:
            raise ValueError("line_number must be positive")
        if not self.marker:
            raise ValueError("marker must not be empty")


@dataclass(frozen=True, slots=True)
class ForbiddenMarkerScanResult:
    scanned_files: int
    findings: tuple[ForbiddenMarkerFinding, ...]
    markers: tuple[str, ...]
    repo_mutation_allowed: bool = False
    auto_fix_allowed: bool = False

    def __post_init__(self) -> None:
        if self.scanned_files < 0:
            raise ValueError("scanned_files must not be negative")
        if any(not isinstance(item, ForbiddenMarkerFinding) for item in self.findings):
            raise TypeError("findings must contain ForbiddenMarkerFinding entries")
        if any(not marker for marker in self.markers):
            raise ValueError("markers must not contain empty values")
        if self.repo_mutation_allowed:
            raise ValueError("repo_mutation_allowed must remain false")
        if self.auto_fix_allowed:
            raise ValueError("auto_fix_allowed must remain false")

    @property
    def clean(self) -> bool:
        return not self.findings


def _iter_files(paths: Sequence[str | Path]) -> tuple[Path, ...]:
    files: list[Path] = []
    for raw_path in paths:
        path = Path(raw_path)
        if path.is_file():
            files.append(path)
        elif path.is_dir():
            files.extend(
                candidate
                for candidate in sorted(path.rglob("*"))
                if candidate.is_file()
                and "__pycache__" not in candidate.parts
                and ".pytest_cache" not in candidate.parts
            )
    return tuple(files)


def scan_forbidden_markers(
    paths: Sequence[str | Path],
    *,
    markers: Sequence[str],
) -> ForbiddenMarkerScanResult:
    marker_tuple = tuple(str(marker) for marker in markers)
    if not marker_tuple:
        raise ValueError("markers must not be empty")

    files = _iter_files(paths)
    findings: list[ForbiddenMarkerFinding] = []

    for file_path in files:
        try:
            text = file_path.read_text(encoding="utf-8")
        except UnicodeDecodeError:
            continue

        for index, line in enumerate(text.splitlines(), start=1):
            for marker in marker_tuple:
                if marker in line:
                    findings.append(
                        ForbiddenMarkerFinding(
                            path=str(file_path),
                            line_number=index,
                            marker=marker,
                            line_preview=line.strip()[:160],
                        )
                    )

    return ForbiddenMarkerScanResult(
        scanned_files=len(files),
        findings=tuple(findings),
        markers=marker_tuple,
    )
