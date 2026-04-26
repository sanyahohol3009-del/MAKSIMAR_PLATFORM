#!/usr/bin/env python3
from __future__ import annotations

import html
import json
import sys
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[3]
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from MAKSIMAR_CORE_LIB.oob_dashboard.gesture_adapter_contract import build_gesture_adapter_contract  # noqa: E402
from MAKSIMAR_CORE_LIB.oob_dashboard.gesture_input_contract import build_gesture_input_contract  # noqa: E402
from MAKSIMAR_CORE_LIB.oob_dashboard.gesture_policy_handoff_contract import build_gesture_policy_handoff_contract  # noqa: E402
from MAKSIMAR_CORE_LIB.oob_dashboard.gesture_preprocessing_contract import build_gesture_preprocessing_contract  # noqa: E402


def main() -> None:
    payload = {
        "gesture_input_contract": build_gesture_input_contract().total_entries,
        "gesture_preprocessing_contract": build_gesture_preprocessing_contract().total_entries,
        "gesture_adapter_contract": build_gesture_adapter_contract().total_entries,
        "gesture_policy_handoff_contract": build_gesture_policy_handoff_contract().total_entries,
    }

    pretty = html.escape(json.dumps(payload, indent=2))
    print("<!doctype html>")
    print("<html><head><meta charset='utf-8'><title>Gesture Flow</title></head><body>")
    print("<h1>Gesture Flow</h1>")
    print("<pre>")
    print(pretty)
    print("</pre>")
    print("</body></html>")


if __name__ == "__main__":
    main()
