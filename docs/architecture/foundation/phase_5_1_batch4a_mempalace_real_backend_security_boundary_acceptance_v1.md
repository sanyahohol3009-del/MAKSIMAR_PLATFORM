# PHASE 5.1 Batch 4A — MemPalace Real Backend Security Boundary Acceptance v1

## Статус

PHASE 5.1 Batch 4A принят.

## Purpose

Batch 4A creates the network, filesystem, process, and secrets boundary required before any real MemPalace backend enablement.

## Accepted state

Filesystem boundary:

- allowed_read_roots:
  - EXTERNAL_BACKENDS/mempalace/source
  - EXTERNAL_BACKENDS/mempalace/manifests
  - EXTERNAL_BACKENDS/mempalace/smoke_reports
  - EXTERNAL_BACKENDS/mempalace/security_reports
- allowed_write_roots:
  - EXTERNAL_BACKENDS/mempalace/sandbox_data
- denied_roots:
  - CORE_ROOT
  - RUNTIME
  - SUPERVISOR
  - MAKSIMAR_CORE_LIB
  - MAKSIMAR_SERVER/EXECUTION_CONTROL
  - MAKSIMAR_SERVER/RUNTIME
  - MAKSIMAR_SERVER/MEMORY_SYNC
  - MAKSIMAR_SERVER/CONTROL_PLANE
  - .env
  - .pymon
- sandbox_data_only: True
- canonical_memory_access: False
- canonical_artifact_access: False
- runtime_state_access: False
- destructive_operations_allowed: False
- filesystem_boundary_ready: True

Network boundary:

- network_default_policy: disabled_until_explicit_review
- outbound_network_allowed: False
- external_download_allowed: False
- remote_model_api_allowed: False
- local_loopback_allowed: False
- network_review_required: True
- network_boundary_ready: True

Process / secrets boundary:

- separate_venv_required: True
- isolated_workdir_required: True
- env_scrub_required: True
- project_env_inheritance_allowed: False
- secrets_access_allowed: False
- shell_execution_allowed: False
- subprocess_execution_allowed: False
- process_boundary_ready: True

Real backend state:

- manual_security_review_required: True
- manual_security_review_completed: False
- real_backend_candidate_detected: True
- real_backend_enablement_allowed: False
- real_backend_query_allowed: False
- canonical_write_allowed: False
- runtime_mutation_allowed: False
- security_boundary_ready: True

## Жёсткие правила

Batch 4A does not enable real backend.

Batch 4A does not allow real backend queries.

Batch 4A does not allow outbound network.

Batch 4A does not allow external downloads.

Batch 4A does not allow remote model API calls.

Batch 4A does not allow secrets access.

Batch 4A does not allow shell execution.

Batch 4A does not allow subprocess execution.

Batch 4A does not allow destructive filesystem operations.

Batch 4A does not allow canonical memory access.

Batch 4A does not allow runtime mutation.

Manual security review remains required before any real backend enablement.

## Проверки

- modularity / direct coupling check: passed
- local tests: 4 passed
- related pack: 168 passed
- full auto parallel with monitor active: 2044 passed
