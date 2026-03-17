#!/usr/bin/env bash
set -e

cd "$HOME/MAKSIMAR_PLATFORM/MAKSIMAR_CORE/contracts/content_media"

cat > media_asset.v1.yaml <<'YAML'
contract_name: media_asset
schema_version: media_asset.v1
description: Canonical media asset descriptor.

required:
  - asset_id
  - asset_type
  - location

fields:
  asset_id:
    type: string
    description: Unique media asset identifier.

  asset_type:
    type: string
    enum:
      - video
      - audio
      - image
      - subtitle
      - animation
    description: Type of media asset.

  location:
    type: string
    description: Storage location or reference.

  hash:
    type: string
    description: Integrity hash of the media asset.

validation_rules:
  - asset_id required
  - asset_type must match enum
  - location required

security_rules:
  - asset reference does not grant execution rights
  - integrity verification recommended
YAML


cat > media_pipeline.v1.yaml <<'YAML'
contract_name: media_pipeline
schema_version: media_pipeline.v1
description: Canonical content generation pipeline definition.

required:
  - pipeline_id
  - stages

fields:
  pipeline_id:
    type: string
    description: Unique pipeline identifier.

  stages:
    type: array
    items:
      type: string
    description: Ordered list of pipeline stages.

  template_ref:
    type: string
    description: Reference to visual template used by the pipeline.

validation_rules:
  - pipeline_id required
  - stages must not be empty

security_rules:
  - pipeline definition does not execute automatically
  - execution remains controlled by workflow layer
YAML


cat > media_template.v1.yaml <<'YAML'
contract_name: media_template
schema_version: media_template.v1
description: Visual template for automated media generation.

required:
  - template_id
  - style_class

fields:
  template_id:
    type: string
    description: Unique template identifier.

  style_class:
    type: string
    description: Style category of the template.

  asset_refs:
    type: array
    items:
      type: string
    description: References to assets used in the template.

validation_rules:
  - template_id required
  - style_class required

security_rules:
  - templates cannot embed executable logic
  - asset references must remain explicit
YAML


cat > media_render_job.v1.yaml <<'YAML'
contract_name: media_render_job
schema_version: media_render_job.v1
description: Render job contract for media pipeline execution.

required:
  - job_id
  - pipeline_ref
  - output_format

fields:
  job_id:
    type: string
    description: Unique render job identifier.

  pipeline_ref:
    type: string
    description: Reference to media pipeline definition.

  output_format:
    type: string
    description: Target output format.

  output_location:
    type: string
    description: Storage destination for rendered media.

validation_rules:
  - job_id required
  - pipeline_ref required
  - output_format required

security_rules:
  - render jobs do not imply publishing authority
  - publishing remains gated by approval workflow
YAML


cat > media_publish.v1.yaml <<'YAML'
contract_name: media_publish
schema_version: media_publish.v1
description: Publication contract for media outputs.

required:
  - publish_id
  - asset_ref
  - target_channel

fields:
  publish_id:
    type: string
    description: Unique publish operation identifier.

  asset_ref:
    type: string
    description: Reference to media asset being published.

  target_channel:
    type: string
    description: Target distribution channel.

  schedule_time:
    type: string
    format: date-time
    description: Optional scheduled publish time.

validation_rules:
  - publish_id required
  - asset_ref required
  - target_channel required

security_rules:
  - publishing must follow approval policy
  - scheduling does not bypass governance rules
YAML

echo "content_media contracts restored successfully"
