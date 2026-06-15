from __future__ import annotations

import json
import sys
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[1]
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from MAKSIMAR_CORE_LIB.runtime_activation import (  # noqa: E402
    build_default_capability_activation_matrix,
)


def build_runtime_activation_matrix_preview_payload() -> dict[str, object]:
    matrix = build_default_capability_activation_matrix().to_read_model()
    return {
        "preview_id": "runtime_activation_matrix_preview_default",
        "preview_kind": "read_only_capability_activation_matrix",
        "schema_version": "1.0",
        "data": matrix,
    }


def render_runtime_activation_matrix_preview_text() -> str:
    return json.dumps(
        build_runtime_activation_matrix_preview_payload(),
        ensure_ascii=False,
        sort_keys=True,
        indent=2,
    )


def main() -> None:
    print(render_runtime_activation_matrix_preview_text())


if __name__ == "__main__":
    main()
