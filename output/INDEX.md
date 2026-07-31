# output/ — Index

| Folder | Trạng thái | Mô tả |
|---|---|---|
| `stage_1/` | **ARCHIVE** — vòng 1 (VNFuture intraday futures, không migrate tự động) | 800 files: thesis_01..48, data_type_alpha, multi_feat_alpha, niche_alpha, single_feat_alpha, index.csv, STATS.md |
| `stage_2/` | **ACTIVE** — vòng 2 (Round 2 Fundamental Alpha Arena, daily equity) | tạo trống, điền dần sau migrate |

## Ghi chú

- `stage_1/` giữ nguyên trạng vòng 1 để rollback/đối chiếu — **không sửa**.
- File mới cho Round 2 đi qua `input/` → `tools/migrate_stage2.py` → `stage_2/`.
- Tham chiếu: `agent/migration_plan_v2.md`.
