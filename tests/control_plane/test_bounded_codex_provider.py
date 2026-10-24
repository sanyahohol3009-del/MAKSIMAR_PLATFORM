import json
from pathlib import Path
from types import SimpleNamespace
import pytest
from MAKSIMAR_SERVER.AI_ORCHESTRATION import external_agent_provider_adapter as provider
from MAKSIMAR_SERVER.AI_ORCHESTRATION import project_workspace_tools as project


@pytest.fixture
def worker(monkeypatch,tmp_path):
    executable=tmp_path/'codex.exe'; executable.write_text('test executable identity')
    target=tmp_path/'owner.py'; target.write_text('value = 42\n')
    monkeypatch.setattr(project,'PROJECT_ROOT',tmp_path)
    original=Path.glob
    monkeypatch.setattr(Path,'glob',lambda path,pattern:iter((executable,)) if str(path).endswith('Codex/bin') else original(path,pattern))
    return executable,target


def events(*items):
    return '\n'.join(json.dumps(item) for item in (*items,
        {'type':'item.completed','item':{'type':'agent_message','text':'Bounded analysis.'}},
        {'type':'turn.completed','usage':{'output_tokens':3}}))


def test_worker_has_no_tools_and_host_independently_reads_source(monkeypatch,worker):
    calls=[]
    def run(args,**kwargs):
        calls.append((args,kwargs)); return SimpleNamespace(returncode=0,stdout=events())
    monkeypatch.setattr(provider.subprocess,'run',run)
    result=provider.run_bounded_codex_proposal('Explain this source.',path='owner.py')
    assert result['ok'] and result['provider_readback']['source_unchanged']
    assert result['provider_readback']['source_sha256']
    args,kwargs=calls[0]
    assert args[args.index('--sandbox')+1]=='read-only' and '--ephemeral' in args
    assert 'shell_tool' in args and 'hooks' in args and 'plugins' in args
    assert 'value = 42' in kwargs['input']


def test_worker_self_report_cannot_hide_file_mutation(monkeypatch,worker):
    def run(*args,**kwargs):
        worker[1].write_text('value = 99\n'); return SimpleNamespace(returncode=0,stdout=events())
    monkeypatch.setattr(provider.subprocess,'run',run)
    result=provider.run_bounded_codex_proposal('Explain.',path='owner.py')
    assert not result['ok'] and result['error']=='codex_incomplete_or_source_changed'


def test_worker_rejects_unexpected_tool_execution(monkeypatch,worker):
    monkeypatch.setattr(provider.subprocess,'run',lambda *a,**k:SimpleNamespace(returncode=0,
        stdout=events({'type':'item.completed','item':{'type':'command_execution','command':'unexpected'}})))
    result=provider.run_bounded_codex_proposal('Explain.')
    assert not result['ok'] and result['error']=='codex_unexpected_tool_activity'
