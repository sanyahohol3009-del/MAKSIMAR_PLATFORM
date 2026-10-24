from __future__ import annotations

import json

from MAKSIMAR_CORE_LIB.action_library_adapters.action_worker_status_read_model import (
    build_action_worker_status_read_model,
)
from MAKSIMAR_CORE_LIB.action_library_adapters.computer_use_worker_contract import (
    resolve_computer_use_action_request,
)
from MAKSIMAR_CORE_LIB.ai_orchestration.semantic_intent_contract import PlanStep
from MAKSIMAR_SERVER.WORKERS.sandboxed_action_worker_runtime import run_sandboxed_action_worker
from MAKSIMAR_CORE_LIB.security_layer.owner_identity_claim import build_owner_identity_claim_for_terminal


def build_action_worker_status_preview() -> dict[str, object]:
    request = resolve_computer_use_action_request(
        PlanStep("preview-step", "preview-goal", "pc.control", "open_browser", ("execution_receipt",),
                 "MUTATE", "local_pc", "REVERSIBLE", True, "MUTATION"),
        target="default_browser",
        input_channel="text",
        owner_identity_claim=build_owner_identity_claim_for_terminal(),
    )
    if request is None:
        raise RuntimeError("action request preview could not be built")
    return build_action_worker_status_read_model(run_sandboxed_action_worker(request)).to_read_model()


def main() -> int:
    print(json.dumps(build_action_worker_status_preview(), indent=2, ensure_ascii=False))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
