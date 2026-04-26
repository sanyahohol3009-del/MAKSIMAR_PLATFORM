#!/usr/bin/env python3
from __future__ import annotations

import sys
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[3]
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from MAKSIMAR_CORE_LIB.oob_dashboard.module_compatibility_contract import (  # noqa: E402
    build_module_compatibility_contract,
)
from MAKSIMAR_CORE_LIB.oob_dashboard.module_manifest_contract import (  # noqa: E402
    build_module_manifest_contract,
)
from MAKSIMAR_CORE_LIB.oob_dashboard.module_permission_matrix_contract import (  # noqa: E402
    build_module_permission_matrix_contract,
)


def main() -> None:
    manifest_contract = build_module_manifest_contract()
    permission_contract = build_module_permission_matrix_contract()
    compatibility_contract = build_module_compatibility_contract()

    print("MODULE GOVERNANCE PREVIEW")
    print("=" * 180)

    print("MANIFEST")
    for entry in manifest_contract.entries:
        print(
            f"{entry.module_id:<24} | "
            f"{entry.module_name:<30} | "
            f"{entry.module_role:<24} | "
            f"{entry.mount_mode:<16}"
        )

    print("-" * 180)
    print("PERMISSION MATRIX")
    for entry in permission_contract.entries:
        print(
            f"{entry.permission_entry_id:<24} | "
            f"{entry.module_id:<24} | "
            f"{entry.permission_level:<24} | "
            f"approval_required={entry.approval_required}"
        )

    print("-" * 180)
    print("COMPATIBILITY")
    for entry in compatibility_contract.entries:
        print(
            f"{entry.compatibility_entry_id:<28} | "
            f"{entry.module_id:<24} | "
            f"mount_eligible={entry.mount_eligible} | "
            f"permission_valid={entry.permission_valid} | "
            f"compatible={entry.compatible_with_base_family}"
        )

    print("-" * 180)
    print(
        f"manifest_total={manifest_contract.total_entries} | "
        f"permission_total={permission_contract.total_entries} | "
        f"compatibility_total={compatibility_contract.total_entries}"
    )


if __name__ == "__main__":
    main()
