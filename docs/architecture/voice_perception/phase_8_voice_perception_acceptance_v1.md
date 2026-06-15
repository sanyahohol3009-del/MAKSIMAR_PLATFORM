# PHASE 8 Voice Perception Acceptance v1

Status: PHASE 8 closed.

## 1. Scope Closure

PHASE 8 closed for voice, gesture, and mobile perception as a contract/read-model layer only.

PHASE 8 remains:

- metadata-only for ASR, voice clone, and gesture/perception contracts
- text intent only
- proposal only
- read-only for status and mobile bridge state

PHASE 8 does not introduce shell execution, canonical write, PC control, direct mobile control, microphone runtime start, camera runtime start, audio playback runtime start, or model download.

## 2. Batch 8.1 Present

Batch 8.1 files/tests are present:

- `MAKSIMAR_CORE_LIB/voice_perception/__init__.py`
- `MAKSIMAR_CORE_LIB/voice_perception/asr_backend_adapter_contract.py`
- `MAKSIMAR_CORE_LIB/voice_perception/voice_clone_backend_adapter_contract.py`
- `MAKSIMAR_CORE_LIB/voice_perception/gesture_backend_adapter_contract.py`
- `MAKSIMAR_CORE_LIB/voice_perception/perception_policy_contract.py`
- `tests/voice_perception/test_asr_backend_adapter_contract_smoke.py`
- `tests/voice_perception/test_voice_clone_backend_adapter_contract_smoke.py`
- `tests/voice_perception/test_gesture_backend_adapter_contract_smoke.py`
- `tests/voice_perception/test_voice_ownership_still_required_smoke.py`
- `tests/voice_perception/test_perception_policy_contract_smoke.py`

ASR/voice clone/gesture contracts are metadata-only.

## 3. Batch 8.2 Present

Batch 8.2 files/tests are present:

- `ANDROID_SHELL/voice_adapter/moonshine_android_adapter_contract.py`
- `ANDROID_SHELL/voice_adapter/mediapipe_android_adapter_contract.py`
- `ANDROID_SHELL/voice_adapter/android_voice_state_bridge.py`
- `IOS_SHELL/voice_adapter/moonshine_ios_adapter_contract.py`
- `IOS_SHELL/voice_adapter/mediapipe_ios_adapter_contract.py`
- `IOS_SHELL/voice_adapter/ios_voice_state_bridge.py`
- `tests/voice_perception/test_android_voice_state_bridge_smoke.py`
- `tests/voice_perception/test_ios_voice_state_bridge_smoke.py`
- `tests/voice_perception/test_local_asr_sends_text_only_smoke.py`
- `tests/voice_perception/test_raw_audio_stream_blocked_by_default_smoke.py`

Android/iOS bridges send text only.
Raw audio blocked by default.

## 4. Batch 8.3 Present

Batch 8.3 files/tests are present:

- `MAKSIMAR_CORE_LIB/voice_perception/voice_perception_status_read_model.py`
- `tools/voice_perception_status_preview.py`
- `CONTAINER_DEPLOYMENT/cubes/voice_perception/container_contract.yaml`
- `tests/voice_perception/test_voice_perception_status_read_model_smoke.py`
- `tests/voice_perception/test_voice_message_allowed_as_chat_attachment_smoke.py`
- `tests/voice_perception/test_voice_message_not_command_without_intent_smoke.py`

Voice messages may be chat attachments.
Voice messages are not commands without explicit text intent.

## 5. Required Safety State

Owner voice gate required.
Raw audio blocked by default.
Text intent only.
No shell execution.
No PC control.
Shell execution allowed = false.
Canonical write allowed = false.
PC control allowed = false.
Direct mobile control allowed = false.
Microphone runtime started = false.
Camera runtime started = false.
Audio playback runtime started = false.
Model download allowed = false.

## 6. Downstream Parking

PHASE 9 junior model parked.
Windows Voice Edge parked.
Push-to-Talk STT live parked.

PHASE 9 junior model runtime remains parked.
Windows Voice Edge remains parked.
Push-to-Talk STT live remains parked.

## 7. Architecture Rule

No second JARVIS.
No second voice world.

Existing voice/mobile surfaces extended by contracts/read-model only:

- `VOICE_LAYER`
- `MAKSIMAR_CORE_LIB/real_voice_runtime`
- `MAKSIMAR_SERVER/VOICE_ROUTING`
- `MAKSIMAR_SERVER/VOICE_DISPLAY_HANDOFF`
- `MAKSIMAR_SERVER/VOICE_EXECUTION_HANDOFF`
- `ANDROID_SHELL/voice_adapter`
- `IOS_SHELL/voice_adapter`

PHASE 8 closure does not create a new runtime world, a new root architecture, or a second assistant.
