# Alpha Ideas — Wave 3: Q/V noise-filtered (self.op) VN-LARGE-CAP

> **Session:** 2026-08-04
> **Mode:** cross_sectional, market-neutral (`rank_demean_l1`)
> **Universe:** VN-LARGE-CAP
> **Nhiệm vụ:** dùng `self.op` lọc nhiễu lên **các candidate ổn định** (Q04 0.911,
> V06 0.815, Q03) — đúng pattern §8 `cross_sectional/strategy_patterns.md`:
> `winsorize_cs_panel` → `zscore_cs_panel` / `rank_cs_panel` → `portfolio_weights_panel`.

## Lý do

Wave 1: Q04/V06 dùng `zscore_cs_panel` trần trên factor, không winsorize → kết quả
bị 1 vài cực trị kinh tế kéo. Wave 2 composite cùng họ không độn được vì 2 leg quá
correlated. Không thay đổi factor/field; **chỉ thay đổi dimension noise-filtering**.

## Ràng buộc self.op (đã xác minh)

- `winsorize_cs_panel(panel, mask, lower, upper)` + `zscore_cs_panel(panel, mask,
  ddof=1)` + `rank_cs_panel(panel, mask)` — đều có trong guideline §5 (supported CS
  operators) và pattern §8. Evidence: `rank/zscore/portfolio_weights` EXAMPLE_VERIFIED;
  `winsorize` CATALOG_ONLY nhưng được guideline vận hành.
- Giữ mask ≥ 0 như cũ; winsorize/zscore/rank chạy trên mask (loại invalid trước).
- Không đụng field/sign guard của factor gốc.

## 6 phiên bản (mỗi cái đổi 1 dimension noise-filtering)

| # | File | Base | Thay đổi |
|---:|---|---|---|
| 1 | `VnLargeCsPreWcWinsorized` | Q04 | thêm `winsorize(0.02,0.98)` trước zscore |
| 2 | `VnLargeCsPreWcRanked` | Q04 | dùng `rank_cs_panel` (magnitude-robust) thay zscore |
| 3 | `VnLargeCsCashEarningsWinsorized` | Q03 | thêm winsorize trước zscore |
| 4 | `VnLargeCsEarningsWinsorized` | V06 | thêm winsorize trước zscore |
| 5 | `VnLargeCsEarningsRanked` | V06 | dùng `rank_cs_panel` thay zscore |
| 6 | `VnLargeCsPreWcRankedWinsorized` | Q04 | winsorize + rank (phối hợp noise) |

## Đánh giá (VN-LARGE-CAP)

PASS: Sharpe≥1.2, CAGR≥15%, MaxDD≥-35%, PF≥1.2, Calmar≥1.1.
Target chính: xem noise-filtering có độn Q04 (0.911) / V06 (0.815) lên và có làm
Test ổn định hơn mà không đổi factor.

## Quy trình

1. ✅ Viết plan.
2. ✅ Gen 6 file `output/stage_2/vn_large_cap/cross_sectional/`.
3. ✅ Đăng ký vào `output/index.csv`.
4. ✅ `validate_framework.py --strict` → 0 issues.
5. ✅ Live submit 6 file (`--files`) 6/6 OK.
6. ✅ So Train/Test vs Q04/V06 gốc.

## Kết quả (2026-08-04) — DEGENERATE, noise-filter là no-op

> ⚠️ **Tất cả 6 phiên bản noise-filter trả metric trùng khớp từng số với base.**
> Nguyên nhân: `portfolio_weights_panel(method='rank_demean_l1')` **tự rank lại
> signal bên trong** → mọi winsorize/zscore/rank trước đó là phép biến đổi đơn
> điệu bị chốt sau cùng, không đổi thứ hạng tương đối → weights y hệt.

| File | Base | Agg Sharpe | Trùng base? |
|---|---|---:|---|
| PreWcWinsorized | Q04 | 0.9106 | ✅ trùng Q04 gốc |
| PreWcRanked | Q04 | 0.9106 | ✅ trùng Q04 gốc |
| PreWcRankedWinsorized | Q04 | 0.9106 | ✅ trùng Q04 gốc |
| CashEarningsWinsorized | Q03 | 0.3456 | ✅ trùng Q03 gốc |
| EarningsWinsorized | V06 | 0.8148 | ✅ trùng V06 gốc |
| EarningsRanked | V06 | 0.8148 | ✅ trùng V06 gốc |

### Phân tích gốc rễ

`method='rank_demean_l1'` lấy thứ hạng signal → normalize → demean. Vì thế:

- `winsorize_cs_panel` (clip 2–98%) giữ nguyên thứ hạng → no-op.
- `rank_cs_panel` đã rank sẵn → rank lần 2 không đổi thứ hạng → no-op.
- `zscore_cs_panel` là affine transform đơn điệu → no-op.

**Noise-filtering qua self.op VÔ NGHĨA trong CS mode nếu dùng `rank_demean_l1`.**
Đây là degenerate thứ 3 ghi nhận được (sau Q01≡Q02 và AgreementFullExit).
Muốn magnitude/winsorize có hiệu lực phải dùng `method='demean_l1'` (magnitude-
sensitive), nhưng pattern canonical vẫn khuyến nghị `rank_demean_l1` vì scale bất
ổn định — và các CS strategy trước dùng `demean_l1` (như ValueTrendP02) đã thành công.

### Hướng đi đúng

1. **Bỏ hẳn ý tưởng noise-filter trước rank_demean_l1** — không thể cải thiện.
2. Nếu muốn thử magnitude weighting thật: dùng `method='demean_l1'` với winsorize
   (pattern §5) — nhưng đây là thay đổi portfolio constructor, cần so với baseline
   `rank_demean_l1` cùng factor.
3. Q04 (0.911) và V06 (0.815) vẫn là candidates; để qua Sharpe 1.2 cần nguồn alpha
   orthogonal (family M/F) chứ không phải lọc nhiễu cùng factor.