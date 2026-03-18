from MAKSIMAR_CORE_LIB.policy_engine.policy_accessor import get_policy


def test_policy_access_smoke() -> None:
    policy = get_policy("access_policy")
    assert policy.name == "access_policy"
    assert policy.version.endswith(".v1")
