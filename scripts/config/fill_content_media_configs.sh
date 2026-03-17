#!/usr/bin/env bash
set -euo pipefail

BASE="$HOME/MAKSIMAR_PLATFORM/CONTENT_MEDIA_LAYER/config"
mkdir -p "$BASE"
cd "$BASE"

cat > template_policy.yaml <<'YAML'
schema_version: content_media_template_policy.v1
description: Canonical policy for media templates and reusable content generation assets.

templates:
  visual_templates_enabled: true
  subtitle_templates_enabled: true
  beat_templates_enabled: true
  reusable_asset_groups_enabled: true

validation:
  template_id_required: true
  template_type_required: true
  asset_reference_tracking_required: true

rules:
  - templates are reusable assets, not publishing authority
  - template provenance must remain visible
  - hidden template-side execution authority is forbidden
YAML

cat > media_pipeline.yaml <<'YAML'
schema_version: content_media_pipeline.v1
description: Canonical policy for content generation and media assembly pipeline.

pipeline:
  subtitle_animation_enabled: true
  beat_sync_enabled: true
  montage_feedback_enabled: true
  template_binding_required: true

validation:
  content_ref_required: true
  stage_traceability_required: true
  render_artifact_logging_required: true

rules:
  - media pipeline produces content artifacts, not publishing authority
  - all generation stages must remain auditable
  - pipeline outputs must preserve provenance and template binding
YAML

cat > publishing_policy.yaml <<'YAML'
schema_version: content_media_publishing_policy.v1
description: Canonical policy for media publishing jobs and channel-bound publication paths.

publishing:
  target_channels_required: true
  content_reference_required: true
  approval_required_before_publish: true
  scheduling_allowed: true

restrictions:
  hidden_autopublish_forbidden: true
  channel_policy_required: true
  publish_without_content_ref_forbidden: true

rules:
  - publishing jobs do not bypass governance or approval policy
  - scheduling does not imply automatic publish authority
  - publication paths must remain explicit and reviewable
YAML

echo "content_media configs filled successfully"
