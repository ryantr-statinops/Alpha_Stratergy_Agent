# Stage 2 Sharpe Diagnostic Audit — VN-LARGE-CAP

> **Date:** 2026-08-02
> **Scope:** GET-only API/schema audit + repository static analysis. No strategy
> update, verify or simulate request was made during the API audit.

## Executive finding

Không có bằng chứng về hard cap Sharpe quanh `1.1`. Bốn candidate mạnh đều đạt
Sharpe cao trong 2020–2021 nhưng cùng thất bại trong 2022 và chỉ phục hồi vừa
phải trong 2023–2024. Aggregate Sharpe thấp chủ yếu là **regime robustness
failure chung của long-only trend/beta architecture**, không phải parameter hoặc
công thức metric khóa cứng.

## Read-only API inventory

Các GET endpoint đã xác nhận hoạt động:

```text
/xalpha-api/v2/editors/{editor_id}/info
/xalpha-api/v1/strategies/{strategy_id}/stages/simulate/summary-aggregate
/xalpha-api/v1/strategies/{strategy_id}/stages/simulate/summary-table
/xalpha-api/v1/strategies/{strategy_id}/stages/train/summary-aggregate
/xalpha-api/v1/strategies/{strategy_id}/stages/train/summary-table
```

`summary-aggregate.data` keys:

```text
cagr, sharpe, calmar, max_drawdown, profit_factor, from_time, to_time
```

`summary-table.data` là list yearly rows với keys:

```text
time, cagr, sharpe, calmar, max_drawdown, profit_factor
```

Không tìm thấy endpoint/documented key cho:

- Daily returns hoặc NAV/equity curve.
- Daily positions/weights.
- Trades/fills.
- Turnover hoặc fee breakdown.
- Benchmark return/beta.
- Universe constituents.
- Sector/industry metadata.

## Annual stability evidence

### ROA candidate

| Year | CAGR | Sharpe |
|---:|---:|---:|
| 2020 | 66.4% | 2.007 |
| 2021 | 55.9% | 1.695 |
| 2022 | -8.0% | -0.325 |
| 2023 | 12.9% | 0.664 |
| 2024 | 10.2% | 0.750 |
| 2025 | 0.0% | 0.000 |

### ProfitReport candidate

| Year | CAGR | Sharpe |
|---:|---:|---:|
| 2020 | 44.2% | 1.686 |
| 2021 | 55.6% | 1.990 |
| 2022 | -18.2% | -0.866 |
| 2023 | 18.5% | 1.106 |
| 2024 | 11.0% | 0.881 |
| 2025 | 0.0% | 0.000 |

### DualTrend candidate

| Year | CAGR | Sharpe |
|---:|---:|---:|
| 2020 | 46.5% | 1.759 |
| 2021 | 43.5% | 1.438 |
| 2022 | -11.1% | -0.756 |
| 2023 | 13.4% | 0.878 |
| 2024 | 11.7% | 1.059 |
| 2025 | 0.0% | 0.000 |

### MACD candidate

| Year | CAGR | Sharpe |
|---:|---:|---:|
| 2020 | 40.8% | 1.765 |
| 2021 | 45.7% | 1.931 |
| 2022 | -13.5% | -0.654 |
| 2023 | 16.4% | 1.146 |
| 2024 | 10.4% | 0.790 |
| 2025 | 0.0% | 0.000 |

Aggregate `from_time/to_time` của cả bốn run là `2020-01-03` đến
`2025-01-01`. Vì 2025 chỉ chứa boundary day, row `2025 = 0` không đại diện cho
một năm performance và phải bị loại khỏi stability interpretation.

## Root causes ranked

### 1. Common long-only beta/trend exposure — very high likelihood

Phần lớn 20 strategy dùng cùng architecture: positive fundamental eligibility +
EMA trend + fixed position tiers. Fundamental thay đổi nhưng P&L source vẫn là
long large-cap trend. Annual tables xác nhận cả bốn candidate cùng thắng/thua ở
các năm giống nhau, đặc biệt cùng âm trong 2022.

### 2. Fundamental filters are too coarse — very high likelihood

Nhiều strategy chỉ dùng `EPS > 0`, `CFO > 0`, `ROA > 0`. Earnings yield dương
gần như lặp lại EPS dương khi giá dương. Các filter này loại doanh nghiệp xấu
nhưng chưa tạo valuation/quality magnitude độc lập.

### 3. No volatility-aware sizing — high likelihood

Position `0/0.25/0.5/1` là capital tiers, không normalize risk giữa symbols.
Repository không biết XNOQuant aggregate per-symbol positions như thế nào, nên
high-vol constituents có thể chi phối aggregate variance.

### 4. Turnover from daily tier resizing — high likelihood

Volume-driven strong state có thể đổi `0.5 ↔ 1` thường xuyên. Scoring được mô tả
là net-of-fees nhưng API không trả gross return, turnover hoặc fees, nên chưa thể
định lượng drag.

### 5. Sector/accounting heterogeneity — high likelihood

CFO, CFO/profit, ROA và equity/assets không có cùng meaning cho bank, insurance,
securities và non-financial. Không có sector mask/map trong API hiện biết.

### 6. Fundamental staleness/event sparsity — medium/high likelihood

Annual state quá stale; report-step chỉ có thông tin ở ngày report. Wave 1 xác
nhận report-step hoạt động tốt hơn khi chỉ là strong overlay, không phải core
holding condition.

### 7. Metric/aggregation opacity — medium likelihood, not proven defect

Round-2 Sharpe formula, annualization, cash handling, execution lag, universe
weighting và fees không được định nghĩa trong repository. Local Round-1 evaluator
không đại diện cho XNOQuant Round 2.

## What can be measured locally now

- Aggregate and yearly CAGR/Sharpe/Calmar/MaxDD/PF.
- Field/operator/profile overlap as a correlation proxy.
- Static churn-risk score from tier/volume logic.
- Accounting-archetype applicability flags.
- Result/manifest completeness and duplicate history.

Không thể tính exact correlation, beta, turnover, sector attribution hoặc risk
contribution nếu không có daily NAV/returns + positions + constituent metadata.

## Required diagnostic export

Minimum data cần lấy từ platform/UI:

1. Daily net NAV/returns per strategy.
2. Daily benchmark returns.
3. Daily target/realized positions by symbol.

Sau đó mới tính được:

- Pairwise return correlation/PCA.
- Beta và residual alpha.
- Turnover/fee drag.
- Symbol contribution-to-risk.
- Sector attribution và eligible breadth.

## Wave 2 recommendation

Không tiếp tục random EMA tuning. Wave 2 phải kiểm tra **2022 defense**:

1. Profile B price/volume strategies dùng rolling return 3 và explicit exit.
2. Profile D/E quality strategies thử 14/42, 18/54, 30/90 theo archetype.
3. Không dùng `pv_vn30_close` regime gate vì live test đã tạo degenerate result.
4. Không giữ volume tier nếu yearly/aggregate risk-adjusted metrics không tăng.
5. Mỗi variant phải so annual table, đặc biệt 2022, không chỉ aggregate.

Sharpe `1.2` vẫn khả thi: ROA hiện chỉ thiếu khoảng `0.105`, nhưng cần giảm
common-regime loss thay vì tăng exposure trong 2020–2021.

## Confirmed OOS status (audit refresh)

Kiểm lại ngày 2026-08-04 với `tools/check_results.py --pass --universe ...` trên
`backtest/results_stage_2.csv` (split-metric):

- **VN-MID-CAP: 0/13 PASS** — `No matching results found`.
- **VN-SMALL-CAP: 0/47 PASS** — `No matching results found`.
- Gần đạt nhất: `VnSmallCsValueTrendP02` (SMALL, cross_sectional) — Test CAGR
  ~12.10%, PF ~1.273 so với yêu cầu 25% / 1.30.

Ưu tiên tiếp theo (không chạy thêm từ đây được — cần live XNOQuant):

1. **Verify runtime ops trước** — hầu hết `self.op.*` mới chỉ `CATALOG_ONLY`
   (`syntax/*/operations_syntax.md`, mục Evidence Status). Chạy probe verify/simulate
   để promote `EXAMPLE_VERIFIED` → `VERIFY_PASSED`/`SIMULATE_PASSED` trước khi dựng
   chiến lược mới.
2. **Wave 2 defense 2022** theo mục "Wave 2 recommendation" ở trên.
3. Mỗi variant mới phải so annual table (đặc biệt 2022), không chỉ aggregate.

## Security noteGit history có dấu hiệu từng chứa credential hard-coded đã bị xóa khỏi worktree.
Nếu credential đó từng là thật, cần revoke/rotate; xóa khỏi file hiện tại không
xóa khỏi Git history.
