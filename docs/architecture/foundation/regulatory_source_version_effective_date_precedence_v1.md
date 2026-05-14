# Regulatory Memory Foundation — STEP 4 — Source Version / Effective Date / Precedence v1

## Status

Accepted when tests are green.

## Track

roadmap_family: regulatory_memory_foundation  
current_step: STEP 4 — Source Version / Effective Date / Precedence  
next_step: STEP 5 — Regulatory Conflict / Drift / Supersession  

## Purpose

This step requires every regulatory source to be source-bound, versioned, effective-date-bound, tenant-scope-bound and jurisdiction-bound.

It does not resolve legal truth automatically. It prepares precedence visibility and review routing only.

## Reused base

- STEP 1 — Regulatory Track Entry / Surface Inventory
- STEP 2 — Country / Jurisdiction Registry Binding
- STEP 3 — Tenant Regulatory Scope & Isolation
- source version chain models
- memory source priority policy
- legal jurisdiction models
- tenant regulatory scope registry

## Step 4 gates

- source_version_required: enforced
- effective_date_required: enforced
- jurisdiction_id_required: enforced
- tenant_scope_id_required: enforced
- precedence_required: enforced
- no_automatic_legal_truth_resolution: enforced

## Accepted state

- regulatory_source_version_registry_ready: True
- effective_date_precedence_matrix_ready: True
- legal_precedence_resolver_ready: True
- source_version_required: True
- effective_date_required: True
- jurisdiction_id_required: True
- tenant_scope_id_required: True
- precedence_required: True
- approval_required: True
- human_review_required: True
- automatic_resolution_allowed: False
- canonical_truth_update_allowed: False
- runtime_mutation_allowed: False
- direct_core_write_allowed: False
- deployment_allowed_now: False

## Next step

STEP 5 — Regulatory Conflict / Drift / Supersession.
