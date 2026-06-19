from __future__ import annotations

import json

from MAKSIMAR_CORE_LIB.action_library_adapters.external_tool_library_adapter import (
    build_jarvis_external_adapter_visibility_read_model,
)


def build_external_tool_library_probe() -> dict[str, object]:
    return build_jarvis_external_adapter_visibility_read_model()


def main() -> int:
    print(json.dumps(build_external_tool_library_probe(), indent=2, ensure_ascii=False))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
