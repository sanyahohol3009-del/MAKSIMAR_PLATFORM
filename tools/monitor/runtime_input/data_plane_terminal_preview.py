from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[3]
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from MAKSIMAR_CORE_LIB.data_plane.data_plane_read_model import (  # noqa: E402
    DataPlaneAppendLogReadModel,
    DataPlaneHealthReadModel,
    DataPlaneLedgerReadModel,
)
from MAKSIMAR_SERVER.DATA_PLANE.data_plane_read_model_builder import (  # noqa: E402
    build_data_plane_runtime_read_model,
)
from MAKSIMAR_SERVER.DATA_PLANE.data_plane_telemetry_read_model_builder import (  # noqa: E402
    build_data_plane_telemetry_read_model,
)

ONE_HASH = "1" * 64
TWO_HASH = "2" * 64


def build_preview_runtime_read_model():
    append_log = DataPlaneAppendLogReadModel(
        append_log_id="preview_append_log",
        stream_id="preview_stream",
        log_path="RUNTIME/state/data_plane_append_log.jsonl",
        record_count=1,
        head_hash=ONE_HASH,
        latest_record_id="preview_stream:00000000000000000000",
        write_performed=False,
        append_only_enforced=True,
        reason_codes=("preview_append_log_read_model",),
    )
    ledger = DataPlaneLedgerReadModel(
        ledger_adapter_id="preview_ledger_adapter",
        ledger_id="preview_ledger",
        ledger_path="RUNTIME/state/data_plane_ledger.jsonl",
        entry_count=1,
        head_hash=TWO_HASH,
        latest_entry_id="preview_ledger:00000000000000000000",
        write_performed=False,
        immutable_ledger_enforced=True,
        reason_codes=("preview_ledger_read_model",),
    )
    health = DataPlaneHealthReadModel(
        layer_id="DATA_PLANE",
        status="ready",
        checked_paths=("DATA_PLANE", "MAKSIMAR_CORE_LIB/data_plane", "MAKSIMAR_SERVER/DATA_PLANE"),
        missing_paths=(),
        health_ok=True,
        reason_codes=("preview_health_read_model",),
    )
    telemetry = build_data_plane_telemetry_read_model(
        append_log=append_log,
        ledger=ledger,
        health=health,
    )
    return build_data_plane_runtime_read_model(telemetry)


def main() -> int:
    parser = argparse.ArgumentParser(description="Render DATA_PLANE terminal preview.")
    parser.add_argument("--json", action="store_true", help="Render JSON output.")
    args = parser.parse_args()

    runtime_read_model = build_preview_runtime_read_model()

    if args.json:
        print(json.dumps(runtime_read_model.to_dict(), indent=2, sort_keys=True))
        return 0

    print("DATA_PLANE RUNTIME READ MODEL")
    print("=" * 32)
    print(f"runtime_read_model_id: {runtime_read_model.runtime_read_model_id}")
    print(f"layer_id: {runtime_read_model.layer_id}")
    print(f"append_log_records: {runtime_read_model.telemetry.append_log.record_count}")
    print(f"ledger_entries: {runtime_read_model.telemetry.ledger.entry_count}")
    print(f"health_status: {runtime_read_model.telemetry.health.status}")
    print(f"dashboard_safe: {runtime_read_model.dashboard_safe}")
    print(f"preview_safe: {runtime_read_model.preview_safe}")
    print(f"execution_allowed_from_preview: {runtime_read_model.execution_allowed_from_preview}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
