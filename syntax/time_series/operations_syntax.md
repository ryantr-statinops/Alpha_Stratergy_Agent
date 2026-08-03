# Time-Series Operations Syntax

Canonical location for `SeriesT` operations used through `self.op` in Round 2 `time_series` strategies.

> **Inventory status:** awaiting the authoritative time-series operation API list. No operation is declared supported merely because a similarly named panel operation exists.

## Contract

- Inputs and outputs must be `SeriesT` unless explicitly documented otherwise.
- Time-dependent operations must be causal; negative shifts, centered windows, and backfill are forbidden.
- Strategy logic uses bitwise `&`, `|`, and `~` for vectorized Boolean composition.
- Native arithmetic and comparison operators are preferred where supported.
- Every operation added here must document signature, output, axis, missing behavior, causal constraints, and evidence status.

## Evidence Labels

| Label | Meaning |
|---|---|
| `CATALOG_ONLY` | Present in the authoritative API inventory |
| `VERIFY_PASSED` | Accepted by XNOQuant verify |
| `SIMULATE_PASSED` | Used in a completed simulation |
| `BEHAVIOR_VERIFIED` | Edge behavior and output semantics were checked |

## Pending Inventory

Do not generate undocumented `self.op` calls from this file. Existing strategy examples may provide evidence, but they are not a substitute for the complete authoritative operation catalog.
