# Open Source Exclusion Registry v1

Status: PHASE 1 / Batch 1.1.

This registry defines which open-source capability families must not be imported into MAKSIMAR Core.

Main rule:
Open-source projects are never loaded into immutable core directly.

Allowed path:
quarantine -> vendor/security scan -> policy review -> adapter boundary -> read-model/runtime gate

Excluded from core:
- generic workflow brain
- generic approval/action model
- retrieval source of truth
- proposal/codegen governance spine
- media artifact memory

Existing MAKSIMAR coverage:
- workflow registry and control-plane routing
- proposal/audit/approval governance
- codegen context and sandbox review
- memory registry and retrieval routing
- storage registry and media artifact references
- security/vendor gate and quarantine policy
- container boundary and external backend profile

Containerization rule:
Each future cube, capability or adapter must be independently disableable.

A disabled cube must not break:
- immutable core
- canonical contracts
- project readiness map
- dashboard read-only surfaces
- security/vendor gates
- memory/source-of-truth boundaries

Prohibited paths:
Open-source projects must not:
- become source of truth
- write into immutable core
- bypass security gate
- bypass repository quarantine policy
- bypass approval gate
- mutate runtime directly
- create a second dashboard root
- create a second roadmap/readiness engine

Machine-readable registry:
docs/architecture/open_source_integration/open_source_exclusion_registry_v1.json
