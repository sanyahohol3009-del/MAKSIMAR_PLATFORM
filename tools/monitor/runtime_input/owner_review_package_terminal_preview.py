#!/usr/bin/env python3
from __future__ import annotations

import sys
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[3]
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from MAKSIMAR_CORE_LIB.oob_dashboard.owner_review_package_contract import (  # noqa: E402
    build_owner_review_package_contract,
)


def main() -> None:
    contract = build_owner_review_package_contract()

    print("OWNER REVIEW PACKAGE PREVIEW")
    print("=" * 180)

    for entry in contract.entries:
        print(
            f"{entry.owner_review_package_id:<28} | "
            f"{entry.operator_intent_id:<18} | "
            f"{entry.panel_id:<16} | "
            f"{entry.owner_review_package_class:<30}"
        )
        print(
            " " * 5
            + f"workspace_id={entry.workspace_id} | "
            f"owner_review_package_state={entry.owner_review_package_state}"
        )
        print(
            " " * 5
            + f"owner_review_evidence_mode={entry.owner_review_evidence_mode} | "
            f"approval_required={entry.approval_required} | "
            f"handoff_ready={entry.handoff_ready} | "
            f"audit_visible={entry.audit_visible}"
        )
        print(
            " " * 5
            + f"operator_visible={entry.operator_visible} | "
            f"trace_id={entry.trace_id}"
        )
        print(" " * 5 + entry.description)

    print("-" * 180)
    print(
        f"total_entries={contract.total_entries} | "
        f"read_only_review_entries={contract.read_only_review_entries} | "
        f"approval_bound_review_entries={contract.approval_bound_review_entries} | "
        f"audit_visible_entries={contract.audit_visible_entries} | "
        f"operator_visible_entries={contract.operator_visible_entries}"
    )


if __name__ == "__main__":
    main()
