# Time-Series Syntax

Canonical entry point for Round 2 `time_series` mode.

| Document | Purpose |
|---|---|
| [`feature_syntax.md`](feature_syntax.md) | `SeriesT` indicators and transforms |
| [`operations_syntax.md`](operations_syntax.md) | Causal `SeriesT` operations |
| [`parameters.md`](parameters.md) | Daily-equity research parameter profiles |
| [`strategy_patterns.md`](strategy_patterns.md) | Long-only construction patterns |

## Contract

- Data comes from the shared [`../data_syntax.md`](../data_syntax.md) catalog using accessors without `_panel`.
- Features and operations in this directory consume or return `SeriesT` unless explicitly documented otherwise.
- Position construction uses `self.set_positions()` and remains within `[0, 1]`.
- Runtime defaults document API behavior; strategy code must use explicit parameters selected from the research profile or experiment manifest.
