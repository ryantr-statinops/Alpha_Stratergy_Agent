# Kế hoạch Backtest — 805 Strategies cho XNOQuant

> **Constraint:** Upload manual — paste code từng file lên web XNOQuant  
> **Time per strategy:** ~5-10 phút (paste + set params + run + ghi kết quả)  
> **Target:** 10-15 strategies/tuần (≈ 2-3 giờ/tuần)

---

## 🔄 Workflow cho mỗi strategy

```
1. Mở file .py trong output/
2. Copy toàn bộ code
3. Paste lên XNOQuant → New Strategy
4. Set timeframe = tên folder (5min/15min/30min/60min)
5. Set data range = 6 tháng (mặc định)
6. Run backtest
7. Ghi kết quả vào tracking sheet (dưới đây)
8. Move sang strategy tiếp theo
```

**Ghi lại các metrics này (tối thiểu):**

```
Sharpe:     [ ]    (mục tiêu ≥ 1.2)
Win Rate:   [ ]    (mục tiêu ≥ 50%)
Profit Fac: [ ]    (mục tiêu ≥ 1.5)
Max DD:     [ ]    (mục tiêu ≥ -30%)
Số tín hiệu: [ ]   (tín hiệu/tháng)
return_roll: [ ]   (có hoạt động không? ghi chú)
```

---

## 📋 Phases

### Phase 1: Quick Screening (8 sessions ≈ 4 tuần)

Mỗi thesis test **2 đại diện × 2 timeframe (nhanh nhất + chậm nhất)** = 4 uploads/thesis.  
Nếu thesis nào Sharpe < 0.5 trên cả 4 → skip thesis đó (tập trung tài nguyên).

#### Session 1: Thesis 01 — Momentum
| # | File | TF | Ghi chú |
|:-:|:-----|:--:|:--------|
| 1 | `output/thesis_01_momentum/5min/01-0001_MomFast_5min.py` | 5min | Pure ROC(8) — baseline nhanh nhất |
| 2 | `output/thesis_01_momentum/5min/01-0009_MomVolVolFast_5min.py` | 5min | ROC + volume — có return_roll |
| 3 | `output/thesis_01_momentum/60min/01-0100_MomFast_60min.py` | 60min | Pure ROC slow TF |
| 4 | `output/thesis_01_momentum/60min/01-0108_MomVolVolFast_60min.py` | 60min | ROC + volume slow TF |

→ Nếu Sharpe ≥ 1.0 ở bất kỳ TF nào → test thêm cascade + cmo variants.

#### Session 2: Thesis 02 — Trend
| # | File | TF | Ghi chú |
|:-:|:-----|:--:|:--------|
| 1 | `output/thesis_02_trend/5min/02-0143_TrendMACDStd_5min.py` | 5min | MACD + ADX(20) — tiered sizing |
| 2 | `output/thesis_02_trend/5min/02-0133_TrendMACMA8x20_5min.py` | 5min | MA cross — baseline |
| 3 | `output/thesis_02_trend/60min/02-0251_TrendMACDStd_60min.py` | 60min | MACD + ADX slow |
| 4 | `output/thesis_02_trend/60min/02-0241_TrendMACMA30x100_60min.py` | 60min | MA cross slow |

#### Session 3: Thesis 03 — Mean Reversion
| # | File | TF | Ghi chú |
|:-:|:-----|:--:|:--------|
| 1 | `output/thesis_03_mean_reversion/5min/03-0277_MRQStd_5min.py` | 5min | Quantile rev — có return_roll |
| 2 | `output/thesis_03_mean_reversion/5min/03-0285_MRRSIStd_5min.py` | 5min | RSI extreme |
| 3 | `output/thesis_03_mean_reversion/60min/03-0379_MRQStd_60min.py` | 60min | Quantile slow |
| 4 | `output/thesis_03_mean_reversion/60min/03-0387_MRRSIStd_60min.py` | 60min | RSI slow |

#### Session 4: Thesis 04 — Breakout
| # | File | TF | Ghi chú |
|:-:|:-----|:--:|:--------|
| 1 | `output/thesis_04_breakout/5min/04-0413_BOQStd_5min.py` | 5min | Quantile BO |
| 2 | `output/thesis_04_breakout/5min/04-0421_BODonFast_5min.py` | 5min | Donchian |
| 3 | `output/thesis_04_breakout/60min/04-0494_BOQStd_60min.py` | 60min | Quantile slow |
| 4 | `output/thesis_04_breakout/60min/04-0502_BODonFast_60min.py` | 60min | Donchian slow |

#### Session 5: Thesis 05 — Cross Market
| # | File | TF | Ghi chú |
|:-:|:-----|:--:|:--------|
| 1 | `output/thesis_05_cross_market/15min/05-0521_XMRelFast_15min.py` | 15min | Relative strength |
| 2 | `output/thesis_05_cross_market/15min/05-0528_XMDJIFast_15min.py` | 15min | DJI spillover |
| 3 | `output/thesis_05_cross_market/60min/05-0575_XMRelFast_60min.py` | 60min | Relative slow |
| 4 | `output/thesis_05_cross_market/60min/05-0582_XMDJIFast_60min.py` | 60min | DJI slow |

#### Session 6: Thesis 06 — Volume Flow
| # | File | TF | Ghi chú |
|:-:|:-----|:--:|:--------|
| 1 | `output/thesis_06_volume_flow/15min/06-0602_VFOISlow_15min.py` | 15min | OI trend |
| 2 | `output/thesis_06_volume_flow/15min/06-0608_VFVolStd_15min.py` | 15min | Matched vol surge |
| 3 | `output/thesis_06_volume_flow/60min/06-0666_VFOISlow_60min.py` | 60min | OI slow |
| 4 | `output/thesis_06_volume_flow/60min/06-0672_VFVolStd_60min.py` | 60min | Vol surge slow |

#### Session 7: Thesis 07 — Intraday Session
| # | File | TF | Ghi chú |
|:-:|:-----|:--:|:--------|
| 1 | `output/thesis_07_intraday_session/5min/07-0698_ISMOpnStd_5min.py` | 5min | Open drive — có session ranges |
| 2 | `output/thesis_07_intraday_session/5min/07-0704_ISMLunStd_5min.py` | 5min | Lunch revert |
| 3 | `output/thesis_07_intraday_session/5min/07-0710_ISMClsStd_5min.py` | 5min | Close squeeze |
| 4 | `output/thesis_07_intraday_session/5min/07-0716_ISMGapStd_5min.py` | 5min | Gap fill |

#### Session 8: Thesis 08 — Multi-Factor
| # | File | TF | Ghi chú |
|:-:|:-----|:--:|:--------|
| 1 | `output/thesis_08_multifactor/15min/08-0746_MFZStd_15min.py` | 15min | Z-score composite — tiered |
| 2 | `output/thesis_08_multifactor/15min/08-0754_MFMomStd_15min.py` | 15min | Momentum multi-factor |
| 3 | `output/thesis_08_multifactor/60min/08-0786_MFZStd_60min.py` | 60min | Z-score slow |
| 4 | `output/thesis_08_multifactor/60min/08-0794_MFMomStd_60min.py` | 60min | Momentum multi slow |

---

### Phase 2: Hypothesis A/B (theo yêu cầu — chỉ khi cần)

Sau Phase 1, với thesis có Sharpe ≥ 1.0, chạy hypothesis tests:

| Hypothesis | Upload thêm | Để đo |
|:-----------|:------------|:------|
| HYP-MOM-01 | So MomFast vs MomFast2 (return_roll vs smoothed) | return_roll impact |
| HYP-MOM-04 | So MomVol(1.0) vs (tiered 0.5/1.0) | Tiered sizing impact |
| HYP-TRN-01 | So TrendMACD-Std(20) vs Strict(25) vs Mild(15) | ADX threshold |
| HYP-MLT-01 | So MFZ-Std(1.5) vs Tight(2.0) vs Mild(1.0) | Z threshold |
| HYP-TRN-04 | So exit ADX<14 vs ADX<14\|return_roll<thresh | Exit optimization |

Mỗi A/B test = 2-3 uploads, mất 15-20 phút.

---

### Phase 3: Deep Dive (top strategies)

Với strategies pass Phase 1 (Sharpe ≥ 1.0):
- Test thêm trên TF khác (thêm 3 uploads)
- Test regime: ranging market riêng
- Ghi scorecard đầy đủ (13 metrics)
- Quyết định: VALIDATED / REJECTED

---

## 📊 Tracking Sheet

Copy bảng này vào file `backtest_results.csv` (hoặc excel) và cập nhật sau mỗi lần test:

```csv
Date,Session,File,TF,Sharpe,WinRate,PF,MaxDD,Signals,Notes
2026-07-02,S1,01-0001_MomFast_5min,5min,0.85,51%,1.32,-22%,47,return_roll OK
2026-07-02,S1,01-0009_MomVolVolFast_5min,5min,1.05,54%,1.45,-18%,38,vol filter helps
```

Template ghi chú nhanh sau mỗi test:

```
PASS: Sharpe > 1.0, Win Rate > 50%, PF > 1.3
WARN: Sharpe 0.5-1.0, cần điều chỉnh
FAIL: Sharpe < 0.5, skip template này
```

---

## 🚩 Decision Rules

| Điều kiện | Hành động |
|:----------|:----------|
| Sharpe ≥ 1.5 | 🎯 VALIDATED — ghi scorecard, deep dive sau |
| 1.0 ≤ Sharpe < 1.5 | ✅ POTENTIAL — test thêm variants |
| 0.5 ≤ Sharpe < 1.0 | ⚠️ BORDERLINE — test 1 variant khác để confirm |
| Sharpe < 0.5 | ❌ SKIP — template này không khả thi, move on |
| Win Rate < 40% (dù Sharpe cao) | ⚠️ Cảnh báo — có thể do vài trade lớn, check PF |

---

## 📝 Hypothesis Doc Update Format

Sau mỗi backtest, mở file `idea/hypothesis/hyp_thesis_NN_group.md` và update:

```markdown
## HYP-XXX-YY: [Tên hypothesis]

...

**Metric Actual:**
- Sharpe: 1.15 (target ≥ 1.0) ✓
- Win Rate: 54% (target ≥ 52%) ✓
- Profit Factor: 1.42 (target ≥ 1.5) ✗

**Status:** VALIDATED (pass 2/3 core metrics)
**Notes:** return_roll filter giúp giảm noise, nhưng PF chưa đạt target do exit chưa optimal
```

---

## ⏱ Timeline Ước Lượng

| Phase | Số session | Số strategies | Thời gian | Tuần |
|:------|:----------:|:-------------:|:---------:|:----:|
| Phase 1a: Momentum + Trend | 2 | 8 | ~60 phút | Tuần 1 |
| Phase 1b: MeanRev + Breakout | 2 | 8 | ~60 phút | Tuần 1 |
| Phase 1c: Cross + Volume | 2 | 8 | ~60 phút | Tuần 2 |
| Phase 1d: Intraday + Multi | 2 | 8 | ~60 phút | Tuần 2 |
| Phase 2: Hypothesis A/B | 3-5 | 6-15 | ~45-120 phút | Tuần 3 |
| Phase 3: Deep Dive | 2-3 | 3-5 | ~30-60 phút | Tuần 4 |
| **TOTAL** | **13-16** | **~41-52** | **~5-7 giờ** | **4 tuần** |

---

## 📁 File Structure cho Results

```
backtest/
├── backtest_results.csv          # Master tracking — cập nhật sau mỗi session
├── hypothesis_updates.md         # Log các thay đổi vào hypothesis docs
└── scorecards/
    ├── thesis_01_momentum.md     # Scorecard đầy đủ cho từng thesis
    ├── thesis_02_trend.md
    └── ...
```

> **Mẹo:** Giữ terminal/file `backtest_results.csv` mở sẵn. Test xong strategy nào ghi ngay, tránh quên.
