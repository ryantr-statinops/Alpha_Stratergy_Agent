# Round 1 — VN30F intraday futures

Round 1 đã kết thúc. Hồ sơ gồm ý tưởng, hypotheses, strategy variants, local backtest engine, manifests và cache dữ liệu.

- Ideas: `research/round_1/ideas/`
- Bản strategy đã tổ chức: `research/round_1/strategies/`
- Bản archive nguyên trạng thứ hai: `research/round_1/archive_copy/stage_1/`
- Manifest: `research/round_1/manifests/strategies.csv`; manifest nguồn: `source_index.csv`
- Engine: `src/backtest/`; cache: `data_local/round_1/cache/`
- Kết quả: `research/round_1/results/`

Manifest mới giữ các dòng từ index cũ và có `file_present` để phân biệt đường dẫn còn tồn tại với mục stale trong index lịch sử.
