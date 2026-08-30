# CODE - OSS SOURCE ARCHAEOLOGY — JWB-2 v1

Pinned source: `microsoft/vscode@f291f3fd7a3aa047515c65348d8f674a009aba94`  
Status: first-pass source map, no removal/rewrite yet

## 1. Source organization relevant to JARVIS

The pinned Code - OSS source documents chat as a large workbench contribution with clear UI/service separation.

Important source families:

- `src/vs/workbench/contrib/chat/browser/widget/` — core ChatWidget rendering, input, list, model/agent pickers and main UI pieces
- `src/vs/workbench/contrib/chat/browser/widgetHosts/` — hosts that embed the chat widget in view pane/editor/quick chat
- `src/vs/workbench/contrib/chat/browser/chatContentParts/` — response rendering such as Markdown/code/tool output
- `src/vs/workbench/contrib/chat/browser/attachments/` — context attachment model/pickers/widgets
- `src/vs/workbench/contrib/chat/browser/chatEditing/` — edit-session model and diff UI
- `src/vs/workbench/contrib/chat/browser/chatSetup/` — chat setup/auth/install flow
- `src/vs/workbench/contrib/chat/common/chatService/` — `IChatService`, implementation and related service code
- `src/vs/workbench/contrib/chat/common/model/` — chat model/view-model/session storage
- `src/vs/workbench/contrib/chat/common/participants/` — participant/agent management
- `src/vs/workbench/contrib/chat/common/tools/` — language-model tools infrastructure

## 2. Initial KEEP surface

Reuse-first candidates for the first JARVIS Workbench:

- `browser/widget/`
- `browser/widgetHosts/`
- generic `chatContentParts/`
- generic attachments/context UI where it does not own semantic truth
- generic chat model/view-model/session presentation where compatible
- editor/diff UI used for review

These are presentation/session facilities, not permission to copy Copilot authority into JARVIS.

## 3. First ADAPTER seam

The first integration should target the service/backend boundary rather than rewrite the widget tree.

Primary seam to inspect after clean local build:

`src/vs/workbench/contrib/chat/common/chatService/`

The Workbench should preserve the existing UI-facing contracts where practical while adapting the backend flow to the canonical JARVIS endpoint/contracts.

Target concept:

```text
existing ChatWidget / hosts / renderers
             |
             v
UI-facing chat service contract
             |
             v
JARVIS Workbench adapter
             |
             v
existing JARVIS conversation path
```

No direct provider or tool execution is introduced here.

## 4. Copilot/product coupling confirmed in pinned baseline

`product.json` in the pinned baseline currently configures:

- product identity as `Code - OSS`
- `defaultChatAgent` as GitHub Copilot/Copilot Chat
- GitHub/GHE/Google/Apple/Microsoft provider metadata for that default chat agent
- Copilot entitlement/token/quota URLs and commands
- `GitHub.copilot-chat` in built-in extensions enabled with auto-updates
- Microsoft-hosted voice WebSocket URL

This is exactly why the architecture separates KEEP UI from REPLACE backend/product coupling.

## 5. Initial classification

### KEEP before live gate

- chat widget/rendering/hosting
- editor/terminal/workspace/settings/layout infrastructure
- Extension Host / required APIs
- generic diff/review surfaces

### ADAPT / REPLACE before JARVIS live gate

- default chat backend routing
- JARVIS session/stream/cancel mapping
- model projection from canonical JARVIS registry
- authentication bridge using existing JARVIS host-principal/session path

### REMOVE only after live JARVIS + Codex gate

- Copilot entitlement/quota/signup/pricing/onboarding
- Copilot cloud endpoints not required by MAKSIMAR
- Copilot auto-update coupling
- Microsoft voice endpoint after approved local JARVIS voice path is wired
- telemetry/experiments/recommendations and other unneeded cloud services

## 6. What NOT to import as JARVIS authority

The Code - OSS chat stack contains its own participant/tool/model concepts because it is a generic editor platform.
Those concepts must not silently become the canonical JARVIS capability/provider/tool registries.

If retained internally for UI mechanics, they remain adapters/projections only.
Canonical semantic ownership stays upstream in MAKSIMAR/JARVIS.

## 7. Next archaeology step

After JWB-1 clean local build is proven:

1. trace exact request path from ChatWidget submit to `IChatService`
2. identify the narrowest backend injection/adapter seam
3. trace session storage and cancellation
4. map model picker data source
5. map chat setup/entitlement dependencies that can be bypassed without deleting UI
6. run Codex compatibility baseline before structural cleanup

No source deletion is authorized by this document.
