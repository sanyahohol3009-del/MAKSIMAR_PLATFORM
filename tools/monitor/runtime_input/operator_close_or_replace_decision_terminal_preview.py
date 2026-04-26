#!/usr/bin/env python3
from __future__ import annotations

import sys
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[3]
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from MAKSIMAR_CORE_LIB.oob_dashboard.operator_close_or_replace_decision_contract import (  # noqa: E402
    build_operator_close_or_replace_decision_contract,
)


def main() -> None:
    contract = build_operator_close_or_replace_decision_contract()

    print("OPERATOR CLOSE OR REPLACE DECISION PREVIEW")
    print("=" * 180)

    for entry in contract.entries:
        print(
            f"{entry.decision_id:<38} | "
            f"{entry.display_target_id:<30} | "
            f"{entry.decision_class:<34}"
        )
        print(
            " " * 5
            + f"logical_target_id={entry.logical_target_id} | "
            f"decision_state={entry.decision_state} | "
            f"decision_action={entry.decision_action}"
        )
        print(
            " " * 5
            + f"candidate_display_target_id={entry.candidate_display_target_id} | "
            f"operator_visible={entry.operator_visible}"
        )
        print(" " * 5 + entry.description)

    print("-" * 180)
    print(
        f"total_entries={contract.total_entries} | "
        f"retain_entries={contract.retain_entries} | "
        f"replace_entries={contract.replace_entries} | "
        f"operator_visible_entries={contract.operator_visible_entries}"
    )


if __name__ == "__main__":
    main()
