# Commit + Push Plan

## Mục tiêu
- Giữ thay đổi nhỏ nhất có thể.
- Mỗi commit chỉ chứa 1 nhóm logic rõ ràng.
- Push ngay sau mỗi commit.

## Trạng thái hiện tại
- Đã có các vòng unique hóa và submit cho `output/niche_alpha/`.
- 12 file còn fail đang được ưu tiên theo hướng uniqueness + pass rate.
- `backtest/strategy_index.json` đang là file sinh tự động, không đưa vào commit này.

## Kế hoạch commit nhỏ nhất
1. Commit 1: thêm file plan này.
2. Commit 2: chỉ sửa nhóm `NATR_EXPANSION` nếu có chỉnh thêm.
3. Commit 3: chỉ sửa nhóm `HAMMER_DOJI` nếu đổi concept.
4. Commit 4: chỉ sửa nhóm `ROLLING_RANK_BREAKOUT` và `TSF_BREAKOUT` nếu cùng concept cần tách.
5. Commit 5: chỉ sửa nhóm reversal candle còn lại nếu có thay đổi.

## Quy tắc commit
- Không gộp nhiều archetype vào cùng một commit.
- Không commit file sinh tự động hoặc file ngoài scope.
- Sau mỗi commit: `git push` ngay.

## Quy tắc dừng
- Dừng khi file đã đạt pass hoặc concept đã được xác nhận unique.
- Nếu một file vẫn ra `0,0,0,0,0` sau 1 vòng chỉnh, đổi concept thay vì tweak ngưỡng.

## Thứ tự ưu tiên
1. `NC_NATR_EXPANSION_ADX_15min.py`
2. `NC_HAMMER_DOJI_REVERSAL_ADX_15min.py`
3. `NC_ROLLING_RANK_BREAKOUT_ADX_15min.py`
4. `NC_TSF_BREAKOUT_ADX_15min.py`
5. Các file candle reversal còn lại nếu cần
