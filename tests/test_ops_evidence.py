import pathlib
import re

ROOT = pathlib.Path(__file__).resolve().parents[1]

EXAMPLE_GLOBS = [
    "template_example/VN-*/*.py",
    "output/stage_2/*/*/*.py",
]

CATALOGS = {
    "time_series": ROOT / "syntax/time_series/operations_syntax.md",
    "cross_sectional": ROOT / "syntax/cross_sectional/operations_syntax.md",
}

OP_PATTERN = re.compile(r"self\.op\.([A-Za-z_][A-Za-z0-9_]*)")


def _scanned_ops():
    ops = set()
    for pattern in EXAMPLE_GLOBS:
        for path in ROOT.glob(pattern):
            ops.update(OP_PATTERN.findall(path.read_text(encoding="utf-8")))
    return ops


def _verified_ops(key):
    text = CATALOGS[key].read_text(encoding="utf-8")
    match = re.search(r"## Evidence Status\n(.*?)(?=\n## |\Z)", text, re.S)
    assert match, f"missing Evidence Status section in {key} catalog"
    verified = set()
    for line in match.group(1).splitlines():
        cells = [cell.strip() for cell in line.strip().strip("|").split("|")]
        if len(cells) == 2 and cells[1] == "EXAMPLE_VERIFIED":
            verified.add(cells[0].strip("`"))
    return verified


def _split_by_mode(ops):
    cs_verified = _verified_ops("cross_sectional")
    cs = {op for op in ops if op in cs_verified or op.endswith("_panel")}
    return ops - cs, cs


def test_used_ops_are_marked_example_verified():
    ts_used, cs_used = _split_by_mode(_scanned_ops())
    assert ts_used <= _verified_ops("time_series"), f"used but not EXAMPLE_VERIFIED: {ts_used - _verified_ops('time_series')}"
    assert cs_used <= _verified_ops("cross_sectional"), f"used but not EXAMPLE_VERIFIED: {cs_used - _verified_ops('cross_sectional')}"


def test_example_verified_ops_are_actually_used():
    ts_used, cs_used = _split_by_mode(_scanned_ops())
    assert _verified_ops("time_series") <= ts_used, f"stale EXAMPLE_VERIFIED: {_verified_ops('time_series') - ts_used}"
    assert _verified_ops("cross_sectional") <= cs_used, f"stale EXAMPLE_VERIFIED: {_verified_ops('cross_sectional') - cs_used}"
