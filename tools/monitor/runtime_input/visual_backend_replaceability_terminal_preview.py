#!/usr/bin/env python3
from __future__ import annotations

import sys
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[3]
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from MAKSIMAR_CORE_LIB.oob_dashboard.visual_backend_path_replaceability_contract import (  # noqa: E402
    build_visual_backend_path_replaceability_contract,
)
from MAKSIMAR_CORE_LIB.oob_dashboard.visual_backend_swap_equivalence_contract import (  # noqa: E402
    build_visual_backend_swap_equivalence_contract,
)


def main() -> None:
    swap_contract = build_visual_backend_swap_equivalence_contract()
    path_contract = build_visual_backend_path_replaceability_contract()

    print("VISUAL BACKEND REPLACEABILITY PREVIEW")
    print("=" * 180)
    print(
        f"swap_equivalence_entries={swap_contract.total_entries} | "
        f"swap_equivalent_entries={swap_contract.swap_equivalent_entries} | "
        f"path_replaceability_entries={path_contract.total_entries} | "
        f"path_swap_safe_entries={path_contract.path_swap_safe_entries}"
    )


if __name__ == "__main__":
    main()
