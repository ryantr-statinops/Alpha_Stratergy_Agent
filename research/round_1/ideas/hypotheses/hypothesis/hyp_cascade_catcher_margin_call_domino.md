# Hypothesis — Idea 1: Cascade Catcher (Margin Call Domino)

**ID:** HYP-CASCADE-001  
**Thesis:** Margin call cascade exploitation on VN30F1M  
**Target Timeframes:** 5min (primary), 15min (secondary)  
**Data Fields:** `pv_close`, `pv_high`, `pv_low`, `pv_volume`, `fut_matched_volume_vn30f1m_1d`, `fut_open_interest_vn30f1m_1d`, `fut_matched_value_vn30f1m_1d`  
**Status:** PLANNING

---

## 1. Null Hypothesis

Đòn bẩy 1:6-1:8 không tạo ra cascade pattern có thể khai thác. Volume spike + OI drop là random noise, không predictive cho price continuation hay reversal. Chiến lược short theo cascade không outperform random entry.

## 2. Alternative Hypothesis

Khi OI giảm đột ngột (> 1%) kết hợp matched volume spike (> 2x SMA) và price drop (> 0.5%), xác suất giá tiếp tục giảm thêm 1-3 nến là ≥ 65%. Cascade exhaustion (volume collapse + price stabilization) báo hiệu reversal với win rate ≥ 60%.

**Target metrics:**
- Sharpe ≥ 2.0 (Train) / ≥ 1.5 (Test)
- Win Rate ≥ 55%
- Profit Factor ≥ 1.5
- Max Consecutive Losses ≤ 3
- Avg Win / Avg Loss ≥ 1.3

---

## 3. Core Logic

### 3.1 Data Variables
```python
close = self.data.pv_close
high = self.data.pv_high
low = self.data.pv_low
matched_vol = self.data.fut_matched_volume_vn30f1m_1d
oi = self.data.fut_open_interest_vn30f1m_1d
matched_val = self.data.fut_matched_value_vn30f1m_1d
```

### 3.2 Computed Signals
```python
return_1 = self.op.fillna(self.op.pct_change(close, periods=1), value=0)
return_roll = self.feat.rolling_mean(return_1, window=5)
adx = self.feat.adx(high, low, close, timeperiod=10)
vol_sma = self.feat.sma(matched_vol, timeperiod=20)
oi_change = self.op.fillna(self.op.pct_change(oi, periods=1), value=0)
vol_ratio = matched_vol / vol_sma
```

### 3.3 Entry Logic

**Short — Cascade Active:**
```python
oi_drop = oi_change < -0.01               # OI giảm > 1%
vol_spike = vol_ratio > 2.0               # Volume gấp đôi SMA
price_fall = self.op.pct_change(close, periods=1) < -0.005  # Giảm > 0.5%
cascade = oi_drop & vol_spike & price_fall
short_setup = cascade & (return_roll < 0) & (adx > 22)
```

**Long — Cascade Exhaustion:**
```python
vol_collapse = vol_ratio < 0.5            # Volume < 50% SMA
price_stable = self.op.abs(self.op.pct_change(close, periods=1)) < 0.001
exhaustion = oi_drop & vol_collapse & price_stable
long_setup = exhaustion & (return_roll > 0) & (adx > 22)
```

### 3.4 Exit Logic
```python
# Short exit: momentum chết hoặc cascade hết
short_exit_signal = (return_roll > 0) | self.op.crossed_below(adx, 15)

# Long exit: hồi phục xong hoặc cascade lại
long_exit_signal = (return_roll < 0) | self.op.crossed_below(adx, 15)

exit_setup = short_exit_signal | long_exit_signal
```

### 3.5 Position Sizing
```python
# Cascade short: position theo vol_scale
vol_scale = self.op.clip(avg_range / daily_range, 0.3, 1.0)
# Cascade exhaustion: nhẹ hơn (0.5x)
reversal_scale = vol_scale * 0.5
```

---

## 4. Parameter Variants

| Variant | OI Drop | Vol Spike | Price Fall | Return Roll Window | ADX Window | ADX Entry | ADX Exit |
|---------|:-------:|:---------:|:----------:|:------------------:|:----------:|:---------:|:--------:|
| **Aggressive** | > 0.5% | > 1.5x | > 0.3% | 3 | 7 | 20 | 13 |
| **Standard** | > 1.0% | > 2.0x | > 0.5% | 5 | 10 | 22 | 15 |
| **Conservative** | > 2.0% | > 3.0x | > 1.0% | 5 | 10 | 25 | 18 |

---

## 5. Hard Rules Compliance

| Rule | Check | Status |
|------|-------|--------|
| HM-1: Anomaly Filtering | Không trade nếu gap > 10% | ✅ Built-in via ADX filter |
| HM-2: Liquidity Validation | Spread < 0.2% on VN30F1M | ✅ Always true for VN30F1M |
| HM-3: Continuity Check | Skip illiquid periods | ✅ Session gating handles |
| RK-1: Risk per trade ≤ 2% | Vol_scale sizing | ✅ Dynamic sizing |
| RK-2: Max DD 15-20% | Cooldown + ADX exit | ✅ Exit logic |
| RK-3: Consecutive Loss ≤ 5 | Cooldown period | ✅ recent_exit filter |
| RK-4: Max 3 concurrent positions | Single position per strategy | ✅ |

---

## 6. Scorecard Targets

| Metric | Weight | Target (Study) | Acceptable (Competition) |
|--------|:------:|:--------------:|:------------------------:|
| Sharpe Ratio | High | ≥ 2.0 | ≥ 1.2 |
| CAGR | High | ≥ 25% | ≥ 25% |
| Sortino | Medium | ≥ 1.5 | ≥ 1.5 |
| Calmar | Medium | ≥ 0.9 | ≥ 0.9 |
| Max DD | High | ≥ -20% | ≥ -40% |
| Profit Factor | Medium | ≥ 1.5 | ≥ 1.7 |
| VaR 95% | Medium | ≥ -5% | ≥ -5% |
| CVaR 95% | Low | ≥ -6% | ≥ -6% |
| Ulcer Index | Low | ≤ 10 | ≤ 12 |
| Cost | Low | ≤ 1% | ≤ 1% |

**Must-pass:** Sharpe, CAGR, Max DD  
**Pass threshold:** ≥ 8.0/13pts

---

## 7. Backtest Scenarios

| Scenario | Expectation |
|----------|-------------|
| **Normal trending** — ADX > 25 | Cascade signals rõ ràng, PF > 2.0 |
| **Ranging** — ADX < 20 | Không trade (ADX filter blocks) |
| **High volatility** — gap > 2% | Cascade mạnh nhưng risk cao, sizing giảm |
| **Low liquidity** — holiday period | Volume spike false signals, cần vol_ratio > 3x để confirm |

---

## 8. Test Plan

**Data split:** Train 70% → Test 30% (chronological)  
**Train period:** Dữ liệu cũ nhất → thời điểm Test bắt đầu  
**Test period:** 30% dữ liệu gần nhất (giấu kín)

**Validation steps:**
1. Run Standard variant trên 5min + 15min
2. Check win rate, PF, Sharpe
3. If pass threshold → run Aggressive + Conservative variants
4. Multi-scenario backtest (4 scenarios)
5. Scorecard → PASS (≥ 8.0) or REJECT

---

## 9. Edge Cases & Failure Scenarios

| Edge Case | Impact | Mitigation |
|-----------|--------|------------|
| OI data delayed | Tín hiệu OI_drop trễ 1 nến | Dùng `self.op.shift(oi_drop, 1)` để đồng bộ |
| Margin call đã xong trước khi signal | False entry, mua đỉnh | Luôn đợi vol_spike xác nhận, không preempt |
| Afternoon session cascade yếu | Win rate thấp hơn | Session gating: ưu tiên morning (02:00-04:30 UTC) |
| Expiry week OI bất thường | False OI_drop | Adjust threshold 2x trong expiry week |
| Cascade kéo dài > 5 nến | Exit quá sớm | Cho phép hold thêm nếu return_roll vẫn < 0 |

---

## 10. Next Steps

- [ ] User review logic & approve
- [ ] Code strategy template trong generator
- [ ] Gen + validate
- [ ] Upload lên XNOQuant để Simulate
- [ ] Update scorecard với kết quả backtest
