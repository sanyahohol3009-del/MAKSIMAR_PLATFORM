#!/usr/bin/env python3
from __future__ import annotations

import sys
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[3]
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from MAKSIMAR_CORE_LIB.oob_dashboard.logs_panel_payload_builder import (  # noqa: E402
    build_logs_panel_payload,
)


def main() -> None:
    payload = build_logs_panel_payload()

    print("LOGS PANEL PREVIEW")
    print("=" * 140)
    print(
        f"panel_id={payload['panel_id']} | "
        f"panel_state={payload['panel_state']}"
    )
    print(f"summary={payload['summary']}")
    print(f"severity={payload['severity']}")
    print(f"visibility={payload['visibility']}")
    print(payload["description"])


if __name__ == "__main__":
    main()
