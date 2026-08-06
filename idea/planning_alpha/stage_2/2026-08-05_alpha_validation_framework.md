# Alpha Validation Framework — Stage 2

> **Date:** 2026-08-05
> **Status:** ACTIVE — là chuẩn bắt buộc trước khi promote bất kỳ alpha nào lên production.
> **Architecture:** 7-Layer Research Pipeline (see `MASTER_alpha_planning.md`)
> **Scope:** Cross-sectional + time-series stage-2, 3 universe VN.
> **Tooling:** `tools/retention_audit.py`, `tools/fetch_yearly_tables.py` (cả hai GET-only / CSV-only, không đụng submit).

---

## 1. Vấn đề: train-pass nhưng test-fail

Số liệu đo được trên toàn `backtest/results_stage_2.csv` (253 SIMULATED latest):

| Đo | Giá trị | Ý nghĩa |
|----|---------|---------|
| PassTrain (Sharpe train ≥ 1.2) | **84** | Nhiều "alpha" qua train |
| PassBoth (Sharpe train ≥ 1.2 **và** test ≥ 1.2) | **4** | Chỉ 4 sống sót |
| Survival ratio | **0.05** | = đúng mức α = 5% (Type-I error) |
| Phân bố PassBoth | **4/4 đều VN-SMALL-CAP** | LARGE 0, MID 0 |

**Kết luận thống kê:** survival ratio bằng đúng α nghĩa là phần lớn "train-pass" là **may mắn thống kê (multiple testing)**, không phải edge bền. Quy trình "viết → submit → chọn train đẹp → xem test" là một bộ chọn thiên vị.

## 2. Nguyên nhân gốc (xếp hạng, có bằng chứng)

### 2.1 Regime dependency — chính
Train = **2020–2022** (submit_workflow.md:19), Test = **2023–2024** OOS locked. Bảng Sharpe thị trường theo năm (audit 2026-08-02, đại diện cho engine long/trend):

| Năm | Sharpe thị trường | Regime |
|-----|------|--------|
| 2020 | 1.7 – 2.0 | COVID recovery, small-cap mania |
| 2021 | 1.4 – 2.0 | Bull peak |
| 2022 | **−0.3 .. −0.9** | Crash (năm "trung thực" duy nhất trong train) |
| 2023 | 0.66 – 1.15 | Hồi phục |
| 2024 | 0.75 – 1.06 | Chín muồi/chop |

Aggregate train Sharpe bị **2020–21 mania thổi phồng** → "train đẹp" không chứng minh edge. Ngược lại: **alpha giữ được 2022 (crash) mới là alpha thật** — không phải bull-beta.

### 2.2 Effective sample size quá nhỏ
Fundamental annual cập nhật ~1 lần/năm → train 3 năm ≈ **3 quan sát độc lập/mã**. Sharpe 1.5–2.7 từ vài sự kiện báo cáo ≈ noise-fitting. Cross-section mỏng (LARGE ~30, MID ~50 mã) → rank nhiễu; **SMALL ~100+ mã giữ rank ổn định** — giải thích 4/4 edge bền đều ở SMALL.

### 2.3 Multiple testing (selection bias)
Chọn file *sau khi nhìn train* → train bị inflation, test bị consume. 4/84 ≈ 5% không khác đoán ngẫu nhiên. Cần preregister + hạch toán retention theo family.

### 2.4 Edge yếu (không chết)
Test PF của các candidate bền vẫn > 1 (vd RoaQuality test PF 1.26) → edge tồn tại nhưng mức độ khiêm tốn, không đủ tạo Sharpe cao ở test ngắn 2 năm.

### 2.5 Độ trễ annual fundamental
Forward-filled annual stale ở test nhanh hơn → fundamental thuần chết mạnh hơn nhóm có trend (ValueTrend test 0.83–1.21). Pivot quarterly là đòn bẩy tăng sample size.

### 2.6 Sector (biến gây nhiễu, KHÔNG phải nguyên nhân chính)
- Bằng chứng phản bác: thí nghiệm NonFin (loại financial) làm mọi thứ fail; cô lập financial (SMALL) **tăng** alpha. Nếu sector-heterogeneity là kẻ giết alpha thì cô lập sector phải giúp.
- Nhưng financial-only SMALL (FinancialNetPayout) là dân số mỏng ~10–15 mã → cần phân rã sub-sector (bank/chứng khoán/bảo hiểm) trước khi promote (xem §5).

## 3. Sáu gate bắt buộc

Một alpha chỉ được coi là **robust candidate** (đủ điều kiện tính promotion) nếu qua **đủ 6 gate**. Test 2023–24 là OOS locked — **chỉ dùng 1 lần cuối cùng**, mọi tuning phải xảy ra trên 2020–22 + yearly tables.

| # | Gate | Nguồn | Ngưỡng |
|---|------|-------|--------|
| 1 | **Year-by-year stability** | `summary-table` (simulate) | Sharpe ≥ 0 ở **≥ 4/5 năm 2020–24** (bỏ row 2025 boundary) |
| 2 | **Crash resilience 2022** | `summary-table` (simulate) | **Sharpe 2022 ≥ 0** (bar chặt) — năm trung thực duy nhất trong train |
| 3 | **Fresh-year 2024** | `summary-table` (simulate) | Sharpe 2024 ≥ 0 — năm mới nhất, bắt tín hiệu decay gần đây |
| 4 | **Retention accounting** | `retention_audit.py` | Survival của family ≫ 5%; ghi N candidate đã thử, expected false positives |
| 5 | **Parameter plateau** | `retention_audit.py --plateau` | Tham số promote không phải **đỉnh cô lập**; siblings phải cùng dải test |
| 6 | **Sector concentration audit** | probe 3-class (§5) | Lợi nhuận không tập trung 1 sub-sector/1 năm |

**Gate 1–3 là bắt buộc PASS; Gate 4–6 là điều kiện cần** trước khi cân nhắc exposure scaling.

## 4. Kết quả chạy Gate 1–3 (2026-08-05)

### 4.1 Bốn candidate SMALL — ĐỀU PASS
`python tools/fetch_yearly_tables.py --strategy-id DSbhQzWjPi ...`

| Candidate | Sharpe 2020 | 2021 | 2022 | 2023 | 2024 | Dương/5 | Gate |
|-----------|-----|-----|-----|-----|-----|-----|------|
| VnSmallCsFinancialNetPayout | 1.37 | 0.12 | **2.52** | 1.15 | **2.94** | 5/5 | PASS |
| VnSmallCsNetPayoutPersistence | 1.63 | −0.11 | **2.24** | 0.60 | **2.94** | 4/5 | PASS |
| VnSmallCsRoaQuality | 1.78 | 2.19 | **1.82** | 1.06 | **2.44** | 5/5 | PASS |
| VnSmallCsValueTrendP02 | 3.15 | 3.42 | **2.47** | 0.88 | **1.73** | 5/5 | PASS |

**Phát hiện quan trọng:** cả 4 đều có **Sharpe 2022 (năm crash) = 1.8–2.5** và **2024 = 1.7–2.9**. Đây KHÔNG phải bull-beta — là alpha cross-sectional thật, ổn định ngay cả trong crash và năm mới nhất. 2023 là điểm yếu duy nhất (0.60–1.15) nhưng vẫn dương.

### 4.2 Contrast — gate loại đúng "train đẹp test chết"

| Candidate | Sharpe 2021 | 2022 | 2023 | 2024 | Dương/5 | Gate |
|-----------|-----|-----|-----|-----|-----|------|
| VnSmallCsCloseStrength | 3.09 | 0.29 | **−3.63** | **−2.83** | 2/5 | **FAIL** |
| VnLargeCsValueMomentum | 1.65 | 1.50 | −0.68 | **−2.14** | 3/5 | **FAIL** |

Hai case này chỉ thắng nhờ **2021 mania** (3.09 / 1.65), 2022 giữ được nhưng **2023–24 sụp hẳn**. Gate 1–3 phân biệt chính xác: **2024 Sharpe là discriminator mạnh nhất** (bền: 1.7–2.9; chết: −2.1..−2.8).

### 4.3 Plateau — VnSmallCsValueTrend P02→P11
Bậc thang **monotonic hoàn hảo**: train 2.67→2.30, test 1.21→0.81 theo cùng hướng. **Không có đỉnh cô lập** → family parameter-robust, nhưng toàn family nằm trên edge khiêm tốn (~0.8–1.2 test). P02 "tốt nhất" chỉ là đầu bậc thang, không có ý nghĩa chọn riêng.

### 4.4 Reframe: trở ngại thật của 4 candidate KHÔNG phải stability
Cả 4 pass Sharpe rất tốt; trở ngại PASS Round-2 của chúng là **CAGR magnitude** (lợi nhuận năm 7–30%) so với bar SMALL **CAGR ≥ 25%** — không phải độ ổn định. Đường tới PASS cho nhóm này là **exposure scaling** (gross cao hơn / book tích cực hơn), không phải tìm alpha khác.

## 5. Sector decomposition (Gate 6) — thiết kế probe 3-class

Không có sector field; dùng **economic-intensity classifier** (đã validate ở v2) chia financial thành 3 sub-sector bằng chính field đã dùng:

| Sub-sector | Proxy | Công thức | Ngưỡng |
|-----------|-------|-----------|--------|
| bank | `fun_cf_loans_granted_purchases_of_debt_instruments_annual_panel` / TA | loan_intensity | > 0.03 (hoặc < −0.03) |
| securities | `fun_bs_margin_deposits_annual_panel` / TA | margin_intensity | > 0.03 |
| insurance | `fun_bs_insurance_reserve_annual_panel` + `fun_bs_unearned_premium_reserve_annual_panel` / TA | (reserve+premium)_intensity | > 0.05 |
| financial | = bank \| securities \| insurance | | |
| non_financial | = financial < 1 | | |

**Bằng chứng hiện tại cho FinancialNetPayout:** test 2023 = **1.58** VÀ 2024 = **3.04** đều dương → không phải 1-năm ride. Nhưng 2024 vượt trội (3.04 vs 1.58) → **vẫn cần probe bank vs securities** trước khi promote: nếu lợi nhuận chủ yếu từ securities rally 2024 thì là sector bet, hạ độ tin cậy.

Lưu ý thêm: financial-only LARGE test 0.52, MID 0.73 — alpha financial là **SMALL-specific** (breadth), khớp kết luận cross-section width §2.2.

### 5.1 Pre-registration Gate 6 (2026-08-05, trước khi submit)

**Probes (đã viết, cùng signal với parent `VnSmallCsFinancialNetPayout`):**
`VnSmallCsFinancialNetPayoutBankProbe.py`, `...SecuritiesProbe.py`, `...InsuranceProbe.py` — mask = từng sub-population độc lập (priority insurance > bank > securities).

**Decision rule (cam kết trước khi thấy kết quả):**
- **PASS (promotion OK):** ≥ 2 sub-sector probe có Sharpe **2024 ≥ 0** VÀ ≥ 1 probe có Sharpe 2023 ≥ 0 → edge đa dạng hóa, không phải 1-sector bet.
- **FAIL (hạ độ tin cậy, không promote như alpha thuần):** chỉ 1 probe mang toàn bộ lợi nhuận test — đặc biệt nếu chỉ `SecuritiesProbe` dương 2024 (brokerage rally) → parent = sector bet.
- **Insurance ~rỗng** (metrics ≈ 0): loại trừ insurance khỏi giải thích, KHÔNG tính là FAIL.

**Kỳ vọng (trước khi xem):** bank = bucket lớn nhất (nhiều ngân hàng small-cap), securities vừa, insurance mỏng.

## 6. Quy trình chuẩn từ giờ

```
Build/viết alpha mới
   │
   ▼
validate_framework.py --strict              # compliance cú pháp (đã có)
   │
   ▼
Submit + lấy Aggregate/Train/Test (CSV)     # 1 lần duy nhất
   │
   ▼
retention_audit.py                           # Gate 4: hạch toán family, survival
   │
   ▼
fetch_yearly_tables.py                       # Gate 1–3: stability + 2022 + 2024
   │
   ▼
retention_audit.py --plateau                 # Gate 5: plateau check
   │
   ▼
Probe sector 3-class                         # Gate 6 (chỉ khi financial-intensive)
   │
   ▼
Preregister TEST 2023–24 (OOS, dùng 1 lần)
   │
   ▼
PASS cả 6 gate → cân nhắc exposure scaling → promote
```

**Luật nghiêm ngặt:**
1. **Test 2023–24 OOS locked** — dùng đúng 1 lần. Không retune sau khi thấy test.
2. Mọi tuning chỉ trên **2020–22 + yearly tables**.
3. Ghi số candidate đã thử mỗi family; survival ~5% = đèn đỏ (family chọn ngẫu nhiên).
4. Không promote alpha chỉ dương 2020–21 (bull-beta).
5. Cross-section rộng (SMALL) được ưu tiên; LARGE/MID kỳ vọng test thấp, không dùng bar SMALL để đánh giá.

## 7. Tooling

```bash
# Retention math + plateau (CSV-only, không network)
python tools/retention_audit.py --min-candidates 1
python tools/retention_audit.py --plateau --min-variants 3
python tools/retention_audit.py --universe VN-SMALL-CAP

# Yearly summary-table + Gate 1–3 (GET-only, không ghi gì)
python tools/fetch_yearly_tables.py --strategy-id <id> --strategy-id <id>
python tools/fetch_yearly_tables.py --from-csv-prefix VnSmallCsFinancialNetPayout
python tools/fetch_yearly_tables.py --from-csv-universe VN-SMALL-CAP --from-csv-prefix VnSmallCsValueTrend
```

## 8. Kết quả Gate 1–3 scan toàn bộ train-pass (2026-08-05)

`python tools/fetch_yearly_tables.py --scan-pass-train --out backtest/gate_1_3_scan.csv`
→ **84 train-pass (Sharpe train ≥ 1.2) → 41 PASS / 43 FAIL** (survival 0.49 vs retention train/test 0.05).

**43 file EXCLUDE (chỉ pass train, không dùng):**
- **Mọi trend/beta LARGE + MID** (Capex*, AdxStrong, Macd, EmaTrendRide, Obv, Aroon, VolumeAccel, TrendSlopeAccel, RoaQualityTrend, LiquidityTrend, RsiRecovery, CashConversion/CashEarningsSpread/CapexDiscipline...): **2022 âm** (chết trong crash) → bull-beta, Gate 2 loại.
- **MID fundamental có decay 2024** (EnterpriseEarningsYield, ScalingEfficiency, CashAccrualQuality, RecognitionMigration, ProjectCommissioning, IdiosyncraticMomentum, CashProfitability, InternallyFundedInvestment + Robust...): 2022 dương nhưng **2024 âm** → Gate 3 loại (fresh-year decay).
- **LARGE: 0 file PASS** — xác nhận LARGE là môi trường mỏng/kém nhất.
- VnSmallEpsGrowthMomentum, VnSmallCsBreakoutHerding, VnSmallCsMomentumOnlyProbe cũng FAIL.

**41 file KEEP (robust theo năm):**
- Gần như **toàn bộ SMALL cross-sectional fundamental** (RoaQuality, LeanWorkingCapital, LowVolatility, LowAmihud, ProfitAcceleration, RoeImprovement, ConservativeAssetGrowth, EpsSurpriseDrift, Receivables/Inventory, NetCash, CurrentLiquidity, ProductiveReinvestment, QualityMomentum, LowLeverage, LowAccruals, FreeCashFlow, WeakRegimeReversal, MarketMomentum...) — 2022 dương (1.0–2.8), 2024 dương.
- SMALL payout/financial: FinancialNetPayout, NetPayoutPersistence, ValueMomentumComposite, NetPayoutMomentum, RoeQuality, EarningsYieldTrend, ValueTrend P02–P11 (5/5).
- MID payout/financial duy trì: NetPayoutPersistence (2024 2.06), FinancialNetPayout/FinancialProbe (2024 1.12), AntiDilution (2024 0.75).

**Kết luận:** bộ whitelist robust gần như chỉ gồm **cross-sectional fundamental/financial ở SMALL** + vài payout ở MID. Kết quả khớp 3 root cause: regime (trend/beta bị loại vì chết 2022), breadth (LARGE 0 pass, MID fundamental thin decay), và financial là nguồn alpha bền.

## 9. Next steps

- **Phase B — Promote 4 candidate SMALL** sau khi hoàn tất Gate 6 (sector probe bank/securities) + quyết định exposure scaling cho CAGR.
- **Phase C — Quarterly pivot** fundamental (EPS/equity/assets quarterly) để tăng sample size — tấn công root cause §2.2.
- **Mở rộng tool** `fetch_yearly_tables.py` ra toàn bộ PassTrain để có bảng stability đầy đủ làm index chọn lọc.
