# Alpha Ideas — Batch 4 (Round 2, 20 time-series long-only alpha cho VN-LARGE-CAP)

> **Session:** 2026-08-01
> **Trạng thái:** 🚀 Đang gen (thay thế Batch 3 cross-sectional — đã xóa, vì 0/20 pass)
> **Mục đích:** Chuyển hoàn toàn sang **`time_series` long-only** — đánh từng cổ phiếu VN-LARGE-CAP độc lập (không short, không market-neutral), đúng cách giao dịch cổ phiếu Việt Nam thực tế. Fundamental xác định *cổ phiếu nào*, trend/volume xác định *khi nào*, exit chủ động khi xu hướng/fundamental suy yếu.
> **Universe:** VN-LARGE-CAP (daily)

---

## Vì sao chuyển từ cross_sectional → time_series

| Cross_sectional (batch 2-3) | Time_series (batch 4) |
|---|---|
| `portfolio_weights_panel` long+short | `set_positions` long-only `[0, 1]` |
| Short leg khiến kết quả âm (Liquidity -1.93, LowVol -1.20, VolumeZ -0.97) | Không short — chỉ giữ 0→1 |
| Rank ngành chéo (ngân hàng vs sản xuất) không chuẩn | Từng cổ phiếu tự quyết định, không so chéo |
| Level ratio tĩnh bị thị trường định giá hết | Fundamental là filter, price/volume quyết định entry |
| VN không phổ biến short cổ phiếu cơ sở | Long-only phản ánh thị trường thực |

**Nguồn:** `data/vietnam_market_characteristics.md` (§1 retail 80-90%, §2 large-cap ưu tiên cash flow/value + trend xác nhận) — KHÔNG áp dụng `vietnam_market_characteristics_v1.md` (futures intraday legacy: ADX/session/ATC/basis).

## Contract code

```python
class CustomStrategy(SimpleAlgorithm):
    def __algorithm__(self):
        close = self.data.pv_close              # field KHÔNG suffix
        volume = self.data.pv_volume
        <fundamental field> = self.data.fun_*_quarterly/annual   # không suffix

        ema_fast = self.feat.ema(close, timeperiod=8)     # 8 hoặc 12
        ema_slow = self.feat.ema(close, timeperiod=24)    # 24 hoặc 36
        vol_base = self.feat.sma(volume, timeperiod=20)   # 10 hoặc 20

        <quality> = ...                                    # CFO/ROE/EY...
        base_entry = <quality> & (close > ema_slow) & (ema_fast > ema_slow)
        strong_entry = base_entry & (volume > vol_base)
        exit_setup = (close < ema_slow) | (ema_fast < ema_slow) | <fundamental suy yếu>

        self.set_positions(exit_setup, position=0)     # exit ưu tiên trước
        self.set_positions(base_entry, position=0.5)
        self.set_positions(strong_entry, position=1)
```

**Quy tắc:**
- Position `[0, 0.5, 1]`, long-only. Exit đặt trước entry.
- Chỉ dùng field không suffix cho time_series (`pv_close`, `pv_volume`, `fun_*_quarterly/annual`).
- Point-in-time: dùng `self.op.notna(...)` cho fundamentals; không zero-fill, không backfill, không shift âm.
- Tham số chỉ trong bộ chuẩn `syntax/time_series/parameters.md`: EMA 8/12/24/36, SMA vol 10/20, RSI 7/9, MACD 8/21/5, ATR 14, pct_change periods=1.
- Không import, không loop/lambda/apply, không `.mean()/.rank()/.quantile()` toàn chuỗi.

## Field đã verify (data_syntax.md)

| Nhóm | Field (time_series) | Field (panel) |
|---|---|---|
| Price | `pv_close`, `pv_volume`, `pv_high`, `pv_low` | `pv_close_panel`, ... |
| Income | `fun_is_eps_basis_quarterly`, `fun_is_net_profit_loss_after_tax_quarterly` | `_panel` |
| Income A | `fun_is_net_profit_loss_after_tax_annual` | `_panel` |
| Balance | `fun_bs_owners_equity_quarterly`, `fun_bs_total_assets_quarterly`, `fun_bs_equity...` | `_panel` |
| Cash flow A | `fun_cf_net_cash_inflows_outflows_from_operating_activities_annual` | `_panel` |

> Chỉ dùng field đã xác nhận tồn tại; `annual` cho đại lượng ổn định (CFO), `quarterly` cho trigger/report change.

---

## 20 Alpha

### Nhóm A — Trend Baseline (1–5) — không fundamental, đo edge thuần trend+volume

| # | File | Entry | Strong | Exit |
|---:|---|---|---|---|
| 1 | `VnLargeTrendVolume824` | close > EMA24 & EMA8 > EMA24 | + vol > SMA10 | close < EMA24 |
| 2 | `VnLargeTrendVolume1236` | close > EMA36 & EMA12 > EMA36 | + vol > SMA20 | EMA12 < EMA36 |
| 3 | `VnLargeDualTrend` | EMA8 > EMA24 & EMA12 > EMA36 | + close > EMA36 | EMA8 < EMA24 |
| 4 | `VnLargeMacdTrend` | MACD 8/21/5 > 0 & EMA8 > EMA24 | + close > EMA24 | MACD < 0 |
| 5 | `VnLargeRsiTrend` | RSI9 trong vùng momentum (50-75) & EMA12 > EMA36 | + close > EMA36 | RSI < 45 |

### Nhóm B — Cash-Flow Quality (6–10) — core thesis large-cap

| # | File | Entry | Strong | Exit |
|---:|---|---|---|---|
| 6 | `VnLargeCashFlowTrend` | CFO annual > 0 & close > EMA24 | + EMA8 > EMA24 | CFO < 0 or close < EMA24 |
| 7 | `VnLargeCashFlowVolume` | CFO > 0 & EMA12 > EMA36 | + vol > SMA20 | CFO < 0 or EMA12 < EMA36 |
| 8 | `VnLargeCashReturnTrend` | CFO/TA annual > 0.02 & close > EMA24 | + EMA8 > EMA24 | CFO/TA < 0 or close < EMA24 |
| 9 | `VnLargeCashConversionTrend` | CFO/NP annual > 0.5 & close > EMA36 | + EMA12 > EMA36 | CFO < 0 or NP < 0 |
| 10 | `VnLargeStableCashQuality` | CFO > 0 & NP quarterly > 0 & EMA12 > EMA36 | + vol > SMA20 | NP < 0 or EMA12 < EMA36 |

### Nhóm C — Value & Profitability (11–15)

| # | File | Entry | Strong | Exit |
|---:|---|---|---|---|
| 11 | `VnLargeEarningsYieldTrend` | EPS > 0 & close > EMA24 & EY dương | + EMA8 > EMA24 | EPS < 0 or close < EMA24 |
| 12 | `VnLargeEarningsYieldVolume` | EPS > 0 & EY dương & EMA12 > EMA36 | + vol > SMA20 | EMA12 < EMA36 |
| 13 | `VnLargeRoaTrend` | ROA annual > 0.01 & close > EMA24 | + EMA8 > EMA24 | ROA < 0 or close < EMA24 |
| 14 | `VnLargeRoeTrend` | ROE quarterly > 0.02 & EMA12 > EMA36 | + vol > SMA20 | ROE < 0 or EMA12 < EMA36 |
| 15 | `VnLargeCapitalStrengthTrend` | Equity/TA annual > 0.3 & EMA8 > EMA24 | + close > EMA24 | Equity/TA < 0.2 or EMA8 < EMA24 |

### Nhóm D — Report Reaction & Institutional (16–20)

| # | File | Entry | Strong | Exit |
|---:|---|---|---|---|
| 16 | `VnLargeEpsReportMomentum` | EPS q/q tăng & close > EMA24 | + vol > SMA10 | EPS giảm mạnh or close < EMA24 |
| 17 | `VnLargeProfitReportMomentum` | NP q/q tăng & EMA8 > EMA24 | + close > EMA24 | NP giảm mạnh or EMA8 < EMA24 |
| 18 | `VnLargeBreakoutCashFlow` | close > Donchian upper & CFO > 0 | + vol > SMA20 | close < EMA24 |
| 19 | `VnLargePullbackQuality` | CFO > 0 & EMA8 > EMA24 & close ≥ EMA24 (pullback) | + RSI7 không quá mua | close < EMA24 |
| 20 | `VnLargeValueCashTrend` | EY dương & CFO > 0 & EMA8 > EMA24 | + vol > SMA20 | CFO < 0 or EMA8 < EMA24 |

---

## Tiêu chí đánh giá sau submit

| Mức | Điều kiện |
|---|---|
| PASS | Đạt hết threshold LARGE (Sharpe≥1.2, CAGR≥15%, MaxDD≥-35%, PF≥1.2, Calmar≥1.1) |
| Candidate | Sharpe ≥ 1.0 & CAGR ≥ 12% |
| Research | Sharpe ≥ 0.6 & MaxDD hợp lý |
| Reject | Sharpe < 0 hoặc không tạo giao dịch |

**Đích cuối:** tất cả 20 phải PASS; các strategy gần chuẩn sẽ được cải thiện tham số/threshold tới khi PASS.

## Quy trình implement

1. ✅ Dọn Batch 3 (xóa 20 file + index + CSV + plan).
2. Viết plan này.
3. Gen 20 file vào `output/stage_2/vn_large_cap/time_series/`.
4. Thêm 20 dòng `time_series` vào `output/index.csv`.
5. `python tools/validate_framework.py --strict` → 0 issues.
6. Dry-run đúng 20 file → submit live qua editor LARGE.
7. Tổng hợp PASS/FAIL, xếp hạng Sharpe/CAGR, phân tích theo nhóm A-D.

---

## Research log — Improvement Round 1

Đã chạy ablation có kiểm soát trên bốn baseline mạnh nhất.

### Thay đổi bị loại

- Thêm ROA guard vào `DualTrend`: giảm CAGR/Sharpe/Calmar.
- Thêm dual trend vào `RoaTrend` và `CashConversionTrend`: giảm hiệu quả.
- Chuyển tiered sizing thành binary full-only: giảm CAGR, không tăng Sharpe đủ.
- Weak-size `0.25` không tổng quát cho DualTrend/CashConversion/TrendVolume.
- Volume SMA20 kém SMA10 trong `TrendVolume824`.
- Cash conversion `0.75` không tốt hơn `0.5`.
- EMA10/30 và EMA12/36 trên ROA kém EMA8/24 về Sharpe/Calmar.
- `pv_vn30_close` làm regime gate tạo gần như không có giao dịch; không dùng.

Các code variant bị loại đã được khôi phục về baseline; CSV chỉ giữ kết quả đại
diện cho code hiện hành và candidate được giữ.

### Thay đổi được giữ

`VnLargeRoaTrend`:

- Nới annual ROA threshold từ `> 0.01` xuống `> 0`.
- Giảm weak-regime position từ `0.5` xuống `0.25`.
- Giữ EMA8/24 và strong position `1.0`.

Kết quả tốt nhất hiện tại:

| CAGR | Sharpe | Calmar | MaxDD | PF |
|---:|---:|---:|---:|---:|
| 19.41% | 1.095 | 1.175 | -16.52% | 1.318 |

Strategy đã đạt CAGR, Calmar, MaxDD và PF; còn thiếu Sharpe `1.2`.

### Infrastructure note

`VnLargeMacdTrend` từng timeout hai lần do dùng sai multi-output MACD contract.
Lỗi đã được sửa và metrics hiện sẵn sàng (xem phần MACD contract fix bên dưới).

## Canonical profile mapping

Mapping này dùng `syntax/time_series/parameters.md` làm nguồn canonical cho các wave tiếp
theo. Profile là baseline nghiên cứu, không tự động thay parameter đã có bằng
mọi giá nếu ablation thực tế cho kết quả xấu hơn.

| Strategy | Canonical profile | Primary parameter family |
|---|---|---|
| `VnLargeTrendVolume824` | B — Price/Volume Trend | EMA10/30, volume20, return3 |
| `VnLargeTrendVolume1236` | B/C adjacent | EMA12/36, volume20, return3 |
| `VnLargeDualTrend` | Multi-horizon exception | EMA8/24 + EMA12/36 |
| `VnLargeMacdTrend` | A — Active Momentum | MACD8/21/5, EMA8/24 |
| `VnLargeRsiTrend` | A — Active Momentum | EMA7/21, RSI7 or RSI9 |
| `VnLargeCashFlowTrend` | D — Cash-Flow Quality | EMA14/42 |
| `VnLargeCashFlowVolume` | D — Cash-Flow Quality | EMA14/42, volume20 |
| `VnLargeCashReturnTrend` | D — Cash-Flow Quality | EMA14/42 or 18/54 |
| `VnLargeCashConversionTrend` | D — Cash-Flow Quality | EMA14/42, conversion0.5 |
| `VnLargeStableCashQuality` | E — Stable Quality Hold | EMA30/90 |
| `VnLargeEarningsYieldTrend` | C — Balanced Fundamental | EMA12/36 |
| `VnLargeEarningsYieldVolume` | C — Balanced Fundamental | EMA12/36, volume20 |
| `VnLargeRoaTrend` | D with retained candidate exception | Test 14/42, retain EMA8/24 if worse |
| `VnLargeRoeTrend` | C — Balanced Fundamental | EMA12/36, volume20 optional |
| `VnLargeCapitalStrengthTrend` | E — Stable Quality Hold | EMA30/90 or adjacent 18/54 |
| `VnLargeEpsReportMomentum` | A — Active Momentum | EMA8/24, volume10 |
| `VnLargeProfitReportMomentum` | A/B adjacent | EMA10/30, report overlay |
| `VnLargeBreakoutCashFlow` | B — Price/Volume Trend | EMA10/30, volume20, return3 |
| `VnLargePullbackQuality` | A — Active Momentum | EMA7/21, RSI7 |
| `VnLargeValueCashTrend` | D — Cash-Flow Quality | EMA14/42, volume20 optional |

### MACD contract fix

`VnLargeMacdTrend` đã được sửa từ single-object comparison sang đúng contract:

```python
macd, macd_signal, _hist = self.feat.macd(
    close,
    fastperiod=8,
    slowperiod=21,
    signalperiod=5,
)
```

Sau sửa, simulation hoàn tất:

| CAGR | Sharpe | Calmar | MaxDD | PF |
|---:|---:|---:|---:|---:|
| 10.59% | 0.982 | 0.885 | -11.97% | 1.322 |

Timeout trước đó là lỗi sử dụng multi-output contract, không phải metrics
readiness đơn thuần.

## Wave 1 — Active Momentum migration

Đã migrate 5 strategy theo canonical Profile A và chỉ giữ variant cải thiện.

| Strategy | Baseline Sharpe / CAGR | Wave 1 Sharpe / CAGR | Decision |
|---|---|---|---|
| `MacdTrend` | 0.982 / 10.59% | 1.071 / 15.45% | Keep |
| `RsiTrend` | 0.802 / 10.43% | 0.914 / 13.90% | Keep |
| `EpsReportMomentum` | 0.344 / 2.90% | 0.826 / 7.21% | Keep |
| `ProfitReportMomentum` | 0.177 / 1.10% | 1.065 / 16.69% | Keep |
| `PullbackQuality` | 0.850 / 10.89% | 0.778 / 10.22% | Revert to EMA8/24 |

Key findings:

- MACD canonical contract + RSI9/volume10 full-size confirmation cải thiện rõ.
- RSI recovery 7/21 và thresholds 48/42 tốt hơn balanced 12/36 version.
- Report-step phải là strong overlay; persistent positive level + trend mới giữ
  được position giữa các kỳ báo cáo.
- EMA7/21 không tổng quát cho cash-flow pullback; file này giữ EMA8/24.
