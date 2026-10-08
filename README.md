# Alpha Strategy Research Archive

Kho nghiên cứu chiến lược định lượng cho hai round đã hoàn tất. Repo được sắp xếp để tra cứu ý tưởng, strategy, manifest, kết quả và tài nguyên dùng chung; các file nguồn được giữ lại, bao gồm cả bản Round 1 trùng lặp đã có từ trước.

## Bắt đầu tra cứu

- [Hướng dẫn agent](.agents/AGENTS.md)
- [Bộ skill dự án](.agents/skills/)
- [Tình trạng dự án](docs/project_status.md)
- [Round 1 — VN30F futures intraday](docs/rounds/round_1/README.md)
- [Round 2 — Vietnamese equities](docs/rounds/round_2/README.md)
- [Danh mục công cụ](tools/INDEX.md)
- [Syntax và catalog dữ liệu](references/syntax/INDEX.md)
- [Framework và strategy mẫu](references/templates/xnoquant/strategy_framework.md)

## Cây thư mục

```text
.
├── .env                          # Cấu hình riêng hiện có, giữ ở root
├── .agents/                      # AGENTS.md và bộ skill/reference nghiệp vụ
├── docs/                         # Trạng thái dự án và hướng dẫn từng round
├── research/
│   ├── round_1/
│   │   ├── ideas/                # Hypotheses, plans, session notes
│   │   ├── strategies/           # Bản strategy nghiên cứu đã tổ chức theo thesis/loại
│   │   ├── archive_copy/         # Bản sao nguyên trạng từ archive/stage_1 cũ
│   │   ├── manifests/            # Manifest mới và bản nguồn được giữ nguyên
│   │   └── results/              # Kết quả backtest Round 1 nếu có
│   └── round_2/
│       ├── ideas/                # Planning và framework
│       ├── input_materials/      # Input templates của Round 2
│       ├── strategies/           # Universe × mode
│       ├── selected/             # Bốn strategy được tuyển chọn
│       ├── manifests/            # Manifest mới và manifest nguồn
│       └── results/              # Backtests và phân tích
├── src/backtest/                 # Local VN30F backtest engine Round 1
├── tools/                        # CLI dùng chung và công cụ lưu trữ round
├── references/                   # Market notes, syntax, XNOQuant templates
├── tests/                        # Kiểm thử cho code và cấu trúc
└── data_local/round_1/cache/      # Cache dữ liệu VN30F đã lưu
```

## Vị trí manifest và dữ liệu

- Round 1: `research/round_1/manifests/strategies.csv`. Manifest được tạo từ chỉ mục cũ; cột `file_present` đánh dấu các đường dẫn còn tìm thấy sau khi tổ chức lại. `source_index.csv` được giữ nguyên làm bản tham chiếu.
- Round 2: `research/round_2/manifests/strategies.csv`. Bản `source_index.csv` giữ nguyên nội dung ban đầu.
- Round 2 results: `research/round_2/results/backtests.csv`; các bảng và báo cáo phân tích ở `research/round_2/results/analysis/`.
- Round 1 có hai bản strategy: bản tổ chức theo thesis/loại ở `strategies/`, và bản archive nguyên trạng ở `archive_copy/stage_1/`.

Các công cụ API Round 2 được giữ cho mục đích tham khảo/tái lập. Chỉ chạy công cụ submit khi chủ động muốn kết nối XNOQuant và đã kiểm tra cấu hình `.env`.
