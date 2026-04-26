#!/usr/bin/env python3
from __future__ import annotations

import sys
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[3]
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from MAKSIMAR_CORE_LIB.oob_dashboard.avatar_state_panel_contract import (  # noqa: E402
    build_avatar_state_panel_contract,
)
from MAKSIMAR_CORE_LIB.oob_dashboard.family_status_panel_contract import (  # noqa: E402
    build_family_status_panel_contract,
)
from MAKSIMAR_CORE_LIB.oob_dashboard.security_telemetry_panel_contract import (  # noqa: E402
    build_security_telemetry_panel_contract,
)


def main() -> None:
    family_status_contract = build_family_status_panel_contract()
    avatar_state_contract = build_avatar_state_panel_contract()
    security_telemetry_contract = build_security_telemetry_panel_contract()

    print("FAMILY / AVATAR / SECURITY / TELEMETRY FAMILY PREVIEW")
    print("=" * 180)
    print(
        f"family_status_entries={family_status_contract.total_entries} | "
        f"avatar_state_entries={avatar_state_contract.total_entries} | "
        f"security_telemetry_entries={security_telemetry_contract.total_entries}"
    )


if __name__ == "__main__":
    main()
