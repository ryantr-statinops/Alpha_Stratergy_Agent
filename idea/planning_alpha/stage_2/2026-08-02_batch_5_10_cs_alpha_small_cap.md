# Alpha Ideas — Batch 5 (10 cross-sectional alphas cho VN-SMALL-CAP)

> **Date:** 2026-08-02
> **Mode:** cross_sectional, market-neutral (`rank_demean_l1`)
> **Universe:** VN-SMALL-CAP
> **Objective:** earnings re-rating + retail herding + liquidity control.

## Design rules

- Quarterly EPS/profit growth là core; static ROA/ROE không dùng làm primary alpha.
- Report events được làm mượt bằng rolling features để tránh one-day sparse signal.
- Price momentum/volume xác nhận re-rating.
- Liquidity rank loại bottom 30% khi strategy cần execution filter.
- Common mask dùng `_panel` fields; không dùng time-series `op.notna` trên panel.
- Portfolio market-neutral, net exposure gần 0, gross exposure 1.

## Strategies

| # | File | Thesis |
|---:|---|---|
| 1 | `VnSmallCsEpsReRating.py` | Rolling EPS surprise + price momentum |
| 2 | `VnSmallCsProfitReRating.py` | Profit acceleration/assets + momentum |
| 3 | `VnSmallCsEpsGrowthLiquidity.py` | Smoothed EPS growth, top-70% liquidity |
| 4 | `VnSmallCsEarningsVolumeConfirmation.py` | EPS surprise + abnormal volume |
| 5 | `VnSmallCsBreakoutHerding.py` | Donchian proximity + momentum + volume |
| 6 | `VnSmallCsTrendParticipation.py` | EMA/SMA trend among liquid names |
| 7 | `VnSmallCsRsiContinuation.py` | Relative RSI + smoothed return |
| 8 | `VnSmallCsCloseStrength.py` | Close-location persistence + volume + momentum |
| 9 | `VnSmallCsValueReRating.py` | Earnings yield + momentum, liquidity filtered |
| 10 | `VnSmallCsCashBackedGrowth.py` | EPS growth + momentum with positive annual CFO |

## Evaluation thresholds

VN-SMALL-CAP PASS requires Sharpe >= 1.0, CAGR >= 25%, MaxDD >= -45%,
Profit Factor >= 1.3 and Calmar >= 0.8.

The existing `VnSmallCsEpsRank.py` remains unchanged as the baseline.

## Live results

All 10 strategies verified and simulated successfully. No strategy passed all
VN-SMALL-CAP thresholds.

| Strategy | CAGR | Sharpe | Calmar | MaxDD | PF |
|---|---:|---:|---:|---:|---:|
| `ValueReRating` | 9.02% | 0.973 | 0.893 | -10.10% | 1.214 |
| `EpsGrowthLiquidity` | 3.05% | 0.789 | 0.727 | -4.20% | 1.256 |
| `EpsReRating` | 7.25% | 0.514 | 0.392 | -18.48% | 1.199 |
| `TrendParticipation` | 2.42% | 0.299 | 0.130 | -18.62% | 1.062 |
| `BreakoutHerding` | 0.92% | 0.087 | 0.028 | -32.35% | 1.027 |
| `RsiContinuation` | 0.39% | 0.038 | 0.014 | -27.35% | 1.016 |
| `EarningsVolumeConfirmation` | -0.74% | -0.058 | -0.025 | -29.11% | 0.999 |
| `CloseStrength` | -2.34% | -0.230 | -0.061 | -38.56% | 0.955 |
| `ProfitReRating` | -6.42% | -0.717 | -0.181 | -35.38% | 0.876 |
| `CashBackedGrowth` | -15.43% | -1.840 | -0.273 | -56.45% | 0.719 |

## Yearly findings

- `ValueReRating` đạt Sharpe 3.264 trong 2021 và 1.269 trong 2022, nhưng âm
  trong 2023 và chỉ 0.706 trong 2024.
- `EpsGrowthLiquidity` dương và Sharpe >1.3 trong 2021–2023, với drawdown tổng
  rất thấp, nhưng CAGR nhỏ và Sharpe âm trong 2024.
- `EpsReRating` mạnh trong 2020/2022 nhưng thất bại rõ trong 2023.

Cross-sectional SMALL-CAP không gặp cùng 2022 failure như LARGE time-series;
vấn đề chính là stability sau 2022 và return magnitude không đủ cho CAGR 25%.

Research priority:

1. Giữ `ValueReRating` làm high-return baseline.
2. Giữ `EpsGrowthLiquidity` làm low-risk/stability baseline.
3. Nghiên cứu blend hai signal hoặc regime-aware weighting, không tiếp tục thêm
   volume/technical components độc lập vì các variants đó không cải thiện.

## Revision 2 — investment-style long-only

Định hướng chiến lược chuyển sang "mua stock" (long-only) thay cho đánh phái
sinh. **Phát hiện platform:** mode `cross_sectional` dùng `set_portfolio_positions`
ép market-neutral — thử long-only qua `normalize_l1_cs_panel`, `rank * buy`,
`portfolio_weights_panel(method='rank')` và body flag `long_only` đều fail runtime
(`status=error`); PUT payload chỉ nhận `{"code": code}`; không có endpoint tách
long/short leg. Long-only không khả thi trên platform.

Quyết định: giữ construction market-neutral (long side là hàng đầu, short side là
hedge giấy platform yêu cầu) nhưng tái thiết kế **signal** theo triết lý
fundamental value/quality/growth cho người đầu tư stock.

- Xóa 7 alpha technical/herding yếu: `ProfitReRating`, `EarningsVolumeConfirmation`,
  `BreakoutHerding`, `TrendParticipation`, `RsiContinuation`, `CloseStrength`,
  `CashBackedGrowth`.
- Giữ 3 alpha tốt dạng fundamental: `ValueReRating`, `EpsGrowthLiquidity`, `EpsReRating`.
- Thêm 7 alpha fundamental mới (đều market-neutral, mask liquidity top-70%,
  dùng fields `eps`, `net_profit`, `total_assets`, `owners_equity` + PV):

| Sequence | File | Signal |
|---:|---|---|
| 4 | `VnSmallCsRoaQuality` | ROA + earnings yield |
| 5 | `VnSmallCsRoeQuality` | ROE + earnings yield |
| 6 | `VnSmallCsProfitGrowth` | asset-scaled profit growth + profitability |
| 7 | `VnSmallCsCapitalStrength` | equity/assets (low leverage) + ROA |
| 8 | `VnSmallCsQualityMomentum` | ROA + price momentum |
| 9 | `VnSmallCsEarningsYieldTrend` | earnings yield + price trend (SMA) |
| 10 | `VnSmallCsEpsAcceleration` | EPS acceleration + ROA |

Tổng 10 alpha tối ưu. `VnSmallCsEpsRank.py` giữ nguyên làm baseline.

## Live results (fundamental set, long-only thesis)

10/10 submit thành công. Pivot fundamental cải thiện vượt bậc so với batch
technical/herding.

| Strategy | CAGR | Sharpe | Calmar | MaxDD | PF |
|---|---:|---:|---:|---:|---:|
| `RoeQuality` | 14.01% | **1.975** | 0.764 | -18.34% | **1.400** |
| `RoaQuality` | 12.73% | **1.871** | 0.668 | -19.05% | **1.366** |
| `ProfitGrowth` | 8.24% | **1.324** | 0.631 | -13.06% | 1.237 |
| `EpsAcceleration` | 7.60% | **1.144** | 0.385 | -19.71% | 1.203 |
| `ValueReRating` | 9.02% | 0.973 | 0.893 | -10.10% | 1.214 |
| `CapitalStrength` | 4.31% | 0.983 | 0.530 | -8.14% | 1.168 |
| `EarningsYieldTrend` | 6.93% | 0.874 | 0.575 | -12.06% | 1.182 |
| `QualityMomentum` | 7.21% | 0.825 | 0.598 | -12.06% | 1.173 |
| `EpsGrowthLiquidity` | 3.05% | 0.789 | 0.727 | -4.20% | 1.256 |
| `EpsReRating` | 7.25% | 0.514 | 0.392 | -18.48% | 1.199 |

Top 2 (Roe/RoaQuality) có Sharpe >1.87 và PF >1.37, vượt ngưỡng Sharpe 1.0 + PF
1.3; Calmar chưa đạt 0.8. CAGR cao nhất ~14% < ngưỡng 25%.

### Yearly stability (top 3)

| Year | RoeQuality | RoaQuality | ProfitGrowth |
|---|---:|---:|---:|
| 2020 | +16.1% / 2.61 | +12.0% / 2.03 | -4.1% / -0.78 |
| 2021 | +7.2% / 0.67 | +5.6% / 0.55 | +4.5% / 0.59 |
| 2022 | +34.0% / 2.89 | +30.0% / 2.80 | +26.3% / 2.79 |
| 2023 | +7.3% / 0.84 | +7.2% / 0.87 | +3.8% / 0.49 |
| 2024 | +29.2% / 3.55 | +28.3% / 3.70 | +19.5% / 3.59 |

Kết luận:

- Fundamental value/quality là hướng đúng cho "mua stock" VN small-cap; alpha
  dương gần như mọi năm kể cả 2022 (thời điểm batch cũ thất bại).
- Technical/herding thua đồng loạt nên đã xóa khỏi set.
- User xác nhận phải giữ nguyên toàn bộ ngưỡng gốc; không được hạ CAGR để tạo
  PASS. `RoeQuality` với CAGR 14.01% vẫn **chưa PASS** vì thiếu CAGR 25% và
  Calmar 0.8. Wave tiếp theo phải tối ưu đến đủ 5/5 theo tiêu chí gốc.

## Wave 2 - tested value-trend exponent family

Original VN-SMALL-CAP thresholds are retained: Sharpe >= 1.0, CAGR >= 25%,
MaxDD >= -45%, Profit Factor >= 1.3, and Calmar >= 0.8. The old ten-strategy
fundamental set had no pass. The tested value-trend exponent family p2-p11
passed all original thresholds for every exponent.

| Exponent | CAGR | Sharpe | Calmar | MaxDD | PF |
|---:|---:|---:|---:|---:|---:|
| p2 | 0.2512 | 1.8638 | 1.4453 | -0.1738 | 1.5015 |
| p3 | 0.2550 | 1.8200 | 1.4807 | -0.1722 | 1.4927 |
| p4 | 0.2594 | 1.7699 | 1.5229 | -0.1704 | 1.4813 |
| p5 | 0.2656 | 1.7206 | 1.5758 | -0.1685 | 1.4698 |
| p6 | 0.2738 | 1.6761 | 1.6613 | -0.1648 | 1.4596 |
| p7 | 0.2844 | 1.6364 | 1.7972 | -0.1582 | 1.4521 |
| p8 | 0.2972 | 1.6007 | 2.0071 | -0.1480 | 1.4471 |
| p9 | 0.3128 | 1.5716 | 2.2556 | -0.1387 | 1.4448 |
| p10 | 0.3309 | 1.5474 | 2.6291 | -0.1258 | 1.4449 |
| p11 | 0.3515 | 1.5282 | 2.8458 | -0.1235 | 1.4466 |

These results represent one highly correlated parameter family, not ten
independent alpha sources. Out-of-sample validation and robustness risk remain;
the in-sample pass rate must not be interpreted as independent confirmation.

Independent follow-up research is documented in
`2026-08-02_20_independent_small_cap_alpha_ideas.md`; it replaces parameter
variants with 20 distinct economic mechanisms from the canonical data catalog.
