# DATA_PLANE BATCH 2.4 Roadmap Reconciliation v1

## Status

Required correction before PHASE 2 / BATCH 2.4 implementation.

## Reason

BATCHED FOUNDATION ROADMAP v1 uses Runtime Logger + Read Model + Preview names:

- append_only_log_writer.py
- immutable_ledger_builder.py
- data_plane_logger.py
- data_plane_read_model_builder.py
- data_plane_append_log_terminal_preview.py
- data_plane_append_log_web_preview.py
- event_journal_adapter.py
- existing_storage_registry_adapter.py
- DataPlaneRuntimeReadModel

BATCHED FOUNDATION ROADMAP v2.1 uses dashboard-ready implementation names:

- data_plane_append_log_adapter.py
- data_plane_ledger_adapter.py
- data_plane_telemetry_read_model_builder.py
- data_plane_terminal_preview.py
- data_plane_web_preview.py
- data_plane_existing_storage_adapter.py
- DataPlaneTelemetryReadModel

## Decision

v2.1 does not replace v1 by deletion.

Implementation rule:

- v2.1 files remain canonical implementation surfaces.
- v1 filenames are preserved as compatibility/facade surfaces.
- No move.
- No delete.
- No migration.
- No duplicate business logic.
- Facades must delegate to canonical implementation contracts/adapters.
- Runtime writes only to DATA_PLANE runtime append/ledger artifacts.
- Canonical truth remains untouched.
- Preview/read models remain dashboard-safe and read-only.
- UI-to-execution remains forbidden.

## Required BATCH 2.4 compatibility files

- MAKSIMAR_SERVER/DATA_PLANE/append_only_log_writer.py
- MAKSIMAR_SERVER/DATA_PLANE/immutable_ledger_builder.py
- MAKSIMAR_SERVER/DATA_PLANE/data_plane_logger.py
- MAKSIMAR_SERVER/DATA_PLANE/data_plane_read_model_builder.py
- tools/monitor/runtime_input/data_plane_append_log_terminal_preview.py
- tools/monitor/runtime_input/data_plane_append_log_web_preview.py
- MAKSIMAR_SERVER/DATA_PLANE/adapters/event_journal_adapter.py
- MAKSIMAR_SERVER/DATA_PLANE/adapters/existing_storage_registry_adapter.py

## Required BATCH 2.4 compatibility tests

- tests/data_plane/test_data_plane_logger_smoke.py
- tests/data_plane/test_event_journal_adapter_smoke.py
- tests/data_plane/test_existing_storage_registry_adapter_smoke.py
