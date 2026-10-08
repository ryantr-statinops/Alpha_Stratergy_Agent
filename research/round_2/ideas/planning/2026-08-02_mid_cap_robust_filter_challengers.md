# MID-CAP Robust Filter Challengers

Objective: improve OOS stability and reduce portfolio breadth without modifying
the ten aggregate-pass MID strategies during the initial experiment. A later
split audit established that none of those strategies is a true OOS PASS.

## Validated active filter stack

1. Top-70% rolling traded value (`liquidity_rank > 0.30`).
2. Exclude the highest 5% NATR (`volatility_rank < 0.95`).
3. Exclude the highest 5% Amihud illiquidity (`illiquidity_rank < 0.95`).
4. No tail signal mask, `winsorize_cs_panel`, or `max_abs_weight`.

The first runtime probe is `VnMidCsEnterpriseEarningsYieldRobust.py`. The strict
tail version reduced CAGR to 11.4%, so the active challenger keeps top-70%
liquidity and removes only the highest 5% NATR/Amihud names. Existing
aggregate-pass files remained unchanged and were not included in submit commands.

## Enterprise result

| Variant | CAGR | Sharpe | Calmar | MaxDD | PF |
|---|---:|---:|---:|---:|---:|
| Enterprise robust final | .2166 | 1.1744 | 1.3103 | -.1653 | 1.3152 |
| Original Enterprise | .2549 | 1.3258 | 1.4507 | -.1757 | 1.3515 |

The final robust filter reduced drawdown but did not improve CAGR, Sharpe, Calmar,
or profit factor. It is not evidence of proven OOS robustness.

The split audit confirms failure: Test CAGR 0.92%, Sharpe 0.129, Calmar 0.088,
MaxDD -10.56%, and PF 1.028. The robust filter therefore does not pass the MID
Test/OOS hurdle.

## Yearly stability proxy

| Year | Original CAGR / Sharpe / MaxDD | Robust CAGR / Sharpe / MaxDD |
|---|---:|---:|
| 2020 | 86.9% / 3.92 / -7.9% | 74.7% / 3.68 / -5.7% |
| 2021 | 20.3% / 0.84 / -17.2% | 25.4% / 1.07 / -15.6% |
| 2022 | 89.9% / 1.81 / -20.2% | 52.5% / 1.15 / -22.9% |
| 2023 | 17.2% / 0.62 / -37.0% | 12.9% / 0.57 / -31.8% |
| 2024 | -7.0% / -0.27 / -25.2% | -0.6% / -0.03 / -12.3% |

The robust variant materially improves 2024 defense and reduces drawdown in
2020, 2021, 2023, and 2024. It sacrifices a large part of the 2022 upside, so it
is a defensive challenger rather than a replacement proven by aggregate metrics.

## Rejected challengers

- Internally Funded Investment robust: final CAGR 22.74%, Sharpe 1.203, Calmar
  0.934, MaxDD -24.35%, PF 1.305. Failed Calmar.
- Recognition Migration robust: final CAGR 21.20%, Sharpe 1.138, Calmar 0.896,
  MaxDD -23.67%, PF 1.289. Failed Calmar.

Both files were removed from the active manifest. Their historical result rows
remain append-only for auditability.

## Active recommendation

Keep `VnMidCsEnterpriseEarningsYieldRobust.py` only as a failed research reference,
not an allocation candidate. The original ten aggregate-pass strategies also
remain failed research references because they share the same return engine and
all fail Test/OOS.
