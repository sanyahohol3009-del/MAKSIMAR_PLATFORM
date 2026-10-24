import jsonschema
import pytest
from CONTROL_PLANE import canonical_semantic_spine as spine


def _reference_schema():
    return spine.GOALFRAME_UNDERSTANDING_JSON_SCHEMA["properties"]["response_requirements"]["items"]["properties"]["applies_to_goal_ids"]


def test_response_reference_schema_reuses_existing_goal_identity_domain():
    goal = spine._goalframe_item_schema("PRIMARY_OUTCOME")["properties"]["goal_id"]
    refs = _reference_schema()
    assert refs["items"] == goal
    for value in goal["enum"]:
        jsonschema.validate([value], refs)
    with pytest.raises(jsonschema.ValidationError):
        jsonschema.validate(["outside_existing_goal_identity_domain"], refs)


def test_generation_schema_rejects_empty_goal_references():
    with pytest.raises(jsonschema.ValidationError):
        jsonschema.validate([], _reference_schema())


def test_legal_domain_reference_still_requires_actually_declared_goal():
    legal = spine._goalframe_item_schema("PRIMARY_OUTCOME")["properties"]["goal_id"]["enum"]
    violations = spine._goalframe_response_requirement_violations(
        ({"goal_id":legal[0]},), ({"applies_to_goal_ids":[legal[1]], "description":"present evidence"},))
    assert violations
    assert "unknown goal_id" in violations[0][1]
