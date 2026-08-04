# Alpha Ideas — 20 Time-Series VN-MID-CAP (Round 2)

> **Session:** 2026-08-04
> **Trạng thái:** ✅ Đã submit 20/20 — kết quả ghi ở mục Kết quả
> **Universe:** VN-MID-CAP (daily equity, long-only)
> **Mode:** `time_series` (không `_panel`, `self.set_positions`, bounds `[0,+1]`)
> **Nguồn:** `data/VN-MID-CAP.md` (trend 20–45 phiên, breakout+volume, volume spike,
> pullback 10–15%, sector rotation, PEAD) + `data/vietnam_market_characteristics_v1.md`
> (LEGACY vòng 1: herding, margin-call cascade, no circuit breaker) + OSINT:
> - Vo & Truong (2018): momentum tồn tại trên HOSE.
> - Entropy+volume momentum VNINDEX 2015–2025 đạt Sharpe 3.96 (downside control, không phải
>   return tăng).
> - JumpStart 14-yr: volume ĐƠN LẺ không có edge — chỉ dùng làm confirmation.
> - Ho, Nguyen & Tran (2024): PEAD có ý nghĩa tại VN, mạnh hơn khi insider cao / institution thấp.
> - HOSE overreaction: loser thắng winner 1.80% / 2.17% ở T+2 / T+3 (nền tảng pullback/contrarian).

## Không trùng với strategy VN-MID-CAP đã submit

Đã có 13 strategy MID-CAP (1 TS + 12 CS). Batch này **chỉ time_series**, 20 idea mới,
không lặp `VnMidTrendQuality` (ROE + trend) và không trùng 12 CS.

## Ràng buộc kỹ thuật (nắm từ lần LARGE-CAP)

1. Chỉ `self.data.<field>` không suffix, `self.feat.*` + `self.op.*` time-series, `self.set_positions`.
2. Long-only `[0, 0.5, 1]`; **exit đặt trước entry** (priority).
3. Fundamental missing = unavailable: `notna`, không `fillna(0)` fundamental.
4. Fundamental ratio/pct_change bắt buộc `notna` + positive denominator (validator strict).
5. Price return được `fillna(..., 0)`.
6. Không import, loop, global aggregation, negative shift, backfill, centered window.
7. Không dùng `pv_vn30_close` làm regime gate (LARGE đã degenerate) — chỉ dùng trong T20
   beta-feature probe.
8. Entry ≤ 4 điều kiện, exit ≤ 3 nhánh.

## Evidence status của features/ops dùng (bắt buộc khai báo)

| Feature/Op | Evidence trong TS | Ghi chú |
|---|---|---|
| `ema`, `sma`, `macd`, `rsi` | SIMULATE (đã dùng) | core an toàn |
| `notna`, `pct_change` | SIMULATE | core an toàn |
| `rolling_max`, `rolling_min` | CATALOG_ONLY | lần đầu dùng trong TS |
| `adx`, `plus_di`, `minus_di`, `atr`, `bbands`, `obv`, `mfi`, `aroon`, `linearreg_slope`, `beta`, `rolling_quantile` | CATALOG_ONLY | lần đầu dùng trong TS |
| `rising`, `falling`, `hold_for`, `consecutive_true`, `crossed_above`, `crossed_below` | CATALOG_ONLY | lần đầu dùng trong TS |

Mọi CATALOG_ONLY khi live verify/simulate lỗi → ghi nhận `SIMULATED_FAIL` trung thực,
không đổi feature để cứu kết quả.

## Parameter families (preregistered — selection rule cố định)

Mỗi family khai báo baseline + variant (đổi 1 dimension/lần). Selection:
**baseline trước; chỉ submit variant nếu baseline lỗi field hoặc không tạo giao dịch;
không retune sau khi đọc Test.** Test (2023–2024) là OOS khóa.

| Family | Baseline | Variants (chỉ khi baseline lỗi/tạo 0 giao dịch) |
|---|---|---|
| T02 EMA | 10/30 | 12/36, 8/24 |
| T04 ADX | 22/18 | 25/20, 20/15 |
| T06 vol | 2.0× | 1.5×, 2.5× |
| T07 spike | 3.0×/6.8% | 2.5×/6.8% |
| T11 RSI | 9/0.85–0.90 | 7/0.85–0.90 |
| T12 RSI | 7/48/42 | 9/48/42 |
| T09 squeeze | 0.15 quantile/250 | 0.10/250 |
| T14–T17 | growth>0 | growth>0.05 (loose) |

Không tối ưu đồng thời period+threshold+sizing+exit.

## 20 ideas

### A. Trend following (cốt lõi mid-cap, trend 20–45 phiên)

| ID | File | Thesis | Entry / Exit |
|---|---|---|---|
| T01 | `VnMidDonchianBreakout` | Donchian 20: phá đỉnh 20 phiên trong uptrend | Entry `close>rollmax(high,20)` & `close>EMA30`; Exit `close<rollmin(low,20)` |
| T02 | `VnMidEmaTrendRide` | EMA golden cross bám trend | Entry `close>EMA10>EMA30` & ret1>0; Exit `close<EMA30` |
| T03 | `VnMidMacdTrend` | MACD 8/21/5 + trend | Entry `macd>signal` & `close>EMA30`; Exit `macd<signal` ∨ `close<EMA30` |
| T04 | `VnMidAdxStrongTrend` | ADX chỉ giao dịch khi có directional strength | Entry `ADX>22` & `+DI>-DI` & `close>EMA30`; Exit `ADX<18` |
| T05 | `VnMidAroonBreakout` | Aroon-up xác nhận breakout | Entry `aroon_up>70` & `close>EMA30`; Exit `close<EMA30` ∨ `aroon_up<50` |

### B. Volume-confirmed breakout / accumulation (volume = confirmation)

| ID | File | Thesis | Entry / Exit |
|---|---|---|---|
| T06 | `VnMidBreakoutVolume` | Breakout 20d-high + vol>2×SMA(vol,20) | Entry `close>rollmax(high,20)` & `close>EMA30`; strong thêm vol>2×; Exit `close<EMA30` |
| T07 | `VnMidSmartMoneySpike` | Vol spike 3× + ret≥6.8% = smart money đẩy giá | Entry spike & `close>EMA30`; Exit `close<EMA30` |
| T08 | `VnMidVolumeAcceleration` | Vol-ratio tăng + MFI>60 | Entry vol_ratio>1.2 & `MFI>60` & `close>EMA30`; strong thêm `rising(vol_ratio,3)`; Exit `close<EMA30` ∨ `MFI<50` |
| T09 | `VnMidVolatilitySqueeze` | Squeeze width phân vị thấp rồi breakout | Entry `width<quantile(250,0.15)` giữ 3 bar & `close>bb_upper` & vol; Exit `close<bb_middle` ∨ `close<EMA30` |
| T10 | `VnMidObvTrendConfirm` | OBV > EMA(OBV) xác nhận trend | Entry `OBV>ema(OBV,20)` & `close>EMA30`; strong thêm OBV tăng; Exit `OBV<ema(OBV,20)` ∨ `close<EMA30` |

### C. Pullback / hồi trong uptrend (pullback 10–15%; HOSE overreaction)

| ID | File | Thesis | Entry / Exit |
|---|---|---|---|
| T11 | `VnMidUptrendPullback` | Mua hồi 10–15% từ peak trong uptrend | Entry `close>EMA30` & drawdown 0.85–0.90 & RSI9<45; strong thêm `rising(close,3)`; Exit `close<EMA30` |
| T12 | `VnMidRsiRecoveryTrend` | RSI recovery trong trend (Profile A) | Entry `RSI7>48` & `close>EMA24` & EMA8>EMA24; strong RSI>55; Exit `RSI7<42` ∨ `close<EMA24` |
| T13 | `VnMidTrendSlopeAccel` | LinReg slope dương và tăng tốc | Entry `slope14>0` & `close>EMA30`; strong `rising(slope,3)`; Exit `slope<0` ∨ `close<EMA30` |

### D. Fundamentals + trend (PEAD: Ho, Nguyen & Tran 2024; earnings seasonality)

| ID | File | Thesis | Entry / Exit |
|---|---|---|---|
| T14 | `VnMidEpsSurpriseDrift` | EPS surprise dương giữ drift 20–60 phiên | Entry EPS>0 & `eps_growth>0.05` & `close>EMA30`; strong `>0.15`; Exit trend break ∨ `eps_growth<-0.02` |
| T15 | `VnMidProfitEventTrend` | Profit event + trend | Entry profit>0 & `profit_growth>0` & `close>EMA36`; strong `>0.10`; Exit `close<EMA36` ∨ `profit_growth<-0.05` |
| T16 | `VnMidCfoSurpriseTrend` | CFO surprise + cash quality | Entry cfo>0 & `cfo_growth>0` & `cfo/np>0.5` & `close>EMA30`; strong `>0.10`; Exit trend break ∨ `cfo_growth<-0.05` |
| T17 | `VnMidRoaQualityTrend` | ROA quality + trend (khác ROE của TrendQuality) | Entry `roa>0.01` & profit>0 & `close>EMA36`; strong EMA12>EMA36; Exit `close<EMA36` ∨ `roa<0` |

### E. Anti-chase / liquidity guard (đu đỉnh cuối sóng, mã thanh khoản ảo)

| ID | File | Thesis | Entry / Exit |
|---|---|---|---|
| T18 | `VnMidAntiChaseGuard` | Giảm size khi quá mua / tăng >4 phiên liên tiếp | weak 0.5 khi `RSI9>75` ∨ `consecutive_true(ret1>0,4)>=4`; strong 1.0 ngược lại; Exit `close<EMA30` |
| T19 | `VnMidLiquidityTrend` | Chỉ long cổ phiếu có thanh khoản trên floor | Entry traded_value>0 & `close*vol>sma(close*vol,20)*0.5` & `close>EMA30`; strong thêm `>sma`; Exit `close<EMA30` |
| T20 | `VnMidBetaFollower` | Beta-VN30 tăng = follower tham gia sóng (**probe `pv_vn30_close`**) | Entry `beta(close,pv_vn30_close,60)>0.5` & `close>EMA30`; strong `rising(beta,3)`; Exit `close<EMA30` ∨ `beta<0.3` |

## Tiêu chí đánh giá (VN-MID-CAP)

| Mức | Điều kiện |
|---|---|
| PASS | Aggregate + Train + Test đều Sharpe≥1.1, CAGR≥20%, MaxDD≥-40%, PF≥1.25, Calmar≥1.0 |
| Candidate | Sharpe ≥ 1.0 & CAGR ≥ 15% |
| Research | Sharpe ≥ 0.6 & MaxDD hợp lý |
| Reject | Sharpe < 0 hoặc 0 giao dịch hoặc field lỗi |

Ngoài aggregate, bắt buộc so với baseline `VnMidTrendQuality`: variant nào không tạo
giao dịch hoặc field lỗi → `REJECTED`; giữ nguyên bản ghi (không đổi tên để reset trial).

## Quy trình implement

1. ✅ Preregister plan này (trước khi test).
2. ✅ Gen 20 file vào `output/stage_2/vn_mid_cap/time_series/`.
3. ✅ Thêm 20 dòng vào `output/index.csv`.
4. ✅ `python tools/validate_framework.py --strict` → 0 issues (119 files).
5. ✅ Dry-run submit batch VN-MID-CAP (`--dry-run`) → 33/33 OK.
6. ✅ Live submit 20/20 (1 file VERIFY_FAIL, 19 SIMULATED), ghi kết quả ở dưới.

## Kết quả (2026-08-04)

Lưu trong `backtest/results_stage_2.csv` (strategy_id ghi trong bảng). Không strategy
nào đạt PASS (Test Sharpe cao nhất = 1.00, ngưỡng PASS 1.1). 3 Candidate, 7 Research,
10 Reject.

| ID | File | Verdict | Agg CAGR | Agg Sharpe | Agg MaxDD | Test CAGR | Test Sharpe | Trades | Ghi chú |
|---|---|---|---|---|---|---|---|---|---|
| T01 | VnMidDonchianBreakout | 🔴 REJECTED | 0.017 | 0.30 | -0.053 | 0.004 | 0.11 | 0 | 0 giao dịch: `close>rollmax(high,20)` bất khả thi vì window gồm bar hiện tại |
| T02 | VnMidEmaTrendRide | 🟡 Research | 0.130 | 1.13 | -0.091 | 0.032 | 0.32 | 21017 | CAGR<15% nên không phải Candidate |
| T03 | VnMidMacdTrend | 🟡 Research | 0.116 | 1.16 | -0.083 | 0.021 | 0.27 | 8157 | CAGR<15% |
| T04 | VnMidAdxStrongTrend | 🟢 Candidate | 0.166 | 1.25 | -0.123 | 0.086 | 0.74 | 3854 | Sharpe≥1.0 & CAGR≥15% |
| T05 | VnMidAroonBreakout | 🟡 Research | 0.097 | 0.92 | -0.098 | 0.024 | 0.28 | 8670 | aroon chạy được, Sharpe dưới 1.0 |
| T06 | VnMidBreakoutVolume | 🔴 REJECTED | 0.017 | 0.30 | -0.053 | 0.004 | 0.11 | 0 | 0 giao dịch, cùng nguyên nhân T01 |
| T07 | VnMidSmartMoneySpike | 🔴 Reject (yếu) | 0.029 | 0.52 | -0.051 | 0.011 | 0.35 | 470 | Sharpe<0.6 dù PF 1.38 |
| T08 | VnMidVolumeAcceleration | 🟡 Research | 0.134 | 1.08 | -0.186 | 0.075 | 0.76 | 10786 | MFI+rising OK, MaxDD -18.6% |
| T09 | VnMidVolatilitySqueeze | 🔴 REJECTED | 0.010 | 0.17 | -0.058 | -0.006 | -0.17 | 1364 | Test OOS âm |
| T10 | VnMidObvTrendConfirm | 🟡 Research | 0.136 | 1.09 | -0.166 | 0.063 | 0.55 | 14530 | OBV chạy tốt, CAGR<15% |
| T11 | VnMidUptrendPullback | 🔴 Reject (yếu) | 0.049 | 0.60 | -0.149 | 0.004 | 0.13 | 177 | chỉ 4 closed trades (177 tổng) |
| T12 | VnMidRsiRecoveryTrend | 🟢 Candidate | 0.170 | 1.35 | -0.108 | 0.097 | 0.83 | 10195 | tốt nhất batch (Sharpe 1.35, PF 1.37) |
| T13 | VnMidTrendSlopeAccel | 🟡 Research | 0.123 | 1.14 | -0.134 | 0.067 | 0.78 | 8641 | linearreg_slope+rising OK |
| T14 | VnMidEpsSurpriseDrift | 🔴 Reject (yếu) | 0.034 | 0.54 | -0.053 | 0.005 | 0.16 | 460 | PEAD drift yếu ở TS mid-cap |
| T15 | VnMidProfitEventTrend | 🟡 Research | 0.054 | 0.64 | -0.119 | 0.011 | 0.30 | 720 | Sharpe≥0.6 |
| T16 | VnMidCfoSurpriseTrend | 🔴 REJECTED | 0.018 | 0.31 | -0.053 | 0.004 | 0.11 | 104 | annual CFO thưa với mid-cap |
| T17 | VnMidRoaQualityTrend | 🟡 Research | 0.133 | 1.17 | -0.113 | 0.075 | **1.00** | 3433 | Test Sharpe cao nhất batch |
| T18 | VnMidAntiChaseGuard | 🔴 REJECTED | — | — | — | — | — | — | VERIFY_FAIL: `self.op` không có `consecutive_true` |
| T19 | VnMidLiquidityTrend | 🟢 Candidate | 0.179 | 1.28 | -0.174 | 0.111 | 0.84 | 20529 | Sharpe 1.28, Test CAGR 11.1% |
| T20 | VnMidBetaFollower | 🔴 REJECTED | 0.017 | 0.30 | -0.053 | 0.004 | 0.11 | 0 | 0 giao dịch: beta không bao giờ >0.5 (NaN/không trigger) |

### Phát hiện kỹ thuật (cập nhật evidence)

1. `rolling_max`/`rolling_min` (CATALOG_ONLY): SIMULATE chạy được nhưng **window gồm bar
   hiện tại** → `close > rollmax(high, N)` không bao giờ trigger (close ≤ high). Mọi entry
   kiểu "phá đỉnh" cần shift 1 (bị cấm). T01/T06 0 giao dịch.
2. `consecutive_true` (CATALOG_ONLY): **VERIFY_FAIL** — runtime `self.op` không có method này.
   Ghi nhận `SIMULATED_FAIL` trung thực (T18), không đổi feature.
3. `beta` (CATALOG_ONLY): SIMULATE OK nhưng 0 trigger → không khả thi làm entry với MID-CAP
   ở tham số hiện tại.
4. Chạy thành công và tạo giao dịch (SIMULATE_PASSED mới): `aroon` (T05), `mfi` + `rising`
   (T08), `bbands` + `rolling_quantile` + `hold_for` (T09, nhưng OOS âm), `obv` (T10),
   `linearreg_slope` (T13), `adx/plus_di/minus_di` (T04).
5. Không strategy nào PASS (Test Sharpe cao nhất 1.00). Đu trend core (EMA/MACD/ADX/RSI/
   slope/OBV) đều tạo nhiều giao dịch nhưng OOS (2023-2024) yếu — phù hợp môi trường
   MID-CAP nhiễu, đuổi theo trend.
6. Baseline `VnMidTrendQuality` không có record trong `results_stage_2.csv` (chưa từng submit
   qua pipeline này) → không so sánh số được; đánh giá theo tiêu chí preregistered.
