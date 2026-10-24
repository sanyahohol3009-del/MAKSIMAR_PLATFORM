"""Compatibility exports for the one canonical live-memory health projection.

No user text, routing, memory writes or independent availability defaults.
"""
from MAKSIMAR_SERVER.AI_ORCHESTRATION.jarvis_live_read_models import (
    build_jarvis_live_memory_federation_status,
)
from MAKSIMAR_SERVER.AI_ORCHESTRATION.session_memory_store import _session_turn_log_path

# Retain the old imported name with the actual canonical store path.
RUNTIME_HISTORY_STORE = _session_turn_log_path()
