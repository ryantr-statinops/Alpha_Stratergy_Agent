# Tools

The research rounds are complete. Run package entry points from the repository root with `python -m ...`.

## Round 1 — generators

| Utility | Command |
|---|---|
| Strategy generator | `python -m tools.round_1.generate_strategies` |
| Single-feature generator | `python -m tools.round_1.gen_single_feat <indicator> <feature-call> <threshold>` |

The local backtest engine is in `src/backtest/` and is documented in `src/backtest/README.md`.

## Round 2 — validation

| Utility | Command |
|---|---|
| Framework validator | `python -m tools.round_2.validation.validate_framework [--strict]` |
| Offline validation pipeline | `python -m tools.round_2.validation.alpha_gate` |
| Factor diagnostics | `python -m tools.round_2.validation.factor_diagnostics` |
| Economic validation | `python -m tools.round_2.validation.economic_validation` |

## Round 2 — results

| Utility | Command |
|---|---|
| Results report | `python -m tools.round_2.results.check_results` |
| Retention audit | `python -m tools.round_2.results.retention_audit` |
| Regenerate strategy stats | `python -m tools.round_2.results.update_guide_stats` |

## Round 2 — XNOQuant

| Utility | Command | Network behavior |
|---|---|---|
| Submit and fetch metrics | `python -m tools.round_2.xnoquant.submit_and_check` | Live submission can mutate an external editor and call the API |
| Backfill split metrics | `python -m tools.round_2.xnoquant.backfill_split_metrics` | Read-only unless `--write` is supplied |
| Fetch yearly tables | `python -m tools.round_2.xnoquant.fetch_yearly_tables` | GET-only API calls |

Shared result parsing and pass criteria live in `tools/shared/common.py`. XNOQuant settings continue to load from the root `.env`.
