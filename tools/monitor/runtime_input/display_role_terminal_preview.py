from __future__ import annotations

import sys
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[3]
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from MAKSIMAR_CORE_LIB.oob_dashboard.display_role_contract import (
    build_display_role_contract,
)


def main() -> None:
    contract = build_display_role_contract()

    print("DISPLAY ROLE PREVIEW")
    print("=" * 100)
    for entry in contract.entries:
        print(
            f"{entry.display_target_id:<32} | "
            f"{entry.display_role:<28}"
        )
        print(f"     {entry.description}")


if __name__ == "__main__":
    main()
