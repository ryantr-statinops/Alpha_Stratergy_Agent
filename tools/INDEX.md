# Tools INDEX — Alpha Bot

## Quick Reference

| Tool | When to use | Command |
|------|------------|---------|
| `generate_strategies.py` | Generate all thesis strategies | `python tools/generate_strategies.py` |
| `validate_framework.py` | Validate generated files for framework compliance | `python tools/validate_framework.py` |
| `submit_and_check.py` | Submit strategies to XNOQuant and fetch metrics | `python tools/submit_and_check.py [--batch \| --files ...]` |
| `check_results.py` | Review backtest results from CSV | `python tools/check_results.py [--detail \| --pass \| --today]` |
| `update_guide_stats.py` | Regenerate strategy count stats | `python tools/update_guide_stats.py [--patch]` |
| `gen_single_feat.py` | Generate a single-feature alpha strategy | `python tools/gen_single_feat.py <indicator> <call> <threshold>` |
| `common.py` | Shared helpers (imported by other tools, not standalone) | — |
| `INDEX.md` | This file — tool reference guide | — |

---

## Core Pipeline

The standard generation → validation → submission → review flow:

```
1. python tools/generate_strategies.py     # Generate strategy files
2. python tools/validate_framework.py      # Validate framework compliance
3. python tools/submit_and_check.py --batch # Submit all to XNOQuant
4. python tools/check_results.py --detail   # Review PASS/FAIL metrics
5. python tools/update_guide_stats.py       # Update strategy count stats
```

---

## Tool Details

### `generate_strategies.py`

Master strategy generator. Reads 38 thesis groups with templates, generates parameter variants.

- **Output:** `output/thesis_NN_name/*.py`, `output/index.csv`
- **Architecture:** `TEMPLATES` dict with code templates + `inject_filters()` post-processor
- **Modification:** All code changes go here — NEVER patch output files directly

### `validate_framework.py`

Framework compliance validator per `template_example/strategy_framework.md`.

- **Checks:** Required structure (`CustomStrategy`, `__algorithm__`, `set_positions`), forbidden patterns (`pandas`, `SeriesT`, `open` variable), set_positions order (Exit → Long → Short)
- **Also checks:** `output/index.csv` consistency against files on disk

### `submit_and_check.py`

Submit strategy code to XNOQuant via API and fetch backtest metrics.

- **Interactive mode:** `python tools/submit_and_check.py` — enter file paths one by one
- **Batch mode:** `python tools/submit_and_check.py --batch` — submit all discovered files
- **Files mode:** `python tools/submit_and_check.py --files f1.py f2.py` — submit specific files
- **Flags:**
  - `--test` — only submit first file (dry-run)
  - `--force` — re-submit even if already passed
  - `--start N` — start from index N in batch
  - `--limit N` — max N files in batch
- **Config:** Create `.env` in project root with `XNO_EDITOR_ID` and `XNO_TOKEN`

See `agent/submit_workflow.md` for detailed setup and API reference.

### `check_results.py`

Consolidated results checker — replaces the legacy `check_detail.py`, `check_files.py`, `check_new.py`, `check_today.py`, `report_results.py`.

- **All results:** `python tools/check_results.py`
- **Filter by prefix:** `python tools/check_results.py --prefix MF`
- **Filter by glob:** `python tools/check_results.py --pattern 'MF_*'`
- **Today only:** `python tools/check_results.py --today`
- **PASS/FAIL only:** `python tools/check_results.py --pass` / `--fail`
- **Full metrics:** `python tools/check_results.py --detail`
- **Custom CSV:** `python tools/check_results.py --csv path/to/results.csv`

### `update_guide_stats.py`

Count strategy files and generate `output/STATS.md`. Optionally patch `agent/GUIDE.md` with placeholder values.

- `python tools/update_guide_stats.py` — generate STATS.md only
- `python tools/update_guide_stats.py --patch` — also update GUIDE.md placeholders

### `gen_single_feat.py`

Generate a single-feature alpha strategy file following the trend-following pattern.

```
python tools/gen_single_feat.py rsi "rsi(close, timeperiod=14)" 50
python tools/gen_single_feat.py cci "cci(high, low, close, timeperiod=20)" 0 --data "high low"
```

- **Output:** `output/single_feat_alpha/SF_<INDICATOR>_15min.py`
- **Parameters:** Read from `syntax/parameters.md` for 15min VNFuture

### `common.py`

Shared helpers module used by `submit_and_check.py`, `check_results.py`, and other tools.

- `PASS_THRESHOLDS` — 5-criteria dict (Sharpe ≥ 1.3, CAGR ≥ 15%, MaxDD ≥ -35%, PF ≥ 1.2, Calmar ≥ 1.1)
- `getf(row, key)` — parse float from CSV cell safely
- `is_pass(row)` — check all 5 thresholds
- `load_results_csv(path)` — load and parse CSV
- `load_previous_results(csv_path)` — build {filename: is_pass} map
- `format_metrics(metrics)` — format dict to display string
- `build_latest(rows)` — keep latest row per filename
- `timestamp_today()` — today's date string

---

## File Reference

| File | Purpose | Status |
|------|---------|--------|
| `common.py` | Shared helpers (PASS_THRESHOLDS, getf, is_pass, ...) | Active |
| `generate_strategies.py` | Master strategy generator | Active |
| `validate_framework.py` | Framework compliance validator | Active |
| `submit_and_check.py` | XNOQuant submission + metrics fetcher | Active |
| `update_guide_stats.py` | Strategy count stats generator | Active |
| `gen_single_feat.py` | Single-feature alpha generator | Active |
| `check_results.py` | Consolidated results checker | Active |
| `INDEX.md` | This file | Active |