from __future__ import annotations

from tools.monitor.oob_foundation_monitor import render_screen


def test_render_screen_contains_main_sections() -> None:
    screen = render_screen()

    assert "MAKSIMAR OOB FOUNDATION MONITOR" in screen
    assert "SESSIONS" in screen
    assert "HEARTBEATS" in screen
    assert "RUNTIME ACCESS" in screen
    assert "LOG TAILS" in screen


def test_log_tail_reads_only_bounded_suffix_and_preserves_source(monkeypatch, tmp_path):
    from pathlib import Path
    from tools.monitor.oob_foundation_monitor import tail_log
    path = tmp_path / 'large.log'
    with path.open('wb') as handle:
        handle.seek(256 * 1024 * 1024)
        handle.write(b'old\nfirst\nsecond\nthird\n')
    size = path.stat().st_size
    original_open = Path.open
    read_sizes = []
    class BoundedReader:
        def __init__(self, handle): self.handle = handle
        def __enter__(self): return self
        def __exit__(self, *args): return self.handle.__exit__(*args)
        def __getattr__(self, name): return getattr(self.handle, name)
        def read(self, size=-1):
            assert 0 < size <= 65536, 'tail must never read the whole file'
            read_sizes.append(size)
            return self.handle.read(size)
    def monitored_open(self, *args, **kwargs):
        handle = original_open(self, *args, **kwargs)
        return BoundedReader(handle) if self == path else handle
    monkeypatch.setattr(Path, 'open', monitored_open)
    assert tail_log(path, 3) == ['first', 'second', 'third']
    assert sum(read_sizes) <= 65536
    assert path.stat().st_size == size


def test_log_tail_preserves_unicode_final_line_and_empty_bounds(tmp_path):
    from tools.monitor.oob_foundation_monitor import tail_log
    path = tmp_path / 'unicode.log'
    path.write_text('предыдущая\nпервая\nвторая\nтретья', encoding='utf-8')
    assert tail_log(path, 3) == ['первая', 'вторая', 'третья']
    assert tail_log(path, 0) == []
    assert tail_log(tmp_path / 'missing.log') == []


def test_oversized_single_log_line_has_explicit_bounded_display(tmp_path):
    from tools.monitor.oob_foundation_monitor import tail_log
    path = tmp_path / 'single.log'
    path.write_bytes(b'x' * 200000)
    result = tail_log(path)
    assert result and 'truncated' in result[0]
    assert sum(len(line) for line in result) < 66000
    assert path.stat().st_size == 200000
