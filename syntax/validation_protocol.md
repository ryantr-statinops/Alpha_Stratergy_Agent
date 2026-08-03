# Strategy Validation Protocol

This document is the canonical research-validation contract for Round 2 strategies. Aggregate backtest success is not sufficient. A promoted alpha must be technically valid, causally constructed, tracked as part of an experiment family, and confirmed on data that did not influence its design.

## 1. Validation Ladder

| Level | Name | Required evidence |
|---|---|---|
| L0 | Catalog valid | Every field, feature, and operator is documented |
| L1 | Syntax valid | XNOQuant verification and local strict validation pass |
| L2 | Contract valid | Mode, shape, position, and point-in-time rules pass |
| L3 | Simulated | Aggregate simulation completes with metrics |
| L4 | Train candidate | Baseline/ablation evidence is acceptable on development data |
| L5 | Validation candidate | Family selection is stable on chronological validation data |
| L6 | Final OOS evaluated | Frozen strategy is evaluated on locked test data |
| L7 | OOS pass | Test thresholds, degradation, coverage, and protocol rules pass |

No lower level implies a higher level. `SIMULATED` is not synonymous with validated.

## 2. Required Experiment Stages

Preferred chronological design:

```text
Train 60% -> Validation 20% -> Final OOS 20%
```

- **Train:** develop the baseline and run one-component ablations.
- **Validation:** select among preregistered variants in one alpha family.
- **Final OOS:** confirm the frozen winner once.

If the platform exposes only Train/Test:

- use Train as development data;
- preregister a small family and selection rule before any Test access;
- treat Test as locked final OOS;
- do not retune after reading Test and continue calling it OOS.

Splits must be chronological, never random.

## 3. Alpha Family Is the Unit of Testing

Strategies that share a thesis and differ by a field, threshold, weight, period, exponent, mask, sizing, or exit belong to one family.

Example:

```text
Family: small-cap value x trend
Variants: P02, P03, ... P11
```

These are not ten independent discoveries. The trial count is ten, and the selection process must be disclosed.

Before running a family, record:

- hypothesis and economic mechanism;
- universe and mode;
- baseline;
- planned variants;
- dimensions allowed to change;
- selection metric;
- rejection rule;
- split policy;
- whether final test has been opened.

Use `experiment_manifest_schema.md` for the record format.

## 4. Locked-Test Rule

A test remains OOS only while its results have not influenced:

- field choice;
- feature choice;
- parameter or threshold;
- eligibility mask;
- factor weight/exponent;
- position sizing;
- exit logic;
- strategy-family selection.

If any of these change after seeing test results:

```text
validation_status = INVALIDATED_BY_RETUNING
```

The old test becomes development evidence. A new untouched period is required for another final OOS claim.

Repeatedly submitting variants against the same visible test is test-set optimization, even if each file has a different name.

## 5. Embargo and Leakage Control

Use a gap between development and evaluation periods when rolling features or report events can cross the boundary.

Minimum principle:

```text
embargo >= maximum known feature lookback
```

Also consider:

- report publication/event holding horizon;
- forward-filled stale fundamentals;
- overlapping return labels if introduced later;
- unknown panel defaults.

If a panel feature's lookback is unknown, mark `embargo_verified: false`; do not claim that the split is fully purged. Resolve the API contract before final promotion.

## 6. Baseline and Ablation Protocol

Required sequence:

```text
B0: simplest economically valid baseline
B1: B0 + one component
B2: B1 + one component
B3: B2 + one component
```

At each step:

1. Change one dimension only.
2. Record aggregate, train, validation/test metrics.
3. Record coverage and turnover where available.
4. Keep a component only if improvement is economically explainable and stable.
5. Record failed variants; do not retain only winners.

Do not optimize period, threshold, factor composition, mask, sizing, and exit in the same iteration.

## 7. Universe Pass Thresholds

The executable source of truth is `PASS_THRESHOLDS_BY_UNIVERSE` in `tools/common.py`. Current documented targets are:

| Universe | Sharpe | CAGR | MaxDD | Profit Factor | Calmar |
|---|---:|---:|---:|---:|---:|
| `VN-SMALL-CAP` | >= 1.0 | >= 25% | >= -45% | >= 1.30 | >= 0.8 |
| `VN-MID-CAP` | >= 1.1 | >= 20% | >= -40% | >= 1.25 | >= 1.0 |
| `VN-LARGE-CAP` | >= 1.2 | >= 15% | >= -35% | >= 1.20 | >= 1.1 |

If this table and `tools/common.py` differ, the code is authoritative and this file must be updated.

Final OOS PASS requires all five test metrics to pass. Aggregate PASS cannot override Test FAIL.

## 8. Degradation and Stability Rules

In addition to absolute thresholds, report:

```text
sharpe_retention = test_sharpe / train_sharpe
sharpe_delta = test_sharpe - train_sharpe
cagr_retention = test_cagr / train_cagr
```

Starting promotion rules when denominators are positive:

- Test Sharpe must be positive and pass its universe threshold.
- Test CAGR must be positive and pass its universe threshold.
- All five official test metrics must pass.
- Sharpe retention should be at least 50%; otherwise label the result `OOS_FRAGILE` even if absolute thresholds pass.
- No central performance metric should reverse sign.
- A result dependent on one short subperiod must not be promoted without further evidence.

The 50% retention rule is a conservative initial governance threshold, not a competition rule. Revisions require documented evidence and must not be made to rescue a known strategy.

## 9. Parameter-Neighbourhood Robustness

Do not promote a narrow optimum. Predefine neighbouring specifications and check whether the thesis survives.

Valid neighbourhood dimensions may include:

- one adjacent period profile;
- one nearby eligibility threshold;
- one nearby factor weight;
- one simpler sizing choice;
- one simpler exit.

Rules:

- vary one dimension at a time;
- count every neighbour as a family trial;
- do not search an unbounded grid;
- do not claim period robustness for hidden panel defaults;
- prefer a plateau to the highest isolated point.

## 10. Mode-Specific Validation

### 10.1 Time series

Audit:

- breadth across symbols;
- contribution concentration;
- percentage of symbols with positive performance;
- exposure and flat-time distribution;
- performance across market regimes;
- sensitivity to trend/exit horizon;
- whether a few names dominate the universe result.

A universe-level result is fragile when only a small number of symbols provide the edge.

### 10.2 Cross sectional

Audit:

- median/minimum eligible symbols;
- train/test coverage;
- empty or zero-weight dates;
- maximum absolute weight if available;
- gross and net exposure;
- turnover;
- factor and sector/accounting concentration;
- sensitivity to winsorization and liquidity thresholds.

A market-neutral label does not guarantee sector, size, liquidity, or beta neutrality.

## 11. Fundamental-Specific Validation

For fundamental alphas:

- count actual report updates, not forward-filled daily rows;
- distinguish persistent states from event signals;
- compare quarterly and annual coverage;
- check accounting-population compatibility;
- verify cash-flow sign conventions;
- inspect sign-changing denominators/bases;
- measure whether missingness is the real selector.

See `fundamental_data_contract.md`.

## 12. Multiple-Testing Disclosure

Every report must include:

```text
candidate fields considered
fields actually tested
ratios tested
parameter variants tested
mask variants tested
number of simulations
number of times final test was viewed
```

A strategy selected from many trials receives a stronger burden of evidence. Do not reset the trial count by renaming a file or starting a new batch with the same thesis.

Where formal multiple-testing correction is unavailable, control risk through:

- preregistration;
- small planned families;
- locked final OOS;
- simple baselines;
- neighbourhood stability;
- transparent failure retention.

## 13. Decision Statuses

| Status | Meaning |
|---|---|
| `DRAFT` | Idea/code under construction |
| `SYNTAX_VALID` | Technical validation passed |
| `SIMULATED` | Aggregate metrics available |
| `TRAIN_CANDIDATE` | Development evidence acceptable |
| `VALIDATION_CANDIDATE` | Frozen candidate selected without final-test influence |
| `OOS_FAIL` | Final test fails official thresholds |
| `OOS_FRAGILE` | Absolute result may pass but degradation/coverage/robustness is weak |
| `OOS_PASS` | Full protocol and final test pass |
| `INVALIDATED_BY_RETUNING` | Strategy changed after final-test results influenced design |

Only `OOS_PASS` may be described as validated. Competition submission policy may be less strict, but research status must remain honest.

## 14. Required Result Record

```yaml
hypothesis_id: HYP-...
family_id: ...
variant_id: ...
universe: VN-SMALL-CAP
mode: cross_sectional
trials_planned: 3
trials_run: 3
final_test_opened: true
retuned_after_test: false
embargo_verified: false
train_pass: true
validation_pass: true
final_oos_pass: false
sharpe_retention: 0.42
coverage_train: <value>
coverage_test: <value>
validation_status: OOS_FAIL
```

## 15. Operational Checks

```bash
python tools/validate_framework.py --strict
python tools/submit_and_check.py --batch --dry-run --universe VN-<CAP>
python tools/check_results.py --splits --universe VN-<CAP>
```

`--dry-run` does not call the API. Universe must still be selected manually on the XNOQuant editor before a live submit.

## 16. Final Promotion Checklist

- [ ] Hypothesis and family were registered before testing.
- [ ] Trial budget and selection metric were fixed in advance.
- [ ] Strategy passes catalog, syntax, mode, shape, and point-in-time checks.
- [ ] Baseline and one-component ablations are recorded.
- [ ] Split is chronological.
- [ ] Embargo covers known lookbacks, or uncertainty is disclosed.
- [ ] Final test did not influence the frozen strategy.
- [ ] All five official test metrics pass.
- [ ] Sharpe retention and metric deltas are reported.
- [ ] Parameter neighbourhood is stable.
- [ ] Coverage and concentration are acceptable for the mode.
- [ ] All failed and successful family variants remain counted.
- [ ] Status is not `INVALIDATED_BY_RETUNING`.
- [ ] Result is labelled `OOS_PASS` only after every requirement passes.
