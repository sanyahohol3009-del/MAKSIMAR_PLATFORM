#!/usr/bin/env python3
from __future__ import annotations

import sys
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[3]
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from MAKSIMAR_CORE_LIB.oob_dashboard.visual_backend_import_policy_contract import (  # noqa: E402
    build_visual_backend_import_policy_contract,
)
from MAKSIMAR_CORE_LIB.oob_dashboard.visual_backend_replaceability_contract import (  # noqa: E402
    build_visual_backend_replaceability_contract,
)


def main() -> None:
    replaceability_contract = build_visual_backend_replaceability_contract()
    import_policy_contract = build_visual_backend_import_policy_contract()

    print("REPLACEABILITY GUARD PREVIEW")
    print("=" * 180)
    print(
        f"replaceability_entries={replaceability_contract.total_entries} | "
        f"swap_ready_entries={replaceability_contract.swap_ready_entries} | "
        f"import_policy_entries={import_policy_contract.total_entries} | "
        f"swap_safe_entries={import_policy_contract.swap_safe_entries}"
    )


if __name__ == "__main__":
    main()
