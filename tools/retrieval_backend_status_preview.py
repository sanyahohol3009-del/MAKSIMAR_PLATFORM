from __future__ import annotations

import sys
from pathlib import Path


PROJECT_ROOT = Path(__file__).resolve().parents[1]
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from MAKSIMAR_CORE_LIB.retrieval_backend.retrieval_backend_status_read_model import (
    build_retrieval_backend_status_read_model_json,
)


def main() -> int:
    print(build_retrieval_backend_status_read_model_json())
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
