#!/usr/bin/env python3
from __future__ import annotations

import sys
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[3]
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from MAKSIMAR_CORE_LIB.oob_dashboard.guard_chain_panel_payload_builder import (  # noqa: E402
    build_guard_chain_panel_payload,
)


def main() -> None:
    payload = build_guard_chain_panel_payload()

    print("GUARD CHAIN PANEL PREVIEW")
    print("=" * 140)
    print(
        f"panel_id={payload['panel_id']} | "
        f"panel_state={payload['panel_state']}"
    )
    print(f"summary={payload['summary']}")
    print(f"chain_health={payload['chain_health']}")
    print(f"presence={payload['presence']}")
    print(f"state_context={payload['state_context']}")
    print(f"visibility={payload['visibility']}")
    print(payload["description"])


if __name__ == "__main__":
    main()
