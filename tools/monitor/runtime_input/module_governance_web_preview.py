#!/usr/bin/env python3
from __future__ import annotations

import html
import json
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

    payload = {
        "manifest": {
            "contract_id": manifest_contract.contract_id,
            "total_entries": manifest_contract.total_entries,
            "entries": [
                {
                    "module_id": entry.module_id,
                    "module_name": entry.module_name,
                    "module_role": entry.module_role,
                    "mount_mode": entry.mount_mode,
                    "allowed_workspace": entry.allowed_workspace,
                    "operator_visible": entry.operator_visible,
                    "truth_bound": entry.truth_bound,
                    "description": entry.description,
                }
                for entry in manifest_contract.entries
            ],
        },
        "permission_matrix": {
            "contract_id": permission_contract.contract_id,
            "total_entries": permission_contract.total_entries,
            "entries": [
                {
                    "permission_entry_id": entry.permission_entry_id,
                    "module_id": entry.module_id,
                    "permission_level": entry.permission_level,
                    "approval_required": entry.approval_required,
                    "operator_visible": entry.operator_visible,
                    "truth_bound": entry.truth_bound,
                    "description": entry.description,
                }
                for entry in permission_contract.entries
            ],
        },
        "compatibility": {
            "contract_id": compatibility_contract.contract_id,
            "total_entries": compatibility_contract.total_entries,
            "entries": [
                {
                    "compatibility_entry_id": entry.compatibility_entry_id,
                    "module_id": entry.module_id,
                    "mount_eligible": entry.mount_eligible,
                    "permission_valid": entry.permission_valid,
                    "compatible_with_base_family": entry.compatible_with_base_family,
                    "operator_visible": entry.operator_visible,
                    "truth_bound": entry.truth_bound,
                    "description": entry.description,
                }
                for entry in compatibility_contract.entries
            ],
        },
    }

    pretty = html.escape(json.dumps(payload, indent=2))

    print("<!doctype html>")
    print("<html><head><meta charset='utf-8'><title>Module Governance</title></head><body>")
    print("<h1>Module Governance</h1>")
    print("<pre>")
    print(pretty)
    print("</pre>")
    print("</body></html>")


if __name__ == "__main__":
    main()
