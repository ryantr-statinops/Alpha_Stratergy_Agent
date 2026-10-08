# Round 1 local backtest engine

Local engine cho VN30F intraday futures. Các module chính nằm ở root; `features/` chứa indicator helpers, `runners/` chứa thesis strategies và `data/` chứa fetcher cùng script phát triển.

Chạy từ root repo bằng:

```bash
python3 src/backtest/run.py
```

Cache dữ liệu ở `data_local/round_1/cache/`; kết quả backtest mới được ghi vào `research/round_1/results/backtest.csv`.
