# Syntax Guide

Tài liệu này hướng dẫn cách đọc và sử dụng hai catalog:

- [`syntax/feature_syntax.md`](feature_syntax.md)
- [`syntax/operations_syntax.md`](operations_syntax.md)

## How To Read

1. Tra `Quick Lookup` trước để chọn đúng nhóm hàm hoặc toán tử.
2. Mở phần chi tiết bên dưới để lấy signature chính xác.
3. Với hàm trả tuple, luôn kiểm tra thứ tự output trước khi code.
4. Với `self.op.*`, ưu tiên các primitive causal-safe như `previous`, `shift`, `pct_change`, `bars_since`, `hold_for`.

## Feature Selection Rules

| Strategy need | Feature groups to read first |
|---|---|
| Trend following | Trend, Moving Average, Directional |
| Mean reversion | Statistics, Volatility, Momentum |
| Breakout | Volatility, Rolling Statistics, Price Transforms |
| Session / intraday | Price Transforms, Momentum, Rolling Statistics |
| Cross-market | Statistics, Momentum, Volume / Flow |
| Flow / participation | Volume / Flow, Statistics |

## Operator Selection Rules

| Intent | Operators to prefer |
|---|---|
| Detect crossovers | `crossed_above`, `crossed_below`, `crossed` |
| Compare with prior bar | `previous`, `shift`, `diff`, `pct_change` |
| Keep a signal alive | `hold_for`, `bars_since`, `value_when` |
| Handle missing data | `fillna`, `ffill`, `zero_ifna` |
| Build masks | `between`, `clip`, `where`, `and_`, `or_`, `not_` |

## Anti-Patterns

- Do not use `open` as a variable name; use `open_price`.
- Do not use `SeriesT` or type-hint syntax from docs in generated code.
- Do not rely on future values for signal construction.
- Do not guess tuple output order; check the function entry.

## Minimal Workflow

`idea` -> `hypothesis` -> `feature/operations syntax` -> `strategy_framework` -> code -> validate -> backtest

