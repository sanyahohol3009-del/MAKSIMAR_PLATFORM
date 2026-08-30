# JARVIS CODE - OSS INTEGRATION CONTRACT v1

Status: active implementation contract for `workbench/code-oss-baseline-2026-08-31`  
Track: `JARVIS_DEVELOPER_WORKBENCH` / JWB-0 onward  
Purpose: integrate a frozen Code - OSS shell into the existing MAKSIMAR/JARVIS architecture without creating parallel authority.

## 1. Non-negotiable architecture

JARVIS remains one system and one Global Brain.

```text
UNDERSTAND GLOBALLY
 -> SELECT ORGAN
 -> EXPAND LOCALLY
 -> EXECUTE LOCALLY
 -> REPORT CANONICALLY
```

Implementation discovery law:

```text
DISCOVER EXISTING
 -> REUSE EXISTING
 -> EXTEND EXISTING
 -> ADD NEW ONLY IF IT DOES NOT EXIST
```

Code - OSS is downstream from these laws.

## 2. What Code - OSS becomes

Code - OSS is the initial implementation substrate for `JARVIS_DEVELOPER_WORKBENCH`.
It is not a new JARVIS, new planner, new memory system, new registry family or new execution authority.

```text
Code - OSS shell
      |
      v
JARVIS Developer Workbench
      |
      v
Global JARVIS
      |
      v
canonical capability / organ / provider
      |
      v
evidence / canonical response
```

## 3. Existing owners that MUST be reused

The Workbench must consume and expose the already existing owners rather than reproduce them:

- Global Semantic Spine / GoalFrame path
- hierarchical semantic capability -> operation -> organ architecture
- provider identity separation from semantic capability
- External Agent Provider Layer
- runtime model transport and readiness path
- owner identity / host principal / authenticated session path
- authorization / approval boundaries
- PC Hands controlled action layer
- Browser Organ
- existing Voice software path
- Simulation Organ / worker path
- `SANDBOX_REVIEW`
- `ExecutionReceipt`
- `EvidenceBundle`
- FinalBrain evidence discipline
- `DeveloperExperience`
- `LearningBundle`
- `CLIENT_LEARNING_INPUT`
- append-only experience persistence / retrieval
- proposal / evolution / self-expansion gates
- canonical observability / bounded developer trace

## 4. Forbidden duplicate systems

Do not create:

- `CodeOSSBrain`
- `IDEBrain`
- `VSCodePlanner`
- `CodexBrain`
- `DeepSeekBrain`
- second Semantic Brain
- second global planner
- second canonical memory
- second policy engine
- second capability registry
- second provider registry
- second evidence authority
- second learning/evolution engine
- IDE-owned project vector database merely for convenience
- IDE-owned security/action authority

## 5. Semantic routing boundary

User language must not directly select Codex, DeepSeek, a worker or an implementation framework.

Correct:

```text
user intent
 -> GoalFrame / semantic understanding
 -> public semantic capability
 -> operation
 -> organ
 -> provider / worker if required
```

Incorrect:

```text
if prompt contains "Codex":
    codex.execute()
```

Provider identity remains separate from semantic capability.

## 6. Authorization boundary

`UNDERSTANDING != AUTHORIZATION` and `PROPOSAL != AUTHORIZATION` remain absolute.

The Workbench may show plans, proposals, diffs and execution intent.
It may not interpret a conversational answer as permission to modify files, execute arbitrary commands or mutate external state.

All controlled actions continue through existing policy/auth/approval/execution/evidence paths.

## 7. Evidence boundary

Coder/provider claims are not execution truth.

A statement such as "I fixed the file" is not canonical evidence.
The platform must rely on readback, tests, receipts and evidence already owned upstream.

The Workbench may visualize:

- intent
- GoalFrame
- selected capability
- operation
- provider
- authorization
- execution
- receipt
- sandbox review
- evidence
- learning result

but UI state is not canonical truth.

## 8. Coder roles

Codex remains a permanent independent co-developer during the initial Workbench stages.
JARVIS does not silently become Codex's controller.
Codex compatibility is a protected STOP-GATE before deep cleanup of Code - OSS extension/runtime surfaces.

DeepSeek, when used for JARVIS coding work, must enter through the existing bounded external provider architecture rather than as a second brain.

When multiple coder actors work on the same change, preserve the one-primary-writer rule. Other actors review, diagnose, propose or verify unless a different owner-approved role assignment exists.

## 9. First Workbench surface

Initial useful surface should reuse existing Code - OSS facilities and expose only canonical JARVIS data/contracts:

```text
JARVIS
|- Chat
|- Current Goal
|- Semantic Trace
|- Agents / coder status
|- Project
|- Dirty Tree
|- Tests
|- Evidence
`- Learning
```

The first conversation path must be:

```text
existing Code - OSS Chat UI
 -> existing JARVIS endpoint / Workbench bridge
 -> Global Semantic Brain
 -> canonical capability
 -> provider if required
 -> EvidenceBundle
 -> answer
```

## 10. Code - OSS keep-first policy

Before live acceptance retain the mature facilities already approved in the canonical Workbench architecture:

- top bars / menus / Command Center
- Settings / profiles / themes / keybindings
- Activity Bar / sidebars
- Explorer / Search / Source Control
- editor / tabs / breadcrumbs / diff
- terminal
- Problems / Output / Testing / Debug
- status bar / layout persistence
- Extension Host and required APIs
- existing chat presentation

Do not mass-delete Microsoft/Copilot code before the live Workbench is proven.

## 11. Cleanup order after live gate

After JARVIS + Codex acceptance, remove/replace in bounded batches:

1. Copilot backend/provider authority
2. Copilot entitlement/quota/signup/pricing/onboarding
3. cloud-only AI provider coupling not needed by MAKSIMAR
4. unwanted telemetry/experiments/recommendations
5. Settings Sync / tunnels if unneeded
6. Microsoft product updater/release dependency
7. unrestricted external Marketplace dependency
8. unused bundled extensions/services

Each batch requires inventory -> dependency map -> diff -> build/tests -> JARVIS smoke -> Codex smoke -> acceptance.

## 12. Frozen upstream baseline

Pinned Code - OSS snapshot:

- repository: `microsoft/vscode`
- commit: `f291f3fd7a3aa047515c65348d8f674a009aba94`
- observed upstream commit time: `2026-08-30T22:10:47Z`
- package: `code-oss-dev 1.136.0`
- Node: `24.18.0`
- Electron target: `42.10.0`
- license: MIT

Automatic upstream feature merging is forbidden.
Security monitoring/backports remain MAKSIMAR-controlled.

## 13. Parallel-track isolation

The current Semantic Spine / GoalFrame repair remains owned by the existing active development track.
This Code - OSS branch MUST NOT repair, normalize, reset or clean that work.

The Workbench branch may proceed with:

- upstream archaeology
- frozen baseline pinning
- bootstrap/build reproduction
- Workbench shell contract work
- adapter/interface discovery
- read-only integration design

Before merge, this branch must be rebased/reconciled against the completed semantic track.

## 14. Known semantic blocker is not a Workbench bug

The current recorded RU stability defect is a GoalFrame binding-input gap in the existing semantic track.
The Workbench must not patch around it with UI keyword routing, provider shortcuts or hardcoded `simulation.run` behavior.

## 15. Live acceptance gate

Deep cleanup is blocked until the modified Workbench proves:

- reproducible build and launch
- Explorer/editor/terminal/Git/diff/settings/top bars
- existing chat UI connected to real JARVIS
- streaming/cancellation/session restoration
- canonical model projection
- approved voice path
- independent Codex operation
- persistent layout/state

## 16. Final rule

The objective is not "VS Code plus a JARVIS plugin".
The objective is a MAKSIMAR-owned `JARVIS_DEVELOPER_WORKBENCH` whose initial shell is Code - OSS, whose authority is upstream JARVIS, and whose external dependencies are progressively reduced without breaking the platform laws.
