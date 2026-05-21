from __future__ import annotations

import json
import sys
from pathlib import Path


_REPO_ROOT = Path(__file__).resolve().parents[1]
if str(_REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(_REPO_ROOT))

from MAKSIMAR_CORE_LIB.foundation_registry_enrollment.foundation_layer_dashboard_visibility_builder import (
    build_foundation_layer_dashboard_visibility_read_model,
)


def main() -> None:
    read_model = build_foundation_layer_dashboard_visibility_read_model()
    payload = {
        "preview_id": "foundation_layer_dashboard_visibility_preview_v1",
        "preview_mode": "read_only",
        "registry_write_allowed": False,
        "runtime_mutation_allowed": False,
        "dashboard_control_allowed": False,
        "source_read_model": read_model.to_dict(),
    }
    print(json.dumps(payload, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
