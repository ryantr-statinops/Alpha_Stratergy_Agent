# Cross-Sectional Syntax

Canonical entry point for Round 2 `cross_sectional` mode.

| Document | Purpose |
|---|---|
| [`feature_syntax.md`](feature_syntax.md) | `PanelT` features and transforms |
| [`operations_syntax.md`](operations_syntax.md) | Cross-sectional and panel operations |
| [`parameters.md`](parameters.md) | Ranking, normalization, eligibility, and portfolio parameters |
| [`panel_contract.md`](panel_contract.md) | Panel axes, masks, missingness, and evidence |
| [`strategy_patterns.md`](strategy_patterns.md) | Market-neutral portfolio patterns |

## Contract

- Data comes from the shared [`../data_syntax.md`](../data_syntax.md) catalog using `_panel` accessors.
- Features and operations in this directory consume or return `PanelT` unless explicitly documented otherwise.
- Portfolio construction uses `self.set_portfolio_positions()`.
- Market-neutral weights do not imply sector, beta, liquidity, or real-world shortability neutrality.
