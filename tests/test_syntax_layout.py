from pathlib import Path
import re


ROOT = Path(__file__).resolve().parents[1]
SYNTAX = ROOT / "syntax"


def test_mode_specific_syntax_layout_exists():
    required = [
        SYNTAX / "INDEX.md",
        SYNTAX / "data_syntax.md",
        SYNTAX / "mode_contract.md",
        SYNTAX / "fundamental_data_contract.md",
        SYNTAX / "time_series" / "INDEX.md",
        SYNTAX / "time_series" / "feature_syntax.md",
        SYNTAX / "time_series" / "operations_syntax.md",
        SYNTAX / "time_series" / "parameters.md",
        SYNTAX / "time_series" / "strategy_patterns.md",
        SYNTAX / "cross_sectional" / "INDEX.md",
        SYNTAX / "cross_sectional" / "feature_syntax.md",
        SYNTAX / "cross_sectional" / "operations_syntax.md",
        SYNTAX / "cross_sectional" / "parameters.md",
        SYNTAX / "cross_sectional" / "panel_contract.md",
        SYNTAX / "cross_sectional" / "strategy_patterns.md",
        SYNTAX / "research" / "validation_protocol.md",
        SYNTAX / "research" / "experiment_manifest_schema.md",
    ]
    assert all(path.is_file() for path in required)


def test_root_has_only_shared_documents():
    root_files = {p.name for p in SYNTAX.iterdir() if p.is_file()}
    assert root_files == {"INDEX.md", "data_syntax.md", "mode_contract.md",
                          "fundamental_data_contract.md"}


def test_shared_data_is_not_duplicated_by_mode():
    assert not (SYNTAX / "time_series" / "data_syntax.md").exists()
    assert not (SYNTAX / "cross_sectional" / "data_syntax.md").exists()


def test_feature_catalogs_are_shape_specific():
    ts = (SYNTAX / "time_series" / "feature_syntax.md").read_text(encoding="utf-8")
    cs = (SYNTAX / "cross_sectional" / "feature_syntax.md").read_text(encoding="utf-8")
    assert "SeriesT" in ts
    assert "PanelT" in cs
    assert "self.feat.ema_panel" in cs
    assert "`ema`" in ts


def test_time_series_catalog_has_expected_unique_inventory():
    text = (SYNTAX / "time_series" / "feature_syntax.md").read_text(encoding="utf-8")
    inventory = text.split("## Multi-Output Rules", 1)[0]
    names = re.findall(r"^\| `([a-z0-9_]+)` \| `[^`]+` \|", inventory, re.MULTILINE)
    assert len(names) == 174
    assert len(names) == len(set(names))
    assert {"adx", "ema", "macd", "rolling_zscore", "xside_gap_3methods"} <= set(names)


def test_markdown_relative_links_resolve():
    pattern = re.compile(r"\[[^\]]*\]\(([^)#]+)(?:#[^)]+)?\)")
    missing = []
    for document in SYNTAX.rglob("*.md"):
        for target in pattern.findall(document.read_text(encoding="utf-8")):
            if "://" in target or target.startswith("#"):
                continue
            resolved = (document.parent / target).resolve()
            if not resolved.exists():
                missing.append((document.relative_to(ROOT).as_posix(), target))
    assert missing == []
