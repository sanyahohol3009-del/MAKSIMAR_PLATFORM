# 07. History Import Acceptance and Corrective Pass

## Purpose
This document defines the acceptance conditions and corrective-pass rules for the history import track.

## Acceptance Conditions Already Confirmed
The following conditions are already confirmed for export #1:

- live import foundation built;
- project write completed;
- incremental reimport safety confirmed;
- attachment root linkage confirmed;
- message candidate attachment linkage confirmed;
- history store acceptance confirmed.

## Confirmed Acceptance Values
The current accepted values are:
- session_manifest_count = 1
- attachment_summary_count = 1
- conversation_manifest_count = 18
- normalized_record_count = 18
- message_unit_count = 11822
- store_acceptance_ready = True

## Meaning of Acceptance
Acceptance means:
- the imported history store is structurally valid;
- the counts are internally consistent;
- the layer is readable by JARVIS;
- the layer is stable enough to pause until export #2 arrives.

Acceptance does not mean:
- the layer may never be improved;
- the current candidate linkage is the final highest-fidelity linkage;
- corrective work is forbidden.

## Corrective Pass Rule
Corrective passes are allowed when they:
- reduce drift;
- improve determinism;
- improve consistency between preview / summary / writer / store;
- improve fidelity of message or attachment linkage;
- preserve the current valid storage topology.

## Forbidden Corrective Passes
Corrective passes must not:
- create a second storage world;
- silently rewrite accepted conversation buckets without justification;
- break repeat-safe import;
- move history import out of the current history_ingestion domain.

## Track Closure Condition Before Export #2
The current history import track may be considered closed before export #2 if:
- tests stay green;
- store acceptance remains valid;
- internal docs are complete;
- no unresolved drift remains in the current architecture.

## Reopening Condition
The track reopens when one of the following happens:
- export #2 arrives;
- richer payload import is started;
- exact attachment-to-message linkage is introduced;
- a corrective pass is explicitly scheduled.
