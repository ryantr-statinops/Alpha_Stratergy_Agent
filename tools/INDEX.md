# Tools

Các round đã hoàn tất. Script được giữ để tra cứu hoặc tái lập nghiên cứu; script submission có thể gọi XNOQuant API khi chạy chế độ live.

## Round 2 — Vietnamese equities

| Script | Tác dụng | Mặc định |
|---|---|---|
| `validate_framework.py` | Kiểm tra strategy theo framework | `research/round_2/strategies/` và manifest mới |
| `alpha_gate.py` | Chạy các bước kiểm tra offline trước submit | Round 2 cross-sectional strategies |
| `factor_diagnostics.py` | Chẩn đoán feature/field | Backtests và analysis trong `research/round_2/results/` |
| `economic_validation.py` | Kiểm tra nhất quán dữ liệu tài chính | Round 2 cross-sectional strategies |
| `submit_and_check.py` | Gửi strategy, lấy metrics | Live API; cần cấu hình `.env` |
| `check_results.py` | Lọc và xem kết quả | `research/round_2/results/backtests.csv` |
| `backfill_split_metrics.py` | Lấy bổ sung train/test metrics | Chế độ chỉ đọc nếu không dùng `--write` |
| `retention_audit.py` | Phân tích retention và parameter plateau | Round 2 backtests CSV |
| `fetch_yearly_tables.py` | Lấy bảng kết quả theo năm | API read-only; cần token |
| `update_guide_stats.py` | Tạo thống kê từ manifest | `research/round_2/manifests/strategies.csv` |

## Round 1 — VN30F futures

| Script | Tác dụng |
|---|---|
| `generate_strategies.py` | Generator strategy cũ; ghi vào `research/round_1/strategies/by_thesis/` |
| `gen_single_feat.py` | Generator single-feature cũ; ghi vào `research/round_1/strategies/by_type/single_feat_alpha/` |
| `src/backtest/run.py` | Chạy local backtest; cache trong `data_local/round_1/cache/` |

## Dùng chung

`common.py`, `editor_pool.py` và các helper hỗ trợ CLI Round 2. Xem `--help` của từng script để biết tùy chọn. Các hướng dẫn workflow lịch sử được lưu tại `docs/historical_agent_guides/`.
