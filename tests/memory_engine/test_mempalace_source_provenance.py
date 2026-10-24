"""Exercise the installed child owner's source-change gate without embeddings."""
from pathlib import Path
import subprocess


def test_native_miner_binds_actual_bytes_and_detects_same_mtime_changes():
    root = Path(__file__).resolve().parents[2]
    python = root / "EXTERNAL_BACKENDS/mempalace/venv/bin/python"
    script = r'''
import hashlib, os, tempfile
from pathlib import Path
from contextlib import nullcontext
from mempalace import miner, palace
class Collection:
    def __init__(self): self.rows=[]
    def get(self, **kwargs):
        return {'ids':[row[0] for row in self.rows[:1]], 'metadatas':[row[2] for row in self.rows[:1]]}
    def delete(self, **kwargs): self.rows=[]
    def upsert(self, documents, ids, metadatas):
        self.rows.extend(zip(ids, documents, metadatas))
with tempfile.TemporaryDirectory() as tmp:
    path=Path(tmp)/'source.md'
    path.write_text('Original verified source content. ' * 100)
    before=path.read_bytes(); digest=hashlib.sha256(before).hexdigest()
    collection=Collection()
    miner.mine_lock=lambda _: nullcontext()
    count,_=miner.process_file(path,Path(tmp),collection,'project',[],'JARVIS',False)
    assert count>0
    assert all(row[2]['source_sha256']==digest for row in collection.rows)
    assert palace.file_already_mined(collection,str(path),True)
    timestamp=path.stat().st_mtime_ns
    path.write_bytes(before.replace(b'Original',b'Modified'))
    os.utime(path,ns=(timestamp,timestamp))
    assert not palace.file_already_mined(collection,str(path),True)
    count,_=miner.process_file(path,Path(tmp),collection,'project',[],'JARVIS',False)
    assert count>0 and len({row[0] for row in collection.rows})==len(collection.rows)
    assert all(row[2]['source_sha256']==hashlib.sha256(path.read_bytes()).hexdigest() for row in collection.rows)
    assert palace.file_already_mined(collection,str(path),True)
    del collection.rows[0][2]['source_sha256']
    assert not palace.file_already_mined(collection,str(path),True)
print('NATIVE_SOURCE_HASH_AND_REINDEX_GATE_PASS')
'''
    completed = subprocess.run([str(python), "-B", "-c", script], cwd=root, capture_output=True,
                               text=True, timeout=30, check=False)
    assert completed.returncode == 0, completed.stderr
    assert "NATIVE_SOURCE_HASH_AND_REINDEX_GATE_PASS" in completed.stdout
