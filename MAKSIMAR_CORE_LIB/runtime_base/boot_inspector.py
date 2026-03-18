from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path

from MAKSIMAR_CORE_LIB.runtime_base.runtime_loader import load_runtime_root
from MAKSIMAR_CORE_LIB.runtime_base.runtime_summary import (
    RuntimeLoadSummary,
    build_runtime_summary,
)
from MAKSIMAR_CORE_LIB.shared_services.path_resolver import PATHS


@dataclass(frozen=True, slots=True)
class BootInspection:
    """Boot-state inspection result for one runtime root."""

    root_name: str
    root_path: Path
    summary: RuntimeLoadSummary


def inspect_boot_state() -> list[BootInspection]:
    """Inspect all known runtime roots.

    Returns:
        List of boot inspections by runtime root.
    """
    runtime_roots: dict[str, Path] = {
        "project_runtime": PATHS.project_root / "runtime",
        "state_runtime": PATHS.project_root / "state",
        "capital_runtime": PATHS.project_root / "RUNTIME",
        "safety_runtime": PATHS.project_root / "SAFETY_FOUNDATION" / "RUNTIME",
    }

    inspections: list[BootInspection] = []

    for root_name, root_path in runtime_roots.items():
        results = load_runtime_root(root_path)
        summary = build_runtime_summary(results)

        inspections.append(
            BootInspection(
                root_name=root_name,
                root_path=root_path,
                summary=summary,
            )
        )

    return inspections
