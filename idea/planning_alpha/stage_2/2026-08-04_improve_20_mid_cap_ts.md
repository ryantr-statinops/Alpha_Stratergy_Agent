# Improvement Plan — 20 Time-Series VN-MID-CAP

> **Session:** 2026-08-04
> **Trạng thái:** 📝 Chờ user duyệt plan
> **Nguồn gốc:** Batch 2026-08-04 (20/20 đã submit, 0 PASS)
> **Mục tiêu:** Fix lỗi kỹ thuật + chuẩn hóa timeperiod + nâng 3 Candidate lên PASS

---

## 1. Tổng kết batch trước

| Category | Count | Chi tiết |
|---|---|---|
| 🔴 REJECTED (0 giao dịch / VERIFY_FAIL) | 5 | T01 (rolling_max), T06 (rolling_max), T18 (consecutive_true), T20 (beta 0.5 never), T09 (Test OOS âm) |
| 🔴 REJECTED (thấp) | 5 | T07 (Sharpe 0.52), T11 (0.004 Test CAGR), T14 (Sharpe 0.54), T16 (annual CFO thưa) |
| 🟡 Research (Sharpe≥0.6) | 7 | T02, T03, T05, T08, T10, T13, T15 |
| 🟢 Candidate (Sharpe≥1.0 & CAGR≥15%) | 3 | T12 (Sharpe 1.35), T19 (Sharpe 1.28), T04 (Sharpe 1.25) |

### Phát hiện kỹ thuật từ batch trước

1. `rolling_max`/`rolling_min` gồm bar hiện tại → `close > rollmax(high,20)` **không bao giờ trigger** (T01/T06).
2. `self.op.consecutive_true` **không tồn tại** → VERIFY_FAIL (T18).
3. `self.feat.beta(close, vn30, 60) > 0.5` never trigger → 0 giao dịch (T20).
4. Baseline `VnMidTrendQuality` không có record trong results_stage_2.csv.

---

## 2. Fixes kỹ thuật (block 1 — ưu tiên cao nhất)

### T01 `VnMidDonchianBreakout` + T06 `VnMidBreakoutVolume`

**Vấn đề:** `rolling_max(high, window=20)` gồm bar hiện tại → close ≤ high luôn đúng → entry không bao giờ trigger.

**Fix:** Thêm `shift=1` cho `rolling_max`/`rolling_min`:

```python
# T01: shift=1 để chỉ dùng high/low của 19 bar trước
upper_channel = self.feat.rolling_max(high, window=20, shift=1)
lower_channel = self.feat.rolling_min(low, window=20, shift=1)

# T06: tương tự
upper_high = self.feat.rolling_max(high, window=20, shift=1)
```

**EMA:** Giữ EMA30 (Profile B — Price/Volume Trend: EMA 10/30). Đổi thành EMA slow 30, thêm fast 10 cho trend filter (tùy chọn).

### T18 `VnMidAntiChaseGuard`

**Vấn đề:** `self.op.consecutive_true(ret1 > 0, periods=4)` không tồn tại ở runtime.

**Fix:** Thay bằng 4 lần `pct_change` riêng lẻ:

```python
ret1 = self.op.fillna(self.op.pct_change(close, periods=1), 0)
ret2 = self.op.fillna(self.op.pct_change(close, periods=2), 0)
ret3 = self.op.fillna(self.op.pct_change(close, periods=3), 0)
ret4 = self.op.fillna(self.op.pct_change(close, periods=4), 0)

# drift liên tục 4 phiên = close[t] > close[t-4] (tích cực trên cả 4 bar)
up_streak_4 = (ret1 > 0) & (ret2 > 0) & (ret3 > 0) & (ret4 > 0)
```

**RSI:** Giữ RSI9 > 75 overbought guard (Profile A: period 9, overbought <75).

### T20 `VnMidBetaFollower`

**Vấn đề:** `beta(close, vn30, 60) > 0.5` never trigger — beta window quá dài, mid-cap beta thường thấp hơn 0.5 trên window dài.

**Fix options (chọn 1):**

- **Option A (recommended):** Giảm window xuống 21 (1 tháng) và giảm ngưỡng xuống `>0.3`. Mid-cap thường có beta 0.3–0.6 với VN30 trên window ngắn.
- **Option B:** Bỏ beta làm entry chính, chuyển sang dual-price confirmation: `close > EMA_fast(close,10)` & `close_vn30 > EMA_slow(vn30,30)` (rider trên VN30 uptrend).

**Chọn Option A** (giữ nguyên thesis beta nhưng giảm window/ngưỡng):

```python
beta_val = self.feat.beta(close, vn30_close, timeperiod=21)  # 1 tháng
base_long = known & (beta_val > 0.3) & (close > ema_slow)
exit_setup = known & ((close < ema_slow) | (beta_val < 0.1))
```

---

## 3. Chuẩn hóa timeperiod (block 2)

### Nguyên tắc

Mọi timeperiod **phải có ý nghĩa trên daily** (5/21/63/252 phiên). Không dùng tham số "vô nghĩa" cho daily (ví dụ: 60/90/250 cho beta hoặc rolling window mà không có lý do kinh tế rõ ràng).

### Bảng chuẩn hóa

| Strategy | Timeperiod hiện tại | Timeperiod chuẩn (theo profile) | Lý do |
|---|---|---|---|
| T01 Donchian | 20 (rolling) | 20 (giữ) | Trend 20–45 phiên theo VN-MID-CAP.md |
| T02 EMA | 10/30 | 10/30 (giữ) | Profile B: Price-volume trend |
| T03 MACD | 8/21/5 | 8/21/5 (giữ) | Canonical MACD |
| T04 ADX | 22/18 | 22/18 (giữ) | Canonical ADX, strong trend filter |
| T05 Aroon | (không rõ) | 25 (giữ) | Breakout 20–25 phiên |
| T06 Vol SMA | 20 | 20 (giữ) | Canonical volume SMA |
| T07 Spike | 3.0×/6.8% | 3.0×/6.8% (giữ) | VN-MID-CAP.md observation |
| T08 MFI | (không rõ) | 14 (giữ) | Canonical MFI |
| T09 BB squeeze | 250 quantile | 63 quantile (1 quý) | 250 quá dài cho squeeze detection |
| T10 OBV EMA | 20 | 20 (giữ) | Canonical volume trend |
| T11 RSI | 9 | 9 (giữ) | Profile A: period 9 |
| T12 RSI | 7 | 7 (giữ) | Profile A: recovery RSI 7 |
| T13 LinReg | 14 | 14 (giữ) | Canonical slope |
| T14–T17 | EMA 30/36 | EMA 30/36 (giữ) | Profile C/D: fundamental trend |
| T18 RSI | 9 | 9 (giữ) | Profile A |
| T19 SMA vol | 20 | 20 (giữ) | Canonical volume |
| T20 Beta | 60 | 21 (đổi) | 60 vô nghĩa cho beta daily; 1 tháng = 21 phiên |

### Thay đổi duy nhất: T09 BB squeeze quantile window

```python
# T09: giảm từ 250 (1 năm) xuống 63 (1 quý)
bb_width = (bb_upper - bb_lower) / bb_middle
squeeze = self.op.rolling_quantile(bb_width, window=63, quantile=0.15)
```

---

## 4. Nâng Candidate lên PASS (block 3)

### Target

| Strategy | Agg Sharpe hiện tại | Agg CAGR hiện tại | Target | Ghi chú |
|---|---|---|---|---|
| T12 RsiRecoveryTrend | 1.35 | 17.0% | PASS (≥1.0/≥18%) | CAGR thấp → cần tăng exposure hoặc减少 churn |
| T19 LiquidityTrend | 1.28 | 17.9% | PASS | CAGR thấp → tương tự |
| T04 AdxStrongTrend | 1.25 | 16.6% | PASS | CAGR thấp → tương tự |

### Phương pháp improvement (research rules — 1 dimension/lần)

**T12 `VnMidRsiRecoveryTrend`:**

- **Baseline:** EMA 8/24, RSI7 >48/<42, strong RSI>55, exit RSI<42 | close<EMA24
- **Variant 1:** Tăng strong RSI threshold từ 55 lên 58 (nâng xác nhận → giảm churn)
- **Variant 2:** Thêm `rising(close, 3)` làm confirmation cho weak state (giảm số lệnh yếu)
- **Variant 3:** Đổi exit RSI từ 42 xuống 40 (giữ lệnh lâu hơn trong uptrend)

**T19 `VnMidLiquidityTrend`:**

- **Baseline:** traded_value>0 & `close*vol > sma(close*vol,20)*0.5` & close>EMA30
- **Variant 1:** Tăng liquidity floor từ `0.5×` lên `0.8×` (chỉ giữ cổ thanh khoản cao → giảm slippage)
- **Variant 2:** Thêm confirmation `rising(close*vol, 5)` cho strong state (volume momentum)
- **Variant 3:** Đổi EMA slow từ 30 xuống 24 (nhanh hơn → bắt trend sớm hơn)

**T04 `VnMidAdxStrongTrend`:**

- **Baseline:** ADX>22 & +DI>-DI & close>EMA30; exit ADX<18
- **Variant 1:** Nới lỏng entry ADX từ 22 xuống 20 (nhiều lệnh hơn trong weak trend)
- **Variant 2:** Thêm `rising(ADX, 3)` cho strong state (ADX đang tăng = trend đang mạnh)
- **Variant 3:** Đổi EMA slow từ 30 xuống 36 (Profile C: fundamental trend, chậm hơn)

### Research rules (preregistered)

1. Chỉ ablate **1 dimension/lần** trên Train.
2. Test (2023–2024) là **OOS locked** — chỉ đo cuối, không retune.
3. Nếu variant không cải thiện Sharpe/Calmar trên Train → loại, giữ baseline.
4. Không thêm >1 condition mới cho entry/exit mỗi iteration.
5. Không đảo signal để cứu backtest.

---

## 5. Quy trình thực hiện (block 4)

### Step 1: Fix 4 lỗi kỹ thuật (block 1)

- [ ] Sửa T01 `VnMidDonchianBreakout`: thêm `shift=1` cho rolling_max/rolling_min
- [ ] Sửa T06 `VnMidBreakoutVolume`: thêm `shift=1` cho rolling_max
- [ ] Sửa T18 `VnMidAntiChaseGuard`: thay `consecutive_true` bằng 4 lần pct_change
- [ ] Sửa T20 `VnMidBetaFollower`: giảm beta window từ 60 xuống 21, ngưỡng 0.5→0.3

### Step 2: Chuẩn hóa timeperiod (block 2)

- [ ] Sửa T09 `VnMidVolatilitySqueeze`: giảm quantile window từ 250 xuống 63
- [ ] Kiểm tra tất cả strategy đã dùng `timeperiod=` rõ ràng (không default)

### Step 3: Ablation trên Train (block 3)

- [ ] T12: chạy 3 variants trên Train, chọn variant tốt nhất
- [ ] T19: chạy 3 variants trên Train, chọn variant tốt nhất
- [ ] T04: chạy 3 variants trên Train, chọn variant tốt nhất

### Step 4: Validate + Submit

- [ ] `python tools/validate_framework.py --strict` → 0 issues
- [ ] Dry-run submit batch VN-MID-CAP
- [ ] Live submit → đo Test metrics

### Step 5: Ghi kết quả

- [ ] Cập nhật planning doc với kết quả improvement
- [ ] So sánh trước/sau trên cùng baseline `VnMidTrendQuality`

---

## 6. Risk & fallback

| Risk | Fallback |
|---|---|
| T01/T06 vẫn 0 giao dịch sau shift=1 | Kiểm tra `shift` parameter có khả dụng; nếu không → chuyển sang logic khác (close > prev_high where prev_high = high shifted by 1 bar manually) |
| T20 beta vẫn never trigger | Drop T20, thay bằng strategy mới (dual-price confirmation) |
| Ablation không cải thiện Train Sharpe | Giữ baseline, ghi nhận "research" thay vì force improvement |
| Validation fail | Fix error, không submit nếu có issue |

---

## 7. Timeline ước tính

| Phase | Thời gian |
|---|---|
| Fix 4 lỗi kỹ thuật | 15 phút |
| Chuẩn hóa timeperiod | 5 phút |
| Ablation (3×3 variants) | 30 phút |
| Validate + Submit | 10 phút |
| **Tổng** | **~60 phút** |

---

*Plan preregistered trước khi test. Test (2023–2024) là OOS locked.*
