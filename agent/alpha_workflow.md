# Alpha Workflow Pipeline

> Date: 2026-08-05
> Purpose: End-to-end workflow from idea to validated alpha
> Architecture: 7-Layer Research Pipeline (see `MASTER_alpha_planning.md`)

## Pipeline Overview

```
┌──────────┐   ┌──────────┐   ┌──────────┐   ┌──────────┐   ┌──────────┐   ┌──────────┐
│  IDEA    │ → │  BUILD   │ → │ DIAGNOSE │ → │ VALIDATE │ → │  SELECT  │ → │  DEPLOY  │
│          │   │          │   │          │   │          │   │          │   │          │
│Hypothesis│   │Layer 0-6 │   │IC, IC,   │   │Accounting│   │Retention │   │Submit    │
│Factor    │   │Code      │   │Coverage, │   │Economic, │   │Stability │   │Monitor   │
│Evidence  │   │Eligible  │   │Turnover  │   │Statistical│  │Corr check│   │Rebalance │
└──────────┘   └──────────┘   └──────────┘   └──────────┘   └──────────┘   └──────────┘
```

## Step 1: IDEA

**Input:** Economic thesis, market observation, or factor research
**Output:** Idea doc with hypothesis, factor, expected mechanism

**Template:** `idea/planning_alpha/_framework/HYPOTHESIS_LIBRARY.md`

**Questions to answer:**
1. What economic hypothesis drives the signal? (Pick from HYPOTHESIS_LIBRARY or document new)
2. Which factor does this test? (Value/Quality/Growth/Momentum/Leverage/Liquidity/Efficiency/Capital Allocation/Operating Quality/Risk)
3. What ratios answer "one unit of X creates how much Y?"
4. What validation rules apply? (Layer 4)
5. What universe/mode is appropriate?

**Deliverable:** `idea/planning_alpha/stage_2/YYYY-MM-DD_<name>.md`

---

## Step 2: BUILD

**Input:** Idea doc
**Output:** Validated strategy file

**Process:**
1. Follow 7-layer architecture: Layer 0→6 (see MASTER_alpha_planning.md)
2. Layer 0: Load raw fields
3. Layer 1: Apply primitive transforms (Ratio/Growth/Trend/etc.)
4. Layer 2: Compute economic factor score
5. Layer 3: Run diagnostics (coverage, IC, turnover) — STOP if fail
6. Layer 4: Apply economic validation rules
7. Layer 5: Apply eligibility filters (L1-L10)
8. Layer 6: Composite (if multi-factor)
9. Run `python tools/validate_framework.py --strict`
10. Fix any validation errors

**Deliverable:** `output/stage_2/{universe}/{mode}/<StrategyName>.py`

**Validation commands:**
```bash
python tools/validate_framework.py output/stage_2/{universe}/{mode}/<StrategyName>.py --strict
```

---

## Step 3: VALIDATE

**Input:** Strategy file
**Output:** Gate 1-3 pass/fail + Diagnostics report

**Pre-checks (Layer 3 — Diagnostics):**
Before running backtest, verify:
- Coverage > 70% of universe
- IC > 0.02 (or Rank IC > 0.02)
- Turnover < 80%
- Factor correlation with existing factors < 0.6
- If any fail → STOP. Do not backtest.

**Gates:**

| Gate | Criteria | Tool |
|------|----------|------|
| Gate 1 | Sharpe ≥ 0 in ≥ 4/5 years (2020-2024) | `tools/fetch_yearly_tables.py` |
| Gate 2 | Sharpe 2022 ≥ 0 (crash year) | `tools/fetch_yearly_tables.py` |
| Gate 3 | Sharpe 2024 ≥ 0 (most recent) | `tools/fetch_yearly_tables.py` |

**Process:**
1. Run diagnostics (Layer 3): `python tools/run_diagnostics.py <strategy>` (if available)
2. If diagnostics PASS → fetch yearly tables
3. Check Gate 1-3 criteria
4. Record in `backtest/gate_1_3_scan.csv`
5. If FAIL → debug or discard
6. If PASS → proceed to Step 4

**Tools:**
```bash
# Fetch yearly performance
python tools/fetch_yearly_tables.py output/stage_2/{universe}/{mode}/<StrategyName>.py --out backtest/yearly/

# Run retention audit
python tools/retention_audit.py --results backtest/results_stage_2.csv
```

---

## Step 4: SELECT

**Input:** Gate 1-3 PASS strategies
**Output:** Portfolio of validated alphas

**Criteria:**
1. Retention rate: survival = pass-both / pass-train (target: >10%)
2. Yearly stability: consistent performance across years
3. Correlation check: low correlation with existing alphas
4. Turnover: manageable trading costs
5. Capacity: sufficient liquidity for position sizes

**Process:**
1. Review Gate 1-3 scan results
2. Check retention metrics in `backtest/results_stage_2.csv`
3. Run correlation analysis between PASS strategies
4. Select diverse set (different mechanisms, low correlation)
5. Document selection rationale

**Deliverable:** Portfolio composition doc

---

## Step 5: DEPLOY

**Input:** Selected portfolio
**Output:** Live strategy

**Process:**
1. Submit to platform via `agent/submit_workflow.md`
2. Monitor daily performance
3. Rebalance on schedule
4. Track drawdown and risk metrics
5. Revalidate quarterly

**Monitoring:**
- Daily: check positions, PnL
- Weekly: review turnover, costs
- Monthly: compare vs benchmark
- Quarterly: re-run Gate 1-3 check

---

## Tool Reference

| Tool | Purpose | Location |
|------|---------|----------|
| `validate_framework.py` | Syntax/mode validation | `tools/` |
| `fetch_yearly_tables.py` | Yearly performance + Gate 1-3 | `tools/` |
| `retention_audit.py` | Retention metrics + plateau | `tools/` |
| `results_stage_2.csv` | All strategy metrics | `backtest/` |
| `gate_1_3_scan.csv` | Gate 1-3 results | `backtest/` |

---

## Quality Gates Summary

```
IDEA → BUILD (Layer 0-6) → DIAGNOSE → VALIDATE → SELECT → DEPLOY
         ↓                      ↓           ↓          ↓
      validate              IC, coverage  Gate 1-3  retention
      syntax                turnover      yearly    correlation
                            exposure      2022/2024 turnover
```

**Pass rates (historical):**
- Train pass: 84/253 (33%)
- Gate 1-3 pass: 41/84 (49%)
- Overall survival: 41/253 (16%)

**Target:**
- Gate 1-3 pass: >50%
- Retention (pass-both / pass-train): >10%
- Portfolio Sharpe: >1.5
- CAGR: >25%
