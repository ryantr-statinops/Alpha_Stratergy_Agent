# 10 New Thesis Ideaplan — Batch 39 to 48

**Scope:** `thesis_39_gap_open_reversion` → `thesis_48_range_expansion_followthrough`

**Goal:** Turn the 10 newly created thesis folders into a consistent, submit-ready research batch, then iterate toward XNOQuant-compatible implementations with better verification stability and higher backtest quality.

**Current state:**
- 10 thesis folders were created under `output/`
- 10 minimal `.py` strategies were created and submitted once
- 5 passed verify/simulate, 5 failed on platform restrictions
- Results were saved to `backtest/results.csv`

**Key constraints learned from submit pass:**
- `self.feat.shift(...)` is not allowed in this sandbox
- `self.op.minimum(...)` is not allowed
- `hasattr(...)` is not allowed in sanitized strategies
- `verify` / `simulate` can trigger rate limits, so pacing matters

---

## Thesis Summary

| Thesis | Theme | Current state |
|---|---|---|
| `thesis_39_gap_open_reversion` | Gap fade / open reversion | Fails verify due to unsupported shift |
| `thesis_40_liquidity_void_rebound` | Range/void rebound | Passes verify and simulate |
| `thesis_41_entropy_trend_filter` | Entropy-based trend gating | Fails verify due to unsupported shift |
| `thesis_42_price_impact_decay` | Exhaustion / impact decay | Passes verify, metrics still incomplete |
| `thesis_43_session_transition_drift` | Session drift / carryover | Fails verify due to unsupported shift |
| `thesis_44_volume_cluster_persistence` | Volume persistence | Passes and best Sharpe so far |
| `thesis_45_tail_risk_momentum` | Tail-risk filtered momentum | Fails verify due to unsupported minimum |
| `thesis_46_intraday_liquidity_skew` | Intraday skew | Passes verify and decent metrics |
| `thesis_47_funding_basis_carry` | Basis / carry proxy | Fails verify due to `hasattr` |
| `thesis_48_range_expansion_followthrough` | Range expansion follow-through | Passes verify, metrics incomplete |

---

## Working Hypothesis

The first implementation pass showed that the strongest ideas are the ones that:
1. rely on simple platform-supported operators,
2. avoid unsupported lookback helpers that are not exposed in sanitize,
3. use direct price/volume relations instead of Python introspection,
4. and keep the logic compact enough for stable verify/simulate cycles.

Therefore, the next iteration should focus on two parallel tracks:
- **Track A: compatibility cleanup** for the 5 failing theses
- **Track B: quality improvement** for the 5 passing theses, especially Sharpe, CAGR, and MaxDD

---

## Implementation Plan

### Phase 1 — Make all 10 strategies platform-safe

#### 1. Replace unsupported lag logic
For theses 39, 41, 43, and any other strategy using `self.feat.shift`, replace lag comparisons with allowed alternatives already present in the repo style:
- `rolling_mean(...)`
- `rolling_sum(...)`
- `crossed_above(...)`
- `crossed_below(...)`
- direct current-bar relationships

**Target outcome:** no `shift` calls remain in the 10 thesis files.

#### 2. Replace unsupported min/max helpers
For thesis 45, replace `self.op.minimum(ret, 0)` with an allowed pattern:
- derive downside pressure via boolean conditions
- or use `ret < 0` gates with absolute-return transforms

**Target outcome:** tail-risk proxy remains, but the implementation uses only supported operations.

#### 3. Remove introspection / sanitize blockers
For thesis 47, remove `hasattr(...)` and choose a fixed data source strategy:
- either assume `pv_vwap_px` is available if it is standard in this codebase
- or replace the basis proxy with `pv_close` vs `rolling_mean(close)` to avoid optional access

**Target outcome:** no sanitizer-blocked expressions remain.

---

### Phase 2 — Improve metrics of the passing strategies

#### 4. Strengthen thesis 44 for drawdown control
`thesis_44_volume_cluster_persistence` currently has the best Sharpe but weak drawdown.

Planned upgrades:
- add a volatility filter
- add an exit on momentum decay
- reduce exposure when volume persistence weakens

**Target outcome:** preserve Sharpe while improving MaxDD.

#### 5. Tighten thesis 46 for Sharpe and CAGR balance
`thesis_46_intraday_liquidity_skew` has strong Calmar and PF, but Sharpe/CAGR still need improvement.

Planned upgrades:
- add trend confirmation
- use a stricter skew threshold
- gate trades by range expansion or low-noise regime

**Target outcome:** push Sharpe above target without inflating drawdown.

#### 6. Convert thesis 40 / 42 / 48 from generic prototypes into thesis-specific edges
These pass, but the logic is still very generic.

Planned upgrades:
- thesis 40: define a clearer void/rebound regime using range compression → expansion sequence
- thesis 42: make impact decay directional instead of symmetric
- thesis 48: require follow-through confirmation after range expansion

**Target outcome:** make the thesis identity clearer and reduce overfitting risk.

---

### Phase 3 — Normalize file structure and documentation

#### 7. Add minimal documentation to each thesis folder
For each of the 10 thesis folders, add:
- `README.md` — thesis description and intent
- `spec.md` — signal definition and rules
- `validation.md` — submit result summary and next tweak notes

**Target outcome:** each thesis folder becomes self-describing and easier to resume later.

#### 8. Keep the folder naming stable
Use the current folder names and keep the `.py` files aligned with the thesis ID.

**Target outcome:** clean navigation and no duplicate naming collisions.

---

### Phase 4 — Re-submit and measure

#### 9. Re-run submit/check on the modified files only
Use `tools/submit_and_check.py` in interactive mode or a controlled batch so only updated files are re-tested.

**Target outcome:** compare new metrics to the first pass and identify winners.

#### 10. Promote winners into the next research round
Classify each thesis as:
- **Keep** — passes and reaches target metrics
- **Refine** — passes but needs metric improvement
- **Drop** — fails too often or remains structurally weak

**Target outcome:** create a clear next-round shortlist.

---

## Recommended Execution Order

1. Fix thesis 39, 41, 43, 45, 47 for compatibility
2. Re-submit and confirm all 10 are at least verify-safe
3. Improve thesis 44 and 46 first because they are already close to useful quality
4. Then refine 40, 42, and 48 for thesis-specific edge clarity
5. Finally document all folders and capture the next action per thesis

---

## Success Criteria

A thesis is considered ready for the next round when:
- it verifies and simulates without platform errors,
- it has a clean folder-level README/spec/validation trail,
- and it produces metrics that are either competitive or clearly promising.

**Practical near-term target:**
- at least 8/10 strategies verify successfully
- at least 2 strategies meet or beat the current best metrics profile after the second pass

---

## Notes for the next agent pass

- Do not use unsupported helpers like `shift`, `minimum`, or introspection functions.
- Keep code simple and explicit.
- Prefer supported rolling statistics and direct price/volume relationships.
- Re-check after each small edit rather than changing all 10 at once.
- Record every submit result in `backtest/results.csv` and folder-level validation notes.
