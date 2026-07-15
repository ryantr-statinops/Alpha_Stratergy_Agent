# Data Syntax Reference

Use this file as the canonical catalog for `self.data.*`.

## Quick Lookup

| Group | Typical use | Representative fields |
|---|---|---|
| Core OHLCV | base price/volume input | `pv_open`, `pv_high`, `pv_low`, `pv_close`, `pv_volume` |
| VN30 Index | cross-market confirmation | `pv_vn30_open`, `pv_vn30_high`, `pv_vn30_low`, `pv_vn30_close`, `pv_vn30_volume` |
| Dow Jones | global spillover filter | `pv_dji_open`, `pv_dji_high`, `pv_dji_low`, `pv_dji_close`, `pv_dji_volume` |
| Futures Daily | futures participation / flow | `fut_matched_volume_vn30f1m_1d`, `fut_matched_value_vn30f1m_1d`, `fut_agreed_volume_vn30f1m_1d`, `fut_agreed_value_vn30f1m_1d`, `fut_total_volume_vn30f1m_1d`, `fut_total_value_vn30f1m_1d`, `fut_open_interest_vn30f1m_1d` |

## Reading Tips

- Start with Core OHLCV for almost every strategy.
- Use VN30 and DJI when building cross-market or regime-filter logic.
- Use futures daily fields when you need open interest, matched volume, or flow confirmation.
- Keep the field names exactly as written in code; do not rename them into custom aliases in the docs.

## Core OHLCV

| Field | Meaning | Common use |
|---|---|---|
| `pv_open` | session open | intraday session logic, gap style setups |
| `pv_high` | session high | breakout, ATR, range logic |
| `pv_low` | session low | breakout, ATR, range logic |
| `pv_close` | session close | default price input for most indicators |
| `pv_volume` | traded volume | flow confirmation, participation filter |

## VN30 Index

| Field | Meaning | Common use |
|---|---|---|
| `pv_vn30_open` | VN30 open | cross-market trend alignment |
| `pv_vn30_high` | VN30 high | regime confirmation |
| `pv_vn30_low` | VN30 low | regime confirmation |
| `pv_vn30_close` | VN30 close | relative strength, confirmation |
| `pv_vn30_volume` | VN30 volume | market breadth / participation proxy |

## Dow Jones Index

| Field | Meaning | Common use |
|---|---|---|
| `pv_dji_open` | DJI open | global risk-on / risk-off context |
| `pv_dji_high` | DJI high | global regime confirmation |
| `pv_dji_low` | DJI low | global regime confirmation |
| `pv_dji_close` | DJI close | spillover / alignment filter |
| `pv_dji_volume` | DJI volume | optional context proxy |

## Futures Daily Fields

| Field | Meaning | Common use |
|---|---|---|
| `fut_matched_volume_vn30f1m_1d` | matched volume | participation and liquidity filter |
| `fut_matched_value_vn30f1m_1d` | matched value | turnover confirmation |
| `fut_agreed_volume_vn30f1m_1d` | agreed volume | negotiated flow context |
| `fut_agreed_value_vn30f1m_1d` | agreed value | negotiated flow context |
| `fut_total_volume_vn30f1m_1d` | total volume | combined flow signal |
| `fut_total_value_vn30f1m_1d` | total value | combined flow signal |
| `fut_open_interest_vn30f1m_1d` | open interest | positioning / regime proxy |

## Usage Notes

- `self.data.*` is the raw data layer. Do not invent extra field names in generated code.
- For most strategies, `pv_close` is the default input; other fields are contextual filters.
- For intraday session work, prefer `pv_open`, `pv_high`, `pv_low`, `pv_close`, `pv_volume`.
- For cross-market work, prefer `pv_vn30_*` and `pv_dji_*` as confirmation signals.
