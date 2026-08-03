from pathlib import Path
import re


ROOT = Path(__file__).resolve().parents[1]
SYNTAX = ROOT / "syntax"


def test_mode_specific_syntax_layout_exists():
    required = [
        SYNTAX / "data_syntax.md",
        SYNTAX / "time_series" / "feature_syntax.md",
        SYNTAX / "time_series" / "operations_syntax.md",
        SYNTAX / "time_series" / "parameters.md",
        SYNTAX / "time_series" / "strategy_patterns.md",
        SYNTAX / "cross_sectional" / "feature_syntax.md",
        SYNTAX / "cross_sectional" / "operations_syntax.md",
        SYNTAX / "cross_sectional" / "parameters.md",
        SYNTAX / "cross_sectional" / "panel_contract.md",
        SYNTAX / "cross_sectional" / "strategy_patterns.md",
        SYNTAX / "research" / "validation_protocol.md",
        SYNTAX / "research" / "experiment_manifest_schema.md",
    ]
    assert all(path.is_file() for path in required)


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


def test_compatibility_entry_points_link_to_canonical_docs():
    expected = {
        "feature_syntax.md": ("time_series/feature_syntax.md", "cross_sectional/feature_syntax.md"),
        "operations_syntax.md": ("time_series/operations_syntax.md", "cross_sectional/operations_syntax.md"),
        "parameters.md": ("time_series/parameters.md", "cross_sectional/parameters.md"),
        "strategy_patterns.md": ("time_series/strategy_patterns.md", "cross_sectional/strategy_patterns.md"),
        "panel_feature_contract.md": ("cross_sectional/panel_contract.md",),
        "validation_protocol.md": ("research/validation_protocol.md",),
        "experiment_manifest_schema.md": ("research/experiment_manifest_schema.md",),
    }
    for filename, targets in expected.items():
        text = (SYNTAX / filename).read_text(encoding="utf-8")
        assert all(target in text for target in targets)
