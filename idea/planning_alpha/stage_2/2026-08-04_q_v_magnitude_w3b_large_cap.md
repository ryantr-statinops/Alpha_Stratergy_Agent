# Alpha Ideas — Wave 3b: magnitude weighting (demean_l1) VN-LARGE-CAP

> **Session:** 2026-08-04
> **Mode:** cross_sectional, market-neutral
> **Universe:** VN-LARGE-CAP
> **Nhiệm vụ:** đổi portfolio constructor từ `rank_demean_l1` sang **`demean_l1`**
> để magnitude của factor có hiệu lực — đòn bẩy duy nhất làm winsorize/zscore
> (đã chứng minh no-op với rank_demean_l1) có tác dụng.

## Lý do

Wave 3 (rank_demean_l1 + winsorize/rank) → 6/6 metric trùng base. Gốc rễ:
`rank_demean_l1` tự rank lại signal nên mọi biến đổi đơn điệu trước đó vô nghĩa.
`demean_l1` giữ magnitude của signal (sau demean, chuẩn hóa L1) → winsorize + zscore
trước đó mới thay đổi weights. Bằng chứng: 31 file dùng `demean_l1` đã SIMULATE_PASSED
(kể cả winner `VnSmallCsValueTrendP02`).

## Pattern (theo §5 cross_sectional/strategy_patterns.md)

```python
factor = <ratio kinh tế>
eligible = <guard>
clean = self.op.winsorize_cs_panel(factor, mask=eligible, lower=0.02, upper=0.98)
score = self.op.zscore_cs_panel(clean, mask=eligible)
weights = self.op.portfolio_weights_panel(score, method='demean_l1', mask=eligible)
```

Anti-pattern §10: cấm `demean_l1` trần trên raw factor (extreme-symbol dominance) →
bắt buộc winsorize + zscore trước.

## 4 phiên bản (giữ nguyên factor Q04/V06/Q03/Composite, chỉ đổi constructor)

| # | File | Factor | Guard |
|---:|---|---|---|
| 1 | `VnLargeCsPreWcMagnitude` | Q04 pre-WC cash strength | PreWCCash>0, PAT>0, Assets>0 |
| 2 | `VnLargeCsEarningsMagnitude` | V06 EPS/close | EPS>0, close>0 |
| 3 | `VnLargeCsCashEarningsMagnitude` | Q03 CFO/Assets − PAT/Assets | CFO>0, PAT>0, Assets>0 |
| 4 | `VnLargeCsCompositeMagnitude` | z(Q04) + z(V06) composite | PreWCCash>0, PAT>0, Assets>0, EPS>0, close>0 |

## Đánh giá (VN-LARGE-CAP)

PASS: Sharpe≥1.2, CAGR≥15%, MaxDD≥-35%, PF≥1.2, Calmar≥1.1.
So sánh trực tiếp với baseline rank_demean_l1 (Q04 0.911 / V06 0.815 / Q03 0.346 /
Composite 0.910). Nếu demean_l1 cùng factor vượt baseline → magnitude có giá trị
kinh tế; nếu không → xác nhận rank-neutral là đúng.

## Quy trình

1. ✅ Viết plan.
2. ✅ Gen 4 file `output/stage_2/vn_large_cap/cross_sectional/`.
3. ✅ Đăng ký `output/index.csv`.
4. ✅ `validate_framework.py --strict` → 0 issues.
5. ✅ Live submit 4 file (`--files`) 4/4 OK.
6. ✅ So demean_l1 vs rank_demean_l1 trong doc.

## Kết quả (2026-08-04) — demean_l1: MIXED, không vượt trội

| File | demean_l1 Agg | rank_demean_l1 base | Δ | Verdict |
|---|---:|---:|---:|---|
| PreWcMagnitude | 0.630 | 0.911 (PreWc) | **-0.28** | Tệ hơn hẳn |
| EarningsMagnitude | 0.843 | 0.815 (Earnings) | +0.03 | Cải thiện nhẹ |
| CashEarningsMagnitude | 0.629 | 0.346 (Spread) | +0.28 | Cải thiện từ base yếu |
| CompositeMagnitude | 0.875 | 0.910 (Composite) | -0.04 | Tương đương |

Splits:
- CompositeMagnitude: Train 1.030 / Test 0.664 (ổn định hơn base rank 1.027/0.747? Test thấp hơn)
- EarningsMagnitude: Train 0.951 / Test 0.656 (Test 0.66 < base 0.79 → kém hơn OOS)
- PreWcMagnitude: Train 0.603 / Test (chưa cắt, ~0.6) — phá hỏng Q04 (rank 0.987/0.817)

### Phân tích

1. **demean_l1 phá hỏng Q04** (0.911 → 0.630): magnitude của pre-WC cash strength
   không có giá trị kinh tế ở LARGE — thứ hạng mới là thứ bền. Xác nhận
   `rank_demean_l1` đúng cho Q04.
2. **Earnings/CashEarnings cải thiện Agg nhẹ nhưng Test kém hơn**: magnitude của
   value spread giúp Train nhưng không bền OOS → risk của magnitude weighting.
3. **Kết luận chung:** đổi constructor không phải con đường tới Sharpe 1.2. Ở LARGE,
   rank-neutral là lựa chọn đúng; magnitude weighting chỉ thắng trên vài leg và
   không đáng tin OOS.

### Trạng thái Q/V sau 3 wave

- **Q04 `PreWcCashStrength` (rank_demean_l1) vẫn là candidate tốt nhất**: Agg 0.911,
  Train 0.987 → Test 0.817, ổn định nhất. V06 (0.815) là value control ổn định.
- Mọi variation (composite, winsorize/rank filter, demean_l1) đều **không vượt Q04**.
- Degenerate đã loại: Q01≡Q02, AgreementFullExit, noise-filter no-op, magnitude mixed.
- Để qua 1.2: cần alpha orthogonal (family M/F — VN30-residual price/flow), không
  phải tuning constructor của cùng factor.