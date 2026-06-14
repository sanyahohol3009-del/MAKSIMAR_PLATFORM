# Retrieval Vendor Enablement Plan v1

## Scope

This plan starts the post-PHASE 7 Retrieval Vendor Acquisition and Read-Only Tool Enablement track. It keeps `mgrep`, `sqlite-vec`, and `qdrant` as disabled, source-bound, evidence-bound adapter candidates until vendor source, license, scanner, and policy gates are complete.

## Source Resolution

- `sqlite-vec` source is declared as `https://github.com/asg017/sqlite-vec`.
- `qdrant` source is declared as `https://github.com/qdrant/qdrant`.
- `mgrep` source is unresolved and must fail closed until an official source is verified.
- The project-owned manifest is `EXTERNAL_BACKENDS/vendor_quarantine/retrieval_backend_manifest.yaml`.

## Gate Rules

- Vendor gate is required before runtime.
- License review is required before runtime.
- Scanner review is required before runtime.
- Vendor source version/ref must be recorded before runtime.
- External vendor code stays in `EXTERNAL_BACKENDS/vendor_quarantine`.
- Vendor code is not committed as part of this track.
- Runtime remains disabled until an approved later runtime batch changes it.

## Read-Only Tool Enablement

Read-only tool contracts may exist before runtime execution. The approved tool kinds are:

- `mgrep_readonly`
- `sqlite_vec_readonly`
- `qdrant_readonly`

Each tool requires:

- `source_ref`
- `evidence_binding`
- output normalization
- read-only policy gate
- no source-of-truth claim
- no canonical write
- no runtime mutation
- no direct execution
- no network by default

## JARVIS Router Binding Decision

Existing JARVIS read-only routing is in `tools/jarvis_live_runtime/jarvis_live_brain_loop.py`, exposed through `MAKSIMAR_SERVER/AI_ORCHESTRATION/jarvis_live_brain_loop_server_adapter.py` and `CONTROL_PLANE/api_server.py`.

Decision:

- EXTEND the existing read-only router.
- ADAPTER through the existing Control Plane surfaces.
- Do not create a second JARVIS brain, router, runtime, or tool registry.
- Do not enable runtime tool execution in this batch.

## Semantic Routing Coverage

The retrieval tool enablement policy records canonical semantic intent groups for:

- project delta
- file lookup
- project code search
- memory history
- semantic similarity
- backend status
- roadmap readiness
- test validation
- source evidence audit
- architecture docs
- vendor quarantine
- container runtime boundary
- autonomous read-only tool use

Runtime auto-routing is not enabled until a later approved router-binding batch extends the existing JARVIS router and tests the behavior end to end.
