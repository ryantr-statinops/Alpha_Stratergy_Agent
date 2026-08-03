# Operations Syntax Reference (Round 2)

Use this file as the canonical catalog for `self.op.*` on the Round 2 equity model.

## Mode Contract

`self.op.*` comes in two families:

| Mode | Operator family | Shape | Example |
|---|---|---|---|
| `time_series` | suffix-less operators | one time series per symbol | `self.op.pct_change(series, periods=1)`, `self.op.fillna(series, value=0)` |
| `cross_sectional` | `_cs_panel` operators | time × symbol panel | `self.op.rank_cs_panel(panel)`, `self.op.portfolio_weights_panel(signal)` |

- In `cross_sectional` mode the seven operators below operate on a `PanelT` (time × symbol) at each
  timestamp across the eligible symbol cross-section.
- Use `_cs_panel` operators **only** with `_panel` data fields; never mix families.
- `time_series` mode keeps the suffix-less operators (see `(Old)vnfuture/strategy_framework.md` and the
  Round-2 examples, e.g. `self.op.pct_change(premium_revenue, periods=1)`).

## Section Index

| Group | Jump to |
|---|---|
| Cross-Sectional Normalization | [Cross-Sectional Normalization](#cross-sectional-normalization) |
| Cross-Sectional Portfolio Weights | [Cross-Sectional Portfolio Weights](#cross-sectional-portfolio-weights) |

## Quick Lookup

| Group | Typical use | Representative functions |
|---|---|---|
| Cross-Sectional Normalization | rank/demean/winsorize/zscore each date's eligible cross-section | `rank_cs_panel`, `demean_cs_panel`, `normalize_l1_cs_panel`, `winsorize_cs_panel`, `zscore_cs_panel` |
| Cross-Sectional Portfolio Weights | build market-neutral weights from signals | `portfolio_weights_panel` |

## Reading Tips

- Every `_cs_panel` operator accepts an optional `mask: PanelT` to restrict eligibility at each timestamp.
- Symbols outside the universe receive weight/rank as if excluded by the mask.
- For portfolio construction prefer `portfolio_weights_panel` with `method='rank_demean_l1'`
  (market-neutral: net exposure ≈ 0, gross exposure normalized to 1).

## Cross-Sectional Normalization

| Name | Returns | Syntax | Description |
|---|---|---|---|
| `rank_cs_panel` | `PanelT` | `self.op.rank_cs_panel(panel: PanelT, mask: PanelT = None, method='average')` | Rank eligible symbols independently at each timestamp as percentile ranks. |
| `demean_cs_panel` | `PanelT` | `self.op.demean_cs_panel(panel: PanelT, mask: PanelT = None, winsorize=None)` | Subtract the cross-sectional mean from each eligible symbol. |
| `normalize_l1_cs_panel` | `PanelT` | `self.op.normalize_l1_cs_panel(panel: PanelT, mask: PanelT = None, eps=1e-12)` | Normalize each timestamp to unit L1 exposure after masking. |
| `winsorize_cs_panel` | `PanelT` | `self.op.winsorize_cs_panel(panel: PanelT, mask: PanelT = None, lower=0.02, upper=0.98)` | Clip each date's eligible cross-section to quantile bounds. |
| `zscore_cs_panel` | `PanelT` | `self.op.zscore_cs_panel(panel: PanelT, mask: PanelT = None, ddof=1)` | Standardize each eligible cross-section with safe zero-variance handling. |

## Cross-Sectional Portfolio Weights

| Name | Returns | Syntax | Description |
|---|---|---|---|
| `portfolio_weights_panel` | `PanelT` | `self.op.portfolio_weights_panel(signal: PanelT, method='rank_demean_l1', mask: PanelT = None, rank_method='average', max_abs_weight=None)` | Build neutral unit-gross portfolio weights from cross-sectional ranks. |

## Time-Series Mode Notes

In `time_series` mode the suffix-less operators remain available (from Round 1), for example:

```python
profit_growth = self.op.fillna(self.op.pct_change(net_profit, periods=1), value=0)
capital_ratio = self.op.fillna(equity / total_assets, value=0)
eligible = self.op.notna(net_profit) & (total_assets > 0)
```

- Keep `fillna` causal by using a constant or forward-fill only.
- Use `self.op.notna(series)` (or `.notna()`) to exclude unavailable fundamentals — treat them as unavailable, not zero.
- Do not use global aggregations such as `.mean()`, `.rank()`, `.quantile()`, `.sort_values()`.
