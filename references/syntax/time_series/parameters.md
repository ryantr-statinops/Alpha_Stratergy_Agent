# Time-Series Parameter Reference (Round 2 — Daily Equity)

Tài liệu này là nguồn canonical cho parameter `time_series` Round 2. Round 2 là
daily equity (small/mid/large-cap), không dùng parameter intraday futures từ
`template_example/(Old)vnfuture/`.

Parameter được tổ chức theo **strategy archetype**, không có một cặp EMA duy
nhất phù hợp cho mọi alpha. Mọi lời gọi feature time-series phải truyền parameter
rõ ràng; không dựa vào default implementation.

> Nguồn bằng chứng: 14 equity examples trong `template_example/VN-*/`,
> `backtest/features/ma.py`, và các live simulations Stage 2. Chỉ parameter gắn
> nhãn `PASS` mới được coi là đã đạt toàn bộ scoring threshold.

## Section Index

| Group | Jump |
|---|---|
| Daily convention | [Daily Convention](#daily-convention) |
| Canonical profiles | [Canonical Parameter Profiles](#canonical-parameter-profiles) |
| Trend / MA | [Trend / Moving Average](#trend-moving-average) |
| Momentum | [Momentum / Oscillator](#momentum-oscillator) |
| Price returns | [Price-Return Confirmation](#price-return-confirmation) |
| Volume | [Volume / Flow](#volume-flow) |
| Volatility | [Volatility / Risk](#volatility-risk) |
| Fundamentals | [Persistent Fundamental Quality](#persistent-fundamental-quality) |
| Report events | [Fundamental Report Events](#fundamental-report-events) |
| Position sizing | [Position Sizing](#position-sizing) |
| Evidence | [Parameter Evidence Status](#parameter-evidence-status) |
| Research rules | [Research Rules](#research-rules) |

## Daily Convention

| Đơn vị | Daily bars |
|---|---:|
| 1 tuần | 5 |
| 1 tháng | ~21 |
| 1 quý | ~63 |
| 1 năm | ~252 |

Moving-average families ưu tiên tỷ lệ fast:slow gần `1:3`:

```text
7/21, 8/24, 10/30, 12/36, 14/42, 18/54, 30/90
```

`backtest/features/ma.py` có default EMA/SMA 30 và rolling window 20, nhưng
strategy **không được dựa vào default**. Luôn truyền `timeperiod=` hoặc `window=`.

## Canonical Parameter Profiles

### Profile A — Active Momentum

Dùng cho RSI/MACD recovery, report reaction và momentum ngắn.

| Component | Canonical value |
|---|---|
| EMA | `8/24` |
| Volume SMA | `10` |
| RSI | period `9`, entry `>48`, exit `<42`, overbought `<75` |
| MACD | `8/21/5` |
| Sizing | `0/1`, hoặc `0/0.5/1` khi có weak state rõ |

Recovery variant đã xuất hiện trong insurance examples:

```text
EMA 7/21, RSI7, entry >48, exit <42, overbought <70
```

### Profile B — Price/Volume Trend

Dùng cho pure trend, breakout và volume-confirmed momentum.

| Component | Canonical value |
|---|---|
| EMA | `10/30` |
| Volume SMA | `20` |
| Price return | `pct_change(..., periods=1)` |
| Return smoothing | `rolling_mean(..., window=3)` |
| ATR | `14` khi có vai trò risk/availability rõ |
| Sizing | `0/0.5/1` |

### Profile C — Balanced Fundamental Trend

Dùng cho EPS/profit trend, earnings yield, ROE và moderate quality.

| Component | Canonical value |
|---|---|
| EMA | `12/36` |
| Volume SMA | `20`, optional strong confirmation |
| Sizing | `0/0.5/1` |

### Profile D — Cash-Flow Quality

Dùng cho CFO, ROA, cash conversion và quality trung hạn.

| Component | Canonical value |
|---|---|
| EMA | `14/42` |
| Research variant | `18/54` |
| Volume SMA | `20`, optional |
| ATR | `14` chỉ khi có risk role |
| Sizing | `0/0.5/1` |

### Profile E — Stable Quality Hold

Dùng cho defensive quality, capital strength, stable cash flow và low-turnover
hold.

| Component | Canonical value |
|---|---|
| EMA | `30/90` |
| Volume | Không bắt buộc |
| Sizing | `0/1` hoặc persistent `0/0.5/1` |

## Trend / Moving Average

| Archetype | Fast | Slow | Typical use |
|---|---:|---:|---|
| Recovery | 7 | 21 | Fast recovery |
| Active | 8 | 24 | Momentum / active trend |
| Price-volume | 10 | 30 | Price + rolling-return confirmation |
| Balanced | 12 | 36 | Fundamental trend |
| Cash quality | 14 | 42 | Medium quality trend |
| Quality hold | 18 | 54 | Lower noise |
| Stable hold | 30 | 90 | Low turnover |

Usage:

```python
ema_fast = self.feat.ema(close, timeperiod=12)
ema_slow = self.feat.ema(close, timeperiod=36)
```

Rules:

- Không trộn period từ nhiều profile nếu không có ablation rõ ràng.
- Multi-horizon trend được phép dùng `8/24 + 12/36` khi thesis là trend
  agreement; đây là một strategy architecture, không phải default cho quality.
- Một parameter family chỉ được giữ nếu tốt trên một vùng hợp lý, không chỉ một
  điểm tối ưu đơn lẻ.

## Momentum / Oscillator

### RSI

| Mode | Period | Entry | Exit | Overbought guard |
|---|---:|---:|---:|---:|
| Active recovery | 7 | `>48` | `<42` | `<70` |
| Balanced momentum | 9 | `>48` | `<42` | `<75` |

RSI là confirmation/recovery signal, không thay thế trend core.

### MACD

Canonical parameters: `fastperiod=8`, `slowperiod=21`, `signalperiod=5`.

MACD time-series trả **ba output** và phải được unpack:

```python
macd, macd_signal, _hist = self.feat.macd(
    close,
    fastperiod=8,
    slowperiod=21,
    signalperiod=5,
)

long_signal = macd > macd_signal
exit_signal = macd < macd_signal
```

Không viết:

```python
macd = self.feat.macd(close, fastperiod=8, slowperiod=21, signalperiod=5)
long_signal = macd > 0
```

vì biến `macd` khi đó có thể là multi-output object, không phải một series.

## Price-Return Confirmation

Price return có thể fill missing bằng zero; quy tắc này **không áp dụng cho
fundamentals**.

```python
return_1 = self.op.fillna(
    self.op.pct_change(close, periods=1),
    value=0,
)
return_avg = self.feat.rolling_mean(return_1, window=3)
```

| Parameter | Canonical value |
|---|---:|
| `pct_change.periods` | 1 |
| `rolling_mean.window` | 3 |

Typical use:

- Weak trend: `return_avg > 0`.
- Strong confirmation: `return_1 > 0`.
- Exit overlay: `return_avg < 0`.

## Volume / Flow

| Profile | SMA period | Role |
|---|---:|---|
| Active/recovery | 10 | Fast participation confirmation |
| Trend/quality | 20 | Stable participation confirmation |
| Stable hold | none | Avoid unnecessary turnover |

Rules:

- Volume chỉ nên xác nhận entry hoặc full-size state.
- Không exit chỉ vì một ngày volume dưới SMA.
- Nếu strong state phụ thuộc volume hàng ngày, phải kiểm tra churn `0.5 ↔ 1.0`.
- Không thêm volume nếu ablation làm Sharpe/Calmar giảm.

## Volatility / Risk

| Feature | Parameter | Canonical value |
|---|---|---:|
| ATR | `timeperiod` | 14 |

ATR chỉ được dùng khi có vai trò rõ:

- Availability/range validity.
- Volatility regime.
- Position/risk adjustment.
- Stop distance.

`atr > 0` chỉ là availability guard, không phải alpha hoặc volatility filter.

## Persistent Fundamental Quality

Persistent quality là state kéo dài giữa hai report và nên được dùng làm
eligibility filter.

| Factor | Baseline | Research range | Notes |
|---|---:|---:|---|
| ROA | `>0` | `0`, `0.01`, `0.02` | Denominator assets phải dương |
| Cash conversion | `>0.5` | `0.5`, `0.75`, `1.0` | CFO và net profit phải dương |
| Operating cash flow | `>0` | fixed | Ý nghĩa khác nhau theo sector |
| Net profit | `>0` | fixed | Availability/quality guard |
| Equity/assets | sector-specific | none global | Không dùng một hard threshold xuyên ngành |

Ratio guard chuẩn:

```python
ratio = numerator / denominator
available = (
    self.op.notna(numerator)
    & self.op.notna(denominator)
    & (denominator > 0)
    & self.op.notna(ratio)
)
```

Sector rules:

- Non-financial: CFO/net profit, ROA, cash return phù hợp hơn.
- Bank: tránh CFO generic làm hard requirement.
- Insurance: premium, claims, insurance/investment profit.
- Securities: fee, commission, derivatives/FVTPL income, expense pressure.

## Fundamental Report Events

Fundamentals daily-aligned chỉ đổi khi report mới được công bố. `pct_change`
trên fundamental là report event, không phải daily growth và không phải
persistent quality state.

```python
profit_growth = self.op.pct_change(net_profit, periods=1)
report_known = self.op.notna(net_profit) & self.op.notna(profit_growth)
positive_event = report_known & (net_profit > 0) & (profit_growth > 0)
```

Không dùng:

```python
self.op.fillna(self.op.pct_change(net_profit, periods=1), value=0)
```

vì missing fundamental là unavailable, không phải zero growth.

| Event role | Canonical threshold | Notes |
|---|---:|---|
| Loose report guard | `> -0.02` | Chỉ khi current/base sign hợp lệ |
| Positive event | `> 0` | Strong/event overlay |
| Material deterioration | `< -0.05` | Không dùng cho noisy sign changes |
| High-noise sector fields | `-0.05 / -0.15` | Insurance/sector-specific only |

Cấu trúc entry 3 tầng (weak → strong → exit) dùng ngay các band này:
loose guard giữ coverage, positive tier xác nhận, negative band mới exit:

```python
weak_long = quality & (profit_growth > -0.02)
strong_long = weak_long & (profit_growth > 0)
exit_setup = quality_failure | (profit_growth < -0.05)

self.set_positions(exit_setup, position=0)
self.set_positions(weak_long, position=0.5)
self.set_positions(strong_long, position=1)
```

Với EPS/profit có thể âm hoặc đổi dấu, raw `pct_change` có thể đảo nghĩa. Ưu
tiên positive-level guard hoặc delta được scale bằng assets/equity dương.

## Position Sizing

| State | Position | Status |
|---|---:|---|
| Flat | 0 | Canonical |
| Reduced weak state | 0.25 | Research; chỉ giữ khi ablation chứng minh |
| Standard base | 0.5 | Canonical default |
| Full confirmation | 1.0 | Canonical |

Rules:

- Default tiered sizing là `0/0.5/1`.
- `0.25` không phải global default; dùng khi weak regime được chứng minh gây
  nhiễu. Live research hiện chỉ ủng hộ nó cho một ROA variant.
- Không mặc định binary full-only; Stage 2 ablation cho thấy cách này có thể
  giảm CAGR mà không nâng Sharpe đủ.
- `time_series` luôn long-only `[0,1]`.

## Parameter Evidence Status

| Label | Meaning |
|---|---|
| `TEMPLATE` | Xuất hiện trong equity examples |
| `PLATFORM` | Verify/simulate thành công trên Stage 2 platform |
| `CANDIDATE` | Gần đạt scoring threshold |
| `PASS` | Strategy dùng parameter đã đạt toàn bộ threshold |
| `RESEARCH` | Chưa đủ bằng chứng |

Current evidence:

| Parameter/profile | Evidence |
|---|---|
| EMA 7/21 | `TEMPLATE` |
| EMA 8/24 | `TEMPLATE`, `PLATFORM`, `CANDIDATE` |
| EMA 10/30 | `TEMPLATE`, `PLATFORM` |
| EMA 12/36 | `TEMPLATE`, `PLATFORM` |
| EMA 14/42 | `TEMPLATE`, `RESEARCH` |
| EMA 18/54 | `TEMPLATE`, `RESEARCH` |
| EMA 30/90 | `TEMPLATE`, `RESEARCH` |
| MACD 8/21/5 | `TEMPLATE`; runtime contract phải unpack outputs |
| RSI 7/9 | `TEMPLATE`, `PLATFORM` |
| ATR14 | `TEMPLATE`, `PLATFORM` |
| Volume SMA10/20 | `TEMPLATE`, `PLATFORM` |
| ROA >0 + EMA8/24 + weak 0.25 | `PLATFORM`, `CANDIDATE` |

Hiện chưa có profile nào được gắn nhãn `PASS`.

## Research Rules

1. Chọn profile theo strategy archetype trước khi code.
2. Baseline phải dùng canonical profile, sau đó mới thử adjacent profile.
3. Mỗi iteration chỉ đổi một dimension: period, threshold, sizing hoặc exit.
4. Không tối ưu đồng thời nhiều parameter.
5. Parameter robustness test theo family hợp lý, không random grid.
6. Chỉ giữ thay đổi nếu cải thiện risk-adjusted metrics mà không phá thesis.
7. Ghi lại và loại code variant không cải thiện; không để CSV trỏ tới code cũ.
8. Không đảo signal chỉ để cứu một backtest.
9. Không dùng parameter futures/session cho daily equity.
10. Sau mỗi change: strict validate → live simulate → so với exact baseline.

## Forbidden Parameter Practices

- Dựa vào implicit/default `timeperiod` hoặc `window`.
- Dùng cùng một EMA family cho mọi archetype.
- Dùng `fillna(..., 0)` cho missing fundamentals.
- Dùng raw `pct_change` quanh sign-changing fundamentals mà không guard.
- Dùng global capital-ratio threshold xuyên mọi sector.
- Dùng volume hoặc ATR như điều kiện trang trí không có economic role.
- Gắn nhãn `PASS` cho parameter chỉ vì xuất hiện trong template.
