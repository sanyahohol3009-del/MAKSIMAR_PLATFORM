#!/usr/bin/env bash
set -euo pipefail

BASE="$HOME/MAKSIMAR_PLATFORM/KNOWLEDGE_SYSTEM/config"
mkdir -p "$BASE"
cd "$BASE"

cat > knowledge_ingest.yaml <<'YAML'
schema_version: knowledge_ingest_config.v1
description: Canonical ingest policy for knowledge objects, sources, and packs.

ingest_sources:
  local_doc_enabled: true
  web_enabled: true
  connector_enabled: true
  manual_entry_enabled: true
  benchmark_enabled: true

classification_policy:
  require_source_descriptor: true
  require_object_type: true
  require_provenance_level: true
  auto_reject_untyped_objects: true

review_policy:
  imported_verified_auto_admit: false
  imported_unverified_requires_review: true
  benchmark_sources_require_labeling: true

rules:
  - every ingested knowledge object must carry source_ref
  - provenance must be explicit at ingest time
  - unreviewed external imports must not silently become trusted knowledge
YAML

cat > knowledge_indexing.yaml <<'YAML'
schema_version: knowledge_indexing_config.v1
description: Canonical indexing policy for knowledge stores.

index_types:
  lexical_enabled: true
  vector_enabled: true
  graph_enabled: true
  hybrid_enabled: true

indexing_policy:
  default_index_type: hybrid
  reindex_on_update: true
  preserve_provenance_links: true
  shard_large_packs: true

limits:
  max_objects_per_pack_before_sharding: 1000
  max_index_refresh_batch: 500

rules:
  - index contents must preserve source and provenance traceability
  - indexing must not strip access boundaries
  - hybrid indexing should remain preferred unless explicitly overridden
YAML

cat > retrieval_policy.yaml <<'YAML'
schema_version: knowledge_retrieval_policy.v1
description: Canonical retrieval policy for grounded knowledge access.

retrieval_defaults:
  default_max_results: 10
  citation_required_by_default: true
  grounding_required_by_default: true
  allow_hybrid_retrieval: true

ranking_signals:
  trust_level_weight: 0.35
  relevance_weight: 0.30
  freshness_weight: 0.15
  provenance_weight: 0.20

filters:
  exclude_deprecated_by_default: true
  exclude_unverified_when_verified_exists: true
  restricted_knowledge_requires_policy: true

rules:
  - retrieval must preserve citations and provenance
  - ranking must not override access controls
  - deprecated or weakly trusted knowledge should be downranked or filtered
YAML

cat > provenance_policy.yaml <<'YAML'
schema_version: knowledge_provenance_policy.v1
description: Canonical provenance requirements for all knowledge objects and retrieval outputs.

requirements:
  source_id_required: true
  provenance_record_required_for_imports: true
  transformation_chain_required_for_derived_objects: true
  verification_status_required: true

immutability:
  provenance_append_only: true
  source_traceability_mandatory: true

rules:
  - provenance must survive indexing and retrieval
  - derived knowledge must keep transformation lineage
  - missing provenance blocks promotion to trusted knowledge
YAML

cat > knowledge_pack_policy.yaml <<'YAML'
schema_version: knowledge_pack_policy.v1
description: Canonical policy for curated and versioned knowledge packs.

packaging:
  version_required: true
  included_objects_explicit: true
  target_profiles_explicit: true
  import_review_required_for_external_packs: true

promotion_policy:
  draft_pack_allowed: true
  trusted_pack_requires_review: true
  deprecated_pack_hidden_by_default: true

rules:
  - pack versioning is mandatory
  - packs must not include hidden objects
  - external packs require explicit review before trusted use
YAML

echo "knowledge configs filled successfully"
