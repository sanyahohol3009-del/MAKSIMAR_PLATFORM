#!/usr/bin/env python3
from __future__ import annotations

import html
import json
import sys
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[3]
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from MAKSIMAR_CORE_LIB.oob_dashboard.voice_display_handoff_contract import build_voice_display_handoff_contract  # noqa: E402
from MAKSIMAR_CORE_LIB.oob_dashboard.voice_normalization_contract import build_voice_normalization_contract  # noqa: E402
from MAKSIMAR_CORE_LIB.oob_dashboard.voice_routing_contract import build_voice_routing_contract  # noqa: E402


def main() -> None:
    payload = {
        "voice_normalization_contract": build_voice_normalization_contract().total_entries,
        "voice_routing_contract": build_voice_routing_contract().total_entries,
        "voice_display_handoff_contract": build_voice_display_handoff_contract().total_entries,
    }

    pretty = html.escape(json.dumps(payload, indent=2))
    print("<!doctype html>")
    print("<html><head><meta charset='utf-8'><title>Voice Routing</title></head><body>")
    print("<h1>Voice Routing</h1>")
    print("<pre>")
    print(pretty)
    print("</pre>")
    print("</body></html>")


if __name__ == "__main__":
    main()
