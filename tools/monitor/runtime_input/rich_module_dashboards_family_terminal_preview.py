#!/usr/bin/env python3
from __future__ import annotations

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
    dashboard_surface_contract = build_module_dashboard_surface_contract()
    status_widget_contract = build_module_status_widget_contract()
    settings_schema_contract = build_module_settings_schema_contract()
    navigation_entry_contract = build_module_navigation_entry_contract()
    registry_audit_contract = build_module_registry_audit_contract()

    print("RICH MODULE DASHBOARDS FAMILY PREVIEW")
    print("=" * 180)
    print(
        f"dashboard_surface_entries={dashboard_surface_contract.total_entries} | "
        f"status_widget_entries={status_widget_contract.total_entries} | "
        f"settings_schema_entries={settings_schema_contract.total_entries} | "
        f"navigation_entry_entries={navigation_entry_contract.total_entries} | "
        f"registry_audit_entries={registry_audit_contract.total_entries}"
    )


if __name__ == "__main__":
    main()
