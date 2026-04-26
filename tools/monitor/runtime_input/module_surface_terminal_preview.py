#!/usr/bin/env python3
from __future__ import annotations

import sys
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[3]
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from MAKSIMAR_CORE_LIB.oob_dashboard.module_alert_binding_contract import build_module_alert_binding_contract  # noqa: E402
from MAKSIMAR_CORE_LIB.oob_dashboard.module_dashboard_surface_contract import build_module_dashboard_surface_contract  # noqa: E402
from MAKSIMAR_CORE_LIB.oob_dashboard.module_mount_eligibility_contract import build_module_mount_eligibility_contract  # noqa: E402
from MAKSIMAR_CORE_LIB.oob_dashboard.module_navigation_entry_contract import build_module_navigation_entry_contract  # noqa: E402
from MAKSIMAR_CORE_LIB.oob_dashboard.module_registry_audit_contract import build_module_registry_audit_contract  # noqa: E402
from MAKSIMAR_CORE_LIB.oob_dashboard.module_settings_schema_contract import build_module_settings_schema_contract  # noqa: E402
from MAKSIMAR_CORE_LIB.oob_dashboard.module_status_widget_contract import build_module_status_widget_contract  # noqa: E402


def main() -> None:
    surface = build_module_dashboard_surface_contract()
    settings = build_module_settings_schema_contract()
    widget = build_module_status_widget_contract()
    mount = build_module_mount_eligibility_contract()
    navigation = build_module_navigation_entry_contract()
    alert = build_module_alert_binding_contract()
    registry = build_module_registry_audit_contract()

    print("MODULE SURFACE PREVIEW")
    print("=" * 180)
    print(
        f"dashboard_surface_total={surface.total_entries} | "
        f"settings_total={settings.total_entries} | "
        f"status_widget_total={widget.total_entries}"
    )
    print(
        f"mount_total={mount.total_entries} | "
        f"navigation_total={navigation.total_entries} | "
        f"alert_total={alert.total_entries} | "
        f"registry_total={registry.total_entries}"
    )


if __name__ == "__main__":
    main()
