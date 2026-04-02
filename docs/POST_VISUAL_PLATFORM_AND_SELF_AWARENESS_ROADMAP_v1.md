# POST VISUAL PLATFORM AND SELF-AWARENESS ROADMAP v1

Status: active canonical post-visual roadmap
Scope: mandatory project work after visual premium baseline is reached
Rule: after the visual milestone, the platform must continue through platform completion, adaptive display intelligence, self-awareness, archive intelligence, evidence display, investor/demo mode, and only then into agent-swarm cube development

---

## 1. Purpose

This document defines the official next roadmap after the visual premium baseline.

It exists to prevent:
- losing strategic continuity after the first premium visual result
- jumping into agent systems before platform completion
- building self-awareness as vague chat memory instead of a structured system
- mixing read-only project awareness with uncontrolled self-modification
- losing historical project knowledge from chats, files, and artifacts
- leaving critical post-visual layers underspecified

---

## 2. Core Rule

After the visual milestone, the correct order is:

1. finish the platform properly
2. build adaptive display / monitor intelligence
3. build project self-awareness / provenance / archive intelligence
4. build artifact registry and evidence display
5. build investor / demo mode
6. only then build the agent swarm cube

No bypass is allowed.

---

## 3. Current Confirmed Foundation Already Present

The following project elements are already considered part of the architecture baseline.

### 3.1 Safety / governance / execution philosophy
- immutable core direction
- control-plane separation
- sandbox-first execution discipline
- proposal → sandbox → diff → tests → review → explicit approval → apply
- control ≠ execution ≠ dashboard
- read-only visual discipline
- no direct UI-owned execution shortcuts
- security-first architecture direction
- approval-based mutation model

### 3.2 Visual / operator baseline already built
The following visual track is already established as part of the current project trajectory:
- panel vocabulary / mapping direction
- display/workspace/view separation
- visual theme contracts
- visual shell contracts
- panel-to-visual mapping
- visual signal overlay
- visual topology overlay
- visual explainability sidebar
- visual status bar
- visual bottom ticker
- visual HUD composition
- visual HUD snapshot / preview / screen / render-result / preview-artifact / preview-state chain
- Phase 1 visual polish hardening chain
- first view / showable / observable / displayable / presentable / demo / watchable / presented / renderable / output-ready / result / viewable-result progression

### 3.3 Project-wide architectural laws already established
- platform first
- no drift
- no duplication
- no shortcuts
- only production-grade architecture
- dashboard remains downstream
- UI must not become execution authority
- network / segmentation / trust boundaries remain separate engineering layers
- read scope is not the same as write/apply scope

---

## 4. Mandatory Next Macro-Phase After Visual Premium Baseline

After the visual milestone, the next macro-phase is:

### 4.1 Platform completion
The platform must be completed and hardened before advanced self-awareness or agent swarm expansion.

### 4.2 Adaptive display / monitor intelligence
The system must understand its display environment automatically.

### 4.3 Project self-awareness / provenance / archive intelligence
The system must be able to understand its own project history, architecture, code, dependencies, and evidence trail.

### 4.4 Artifact registry + evidence display
The system must be able to show project evidence on-screen.

### 4.5 Investor / demo mode
The system must be able to explain itself and present the project from verified sources.

### 4.6 Agent swarm cube
Only after the above are stable should the agent helper / swarm cube be built.

---

## 5. Adaptive Display / Monitor Intelligence Layer

### 5.1 Goal

The platform must automatically understand each display it is using.

This includes:
- monitor identity
- display role
- geometry
- scale
- density
- motion budget
- placement in a multi-monitor topology

### 5.2 Required capabilities

The platform must know:

- `display_id`
- human-readable display label if available
- resolution
- aspect ratio
- physical size / diagonal when available
- pixel density / DPI / scale
- refresh rate when available
- display position in topology
- primary / secondary / operator / wall / mobile / wrist / external roles
- available render workspace
- fullscreen / windowed constraints
- orientation / rotation state
- multi-monitor relationship

### 5.3 Required behavior

The dashboard / HUD must not assume one fixed monitor.

It must automatically adapt:
- panel density
- spacing
- font scaling
- layout mode
- motion budget
- visual effects intensity
- signal animation budget
- center-core scale
- sidebar width
- navigation density

### 5.4 What this layer must contain

#### Must create
- `display_runtime_profile_contract`
- `display_capability_contract`
- `display_density_policy_contract`
- `display_motion_budget_contract`
- `display_layout_adaptation_contract`
- `display_topology_identity_contract`
- `display_role_assignment_contract`
- `display_placement_resolution_contract`
- `adaptive_visual_scaling_contract`

#### Hardening contracts
- `display_runtime_safety_contract`

#### Likely directories
- `MAKSIMAR_CORE_LIB/display_runtime/`
- `MAKSIMAR_CORE_LIB/display_capabilities/`
- `MAKSIMAR_SERVER/RUNTIME/display_runtime/`
- `MAKSIMAR_SERVER/CONTROL_PLANE/display_resolution/`
- `MAKSIMAR_CORE_LIB/oob_dashboard/` for downstream display-facing read models only

### 5.5 Display runtime safety requirements

The system must define what happens when:
- monitor metadata is false or inconsistent
- DPI is unavailable
- scale is unavailable
- topology conflicts are detected
- two displays expose the same identifier
- refresh rate is unavailable
- geometry is partial or malformed

The safety layer must support:
- fallback display identity logic
- degraded display mode
- conservative scaling fallback
- conflict flagging
- deterministic tie-breaking
- explicit unknown/unavailable states

### 5.6 Hard rule

Adaptive display intelligence must be capability-driven and contract-driven.
It must not be hardcoded into one UI mockup.

---

## 6. Project Self-Awareness / Provenance / Archive Intelligence Layer

### 6.1 Goal

JARVIS / MAKSIMAR must be able to understand and explain:
- what it is
- how it was created
- what was decided
- what failed
- what was fixed
- what code and dependencies currently exist
- what evidence supports its statements

### 6.2 This is NOT “chat memory”

This layer is not vague conversational memory.

It is a structured, evidence-backed project awareness layer.

### 6.3 Required read-only awareness domains

The system must be able to inspect and reason over:

- repository structure
- current code tree
- contracts
- architecture documents
- dependency relationships
- test inventory
- historical decisions
- prior mistakes and fixes
- imported chat archives
- imported project documents
- imported PDFs
- imported images
- imported code snippets
- imported artifacts from prior sessions

### 6.4 Required capabilities

The system must be able to answer:
- who created this part of the project
- when was it introduced
- in which chat / source / document did it appear
- what problem was it solving
- what later replaced or corrected it
- what is canonical now
- what evidence supports that answer

### 6.5 Must create

#### Contracts
- `project_self_awareness_contract`
- `project_provenance_contract`
- `project_decision_history_contract`
- `repository_awareness_contract`
- `code_dependency_awareness_contract`
- `architecture_history_contract`
- `conversation_archive_awareness_contract`
- `artifact_evidence_link_contract`
- `canonical_truth_resolution_contract`
- `truth_conflict_resolution_policy`

#### Likely directories
- `MAKSIMAR_CORE_LIB/project_self_awareness/`
- `MAKSIMAR_CORE_LIB/provenance/`
- `MAKSIMAR_CORE_LIB/repository_intelligence/`
- `MAKSIMAR_CORE_LIB/archive_intelligence/`
- `MAKSIMAR_SERVER/KNOWLEDGE/project_awareness/`

### 6.6 Truth arbitration requirements

The self-awareness layer must define how conflicting sources are resolved.

It must explicitly handle:
- chat vs code conflicts
- document vs document conflicts
- old contract vs new contract conflicts
- stale architecture notes vs current repository truth
- conflicting provenance chains

The truth arbitration layer must support:
- canonical source ranking
- recency-aware conflict handling
- source trust tiers
- conflict surfacing instead of silent suppression
- evidence-backed resolution decisions
- explicit unresolved-conflict state when necessary

### 6.7 Hard rule

This layer is read-only.
Self-awareness does not imply self-modification.

---

## 7. Conversation / Archive Ingestion Pipeline

### 7.1 Goal

The system must be able to ingest exported conversations and project archives in a controlled way.

### 7.2 Supported input types

The ingestion pipeline must eventually support:
- JSON conversation exports
- text exports
- PDFs
- images
- code files
- markdown docs
- structured metadata
- attached artifacts from conversations

### 7.3 Required pipeline stages

1. raw source intake
2. parsing
3. normalization
4. metadata extraction
5. code block extraction
6. attachment extraction
7. stable ID generation
8. fingerprint generation
9. deduplication
10. evidence linking
11. searchable indexing
12. project-phase tagging
13. archive persistence

### 7.4 Deduplication requirement

When new exports are imported, the system must add only what is new.

It must not duplicate content that already exists.

#### Deduplication basis should include
- source identifier
- chat/thread identifier if available
- timestamp
- normalized text hash
- attachment hash
- artifact hash
- extracted code block hash
- normalized message fingerprint

### 7.5 Must create

#### Contracts
- `archive_source_contract`
- `conversation_import_contract`
- `conversation_normalization_contract`
- `conversation_message_fingerprint_contract`
- `archive_deduplication_contract`
- `attachment_extraction_contract`
- `archive_indexing_contract`
- `archive_source_metadata_contract`
- `archive_input_safety_contract`
- `archive_sanitization_contract`

#### Likely directories
- `MAKSIMAR_CORE_LIB/archive_ingestion/`
- `MAKSIMAR_CORE_LIB/conversation_import/`
- `MAKSIMAR_CORE_LIB/deduplication/`
- `MAKSIMAR_SERVER/INGESTION/archive_pipeline/`

### 7.6 Archive input safety requirements

The ingestion pipeline must define what happens when input is unsafe or malformed.

It must explicitly handle:
- malicious PDFs
- oversized files
- zip bombs
- malformed archives
- unsupported encodings
- corrupted JSON
- truncated exports
- binary payloads masquerading as text
- attachment explosion / fan-out abuse

The safety layer must support:
- reject
- quarantine
- sanitize
- size limits
- encoding fallback
- safe parse timeout
- parser isolation
- explicit unsafe input state

### 7.7 Hard rule

The ingestion system must preserve raw history and canonical extracted knowledge separately.

---

## 8. Artifact Registry + Evidence Display Layer

### 8.1 Goal

The system must be able to store, index, retrieve, and display evidence artifacts.

### 8.2 Artifact types

The registry must support:
- chats
- documents
- markdown files
- PDFs
- code files
- code snippets
- screenshots
- images
- architectural notes
- test outputs
- decision records

### 8.3 What the system must be able to do

On request, it should be able to:
- show the relevant source conversation
- show a code file or snippet
- show a PDF
- show an image
- show a timeline event
- show supporting evidence for a claim
- explain why that artifact matters

### 8.4 Must create

#### Contracts
- `artifact_registry_contract`
- `artifact_identity_contract`
- `artifact_storage_contract`
- `artifact_reference_contract`
- `artifact_evidence_display_contract`
- `artifact_source_link_contract`
- `artifact_screen_presentation_contract`

#### Likely directories
- `MAKSIMAR_CORE_LIB/artifact_registry/`
- `MAKSIMAR_CORE_LIB/evidence_display/`
- `MAKSIMAR_SERVER/ARTIFACTS/`

### 8.5 Hard rule

Displayed evidence must be source-backed.
No invented provenance.

---

## 9. Investor / Demo Mode

### 9.1 Goal

JARVIS should eventually be able to present the project directly to investors or observers.

### 9.2 Required behavior

In demo mode, the system should:
- answer from verified project knowledge
- explain architecture
- explain timeline and evolution
- show supporting code/documents/artifacts
- explain mistakes and fixes honestly
- avoid inventing capabilities not yet built
- remain controlled and safe

### 9.3 What it must present

It should be able to present:
- project vision
- architecture
- security model
- roadmap
- current implementation state
- tests
- governance
- evidence
- historical decisions
- artifact-backed explanations

### 9.4 Must create

#### Contracts
- `investor_demo_mode_contract`
- `demo_question_answering_contract`
- `evidence_backed_response_contract`
- `demo_artifact_presentation_contract`
- `controlled_demo_session_contract`

#### Likely directories
- `MAKSIMAR_CORE_LIB/demo_mode/`
- `MAKSIMAR_SERVER/DEMO_MODE/`

### 9.5 Hard rule

Demo mode must be evidence-backed and controlled.
It must not become a hallucination layer.

---

## 10. Governance Boundary For Self-Awareness

### 10.1 Rule

Self-visibility is not the same as self-authority.

### 10.2 Read vs write

The self-awareness layer may have broad read access to:
- code
- contracts
- docs
- test results
- ingested archives
- artifacts
- project history

But it must not automatically gain:
- mutation authority
- apply authority
- delete authority
- publish authority

### 10.3 Mandatory mutation path

Any self-change must still go through:

`proposal → sandbox → diff → tests → review → explicit approval → apply`

### 10.4 Hard rule

The system may explain itself freely.
It may not rewrite itself freely.

---

## 11. Agent Swarm Cube — Correct Position In Roadmap

### 11.1 Rule

The agent swarm must not be built before platform completion and self-awareness foundations.

### 11.2 Correct placement

The correct order is:

1. visual premium baseline
2. platform completion
3. adaptive display / monitor intelligence
4. self-awareness / provenance / archive intelligence
5. artifact registry + evidence display
6. investor / demo mode
7. agent swarm cube

### 11.3 Agent swarm placement rule

The swarm must be built as:
- separate module / cube
- not as a replacement core
- not as alternate authority
- policy-bound
- dashboard-exposed
- approval-controlled

### 11.4 Must create later

#### Contracts
- `agent_swarm_cube_contract`
- `agent_role_registry_contract`
- `agent_handoff_contract`
- `agent_evidence_access_contract`
- `agent_tool_governance_contract`
- `agent_approval_boundary_contract`
- `agent_capability_boundary_contract`
- `agent_capability_tier_contract`

#### Likely directories
- `DOMAIN_CUBES/agent_swarm_cube/`
- `MAKSIMAR_CORE_LIB/agent_swarm/`
- `MAKSIMAR_SERVER/AGENT_SWARM/`

### 11.5 Agent capability governance requirements

The swarm layer must explicitly define:
- forbidden capabilities
- read-only capabilities
- capabilities that require evidence
- capabilities that require sandbox
- capabilities that require approval
- capability escalation rules
- agent role-specific restrictions

The swarm must not rely on implicit trust.

---

## 12. What Already Exists vs What Must Be Created

### 12.1 Already exists in meaningful form
- visual contract chain
- dashboard/view/display separation logic
- control vs execution vs dashboard law
- approval and sandbox philosophy
- platform-first architectural direction
- read-only visual discipline
- many operator HUD contracts and preview/result boundaries

### 12.2 Must still be created after visual milestone

#### Adaptive display
- display runtime profile layer
- display capability layer
- adaptive scaling and motion budget layer
- multi-monitor identity / topology layer
- display runtime safety layer

#### Self-awareness
- repository awareness
- dependency awareness
- provenance layer
- decision history layer
- architecture history layer
- truth arbitration layer

#### Archive ingestion
- conversation import pipeline
- normalization pipeline
- deduplication
- artifact extraction
- indexing layer
- input safety / sanitization layer

#### Artifact registry / display
- registry
- identity model
- evidence display
- artifact screen presentation

#### Demo mode
- investor/demo contracts
- evidence-backed Q&A mode
- controlled demo session layer

#### Agent swarm cube
- only after all the above
- with explicit capability governance

---

## 13. Canonical Post-Visual Build Order

The official build order after visual premium baseline is:

### Stage A — Platform completion
- finish remaining platform obligations
- no visual shortcuting
- stabilize contracts, read models, and boundaries

### Stage B — Adaptive display / monitor intelligence
- monitor identity
- display capability
- scaling
- density
- layout adaptation
- motion budget
- display runtime safety

### Stage C — Project self-awareness / provenance / archive intelligence
- repository awareness
- dependency awareness
- history awareness
- archive awareness
- provenance graph
- truth arbitration

### Stage D — Conversation/archive ingestion pipeline
- JSON import
- normalization
- deduplication
- indexing
- persistence
- input safety
- sanitization

### Stage E — Artifact registry + evidence display
- artifact storage
- retrieval
- evidence display
- on-screen artifact explanation

### Stage F — Investor/demo mode
- controlled evidence-backed project presentation

### Stage G — Agent swarm cube
- separate module
- policy-bound
- approval-bound
- dashboard-exposed
- capability-tiered

---

## 14. Hard Rule For Future Chats

This roadmap must be treated as canonical project direction after the visual milestone.

Any future proposal that:
- jumps directly to agent swarm before platform completion
- skips display intelligence
- skips self-awareness structure
- skips archive ingestion / deduplication
- skips archive input safety
- skips truth arbitration
- skips artifact evidence layer
- turns self-awareness into self-authority
- builds swarm without capability boundaries

must be treated as architectural drift.

---

## 15. Final Rule

After beauty, the project must not become shallow.

It must become:
- adaptive
- self-aware
- provenance-backed
- evidence-backed
- investor-demonstrable
- policy-safe
- platform-complete

Only then should the agent swarm cube be introduced.

---

## 16. Status

This document is the active canonical roadmap for the project after the visual milestone until replaced by a stricter platform-completion roadmap.
