# Syntax Documentation Index

Canonical entry point for Round 2 XNOQuant strategy syntax and research contracts.

## Shared Data and Contracts

| Document | Scope |
|---|---|
| [`data_syntax.md`](data_syntax.md) | Shared raw-data catalog for both modes; use non-`_panel` accessors for `time_series` and `_panel` accessors for `cross_sectional` |
| [`mode_contract.md`](mode_contract.md) | Mode, shape, position API, and separation rules |
| [`fundamental_data_contract.md`](fundamental_data_contract.md) | Point-in-time, accounting, missingness, and coverage rules |

Data is shared by both execution modes. Features, operations, parameters, and strategy patterns are mode-specific.

## Time-Series

See [`time_series/INDEX.md`](time_series/INDEX.md).

| Document | Purpose |
|---|---|
| [`time_series/feature_syntax.md`](time_series/feature_syntax.md) | `SeriesT` feature API |
| [`time_series/operations_syntax.md`](time_series/operations_syntax.md) | `SeriesT` operation API and pending authoritative inventory |
| [`time_series/parameters.md`](time_series/parameters.md) | Daily indicator and position profiles |
| [`time_series/strategy_patterns.md`](time_series/strategy_patterns.md) | Long-only state, timing, sizing, and exit patterns |

## Cross-Sectional

See [`cross_sectional/INDEX.md`](cross_sectional/INDEX.md).

| Document | Purpose |
|---|---|
| [`cross_sectional/feature_syntax.md`](cross_sectional/feature_syntax.md) | `PanelT` feature API |
| [`cross_sectional/operations_syntax.md`](cross_sectional/operations_syntax.md) | Panel and cross-sectional operations |
| [`cross_sectional/parameters.md`](cross_sectional/parameters.md) | Ranking, normalization, eligibility, and weighting profiles |
| [`cross_sectional/panel_contract.md`](cross_sectional/panel_contract.md) | Axes, masks, missingness, defaults, and evidence |
| [`cross_sectional/strategy_patterns.md`](cross_sectional/strategy_patterns.md) | Factor, eligibility, and market-neutral portfolio patterns |

## Research Governance

See [`research/INDEX.md`](research/INDEX.md).

| Document | Purpose |
|---|---|
| [`research/validation_protocol.md`](research/validation_protocol.md) | Experiment ladder, locked OOS, robustness, and decision taxonomy |
| [`research/experiment_manifest_schema.md`](research/experiment_manifest_schema.md) | Hypothesis, family, variant, trial count, freeze, and Test-access records |

## Compatibility Entry Points

The following root files remain as temporary links so existing repository references do not break during migration:

- `feature_syntax.md`
- `operations_syntax.md`
- `parameters.md`
- `strategy_patterns.md`
- `panel_feature_contract.md`
- `validation_protocol.md`
- `experiment_manifest_schema.md`

New documentation and active references must use the canonical mode/research paths above.

## Required Reading Order

1. `mode_contract.md`
2. `data_syntax.md`
3. `fundamental_data_contract.md` when using accounting data
4. Mode-specific `feature_syntax.md`
5. Mode-specific `operations_syntax.md`
6. Mode-specific `parameters.md`
7. Mode-specific `strategy_patterns.md`
8. `research/validation_protocol.md`
9. `research/experiment_manifest_schema.md`

## Hard Rules

1. Never mix `SeriesT` and `PanelT` in one strategy.
2. `time_series` uses data accessors without `_panel` and `self.set_positions()` within `[0, 1]`.
3. `cross_sectional` uses `_panel` accessors and `self.set_portfolio_positions()`.
4. Data presence in the shared catalog does not prove runtime or economic suitability for every mode.
5. Runtime defaults are not canonical research parameters; pass supported parameters explicitly.
6. Missing fundamental data means unavailable, not zero.
7. Final OOS may be opened only after strategy freeze and must not be retuned against.
