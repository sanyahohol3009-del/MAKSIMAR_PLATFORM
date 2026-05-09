# PHASE 2.3 Batch 2 — Promotion Binding / Candidate / Summary Acceptance v1

## Статус

PHASE 2.3 Batch 2 принят.

Слой расширен через existing server promotion root:

- MAKSIMAR_SERVER/MEMORY_PROMOTION_PIPELINE/

Новый promotion root не создавался.

## Добавлено

- promotion_binding_models.py
- promotion_candidate_builder.py
- promotion_summary_builder.py

Изменено:

- __init__.py

Новые тесты:

- test_promotion_binding_models_smoke.py
- test_promotion_candidate_builder_smoke.py
- test_promotion_summary_builder_smoke.py
- test_promotion_governance_binding_ready_smoke.py
- test_promotion_archived_dedup_candidate_smoke.py
- test_promotion_archived_conflict_candidate_smoke.py
- test_promotion_binding_id_uniqueness_smoke.py

## Принятые результаты

Promotion Binding:

- total_bindings: 2
- ready_bindings: 2
- evidence_bound_bindings: 2
- governance_bound_bindings: 2
- approval_required_bindings: 2
- auto_promotion_allowed_bindings: 0
- controlled_promotion_bindings: 2
- read_only_bindings: 2
- promoted_entries: 1
- archived_entries: 1

Promotion Summary:

- pipeline_total_entries: 2
- pipeline_promoted_entries: 1
- pipeline_archived_entries: 1
- pipeline_evidence_bound_entries: 2
- promotion_binding_entries: 2
- promotion_ready_bindings: 2
- summary_ready: True

## Важная семантика

Promoted entry:

- deduplication_passed must be True
- conflict_check_passed must be True

Archived entry:

- deduplication_passed may be False
- conflict_check_passed may be False
- binding can still be ready_for_review

All promotion bindings:

- approval_required=True
- auto_promotion_allowed=False
- controlled_promotion_allowed=True
- read_only=True
- governance_bound=True
- evidence_bound=True

## ID rule

promotion_binding_id must include:

- module_slug
- input_event_id
- disposition: promoted / archived / candidate

This prevents duplicate promotion binding ids when several pipeline entries belong to the same module.

## Жёсткие правила

Batch 2 is read-only.

Batch 2 does not mutate memory.

Batch 2 does not execute promotion.

Batch 2 does not auto-promote.

Batch 2 does not resolve conflicts.

Batch 2 only builds review-ready promotion bindings.

Approval remains required.

## Проверки

- local tests: 11 passed
- related pack: 95 passed
- full auto parallel: 1895 passed
