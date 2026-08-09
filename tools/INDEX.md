# Tools INDEX — Alpha Bot

## Quick Reference

| Tool | When to use | Command |
|------|------------|---------|
| `system_health_check.md` | Kiểm tra trạng thái hệ thống / sẵn sàng chạy Stage 2 (offline → API read-only → live opt-in) | `agent/system_health_check.md` |
| `generate_strategies.py` | Generate all thesis strategies (vòng 1 — ARCHIVED) | `python tools/generate_strategies.py` |
| `validate_framework.py` | Validate Round-2 files for framework compliance (quét `output/stage_2/`) | `python tools/validate_framework.py` |
| `submit_and_check.py` | Submit Round-2 strategies to XNOQuant + fetch metrics | `python tools/submit_and_check.py [--batch \| --files ...] [--dry-run] [--universe VN-...]` |
| `check_results.py` | Review Round-2 backtest results (`backtest/results_stage_2.csv`) | `python tools/check_results.py [--detail \| --pass \| --universe ...]` |
| `backfill_split_metrics.py` | GET-only audit/backfill Aggregate + Train + Test cho row cũ | `python tools/backfill_split_metrics.py [--universe ...] [--prefix ...] [--write]` |
| `retention_audit.py` | Multiple-testing math + parameter plateau theo family (CSV-only) | `python tools/retention_audit.py [--plateau] [--universe ...]` |
| `fetch_yearly_tables.py` | GET-only yearly `summary-table` + Gate 1–3 (stability / 2022 / 2024) | `python tools/fetch_yearly_tables.py --strategy-id <id> [--from-csv-prefix ...]` |
| `update_guide_stats.py` | Regenerate Round-2 strategy stats from `output/index.csv` | `python tools/update_guide_stats.py` |
| `gen_single_feat.py` | Generate a single-feature alpha strategy (vòng 1 — ARCHIVED) | `python tools/gen_single_feat.py <indicator> <call> <threshold>` |
| `common.py` | Shared helpers (imported by other tools, not standalone) | — |
| `INDEX.md` | This file — tool reference guide | — |

---

## Core Pipeline

The standard Round-2 pipeline (agent writes strategies directly, no code generator):

```
1. Agent writes strategy -> output/stage_2/<cap>/<mode>/  (+ row in output/index.csv)
2. python tools/validate_framework.py --strict            # Validate Round-2 compliance (strict)
3. python tools/submit_and_check.py --batch --dry-run --universe VN-...  # Preview (no HTTP)
   # Choose universe on XNOQuant UI manually -> live: --batch --test / --batch
4. python tools/check_results.py --detail                 # Aggregate + Train/Test PASS/FAIL
5. python tools/update_guide_stats.py                     # Update strategy count stats
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
- **Checks:** Required structure (`CustomStrategy`, `__algorithm__`), forbidden patterns (`import`, `print/eval/exec/open(` , loops/lambdas/comprehensions/`.apply`), point-in-time (cấm global aggregations `.mean()/.rank()/.quantile()/.sort_values()`), forbidden timing (`shift` âm, `bfill/backfill`, `center=True`), **mode contract** (detect `set_portfolio_positions` = cross_sectional vs `set_positions` = time_series; CS bắt buộc `portfolio_weights_panel` + `mask`, method ∈ {`rank_demean_l1`, `demean_l1`}), field suffix (`_panel` đúng mode), bounds (`time_series` long-only 0/0.5/1.0, position phải numeric), fundamental guard (`.notna()` + denominator `>0`).
- **`--strict`:** nâng mọi warning lên error, exit 1 — dùng trong pipeline chuẩn.
- **Also checks:** `output/index.csv` (header: `filepath,thesis_group,template,mode,universe,description,params`) consistency — filepath `<cap>/<mode>/<file>.py`, universe khớp cap, không orphan/ghost/duplicate.
- **Không dùng** để check vòng 1 (đã archive tại `output/stage_1/`).

### `submit_and_check.py`

Submit Round-2 strategy code (in `output/stage_2/`) to XNOQuant via API and fetch backtest metrics.

- **Interactive mode:** `python tools/submit_and_check.py` — enter file paths one by one
- **Batch mode:** `python tools/submit_and_check.py --batch` — submit all files in `output/stage_2/`
- **Files mode:** `python tools/submit_and_check.py --files f1.py f2.py` — submit specific files
- **Flags:**
  - `--dry-run` — xem trước editor/universe/files, KHÔNG gọi API (an toàn)
  - `--test` — live submit file đầu tiên của cap (KHÔNG phải dry-run)
  - `--force` — re-submit dù đã có kết quả trước đó
  - `--yes` — bỏ qua xác nhận interactive (chỉ khi đã chắc chắn universe trên UI)
  - `--start N` — start from index N in batch
  - `--limit N` — max N files in batch
  - `--universe VN-...` — FILTER chọn 1 cap (VN-SMALL-CAP / VN-MID-CAP / VN-LARGE-CAP). Universe ghi CSV suy từ path, KHÔNG bị override. Batch trộn nhiều cap không có flag → từ chối.
- **Config:** `.env` in project root — **1 editor per cap** (`XNO_EDITOR_ID_SMALL` / `XNO_EDITOR_ID_MID` / `XNO_EDITOR_ID_LARGE`) + `XNO_TOKEN`; legacy single `XNO_EDITOR_ID` dùng làm fallback. (required — no hardcoded fallbacks)
- **Flow per file:** update → verify → simulate → poll cả `simulate` + `train` + `test` summary (chỉ hoàn tất khi đủ cả ba) → ghi 1 row CSV
- **Idempotency:** skip theo `(filepath, universe)` chỉ khi Aggregate + Train + Test đều PASS; row aggregate-only cũ không bị skip
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
- **Detailed splits:** `python tools/check_results.py --splits`
- **Custom CSV:** `python tools/check_results.py --csv path/to/results.csv`
- PASS/FAIL dùng tiêu chí theo universe; Aggregate, Train và Test phải độc lập đủ 5 metrics và PASS

### `backfill_split_metrics.py`

Chọn row `SIMULATED` mới nhất có `strategy_id` theo `(filepath, universe)`, GET cả ba
summary stage và audit trên console. Mặc định read-only/no CSV writes; thêm `--write`
để append row enriched mới. Hỗ trợ `--universe`, `--prefix`, `.env` `XNO_TOKEN`, và
delay lịch sự giữa strategies. Tool không update/verify/simulate editor.

### `retention_audit.py`

Multiple-testing / retention math + parameter plateau check — đọc `backtest/results_stage_2.csv`,
dedup theo `(filepath, universe)`, nhóm SIMULATED theo family (strip suffix `P<digits>`), và báo
`N / PassTr (Sharpe train ≥ 1.0) / PassBoth / ExpFP (α·PassTr) / Retain`.

- Survival ratio ≈ α = 5% nghĩa là train-pass chủ yếu là may mắn thống kê, không phải edge bền.
- `--plateau --min-variants 3`: bảng train/test của từng variant trong family → phát hiện tham số
  promote có phải **đỉnh cô lập** (overfit) hay thuộc plateau trơn.
- CSV-only, không gọi network. Là Gate 4 + Gate 5 của `idea/planning_alpha/stage_2/2026-08-05_alpha_validation_framework.md`.

```
python tools/retention_audit.py --min-candidates 1
python tools/retention_audit.py --plateau --min-variants 3
python tools/retention_audit.py --universe VN-SMALL-CAP
```

### `fetch_yearly_tables.py`

GET-only yearly `summary-table` cho 1+ strategy (theo `--strategy-id` hoặc chọn từ CSV qua
`--from-csv-prefix` / `--from-csv-universe`). Mỗi stage (simulate/train/test) in bảng theo năm
kèm regime thị trường, và tính **Gate 1–3**:

1. Sharpe ≥ 0 ở ≥ 4/5 năm (2020–24, bỏ row 2025 boundary)
2. Sharpe 2022 ≥ −0.2 (crash resilience — năm trung thực duy nhất trong train)
3. Sharpe 2024 ≥ 0 (năm mới nhất, bắt decay gần đây)

Không ghi CSV, không mutate editor. Yêu cầu `XNO_TOKEN` trong `.env`.

```
python tools/fetch_yearly_tables.py --strategy-id DSbhQzWjPi --strategy-id 6hZhskaS1Y
python tools/fetch_yearly_tables.py --from-csv-prefix VnSmallCsFinancialNetPayout
python tools/fetch_yearly_tables.py --from-csv-universe VN-SMALL-CAP --from-csv-prefix VnSmallCsValueTrend
```

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
- **Parameters:** Archived generator; do not use current parameter docs
  (`syntax/time_series/parameters.md`, `syntax/cross_sectional/parameters.md`,
  canonical for Round-2 daily equity) as a VNFuture 15m reference.

### `common.py`

Shared helpers module used by `submit_and_check.py`, `check_results.py`, and other tools.

- `PASS_THRESHOLDS` — vòng 1: 5-criteria dict (Sharpe ≥ 1.3, CAGR ≥ 15%, MaxDD ≥ -35%, PF ≥ 1.2, Calmar ≥ 1.1)
- `PASS_THRESHOLDS_BY_UNIVERSE` — **Round 2:** bộ tiêu chí riêng cho VN-SMALL-CAP / VN-MID-CAP / VN-LARGE-CAP (user cung cấp)
- `thresholds_for(universe)` — chọn bộ tiêu chí theo universe; **fail-closed:** universe lạ/trống → `KeyError` (hết default)
- `getf(row, key)` — parse float from CSV cell safely
- `is_pass(row)` — PASS chỉ khi `SIMULATED` và cả Aggregate + Train + Test đủ 5 metrics, từng bộ vượt ngưỡng cap
- `status_label(row)` — PASS/FAIL/PENDING/API_ERROR/INVALID_METADATA từ status + metrics
- `row_key(row)` — identity `(filepath, universe)` (thay cho basename — tránh collision giữa cap)
- `load_previous_results(csv_path)` — build {(filepath, universe): is_pass} map
- `format_metrics(metrics)` — format dict to display string
- `build_latest(rows)` — keep latest row per (filepath, universe)
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
| `backfill_split_metrics.py` | Append-only split metrics audit/backfill | Active (V2) |
| `retention_audit.py` | Retention/multiple-testing math + plateau check (CSV-only) | Active (V2) |
| `fetch_yearly_tables.py` | GET-only yearly summary-table + Gate 1–3 stability | Active (V2) |
| `generate_strategies.py` | Master strategy generator (vòng 1 — ARCHIVED) | Archived |
| `gen_single_feat.py` | Single-feature alpha generator (vòng 1 — ARCHIVED) | Archived |
| `INDEX.md` | This file | Active |
