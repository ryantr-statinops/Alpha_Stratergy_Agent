# Tools INDEX — Alpha Bot

## Quick Reference

| Tool | When to use | Command |
|------|------------|---------|
| `generate_strategies.py` | Generate all thesis strategies (vòng 1 — ARCHIVED) | `python tools/generate_strategies.py` |
| `validate_framework.py` | Validate Round-2 files for framework compliance (quét `output/stage_2/`) | `python tools/validate_framework.py` |
| `submit_and_check.py` | Submit Round-2 strategies to XNOQuant + fetch metrics | `python tools/submit_and_check.py [--batch \| --files ...] [--universe VN-...]` |
| `check_results.py` | Review Round-2 backtest results (`backtest/results_stage_2.csv`) | `python tools/check_results.py [--detail \| --pass \| --universe ...]` |
| `update_guide_stats.py` | Regenerate Round-2 strategy stats from `output/index.csv` | `python tools/update_guide_stats.py` |
| `gen_single_feat.py` | Generate a single-feature alpha strategy (vòng 1 — ARCHIVED) | `python tools/gen_single_feat.py <indicator> <call> <threshold>` |
| `common.py` | Shared helpers (imported by other tools, not standalone) | — |
| `INDEX.md` | This file — tool reference guide | — |

---

## Core Pipeline

The standard Round-2 pipeline (agent writes strategies directly, no code generator):

```
1. Agent writes strategy -> output/stage_2/  (+ row in output/index.csv)
2. python tools/validate_framework.py       # Validate Round-2 compliance
3. python tools/submit_and_check.py --batch --universe VN-...  # Submit all to XNOQuant
4. python tools/check_results.py --detail    # Review PASS/FAIL per universe
5. python tools/update_guide_stats.py        # Update strategy count stats
```

---

## Tool Details

### `generate_strategies.py` (VÒNG 1 — ARCHIVED)

Master strategy generator (vòng 1 futures intraday). Reads 38 thesis groups with templates, generates parameter variants.

- **Output:** `output/thesis_NN_name/*.py`, `output/index.csv` (vòng 1)
- **Architecture:** `TEMPLATES` dict with code templates + `inject_filters()` post-processor
- **Round 2 không dùng** — agent viết code trực tiếp theo `agent/framework_build_guide.md`

### `validate_framework.py`

Framework compliance validator per `template_example/strategy_framework.md`.

- **Scope (V2):** quét `output/stage_2/` (Round 2 — Fundamental Alpha Arena) + manifest `output/index.csv`.
- **Checks:** Required structure (`CustomStrategy`, `__algorithm__`), forbidden patterns (`pandas`, `SeriesT`, `open` variable, loops/lambdas/`.apply`), point-in-time (cấm global aggregations `.mean()/.rank()/.quantile()/.sort_values()`), **mode contract** (detect `set_portfolio_positions` = cross_sectional vs `set_positions` = time_series), field suffix (`_panel` đúng mode), bounds (`time_series` long-only 0/0.5/1.0).
- **Also checks:** `output/index.csv` (header: `filepath,thesis_group,template,mode,universe,description,params`) consistency against files on disk.
- **Không dùng** để check vòng 1 (đã archive tại `output/stage_1/`).

### `submit_and_check.py`

Submit Round-2 strategy code (in `output/stage_2/`) to XNOQuant via API and fetch backtest metrics.

- **Interactive mode:** `python tools/submit_and_check.py` — enter file paths one by one
- **Batch mode:** `python tools/submit_and_check.py --batch` — submit all files in `output/stage_2/`
- **Files mode:** `python tools/submit_and_check.py --files f1.py f2.py` — submit specific files
- **Flags:**
  - `--test` — only submit first file (dry-run)
  - `--force` — re-submit even if already passed
  - `--start N` — start from index N in batch
  - `--limit N` — max N files in batch
  - `--universe VN-...` — universe tag written to CSV (VN-SMALL-CAP / VN-MID-CAP / VN-LARGE-CAP) — used for pass thresholds
- **Config:** `.env` in project root with `XNO_EDITOR_ID` and `XNO_TOKEN` (required — no hardcoded fallbacks)
- **Results:** `backtest/results_stage_2.csv`

See `agent/submit_workflow.md` for detailed setup and API reference.

### `check_results.py`

Consolidated Round-2 results checker — reads `backtest/results_stage_2.csv` by default.

- **All results:** `python tools/check_results.py`
- **Filter by prefix:** `python tools/check_results.py --prefix VnTop`
- **Filter by universe:** `python tools/check_results.py --universe VN-SMALL-CAP`
- **Today only:** `python tools/check_results.py --today`
- **PASS/FAIL only:** `python tools/check_results.py --pass` / `--fail`
- **Full metrics:** `python tools/check_results.py --detail`
- **Custom CSV:** `python tools/check_results.py --csv path/to/results.csv`
- PASS/FAIL dùng tiêu chí theo universe (xem `common.py` `PASS_THRESHOLDS_BY_UNIVERSE`)

### `update_guide_stats.py`

Count Round-2 strategies from `output/index.csv` and generate `output/STATS.md`.

- `python tools/update_guide_stats.py` — generate STATS.md only

### `gen_single_feat.py` (VÒNG 1 — ARCHIVED)

Generate a single-feature alpha strategy file following the trend-following pattern.

```
python tools/gen_single_feat.py rsi "rsi(close, timeperiod=14)" 50
python tools/gen_single_feat.py cci "cci(high, low, close, timeperiod=20)" 0 --data "high low"
```

- **Output:** `output/single_feat_alpha/SF_<INDICATOR>_15min.py`
- **Parameters:** Read from `syntax/parameters.md` for 15min VNFuture (vòng 1)

### `common.py`

Shared helpers module used by `submit_and_check.py`, `check_results.py`, and other tools.

- `PASS_THRESHOLDS` — vòng 1: 5-criteria dict (Sharpe ≥ 1.3, CAGR ≥ 15%, MaxDD ≥ -35%, PF ≥ 1.2, Calmar ≥ 1.1)
- `PASS_THRESHOLDS_BY_UNIVERSE` — **Round 2:** bộ tiêu chí riêng cho VN-SMALL-CAP / VN-MID-CAP / VN-LARGE-CAP (user cung cấp)
- `thresholds_for(universe)` — chọn bộ tiêu chí theo universe
- `getf(row, key)` — parse float from CSV cell safely
- `is_pass(row, universe=None)` — check thresholds theo universe (mặc định lấy từ cột `universe` của row)
- `load_results_csv(path)` — load and parse CSV
- `load_previous_results(csv_path)` — build {filename: is_pass} map
- `format_metrics(metrics)` — format dict to display string
- `build_latest(rows)` — keep latest row per filename
- `timestamp_today()` — today's date string

---

## File Reference

| File | Purpose | Status |
|------|---------|--------|
| `common.py` | Shared helpers (PASS_THRESHOLDS_BY_UNIVERSE, is_pass, ...) | Active (V2) |
| `validate_framework.py` | Round-2 compliance validator (mode contract, point-in-time) | Active (V2) |
| `submit_and_check.py` | XNOQuant submission + metrics fetcher (`output/stage_2/` → `results_stage_2.csv`) | Active (V2) |
| `update_guide_stats.py` | Round-2 stats generator từ `output/index.csv` | Active (V2) |
| `check_results.py` | Round-2 results checker (theo universe) | Active (V2) |
| `generate_strategies.py` | Master strategy generator (vòng 1 — ARCHIVED) | Archived |
| `gen_single_feat.py` | Single-feature alpha generator (vòng 1 — ARCHIVED) | Archived |
| `INDEX.md` | This file | Active |