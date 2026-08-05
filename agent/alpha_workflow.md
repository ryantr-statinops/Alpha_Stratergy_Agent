# Alpha Workflow Pipeline

> Date: 2026-08-05
> Purpose: End-to-end workflow from idea to validated alpha

## Pipeline Overview

```
┌─────────────┐    ┌─────────────┐    ┌─────────────┐    ┌─────────────┐    ┌─────────────┐
│   IDEA      │ →  │   BUILD     │ →  │  VALIDATE   │ →  │   SELECT    │ →  │   DEPLOY    │
│             │    │             │    │             │    │             │    │             │
│ • Thesis    │    │ • 4-Layer   │    │ • Gate 1-3  │    │ • Retention │    │ • Submit    │
│ • Data list │    │ • Code      │    │ • Yearly    │    │ • Stability │    │ • Monitor   │
│ • Hypothesis│    │ • Validate  │    │ • Sharpe    │    │ • Corr check│    │ • Rebalance │
└─────────────┘    └─────────────┘    └─────────────┘    └─────────────┘    └─────────────┘
```

## Step 1: IDEA

**Input:** Economic thesis, market observation, or factor research
**Output:** Idea doc with hypothesis, data groups, expected mechanism

**Template:** `idea/planning_alpha/_framework/2026-08-05_alpha_four_layer_template.md`

**Questions to answer:**
1. What economic mechanism drives the signal?
2. Which data groups are needed?
3. Is this a persistent state or report event?
4. What universe/mode is appropriate?
5. What's the expected sign convention?

**Deliverable:** `idea/planning_alpha/stage_2/YYYY-MM-DD_<name>.md`

---

## Step 2: BUILD

**Input:** Idea doc
**Output:** Validated strategy file

**Process:**
1. Follow 4-layer template: DATA → FEAT → MASK → OP → SET_POSITION
2. Run `python tools/validate_framework.py --strict`
3. Fix any validation errors
4. Verify sign conventions for cash-flow fields
5. Test mask coverage (>40% of universe)

**Deliverable:** `output/stage_2/{universe}/{mode}/<StrategyName>.py`

**Validation commands:**
```bash
python tools/validate_framework.py output/stage_2/{universe}/{mode}/<StrategyName>.py --strict
```

---

## Step 3: VALIDATE

**Input:** Strategy file
**Output:** Gate 1-3 pass/fail

**Gates:**

| Gate | Criteria | Tool |
|------|----------|------|
| Gate 1 | Sharpe ≥ 0 in ≥ 4/5 years (2020-2024) | `tools/fetch_yearly_tables.py` |
| Gate 2 | Sharpe 2022 ≥ 0 (crash year) | `tools/fetch_yearly_tables.py` |
| Gate 3 | Sharpe 2024 ≥ 0 (most recent) | `tools/fetch_yearly_tables.py` |

**Process:**
1. Fetch yearly tables: `python tools/fetch_yearly_tables.py <strategy> --out backtest/yearly/`
2. Check Gate 1-3 criteria
3. Record in `backtest/gate_1_3_scan.csv`
4. If FAIL → debug or discard
5. If PASS → proceed to Step 4

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
IDEA → BUILD → Gate 1-3 → SELECT → DEPLOY
         ↓         ↓          ↓
      validate   yearly    retention
      syntax     stability  correlation
                 2022/2024  turnover
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
