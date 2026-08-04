# Alpha Generation Framework — Systematic Thesis Building

> **Session:** 2026-08-04
> **Mục tiêu:** Phương pháp build alpha theo số lượng lớn (1000+ thesis)
> **Nguyên tắc:** Edge = Thesis quality (70%) + Structural integrity (20%) + Parameter (10%)

---

## Tổng quan

Sau khi phân tích kết quả 49 large-cap TS + 20 mid-cap TS, kết luận:

- **Parameter KHÔNG phải mấu chốt** — cùng thesis tốt, đổi parameter vẫn tốt
- **Thesis quality** quyết định 70% kết quả
- **Structural integrity** (code không bug) quyết định 20%
- **Parameter** chỉ tạo sự khác biệt cuối cùng (10%)

---

## Phương pháp 1: Factor Zoo Systematic (~500 thesis)

Mỗi factor kết hợp với trend filter tạo ra 1 thesis:

| Axis | Factors | Count |
|---|---|---|
| **Price** | RSI, MACD, ADX, CCI, TRIX, Stoch, WillR, Aroon, OBV, ATR | ~10 |
| **Volume** | MFI, OBV, volume spike, volume acceleration, volume-price divergence | ~5 |
| **Fundamental** | ROE, ROA, CFO, earnings yield, cash conversion, payout, leverage, revenue growth, EPS growth, profit margin | ~10 |
| **Balance sheet** | Equity/assets, debt/equity, current ratio, cash ratio | ~4 |
| **Combination** | Each price factor × each fundamental factor | 10 × 10 = 100 |
| **Trend filter** | EMA 8/24, 10/30, 12/36, 14/42, no filter | 5 |
| **Exit type** | Reverse entry, trailing stop, fixed holding period | 3 |
| **Tổng** | | **~500+** |

---

## Phương pháp 2: Academic Literature Mining (~200 thesis)

Nghiên cứu đã chứng minh có edge:

| Paper | Factor | Expected edge |
|---|---|---|
| Fama-French (1993) | Value (B/M) | Long cheap |
| Jegadeesh-Titman (1993) | Momentum 12-1 | Cross-sectional momentum |
| Novy-Marx (2013) | Gross profitability | Revenue - COGS |
| Sloan (1996) | Accruals anomaly | Low accruals = higher quality |
| Piotroski (2000) | F-Score | 8-point fundamental score |
| Asness (2013) | Quality composite | Profitability + growth + safety |
| Barroso (2012) | Volatility-managed | Scale position by inverse vol |
| Moskowitz (2012) | Sector momentum | Industry momentum |
| Haugen-Baker (1996) | Low volatility | Minimize variance |

Mỗi paper → 1 thesis base → kết hợp trend filter → 3–5 variants = **~200 thesis**

---

## Phương pháp 3: Feature Engineering Systematic (~150 thesis)

Tạo feature mới từ feature có sẵn:

| Type | Method | Example |
|---|---|---|
| **Ratio** | A / B | CFO / total assets |
| **Growth** | pct_change(X, N) | Revenue growth 4Q |
| **Momentum** | X > SMA(X, N) | Price above 200-day |
| **Divergence** | Price trend vs indicator trend | Price up + OBV down |
| **Rank** | rank(X) within universe | Top 30% by ROE |
| **Z-score** | (X - mean) / std | RSI z-score |
| **Holding period** | hold_for(X, N) | Hold breakout 10 days |
| **Interaction** | X × Y | RSI × volume |

Mỗi type × 5–10 factors = **~150 thesis**

---

## Phương pháp 4: Regime-Based (~100 thesis)

Chia thị trường thành regimes, mỗi regime có strategy riêng:

| Regime detector | Regimes | Strategy per regime |
|---|---|---|
| ADX > 25 vs < 20 | Trending vs sideways | Trend follow vs mean reversion |
| VIX level | High/low vol | Defensive vs aggressive |
| Breadth | >50% above 200MA vs < | Broad rally vs narrow |
| Interest rate | Rising/falling | Growth vs value |
| Seasonality | Q1/Q2/Q3/Q4 | Sector rotation |

5 regimes × 10 factors × 2 variants = **~100 thesis**

---

## Phương pháp 5: Cross-Sectional Ranking (~50 thesis)

Thay vì time-series, rank stocks theo factor:

```
long = top_rank(factor, 30%)
exit = bottom_rank(factor, 30%)
```

| Ranking factor | Universe | Expected edge |
|---|---|---|
| ROE | Large-cap | Quality tilt |
| Momentum 3M | All | Cross-sectional momentum |
| Earnings surprise | All | PEAD |
| CFO/price | Value | Cash flow yield |
| Volume trend | All | Accumulation |

10 factors × 5 universes = **~50 thesis**

---

## Phương pháp 6: ML Feature Discovery (~200 thesis)

Dùng ML để tìm nonlinear patterns:

```
Features: 100+ technical + fundamental
Target: forward 5/10/20-day return
Model: tree-based (XGBoost, LightGBM)
Output: top feature importances → each = 1 thesis
```

Sau khi có top features:
- Feature 1 → thesis 1
- Feature 1 + Feature 2 interaction → thesis 2
- Feature 1 + fundamental → thesis 3
- etc.

---

## Pipeline: 1000 Thesis →5 PASS

```
Step 1: Factor Zoo (500) + Literature (200) + Engineering (150)
        = 850 raw theses

Step 2: Prune (loại bỏ duplicate, structural invalid)
        → ~400 valid theses

Step 3: Quick screen (backtest nhanh trên train)
        → ~100 theses có Sharpe > 0.5

Step 4: Deep backtest (full metrics)
        → ~20 theses có Sharpe > 1.0

Step 5: Ablation + OOS validation
        → ~5 thes PASS
```

## Yield Rate

| Stage | Input | Yield | Output |
|---|---|---|---|
| Raw generation | — | — | 1000 theses |
| Structural prune | 1000 | 40% | 400 |
| Quick screen | 400 | 25% | 100 |
| Deep backtest | 100 | 20% | 20 |
| OOS validation | 20 | 25% | 5 PASS |

**Tỷ lệ PASS trên raw: ~0.5%** — phù hợp industry benchmark (quant hedge funds typically test 10,000+ signals to find 10–20 live strategies).

---

## Evidence từ kết quả thực tế

### Strategies hoạt động tốt (Agg Sharpe ≥ 1.0)

| Strategy | Agg Sharpe | Thesis | Tại sao edge |
|---|---|---|---|
| VnLargeCapexDisciplineTrend | 1.13 | CFO funds CAPEX | Capital discipline = công ty tự chủ tài chính |
| VnLargeCapex1442 | 1.12 | CFO funds CAPEX (14/42 EMA) | Same thesis, different window |
| VnLargeCapexProfitGuard | 1.11 | CFO funds CAPEX + profit | Profit confirmation |
| VnLargeRoaTrend | 1.10 | ROA + trend | Profitability quality |
| VnLargeMacdTrend | 1.07 | MACD signal | Momentum confirmation |
| VnLargeProfitReportMomentum | 1.07 | Profit growth report | PEAD |
| VnLargeRsiRecoveryTrend (mid) | 1.35 | RSI7 recovery | Mean reversion in trend |
| VnLargeBreakoutVolume (mid) | 1.29 | Breakout + volume | Volume confirmation |

### Strategies THẤT BẠI (Root cause analysis)

| Strategy | Sharpe | Root cause |
|---|---|---|
| BollingerSqueezeBreakout | 0.03 | Volatility squeeze không có edge trên large-cap |
| PullbackMeanReversion | 0.56 | Over-constraint (RSI + drawdown + EMA + rising) |
| CashInterestCoverage | 0 | 0 giao dịch (feature sparse) |
| DeleveragingTrend | 0 | 0 giao dịch (feature sparse) |
| PayoutAffordability | 0 | 0 giao dịch (feature sparse) |
| T01 DonchianBreakout (mid, before fix) | 0 | rolling_max gồm bar hiện tại (structural bug) |

### Insight quan trọng

1. **"CFO funds CAPEX"** là thesis tốt nhất cho large-cap — 4/4 strategy Sharpe ≥ 0.88
2. **Cash flow quality** hoạt động tốt hơn **earnings quality** trên large-cap
3. **Structural bugs** (rolling_max, consecutive_true) là nguyên nhân phổ biến nhất gây 0 giao dịch
4. **Feature sparse** (CFO annual, EPS quarterly) là nguyên nhân thứ hai gây 0 giao dịch

---

*Framework preregistered. Next: triển khai Factor Zoo Systematic.*
