# PHASE 8 / PHASE 9 Live Activation Sequence v1

## 1. Purpose

This document is the canonical execution-sequence anchor for `demolition/visual-reset-v1` before any PHASE 8 or PHASE 9 implementation work starts.

It locks the owner-mandated order:

1. check project memory, project knowledge, and roadmap state before every step
2. follow Roadmap v4.2.1 strictly
3. close PHASE 8 first with real voice/perception activation
4. close PHASE 9 second for Android/iOS on-device junior AI
5. continue with `JARVIS-WINDOWS-VOICE-EDGE-RUNTIME-1`
6. continue with `JARVIS-PUSH-TO-TALK-STT-LIVE-1`

This sequence extends existing JARVIS-LIVE surfaces only. It must not create a second JARVIS, a second voice world, or a new root architecture.

## 2. Canonical Sequence

The execution order is fixed:

1. before each batch or sub-step, review project memory state, project knowledge state, and roadmap state
2. keep Roadmap v4.2.1 as the controlling roadmap
3. execute PHASE 8 and do not start PHASE 9 closure work until PHASE 8 is closed
4. execute PHASE 9 and do not start Windows Voice Edge runtime work until PHASE 9 is closed
5. execute `JARVIS-WINDOWS-VOICE-EDGE-RUNTIME-1`
6. execute `JARVIS-PUSH-TO-TALK-STT-LIVE-1`

The pre-step review must treat the following as canonical reuse surfaces:

- `VOICE_LAYER`
- `MAKSIMAR_CORE_LIB/real_voice_runtime`
- `MAKSIMAR_SERVER/VOICE_ROUTING`
- `MAKSIMAR_SERVER/VOICE_DISPLAY_HANDOFF`
- `MAKSIMAR_SERVER/VOICE_EXECUTION_HANDOFF`
- `ANDROID_SHELL`
- `IOS_SHELL`
- existing roadmap and no-drift documents under `docs/architecture/jarvis_live/`

## 3. PHASE 8 Scope

PHASE 8 is the real voice/perception activation gate for the existing JARVIS-LIVE stack.

PHASE 8 includes:

- ASR and TTS contracts
- voice adapters and gesture adapters
- Android and iOS voice bridge contracts
- voice read-model and container/readiness state
- real voice/perception readiness
- mobile senior/junior awareness as reference only

PHASE 8 must extend existing voice surfaces and keep output limited to text intents and proposal-only results.

PHASE 8 must not:

- create a second JARVIS
- create a second voice stack or second voice runtime world
- enable shell execution
- enable write or canonical mutation
- enable PC control
- enable direct mobile device control
- move actions beyond `proposal_only`
- download vendors or models unless a roadmap gate explicitly permits it

## 4. PHASE 9 Scope

PHASE 9 starts only after PHASE 8 is closed.

PHASE 9 includes:

- a small local junior model inside Android and iOS app surfaces
- an app-safe core mirror for mobile
- server-side senior JARVIS awareness of the mobile junior AI node
- mobile junior AI awareness of the server JARVIS node
- a local inference probe
- senior/junior sync

PHASE 9 remains an extension of the existing JARVIS system. The mobile junior model is not a second assistant and not an independent canonical truth source.

## 5. Windows Voice Edge Position

`JARVIS-WINDOWS-VOICE-EDGE-RUNTIME-1` is explicitly downstream of PHASE 8 and PHASE 9.

It must not begin until:

- PHASE 8 is closed
- PHASE 9 is closed
- the roadmap-safe voice and mobile gates above are satisfied

Windows Voice Edge work is therefore a later runtime stage, not part of PHASE 8 closure and not part of PHASE 9 closure.

## 6. Push-to-Talk STT Position

`JARVIS-PUSH-TO-TALK-STT-LIVE-1` comes after Windows Voice Edge runtime work.

Its position is:

1. after PHASE 8
2. after PHASE 9
3. after `JARVIS-WINDOWS-VOICE-EDGE-RUNTIME-1`

The existing push-to-talk contract stays boundary-first: manual activation only, visible status only, no always-listening, no wake-word, no hidden recording, no autonomous voice loop, no shell, no file edit, and no PC control unless a later roadmap gate changes that canonically.

## 7. Shell / Write / PC-Control Boundary

For PHASE 8:

- voice or perception input may produce text intents only
- all actions remain `proposal_only`
- shell execution is forbidden
- file write or canonical mutation is forbidden
- PC control is forbidden
- dashboard execution is forbidden

For PHASE 9:

- mobile junior inference may be local and app-safe
- senior/junior sync must not become unrestricted execution authority
- local mobile AI does not bypass approval, policy, audit, or roadmap gates

Shell execution, write authority, and PC control belong to later Action Library and Computer Use gates, not to PHASE 8.

## 8. Senior/Junior Mobile AI Awareness Rule

There is one JARVIS system with role separation, not two assistants.

The rule is:

- server JARVIS is the senior node
- Android/iOS on-device AI is the junior node
- the senior must know the junior exists
- the junior must know the senior exists
- the junior may mirror app-safe context and propose locally
- the junior must not become a separate canonical truth, separate memory authority, or separate voice world
- sync between senior and junior must preserve existing policy, approval, audit, and canonical ownership boundaries

## 9. Do-Not-Touch List

Do not introduce:

- a second JARVIS
- a second voice world
- a new root architecture
- direct shell control from voice/perception in PHASE 8
- direct canonical write from voice/perception in PHASE 8
- direct PC control in PHASE 8
- direct phone control in PHASE 8
- hidden always-listening runtime
- wake-word runtime inside PHASE 8 closure
- vendor or model downloads before the relevant roadmap gate

Do not replace these existing extension surfaces:

- `VOICE_LAYER`
- `MAKSIMAR_CORE_LIB/real_voice_runtime`
- `MAKSIMAR_SERVER/VOICE_ROUTING`
- `MAKSIMAR_SERVER/VOICE_DISPLAY_HANDOFF`
- `MAKSIMAR_SERVER/VOICE_EXECUTION_HANDOFF`
- `ANDROID_SHELL`
- `IOS_SHELL`

## 10. Acceptance Checklist Before Starting PHASE 8 Batch 8.1

Before PHASE 8 Batch 8.1 starts, confirm all items below:

- project memory state has been reviewed
- project knowledge state has been reviewed
- roadmap state has been reviewed
- Roadmap v4.2.1 is accepted as the controlling sequence source
- PHASE 8 is confirmed as the immediate next closure target
- PHASE 9 is explicitly parked until PHASE 8 is closed
- Windows Voice Edge runtime is explicitly parked until PHASE 9 is closed
- Push-to-Talk STT live runtime is explicitly parked until Windows Voice Edge runtime is closed
- implementation is scoped as an extension of existing voice and mobile shell surfaces
- PHASE 8 outputs are limited to text intents and `proposal_only`
- no shell execution path is introduced
- no write or canonical mutation path is introduced
- no PC-control path is introduced
- no new root architecture is introduced
- no vendor or model download is introduced unless the roadmap gate explicitly permits it
