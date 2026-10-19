from MAKSIMAR_CORE_LIB.security_layer.host_principal import (
    HostPrincipal, identity_from_host_token, issue_host_token, verify_host_token,
)


def test_host_token_is_signed_and_yields_owner_identity() -> None:
    principal = HostPrincipal("owner", "session-1")
    token = issue_host_token(principal, secret="test-secret")
    assert verify_host_token(token, secret="test-secret") == principal
    verified = identity_from_host_token(token)  # environment intentionally absent
    assert verified is None


def test_host_token_tamper_and_wrong_secret_fail_closed() -> None:
    token = issue_host_token(HostPrincipal("owner", "session-1"), secret="test-secret")
    body, _sig = token.split(".", 1)
    assert verify_host_token(body + ".0" * 32, secret="test-secret") is None
    assert verify_host_token(token, secret="wrong") is None
