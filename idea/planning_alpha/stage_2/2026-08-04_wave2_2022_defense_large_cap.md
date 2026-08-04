# Alpha Ideas — Wave 2 (Round 2, VN-LARGE-CAP: 2022 Defense)

> **Session:** 2026-08-04
> **Trạng thái:** 🚀 Đang gen
> **Mục đích:** Wave 2 theo khuyến nghị `2026-08-02_sharpe_diagnostic_audit.md`
> (mục "Wave 2 recommendation"): biến thể "defense 2022" từ **hai thiết kế tốt nhất**
> trong batch gần nhất — `VnLargeQualityTrendAgreement` (ổn định train/test nhất:
> 1.0586 / 1.0180) và `VnLargeCapexDisciplineTrend` (Sharpe aggregate cao nhất
> 1.1272 nhưng train 1.3555 → test 0.6624, overfit).
> **Universe:** VN-LARGE-CAP (daily)

---

## Vì sao "defense 2022"

Train period = 2020–2022 (test OOS = 2023–2024). 2022 là năm thị trường Việt Nam
giảm sâu (VN-Index ~-32%); phần lớn max drawdown của các alpha LARGE hiện tại rơi
vào 2022. Các alpha hiện hữu toàn FAIL vì thiếu Sharpe (~1.0–1.1 vs ngưỡng 1.2),
không phải thiếu CAGR/PF. Wave 2 phải:

1. Giảm whipsaw 2022 bằng EMA chậm hơn theo archetype: `14/42`, `18/54`, `30/90`.
2. Explicit exit rõ ràng (không chỉ dựa `close < ema_slow` mặc định).
3. Không volume tier (audit: chỉ giữ nếu risk-adjusted tăng; không chứng minh được
   trong batch trước).
4. Không dùng `pv_vn30_close` regime gate (live test đã tạo degenerate result).
5. Mỗi variant là **một dimension change** duy nhất so với baseline (research rule 3).

## Nguồn baseline

| Baseline | Fields | Sizing | Exit |
|---|---|---|---|
| `VnLargeQualityTrendAgreement` | CFO annual > 0, NP quarterly > 0, EMA8/24 + EMA12/36 stack | 0/0.5/1 | fast break |
| `VnLargeCapexDisciplineTrend` | CFO annual > 0, capex < CFO, EMA12/36 | 0/0.5/1 | CFO<0 ∨ capex>CFO ∨ close<slow |

Cả hai đều chứng minh được tạo giao dịch (QTA 573/562, CDT 942/955) — fields dùng
lại đã SIMULATE_PASSED.

## 10 Alpha (2 family × 5 biến thể, mỗi biến thể đổi 1 dimension)

### Family A — Quality Trend Agreement (QTA)

| # | File | Dimension thay đổi | Entry | Exit |
|---:|---|---|---|---|
| 1 | `VnLargeAgreement1442` | period | CFO>0 & NP>0 & EMA14/42 + EMA18/54 stack | fast break |
| 2 | `VnLargeAgreement1854` | period | CFO>0 & NP>0 & EMA18/54 + EMA30/90 stack | fast break |
| 3 | `VnLargeAgreementFullExit` | exit | CFO>0 & NP>0 & EMA8/24 + EMA12/36 stack | fast break ∨ close<EMA36 |
| 4 | `VnLargeAgreementConversion` | threshold | CFO>0 & NP>0 & CFO/NP>0.5 & EMA8/24 + EMA12/36 stack | fast break |
| 5 | `VnLargeAgreementHysteresis` | sizing/noise | CFO>0 & NP>0 & EMA8/24 + EMA12/36 stack, strong = close > EMA36*1.02 | fast break ∨ close<EMA36 |

### Family B — Capex Discipline (CDT)

| # | File | Dimension thay đổi | Entry | Exit |
|---:|---|---|---|---|
| 6 | `VnLargeCapex1442` | period | CFO>0 & capex<CFO & EMA14/42 | CFO<0 ∨ capex>CFO ∨ close<EMA42 |
| 7 | `VnLargeCapex1854` | period | CFO>0 & capex<CFO & EMA18/54 | CFO<0 ∨ capex>CFO ∨ close<EMA54 |
| 8 | `VnLargeCapex3090` | period | CFO>0 & capex<CFO & EMA30/90 | CFO<0 ∨ capex>CFO ∨ close<EMA90 |
| 9 | `VnLargeCapexDeadband` | sizing/noise | CFO>0 & capex<CFO & EMA12/36, strong = close > EMA36*1.02 | CFO<0 ∨ capex>CFO ∨ close<EMA36 |
| 10 | `VnLargeCapexProfitGuard` | threshold | CFO>0 & capex<CFO & NP>0 & EMA12/36 | CFO<0 ∨ capex>CFO ∨ NP<0 ∨ close<EMA36 |

## Contract code (giống batch trước, giữ nguyên pattern SIMULATE_PASSED)

```python
class CustomStrategy(SimpleAlgorithm):
    def __algorithm__(self):
        close = self.data.pv_close
        operating_cash_flow = self.data.fun_cf_net_cash_inflows_outflows_from_operating_activities_annual
        net_profit = self.data.fun_is_net_profit_loss_after_tax_quarterly   # QTA family
        capex = self.data.fun_cf_purchases_of_fixed_assets_and_other_long_term_assets_annual  # CDT family

        ema_fast = self.feat.ema(close, timeperiod=...)   # 14/18/30 theo variant
        ema_slow = self.feat.ema(close, timeperiod=...)   # 42/54/90 theo variant

        fundamentals_known = self.op.notna(...) & self.op.notna(...)

        base_entry = <fundamental> & (close > ema_slow)
        strong_entry = base_entry & (ema_fast > ema_slow)
        exit_setup = <explicit>

        self.set_positions(exit_setup, position=0)   # exit ưu tiên trước
        self.set_positions(base_entry, position=0.5)
        self.set_positions(strong_entry, position=1)
```

**Quy tắc:**
- Long-only `[0, 0.5, 1]`, exit đặt trước entry (priority mechanism).
- Chỉ dùng field không suffix `time_series`, point-in-time qua `self.op.notna(...)`.
- Chỉ dùng ops/features đã chứng minh trong batch SIMULATED: `notna`, `pct_change`,
  `ema`, native `> < & |` arithmetic. Không dùng `rolling_mean`/`fillna` (chưa
  VERIFY_PASSED — audit priority 1).
- Cash conversion guard dùng native arithmetic `CFO / NP > 0.5` (không `safe_divide`
  chưa chứng minh), kèm `notna` + `NP > 0`.
- Hysteresis dùng native `close > ema_slow * 1.02` (dead-band theo noise-filtering pattern).
- Không import, không loop, không global aggregation, không negative shift.

## Tiêu chí đánh giá

| Mức | Điều kiện (VN-LARGE-CAP) |
|---|---|
| PASS | Aggregate + Train + Test đều đạt Sharpe≥1.2, CAGR≥15%, MaxDD≥-35%, PF≥1.2, Calmar≥1.1 |
| Candidate | Sharpe ≥ 1.0 & CAGR ≥ 12% |
| Research | Sharpe ≥ 0.6 & MaxDD hợp lý |
| Reject | Sharpe < 0 hoặc không tạo giao dịch |

Ngoài aggregate, **bắt buộc so annual table** — đặc biệt 2022: max drawdown 2022
của variant phải thấp hơn hoặc bằng baseline, và Train Sharpe không được phép
degrade > 15% so với baseline. Variant nào chỉ tăng aggregate nhờ một năm khác nhưng
2022 tệ hơn sẽ bị loại (research rule 6, 7).

## Quy trình implement

1. ✅ Viết plan này.
2. ✅ Gen 10 file vào `output/stage_2/vn_large_cap/time_series/`.
3. ✅ Thêm 10 dòng vào `output/index.csv`.
4. ✅ `python tools/validate_framework.py --strict` → 0 issues.
5. ✅ Dry-run submit batch VN-LARGE-CAP (`--dry-run`), xác nhận editor universe.
6. ✅ Live submit 42/42 OK → `check_results`.

## Kết quả (2026-08-04)

> ⚠️ **Wave 2 defense 2022: REJECTED toàn bộ.** Không variant nào vượt baseline
> trên Aggregate Sharpe. Dữ liệu hiện tại chỉ có Aggregate/Train(=2020–2022)/Test,
> **không có annual table riêng cho 2022** — so sánh 2022 phải proxy qua Train window
> (train_max_drawdown, train_sharpe).

### QTA family (baseline `VnLargeQualityTrendAgreement` — Agg 1.0051 / Train 1.0586 / Test 1.0180)

| Variant | Agg Sharpe | Train Sharpe | Test Sharpe | ΔAgg vs BL | Kết luận |
|---|---:|---:|---:|---:|---|
| Agreement1442 | 0.7382 | 0.7062 | 0.7965 | -0.267 | Reject (train degrade 33%) |
| Agreement1854 | 0.9304 | 0.9916 | 0.8374 | -0.075 | Reject (test worse) |
| AgreementFullExit | 1.0051 | 1.0586 | 1.0180 | 0.000 | **Degenerate — metric trùng baseline từng số** |
| AgreementConversion | 0.9753 | 0.8764 | 1.2127 | -0.030 | Reject (train degrade 17%) |
| AgreementHysteresis | 0.9064 | 0.8866 | 0.9548 | -0.099 | Reject |

**Nhận xét:** `AgreementFullExit` cho metric **trùng khớp từng số** với baseline →
leg exit `close < EMA36` của QTA là redundant với exit `fast break` đã có (8/24 break
luôn xảy ra trước/đồng thời). Variant này là no-op; kiểm tra xóa leg vô dụng. Mọi
EMA chậm hơn đều làm suy giảm Sharpe.

### CDT family (baseline `VnLargeCapexDisciplineTrend` — Agg 1.1272 / Train 1.3555 / Test 0.6624)

| Variant | Agg Sharpe | Train Sharpe | Test Sharpe | ΔAgg vs BL | Kết luận |
|---|---:|---:|---:|---:|---|
| Capex1442 | 1.1202 | 1.3198 | 0.6084 | -0.007 | Reject (test worse) |
| Capex1854 | 0.9880 | 1.1220 | 0.6247 | -0.139 | Reject |
| Capex3090 | 0.9265 | 0.9269 | 0.9133 | -0.201 | Reject (train degrade 32%) |
| CapexDeadband | 0.8835 | 0.9528 | 0.7371 | -0.244 | Reject |
| CapexProfitGuard | 1.1105 | 1.3116 | 0.7220 | -0.017 | Reject (sát baseline) |

**Nhận xét:** Toàn bộ CDT chậm hơn (1442/1854/3090) đều giảm Train Sharpe → càng
chậm càng mất đi sức mạnh của baseline 12/36. Deadband (hysteresis) và ProfitGuard
không cải thiện; ProfitGuard gần nhất baseline nhưng Test vẫn 0.72 < 0.66? — không,
Test 0.7220 > 0.6624, nhưng Train degrade nhẹ và Agg vẫn thấp hơn.

### Kết luận chung

1. **Giả thuyết "chậm EMA → defense 2022" sai.** Slowing timing luôn làm giảm
   Train Sharpe (window chứa 2022); nguồn lợi nhuận của các alpha này nằm ở fast
   re-entry sau 2022, không phải hold-through.
2. **Không có annual 2022 table** trong `results_stage_2.csv` → không thể xác nhận
   maxDD 2022 trực tiếp; proxy bằng train_max_drawdown: mọi variant đều có train
   MaxDD bằng/khá baseline nhưng Train Sharpe thấp hơn → không hữu ích.
3. **`AgreementFullExit` là degenerate no-op** (metric trùng baseline) → leg exit
   `close < EMA36` vô dụng trong QTA; cần xóa để tránh nhiễu manifest.
4. Baseline vẫn giữ nguyên là ứng viên tốt nhất LARGE-CAP (Agg 1.1272) nhưng chưa
   đủ PASS. Hướng tiếp theo nên tập trung vào **Test OOS 0.66** của CDT — vấn đề
   nằm ở overfit 2020–2021, không phải 2022 (audit ghi nhận train 1.35 → test 0.66).
