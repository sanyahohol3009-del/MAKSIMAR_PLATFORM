#!/usr/bin/env bash
set -e

cd "$HOME/MAKSIMAR_PLATFORM/MAKSIMAR_CORE/contracts/content_media"

rm -f media_asset.v1.yaml media_pipeline.v1.yaml media_render_job.v1.yaml media_publish.v1.yaml

cat > media_template.v1.yaml <<'YAML'
contract_name: media_template
schema_version: media_template.v1
description: Template definition for media generation workflows.

required:
  - template_id
  - template_type

fields:
  template_id:
    type: string
    description: Unique media template identifier.

  template_type:
    type: string
    description: Canonical template class or family.

  assets:
    type: array
    items:
      type: string
    description: Explicit asset references used by this template.

  style_profile:
    type: string
    description: Style profile bound to the template.

validation_rules:
  - template_id required
  - template_type required
  - assets should be explicit even when empty

security_rules:
  - templates are assets, not publishing authority
  - template metadata must not embed hidden execution logic
  - asset references must remain traceable
YAML

cat > publishing_job.v1.yaml <<'YAML'
contract_name: publishing_job
schema_version: publishing_job.v1
description: Publishing job descriptor.

required:
  - job_id
  - target_channels
  - content_ref

fields:
  job_id:
    type: string
    description: Unique publishing job identifier.

  target_channels:
    type: array
    items:
      type: string
    description: Explicit list of target publishing channels.

  content_ref:
    type: string
    description: Reference to content artifact being published.

  schedule_ref:
    type: string
    description: Optional reference to schedule or timing policy.

  approval_required:
    type: boolean
    description: Whether explicit approval is required before publication.

validation_rules:
  - job_id required
  - target_channels required
  - target_channels must not be empty
  - content_ref required
  - approval_required should be explicit

security_rules:
  - publish authority requires approval
  - publishing jobs do not bypass governance or channel policy
  - scheduling does not imply automatic publishing authority
YAML

cat > subtitle_animation.v1.yaml <<'YAML'
contract_name: subtitle_animation
schema_version: subtitle_animation.v1
description: Subtitle animation profile contract.

required:
  - profile_id
  - style

fields:
  profile_id:
    type: string
    description: Unique subtitle animation profile identifier.

  style:
    type: string
    description: Canonical subtitle animation style.

  timing_policy:
    type: object
    additional_properties: true
    description: Structured timing and animation policy settings.

validation_rules:
  - profile_id required
  - style required
  - timing_policy should be explicit when animation timing is customized

security_rules:
  - style metadata only
  - subtitle animation profiles do not imply rendering or publishing authority
  - timing policy must remain bounded by content pipeline rules
YAML

cat > beat_profile.v1.yaml <<'YAML'
contract_name: beat_profile
schema_version: beat_profile.v1
description: Beat or rhythm profile for media synchronization.

required:
  - beat_profile_id
  - bpm_or_timing_ref

fields:
  beat_profile_id:
    type: string
    description: Unique beat profile identifier.

  bpm_or_timing_ref:
    type: string
    description: Reference to BPM data, timing map, or rhythm artifact.

  source_audio_ref:
    type: string
    description: Optional reference to source audio asset.

validation_rules:
  - beat_profile_id required
  - bpm_or_timing_ref required
  - source_audio_ref should be explicit when derived from audio

security_rules:
  - informational only
  - beat profiles do not imply rendering or publishing authority
  - rhythm metadata must remain traceable to source artifacts
YAML

echo "content_media strict contracts restored successfully"
