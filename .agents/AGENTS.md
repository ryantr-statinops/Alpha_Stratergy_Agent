# AGENTS.md — Hướng dẫn agent cho repository

Repository này là kho lưu trữ nghiên cứu định lượng cho Round 1 và Round 2 đã hoàn tất. Dùng README và tài liệu trong `docs/`, `research/`, `references/`, `src/`, và `tools/` làm nguồn mô tả cấu trúc hiện tại.

## Cách dùng bộ skill

Các skill trong `.agents/skills/` lưu lại hướng dẫn nghiệp vụ và tài liệu agent trước đây. Round-specific workflow, API, đường dẫn và trạng thái trong đó có thể đã cũ; chỉ dùng khi cần tra cứu hoặc tái lập lịch sử, và kiểm tra layout hiện tại trước khi thực hiện thao tác.

| Skill | Nội dung |
|---|---|
| [`readme`](skills/readme/SKILL.md) | Historical agent and workflow guides |
| [`readme-legacy`](skills/readme-legacy/SKILL.md) | ALPHA_BOT - Quantitative Strategy Builder Engine |
| [`alpha-workflow`](skills/alpha-workflow/SKILL.md) | Alpha Workflow Pipeline |
| [`alpha-workflow-engine`](skills/alpha-workflow-engine/SKILL.md) | ALPHA WORKFLOW ENGINE — Autonomous Generate & Improve Loop |
| [`backtest-index-legacy`](skills/backtest-index-legacy/SKILL.md) | backtest/ — Local Backtest Engine |
| [`check-duplicate-guide`](skills/check-duplicate-guide/SKILL.md) | check_duplicate.py — Usage Guide |
| [`framework-build-guide`](skills/framework-build-guide/SKILL.md) | Framework Build Guide — Round 2 (Fundamental Alpha Arena) |
| [`migration-plan-v2`](skills/migration-plan-v2/SKILL.md) | Migration Plan V2 — Chuyển sang Data Model Mới (Vòng 2) |
| [`output-index-legacy`](skills/output-index-legacy/SKILL.md) | output/ — Index |
| [`stage-2-guideline`](skills/stage-2-guideline/SKILL.md) | stage 2 guideline |
| [`submit-workflow`](skills/submit-workflow/SKILL.md) | Submit Workflow — Paste Code lên XNOQuant |
| [`system-health-check`](skills/system-health-check/SKILL.md) | System Health Check — Stage 2 |
| [`tools-index-legacy`](skills/tools-index-legacy/SKILL.md) | Tools INDEX — Alpha Bot |
| [`v2-tool-readiness`](skills/v2-tool-readiness/SKILL.md) | V2 Tool Readiness — Audit toàn bộ vị trí cần sửa trước khi viết tool Round 2 |

## Cấu trúc repository hiện tại

- `docs/rounds/`: README và tài liệu tổng quan theo từng round.
- `research/round_1/`, `research/round_2/`: ideas, strategies, manifests, results và tài liệu đầu vào đã tổ chức theo round.
- `references/`: syntax, market notes và template XNOQuant.
- `src/backtest/`: backtest engine Round 1.
- `tools/`: CLI và index công cụ.
- `tests/`: kiểm thử cấu trúc và code.

## Nguyên tắc làm việc

- Không giả định competition, API, hay workflow submit còn hoạt động chỉ vì tài liệu lịch sử mô tả chúng.
- Trước khi dùng lệnh hoặc đường dẫn trong skill, đối chiếu với README, `tools/INDEX.md`, và file hiện có trong repository.
- Khi chỉ tổ chức tài liệu, giữ nguyên nội dung; không xóa file nếu yêu cầu không cho phép.
