"""Compatibility import and CLI forwarding to the existing Core probe owner."""
from __future__ import annotations

import sys
from MAKSIMAR_CORE_LIB.action_library_adapters import agent_tooling_runtime_probe as _canonical

if __name__ == "__main__":
    raise SystemExit(_canonical.main())
else:
    sys.modules[__name__] = _canonical
