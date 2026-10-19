from __future__ import annotations

"""Bounded local browser provider.

Playwright is an implementation provider below the canonical Browser Organ.  It
is deliberately executed in the dedicated browser-tooling runtime and returns
only typed DOM observations; it is not a semantic planner or policy owner.
"""

import hashlib
import json
import os
import subprocess
import ipaddress
import socket
from dataclasses import dataclass
from pathlib import Path
from urllib.parse import urlparse

from MAKSIMAR_CORE_LIB.ai_orchestration.semantic_intent_contract import (
    EvidenceBundle, EvidenceItem, ExecutionPlan, ExecutionReceipt,
    PermissionDecision, RequestDeadline, RequestUnderstanding, utc_observed_at,
)

PROVIDER_ID = "browser_playwright_provider"
BROWSER_PYTHON = Path(os.environ.get(
    "JARVIS_BROWSER_PYTHON",
    "/home/aleksandr/MAKSIMAR_RUNTIME/venvs/browser_tooling/bin/python",
))
BROWSER_CAPABILITY = "browser.web"

BROWSER_OPERATION_CONTRACTS = {
    "browser.open_read": {"evidence_kind": "browser_page_opened", "risk": "READ_ONLY", "required_parameters": ("url",), "effect_type": "OBSERVE", "description": "Open a web URL and read page title and visible content; not an OS browser-window action."},
    "browser.navigate": {"evidence_kind": "browser_navigation", "risk": "READ_ONLY", "required_parameters": (), "effect_type": "OBSERVE", "description": "Follow a uniquely resolved link or requested page navigation within web content and read the resulting DOM; DOM locators are provider-private."},
    "browser.fill_submit": {"evidence_kind": "browser_action_result", "risk": "MUTATION", "required_parameters": ("value",), "effect_type": "MUTATE", "reversibility": "UNKNOWN", "external_side_effect": True, "description": "Perform a bounded authorized interaction with a uniquely resolved web form field and action; DOM locators are provider-private."},
}

BROWSER_CAPABILITY_OPERATION_CONTRACTS = {
    BROWSER_CAPABILITY: tuple({
        "operation_id": operation,
        "description": meta["description"],
        "required_parameters": meta["required_parameters"],
        "evidence_kinds": (meta["evidence_kind"],),
        "effect_type": meta["effect_type"], "target_scope": "public_browser_dom",
        "semantic_owner_id": BROWSER_CAPABILITY,
        "external_side_effect": bool(meta.get("external_side_effect", False)), "risk_class": meta["risk"],
        "reversibility": str(meta.get("reversibility", "REVERSIBLE")),
    } for operation, meta in BROWSER_OPERATION_CONTRACTS.items())
}


def _canonical_web_url(value: str) -> str:
    """Normalize a supplied scheme-less web address; never infer its host from context."""
    value = value.strip()
    parsed = urlparse(value)
    if not parsed.scheme and not any(c.isspace() for c in value):
        return 'https:' + value if value.startswith('//') else 'https://' + value
    return value


def _url_allowed(value: str, *, mode: str = "PUBLIC_READ") -> bool:
    parsed = urlparse(value)
    if parsed.username or parsed.password or parsed.scheme not in {"http", "https"} or not parsed.hostname:
        return False
    host = parsed.hostname.lower()
    if mode == "LOCAL_TEST":
        return parsed.scheme == "http" and host in {"localhost", "127.0.0.1", "::1"}
    if host in {"localhost", "127.0.0.1", "::1"}:
        return False
    if parsed.scheme != "https":
        return False
    try:
        addresses = {item[4][0] for item in socket.getaddrinfo(host, 443, type=socket.SOCK_STREAM)}
        return bool(addresses) and all(not (ipaddress.ip_address(addr).is_private or ipaddress.ip_address(addr).is_loopback or ipaddress.ip_address(addr).is_link_local) for addr in addresses)
    except (OSError, ValueError):
        return False


@dataclass(frozen=True, slots=True)
class HostBrowserAuthorization:
    """Opaque host-issued approval; planner parameters cannot construct this."""
    approved_step_ids: frozenset[str] = frozenset()

    def permits(self, step_id: str) -> bool:
        return step_id in self.approved_step_ids


class ExistingPlaywrightBrowserAdapter:
    provider_id = PROVIDER_ID

    def __init__(self, authorization: HostBrowserAuthorization | None = None,
                 permission_decision: PermissionDecision | None = None,
                 *, policy_mode: str = "PUBLIC_READ"):
        self._authorization = authorization or HostBrowserAuthorization()
        self._permission_decision = permission_decision
        self._permission_decisions: dict[str, PermissionDecision] = {}
        self._policy_mode = policy_mode if policy_mode in {"PUBLIC_READ", "LOCAL_TEST"} else "PUBLIC_READ"

    def bind_host_permission(self, *, permissions: tuple[PermissionDecision, ...],
                             plan: ExecutionPlan, trace_id: str) -> None:
        """Derive the opaque step scope from HOST PermissionDecision results.

        This is called only by the canonical execution spine; planner parameters
        are never consulted when minting the provider-local authorization scope.
        """
        approved = frozenset(
            step.step_id for step in plan.steps
            for decision in permissions
            if step.operation == decision.operation_id == "browser.fill_submit"
            and decision.granted and decision.trace_id == trace_id
            and decision.capability_id == step.capability_id
            and decision.step_id == step.step_id
        )
        self._permission_decisions = {
            decision.step_id: decision for decision in permissions
            if decision.granted and decision.trace_id == trace_id
            and decision.capability_id == BROWSER_CAPABILITY
            and decision.operation_id == "browser.fill_submit"
            and decision.step_id in approved
        }
        self._permission_decision = next(iter(self._permission_decisions.values()), None)
        self._authorization = HostBrowserAuthorization(approved)

    def health(self) -> dict[str, object]:
        if not BROWSER_PYTHON.is_file():
            return {"provider_id": self.provider_id, "status": "UNAVAILABLE", "reason": "runtime_missing"}
        try:
            probe = subprocess.run(
                [str(BROWSER_PYTHON), "-c", "import playwright; print('ok')"],
                capture_output=True, text=True, timeout=5, check=False,
            )
        except (OSError, subprocess.SubprocessError):
            return {"provider_id": self.provider_id, "status": "UNAVAILABLE", "reason": "runtime_unreachable"}
        return {"provider_id": self.provider_id, "status": "AVAILABLE" if probe.returncode == 0 else "UNAVAILABLE", "runtime_python": str(BROWSER_PYTHON), "readback": "DOM"}

    @staticmethod
    def _script(steps: list[dict[str, object]]) -> str:
        # The child imports Playwright only in its dedicated owner runtime.
        return """import json, sys, ipaddress, socket
from urllib.parse import urlparse
from playwright.sync_api import sync_playwright
steps=json.loads(sys.argv[1])
out=[]
def allowed(u):
    x=urlparse(u)
    if x.username or x.password or x.scheme not in ('http','https') or not x.hostname: return False
    if x.hostname in ('localhost','127.0.0.1','::1'): return x.scheme == 'http' and sys.argv[2] == 'LOCAL_TEST'
    if x.scheme != 'https': return False
    try:
        ips={a[4][0] for a in socket.getaddrinfo(x.hostname,443,type=socket.SOCK_STREAM)}
        return bool(ips) and all(not (ipaddress.ip_address(a).is_private or ipaddress.ip_address(a).is_loopback or ipaddress.ip_address(a).is_link_local or ipaddress.ip_address(a).is_multicast or ipaddress.ip_address(a).is_reserved or ipaddress.ip_address(a).is_unspecified) for a in ips)
    except Exception: return False
with sync_playwright() as p:
    browser=p.chromium.launch(headless=True)
    context=browser.new_context()
    page=context.new_page()
    page.route('**/*', lambda route: route.abort() if not allowed(route.request.url) else route.continue_())
    try:
        for step in steps:
            op=step['operation']; prm=step['parameters']
            if op == 'browser.fill_submit' and prm.get('url'):
                page.goto(prm['url'], wait_until='domcontentloaded', timeout=5000)
            if op == 'browser.open_read':
                page.goto(prm['url'], wait_until='domcontentloaded', timeout=5000)
                if not (page.url.startswith('http://127.0.0.1') or page.url.startswith('http://localhost') or page.url.startswith('https://')):
                    raise RuntimeError('redirect_target_rejected')
                out.append({'title':page.title(), 'url':page.url, 'text':page.locator('body').inner_text(timeout=3000)[:4000]})
            elif op == 'browser.navigate':
                links = page.locator("a:visible")
                if links.count() != 1:
                    raise RuntimeError('browser_target_ambiguous')
                links.first.click(timeout=3000)
                page.wait_for_load_state('domcontentloaded', timeout=5000)
                out.append({'title':page.title(), 'url':page.url, 'text':page.locator('body').inner_text(timeout=3000)[:4000]})
            elif op == 'browser.fill_submit':
                inputs = page.locator("input:not([type=hidden]):not([type=submit])")
                buttons = page.locator("button, input[type=submit]")
                if inputs.count() != 1 or buttons.count() != 1:
                    raise RuntimeError('browser_target_ambiguous')
                inputs.first.fill(prm['value'], timeout=3000)
                buttons.first.click(timeout=3000)
                page.wait_for_timeout(50)
                out.append({'title':page.title(), 'url':page.url, 'text':page.locator('body').inner_text(timeout=3000)[:4000], 'value':inputs.first.input_value(timeout=3000)})
            else:
                raise RuntimeError('unsupported_operation:'+op)
    finally:
        context.close(); browser.close()
print(json.dumps(out, ensure_ascii=False, sort_keys=True))
"""

    def collect_evidence(self, understanding: RequestUnderstanding, plan: ExecutionPlan,
                         trace_id: str, deadline: RequestDeadline | None = None) -> EvidenceBundle:
        items: list[EvidenceItem] = []
        receipts: list[ExecutionReceipt] = []
        errors: list[str] = []
        child_steps: list[dict[str, object]] = []
        valid_steps = []
        for step in plan.steps:
            contract = BROWSER_OPERATION_CONTRACTS.get(step.operation)
            params = dict(step.parameters)
            if contract is None or step.capability_id != BROWSER_CAPABILITY:
                errors.append(f"{step.operation}:unsupported_operation")
                continue
            url = params.get("url", "")
            if url:
                url = _canonical_web_url(url)
                params['url'] = url
            if url and not _url_allowed(url, mode=self._policy_mode):
                errors.append(f"{step.operation}:url_policy_denied")
                continue
            if contract["risk"] == "MUTATION":
                decision = self._permission_decisions.get(step.step_id, self._permission_decision)
                decision_ok = (
                    decision is not None and decision.granted
                    and decision.capability_id == step.capability_id
                    and decision.operation_id == step.operation
                    and decision.step_id == step.step_id
                    and decision.trace_id == trace_id
                )
                if not decision_ok or not self._authorization.permits(step.step_id):
                    errors.append(f"{step.operation}:host_authorization_required")
                    continue
            if contract["risk"] == "MUTATION":
                params.pop("authorization", None)
            child_steps.append({"operation": step.operation, "parameters": params})
            valid_steps.append(step)
        if child_steps and BROWSER_PYTHON.is_file() and not errors:
            remaining = deadline.remaining() if deadline is not None else 20.0
            env = dict(os.environ)
            env["PYTHONPATH"] = str(Path(__file__).resolve().parents[2])
            try:
                run = subprocess.run(
                    [str(BROWSER_PYTHON), "-c", self._script(child_steps), json.dumps(child_steps), self._policy_mode],
                    capture_output=True, text=True, timeout=min(20.0, max(0.1, remaining)), check=False, env=env,
                )
                if run.returncode != 0:
                    raise RuntimeError(run.stderr.strip()[-400:] or "playwright_failed")
                observations = json.loads(run.stdout)
                if not isinstance(observations, list) or len(observations) != len(valid_steps):
                    raise RuntimeError("playwright_readback_missing")
                for step, result in zip(valid_steps, observations):
                    observation = json.dumps(result, ensure_ascii=False, sort_keys=True)
                    items.append(EvidenceItem(
                        kind=BROWSER_OPERATION_CONTRACTS[step.operation]["evidence_kind"],
                        source=f"{self.provider_id}:{step.operation}", observation=observation,
                        scope=("public_browser_dom" if self._policy_mode == "PUBLIC_READ" else "localhost_browser_dom"), confidence=1.0, trace_id=trace_id,
                        observed_at=utc_observed_at(), content_hash="sha256:" + hashlib.sha256(observation.encode()).hexdigest(),
                        source_reference=str(result.get("url", "localhost")), request_id=understanding.request_id,
                        step_id=step.step_id, capability_id=step.capability_id, operation_id=step.operation,
                        provider_id=self.provider_id,
                    ))
                    receipts.append(ExecutionReceipt(
                        receipt_id=f"{trace_id}:{step.step_id}", request_id=understanding.request_id,
                        trace_id=trace_id, step_id=step.step_id, capability_id=step.capability_id,
                        operation_id=step.operation, provider_id=self.provider_id, status="COMPLETE",
                        result="Playwright completed bounded DOM operation with post-action readback",
                    ))
            except (OSError, subprocess.SubprocessError, TimeoutError, ValueError, RuntimeError, json.JSONDecodeError) as exc:
                errors.append(f"playwright:{type(exc).__name__}:{exc}")
        elif not child_steps and not errors:
            errors.append("browser:runtime_or_plan_precondition_required")
        status = "COMPLETE" if items and not errors else "PARTIAL" if items else "UNAVAILABLE"
        return EvidenceBundle(
            request_id=understanding.request_id, capability_id=BROWSER_CAPABILITY, trace_id=trace_id,
            status=status, items=tuple(items), limitations=(() if status == "COMPLETE" else ("browser operation incomplete",)),
            receipts=tuple(receipts), errors=tuple(errors), capability_ids=(BROWSER_CAPABILITY,),
        )


__all__ = ["ExistingPlaywrightBrowserAdapter", "HostBrowserAuthorization", "BROWSER_CAPABILITY", "BROWSER_OPERATION_CONTRACTS", "BROWSER_CAPABILITY_OPERATION_CONTRACTS", "PROVIDER_ID"]
