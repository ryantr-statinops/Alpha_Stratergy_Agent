# Context Session — Alpha Bot (New Strategy Cycle)

**Session Date:** 2026-07-02  
**Purpose:** New strategy cycle — fresh approach based on VN derivatives market microstructure  
**Next Agent:** Read this first, then proceed

---

## 1. Project Overview

Dự án nghiên cứu và phát triển chiến lược đầu tư định lượng cho nền tảng **XNOQuant**, tập trung vào thị trường phái sinh VnFuture (VN30F1M).

**Target:** Published strategies cho Vietnam Quant Challenge 2026  
**Current Status:** Brainstorming phase — 5 new ideas documented, no strategies generated yet  
**User tightened targets:** Sharpe ≥ 2.5 (min 2.0), CAGR > 20%, Max DD > -20%, PF > 1.3, Calmar > 1.1

**Core Tech Stack:**
- Python on XNOQuant platform
- Framework: `SimpleAlgorithm` → `CustomStrategy`
- API: `self.data`, `self.feat`, `self.op`, `self.set_positions()`

---

## 2. Current Session — Active Work

### 5 New Alpha Ideas (VN Market Specific)
| # | Idea | Core Concept | TF | Status |
|:-:|------|-------------|:--:|--------|
| 1 | **Cascade Catcher** | Margin call domino — OI drop + volume spike | 5-15min | 🎯 **Active — Hypothesis written** |
| 2 | **Basis Bounce** | Futures-cash basis extreme reversion | 30-60min | ⏳ Planning |
| 3 | **Lunch Gap** | Pre/post lunch thin market reversal | 5min | ⏳ Planning |
| 4 | **Whale Footprint** | Average trade size surge detection | 15-30min | ⏳ Planning |
| 5 | **Retail Exhaustion** | Volume spike panic/FOMO reversal | 5-15min | ⏳ Planning |

**Storage:**
- Alpha ideas: `idea/planning_alpha/alpha_5_new_ideas_cascade_basis_lunch_whale_exhaustion.md`
- Hypothesis docs: `idea/hypothesis/hyp_cascade_catcher_margin_call_domino.md`
- Output: (not yet generated)

---

## 3. Active Hypothesis

### HYP-CASCADE-001: Cascade Catcher (Idea 1)

**Logic:** Short khi OI drop > 1% + matched_volume > 2x SMA + price drop > 0.5%, confirm bằng return_roll < 0 + ADX > 22. Long khi cascade exhaustion (volume collapse + price stabilize).

**Targets:** Sharpe ≥ 2.0, Win Rate ≥ 55%, PF ≥ 1.5, Max Consecutive Losses ≤ 3

**Status:** ✅ Coded & generated — 12 strategies (3 variants × 4 TFs) in thesis_06_volume_flow
- 3 variants: CCStd, CCAggr, CCCons
- 4 timeframes: 5min, 15min, 30min, 60min
- 100% validated (27,061 checks)

**Next step:** Upload to XNOQuant → Simulate → Scorecard

---

## 4. Enhancement Status (Deprecated — Fresh Start)

Tất cả Phase 1/2/3 cũ đã clear. Enhancements mới sẽ được thiết kế theo từng idea cụ thể.

---

## 5. Workflow Status

```
Step 1: Alpha Generation    ✅ (5 new ideas in planning_alpha/)
Step 2: Planning & Hypoth   ✅ (1 hypothesis written — Cascade Catcher)
Step 3: User Review         ✅ Approved
Step 4: Chain-of-Thought    ✅ Coded — cascade_catcher template in generator
Step 5: Output              ✅ 849 strategies (12 cascade catcher + 837 legacy) — valid 100%
```

---

*End of Context Session — Awaiting user review for HYP-CASCADE-001.*
