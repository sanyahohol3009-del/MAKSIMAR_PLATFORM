#!/usr/bin/env python3
from __future__ import annotations

import html
import json
import sys
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[3]
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from MAKSIMAR_CORE_LIB.oob_dashboard.module_dashboard_surface_contract import (  # noqa: E402
    build_module_dashboard_surface_contract,
)
from MAKSIMAR_CORE_LIB.oob_dashboard.module_navigation_entry_contract import (  # noqa: E402
    build_module_navigation_entry_contract,
)
from MAKSIMAR_CORE_LIB.oob_dashboard.module_registry_audit_contract import (  # noqa: E402
    build_module_registry_audit_contract,
)
from MAKSIMAR_CORE_LIB.oob_dashboard.module_settings_schema_contract import (  # noqa: E402
    build_module_settings_schema_contract,
)
from MAKSIMAR_CORE_LIB.oob_dashboard.module_status_widget_contract import (  # noqa: E402
    build_module_status_widget_contract,
)


def main() -> None:
    payload = {
        "module_dashboard_surface_contract": build_module_dashboard_surface_contract().total_entries,
        "module_status_widget_contract": build_module_status_widget_contract().total_entries,
        "module_settings_schema_contract": build_module_settings_schema_contract().total_entries,
        "module_navigation_entry_contract": build_module_navigation_entry_contract().total_entries,
        "module_registry_audit_contract": build_module_registry_audit_contract().total_entries,
    }

    pretty = html.escape(json.dumps(payload, indent=2))
    print("<!doctype html>")
    print("<html><head><meta charset='utf-8'><title>Rich Module Dashboards Family</title></head><body>")
    print("<h1>Rich Module Dashboards Family</h1>")
    print("<pre>")
    print(pretty)
    print("</pre>")
    print("</body></html>")


if __name__ == "__main__":
    main()
