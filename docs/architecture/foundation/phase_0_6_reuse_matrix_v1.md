# PHASE 0.6 — Reuse Audit / Existing Surface Consolidation v1

## Назначение

Этот документ фиксирует матрицу переиспользования перед дальнейшей работой по памяти, registry, retrieval/RAG и dashboard.

Цель:
- не создать architectural drift;
- не создать второй memory subsystem;
- не создать второй manifest / ID / registry / dashboard layer;
- сначала зарегистрировать уже существующие поверхности проекта;
- подготовить безопасный переход к PHASE 1 — History Binding.

## Главное правило

Не создавать новую архитектуру, если уже есть принятый слой.

Каждый будущий слой должен получить один из статусов:

- REUSE
- EXTEND
- BIND
- CREATE
- DO_NOT_TOUCH

---

## 1. Принятые стабильные слои

### 1.1 Memory Foundation Inspector

Status: REUSE

Existing surface:
- MAKSIMAR_CORE_LIB/memory_engine/foundation_inspector/
- MAKSIMAR_SERVER/OBSERVABILITY/memory_skill_metrics/foundation_inspector_*
- tests/memory_engine/test_foundation_inspector_*

Decision:
- переиспользовать как read-only entry point;
- не переписывать;
- будущие memory preview/read-models подключать через существующий inspector / memory_skill_metrics.

Next action:
- BIND будущие memory read models через существующие summary/read-model слои.

---

### 1.2 History Ingestion / Project History Store

Status: REUSE + DO_NOT_TOUCH except binding

Existing surface:
- MAKSIMAR_CORE_LIB/memory_engine/history_ingestion/
- runtime_history_store/
- docs/jarvis_internal/history_import/

Known capabilities:
- archive parsing;
- source adapters;
- fingerprint / dedup;
- import session manifests;
- normalized history;
- memory objects;
- memory IDs;
- storage nodes;
- relation graph;
- timeline;
- panel projection;
- traceability;
- attachment linkage;
- message attachment candidate linkage;
- Jarvis read/query layer;
- portable storage / NAS readiness;
- history store acceptance.

Decision:
- не переписывать;
- не создавать второй graph;
- не создавать второй timeline;
- не создавать второй storage identity layer;
- не создавать второй MemoryObject model;
- разрешён только thin binding.

Next action:
- PHASE 1 создаёт тонкий History Binding поверх существующего history_ingestion.

---

## 2. Manifest / ID / Registry

### 2.1 Module Manifest

Status: EXTEND

Existing surface:
- MAKSIMAR_CORE_LIB/module_manifest/
- MAKSIMAR_CORE_LIB/module_manifest/module_manifest_schema.py
- tests/module_manifest/

Decision:
- не создавать второй manifest subsystem;
- расширять существующую schema только при необходимости;
- связать manifest с memory/skill/domain enrollment.

Next action:
- PHASE 1.1 = EXTEND existing module_manifest.

---

### 2.2 Canonical ID Generation

Status: EXTEND

Existing surface:
- MAKSIMAR_CORE_LIB/id_generation/
- MAKSIMAR_CORE_LIB/id_generation/canonical_id_generation.py

Decision:
- не создавать второй allocator;
- расширять существующий canonical ID generation под:
  - module_id
  - skill_id
  - domain_id
  - cube_id
  - storage_node_id
  - retrieval_source_id
  - dashboard_panel_id
  - artifact_ref
  - trace_id

Next action:
- PHASE 1.2 = EXTEND existing id_generation.

---

### 2.3 Memory Registry

Status: EXTEND + BIND

Existing surface:
- MAKSIMAR_SERVER/MEMORY_REGISTRY/
- MAKSIMAR_CORE_LIB/memory_engine/memory_registry.py

Decision:
- не создавать новый MEMORY_REGISTRY root;
- привязать memory domains, storage nodes, retrieval sources и dashboard exposure к существующему registry.

Next action:
- PHASE 1.3 = EXTEND / BIND existing MEMORY_REGISTRY.

---

### 2.4 Registry Auto-Enrollment

Status: EXTEND

Existing surface:
- MAKSIMAR_SERVER/REGISTRY_AUTO_ENROLLMENT/

Decision:
- не создавать второй auto-enrollment;
- расширять существующий REGISTRY_AUTO_ENROLLMENT;
- initial existing domain enrollment должен быть preview-first, а не write-first.

Required flow:
discover -> candidate -> preview -> approval -> enroll

Forbidden flow:
discover -> silently write manifests everywhere

Next action:
- PHASE 1.4 = EXTEND existing REGISTRY_AUTO_ENROLLMENT;
- добавить preview для initial existing domain enrollment.

---

## 3. Existing domain surfaces for enrollment

### 3.1 Domain Cubes

Status: ENROLLMENT_CANDIDATE

Existing surfaces:
- DOMAIN_CUBES/3d_cube/
- DOMAIN_CUBES/automation_cube/
- DOMAIN_CUBES/compute_fleet_cube/
- DOMAIN_CUBES/content_cube/
- DOMAIN_CUBES/desktop_assistant_cube/
- DOMAIN_CUBES/education_cube/
- DOMAIN_CUBES/energy_cube/
- DOMAIN_CUBES/engineering_assistant/
- DOMAIN_CUBES/family_assistant/
- DOMAIN_CUBES/industrial_cube/
- DOMAIN_CUBES/knowledge_assistant/
- DOMAIN_CUBES/mobile_assistant_cube/
- DOMAIN_CUBES/module_templates/
- DOMAIN_CUBES/robotics_cube/
- DOMAIN_CUBES/visual_engineering_cube/
- DOMAIN_CUBES/vpn_cube/

Decision:
- логику кубиков сейчас не реализуем;
- регистрируем как существующие domain/cube surfaces;
- позже каждый cube получает manifest, canonical ID, registry entry, memory binding, retrieval binding, dashboard exposure и observability binding.

Next action:
- PHASE 1.4 initial existing domain enrollment preview должен включать все DOMAIN_CUBES.

---

### 3.2 Engineering / Physical / Media / Workflow Layers

Status: ENROLLMENT_CANDIDATE + CONFIG_SURFACE

Existing surfaces:
- CAD_3D_CAM_LAYER/
- ROBOTICS_LAYER/
- SIMULATION_LAYER/
- INDUSTRIAL_LAYER/
- ENERGY_OPERATIONS_LAYER/
- CONTENT_MEDIA_LAYER/
- VISUAL_ENGINEERING_LAYER/
- VOICE_LAYER/
- COMPUTE_FLEET_LAYER/
- RESEARCH_LAYER/
- VPN_LAYER/
- ACTION_LIBRARY/
- WORKFLOW_ENGINE/
- AI_SERVICES/

Decision:
- это не пустые папки;
- большинство имеют README.md и config/*.yaml;
- учитывать как config-driven domain surfaces;
- не исполнять эти слои в memory-track.

Next action:
- PHASE 1.4 preview должен включать эти слои как existing surfaces.

---

### 3.3 Shell / Client Adapters

Status: ENROLLMENT_CANDIDATE

Existing surfaces:
- ANDROID_SHELL/memory_adapter/
- ANDROID_SHELL/knowledge_adapter/
- IOS_SHELL/memory_adapter/
- IOS_SHELL/knowledge_adapter/
- DESKTOP_SHELL/
- SERVER_SHELL/
- MAKSIMAR_CORE_LIB/mobile_bridge/

Decision:
- root-level mobile_bridge не создавать;
- использовать existing MAKSIMAR_CORE_LIB/mobile_bridge.

Next action:
- включить shell/client adapters в initial enrollment preview.

---

## 4. Dashboard / Display / Explainability

### 4.1 Dashboard Read-Only Views

Status: EXTEND + BIND

Existing surface:
- MAKSIMAR_SERVER/DASHBOARD_READ_ONLY_VIEWS/

Decision:
- не создавать второй dashboard read model root;
- future memory/dashboard exposure должен подключаться к этому слою.

---

### 4.2 Display Orchestration

Status: EXTEND + BIND later

Existing surface:
- MAKSIMAR_SERVER/DISPLAY_ORCHESTRATION/

Decision:
- сейчас не трогать;
- display orchestration идёт позже registry-backed exposure.

---

### 4.3 Explainable View Binding

Status: EXTEND + BIND later

Existing surface:
- MAKSIMAR_SERVER/EXPLAINABLE_VIEW_BINDING/

Decision:
- не создавать второй explainability surface;
- memory views подключать позже.

---

### 4.4 OOB Dashboard / Panel / View / Display Contracts

Status: REUSE + DO_NOT_DUPLICATE

Existing surface:
- MAKSIMAR_CORE_LIB/oob_dashboard/

Decision:
- panel/view/display/workspace/preview/operator contracts уже существуют;
- future memory visualization должна переиспользовать эти contracts;
- новый dashboard root не создавать.

---

## 5. Storage / Data Plane / Artifact Surfaces

### 5.1 Artifact Reference

Status: REUSE + BIND

Existing surface:
- MAKSIMAR_CORE_LIB/artifact_reference_models.py
- MAKSIMAR_CORE_LIB/data_plane/
- MAKSIMAR_SERVER/EXECUTION_CONTROL/artifact_routing/
- MAKSIMAR_CORE_LIB/persistent_storage_migrations/

Decision:
- не создавать несвязанный artifact reference model;
- storage/artifact/model/media memory должен использовать existing artifact/data-plane surfaces.

---

### 5.2 Model Weights / Media / Generated Artifacts

Status: BIND / CREATE_METADATA_ONLY

Decision:
- model weights не являются text memory;
- generated images/video/audio являются artifacts;
- RAG индексирует metadata/evidence, а не тяжёлые binary-файлы.

Future physical layout:
- DATA_PLANE/model_store/
- DATA_PLANE/artifacts/
- DATA_PLANE/retrieval_indexes/

Physical implementation later.

---

## 6. Retrieval / RAG / Vector Backend

### 6.1 Memory + Knowledge Retrieval

Status: EXTEND + BIND

Existing surfaces:
- MAKSIMAR_CORE_LIB/memory_engine/query_models.py
- MAKSIMAR_CORE_LIB/memory_engine/retrieval_summary.py
- MAKSIMAR_CORE_LIB/knowledge_engine/query_models.py
- MAKSIMAR_CORE_LIB/knowledge_engine/retrieval_summary.py
- MAKSIMAR_CORE_LIB/ai_services/

Decision:
- RAG не создавать как одну огромную папку;
- создать retrieval orchestration поверх existing memory/knowledge layers.

---

### 6.2 sqlite-vec

Status: OPTIONAL_RETRIEVAL_BACKEND_LATER

Decision:
- полезен как локальный vector backend;
- не canonical memory;
- не registry;
- не evidence truth;
- не replacement for MemPalace.

Correct placement:
retrieval backend adapter -> sqlite_vec_adapter

Activation phase:
- after Retrieval Orchestration contracts are stable.

---

### 6.3 MemPalace

Status: OPTIONAL_BACKEND_LATER

Decision:
- только для conversational/project notes memory;
- запрещён для constitutional/regulatory/policy/technical/audit truth.

---

## 7. Workers / AI Services / Small LLM Helpers

Status: ENROLLMENT_CANDIDATE + FUTURE_BINDING

Existing surfaces:
- MAKSIMAR_CORE_LIB/ai_services/
- MAKSIMAR_CORE_LIB/real_ai_services_model_adapters/
- MAKSIMAR_CORE_LIB/real_engine_backends/
- MAKSIMAR_CORE_LIB/workers_registry/
- MAKSIMAR_CORE_LIB/workers_runtime/
- MAKSIMAR_SERVER/WORKERS/

Decision:
- small LLM helpers / workers должны получить manifest + ID + registry + model/backend binding;
- сейчас не реализуем;
- после enrollment они должны быть видимы в dashboard.

Future flow:
worker/LLM adapter -> manifest -> canonical ID -> workers_registry / ai_services -> memory/retrieval binding -> dashboard exposure -> observability binding

---

## 8. Network / VPN / Internal Ecosystem Chat

Status: ENROLLMENT_CANDIDATE / FUTURE_FEATURE

Existing surface:
- VPN_LAYER/
- tests/network_trust_boundaries/

Decision:
- VPN и internal ecosystem chat сейчас не реализуем;
- включаем их как visible project surfaces;
- implementation = отдельный future security/network track.

---

## 9. PHASE 0.6 final decision

Current next action:
PHASE 0.6 accepted as documentation / reuse matrix baseline.

Allowed next implementation:
PHASE 1 — History Binding / Reuse Pass

Forbidden before PHASE 1:
- creating new manifests everywhere;
- creating new ID allocator;
- creating new memory graph;
- creating new dashboard root;
- touching history_ingestion internals;
- touching runtime_history_store;
- touching frontend;
- touching CORE_ROOT / SUPERVISOR / RUNTIME.
