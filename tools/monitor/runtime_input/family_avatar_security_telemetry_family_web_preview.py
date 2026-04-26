#!/usr/bin/env python3
from __future__ import annotations

import html
import json
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
    payload = {
        "family_status_panel_contract": build_family_status_panel_contract().total_entries,
        "avatar_state_panel_contract": build_avatar_state_panel_contract().total_entries,
        "security_telemetry_panel_contract": build_security_telemetry_panel_contract().total_entries,
    }

    pretty = html.escape(json.dumps(payload, indent=2))
    print("<!doctype html>")
    print("<html><head><meta charset='utf-8'><title>Family Avatar Security Telemetry Family</title></head><body>")
    print("<h1>Family / Avatar / Security / Telemetry Family</h1>")
    print("<pre>")
    print(pretty)
    print("</pre>")
    print("</body></html>")


if __name__ == "__main__":
    main()
