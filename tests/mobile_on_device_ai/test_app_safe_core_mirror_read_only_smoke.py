from __future__ import annotations

from MAKSIMAR_CORE_LIB.app_safe_core.app_safe_core_export_manifest import (
    build_app_safe_core_export_manifest,
)
from MAKSIMAR_CORE_LIB.mobile_bridge.mobile_core_mirror_contract import (
    build_mobile_core_mirror_contract,
)


def test_app_safe_core_mirror_is_read_only_cache_only() -> None:
    manifest = build_app_safe_core_export_manifest().to_read_model()
    mirror = build_mobile_core_mirror_contract().to_read_model()

    assert manifest["export_is_read_only"] is True
    assert manifest["export_is_intent_only"] is True
    assert manifest["mobile_cache_allowed"] is True
    assert manifest["mobile_cache_canonical"] is False
    assert mirror["mirror_can_write_core"] is False
    assert mirror["mirror_can_write_memory"] is False
    assert mirror["mirror_can_mutate_runtime"] is False
