from __future__ import annotations

from pathlib import Path

from MAKSIMAR_SERVER.DATA_PLANE.data_plane_append_log_adapter import (
    DataPlaneAppendLogAdapterResult,
)
from MAKSIMAR_SERVER.DATA_PLANE.data_plane_ledger_adapter import (
    DataPlaneLedgerAdapterResult,
    anchor_append_log_result_to_ledger,
)


def build_immutable_ledger_anchor(
    *,
    ledger_path: Path,
    ledger_id: str,
    append_result: DataPlaneAppendLogAdapterResult,
    created_at_utc: str,
) -> DataPlaneLedgerAdapterResult:
    return anchor_append_log_result_to_ledger(
        ledger_path=ledger_path,
        ledger_id=ledger_id,
        append_result=append_result,
        created_at_utc=created_at_utc,
    )
