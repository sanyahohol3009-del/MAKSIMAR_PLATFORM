from __future__ import annotations

from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
import threading
import pytest

from MAKSIMAR_CORE_LIB.ai_orchestration.semantic_intent_contract import (
    CapabilityRequirement, ExecutionPlan, Goal, PlanStep, RequestUnderstanding, PermissionDecision,
)
from MAKSIMAR_SERVER.AI_ORCHESTRATION.browser_provider_adapter import ExistingPlaywrightBrowserAdapter, HostBrowserAuthorization
from MAKSIMAR_SERVER.AI_ORCHESTRATION.browser_provider_adapter import BROWSER_OPERATION_CONTRACTS


@pytest.mark.parametrize('source,expected', [
    ('example.org','https://example.org'),
    ('example.org/path?q=1','https://example.org/path?q=1'),
    ('//example.org/path','https://example.org/path'),
    ('http://127.0.0.1/','http://127.0.0.1/'),
    ('javascript:alert(1)','javascript:alert(1)'),
])
def test_web_address_normalization_preserves_target_and_does_not_rewrite_explicit_scheme(source,expected):
    from MAKSIMAR_SERVER.AI_ORCHESTRATION.browser_provider_adapter import _canonical_web_url
    assert _canonical_web_url(source)==expected


def test_normalized_bare_private_host_remains_denied():
    from MAKSIMAR_SERVER.AI_ORCHESTRATION.browser_provider_adapter import _canonical_web_url,_url_allowed
    assert not _url_allowed(_canonical_web_url('127.0.0.1/private'))


def test_public_browser_contract_hides_provider_private_locators():
    for operation in ("browser.navigate", "browser.fill_submit"):
        required = set(BROWSER_OPERATION_CONTRACTS[operation]["required_parameters"])
        assert not required.intersection({"selector", "input_selector", "submit_selector", "css_selector", "xpath", "playwright_locator"})


class _FixtureHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        if self.path == "/b":
            body = b"<title>Page B</title><h1>Second page</h1><p>JARVIS_BROWSER_PROOF_42</p>"
        else:
            body = (b"<title>Page A</title><h1>Local Browser Proof</h1><p>Read and act locally.</p>"
                    b"<a id='next' href='/b'>Page B</a><form><input id='value'><button id='submit' type='button' "
                    b"onclick=\"document.getElementById('status').textContent='submitted:'+document.getElementById('value').value\">Submit</button>"
                    b"<div id='status'>idle</div></form>")
        self.send_response(200); self.send_header("Content-Type", "text/html"); self.end_headers(); self.wfile.write(body)
    def log_message(self, *_args):
        return


def _fixture():
    server = ThreadingHTTPServer(("127.0.0.1", 0), _FixtureHandler)
    thread = threading.Thread(target=server.serve_forever, daemon=True); thread.start()
    return server, f"http://127.0.0.1:{server.server_port}/"


def _understanding():
    return RequestUnderstanding(
        request_id="browser_test", original_text="open local proof page", language="en",
        goals=(Goal("g1", "inspect local page"),),
        required_capabilities=(CapabilityRequirement("browser.web", "local DOM", True),),
        effect_type="MUTATE", target_scope="localhost_browser", reversibility="REVERSIBLE",
        external_side_effect=False, unresolved_capabilities=(), operation_requirements=(),
        current_topic="browser", unresolved_reference="", relevant_context_trace_ids=(),
        risk_class="MUTATION", confidence=1.0, reason_codes=("typed_test",),
    )


def _step(step_id, operation, params, *, risk="READ_ONLY", effect="OBSERVE"):
    return PlanStep(step_id=step_id, goal_id="g1", capability_id="browser.web", operation=operation,
                    required_evidence=("browser_page_opened",), effect_type=effect,
                    target_scope="localhost_browser", reversibility="REVERSIBLE",
                    external_side_effect=False, risk_class=risk, parameters=tuple(params.items()))


def test_playwright_local_read_navigation_and_action_are_evidenced():
    server, url = _fixture()
    try:
        plan = ExecutionPlan("browser_test", (
            _step("open", "browser.open_read", {"url": url}),
            _step("nav", "browser.navigate", {"selector": "#next"}),
        ))
        bundle = ExistingPlaywrightBrowserAdapter(policy_mode="LOCAL_TEST").collect_evidence(_understanding(), plan, "trace_browser")
        assert bundle.status == "COMPLETE", bundle.errors
        assert "Page A" in bundle.items[0].observation
        assert "JARVIS_BROWSER_PROOF_42" in bundle.items[1].observation
        assert all(receipt.status == "COMPLETE" for receipt in bundle.receipts)
    finally:
        server.shutdown(); server.server_close()


def test_playwright_mutation_requires_host_authorization():
    server, url = _fixture()
    try:
        plan = ExecutionPlan("browser_test", (_step("act", "browser.fill_submit", {
            "url": url, "input_selector": "#value", "submit_selector": "#submit", "value": "42",
        }, risk="MUTATION", effect="MUTATE"),))
        bundle = ExistingPlaywrightBrowserAdapter(policy_mode="LOCAL_TEST").collect_evidence(_understanding(), plan, "trace_denied")
        assert bundle.status == "UNAVAILABLE"
        assert "host_authorization_required" in " ".join(bundle.errors)
        assert not bundle.receipts
    finally:
        server.shutdown(); server.server_close()


def test_planner_approval_parameter_cannot_override_host_denial():
    server, url = _fixture()
    try:
        plan = ExecutionPlan("browser_test", (_step("act", "browser.fill_submit", {
            "input_selector": "#value", "submit_selector": "#submit", "value": "42", "authorization": "approved",
        }, risk="MUTATION", effect="MUTATE"),))
        denied = PermissionDecision(False, "browser.web", "local_terminal_session", "test", "denied", "trace_denied", "browser.fill_submit")
        bundle = ExistingPlaywrightBrowserAdapter(HostBrowserAuthorization(frozenset({"act"})), denied, policy_mode="LOCAL_TEST").collect_evidence(_understanding(), plan, "trace_denied")
        assert bundle.status == "UNAVAILABLE" and not bundle.receipts
    finally:
        server.shutdown(); server.server_close()


def test_playwright_authorized_local_action_has_post_action_readback():
    server, url = _fixture()
    try:
        plan = ExecutionPlan("browser_test", (
            _step("open", "browser.open_read", {"url": url}),
            _step("act", "browser.fill_submit", {
                "input_selector": "#value", "submit_selector": "#submit", "value": "42",
                "authorization": "approved",
            }, risk="MUTATION", effect="MUTATE"),
        ))
        decision = PermissionDecision(True, "browser.web", "local_terminal_session", "test", "", "trace_action", "browser.fill_submit", step_id="act")
        bundle = ExistingPlaywrightBrowserAdapter(HostBrowserAuthorization(frozenset({"act"})), decision, policy_mode="LOCAL_TEST").collect_evidence(_understanding(), plan, "trace_action")
        assert bundle.status == "COMPLETE", bundle.errors
        assert "submitted:42" in bundle.items[-1].observation
        assert len(bundle.receipts) == 2
    finally:
        server.shutdown(); server.server_close()


def test_playwright_rejects_non_local_urls():
    plan = ExecutionPlan("browser_test", (_step("open", "browser.open_read", {"url": "file:///etc/passwd"}),))
    bundle = ExistingPlaywrightBrowserAdapter().collect_evidence(_understanding(), plan, "trace_external")
    assert bundle.status == "UNAVAILABLE"
    assert "url_policy_denied" in " ".join(bundle.errors)
