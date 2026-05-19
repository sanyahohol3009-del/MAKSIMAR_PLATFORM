# DATA_PLANE Append-Only Log Policy v1

## Policy

Append-only log records are immutable after creation.

Allowed action:

- append a new validated record.

Forbidden actions:

- overwrite an existing record;
- delete a record;
- truncate the log;
- write directly into canonical truth;
- place heavy payloads in the control path.

## Ledger anchoring

Every accepted runtime operation must be able to produce a ledger anchor.

The ledger anchor references the append-log record and preserves hash continuity.

## Dashboard exposure

Dashboard views may show read models and telemetry only.

Dashboard views must not trigger append or ledger writes.
