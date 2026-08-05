# Cross-Sectional Parameter Reference (Round 2 — Daily Equity)

Canonical research parameters for `cross_sectional` strategies. API signatures remain in [`feature_syntax.md`](feature_syntax.md) and [`operations_syntax.md`](operations_syntax.md). These values are starting points and governance constraints, not guaranteed alpha.

## Canonical Parameters

| Feature / operation | Parameter | Canonical value | Role |
|---|---|---|---|
| `rank_cs_panel` | `method` | `'average'` | Stable tie handling |
| `winsorize_cs_panel` | `lower / upper` | `0.02 / 0.98` | Outlier control before magnitude-based scoring |
| `zscore_cs_panel` | `ddof` | `1` | Cross-sectional standardization |
| `portfolio_weights_panel` | `method` | `'rank_demean_l1'` | Market-neutral rank portfolio |

## Panel Feature Parameters

Panel feature signatures are not inferred from similarly named time-series features. Do not pass `timeperiod` or `window` to a panel feature unless its cross-sectional catalog explicitly documents that argument.

A feature with an undocumented internal window must declare:

```yaml
default_window_dependency: true
default_window_value: unknown
```

Unknown defaults are not parameter choices and must not be tuned indirectly.

## Eligibility Parameters

Eligibility is part of the model, not neutral preprocessing. Every threshold must be preregistered and counted as a variant dimension.

| Dimension | Baseline | Research rule |
|---|---|---|
| Positive price | `close > 0` | Availability guard |
| Positive volume | `volume > 0` | Minimal tradability guard, not sufficient liquidity proof |
| Positive denominator | `denominator > 0` | Required for economically valid ratios |
| Minimum coverage | No global default | Measure before selecting a threshold |
| Liquidity rank cutoff | No global default | At most a small preregistered neighbourhood |
| Maximum absolute weight | No global default | Apply only when API and concentration behavior are verified |

Do not add several eligibility thresholds together after viewing Test results.

## Fundamental Change / Deterioration Thresholds

Cross-sectional mode has no suffix-less `pct_change`. Express change signals as
a delta scaled by a positive denominator, or as a ratio against a trailing
level:

```python
asset_scaled_change = self.feat.safe_divide_panel(
    self.feat.delta_panel(series),
    total_assets,
)

level_ratio = self.feat.safe_divide_panel(series, self.feat.ema_panel(series))
```

Always keep the denominator positive; a raw delta around sign-changing
profit/EPS is unsafe without a positive-level guard.

Eligibility on change signals uses tolerance bands, not a strict zero. The
threshold is the deterioration boundary, not the positivity boundary:

| Role | Threshold (scaled by positive denominator) | Notes |
|---|---:|---|
| Loose / weak guard | `> -0.02` | Keeps near-zero but not yet bad names in the cross-section |
| Positive confirmation | `> 0` | Strong / overlay tier |
| Material deterioration | `< -0.05` | Exclusion or short bias |
| High-noise sector fields | `-0.05 / -0.15` | Sector-specific only |

Rules:

- A strict `> 0` gate on growth or delta collapses the eligible cross-section.
  Small cross-sections make `_cs_panel` ranks noisy and unstable. Audit the
  eligible symbol count per date and prefer a loose weak guard plus a strong
  confirmation tier, mirroring the template weak/strong/exit structure.
- Report-step change is an overlay, not a hard eligibility gate. Do not freeze a
  date's cross-section on a single report event unless the thesis demands it.
- Do not impute missing changes with zero; missing observations are unavailable
  and drop out of the cross-section.
- A change threshold and a level threshold are separate trial dimensions; count
  each variant in the family budget.

## Factor Combination

Baseline composite construction uses equal contribution between independently motivated ranks unless a different weighting is preregistered.

```text
factor A rank + factor B rank
```

Avoid exponent searches and repeated multiplication of the same factor. A factor weight, transform, or eligibility cutoff each counts as a separate trial dimension.

## Portfolio Construction

Canonical baseline:

```python
weights = self.op.portfolio_weights_panel(
    signal,
    method="rank_demean_l1",
    mask=eligible,
)
self.set_portfolio_positions(weights)
```

Required diagnostics when available:

- gross and net exposure;
- eligible symbol count;
- largest absolute weight;
- top-five concentration;
- turnover;
- long- and short-leg performance.

Market-neutral weights do not imply sector, beta, size, liquidity, or real-world shortability neutrality.

## Evidence Status

| Label | Meaning |
|---|---|
| `TEMPLATE` | Appears in an approved equity example |
| `PLATFORM` | Verify/simulate succeeded on Stage 2 |
| `CANDIDATE` | Near scoring thresholds but not fully validated |
| `PASS` | Frozen strategy passed Aggregate, Train, and Test criteria |
| `RESEARCH` | Insufficient evidence |

No parameter becomes `PASS` merely because it appears in an API signature or template.

## Research Rules

1. Start from one canonical ranking/weighting baseline.
2. Change one dimension per ablation: factor, transform, eligibility, or weighting.
3. Count every threshold and method variant in the family trial budget.
4. Do not transfer time-series EMA/RSI/rolling profiles to panel features.
5. Do not rely on hidden panel defaults as if they were chosen parameters.
6. Freeze the selected variant before opening Final OOS.
7. Never retune against the same Test period and continue calling it untouched OOS.
