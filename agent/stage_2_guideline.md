Competition Guidelines
Data Science Talent Competition: Vietnam Quant Challenge 2026 — Round 2: Fundamental Alpha Arena
Data Science Talent Competition · Platform: XNOQuant · Format: Teams of 2

1. About Round 2
Fundamental Alpha Arena is the team stage of Vietnam Quant Challenge 2026. The focus shifts from intraday futures signals in Round 1 to daily equity research on the Vietnam stock market.

Teams build point-in-time strategies that combine company fundamentals, price, and volume, along two research directions: time-series and cross-sectional.

The governing principle of this round is point-in-time discipline — a strategy may only use information that was genuinely available at the moment of the decision.

2. Timeline
Milestone	Description	Dates
Team matching	Via the CTE FTU team-matching platform	Before the round opens
In-depth training	Sessions for the Top 100 advancing participants	Start of Round 2
Strategy development & submission	Research, backtest, and Publish on XNOQuant	01/08 – 16/08/2026
Results	Top 4 teams advance	End of round
Grand Final	Offline pitching in Hanoi	Announced by the Committee
The XNOQuant event page is the source of truth for dates, submission limits, scoring settings, and prizes. Where documents disagree, the event page prevails.

3. Team Rules
Each team has 2 equal members — no team leader.
Teams are formed through the CTE FTU team-matching platform.
Members may leave a team but may not switch to another team.
Each member works on their own account; there is no shared workspace.
Team score = the sum of both members' scores.
The Round 2 leaderboard is private: each team sees only its own score. The Top 4 is announced at the end of the round.
4. Eligible Universes and Data
Only the following three universes are eligible:

Universe	Segment	Frequency
VN-SMALL-CAP	Vietnam small-cap stocks	Daily
VN-MID-CAP	Vietnam mid-cap stocks	Daily
VN-LARGE-CAP	Vietnam large-cap stocks	Daily
Strategies built on any other universe will not be scored.

Available data may include:

Daily stock OHLCV
VN30 index OHLCV (pv_vn30_*_panel)
DJI index OHLCV (pv_dji_*_panel) — cross-market reference
Universe eligibility (in_universe_panel) — boolean: investable universe gate
Income statements (quarterly and annual)
Balance sheets (quarterly and annual)
Cash-flow statements (quarterly and annual)
Field IDs use snake_case, for example: pv_close, pv_volume, pv_dji_close_panel, in_universe_panel, fun_is_net_profit_loss_after_tax_quarterly, fun_bs_total_assets_quarterly, fun_bs_owners_equity_quarterly, fun_cf_cashflow_operating_section_quarterly. Use the editor data catalog and autocomplete to confirm which fields are exposed for the selected universe.

5. Execution Modes
Each strategy must use exactly one mode.

Mode	Research question	Data shape	Position API	Position bounds
time_series	When should each stock be held?	One time series per field, per symbol	self.set_positions(...)	Long-only, within [0, +1]
cross_sectional	How should capital be allocated across stocks?	Time × symbol panel	self.set_portfolio_positions(...)	Market-neutral; both negative and positive weights allowed
Mode contract:

The exact mode name is time_series, not timeseries.
time_series fields carry no suffix: self.data.pv_close.
cross_sectional fields always carry the _panel suffix: self.data.pv_close_panel.
Do not mix series and panel fields in the same strategy.
A panel always has time on rows and symbols on columns — including for a single-symbol universe.
Supported cross-sectional operators: rank_cs_panel, demean_cs_panel, normalize_l1_cs_panel, winsorize_cs_panel, zscore_cs_panel, portfolio_weights_panel. The rank_demean_l1 method produces a market-neutral portfolio: symbols outside the universe receive weight 0, net exposure is approximately 0, and gross exposure is normalized to 1 when enough eligible stocks exist.

Supported panel features: safe_divide_panel, ema_panel, sma_panel, rolling_zscore_panel.

6. Point-in-Time Rules for Fundamental Data
Fundamental observations are aligned to the market timeline by publication date. The most recent available observation is carried forward until a newer report is published.

Requirements:

Use a report only after it was published.
Do not assume quarter-end figures were known on the quarter-end date.
Never shift fundamental data backward, and never use backfill.
Treat missing fundamentals as unavailable, not as zero.
Use ratios when comparing companies of different sizes.
Account for stale fundamentals explicitly in the research thesis.
Require .notna() and a positive denominator before constructing a ratio; do not divide by zero or by a negative denominator without an explicit economic reason.
Sector caveat: banks, insurers, securities firms, and non-financial companies follow materially different accounting conventions. Do not assume a single raw accounting ratio is comparable across every industry.

7. Strategy and Sandbox Rules
Permitted:

Signal logic that is deterministic, vectorized, and causal (past information only).
Documented primitives: self.data, self.feat, self.op.
Not permitted:

Row-by-row loops, comprehensions, lambdas, or helper functions.
Importing Pandas, NumPy, Polars, networking, or filesystem libraries.
print, open, eval, exec, or any hidden runtime access.
Negative shifts, backfill, centered rolling windows, or any future observation.
Global aggregations such as .mean(), .rank(), .quantile(), .sort_values().
In addition:

Avoid excessive rebalancing — turnover and fees directly affect the score.
The metadata docstring must state a genuine economic thesis, not a restatement of the code.
8. Scoring
The Committee automatically selects each participant's best-scoring strategies.
Team score is the sum of both members' scores.
Results are evaluated net of fees; a thin edge paired with high turnover will be penalized heavily.
Strategies must remain stable across evaluation stages (in-sample and out-of-sample). Strong results in one stage that collapse in another are treated as evidence of overfitting.
Full scoring criteria are detailed in How to Build Your Strategy on XNOQuant.
9. Pre-Submit Checklist
Check	Requirement
Universe	Uses VN-SMALL-CAP, VN-MID-CAP, or VN-LARGE-CAP
Universe gate	Uses in_universe_panel as first eligibility filter
Mode	Uses time_series or cross_sectional, never both
Fields	Uses only fields exposed for the selected universe and mode
Timing	Consumes fundamentals only after publication
Missing data	Explicitly excludes unavailable observations
Positions	Respect the bounds defined for the selected mode
Portfolio	Cross-sectional weights satisfy the market-neutral contract
Logic	Metadata explains a defensible fundamental thesis
Execution	Strategy verifies and simulates without runtime errors
Cost	Net-of-fee results survive reasonable turnover
Robustness	Results remain stable across evaluation stages
Status	Strategy reaches Published before submission
