#!/usr/bin/env python3
from __future__ import annotations

import html
import json
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
    title = html.escape(payload["panel_id"])
    state = html.escape(payload["panel_state"])
    pretty = html.escape(json.dumps(payload, indent=2))

    print("<!doctype html>")
    print("<html><head><meta charset='utf-8'><title>Logs Panel</title></head><body>")
    print("<h1>Logs Panel</h1>")
    print(f"<p><strong>panel_id:</strong> {title}</p>")
    print(f"<p><strong>panel_state:</strong> {state}</p>")
    print("<pre>")
    print(pretty)
    print("</pre>")
    print("</body></html>")


if __name__ == "__main__":
    main()
