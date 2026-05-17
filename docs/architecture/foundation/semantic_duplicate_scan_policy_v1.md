# Semantic Duplicate Scan Policy v1

## Status

Canonical semantic duplicate policy for PHASE 0 / BATCH 0.4.

## Purpose

Semantic duplicate scan prevents accidental creation of files, contracts, services, or tools that duplicate existing project meaning.

The scan checks more than exact file names. It checks semantic families and architectural role.

## Required before every batch

Before implementing any batch, run:

1. roadmap reconciliation
2. exact target path scan
3. semantic duplicate scan
4. location validation table
5. create/reuse/adapter decision

## Semantic families

The scan must consider the following families:

- root artifact hygiene
- security
- RBAC
- policy
- approval
- signature
- vault
- quarantine
- data
- storage
- ledger
- append-only log
- journal
- artifact routing
- vector store
- postgres
- update
- recovery
- rollback
- snapshot
- sync
- network
- trust boundary
- VPN
- docker
- container
- AI
- model router
- workers
- orchestration
- agents
- proposal
- tool call boundary
- registry
- enrollment
- domain
- memory registry
- dashboard visibility
- observability
- governance
- execution
- memory
- product
- testing and tooling

## Decision actions

| Action | Meaning |
|---|---|
| `create_new` | No existing semantic match was found. |
| `reuse_in_place` | Existing file already represents the target role. |
| `wrap_as_adapter` | Existing legacy/runtime code should be wrapped through adapter/facade. |
| `keep_legacy` | Existing code remains untouched and is not replaced. |
| `migration_candidate` | Possible future migration, requiring approval. |
| `true_duplicate_risk` | Dangerous duplicate risk; stop and review. |
| `container_boundary_duplicate_allowed` | Intentional boundary duplicate for containerization/facade. |

## High-risk duplicate examples

| Target | Existing | Risk |
|---|---|---|
| `signature_verifier_contract.py` | another `signature_verifier_contract.py` in another layer | high |
| `policy_enforcer_contract.py` | existing policy engine with same responsibility | medium/high |
| `model_router_contract.py` | existing model router runtime contract | medium/high |
| `append_only_log_contract.py` | existing event journal with same responsibility | medium |
| `recovery_service_contract.py` | existing recovery manager with same responsibility | medium |

## Allowed boundary duplicate examples

| New boundary | Existing code | Action |
|---|---|---|
| `SECURITY_LAYER/boundaries/container_adapter_boundary.yaml` | `security_gate_adapter.py` | `container_boundary_duplicate_allowed` |
| `DATA_PLANE/adapters/event_journal_adapter.py` | `EVENT_BUS/event_journal.jsonl` | `wrap_as_adapter` |
| `UPDATE_RECOVERY/adapters/secure_sync_update_transport_adapter.py` | `secure_sync_update_transport` | `wrap_as_adapter` |
| `AI_ORCHESTRATION/adapters/control_plane_ai_router_adapter.py` | `CONTROL_PLANE/ai_router_binding` | `wrap_as_adapter` |

## Forbidden behavior

Semantic duplicate scan must not:

1. delete files
2. move files
3. rewrite files
4. auto-resolve duplicate risks
5. silently permit duplicate business logic
6. downgrade true duplicate risk to warning
7. mark runtime coupling as safe without adapter/facade boundary

## Dashboard output

Dashboard-safe semantic duplicate output may include:

- target path
- existing path
- target family
- existing family
- duplicate relation
- action
- risk level
- approval required
- reason codes
- next action

Dashboard must not include mutation actions.

## Source of truth

The source of truth for semantic duplicate machine logic is:

- `MAKSIMAR_CORE_LIB/root_artifact_hygiene/semantic_duplicate_scan_models.py`
- `MAKSIMAR_CORE_LIB/root_artifact_hygiene/semantic_duplicate_scan_policy.py`
- `MAKSIMAR_CORE_LIB/root_artifact_hygiene/semantic_duplicate_report_builder.py`

This document describes the policy. The Python contracts enforce the machine-readable form.
