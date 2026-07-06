# Context Session — Alpha Bot (Backtest Engine Phase)

**Session Date:** 2026-07-03
**Purpose:** Build offline backtest engine cho VN30F futures (vnstock data) và chuẩn bị chạy 1311 strategy variants
**Next Agent:** Đọc file này trước, sau đó kiểm tra backtest/ và output/ để tiếp tục

---

## 1. Hiện trạng dự án

| Hạng mục | Trạng thái |
|----------|:----------:|
| `output/` — 1311 strategies | ✅ Generated, commit rồi |
| `tools/generate_strategies.py` | ✅ TEMPLATES config + TEMPLATE_META docstring headers |
| `tools/validate_framework.py` | ✅ Recursive scan — 1311/1311 pass |
| `backtest/` — engine | ✅ Hoàn chỉnh |
| `context_session/` | ✅ Updated |

---

## 2. Backtest Engine — Kiến trúc

```
backtest/
├── data/
│   └── fetch_data.py           # Pipeline: daily (60-day chunks) + 5m (5-day chunks, contract codes)
├── features/
│   ├── operators.py             # crossed_above, crossed_below, between, fillna, clip, hline, previous, pct_change
│   ├── ma.py                    # sma, ema, kama, mama, rolling_mean, rolling_zscore, rolling_quantile, rolling_std, rolling_mad, rolling_max/min, rolling_correlation, beta, linearreg_slope/angle, tsf, vwap
│   ├── momentum.py              # rsi, roc, mom, cmo, macd, adx, aroon, apo, ppo, returns
│   ├── volatility.py            # atr, natr, bbands, price_z, volume_z
│   ├── volume.py                # obv, mfi, ad, adosc, bop, cmf
│   ├── cycle.py                 # ht_trendline, sine, dcperiod, dcphase, trendmode, phasor
│   └── candles.py               # hammer, engulfing, morning/evening star, doji, marubozu
├── runners/
│   ├── base.py                  # compute_positions (fixed -1/0/1), compute_positions_tiered (fixed -1/-0.5/0/0.5/1)
│   ├── thesis_01.py             # T01-A → T01-G (7 templates)
│   ├── thesis_02.py             # T02-A → T02-F (6 templates)
│   ├── thesis_03.py             # T03-A → T03-E (5 templates)
│   ├── thesis_04.py             # T04-A → T04-G (7 templates)
│   ├── thesis_05.py             # T05-A → T05-G (7 templates)
│   └── thesis_06.py             # T06-A → T06-E (5 templates)
├── evaluate.py                  # Sharpe, CAGR, Max DD, Calmar, PF, Sortino, Win Rate, Ulcer, VaR, CVaR
├── run.py                       # Orchestrator — đọc TEMPLATES từ generate_strategies.py, map→functions, inject TF defaults
├── _quick_test.py               # Smoke test trên daily data
└── data/cache/
    └── vn30f_daily.parquet      # 865 rows (2021-10-06 → 2025-04-15)
```

---

## 3. Output (1311 strategies)

| Thesis | Variants | Templates |
|:------:|:--------:|:---------:|
| 01 Rolling Mean + Quantile | 652 | T01-A → T01-G (7) |
| 02 Volatility Regime | 272 | T02-A → T02-F (6) |
| 03 Time-Series Decomposition | 66 | T03-A → T03-E (5) |
| 04 Microstructure Flow | 105 | T04-A → T04-G (7) |
| 05 Cross-Market Correlation | 90 | T05-A → T05-G (7) |
| 06 Multi-Factor Composite | 126 | T06-A → T06-E (5) |
| **Total** | **1311** | **37 templates / 239 param variants** |

---

## 4. Quy tắc code quan trọng

1. **Position phải là fixed number (scalar)** — không được dùng array/series. Chỉ dùng `compute_positions` (giá trị -1/0/1) hoặc `compute_positions_tiered` (giá trị -1/-0.5/0/0.5/1). Đã sửa T03-B: bỏ `compute_positions_tiered_scale`.
2. **Backtest/run.py đọc TEMPLATES từ tools/generate_strategies.py** — không hardcode template configs. Map template name → backtest function qua FUNC_MAP.
3. **Tất cả template functions có `**kwargs`** — để nhận extra params từ generator configs (price_source_def, conv, v.v.) mà không bị TypeError.
4. **TF defaults được inject tự động** — adx_entry, adx_exit, rsi_window, vol_window, roc_window, ema_window, return_window, max_cycle_period khác nhau theo từng khung.

---

## 5. Ràng buộc dữ liệu

| Item | Chi tiết |
|------|----------|
| Nguồn | vnstock free tier (guest) — 20 requests/phút |
| 5m data | Chỉ lấy được qua contract code VN30FYYMM (YY=year, MM=expiry month 03/06/09/12) |
| Daily data | VN30F1M — chunk 60 ngày, đã cache 865 rows |
| 5m fetch | 18 contracts × ~20 chunks (5-day) × 3.5s delay ≈ 20 phút |
| Active window | 3 tháng trước expiry → ~21st tháng đáo hạn |
| Khung giờ GD | Sáng 09:00–11:30, Chiều 13:00–15:00 (giờ VN) |

---

## 6. Multi-Timeframe Window Sizing

| TF | Fast | Mid | Slow | RSI | ADX | Vol | ReturnRoll | ADX Entry | ADX Exit | ADX Entry Weak |
|:--:|:----:|:---:|:----:|:---:|:---:|:---:|:----------:|:---------:|:--------:|:--------------:|
| 5m | 8 | 14 | 20 | 7 | 7 | 14 | 3 | 22 | 15 | 18 |
| 15m | 13 | 26 | 34 | 10 | 10 | 20 | 5 | 22 | 15 | 18 |
| 30m | 20 | 40 | 50 | 14 | 14 | 26 | 8 | 18 | 12 | 15 |
| 60m | 30 | 60 | 100 | 21 | 21 | 34 | 14 | 16 | 10 | 13 |

---

## 7. Quick Test Results (Daily Data)

| Strategy | Sharpe | CAGR | MaxDD | Calmar |
|----------|:------:|:----:|:-----:|:------:|
| T01-B MA Crossover | 0.43 | 2.44% | -7.20% | 0.34 |
| T01-D Quantile Breakout | -0.14 | -3.04% | -16.97% | -0.18 |
| T01-F Z-Score Rev | 0.46 | 3.66% | -11.93% | 0.31 |
| T02-A Vol Breakout | -0.19 | -1.23% | -10.43% | -0.12 |
| T02-E NATR Regime | -0.18 | -1.87% | -10.43% | -0.18 |
| T03-C LinReg Slope | 0.33 | 3.73% | -32.52% | 0.11 |

---

## 8. Việc cần làm tiếp theo

1. **Fetch 5m data** — chạy `backtest/data/fetch_data.py` với mode 5m (tốn ~20 phút, rate limit 20 req/min)
2. **Chạy full backtest** — `python backtest/run.py` sẽ backtest 1311 variants × 4 timeframes
3. **Export & phân tích** — results.csv → top candidates per thesis group
4. **Upload top strategies lên XNOQuant** — chạy platform-native simulation
5. **Commit & push** code mới

---

## 9. File quan trọng

| File | Vai trò |
|------|---------|
| `tools/generate_strategies.py` | TEMPLATES config + generator, là single source of truth |
| `backtest/run.py` | Đọc TEMPLATES bên trên, chạy backtest, export CSV |
| `backtest/runners/base.py` | `compute_positions`, `compute_positions_tiered` |
| `backtest/data/fetch_data.py` | Fetch 5m + daily, parquet cache, resample |
| `backtest/evaluate.py` | Tính Sharpe, CAGR, Max DD, v.v. |
| `output/` | 1311 strategy files generated từ TEMPLATES |

---

*End of Context Session — Backtest engine đã sẵn sàng, cần fetch 5m data và chạy backtest.*
