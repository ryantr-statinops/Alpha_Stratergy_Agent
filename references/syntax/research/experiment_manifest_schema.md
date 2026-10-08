# Experiment Manifest Schema

This document defines the metadata required to track Round 2 alpha research at the hypothesis-family-variant level. Its purpose is to expose trial count, prevent test-set reuse from being mislabeled OOS, and make results reproducible.

## 1. Identity Model

```text
Hypothesis
└── Alpha family
    ├── Baseline
    ├── Variant 1
    ├── Variant 2
    └── Frozen candidate
```

- **Hypothesis:** economic mechanism expected to produce returns.
- **Family:** implementations sharing that mechanism and differing in one or more tested dimensions.
- **Variant:** one exact strategy specification.
- **Frozen candidate:** the variant selected before final OOS is opened.

Renaming a file does not create a new hypothesis or reset its trial count.

## 2. Required Fields

### 2.1 Identity

| Field | Type | Description |
|---|---|---|
| `hypothesis_id` | string | Stable ID, e.g. `HYP-SMALL-QUALITY-001` |
| `family_id` | string | Stable kebab-case family ID |
| `variant_id` | string | `baseline`, `v01`, `p02`, etc. |
| `parent_baseline` | string | Baseline filepath or variant ID |
| `filepath` | string | Path relative to `output/stage_2/` |
| `created_at` | ISO date/time | Creation timestamp |

### 2.2 Research scope

| Field | Type | Description |
|---|---|---|
| `universe` | enum | `VN-SMALL-CAP`, `VN-MID-CAP`, or `VN-LARGE-CAP` |
| `mode` | enum | `time_series` or `cross_sectional` |
| `thesis` | string | Economic mechanism, not code restatement |
| `accounting_scope` | string | Intended business/accounting population |
| `signal_type` | enum/list | level, ratio, event, quality, risk, price, liquidity |
| `fields` | list | Exact `self.data` fields |
| `features` | list | Exact `self.feat` calls/families |
| `operators` | list | Exact `self.op` calls/families |

### 2.3 Trial governance

| Field | Type | Description |
|---|---|---|
| `planned_variants` | integer | Family budget fixed before testing |
| `trial_number` | integer | Sequential family trial number |
| `trials_run` | integer | Total family trials so far |
| `dimensions_changed` | list | Field, period, threshold, mask, weight, sizing, exit |
| `selection_metric` | string | Metric fixed before variant comparison |
| `rejection_rule` | string | Predefined family rejection condition |
| `default_window_dependency` | boolean | Uses an unknown/implicit panel default |

### 2.4 Validation state

| Field | Type | Description |
|---|---|---|
| `validation_status` | enum | Status from `validation_protocol.md` |
| `final_test_opened` | boolean | Whether final OOS metrics have been viewed |
| `final_test_opened_at` | ISO date/time/null | First access time |
| `retuned_after_test` | boolean | Whether design changed after test influence |
| `embargo_verified` | boolean | Whether split gap covers all known lookbacks |
| `train_pass` | boolean/null | Official train-stage threshold result |
| `validation_pass` | boolean/null | Validation-stage result if available |
| `final_oos_pass` | boolean/null | Full final-test threshold result |
| `sharpe_retention` | number/null | Test Sharpe divided by Train Sharpe |

### 2.5 Coverage and evidence

| Field | Type | Description |
|---|---|---|
| `feature_evidence` | mapping/list | Evidence state for panel calls |
| `coverage_train` | number/null | Eligible share or count on train |
| `coverage_test` | number/null | Eligible share or count on test |
| `concentration_note` | string/null | Symbol/sector/weight concentration |
| `known_limitations` | list | Unresolved API, data, or interpretation gaps |

## 3. Idea-File Frontmatter

Every new Stage 2 idea should begin with YAML frontmatter:

```yaml
---
hypothesis_id: HYP-SMALL-QUALITY-001
family_id: small-roa-quality
variant_id: baseline
parent_baseline: null
filepath: vn_small_cap/cross_sectional/VnSmallCsRoaQuality.py
created_at: 2026-08-03
universe: VN-SMALL-CAP
mode: cross_sectional
thesis: Profitable small caps with stronger asset-scaled earnings are underpriced.
accounting_scope: broad_with_financial_sector_caution
signal_type:
  - ratio
  - quality
fields:
  - fun_is_net_profit_loss_after_tax_quarterly_panel
  - fun_bs_total_assets_quarterly_panel
features:
  - safe_divide_panel
operators:
  - rank_cs_panel
  - portfolio_weights_panel
planned_variants: 3
trial_number: 1
trials_run: 1
dimensions_changed: []
selection_metric: validation_sharpe
rejection_rule: Reject if validation Sharpe is non-positive or coverage is unstable.
default_window_dependency: false
validation_status: DRAFT
final_test_opened: false
final_test_opened_at: null
retuned_after_test: false
embargo_verified: false
train_pass: null
validation_pass: null
final_oos_pass: null
sharpe_retention: null
coverage_train: null
coverage_test: null
concentration_note: null
known_limitations:
  - No verified sector-neutralization operator.
---
```

The body must explain concept, mechanism, universe choice, mode, fields, logic, risk, ablations, and validation plan.

## 4. Variant Record

A variant must identify exactly one intended change where possible:

```yaml
hypothesis_id: HYP-SMALL-QUALITY-001
family_id: small-roa-quality
variant_id: v02
parent_baseline: baseline
trial_number: 2
planned_variants: 3
dimensions_changed:
  - liquidity_threshold
change_from_parent: liquidity rank threshold 0.40 -> 0.50
selection_metric: validation_sharpe
final_test_opened: false
retuned_after_test: false
```

If multiple dimensions change, the variant is not a clean ablation and must state why.

## 5. Suggested `output/index.csv` Extension

Current columns should remain backward compatible. Suggested appended columns:

```csv
hypothesis_id,family_id,variant_id,parent_baseline,trial_number,planned_variants,selection_metric,validation_status,final_test_opened,retuned_after_test,default_window_dependency,accounting_scope
```

Example:

```csv
HYP-SMALL-QUALITY-001,small-roa-quality,baseline,,1,3,validation_sharpe,TRAIN_CANDIDATE,false,false,false,broad_with_financial_sector_caution
```

Lists such as fields/features are better kept in idea frontmatter or a dedicated manifest file rather than encoded ambiguously in CSV.

## 6. Optional Machine-Readable Family Manifest

Recommended path:

```text
idea/planning_alpha/stage_2/manifests/<family_id>.yaml
```

Suggested structure:

```yaml
hypothesis_id: HYP-SMALL-QUALITY-001
family_id: small-roa-quality
planned_variants: 3
selection_metric: validation_sharpe
final_test_opened: false
variants:
  - variant_id: baseline
    filepath: vn_small_cap/cross_sectional/VnSmallCsRoaQuality.py
    trial_number: 1
    status: TRAIN_CANDIDATE
  - variant_id: v02
    filepath: vn_small_cap/cross_sectional/VnSmallCsRoaQualityLiq50.py
    trial_number: 2
    status: DRAFT
```

This file is proposed; tooling must not assume it exists until implemented and validated.

## 7. Status Transitions

Allowed normal progression:

```text
DRAFT
-> SYNTAX_VALID
-> SIMULATED
-> TRAIN_CANDIDATE
-> VALIDATION_CANDIDATE
-> OOS_PASS | OOS_FAIL | OOS_FRAGILE
```

If the strategy changes after final test influence:

```text
any final-test state -> INVALIDATED_BY_RETUNING
```

A retuned variant may start a new development cycle, but it cannot reuse the same final test as untouched OOS.

## 8. Trial-Counting Rules

Count a new trial when any of the following changes and is simulated:

- raw field;
- quarterly versus annual frequency;
- ratio denominator;
- transform or feature;
- lookback/period;
- threshold;
- eligibility/liquidity mask;
- factor weight or exponent;
- winsorization/ranking method;
- position sizing;
- exit logic.

Do not reset counts when:

- renaming a file;
- moving it to another folder;
- resubmitting identical code due to timeout;
- creating a new batch around the same thesis.

Identical-code resubmissions should be tracked separately as operational attempts, not research trials.

## 9. Final-Test Access Log

At first access, record:

```yaml
final_test_opened: true
final_test_opened_at: 2026-08-03T10:30:00+07:00
frozen_variant: v02
frozen_commit: <git commit hash>
```

`frozen_commit` ties the OOS claim to exact code. Subsequent code changes must trigger a comparison against that commit and set `retuned_after_test` when design changes.

## 10. Minimum Compliance Checklist

- [ ] Hypothesis, family, and variant IDs are present.
- [ ] Universe and mode are valid.
- [ ] Exact fields/features/operators are recorded.
- [ ] Accounting scope and signal type are declared.
- [ ] Planned family budget precedes testing.
- [ ] Trial number includes failed variants.
- [ ] Selection metric and rejection rule are fixed.
- [ ] Hidden/default panel-window dependencies are disclosed.
- [ ] Final-test access is timestamped.
- [ ] Retuning after test is never hidden.
- [ ] Coverage and concentration limitations are recorded.
- [ ] Validation status follows `validation_protocol.md`.
