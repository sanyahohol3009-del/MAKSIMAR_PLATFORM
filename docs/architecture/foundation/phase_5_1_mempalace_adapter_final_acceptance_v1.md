# PHASE 5.1 — MemPalace Adapter Final Acceptance v1

## Статус

PHASE 5.1 принят.

## Итог

MemPalace integrated as subordinate read-only memory routing backend.

## Accepted state

- vendor source acquired in EXTERNAL_BACKENDS/mempalace/source
- vendor venv isolated in EXTERNAL_BACKENDS/mempalace/venv
- source / venv / sandbox_data not committed
- EXTERNAL_BACKENDS excluded from general pytest collection
- vendor security gate passed
- risky findings classified
- controlled real backend import probe passed
- probe result bound to adapter evidence
- read-only routing integration ready

## Allowed

- subordinate backend
- read-only routing
- query domains:
  - conversational_memory
  - project_notes
  - owner_context
  - tenant_conversational_context
- evidence pack
- preview trace
- source attribution
- policy checked query contracts

## Blocked

- full real backend enablement
- general real backend query
- write routing
- canonical write
- runtime mutation
- auto-promotion
- auto-conflict-resolution
- network access
- subprocess / shell access
- destructive filesystem operations
- secrets access

## Required future condition for stronger enablement

Any future move beyond read-only subordinate routing requires a new approval phase and fresh security review.

## Final checks

- final acceptance tests
- related pack
- full auto parallel with monitor active
