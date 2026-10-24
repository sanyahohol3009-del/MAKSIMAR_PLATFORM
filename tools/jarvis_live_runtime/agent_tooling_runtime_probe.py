"""Compatibility import and CLI forwarding to the existing server probe composition owner."""
from __future__ import annotations

import sys
from MAKSIMAR_SERVER.AI_ORCHESTRATION import jarvis_live_read_models as _canonical

if __name__ == "__main__":
    raise SystemExit(_canonical.main())
else:
    sys.modules[__name__] = _canonical
