from __future__ import annotations

from dataclasses import dataclass
from typing import Literal, Tuple


CodegenIntentKind = Literal[
    "bugfix_proposal",
    "contract_extension_proposal",
    "test_extension_proposal",
    "documentation_update_proposal",
    "refactor_proposal",
]

CodegenRiskClass = Literal[
    "low",
    "medium",
    "high",
    "blocked",
]


@dataclass(frozen=True, slots=True)
class CodegenIntentEntry:
    intent_id: str
    intent_kind: CodegenIntentKind
    risk_class: CodegenRiskClass
    proposal_required: bool
    audit_required: bool
    approval_required: bool
    sandbox_required_later: bool
    direct_write_allowed: bool
    deploy_allowed: bool
    intent_ready: bool

    def __post_init__(self) -> None:
        if not self.intent_id:
            raise ValueError("intent_id must be non-empty")
        if self.proposal_required is not True:
            raise ValueError("proposal_required must be True")
        if self.audit_required is not True:
            raise ValueError("audit_required must be True")
        if self.approval_required is not True:
            raise ValueError("approval_required must be True")
        if self.sandbox_required_later is not True:
            raise ValueError("sandbox_required_later must be True")
        if self.direct_write_allowed:
            raise ValueError("direct_write_allowed must be False")
        if self.deploy_allowed:
            raise ValueError("deploy_allowed must be False")
        if self.intent_ready is not True:
            raise ValueError("intent_ready must be True")


@dataclass(frozen=True, slots=True)
class CodegenIntentContract:
    contract_id: str
    intents: Tuple[CodegenIntentEntry, ...]
    proposal_required_for_all: bool
    audit_required_for_all: bool
    approval_required_for_all: bool
    sandbox_required_later_for_all: bool
    direct_write_allowed: bool
    deploy_allowed: bool
    intent_contract_ready: bool

    def __post_init__(self) -> None:
        if not self.contract_id:
            raise ValueError("contract_id must be non-empty")
        if not self.intents:
            raise ValueError("intents must be non-empty")
        intent_ids = {intent.intent_id for intent in self.intents}
        if len(intent_ids) != len(self.intents):
            raise ValueError("intent_id values must be unique")
        if self.proposal_required_for_all is not True:
            raise ValueError("proposal_required_for_all must be True")
        if self.audit_required_for_all is not True:
            raise ValueError("audit_required_for_all must be True")
        if self.approval_required_for_all is not True:
            raise ValueError("approval_required_for_all must be True")
        if self.sandbox_required_later_for_all is not True:
            raise ValueError("sandbox_required_later_for_all must be True")
        if self.direct_write_allowed:
            raise ValueError("direct_write_allowed must be False")
        if self.deploy_allowed:
            raise ValueError("deploy_allowed must be False")
        if not all(intent.intent_ready for intent in self.intents):
            raise ValueError("all intents must be ready")
        if self.intent_contract_ready is not True:
            raise ValueError("intent_contract_ready must be True")


def build_codegen_intent_contract() -> CodegenIntentContract:
    intents = (
        CodegenIntentEntry(
            intent_id="codegen_intent_bugfix_proposal",
            intent_kind="bugfix_proposal",
            risk_class="medium",
            proposal_required=True,
            audit_required=True,
            approval_required=True,
            sandbox_required_later=True,
            direct_write_allowed=False,
            deploy_allowed=False,
            intent_ready=True,
        ),
        CodegenIntentEntry(
            intent_id="codegen_intent_contract_extension_proposal",
            intent_kind="contract_extension_proposal",
            risk_class="medium",
            proposal_required=True,
            audit_required=True,
            approval_required=True,
            sandbox_required_later=True,
            direct_write_allowed=False,
            deploy_allowed=False,
            intent_ready=True,
        ),
        CodegenIntentEntry(
            intent_id="codegen_intent_test_extension_proposal",
            intent_kind="test_extension_proposal",
            risk_class="low",
            proposal_required=True,
            audit_required=True,
            approval_required=True,
            sandbox_required_later=True,
            direct_write_allowed=False,
            deploy_allowed=False,
            intent_ready=True,
        ),
        CodegenIntentEntry(
            intent_id="codegen_intent_documentation_update_proposal",
            intent_kind="documentation_update_proposal",
            risk_class="low",
            proposal_required=True,
            audit_required=True,
            approval_required=True,
            sandbox_required_later=True,
            direct_write_allowed=False,
            deploy_allowed=False,
            intent_ready=True,
        ),
        CodegenIntentEntry(
            intent_id="codegen_intent_refactor_proposal",
            intent_kind="refactor_proposal",
            risk_class="high",
            proposal_required=True,
            audit_required=True,
            approval_required=True,
            sandbox_required_later=True,
            direct_write_allowed=False,
            deploy_allowed=False,
            intent_ready=True,
        ),
    )

    return CodegenIntentContract(
        contract_id="codegen_intent_contract_phase_6_3_001",
        intents=intents,
        proposal_required_for_all=all(intent.proposal_required for intent in intents),
        audit_required_for_all=all(intent.audit_required for intent in intents),
        approval_required_for_all=all(intent.approval_required for intent in intents),
        sandbox_required_later_for_all=all(intent.sandbox_required_later for intent in intents),
        direct_write_allowed=False,
        deploy_allowed=False,
        intent_contract_ready=True,
    )
