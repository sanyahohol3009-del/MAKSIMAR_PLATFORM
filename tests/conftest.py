# BEGIN MAKSIMAR pytest import path stabilization
from __future__ import annotations

import sys
from pathlib import Path

_TESTS_ROOT = Path(__file__).resolve().parent
_PROJECT_ROOT = _TESTS_ROOT.parent

for _path in (str(_PROJECT_ROOT), str(_TESTS_ROOT)):
    if _path not in sys.path:
        sys.path.insert(0, _path)
# END MAKSIMAR pytest import path stabilization

# BEGIN MAKSIMAR Architecture Radar pytest plugin
_ARCHITECTURE_RADAR_PLUGIN = "MAKSIMAR_CORE_LIB.architecture_map.pytest_architecture_plugin"

_existing_pytest_plugins = globals().get("pytest_plugins", [])

if isinstance(_existing_pytest_plugins, str):
    pytest_plugins = [_existing_pytest_plugins]
else:
    pytest_plugins = list(_existing_pytest_plugins)

if _ARCHITECTURE_RADAR_PLUGIN not in pytest_plugins:
    pytest_plugins.append(_ARCHITECTURE_RADAR_PLUGIN)
# END MAKSIMAR Architecture Radar pytest plugin

# BEGIN MAKSIMAR pytest monitor duplicate session guard
def _is_pytest_monitor_duplicate_session_error(exc: BaseException) -> bool:
    """
    Detects the known benign/idempotent sqlite duplicate TEST_SESSIONS insert.

    This must stay narrow:
    - only UNIQUE constraint failures
    - only TEST_SESSIONS table
    - only SESSION_H / SESSION_HASH key family
    """
    message = " ".join(str(part) for part in getattr(exc, "args", ()))
    normalized = message.upper()

    return (
        "UNIQUE CONSTRAINT FAILED" in normalized
        and "TEST_SESSIONS" in normalized
        and (
            "SESSION_H" in normalized
            or "SESSION_HASH" in normalized
        )
    )
# END MAKSIMAR pytest monitor duplicate session guard

