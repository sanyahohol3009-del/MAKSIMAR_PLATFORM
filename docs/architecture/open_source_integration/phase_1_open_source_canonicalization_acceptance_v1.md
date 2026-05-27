# PHASE 1 — Open Source Canonicalization Acceptance v1

Status: accepted by test gate.

## Scope

PHASE 1 establishes the canonical open-source integration boundary for MAKSIMAR/JARVIS.

The phase prevents external repositories, documents, manifests, YAML files, adapter candidates or read-only registry records from being treated as implemented runtime.

## Accepted batches

- PHASE 1.1 — Open Source Exclusion Registry
- PHASE 1.2 — Canonical Capability Registry Models
- PHASE 1.3 — Capability Registry Loader / Summary
- PHASE 1.4 — Truth Status Marking
- PHASE 1.5 — PHASE 1 Acceptance

## Accepted guarantees

1. External open-source projects are not imported directly into immutable core.
2. External backends remain adapter-only, quarantine-only or approval-gated.
3. Registry records are read-only source surfaces.
4. Spec-only documents do not count as implemented runtime.
5. Manifest-only entries do not count as implemented runtime.
6. YAML and JSON configuration files do not count as implemented runtime.
7. Adapter candidates do not count as implemented runtime.
8. Runtime is considered real only when truth status is IMPLEMENTED, evidence level is runtime_verified, source paths exist, runtime evidence paths exist, runtime test paths exist, runtime_implemented is true, and runtime_execution_verified is true.
9. Dashboard/read-model surfaces remain read-only.
10. No direct core import is allowed.
11. No source-of-truth override is allowed.
12. No runtime mutation is allowed.
13. No ports are opened by this phase.
14. No containers are started by this phase.
15. No active deployment is created by this phase.
16. Every accepted capability status must be containerization-ready as a reference contract.
17. Containerization readiness is required for every future batch, not only container/network batches.

## Containerization readiness rule

Every batch must expose container-readiness semantics through contracts, summaries, read-models or acceptance tests.

Required safety semantics:

- disable_safe=true
- dashboard_read_only=true where applicable
- direct_core_import_allowed=false
- source_of_truth_override_allowed=false
- runtime_mutation_allowed=false
- ports_opened=false unless a deployment-gated batch explicitly allows otherwise
- containers_started=false unless a deployment-gated batch explicitly allows otherwise
- active_deployment_created=false unless a deployment-gated batch explicitly allows otherwise
- external backends must remain adapter/quarantine/approval-gated
- every cube, capability or adapter must be disable-safe without breaking core, readiness, dashboard or source-of-truth layers

## Runtime truth rule

Runtime is not inferred from documentation or registry metadata.

The following are not runtime evidence:

- Markdown documents
- YAML manifests
- JSON registry files
- read-only summaries
- adapter candidates
- exclusion registry records
- capability registry records

Implemented runtime requires:

- truth_status=IMPLEMENTED
- evidence_level=runtime_verified
- runtime_implemented=true
- runtime_execution_verified=true
- non-empty source_paths
- non-empty runtime_evidence_paths
- non-empty runtime_test_paths

## Acceptance decision

PHASE 1 is accepted when the test gate confirms:

- open-source exclusion registry is present
- canonical capability registry is present
- capability loader and summary are read-only
- truth status registry rejects fake runtime claims
- manifest-only and spec-only entries remain non-runtime
- all truth status entries are containerization-ready
- all phase readiness files are present
- project readiness map marks PHASE 1 batches as ready
