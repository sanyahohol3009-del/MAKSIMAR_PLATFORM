"""Independent typed acceptance oracles only; NOT a production language parser.

Fixture facet IDs annotate semantic correspondence. They are not extra fields
in the model-facing GoalFrame schema and are not extracted from words.
"""
import copy,json,hashlib
from pathlib import Path
import pytest
from MAKSIMAR_CORE_LIB.ai_orchestration.semantic_intent_contract import hydrate_response_requirements,validate_response_obligation_coverage
R=Path(__file__).resolve().parents[2];A=R/'RUNTIME/audits/WSL_RECOVERY_ACTIVATION_20261011'
KINDS=('PROVENANCE','RATIONALE','EXECUTION','EVIDENCE','REVIEW_STATUS','LEARNING_QUALIFICATION')
RELATIONS=('ACTOR_OF_SUBJECT','SOURCE_OF_SUBJECT','RECEIPT_OF_EFFECT','SOURCE_OF_SUBJECT','REVIEW_OF_SUBJECT_OR_EXPERIENCE','LEARNING_QUALIFICATION_OF_EXPERIENCE')
# Independent semantic annotations of equivalent sources. No production matcher
# reads these words; model multilingual performance is NOT tested here.
SOURCES={'EN':'Who changed it, why, what ran, what proves it, who reviewed it, may it be learned?',
         'RU':'Кто изменил, зачем, что исполнилось, чем доказано, кто проверил, допустимо ли обучение?',
         'DE':'Wer hat es geaendert, warum, was lief, welcher Beleg, wer pruefte es, darf daraus gelernt werden?'}

def semantic_oracle(count=6):
    return tuple({'response_requirement_id':f'fixture_facet_{i}', 'requirement_kind':KINDS[i%6],
                  'memory_query_kind':'PROVENANCE','applies_to_goal_ids':['g1'],
                  'description':f'Independent typed semantic facet {i}'} for i in range(count))

def candidate_fixture(count=6):
    # Separately supplied controlled candidate annotations; never copy the
    # expected source oracle to manufacture a positive source-coverage result.
    annotated=(('fixture_facet_0','PROVENANCE'),('fixture_facet_1','RATIONALE'),
               ('fixture_facet_2','EXECUTION'),('fixture_facet_3','EVIDENCE'),
               ('fixture_facet_4','REVIEW_STATUS'),('fixture_facet_5','LEARNING_QUALIFICATION'))
    return tuple({'response_requirement_id':identifier,'requirement_kind':kind,
        'memory_query_kind':'PROVENANCE','applies_to_goal_ids':['g1'],
        'description':f'Independent typed semantic facet {i}'}
        for i,(identifier,kind) in enumerate(annotated[:count]))

@pytest.mark.parametrize('language',SOURCES)
@pytest.mark.parametrize('mutation',['missing','duplicate','wrong_kind','extra'])
def test_independent_source_oracle_rejects_candidate_semantic_loss_or_change(language,mutation):
    source=semantic_oracle(3);produced=list(candidate_fixture(3))
    if mutation=='missing':produced.pop()
    if mutation=='duplicate':produced.insert(1,copy.deepcopy(produced[1]))
    if mutation=='wrong_kind':produced[2]['requirement_kind']='EVIDENCE'
    if mutation=='extra':produced.append({'response_requirement_id':'extra','requirement_kind':'EVIDENCE'})
    before=copy.deepcopy((source,produced));assert SOURCES[language]
    with pytest.raises(ValueError):validate_response_obligation_coverage(source,tuple(produced))
    assert (source,produced)==before

@pytest.mark.parametrize('language',SOURCES)
@pytest.mark.parametrize('order',[(0,1,2),(2,0,1)])
def test_complete_controlled_semantic_set_is_order_and_language_annotation_invariant(language,order):
    source=semantic_oracle(3);candidate=candidate_fixture(3);produced=tuple(candidate[i] for i in order)
    assert SOURCES[language]
    validate_response_obligation_coverage(source,produced)


def test_six_source_facets_six_goalframe_facets_six_hydrated_requirements():
    source=semantic_oracle();candidate=candidate_fixture()
    validate_response_obligation_coverage(source,candidate)  # A fixture -> B fixture
    native=tuple({k:v for k,v in q.items() if k!='response_requirement_id'} for q in candidate)
    goals=({'goal_id':'g1','subject_constraints':{'scope':'SUBJECT','actor':'ACTOR_FIXTURE','task_ref':'controlled task'}},)
    actual=hydrate_response_requirements(goals,native)
    # Independently stated canonical projection expectations, not hydrate(x)==hydrate(x).
    expected=tuple({'schema_version':'response_requirement.v1','response_requirement_id':f'goalframe_response_{i}',
        'applies_to_goal_ids':['g1'],'description':f'Independent typed semantic facet {i}',
        'memory_query_kind':'PROVENANCE','requirement_kind':KINDS[i],
        'subject_binding':{'scope':'SUBJECT','actor':'ACTOR_FIXTURE','task_ref':'controlled task',
                           'subject_goal_id':'g1','relation':RELATIONS[i]}} for i in range(6))
    validate_response_obligation_coverage(expected,actual)
    assert len(source)==len(candidate)==len(actual)==6
    assert [q['requirement_kind'] for q in actual]==list(KINDS)


def test_complete_source_span_does_not_prove_semantic_facet_completeness():
    from CONTROL_PLANE.canonical_semantic_spine import _source_contains_grounding
    source=SOURCES['EN'];assert _source_contains_grounding(source,source)
    # Entire request copied, but typed semantic representation still omits C.
    expected=semantic_oracle(3);actual=expected[:2]
    with pytest.raises(ValueError):validate_response_obligation_coverage(expected,actual)


def test_saved_five_is_rejected_by_independent_six_facet_acceptance_oracle_without_retrofit():
    path=A/'owner_20261016_loaded_typed_kind_one_natural_response.json';before=path.read_bytes()
    result=json.loads(before)['result'];raw=json.loads(result['goalframe_understanding_attempts'][0]['raw_model_content'])
    actual=raw['response_requirements'];assert len(actual)==5
    # The test oracle supplies six expected semantic facets; runtime contains no
    # request-specific literal or host parser. Preserve raw identities/content.
    # Explicit acceptance-only correspondence annotation: the third emitted
    # EVIDENCE facet addresses execution, while the standalone proof facet is
    # absent. This annotation is NOT runtime inference and does not modify raw.
    source=tuple({'response_requirement_id':f'fixture_facet_{i}','requirement_kind':kind} for i,kind in enumerate(KINDS))
    correspondence=(0,1,2,4,5)
    annotated=tuple({'response_requirement_id':f'fixture_facet_{i}','requirement_kind':q['requirement_kind']} for i,q in zip(correspondence,actual))
    with pytest.raises(ValueError,match='missing_or_extra'):
        validate_response_obligation_coverage(source,annotated)
    assert path.read_bytes()==before


def test_saved_ambiguous_subject_is_still_protected_negative():
    proof=json.loads((A/'owner_20261017_descriptive_subject_saved_trace_proof.json').read_text())
    assert proof['SAVED_TARGET_DESCRIPTIVE_SUBJECT_RESOLVABLE']=='AMBIGUOUS'
    assert proof['history_item_truncated'] and proof['saved_context_turns']==0



def test_declared_set_can_pass_downstream_while_source_facet_is_missing():
    from CONTROL_PLANE.canonical_semantic_spine import _goalframe_response_requirement_violations
    source=semantic_oracle(3);candidate=candidate_fixture(2)
    goals=({'goal_id':'g1','subject_constraints':{'scope':'SUBJECT','actor':'ACTOR_FIXTURE'},
            'memory_filter':{'query_kind':'PROVENANCE','time_basis':'ANY_TIME','time_start':'','time_end':''}},)
    native=tuple({k:v for k,v in q.items() if k!='response_requirement_id'} for q in candidate)
    hydrated=hydrate_response_requirements(goals,native)
    assert len(hydrated)==2
    assert not _goalframe_response_requirement_violations(goals,hydrated)
    # Independent A still requires C; downstream green B->C did not establish A->B.
    with pytest.raises(ValueError,match='missing_or_extra'):
        validate_response_obligation_coverage(source,candidate)
