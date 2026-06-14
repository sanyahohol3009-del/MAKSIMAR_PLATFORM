# PHASE 7 Retrieval Backend Acceptance v1

## Scope

PHASE 7 closes the retrieval backend adapter foundation as contract, read-model, preview, and container-readiness surfaces only. It does not introduce a second retrieval engine, backend runtime execution, backend downloads, backend installation, Docker startup, qdrant server startup, n8n startup, or JARVIS tool registration.

Retrieval backend adapters remain evidence-bound, source-bound, read-only, and not source of truth. Adapter output requires normalization before any downstream use.

## PHASE 7.1 Retrieval Core Contracts

Accepted source surfaces:

- `MAKSIMAR_CORE_LIB/retrieval_backend/retrieval_backend_adapter_contract.py`
- `MAKSIMAR_CORE_LIB/retrieval_backend/vector_backend_contract.py`
- `MAKSIMAR_CORE_LIB/retrieval_backend/semantic_search_contract.py`
- `MAKSIMAR_CORE_LIB/retrieval_backend/evidence_binding_contract.py`

Acceptance state:

- Retrieval adapter results require `source_ref`.
- Retrieval adapter results require `evidence_binding`.
- Retrieval evidence is source-bound and citation-bound.
- Retrieval backend contracts are adapter-only.
- Retrieval backends are not canonical source of truth.
- Direct canonical write is disallowed.
- Runtime mutation is disallowed.

## PHASE 7.2 Retrieval Adapter Contracts

Accepted source surfaces:

- `MAKSIMAR_CORE_LIB/retrieval_backend/retrieval_policy_gate_contract.py`
- `MAKSIMAR_CORE_LIB/retrieval_backend/mgrep_adapter_contract.py`
- `MAKSIMAR_CORE_LIB/retrieval_backend/sqlite_vec_adapter_contract.py`
- `MAKSIMAR_CORE_LIB/retrieval_backend/qdrant_adapter_contract.py`

Acceptance state:

- `mgrep`, `sqlite_vec`, and `qdrant` are contract-only adapter candidates.
- Runtime execution is disallowed.
- Downloads and installs are outside PHASE 7.
- Network access is disabled by default.
- Direct canonical write is disallowed.
- Runtime mutation is disallowed.
- Source-of-truth claims are disallowed.
- Output normalization is mandatory.
- Every output requires `source_ref` and `evidence_binding`.

## PHASE 7.3 Retrieval Read Model / Container

Accepted source and config surfaces:

- `MAKSIMAR_CORE_LIB/retrieval_backend/retrieval_backend_status_read_model.py`
- `tools/retrieval_backend_status_preview.py`
- `CONTAINER_DEPLOYMENT/cubes/retrieval_backend/container_contract.yaml`
- `CONTAINER_DEPLOYMENT/cubes/retrieval_backend/runtime_profile.yaml`

Acceptance state:

- Status read model reports `mgrep`, `sqlite_vec`, and `qdrant`.
- Status read model is deterministic.
- Preview is read-only and prints deterministic JSON.
- `container_ready=true`.
- `runtime_enabled=false`.
- `docker_required_now=false`.
- `qdrant_container_enabled=false`.
- Read-only preview is allowed.
- Vendor gate is required before any real backend.
- Qdrant remains a network service adapter candidate only.
- Qdrant runtime, container, and server are disabled now.

## Post-PHASE 7 Next Track

The next track is Retrieval Vendor Acquisition / Tool Enablement.

Rules for the next track:

- `mgrep`, `sqlite_vec`, and `qdrant` may be acquired only through vendor quarantine, scanner review, and vendor gate approval.
- After vendor gate approval, read-only retrieval tools may be created.
- JARVIS autonomous tool router may call retrieval tools only through policy, evidence binding, and source binding.
- Direct tool execution routes around policy, evidence binding, or source binding are disallowed.
- Network, service, and container boundaries remain explicit and disabled by default until an approved enablement track changes them.

## Final Acceptance

PHASE 7 is accepted as a read-only retrieval backend adapter foundation. It provides contracts, adapter status read models, preview output, and container readiness declarations without executing retrieval backends or making retrieval data canonical truth.
