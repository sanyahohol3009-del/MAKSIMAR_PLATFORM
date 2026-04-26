#!/usr/bin/env python3
from __future__ import annotations

import html
import json
import sys
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[3]
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from MAKSIMAR_CORE_LIB.oob_dashboard.base_family_bundle_contract import build_base_family_bundle_contract  # noqa: E402
from MAKSIMAR_CORE_LIB.oob_dashboard.base_family_manifest_contract import build_base_family_manifest_contract  # noqa: E402
from MAKSIMAR_CORE_LIB.oob_dashboard.base_family_mount_plan_contract import build_base_family_mount_plan_contract  # noqa: E402
from MAKSIMAR_CORE_LIB.oob_dashboard.base_family_readiness_contract import build_base_family_readiness_contract  # noqa: E402


def main() -> None:
    payload = {
        "base_family_manifest_contract": build_base_family_manifest_contract().total_entries,
        "base_family_bundle_contract": build_base_family_bundle_contract().total_entries,
        "base_family_mount_plan_contract": build_base_family_mount_plan_contract().total_entries,
        "base_family_readiness_contract": build_base_family_readiness_contract().total_entries,
    }

    pretty = html.escape(json.dumps(payload, indent=2))
    print("<!doctype html>")
    print("<html><head><meta charset='utf-8'><title>Base Family Composition</title></head><body>")
    print("<h1>Base Family Composition</h1>")
    print("<pre>")
    print(pretty)
    print("</pre>")
    print("</body></html>")


if __name__ == "__main__":
    main()
