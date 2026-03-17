#!/usr/bin/env bash
set -e

cd "$HOME/MAKSIMAR_PLATFORM/MAKSIMAR_CORE/contracts/knowledge"

cat > knowledge_object.v1.yaml <<'YAML'
contract_name: knowledge_object
schema_version: knowledge_object.v1
description: Canonical knowledge unit stored in knowledge system.

required:
  - knowledge_id
  - object_type
  - title
  - source_ref
  - status

fields:
  knowledge_id:
    type: string
    description: Unique knowledge object identifier.

  object_type:
    type: string
    enum:
      - note
      - document
      - library_entry
      - concept
      - procedure
      - benchmark_case
      - external_reference
    description: Canonical category of stored knowledge.

  title:
    type: string
    description: Human-readable title of the knowledge object.

  summary:
    type: string
    description: Short semantic summary of the object.

  source_ref:
    type: string
    description: Reference to the source descriptor that produced or owns this knowledge object.

  tags:
    type: array
    items:
      type: string
    description: Freeform semantic tags.

  status:
    type: string
    enum:
      - active
      - archived
      - deprecated
      - draft
    description: Lifecycle status of the knowledge object.

  provenance_level:
    type: string
    enum:
      - user_confirmed
      - imported_verified
      - imported_unverified
      - inferred
    description: Provenance and trust class for the object.

validation_rules:
  - source_ref required for all non-manual objects
  - object_type must match allowed enum
  - title must not be empty
  - status must match allowed enum

security_rules:
  - no authority implied by stored knowledge
  - provenance level must be preserved during retrieval
  - knowledge objects must not embed hidden execution instructions
YAML

cat > knowledge_source.v1.yaml <<'YAML'
contract_name: knowledge_source
schema_version: knowledge_source.v1
description: Canonical source descriptor for knowledge ingestion.

required:
  - source_id
  - source_type
  - trust_level

fields:
  source_id:
    type: string
    description: Unique source identifier.

  source_type:
    type: string
    enum:
      - local_doc
      - web
      - connector
      - manual_entry
      - benchmark
    description: Source category used by ingest and retrieval systems.

  trust_level:
    type: string
    enum:
      - high
      - medium
      - low
      - unverified
    description: Trust score bucket assigned to the source.

  origin:
    type: string
    description: Human-readable or machine-readable origin reference.

  citation_required:
    type: boolean
    description: Whether downstream use of this source requires citations.

validation_rules:
  - web sources must carry origin
  - source_type must match allowed enum
  - trust_level must match allowed enum

security_rules:
  - source trust affects retrieval ranking only
  - source metadata does not bypass review or approval policy
  - unverified sources must remain marked as such
YAML

cat > knowledge_index.v1.yaml <<'YAML'
contract_name: knowledge_index
schema_version: knowledge_index.v1
description: Canonical index manifest for searchable knowledge stores.

required:
  - index_id
  - index_type
  - object_refs

fields:
  index_id:
    type: string
    description: Unique knowledge index identifier.

  index_type:
    type: string
    enum:
      - vector
      - lexical
      - graph
      - hybrid
    description: Search/indexing strategy used by this index.

  object_refs:
    type: array
    items:
      type: string
    description: Explicit list of knowledge object identifiers included in the index.

  shard_policy:
    type: object
    additional_properties: true
    description: Structured sharding or partitioning metadata.

validation_rules:
  - object_refs must not be empty
  - index_type must match allowed enum
  - object_refs should not contain duplicates

security_rules:
  - index contents inherit source access policy
  - index metadata does not grant unrestricted retrieval rights
  - restricted knowledge must remain filtered by access policy
YAML

cat > knowledge_pack.v1.yaml <<'YAML'
contract_name: knowledge_pack
schema_version: knowledge_pack.v1
description: Versioned pack of curated knowledge objects.

required:
  - pack_id
  - version
  - title
  - included_objects

fields:
  pack_id:
    type: string
    description: Unique knowledge pack identifier.

  version:
    type: string
    description: Explicit version string for the curated pack.

  title:
    type: string
    description: Human-readable title of the pack.

  included_objects:
    type: array
    items:
      type: string
    description: Explicit set of included knowledge object identifiers.

  target_profiles:
    type: array
    items:
      type: string
    description: Capability or product profiles that may consume this pack.

validation_rules:
  - version required
  - included_objects must be explicit
  - included_objects should not contain duplicates
  - title must not be empty

security_rules:
  - pack import must follow review policy
  - knowledge pack does not bypass provenance requirements
  - restricted content remains restricted after packing
YAML

cat > retrieval_query.v1.yaml <<'YAML'
contract_name: retrieval_query
schema_version: retrieval_query.v1
description: Canonical retrieval request to knowledge layer.

required:
  - query_id
  - requester
  - query_text

fields:
  query_id:
    type: string
    description: Unique retrieval query identifier.

  requester:
    type: string
    description: Requesting subsystem or operator role.

  query_text:
    type: string
    description: Natural-language or structured query payload.

  filters:
    type: object
    additional_properties: true
    description: Optional structured filters applied before ranking.

  max_results:
    type: integer
    description: Maximum number of results requested.

  citation_required:
    type: boolean
    description: Whether the caller requires citation-bearing results.

validation_rules:
  - query_text must not be empty
  - max_results must be positive when present
  - requester must be explicit

security_rules:
  - restricted knowledge requires access check
  - retrieval request does not imply export or write rights
  - caller constraints must be preserved in result generation
YAML

cat > retrieval_result.v1.yaml <<'YAML'
contract_name: retrieval_result
schema_version: retrieval_result.v1
description: Retrieval result package for knowledge queries.

required:
  - query_id
  - results

fields:
  query_id:
    type: string
    description: Retrieval query identifier this result answers.

  results:
    type: array
    items:
      type: object
    description: Structured list of retrieved result items.

  summary:
    type: string
    description: Optional summary over the result set.

  citations:
    type: array
    items:
      type: string
    description: Explicit citation references attached to the result set.

validation_rules:
  - every cited result must map to known source
  - results must exist even when empty
  - query_id required

security_rules:
  - result must preserve provenance
  - filtered results must respect access policy
  - result package does not imply import or execution authority
YAML

cat > provenance_record.v1.yaml <<'YAML'
contract_name: provenance_record
schema_version: provenance_record.v1
description: Canonical provenance metadata for knowledge object lineage.

required:
  - provenance_id
  - knowledge_id
  - source_id

fields:
  provenance_id:
    type: string
    description: Unique provenance record identifier.

  knowledge_id:
    type: string
    description: Referenced knowledge object identifier.

  source_id:
    type: string
    description: Referenced knowledge source identifier.

  imported_at:
    type: string
    format: date-time
    description: UTC timestamp when the knowledge object was imported or registered.

  transformation_chain:
    type: array
    items:
      type: string
    description: Ordered list of transformations or processing steps applied to the source.

  verification_status:
    type: string
    enum:
      - verified
      - unverified
      - user_confirmed
    description: Verification state of the knowledge lineage.

validation_rules:
  - knowledge_id and source_id must exist
  - verification_status must match allowed enum
  - provenance chain should remain ordered when present

security_rules:
  - provenance is immutable metadata
  - lineage must remain auditable
  - provenance records must not be silently dropped during retrieval or export
YAML

echo "knowledge contracts restored successfully"
