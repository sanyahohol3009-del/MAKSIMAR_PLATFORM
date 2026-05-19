# DATA_PLANE FOUNDATION v1

DATA_PLANE is the platform layer for append-only operational records, immutable ledger contracts, storage references, object storage references, vector store references, memory index references and payload/data routing boundaries.

## Current batch

PHASE 2 / BATCH 2.1 — Data Plane Surface + Existing Source Binding.

## Existing source rule

Existing `MAKSIMAR_CORE_LIB/data_plane/*` contracts are preserved as working source surfaces.

This batch does not move, delete, replace or migrate existing data-plane artifact contracts.

## Data-plane laws

- Heavy payloads stay in DATA_PLANE.
- Control-path contracts carry references, not heavy payload bodies.
- Append-only records must not support overwrite/delete semantics.
- Ledger records must be immutable by contract.
- Dashboard output is read-only.
- Dashboard does not mutate DATA_PLANE.
- UI does not execute DATA_PLANE actions directly.
- No direct canonical write.
- Container boundary is adapter/facade first.
- Existing storage/artifact/memory surfaces are reference-only until explicit correction pass.

## Dashboard readiness

BATCH 2.1 exposes layer/surface metadata only.

Runtime telemetry, append-log read models and ledger read models are introduced through explicit DATA_PLANE roadmap batches.
