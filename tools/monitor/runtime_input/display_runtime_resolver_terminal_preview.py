from __future__ import annotations

import sys
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[3]
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from MAKSIMAR_CORE_LIB.oob_dashboard.display_runtime_resolver_integration_contract import (
    build_display_runtime_resolver_integration_contract,
)


def main() -> None:
    contract = build_display_runtime_resolver_integration_contract()

    print("DISPLAY RUNTIME RESOLVER PREVIEW")
    print("=" * 160)
    for entry in contract.entries:
        print(
            f"{entry.panel_id:<16} | "
            f"{entry.view_id:<28} | "
            f"{entry.display_target_id:<28} | "
            f"{entry.resolved_display_role:<28} | "
            f"{entry.fallback_display_target_id:<28}"
        )
        print(f"     {entry.description}")


if __name__ == "__main__":
    main()
