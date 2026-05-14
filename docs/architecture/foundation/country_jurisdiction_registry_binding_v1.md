# Regulatory Memory Foundation — STEP 2 — Country / Jurisdiction Registry Binding v1

## Status

Accepted when tests are green.

## Track

roadmap_family: regulatory_memory_foundation  
current_step: STEP 2 — Country / Jurisdiction Registry Binding  
next_step: STEP 3 — Tenant Regulatory Scope & Isolation  

## Purpose

This step binds country codes, jurisdiction IDs and applicability scopes for regulatory memory.

The registry is not legal truth. It is a source-bound routing and applicability structure for future regulatory memory records.

## Reused base

- STEP 1 — Regulatory Track Entry / Surface Inventory
- legal jurisdiction models
- regulatory memory models
- tenant memory models
- memory trust scope policy
- source priority policy
- source version chain models

## Step 2 gates

- country_code_required: enforced
- jurisdiction_id_required: enforced
- applicability_scope_required: enforced
- source_bound_required: enforced
- no_cross_jurisdiction_merge: enforced

## Accepted state

- jurisdiction_registry_ready: True
- country_jurisdiction_binding_ready: True
- applicability_matrix_ready: True
- country_code_required: True
- jurisdiction_id_required: True
- applicability_scope_required: True
- source_bound_required: True
- version_required: True
- effective_date_required: True
- cross_jurisdiction_merge_allowed: False
- runtime_mutation_allowed: False
- direct_core_write_allowed: False
- deployment_allowed_now: False

## Next step

STEP 3 — Tenant Regulatory Scope & Isolation.
