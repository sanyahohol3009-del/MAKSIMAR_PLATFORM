#!/usr/bin/env python3
from __future__ import annotations

import html
import json
import sys
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[3]
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from MAKSIMAR_CORE_LIB.oob_dashboard.interaction_exposure_contract import build_interaction_exposure_contract  # noqa: E402
from MAKSIMAR_CORE_LIB.oob_dashboard.interaction_incident_surface_contract import build_interaction_incident_surface_contract  # noqa: E402
from MAKSIMAR_CORE_LIB.oob_dashboard.interaction_observability_contract import build_interaction_observability_contract  # noqa: E402


def main() -> None:
    payload = {
        "interaction_exposure_contract": build_interaction_exposure_contract().total_entries,
        "interaction_observability_contract": build_interaction_observability_contract().total_entries,
        "interaction_incident_surface_contract": build_interaction_incident_surface_contract().total_entries,
    }

    pretty = html.escape(json.dumps(payload, indent=2))
    print("<!doctype html>")
    print("<html><head><meta charset='utf-8'><title>Interaction Observability</title></head><body>")
    print("<h1>Interaction Observability</h1>")
    print("<pre>")
    print(pretty)
    print("</pre>")
    print("</body></html>")


if __name__ == "__main__":
    main()
