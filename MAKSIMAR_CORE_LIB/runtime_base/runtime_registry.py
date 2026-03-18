from __future__ import annotations

from collections import defaultdict
from pathlib import Path

from MAKSIMAR_CORE_LIB.runtime_base.runtime_loader import load_runtime_root
from MAKSIMAR_CORE_LIB.runtime_base.runtime_models import RuntimeDocument
from MAKSIMAR_CORE_LIB.shared_services.path_resolver import PATHS


def get_runtime_roots() -> dict[str, Path]:
    """Return canonical runtime root registry."""
    return {
        "project_runtime": PATHS.project_root / "runtime",
        "state_runtime": PATHS.project_root / "state",
        "capital_runtime": PATHS.project_root / "RUNTIME",
        "safety_runtime": PATHS.project_root / "SAFETY_FOUNDATION" / "RUNTIME",
    }


class RuntimeRegistry:
    """In-memory registry of runtime state documents."""

    def __init__(self) -> None:
        self._documents: dict[str, RuntimeDocument] = {}
        self._by_root: dict[str, list[RuntimeDocument]] = defaultdict(list)

    def load_all(self) -> None:
        """Load all known runtime roots."""
        for root_name, root_path in get_runtime_roots().items():
            results = load_runtime_root(root_path)

            for result in results:
                if not result.is_valid or result.document is None:
                    continue

                document = result.document
                self._documents[document.name] = document
                self._by_root[root_name].append(document)

    def get(self, name: str) -> RuntimeDocument | None:
        """Get runtime document by logical name."""
        return self._documents.get(name)

    def get_by_root(self, root_name: str) -> list[RuntimeDocument]:
        """Get runtime documents loaded from one root."""
        return self._by_root.get(root_name, [])
