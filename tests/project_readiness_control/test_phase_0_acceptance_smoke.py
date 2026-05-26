from __future__ import annotations

import subprocess
import sys
from pathlib import Path


PHASE_0_ACCEPTANCE_DOC = Path(
    "docs/architecture/foundation/phase_0_readiness_output_hygiene_acceptance_v1.md"
)

EXPECTED_BATCHES = (
    "0.1 — Existing Scanner Discovery",
    "0.2 — Repository Scan Models",
    "0.3 — Repository Scan Runtime",
    "0.4 — Pytest Output Hygiene",
    "0.5 — Project Readiness Runner Core",
    "0.6 — Project Readiness Sub-Runners",
    "0.7 — Readiness Runtime JSON + Dashboard Export",
    "0.8 — PHASE 0 Acceptance",
)


def test_phase_0_acceptance_document_records_required_gates() -> None:
    text = PHASE_0_ACCEPTANCE_DOC.read_text(encoding="utf-8")

    assert "Status: accepted after Batch 0.8." in text
    assert "no duplicate scanner world" in text
    assert "no duplicate roadmap checker" in text
    assert "no duplicate drift checker" in text
    assert "no duplicate X-Ray engine" in text
    assert "no duplicate semantic duplicate engine" in text
    assert "no dashboard mutation" in text
    assert "no UI-to-execution path" in text
    assert "Target pytest runs remain quiet by default." in text
    assert "MAKSIMAR_FULL_PLATFORM_REPORTS=1" in text
    assert "--maksimar-full-platform-reports" in text


def test_phase_0_full_readiness_map_is_ready() -> None:
    completed = subprocess.run(
        (
            sys.executable,
            "tools/project_readiness_control/project_file_readiness_map.py",
        ),
        text=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        check=False,
        shell=False,
    )

    assert completed.returncode == 0, completed.stderr
    assert "MAKSIMAR PROJECT FILE READINESS MAP" in completed.stdout
    assert "status=READY" in completed.stdout
    assert "total_batches=8" in completed.stdout
    assert "ready_batches=8" in completed.stdout
    assert "partial_batches=0" in completed.stdout
    assert "missing_batches=0" in completed.stdout

    for batch in EXPECTED_BATCHES:
        assert batch in completed.stdout
