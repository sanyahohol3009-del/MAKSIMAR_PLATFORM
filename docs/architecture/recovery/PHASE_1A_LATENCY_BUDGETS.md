# Phase 1A Latency Budgets

Budgets share one monotonic `RequestDeadline`. Provisional component ceilings are understanding 90s, each project operation 8s and Final Brain 180s within a 240s total deadline. These are compatibility ceilings, not accepted measured defaults. The model harness and HTTP probes must supply p50/p95 before the exit gate can pass; final values must be configurable and derived from those samples.
