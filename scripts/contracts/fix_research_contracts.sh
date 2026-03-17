#!/usr/bin/env bash
set -e

cd "$HOME/MAKSIMAR_PLATFORM/MAKSIMAR_CORE/contracts/research"

cat > search_request.v1.yaml <<'YAML'
contract_name: search_request
schema_version: search_request.v1
description: Canonical research search request.

required:
  - request_id
  - requester
  - query
  - search_scope

fields:
  request_id:
    type: string
    description: Unique research search request identifier.

  requester:
    type: string
    description: Requesting subsystem or operator role.

  query:
    type: string
    description: Search query text or structured query payload.

  search_scope:
    type: string
    enum:
      - web
      - local
      - connectors
      - hybrid
    description: Scope of the search operation.

  citation_required:
    type: boolean
    description: Whether the caller requires citation-capable results.

  import_candidate:
    type: boolean
    description: Whether results may be considered for knowledge import review.

validation_rules:
  - query required
  - requester required
  - search_scope must match allowed enum
  - citation_required should be explicit for research-critical paths

security_rules:
  - external web use follows online access policy
  - search request does not imply automatic import authority
  - search scope must remain within policy-allowed boundaries
YAML

cat > search_result.v1.yaml <<'YAML'
contract_name: search_result
schema_version: search_result.v1
description: Canonical result set for research search.

required:
  - request_id
  - entries

fields:
  request_id:
    type: string
    description: Identifier of the originating search request.

  entries:
    type: array
    items:
      type: object
    description: Ranked or unranked result entries returned by the search layer.

  ranked_by:
    type: string
    description: Ranking policy or engine used to order results.

  selected_entries:
    type: array
    items:
      type: string
    description: Explicit subset of entries selected for follow-up inspection or review.

validation_rules:
  - entries may be empty but must exist
  - request_id required
  - selected_entries must reference known result entries when present

security_rules:
  - no import happens automatically from search_result
  - result visibility follows source access policy
  - result ranking must not suppress provenance metadata
YAML

cat > import_review.v1.yaml <<'YAML'
contract_name: import_review
schema_version: import_review.v1
description: Review record for importing external knowledge into approved library.

required:
  - review_id
  - source_id
  - decision

fields:
  review_id:
    type: string
    description: Unique import review identifier.

  source_id:
    type: string
    description: Source under review for import.

  decision:
    type: string
    enum:
      - approved
      - rejected
      - needs_review
    description: Final or intermediate review decision.

  rationale:
    type: string
    description: Human-readable review rationale.

  reviewer:
    type: string
    description: Reviewer identity or subsystem role.

  imported_pack_ref:
    type: string
    description: Reference to resulting knowledge pack when import is approved.

validation_rules:
  - approved imports should reference imported_pack_ref
  - decision must match allowed enum
  - source_id required

security_rules:
  - approval required for library import
  - rejected imports must remain non-imported
  - review records are auditable governance artifacts
YAML

cat > citation_record.v1.yaml <<'YAML'
contract_name: citation_record
schema_version: citation_record.v1
description: Canonical citation mapping for research-backed answers.

required:
  - citation_id
  - source_id
  - context_ref

fields:
  citation_id:
    type: string
    description: Unique citation identifier.

  source_id:
    type: string
    description: Source referenced by this citation.

  context_ref:
    type: string
    description: Context, answer, or retrieval item this citation supports.

  quoted_span_ref:
    type: string
    description: Optional reference to quoted or excerpted source span.

  summary_span:
    type: string
    description: Optional summarized supporting passage or rationale span.

validation_rules:
  - source_id required
  - context_ref required
  - citation_id must be unique

security_rules:
  - preserve source traceability
  - citation metadata must not be stripped from grounded answers
  - citations do not imply source approval for import
YAML

cat > source_rank.v1.yaml <<'YAML'
contract_name: source_rank
schema_version: source_rank.v1
description: Ranked trust and relevance score for sources.

required:
  - rank_id
  - source_id
  - trust_score
  - relevance_score

fields:
  rank_id:
    type: string
    description: Unique source ranking record identifier.

  source_id:
    type: string
    description: Source being ranked.

  trust_score:
    type: number
    description: Normalized trust score for the source.

  relevance_score:
    type: number
    description: Normalized relevance score for the current request or domain.

  freshness_score:
    type: number
    description: Optional freshness score based on recency and temporal utility.

  overall_score:
    type: number
    description: Combined ranking score used for ordering or filtering.

validation_rules:
  - scores should be normalized within policy
  - source_id required
  - trust_score and relevance_score required

security_rules:
  - ranking does not bypass import review
  - low-ranked sources may still require explicit review rather than silent discard
  - ranking must not conceal trust classification
YAML

echo "research contracts restored successfully"
