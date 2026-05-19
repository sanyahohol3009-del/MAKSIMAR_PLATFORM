# DATA_PLANE Container Boundary v1

## Rule

DATA_PLANE is a separate data/runtime surface.

It may hold:

- append-only log artifacts;
- immutable ledger artifacts;
- storage references;
- object storage references;
- vector store references;
- memory index references;
- dashboard-safe telemetry.

## Forbidden

DATA_PLANE must not:

- write directly to canonical truth;
- mutate CONTROL_PLANE;
- execute dashboard requests;
- inline heavy payloads through the control path;
- bypass policy and approval gates.

## Runtime adapter boundary

Runtime adapters may write to append-only runtime files only when called by accepted server-side functions.

Preview tools remain read-only and must not execute writes.
