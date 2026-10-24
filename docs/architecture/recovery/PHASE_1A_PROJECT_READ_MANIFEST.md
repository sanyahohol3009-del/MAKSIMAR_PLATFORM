# Phase 1A Project Read Manifest

The versioned manifest is `docs/architecture/open_source_integration/capability_manifests/project.read.v1.json`. The existing canonical loader validates manifests generically, rejects duplicate IDs/schema drift and discovers the existing project adapter without a `project.read` special case. It declares read-only filesystem, denied network, operations, schemas, exclusions, health, timeout and graceful degradation.
