#!/usr/bin/env bash
set -euo pipefail

BASE="$HOME/MAKSIMAR_PLATFORM/RESEARCH_LAYER/config"
mkdir -p "$BASE"
cd "$BASE"

cat > search_policy.yaml <<'YAML'
schema_version: research_search_policy.v1
description: Canonical search policy for web, local, connector, and hybrid research flows.

search_scopes:
  web_enabled: true
  local_enabled: true
  connectors_enabled: true
  hybrid_enabled: true

defaults:
  default_scope: hybrid
  citation_required_by_default: true
  import_candidate_default: false
  max_results_default: 10

rules:
  - every research search must declare requester and query
  - web search must remain policy-bounded
  - search results do not imply automatic import
YAML

cat > source_ranking.yaml <<'YAML'
schema_version: research_source_ranking.v1
description: Canonical source ranking policy for trust, relevance, and freshness.

weights:
  trust_score: 0.40
  relevance_score: 0.30
  freshness_score: 0.20
  provenance_score: 0.10

filters:
  downrank_unverified_sources: true
  downrank_stale_sources: true
  prefer_authoritative_sources: true

rules:
  - ranking must remain explainable
  - ranking cannot override access or import policy
  - authoritative and recent sources should dominate when relevance is comparable
YAML

cat > import_review.yaml <<'YAML'
schema_version: research_import_review.v1
description: Canonical review policy for importing external research into approved knowledge.

review_requirements:
  external_web_review_required: true
  unverified_source_review_required: true
  reviewer_required: true
  rationale_required_for_approval: true

promotion:
  approved_import_creates_pack: true
  rejected_import_remains_nontrusted: true
  needs_review_blocks_promotion: true

rules:
  - no external source becomes trusted without review
  - import review must preserve source traceability
  - approved imports must remain auditable
YAML

cat > citation_policy.yaml <<'YAML'
schema_version: research_citation_policy.v1
description: Canonical citation requirements for research-backed outputs.

requirements:
  citations_required_by_default: true
  source_traceability_required: true
  quoted_span_tracking_enabled: true
  summary_span_tracking_enabled: true

output_rules:
  every_supported_claim_should_have_source: true
  citation_records_must_map_to_known_source_ids: true
  preserve_context_refs: true

rules:
  - citation fidelity must survive summarization
  - unsupported claims must not be presented as sourced
  - citation records are part of grounding evidence
YAML

cat > online_access_policy.yaml <<'YAML'
schema_version: research_online_access_policy.v1
description: Canonical online access policy for controlled internet research.

access:
  web_access_enabled: true
  connector_access_enabled: true
  unrestricted_background_browsing: false
  policy_gated_sensitive_searches: true

restrictions:
  no_direct_core_write_from_research: true
  no_automatic_library_import: true
  no_unbounded_shell_commands: true
  no_privileged_execution_from_search_results: true

rules:
  - research is controlled input, not authority
  - internet access must remain bounded by policy
  - external findings require review before becoming trusted knowledge
YAML

echo "research configs filled successfully"
